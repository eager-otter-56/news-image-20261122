#!/usr/bin/env python3
"""Deliver this entry's poster image to the grading output directory.

The competition runner mounts the repository read-only and points
MAKEFUN_BOT_DIR at it and MAKEFUN_OUTPUT_DIR at a writable directory.
This script copies the entry.png stored beside it into the output
directory, atomically: the copy is staged on a temporary file inside
the output directory, verified against the source by SHA-256, moved
into place with os.replace, and finally chmod'ed to 0644 (a bare
mkstemp file is 0600, which the grader cannot read).
"""

import hashlib
import os
import sys
import tempfile

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def source_path() -> str:
    bot_dir = os.environ.get("MAKEFUN_BOT_DIR")
    base = bot_dir if bot_dir else os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "entry.png")


def output_path() -> str:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.getcwd()
    return os.path.join(out_dir, "entry.png")


def sha256_of(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    src = source_path()
    dst = output_path()
    out_dir = os.path.dirname(dst)

    with open(src, "rb") as fh:
        data = fh.read()
    if not data.startswith(PNG_SIGNATURE):
        print(f"error: {src} is not a PNG file", file=sys.stderr)
        return 1
    want = sha256_of(data)

    os.makedirs(out_dir, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        with open(tmp, "rb") as fh:
            staged = fh.read()
        if sha256_of(staged) != want:
            print("error: staged copy failed SHA-256 verification", file=sys.stderr)
            return 1
        os.replace(tmp, dst)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise
    os.chmod(dst, 0o644)
    # Verify what was actually delivered, not just what was staged:
    # a short write or a racing mount must never pass silently.
    with open(dst, "rb") as fh:
        delivered = fh.read()
    if sha256_of(delivered) != want or len(delivered) != len(data):
        print("error: delivered file failed SHA-256 verification", file=sys.stderr)
        return 1
    print(f"wrote {dst} ({len(data)} bytes, sha256 {want})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

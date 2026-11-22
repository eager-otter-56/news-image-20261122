#!/usr/bin/env python3
"""Entry point for the news-image-20261122 trial-design entry.

Copies the entry.png stored beside this script into the output
directory (MAKEFUN_OUTPUT_DIR, or the current working directory when
that variable is unset), then makes sure the copy is readable by
everyone, as the grader mounts the repository read-only and runs
this script as an unprivileged user.
"""

import hashlib
import os
import sys
import tempfile

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def source_path() -> str:
    """Locate the bundled entry.png: MAKEFUN_BOT_DIR wins, else the
    directory holding this script."""
    bot_dir = os.environ.get("MAKEFUN_BOT_DIR")
    if bot_dir:
        return os.path.join(bot_dir, "entry.png")
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def output_path() -> str:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.getcwd()
    return os.path.join(out_dir, "entry.png")


def digest(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    src = source_path()
    dst = output_path()

    with open(src, "rb") as fh:
        head = fh.read(len(PNG_SIGNATURE))
    if head != PNG_SIGNATURE:
        print(f"error: {src} is not a PNG file", file=sys.stderr)
        return 1

    # Atomic write: stream into a temp file inside the output
    # directory itself (never beside this script — the repository
    # mount may be read-only), verify it, then rename over the
    # destination so a grader never sees a partial entry.png.
    out_dir = os.path.dirname(dst)
    fd, tmp = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as out_fh, open(src, "rb") as in_fh:
            for chunk in iter(lambda: in_fh.read(65536), b""):
                out_fh.write(chunk)
        if digest(src) != digest(tmp):
            print("error: copied file failed sha256 verification", file=sys.stderr)
            return 1
        os.replace(tmp, dst)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)

    os.chmod(dst, 0o644)
    print(f"wrote {dst} ({os.path.getsize(dst)} bytes, sha256 {digest(dst)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

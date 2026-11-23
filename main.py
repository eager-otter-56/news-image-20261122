#!/usr/bin/env python3
"""Deliver this entry's poster image.

Copies entry.png from the bot directory (MAKEFUN_BOT_DIR when set,
otherwise the directory holding this script) into the output directory
(MAKEFUN_OUTPUT_DIR when set, otherwise the current working directory).
The copy lands through a temporary file inside the output directory, is
verified by SHA-256, moved into place with os.replace and chmod 0644.
No network access; works from a read-only repository as an unprivileged
user. Exits non-zero on any failure.
"""

import hashlib
import os
import sys
import tempfile

IMAGE_NAME = "entry.png"


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    bot_dir = os.environ.get("MAKEFUN_BOT_DIR") or os.path.dirname(
        os.path.abspath(__file__)
    )
    source = os.path.join(bot_dir, IMAGE_NAME)
    if not os.path.isfile(source):
        print(f"error: {source} not found", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.getcwd()
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, IMAGE_NAME)
    expected = sha256_of(source)

    fd, tmp_path = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as out:
            with open(source, "rb") as src:
                for chunk in iter(lambda: src.read(65536), b""):
                    out.write(chunk)
        if sha256_of(tmp_path) != expected:
            print("error: copy failed SHA-256 verification", file=sys.stderr)
            return 1
        os.replace(tmp_path, target)
        os.chmod(target, 0o644)
    except OSError as exc:
        print(f"error: delivery failed: {exc}", file=sys.stderr)
        return 1
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

    # Re-read what actually landed in the output directory: the delivery
    # only counts if the file on disk there matches the source exactly.
    if sha256_of(target) != expected:
        print("error: delivered file failed SHA-256 verification", file=sys.stderr)
        return 1
    print(f"delivered {target} (sha256 {expected})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

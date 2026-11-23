#!/usr/bin/env python3
"""Deliver the finished poster for the news-image-20261122 entry.

The grading harness mounts this repository read-only, so this script never
writes anything next to itself. It reads the entry.png that ships beside it
(or under MAKEFUN_BOT_DIR when that variable is set) and places a verified
copy, also named entry.png, in the output directory.
"""

import hashlib
import os
import shutil
import sys
import tempfile

IMAGE_NAME = "entry.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
READ_CHUNK = 1 << 20


def source_image() -> str:
    """Path of the entry.png bundled with this entry."""
    bot_dir = os.environ.get("MAKEFUN_BOT_DIR")
    base = bot_dir if bot_dir else os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, IMAGE_NAME)


def target_dir() -> str:
    """Directory the delivered image belongs in."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or os.getcwd()


def sha256_of(path: str) -> str:
    """Hex sha256 digest of a file, read in blocks."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            block = handle.read(READ_CHUNK)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def looks_like_png(path: str) -> bool:
    """True when the file starts with the PNG signature."""
    with open(path, "rb") as handle:
        return handle.read(len(PNG_MAGIC)) == PNG_MAGIC


def main() -> int:
    src = source_image()
    if not os.path.isfile(src):
        print(f"error: source image missing: {src}", file=sys.stderr)
        return 1
    if not looks_like_png(src):
        print(f"error: {src} does not start with a PNG signature",
              file=sys.stderr)
        return 1

    out_dir = target_dir()
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, IMAGE_NAME)
    wanted = sha256_of(src)

    # Stage the copy on a temp file inside the output directory itself, so
    # the final os.replace is an atomic rename on the same filesystem.
    fd, staging = tempfile.mkstemp(dir=out_dir, prefix=".entry-",
                                   suffix=".part")
    try:
        with os.fdopen(fd, "wb") as out:
            with open(src, "rb") as inp:
                shutil.copyfileobj(inp, out)
        if sha256_of(staging) != wanted:
            print("error: staged copy differs from the source",
                  file=sys.stderr)
            return 1
        os.replace(staging, dest)
    except BaseException:
        try:
            os.unlink(staging)
        except OSError:
            pass
        raise

    # mkstemp leaves the file at 0600, which the grader cannot read.
    os.chmod(dest, 0o644)

    if sha256_of(dest) != wanted:
        print("error: delivered image failed its final check",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except OSError as exc:
        # A read-only source tree or an unwritable output directory should
        # surface as a plain failure message, not a traceback.
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)

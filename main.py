#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261122.

Publishes the entry.png sitting beside this file to /output/entry.png
with an atomic, self-checking copy: the bytes are first written to a
temporary file inside /output, read back and verified against the
source (same length, and starting with the PNG signature), and only
then moved onto /output/entry.png with os.replace, so a reader never
sees a half-written file and a corrupt copy never lands. No network,
no randomness: every run writes the same bytes.
"""
import os
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST_DIR = "/output"
DST = os.path.join(DST_DIR, "entry.png")


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def main():
    os.makedirs(DST_DIR, exist_ok=True)
    with open(SRC, "rb") as f:
        data = f.read()

    # Stage the copy in a temp file inside /output, then verify what
    # actually landed on disk before publishing it atomically.
    fd, tmp = tempfile.mkstemp(dir=DST_DIR, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        with open(tmp, "rb") as f:
            copied = f.read()
        if len(copied) != len(data):
            raise ValueError(
                "copied length %d does not match source length %d"
                % (len(copied), len(data))
            )
        if not copied.startswith(PNG_SIGNATURE):
            raise ValueError("copied bytes do not start with the PNG signature")
        os.replace(tmp, DST)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise
    os.chmod(DST, 0o644)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261122.

Copies the entry.png sitting beside this file to /output/entry.png,
byte for byte. No network, no randomness: every run writes the
same bytes.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST_DIR = "/output"
DST = os.path.join(DST_DIR, "entry.png")


def main():
    os.makedirs(DST_DIR, exist_ok=True)
    with open(SRC, "rb") as f:
        data = f.read()
    with open(DST, "wb") as f:
        f.write(data)
    os.chmod(DST, 0o644)


if __name__ == "__main__":
    main()

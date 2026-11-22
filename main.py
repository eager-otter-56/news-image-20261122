#!/usr/bin/env python3
"""Write the entry poster (entry.png, stored beside this file) into the
output directory: MAKEFUN_OUTPUT_DIR if set, else the working directory.

The copy is atomic and verified: the bytes are written to a temp file
inside the output directory (never beside this script — the grading
mount is read-only), the temp file's sha256 is checked against the
source, and only then is it moved into place and made world-readable.
"""
import hashlib
import os
import sys
import tempfile
from pathlib import Path


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    here = Path(os.environ.get("MAKEFUN_BOT_DIR") or Path(__file__).resolve().parent)
    src = here / "entry.png"
    if not src.is_file():
        print(f"entry.png not found beside main.py (looked in {here})", file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or Path.cwd())
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "entry.png"

    want = sha256_of(src)
    fd, tmp_name = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    tmp = Path(tmp_name)
    try:
        with os.fdopen(fd, "wb") as dst, src.open("rb") as fh:
            while True:
                chunk = fh.read(1 << 20)
                if not chunk:
                    break
                dst.write(chunk)
            dst.flush()
            os.fsync(dst.fileno())
        if sha256_of(tmp) != want:
            print("sha256 mismatch after copy; refusing to publish", file=sys.stderr)
            return 1
        os.replace(tmp, out)
    finally:
        if tmp.exists():
            tmp.unlink()
    os.chmod(out, 0o644)
    print(f"wrote {out} ({out.stat().st_size} bytes, sha256 {want})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

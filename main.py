"""Copy the bundled entry.png into the make.fun output directory.

The poster image lives beside this file. Grading runs this script from a
read-only directory, so nothing is ever written next to main.py: the
temporary file is created inside the output directory and atomically
moved into place as entry.png.
"""

import hashlib
import os
import shutil
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.getcwd()
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "entry.png")
    fd, tmp = tempfile.mkstemp(prefix=".entry-", dir=out_dir)
    try:
        with os.fdopen(fd, "wb") as f:
            with open(SRC, "rb") as src:
                shutil.copyfileobj(src, f)
        # Verify the copy before it becomes the deliverable: same byte
        # length, a valid PNG signature, and an identical sha256.
        if os.path.getsize(tmp) != os.path.getsize(SRC):
            raise ValueError("entry.png copy has the wrong byte length")
        with open(tmp, "rb") as f:
            if f.read(len(PNG_SIGNATURE)) != PNG_SIGNATURE:
                raise ValueError("entry.png copy is not a PNG file")
        if _sha256(tmp) != _sha256(SRC):
            raise ValueError("entry.png copy failed its sha256 check")
        os.replace(tmp, out)
        os.chmod(out, 0o644)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


if __name__ == "__main__":
    main()

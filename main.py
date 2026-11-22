"""Copy the bundled entry.png poster to the output directory.

The poster (entry.png, 1024x1024) sits next to this file. Running this
script writes it to the directory named by the MAKEFUN_OUTPUT_DIR
environment variable, or to the current working directory when that
variable is not set. No network access is needed and the output is
byte-for-byte identical to the bundled poster on every run.
"""

import hashlib
import os
import tempfile

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    with open(src, "rb") as fh:
        data = fh.read()
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("bundled entry.png is not a PNG file")
    expected = hashlib.sha256(data).hexdigest()

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.getcwd()
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "entry.png")

    # Write to a temp file inside the output directory, verify it, then
    # move it into place atomically so a partial file is never visible.
    fd, tmp = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        with open(tmp, "rb") as fh:
            written = fh.read()
        if len(written) != len(data):
            raise IOError("short write while copying entry.png")
        if hashlib.sha256(written).hexdigest() != expected:
            raise IOError("copy verification failed for entry.png")
        os.replace(tmp, out)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise
    # mkstemp creates the temp file with mode 0600, and os.replace keeps
    # that mode; make the delivered poster world-readable as required.
    os.chmod(out, 0o644)
    print("wrote", out)


if __name__ == "__main__":
    main()

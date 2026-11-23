#!/usr/bin/env python3
"""NI22 v11 entrypoint — stdlib-only copier.

Copies entry.png to /output/entry.png (or $MAKEFUN_OUTPUT_DIR), verifying
the PNG signature and the 1 MiB size cap. Never imports draw.py (the
build tool). Deterministic: byte-identical output on every run.
"""
import hashlib
import os
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    dst = os.path.join(outdir, "entry.png")
    with open(src, "rb") as f:
        data = f.read()
    assert data[:8] == PNG_MAGIC, "entry.png is not a PNG"
    assert len(data) <= MAX_BYTES, "entry.png over 1 MiB: %d bytes" % len(data)
    with open(dst, "wb") as f:
        f.write(data)
    print("entry.png: %d bytes, sha256 %s"
          % (len(data), hashlib.sha256(data).hexdigest()))


if __name__ == "__main__":
    sys.exit(main())

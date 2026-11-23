#!/usr/bin/env python3
"""NI22 v7 entrypoint: copy entry.png to the output directory.

Standard library only. Never imports draw.py. Validates the PNG signature
and the 1 MiB size cap, then copies the bytes unchanged.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
PNG_SIG = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    with open(SRC, "rb") as f:
        data = f.read()
    if data[:8] != PNG_SIG:
        print("entry.png is not a PNG", file=sys.stderr)
        return 1
    if len(data) > MAX_BYTES:
        print("entry.png exceeds 1 MiB", file=sys.stderr)
        return 1
    dst = os.path.join(out_dir, "entry.png")
    with open(dst, "wb") as f:
        f.write(data)
    print("copied %d bytes to %s" % (len(data), dst))
    return 0


if __name__ == "__main__":
    sys.exit(main())

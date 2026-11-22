#!/usr/bin/env python3
"""NI22 entrypoint: copy entry.png to the output directory.

Standard library only. Verifies the PNG signature and the 1 MiB size cap
before writing, so a corrupt or oversized image fails loudly instead of
reaching the gate.
"""
import os
import shutil
import sys

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    dst = os.path.join(out_dir, "entry.png")

    with open(src, "rb") as f:
        head = f.read(len(PNG_SIGNATURE))
    if head != PNG_SIGNATURE:
        print("entry.png: bad PNG signature", file=sys.stderr)
        return 1
    size = os.path.getsize(src)
    if size > MAX_BYTES:
        print("entry.png: %d bytes exceeds 1 MiB" % size, file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)
    print("wrote %s (%d bytes)" % (dst, size))
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""make.fun entry for news-image-20261124.

The grader runs this program twice in a sandbox with no network: the
repository is mounted read-only at /bot and /output is writable.
The entry image (entry.png, built by build_image.py) is copied to
/output/entry.png, byte for byte, so both runs write identical bytes.

Local run:  MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def main():
    # /output in the grader, MAKEFUN_OUTPUT_DIR locally
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, target)
    size = os.path.getsize(target)
    print(f"wrote {target} ({size} bytes)")


if __name__ == "__main__":
    main()

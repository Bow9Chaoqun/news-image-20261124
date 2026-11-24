#!/usr/bin/env python3
"""Entry program for make.fun's news-image-20261124 bounty.

In the grading sandbox the repository is read-only and /output is the
only writable place. This program copies the pre-built entry.png next
to it into the output folder, unchanged, so two runs agree byte for
byte. Locally, set MAKEFUN_OUTPUT_DIR to choose the destination.
"""

import os
import shutil
from pathlib import Path


def destination_dir():
    # the grader sets no variable, so this falls back to /output
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def run():
    source_png = Path(__file__).resolve().with_name("entry.png")
    target_dir = destination_dir()
    target_dir.mkdir(parents=True, exist_ok=True)
    target_png = target_dir / "entry.png"
    shutil.copyfile(source_png, target_png)
    print("wrote", target_png, target_png.stat().st_size, "bytes")


if __name__ == "__main__":
    run()

#!/usr/bin/env python3
"""Sum up 25 November's world news in one image.

Entry for make.fun bounty news-image-20261125:
"Sum up 25 November's world news in one image" ($100 USDC).

The image is drawn by draw.py (Pillow, run where Pillow and the
DejaVu fonts are installed) and stored in this repository as
entry.png. This program only copies it to the output directory,
using the Python standard library alone, so it runs in the
grader's sandbox exactly as it runs anywhere else: no network,
no third-party packages, no fonts, no randomness, no timestamps.
Copying bytes means both runs write byte-identical output.

Run:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
    # writes out/entry.png (1024x1024, PNG, under 1 MiB)
In the grader, MAKEFUN_OUTPUT_DIR is unset and the image goes to
/output/entry.png.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def build():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, path)
    return path


if __name__ == "__main__":
    print(build())

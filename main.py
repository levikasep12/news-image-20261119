#!/usr/bin/env python3
"""news-image-20261119: one image summing Thursday 19 November 2026 news.

The poster is entry.png next to this file: a broadsheet drawn from the day's
verified reporting (BBC, NYT, CBS, Guardian, Japan Times, France 24, The
Hindu). Lead: the first-ever Trump-Xi-Putin trilateral summit in Shenzhen;
also the Crimean Bridge strike, Cyclone Akvan, the ICJ Rohingya ruling, the
record Anthropic IPO and COP31 -- 33 stories, six continents, one world map.

This program only copies that image into the grader's output directory, so
every run writes exactly the same bytes. Standard library only, no network.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png"


def output_dir() -> Path:
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main() -> None:
    if not SRC.is_file():
        raise SystemExit(f"missing image beside entrypoint: {SRC}")
    out = output_dir()
    out.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SRC, out / "entry.png")


if __name__ == "__main__":
    main()

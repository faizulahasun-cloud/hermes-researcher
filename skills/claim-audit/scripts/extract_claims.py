#!/usr/bin/env python3
"""Split a draft into claim-like sentences. Deterministic."""

from __future__ import annotations

import re
import sys
from pathlib import Path

_SPLIT = re.compile(r"(?<=[.!?])\s+")
_HEDGE = re.compile(r"\b(I think|maybe|perhaps|might)\b", re.I)


def main() -> int:
    if len(sys.argv) < 2:
        text = sys.stdin.read()
    else:
        text = Path(sys.argv[1]).read_text(encoding="utf-8")
    for sentence in _SPLIT.split(text):
        line = sentence.strip()
        if len(line) < 20:
            continue
        if line.startswith("#") or line.startswith("|"):
            continue
        if _HEDGE.search(line) and len(line) < 40:
            continue
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

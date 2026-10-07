#!/usr/bin/env python3
"""Classify a knob tag from boolean evidence. No network."""

from __future__ import annotations

import argparse
import json
import sys


def classify(has_url: bool, pages_agree: bool, mentioned: bool) -> str:
    if has_url and mentioned and pages_agree:
        return "DOC"
    if mentioned and not has_url:
        return "INF"
    return "UNV"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--has-url", choices=("true", "false"), required=True)
    parser.add_argument("--pages-agree", choices=("true", "false"), required=True)
    parser.add_argument("--mentioned", choices=("true", "false"), default="true")
    args = parser.parse_args(argv[1:])
    tag = classify(
        args.has_url == "true",
        args.pages_agree == "true",
        args.mentioned == "true",
    )
    print(json.dumps({"tag": tag}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

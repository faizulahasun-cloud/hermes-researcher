#!/usr/bin/env python3
"""Canonicalize and dedupe URLs. Deterministic. No model."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

_TRACKING = frozenset(
    {
        "utm_source",
        "utm_medium",
        "utm_campaign",
        "utm_term",
        "utm_content",
        "fbclid",
        "gclid",
        "mc_cid",
        "mc_eid",
    }
)


def canonicalize(url: str) -> str:
    raw = (url or "").strip()
    if not raw:
        return ""
    if "://" not in raw and raw.startswith("www."):
        raw = "https://" + raw
    parsed = urlparse(raw)
    if not parsed.scheme:
        return raw.rstrip("/")
    host = (parsed.hostname or "").lower()
    if host.startswith("m."):
        host = host[2:]
    query = [
        (key, value)
        for key, value in parse_qsl(parsed.query, keep_blank_values=True)
        if key.lower() not in _TRACKING
    ]
    path = parsed.path or ""
    if path.endswith("/") and path != "/":
        path = path.rstrip("/")
    return urlunparse(
        (
            parsed.scheme.lower(),
            host + (f":{parsed.port}" if parsed.port else ""),
            path,
            "",
            urlencode(query, doseq=True),
            "",
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Dedupe URLs by canonical form.")
    parser.add_argument("paths", nargs="*", help="Files of URLs, one per line. stdin if omitted.")
    args = parser.parse_args()
    lines: list[str] = []
    if args.paths:
        for path in args.paths:
            lines.extend(Path(path).read_text(encoding="utf-8").splitlines())
    else:
        lines.extend(sys.stdin.read().splitlines())
    seen: dict[str, str] = {}
    for raw in lines:
        url = raw.strip()
        if not url or url.startswith("#"):
            continue
        key = canonicalize(url) or url
        seen.setdefault(key, url)
    for url in seen.values():
        print(url)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

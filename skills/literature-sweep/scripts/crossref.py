#!/usr/bin/env python3
"""Crossref HTTP lookup. Uses CROSSREF_MAILTO when set."""

from __future__ import annotations

import json
import os
import sys
import urllib.parse
import urllib.request
from typing import Any


def crossref_fields(item: dict[str, Any]) -> dict[str, Any]:
    authors: list[str] = []
    for row in item.get("author") or []:
        if not isinstance(row, dict):
            continue
        name = " ".join(
            part for part in (str(row.get("given") or ""), str(row.get("family") or "")) if part
        ).strip()
        if name:
            authors.append(name)
    issued = ((item.get("issued") or {}).get("date-parts") or [[]])[0]
    published = None
    if isinstance(issued, list) and issued:
        if len(issued) >= 3:
            published = f"{int(issued[0]):04d}-{int(issued[1]):02d}-{int(issued[2]):02d}"
        elif len(issued) >= 2:
            published = f"{int(issued[0]):04d}-{int(issued[1]):02d}"
        else:
            published = str(issued[0])
    containers = item.get("container-title") or []
    return {
        "authors": authors,
        "published": published,
        "container": str(containers[0]) if containers else "",
        "publisher": str(item.get("publisher") or ""),
    }


def main() -> int:
    query = " ".join(sys.argv[1:]).strip()
    if not query:
        print(json.dumps({"error": "query required"}))
        return 1
    params = {"query": query, "rows": "8"}
    mailto = os.environ.get("CROSSREF_MAILTO") or ""
    if mailto:
        params["mailto"] = mailto
    url = "https://api.crossref.org/works?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(url, headers={"User-Agent": "hdr-research-bot/2.0"})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"error": str(exc)}))
        return 1
    items = (((payload or {}).get("message") or {}).get("items")) or []
    rows = []
    for item in items:
        if not isinstance(item, dict):
            continue
        title = (item.get("title") or ["Untitled"])[0]
        doi = item.get("DOI") or ""
        meta = crossref_fields(item)
        rows.append(
            {
                "title": title,
                "doi": doi,
                "url": f"https://doi.org/{doi}" if doi else "",
                **meta,
            }
        )
    print(json.dumps({"ok": True, "results": rows}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

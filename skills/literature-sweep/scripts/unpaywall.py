#!/usr/bin/env python3
"""Unpaywall OA lookup. Requires UNPAYWALL_EMAIL."""

from __future__ import annotations

import json
import os
import sys
import urllib.parse
import urllib.request


def main() -> int:
    doi = " ".join(sys.argv[1:]).strip()
    email = os.environ.get("UNPAYWALL_EMAIL") or ""
    if not doi:
        print(json.dumps({"error": "doi required"}))
        return 1
    if not email:
        print(json.dumps({"error": "UNPAYWALL_EMAIL is not set"}))
        return 1
    url = "https://api.unpaywall.org/v2/" + urllib.parse.quote(doi) + "?" + urllib.parse.urlencode(
        {"email": email}
    )
    request = urllib.request.Request(url, headers={"User-Agent": "hdr-research-bot/2.0"})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"error": str(exc)}))
        return 1
    best = (payload or {}).get("best_oa_location") or {}
    print(
        json.dumps(
            {
                "ok": True,
                "doi": doi,
                "oa_url": best.get("url") or best.get("url_for_pdf"),
                "pdf": best.get("url_for_pdf"),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

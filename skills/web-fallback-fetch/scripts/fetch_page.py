#!/usr/bin/env python3
"""Fetch a URL with curl, extract readable text, then try Wayback.

Uses the curl CLI. Uses the `readable` CLI when present. Otherwise uses
the stdlib HTML parser. Does not bundle a third-party library.
Does not pipe curl to a shell.
"""

from __future__ import annotations

import html
import re
import shutil
import subprocess
import sys
from html.parser import HTMLParser

_SKIP_TAGS = frozenset(
    {"script", "style", "noscript", "svg", "nav", "footer", "header", "aside", "form"}
)
_BLOCK_TAGS = frozenset(
    {"p", "div", "article", "section", "li", "br", "h1", "h2", "h3", "h4", "h5", "h6", "tr"}
)
_USER_AGENT = "hdr-research-bot/2.0"
_CURL_TIMEOUT = "30"


class _ReadableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._skip = 0
        self._parts: list[str] = []
        self._prefer: list[str] = []
        self._in_prefer = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        name = tag.lower()
        if name in _SKIP_TAGS:
            self._skip += 1
            return
        if self._skip:
            return
        if name in {"article", "main"}:
            self._in_prefer += 1
        if name in _BLOCK_TAGS:
            self._emit("\n")

    def handle_endtag(self, tag: str) -> None:
        name = tag.lower()
        if name in _SKIP_TAGS and self._skip:
            self._skip -= 1
            return
        if self._skip:
            return
        if name in {"article", "main"} and self._in_prefer:
            self._in_prefer -= 1
        if name in _BLOCK_TAGS:
            self._emit("\n")

    def handle_data(self, data: str) -> None:
        if self._skip:
            return
        text = data.strip()
        if not text:
            return
        self._emit(text + " ")

    def _emit(self, chunk: str) -> None:
        if self._in_prefer:
            self._prefer.append(chunk)
        else:
            self._parts.append(chunk)

    def text(self) -> str:
        raw = "".join(self._prefer) if self._prefer else "".join(self._parts)
        cleaned = html.unescape(raw)
        cleaned = re.sub(r"[ \t]+", " ", cleaned)
        cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
        return cleaned.strip()


def readable_text(raw_html: str) -> str:
    """Extract article-like text from HTML. Stdlib only."""
    parser = _ReadableParser()
    try:
        parser.feed(raw_html)
        parser.close()
    except Exception:
        return re.sub(r"<[^>]+>", " ", raw_html)
    return parser.text()


def _curl(url: str) -> tuple[int, str, str]:
    curl = shutil.which("curl")
    if not curl:
        return 127, "", "curl is not on PATH"
    try:
        completed = subprocess.run(
            [
                curl,
                "-fsSL",
                "--max-time",
                _CURL_TIMEOUT,
                "-A",
                _USER_AGENT,
                "--",
                url,
            ],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        return 1, "", str(exc)
    return completed.returncode, completed.stdout, completed.stderr


def _readable_cli(raw_html: str) -> str:
    readable = shutil.which("readable")
    if not readable:
        return ""
    try:
        completed = subprocess.run(
            [readable, "--quiet"],
            check=False,
            input=raw_html,
            capture_output=True,
            text=True,
        )
    except OSError:
        return ""
    if completed.returncode != 0:
        return ""
    return (completed.stdout or "").strip()


def extract_readable(raw_html: str) -> str:
    via_cli = _readable_cli(raw_html)
    if via_cli:
        return via_cli
    return readable_text(raw_html)


def fetch_readable(url: str) -> dict[str, str]:
    """Fetch live, then Wayback. Returns status fields plus body text."""
    code, body, err = _curl(url)
    if code == 0 and body.strip():
        text = extract_readable(body)
        if text:
            return {
                "fetch_status": "ok",
                "url": url,
                "archived_url": "",
                "text": text,
            }
    archived = f"https://web.archive.org/web/2/{url}"
    archive_code, archive_body, archive_err = _curl(archived)
    if archive_code == 0 and archive_body.strip():
        text = extract_readable(archive_body)
        if text:
            return {
                "fetch_status": "archived",
                "url": url,
                "archived_url": archived,
                "text": text,
            }
    detail = (err or archive_err or "empty body").strip()
    return {
        "fetch_status": "failed",
        "url": url,
        "archived_url": "",
        "text": "",
        "error": detail,
    }


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: fetch_page.py <url>", file=sys.stderr)
        return 1
    url = sys.argv[1]
    result = fetch_readable(url)
    print(f"# fetch_status: {result['fetch_status']}")
    print(f"# url: {result['url']}")
    if result.get("archived_url"):
        print(f"# archived_url: {result['archived_url']}")
    if result.get("error"):
        print(f"# error: {result['error']}", file=sys.stderr)
    text = result.get("text") or ""
    if text:
        sys.stdout.write(text)
        if not text.endswith("\n"):
            sys.stdout.write("\n")
        return 0
    print("fetch failed; try archive_lookup or browser_navigate", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

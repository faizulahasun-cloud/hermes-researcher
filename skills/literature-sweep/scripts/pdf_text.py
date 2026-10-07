#!/usr/bin/env python3
"""Extract text from a PDF path. Prefers pypdf; falls back to pdftotext."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: pdf_text.py <file.pdf>", file=sys.stderr)
        return 1
    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"missing {path}", file=sys.stderr)
        return 1
    try:
        from pypdf import PdfReader  # type: ignore

        reader = PdfReader(str(path))
        text = "\n".join((page.extract_text() or "") for page in reader.pages)
        sys.stdout.write(text)
        return 0
    except Exception:
        pass
    try:
        completed = subprocess.run(
            ["pdftotext", "-layout", str(path), "-"],
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode == 0:
            sys.stdout.write(completed.stdout)
            return 0
    except FileNotFoundError:
        pass
    print("pdf extract failed; rasterize and use vision_analyze", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

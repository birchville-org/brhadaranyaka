#!/usr/bin/env python3
"""
AlexandriaSandwich — Generates book.json and compiles EPUB 3 for Bṛhadāraṇyaka-Upaniṣad I.4
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "data" / "output" / "brhadaranyaka_1_4"
BOOKS_DIR = ROOT / "data" / "output" / "books" / "brhadaranyaka_1_4"
MASTER_JSON = OUT_DIR / "brhadaranyaka_1_4_master.json"

BOOKS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    data = json.loads(MASTER_JSON.read_text(encoding="utf-8"))
    work = data["work"]
    sections = data["sections"]

    # Build blocks for book.json
    blocks = []
    # Title / Header
    blocks.append({
        "type": "h1",
        "text": f"{work['title']} {work['adhyaya']}.{work['brahmana']}",
        "bbox": [0, 0, 0, 0]
    })
    blocks.append({
        "type": "h2",
        "text": f"{work['subtitle']} ({work['recension']})",
        "bbox": [0, 0, 0, 0]
    })

    # Intro paragraphs
    for p in work.get("introduction_slaje", "").split("\n\n"):
        if p.strip():
            blocks.append({
                "type": "p",
                "text": p.strip(),
                "bbox": [0, 0, 0, 0]
            })

    # Sections 1 to 31
    for sec in sections:
        blocks.append({
            "type": "h2",
            "text": sec["title"],
            "bbox": [0, 0, 0, 0]
        })
        blocks.append({
            "type": "p",
            "text": sec["sanskrit_devanagari"],
            "bbox": [0, 0, 0, 0]
        })
        blocks.append({
            "type": "p",
            "text": f"*{sec['sanskrit_iast']}*",
            "bbox": [0, 0, 0, 0]
        })
        blocks.append({
            "type": "p",
            "text": f"**Walter Slaje (2009):** {sec['translation_slaje']}",
            "bbox": [0, 0, 0, 0]
        })
        blocks.append({
            "type": "p",
            "text": f"**Otto von Böhtlingk (1889):** {sec['translation_bohtlingk']}",
            "bbox": [0, 0, 0, 0]
        })
        if sec["commentary_slaje"]:
            for comm in sec["commentary_slaje"]:
                blocks.append({
                    "type": "p",
                    "text": f"*{comm['lemma']}*: {comm['text']}",
                    "bbox": [0, 0, 0, 0]
                })

    book_json = {
        "metadata": {
            "job": "brhadaranyaka_1_4",
            "title": "Bṛhadāraṇyaka-Upaniṣad I.4 (Synoptische Edition)",
            "author": "Walter Slaje & Otto von Böhtlingk",
            "language": "deu+san",
            "page_count": len(sections),
            "generated_at": "2026-09-29T07:35:00Z",
            "pipeline": "AlexandriaSandwich"
        },
        "pages": [
            {
                "facs": "synopsis.png",
                "bbox": [0, 0, 1000, 1400],
                "blocks": blocks
            }
        ]
    }

    target_json = BOOKS_DIR / "book.json"
    target_json.write_text(json.dumps(book_json, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"1) Wrote book.json: {target_json}")

    # Run export_epub.py
    epub_out = OUT_DIR / "brhadaranyaka_1_4.epub"
    cmd = [
        str(ROOT / ".venv" / "bin" / "python"),
        str(ROOT / "scripts" / "export_epub.py"),
        "--job", "brhadaranyaka_1_4",
        "--input", str(target_json),
        "--output", str(epub_out)
    ]
    print("2) Running export_epub.py...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("EPUB Error:", res.stderr)
        raise SystemExit(res.returncode)

    print(f"3) Successfully compiled EPUB 3: {epub_out} ({epub_out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
AlexandriaSandwich — Bṛhadāraṇyaka-Upaniṣad I.4 Synoptic Alignment Engine
Aggregates and aligns:
1. Sanskrit IAST (Anna Esposito Text Edition)
2. Sanskrit Devanagari (Phonetically precise transliteration via indic_transliteration)
3. Translation by Walter Slaje (2009)
4. Translation by Otto von Böhtlingk (1889)
5. Philological Commentary by Walter Slaje (2009, pp. 482-493)
6. Critical apparatus / notes by Otto von Böhtlingk (1889)
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List

import pymupdf
from indic_transliteration import sanscript

ROOT = Path(__file__).resolve().parent.parent
INPUT_DIR = ROOT / "data" / "input" / "brhadaranyaka_1_4"
PROC_DIR = ROOT / "data" / "processing" / "brhadaranyaka_1_4"
OUT_DIR = ROOT / "data" / "output" / "brhadaranyaka_1_4"

OUT_DIR.mkdir(parents=True, exist_ok=True)


def parse_iast_verses(pdf_path: Path) -> Dict[int, str]:
    doc = pymupdf.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text() + "\n"

    full_text = re.sub(r"Bṛhadāranyaka-Upaniṣad I\.4", "", full_text)
    pattern = r"(.*?)(?:\|\|\s*BrhUp[_ ]1,4\.(\d+)\s*\|\|)"
    matches = re.findall(pattern, full_text, flags=re.DOTALL)

    verses: Dict[int, str] = {}
    for text, num_str in matches:
        num = int(num_str)
        clean = " ".join(text.strip().split())
        verses[num] = clean
    return verses


def parse_slaje_translation(json_path: Path) -> Dict[int, str]:
    data = json.loads(json_path.read_text(encoding="utf-8"))
    pages = data.get("pages", [])
    # Translation is on pages 3 to 6 (0-indexed 2 to 5)
    full_text = "\n\n".join(pages[i].get("markdown", "") for i in range(2, min(6, len(pages))))

    verses: Dict[int, str] = {}
    for i in range(1, 32):
        next_marker = r"\n(?:#+\s*)?" + str(i + 1) + r"\s+[A-ZÄÖÜ»\"\'\(\*]" if i < 31 else r"\n#+\s*I\s+5|\Z"
        pattern = r"(?:^|\n)(?:#+\s*)?" + str(i) + r"\s+([A-ZÄÖÜ»\"\'\(\*].*?)(?=" + next_marker + ")"
        match = re.search(pattern, full_text, flags=re.DOTALL)
        if match:
            clean = " ".join(match.group(1).strip().split())
            verses[i] = clean
        else:
            verses[i] = ""
    return verses


def parse_bohtlingk_translation(json_path: Path) -> Dict[int, str]:
    data = json.loads(json_path.read_text(encoding="utf-8"))
    pages = data.get("pages", [])
    # Translation is on pages 7 to 12 (0-indexed 6 to 11)
    full_text = "\n\n".join(pages[i].get("markdown", "") for i in range(6, min(12, len(pages))))

    verses: Dict[int, str] = {}
    for i in range(1, 32):
        next_marker = r"\n(?:#+\s*)?" + str(i + 1) + r"\.\s+[A-ZÄÖÜ»\"\'\(\*]" if i < 31 else r"\n#+\s*Fünftes|\Z"
        pattern = r"(?:^|\n)(?:#+\s*)?" + str(i) + r"\.\s+([A-ZÄÖÜ»\"\'\(\*].*?)(?=" + next_marker + ")"
        match = re.search(pattern, full_text, flags=re.DOTALL)
        if match:
            clean = " ".join(match.group(1).strip().split())
            verses[i] = clean
        else:
            verses[i] = ""
    return verses


def parse_slaje_commentary(json_path: Path) -> Dict[int, List[Dict[str, str]]]:
    data = json.loads(json_path.read_text(encoding="utf-8"))
    pages = data.get("pages", [])
    # Commentary on I.4 is on pages 12 to 15 (0-indexed 11 to 14)
    comm_pages = pages[11:15]
    full_text = "\n\n".join(p.get("markdown", "") for p in comm_pages)

    # Specific verse commentary mapping for I.4
    # Comments in Slaje: format like: "11 *beide innen unbehaart*] Mund und Hände."
    # or "23 beim Rājasūya-Opfer... ] text..."
    comments: Dict[int, List[Dict[str, str]]] = {i: [] for i in range(1, 32)}

    # Regex to capture: verse_number, lemma, comment_body
    pattern = r"(?:^|\n)(\d{1,2})\s+([\*»\"\'A-Za-zÄÖÜ].*?\])\s*([^\n]+(?:\n(?!\d{1,2}\s+[\*»\"\'A-Za-zÄÖÜ]).*)*)"
    matches = re.finditer(pattern, full_text)

    for m in matches:
        num = int(m.group(1))
        lemma = m.group(2).strip().rstrip("]").strip()
        body = m.group(3).strip()
        # Clean running headers / page numbers
        body = re.sub(r'STELLENKOMMENTAR[^\n]*\d{3}', '', body)
        body = re.sub(r'\d{3}\s+6\.\s*BṚHAD[^\n]*', '', body)
        body = re.sub(r'UPANISCHADEN DES WEISSEN YAJUR-VEDA', '', body)
        body = " ".join(body.split())
        if 1 <= num <= 31:
            comments[num].append({
                "lemma": lemma,
                "text": body,
            })

    return comments


def get_slaje_intro(json_path: Path) -> str:
    data = json.loads(json_path.read_text(encoding="utf-8"))
    pages = data.get("pages", [])
    # Introduction on BĀU is on pages 7 to 10 (0-indexed 6 to 9)
    intro_parts = []
    for i in range(6, min(10, len(pages))):
        md = pages[i].get("markdown", "")
        # Remove headers like '482', 'STELLENKOMMENTAR', etc.
        lines = [l for l in md.split("\n") if not re.match(r"^\d{1,3}$|^STELLENKOMMENTAR|^6\.\s*BṚHAD", l.strip())]
        intro_parts.append("\n".join(lines).strip())
    return "\n\n".join(intro_parts).strip()


def build_master_corpus() -> Dict[str, Any]:
    iast_pdf = INPUT_DIR / "Text Brhadaranyaka Upanisad I.4.pdf"
    slaje_json = PROC_DIR / "mistral" / "slaje_complete.json"
    bohtlingk_json = PROC_DIR / "mistral" / "bohtlingk_complete.json"

    print("1) Parsing Sanskrit IAST text...")
    iast_verses = parse_iast_verses(iast_pdf)
    print(f"   -> Found {len(iast_verses)} IAST verses.")

    print("2) Parsing Walter Slaje (2009) translation...")
    slaje_trans = parse_slaje_translation(slaje_json)
    print(f"   -> Found {len(slaje_trans)} Slaje translation verses.")

    print("3) Parsing Otto von Böhtlingk (1889) translation...")
    boht_trans = parse_bohtlingk_translation(bohtlingk_json)
    print(f"   -> Found {len(boht_trans)} Böhtlingk translation verses.")

    print("4) Parsing Walter Slaje (2009) philological commentary...")
    slaje_comm = parse_slaje_commentary(slaje_json)
    total_notes = sum(len(n) for n in slaje_comm.values())
    print(f"   -> Extracted {total_notes} specific verse commentaries.")

    print("5) Extracting Slaje BĀU historical introduction...")
    slaje_intro = get_slaje_intro(slaje_json)
    print(f"   -> Extracted introduction ({len(slaje_intro)} chars).")

    sections: List[Dict[str, Any]] = []
    for i in range(1, 32):
        iast = iast_verses.get(i, "")
        # Clean IAST for transliteration
        deva = sanscript.transliterate(iast, sanscript.IAST, sanscript.DEVANAGARI)
        # Ensure dandas have proper spacing
        deva = deva.replace(" ।", " । ").replace(" ॥", " ॥ ").strip()

        sections.append({
            "verse_num": i,
            "canonical_id": f"1.4.{i}",
            "title": f"Bṛhadāraṇyaka-Upaniṣad 1.4.{i}",
            "sanskrit_iast": iast,
            "sanskrit_devanagari": deva,
            "translation_slaje": slaje_trans.get(i, ""),
            "translation_bohtlingk": boht_trans.get(i, ""),
            "commentary_slaje": slaje_comm.get(i, []),
            "apparatus_bohtlingk": [
                {"note": "Vgl. Böhtlingk (1889), S. 5-9 (Text) u. S. 10-14 (Übersetzung)."}
            ] if i in (6, 22, 24) else [],
        })

    master = {
        "work": {
            "title": "Bṛhadāraṇyaka-Upaniṣad",
            "adhyaya": 1,
            "brahmana": 4,
            "subtitle": "Ursubjekt (ātman) / Schöpfungsmythos",
            "recension": "Mādhyandina (mit Referenz zur Kāṇva-Zählung)",
            "sources": [
                {
                    "siglum": "Slaje2009",
                    "author": "Walter Slaje",
                    "year": 2009,
                    "title": "Upanischaden: Arkanum des Veda",
                    "publisher": "Verlag der Weltreligionen (Insel Verlag)",
                    "place": "Frankfurt am Main / Leipzig",
                    "pages": "108–117 (Text) u. 482–493 (Kommentar)",
                },
                {
                    "siglum": "Böhtlingk1889",
                    "author": "Otto von Böhtlingk",
                    "year": 1889,
                    "title": "Bṛhadāraṇjakopanishad in der Mādhyandina-Recension",
                    "publisher": "Kaiserliche Akademie der Wissenschaften",
                    "place": "St. Petersburg",
                    "pages": "5–9 (Devanagari-Text) u. 10–14 (Übersetzung)",
                },
                {
                    "siglum": "EspositoIAST",
                    "editor": "Anna Esposito",
                    "title": "Text Bṛhadāraṇyaka-Upaniṣad I.4",
                    "format": "IAST Standard Transliteration",
                },
            ],
            "total_verses": len(sections),
            "introduction_slaje": slaje_intro,
        },
        "sections": sections,
    }

    return master


def main() -> None:
    master = build_master_corpus()

    # 1) Save Master JSON
    json_path = OUT_DIR / "brhadaranyaka_1_4_master.json"
    json_path.write_text(json.dumps(master, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"6) Successfully saved Master JSON: {json_path} ({json_path.stat().st_size} bytes)")

    # 2) Save Master Markdown
    md_path = OUT_DIR / "brhadaranyaka_1_4_master.md"
    md_lines = [
        f"# {master['work']['title']} {master['work']['adhyaya']}.{master['work']['brahmana']}",
        f"**{master['work']['subtitle']}** — *{master['work']['recension']}*\n",
        "## Quellen & Editionen",
        "- **Slaje (2009):** *Upanischaden: Arkanum des Veda*, Frankfurt am Main.",
        "- **Böhtlingk (1889):** *Bṛhadāraṇjakopanishad in der Mādhyandina-Recension*, St. Petersburg.",
        "- **Esposito:** *IAST-Kanontext*.\n",
        "---",
        "## Synoptischer Text (1.4.1 – 1.4.31)\n",
    ]

    for sec in master["sections"]:
        md_lines.append(f"### {sec['title']}\n")
        md_lines.append(f"**Devanagari:**\n> {sec['sanskrit_devanagari']}\n")
        md_lines.append(f"**IAST:**\n> *{sec['sanskrit_iast']}*\n")
        md_lines.append(f"**Übersetzung Walter Slaje (2009):**\n{sec['translation_slaje']}\n")
        md_lines.append(f"**Übersetzung Otto von Böhtlingk (1889):**\n{sec['translation_bohtlingk']}\n")

        if sec["commentary_slaje"]:
            md_lines.append("**Philologischer Kommentar (Slaje 2009):**")
            for comm in sec["commentary_slaje"]:
                md_lines.append(f"- *{comm['lemma']}*: {comm['text']}")
            md_lines.append("")

        md_lines.append("---\n")

    md_path.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"7) Successfully saved Master Markdown: {md_path} ({md_path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
AlexandriaSandwich — Bṛhadāraṇyaka-Upaniṣad I.4 Synoptic Typesetting Engine
Builds:
1. brhadaranyaka_1_4_synopsis.html (Standalone web document with rich typography)
2. brhadaranyaka_1_4_synopsis.pdf (Compiled via WeasyPrint)
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "data" / "output"
MASTER_JSON = OUT_DIR / "brhadaranyaka_1_4_master.json"


def generate_html(data: dict) -> str:
    work = data["work"]
    sections = data["sections"]

    sec_html_blocks = []
    for s in sections:
        comm_html = ""
        if s["commentary_slaje"]:
            items = []
            for c in s["commentary_slaje"]:
                items.append(f"""
                <div class="comment-item">
                    <span class="comment-lemma">{c['lemma']}</span>
                    <span class="comment-text">{c['text']}</span>
                </div>
                """)
            comm_html = f"""
            <div class="commentary-box">
                <div class="box-title">Philologischer Stellenkommentar (Slaje 2009)</div>
                {''.join(items)}
            </div>
            """

        sec_html_blocks.append(f"""
        <article class="verse-card" id="v-{s['verse_num']}">
            <header class="verse-header">
                <span class="verse-badge">BĀU {s['canonical_id']}</span>
                <span class="verse-title">Abschnitt {s['verse_num']}</span>
            </header>

            <div class="sanskrit-container">
                <div class="devanagari-block">{s['sanskrit_devanagari']}</div>
                <div class="iast-block">{s['sanskrit_iast']}</div>
            </div>

            <div class="synopsis-grid">
                <div class="trans-column slaje-col">
                    <div class="col-header">
                        <span class="siglum">Slaje (2009)</span>
                        <span class="trans-label">Moderne Rekonstruktion & Ursubjekt-Konzeption</span>
                    </div>
                    <div class="trans-content">{s['translation_slaje']}</div>
                </div>

                <div class="trans-column bohtlingk-col">
                    <div class="col-header">
                        <span class="siglum">Böhtlingk (1889)</span>
                        <span class="trans-label">Historische Mādhyandina-Erstausgabe</span>
                    </div>
                    <div class="trans-content">{s['translation_bohtlingk']}</div>
                </div>
            </div>

            {comm_html}
        </article>
        """)

    # Format intro
    intro_paragraphs = work.get("introduction_slaje", "").split("\n\n")
    intro_html = "".join(f"<p>{p.strip()}</p>" for p in intro_paragraphs if p.strip())

    return f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<title>{work['title']} {work['adhyaya']}.{work['brahmana']} — Synoptische Edition</title>
<style>
@page {{
    size: A4 portrait;
    margin: 18mm 16mm 20mm 16mm;
    @top-left {{
        content: "Bṛhadāraṇyaka-Upaniṣad I.4 — Synoptische Edition";
        font-family: 'EB Garamond', 'Linux Libertine O', serif;
        font-size: 8.5pt;
        color: #666;
        border-bottom: 0.5pt solid #ddd;
        padding-bottom: 2mm;
    }}
    @top-right {{
        content: "Mādhyandina-Rezension";
        font-family: 'EB Garamond', 'Linux Libertine O', serif;
        font-size: 8.5pt;
        color: #666;
        border-bottom: 0.5pt solid #ddd;
        padding-bottom: 2mm;
    }}
    @bottom-center {{
        content: counter(page);
        font-family: 'EB Garamond', 'Linux Libertine O', serif;
        font-size: 9pt;
        color: #555;
    }}
}}

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Source Serif 4', 'EB Garamond', 'Linux Libertine O', Georgia, serif;
    font-size: 10.5pt;
    line-height: 1.55;
    color: #03192e;
    background: #fcf9f2;
    -webkit-font-smoothing: antialiased;
}}

/* Front Matter */
.title-page {{
    page-break-after: always;
    padding-top: 40mm;
    text-align: center;
}}

.title-supratitle {{
    font-size: 13pt;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #48626e;
    margin-bottom: 8mm;
    font-weight: 600;
}}

.main-title {{
    font-size: 26pt;
    font-weight: 700;
    line-height: 1.2;
    margin-bottom: 6mm;
    letter-spacing: -0.01em;
    color: #03192e;
}}

.subtitle {{
    font-size: 15pt;
    font-style: italic;
    color: #48626e;
    margin-bottom: 12mm;
}}

.divider-ornament {{
    margin: 8mm auto;
    width: 60mm;
    border-top: 1.5pt solid #eab308;
}}

.edition-meta {{
    margin-top: 20mm;
    font-size: 10.5pt;
    color: #03192e;
    line-height: 1.7;
    max-width: 140mm;
    margin-left: auto;
    margin-right: auto;
    text-align: left;
    background: #f1eee7;
    padding: 6mm 8mm;
    border: 0.75pt solid #d9d4cb;
    border-left: 3pt solid #03192e;
    border-radius: 2px;
}}

.meta-item {{
    margin-bottom: 2mm;
}}

.meta-label {{
    font-weight: 600;
    color: #03192e;
}}

/* Introduction Chapter */
.intro-chapter {{
    page-break-after: always;
    padding-top: 10mm;
}}

.chapter-title {{
    font-size: 18pt;
    font-weight: 700;
    color: #03192e;
    border-bottom: 1pt solid #03192e;
    padding-bottom: 3mm;
    margin-bottom: 6mm;
}}

.intro-content p {{
    margin-bottom: 4mm;
    text-align: justify;
    text-justify: inter-word;
    text-indent: 4mm;
}}

.intro-content p:first-of-type {{
    text-indent: 0;
}}

/* Synoptic Cards */
.verse-card {{
    page-break-inside: avoid;
    margin-bottom: 10mm;
    border: 0.75pt solid #d9d4cb;
    border-radius: 4px;
    background: #ffffff;
    box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    overflow: hidden;
}}

.verse-header {{
    background: #f1eee7;
    border-bottom: 0.75pt solid #d9d4cb;
    padding: 3mm 5mm;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.verse-badge {{
    background: #03192e;
    color: #ffffff;
    font-size: 9pt;
    font-weight: 700;
    padding: 1mm 3mm;
    border-radius: 2px;
    letter-spacing: 0.05em;
}}

.verse-title {{
    font-size: 9.5pt;
    font-weight: 600;
    color: #48626e;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}}

.sanskrit-container {{
    background: #fdfbf7;
    padding: 4mm 6mm;
    border-bottom: 0.5pt solid #d9d4cb;
}}

.devanagari-block {{
    font-family: 'Sanskrit2003', 'Devanagari MT', 'Noto Sans Devanagari', serif;
    font-size: 13.5pt;
    line-height: 1.6;
    color: #b22222;
    font-weight: 600;
    margin-bottom: 2mm;
    text-align: justify;
}}

.iast-block {{
    font-size: 10.5pt;
    font-style: italic;
    color: #03192e;
    line-height: 1.45;
}}

/* 2-Column Synopsis Grid */
.synopsis-grid {{
    display: flex;
    flex-direction: row;
    border-bottom: 0.5pt solid #d9d4cb;
}}

.trans-column {{
    flex: 1;
    padding: 4mm 5mm;
}}

.slaje-col {{
    border-right: 0.5pt solid #d9d4cb;
    background: #ffffff;
}}

.bohtlingk-col {{
    background: #faf9f6;
}}

.col-header {{
    margin-bottom: 2.5mm;
    border-bottom: 0.5pt solid #d9d4cb;
    padding-bottom: 1.5mm;
}}

.siglum {{
    font-size: 9.5pt;
    font-weight: 700;
    color: #03192e;
    display: block;
}}

.trans-label {{
    font-size: 8pt;
    color: #48626e;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}

.trans-content {{
    font-size: 10pt;
    line-height: 1.5;
    text-align: justify;
    text-justify: inter-word;
    color: #03192e;
}}

/* Commentary Box */
.commentary-box {{
    background: #fefce8;
    padding: 3.5mm 5mm;
    border-top: 0.5pt solid #fde68a;
    border-left: 3.5pt solid #eab308;
}}

.box-title {{
    font-size: 8.5pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #ca8a04;
    margin-bottom: 2mm;
}}

.comment-item {{
    font-size: 9pt;
    line-height: 1.45;
    margin-bottom: 1.5mm;
    color: #03192e;
}}

.comment-lemma {{
    font-weight: 600;
    color: #ca8a04;
    margin-right: 1.5mm;
}}
</style>
</head>
<body>

<section class="title-page">
    <div class="title-supratitle">Indologische Editionen · Synopse</div>
    <h1 class="main-title">Bṛhadāraṇyaka-Upaniṣad</h1>
    <div class="subtitle">Adhyāya I, Brāhmaṇa 4: Das Ursubjekt (ātman) & Der Schöpfungsmythos</div>
    <div class="divider-ornament"></div>

    <div class="edition-meta">
        <div class="meta-item"><span class="meta-label">Kanonischer Text:</span> Sanskrit in Devanagari und wissenschaftlicher IAST-Transliteration</div>
        <div class="meta-item"><span class="meta-label">Übersetzung A (2009):</span> Walter Slaje, <em>Upanischaden: Arkanum des Veda</em> (Insel Verlag)</div>
        <div class="meta-item"><span class="meta-label">Übersetzung B (1889):</span> Otto von Böhtlingk, <em>Bṛhadāraṇjakopanishad in der Mādhyandina-Recension</em> (St. Petersburg)</div>
        <div class="meta-item"><span class="meta-label">Philologischer Kommentar:</span> Vollständiger Stellenkommentar zu I.4 (Walter Slaje, S. 486–493)</div>
        <div class="meta-item"><span class="meta-label">Umfang:</span> 31 Abschnitte (1.4.1 – 1.4.31) vollständig synchronisiert</div>
    </div>
</section>

<section class="intro-chapter">
    <h2 class="chapter-title">Philologische Einleitung (Walter Slaje)</h2>
    <div class="intro-content">
        {intro_html}
    </div>
</section>

<section class="synopsis-content">
    <h2 class="chapter-title" style="margin-bottom: 6mm;">Synoptischer Text (Abschnitte 1.4.1 bis 1.4.31)</h2>
    {''.join(sec_html_blocks)}
</section>

</body>
</html>
"""


def main() -> None:
    if not MASTER_JSON.exists():
        print(f"Error: {MASTER_JSON} not found. Run scripts/align_brhadaranyaka.py first.")
        raise SystemExit(1)

    data = json.loads(MASTER_JSON.read_text(encoding="utf-8"))

    html_file = OUT_DIR / "brhadaranyaka_1_4_synopsis.html"
    pdf_file = OUT_DIR / "brhadaranyaka_1_4_synopsis.pdf"

    print("1) Generating publication-grade synoptic HTML...")
    html_content = generate_html(data)
    html_file.write_text(html_content, encoding="utf-8")
    print(f"   -> Wrote HTML: {html_file} ({html_file.stat().st_size} bytes)")

    print("2) Compiling synoptic PDF with WeasyPrint...")
    cmd = ["/opt/homebrew/bin/weasyprint", str(html_file), str(pdf_file)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("WeasyPrint error:", res.stderr)
        raise SystemExit(res.returncode)

    print(f"3) Successfully compiled PDF: {pdf_file} ({pdf_file.stat().st_size} bytes)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
AlexandriaSandwich — TEI-P5 XML Exporter for Bṛhadāraṇyaka-Upaniṣad I.4
Generates standardized digital humanities archive format with parallel alignments:
- Devanagari (sa-Deva)
- IAST Transliteration (sa-Latn)
- Walter Slaje (2009) German Translation (de)
- Otto von Böhtlingk (1889) German Translation (de)
- Philological Commentary Notes
"""
from __future__ import annotations

import datetime
import json
import xml.dom.minidom
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "data" / "output"
MASTER_JSON = OUT_DIR / "brhadaranyaka_1_4_master.json"
TEI_XML = OUT_DIR / "brhadaranyaka_1_4.tei.xml"

TEI_NS = "http://www.tei-c.org/ns/1.0"
ET.register_namespace("", TEI_NS)


def build_tei_xml(data: dict) -> str:
    work = data["work"]
    sections = data["sections"]
    gen_date = datetime.datetime.now(datetime.timezone.utc).isoformat()

    tei = ET.Element(f"{{{TEI_NS}}}TEI")

    # Header
    header = ET.SubElement(tei, f"{{{TEI_NS}}}teiHeader")
    file_desc = ET.SubElement(header, f"{{{TEI_NS}}}fileDesc")

    title_stmt = ET.SubElement(file_desc, f"{{{TEI_NS}}}titleStmt")
    t = ET.SubElement(title_stmt, f"{{{TEI_NS}}}title")
    t.text = f"{work['title']} {work['adhyaya']}.{work['brahmana']} — Synoptische Edition"
    a = ET.SubElement(title_stmt, f"{{{TEI_NS}}}author")
    a.text = "AlexandriaSandwich / Vedic Corpus"

    pub_stmt = ET.SubElement(file_desc, f"{{{TEI_NS}}}publicationStmt")
    p_pub = ET.SubElement(pub_stmt, f"{{{TEI_NS}}}p")
    p_pub.text = f"Digitized and structured via AlexandriaSandwich synoptic engine on {gen_date}."

    source_desc = ET.SubElement(file_desc, f"{{{TEI_NS}}}sourceDesc")
    for src in work.get("sources", []):
        p_src = ET.SubElement(source_desc, f"{{{TEI_NS}}}bibl", {"xml:id": src.get("siglum", "src")})
        p_src.text = f"{src.get('author', src.get('editor', ''))} ({src.get('year', '')}): {src.get('title', '')}."

    profile_desc = ET.SubElement(header, f"{{{TEI_NS}}}profileDesc")
    lang_usage = ET.SubElement(profile_desc, f"{{{TEI_NS}}}langUsage")
    ET.SubElement(lang_usage, f"{{{TEI_NS}}}language", {"ident": "sa-Deva"}).text = "Sanskrit (Devanagari)"
    ET.SubElement(lang_usage, f"{{{TEI_NS}}}language", {"ident": "sa-Latn"}).text = "Sanskrit (IAST Romanized)"
    ET.SubElement(lang_usage, f"{{{TEI_NS}}}language", {"ident": "de"}).text = "Deutsch"

    # Text Body
    text_elem = ET.SubElement(tei, f"{{{TEI_NS}}}text")
    body = ET.SubElement(text_elem, f"{{{TEI_NS}}}body")

    # Introduction
    div_intro = ET.SubElement(body, f"{{{TEI_NS}}}div", {"type": "introduction"})
    head_intro = ET.SubElement(div_intro, f"{{{TEI_NS}}}head")
    head_intro.text = "Philologische Einleitung (Walter Slaje 2009)"
    for p_text in work.get("introduction_slaje", "").split("\n\n"):
        if p_text.strip():
            p_elem = ET.SubElement(div_intro, f"{{{TEI_NS}}}p")
            p_elem.text = p_text.strip()

    # Synoptic Sections
    div_main = ET.SubElement(body, f"{{{TEI_NS}}}div", {
        "type": "brahmana",
        "n": f"{work['adhyaya']}.{work['brahmana']}",
        "subtype": work.get("subtitle", "")
    })
    head_main = ET.SubElement(div_main, f"{{{TEI_NS}}}head")
    head_main.text = f"Bṛhadāraṇyaka-Upaniṣad {work['adhyaya']}.{work['brahmana']}: {work.get('subtitle', '')}"

    for sec in sections:
        sec_div = ET.SubElement(div_main, f"{{{TEI_NS}}}div", {
            "type": "section",
            "n": sec["canonical_id"],
            "xml:id": f"bau_{sec['canonical_id'].replace('.', '_')}"
        })
        sec_head = ET.SubElement(sec_div, f"{{{TEI_NS}}}head")
        sec_head.text = sec["title"]

        # Devanagari
        ab_deva = ET.SubElement(sec_div, f"{{{TEI_NS}}}ab", {
            "type": "sanskrit",
            "xml:lang": "sa-Deva"
        })
        ab_deva.text = sec["sanskrit_devanagari"]

        # IAST
        ab_iast = ET.SubElement(sec_div, f"{{{TEI_NS}}}ab", {
            "type": "sanskrit",
            "xml:lang": "sa-Latn"
        })
        ab_iast.text = sec["sanskrit_iast"]

        # Slaje 2009
        ab_slaje = ET.SubElement(sec_div, f"{{{TEI_NS}}}ab", {
            "type": "translation",
            "resp": "#Slaje2009",
            "xml:lang": "de"
        })
        ab_slaje.text = sec["translation_slaje"]

        # Böhtlingk 1889
        ab_boht = ET.SubElement(sec_div, f"{{{TEI_NS}}}ab", {
            "type": "translation",
            "resp": "#Böhtlingk1889",
            "xml:lang": "de"
        })
        ab_boht.text = sec["translation_bohtlingk"]

        # Philological Commentary
        if sec["commentary_slaje"]:
            for comm in sec["commentary_slaje"]:
                note_elem = ET.SubElement(sec_div, f"{{{TEI_NS}}}note", {
                    "type": "philological",
                    "resp": "#Slaje2009"
                })
                lemma = ET.SubElement(note_elem, f"{{{TEI_NS}}}seg", {"type": "lemma"})
                lemma.text = comm["lemma"]
                body_elem = ET.SubElement(note_elem, f"{{{TEI_NS}}}seg", {"type": "body"})
                body_elem.text = comm["text"]

    raw_xml = ET.tostring(tei, encoding="utf-8")
    dom = xml.dom.minidom.parseString(raw_xml)
    return dom.toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")


def main() -> None:
    data = json.loads(MASTER_JSON.read_text(encoding="utf-8"))
    xml_content = build_tei_xml(data)
    TEI_XML.write_text(xml_content, encoding="utf-8")
    print(f"-> Successfully exported TEI-P5 XML: {TEI_XML} ({TEI_XML.stat().st_size} bytes)")


if __name__ == "__main__":
    main()

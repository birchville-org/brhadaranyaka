# 📜 Bṛhadāraṇyaka-Upaniṣad I.4: Das Ursubjekt & Schöpfungsmythos

> **Synoptische philologische Edition, Master-JSON, TEI-P5 XML, Neusatz-PDF & Interaktiver QA-Viewer für Bṛhadāraṇyaka-Upaniṣad 1.4.1–1.4.31 (Mādhyandina-Rezension).**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](pyproject.toml)
[![TEI-P5](https://img.shields.io/badge/format-TEI--P5%20XML-orange.svg)](data/output/brhadaranyaka_1_4.tei.xml)
[![EPUB 3](https://img.shields.io/badge/format-EPUB%203-purple.svg)](data/output/brhadaranyaka_1_4.epub)

---

## 🎯 Zweck & Editionsgegenstand

Die **Bṛhadāraṇyaka-Upaniṣad (BĀU)** gilt unstreitig als die älteste und bedeutendste Prosa-Upanischad des Weißen Yajurveda. Der vierte Abschnitt des ersten Adhyāya (**I.4**) entfaltet den fundamentalen altindischen Schöpfungs- und Emanationsmythos des **Ursubjekts (ātman)** und die Manifestation der Stände (*kṣatra*, *viś*, *śūdra*, *dharma*).

Dieses Repository stellt eine vollständige synoptische Edition der **Mādhyandina-Rezension** (mit Konkordanz zur Kāṇva-Zählung) bereit, basierend auf der Zusammenführung dreier maßgeblicher Textzeugen:

1. **Kanonischer Sanskrit-Urtext:**
   * Devanagari (satz- und ligaturengerecht mit Danda-Gliederung).
   * Wissenschaftliche lateinische Transliteration (IAST) nach Anna Esposito.
2. **Walter Slaje (2009):**
   * *Upanischaden: Arkanum des Veda*. Frankfurt am Main: Verlag der Weltreligionen (Insel Verlag).
   * Moderne philosophische Rekonstruktion mit konsequenter Herausarbeitung der *Ursubjekt*-Konzeption.
   * Vollständiger philologischer Stellenkommentar zu I.4 (S. 482–493, 36 Lemma-Erläuterungen).
3. **Otto von Böhtlingk (1889):**
   * *Bṛhadāraṇjakopanishad in der Mādhyandina-Recension*. St. Petersburg: Kaiserliche Akademie der Wissenschaften.
   * Historische Erstausgabe der Mādhyandina-Rezension (S. 5–9 Text, S. 10–14 Übersetzung).

---

## 📦 Multi-Format Zielmatrix

| Format | Pfad | Beschreibung |
| :--- | :--- | :--- |
| **Interaktiver QA-Viewer** | [`viewer.html`](viewer.html) | Autarker Split-Pane Web-Editor (Payer Standard) mit Silent Auto-Repair und Snippet-Bar. |
| **Satz-PDF** | [`data/output/brhadaranyaka_1_4_synopsis.pdf`](data/output/brhadaranyaka_1_4_synopsis.pdf) | 33-seitiges typografisches Editions-PDF (A4) via WeasyPrint. |
| **Web-Synopse** | [`data/output/brhadaranyaka_1_4_synopsis.html`](data/output/brhadaranyaka_1_4_synopsis.html) | Standalone HTML-Präsentation mit allen Textzeugen und Noten. |
| **Single Source JSON** | [`data/output/brhadaranyaka_1_4_master.json`](data/output/brhadaranyaka_1_4_master.json) | Strukturierter AST mit allen 31 Abschnitten, Varianten und Metadaten. |
| **TEI-P5 XML** | [`data/output/brhadaranyaka_1_4.tei.xml`](data/output/brhadaranyaka_1_4.tei.xml) | Standardkonformes Archivformat für Digital Humanities mit `<ab>`-Parallelität. |
| **EPUB 3 eBook** | [`data/output/brhadaranyaka_1_4.epub`](data/output/brhadaranyaka_1_4.epub) | Reflowable eBook mit eingebetteten Schriften (*Noto Serif Devanagari* & *Linux Libertine O*). |
| **Clean Markdown** | [`data/output/brhadaranyaka_1_4_master.md`](data/output/brhadaranyaka_1_4_master.md) | Lineare Textfassung für KI-Pipelines und RAG. |
| **1:1 Sandwich-PDF** | [`data/output/slaje2009.sandwich.pdf`](data/output/slaje2009.sandwich.pdf) | Originalfaksimile von Slaje (2009) mit unsichtbarer Volltextebene (PDF/A-2b). |

---

## 🛠️ Interaktiver QA-Viewer (Payer Global Web Editor Standard)

Der [`viewer.html`](viewer.html) implementiert den vierstufigen Standard für Editionseditoren:

1. **Split-Pane Layout:**
   * **Links:** Synoptische Vorschau mit Tabs (*Synopse*, *Slaje 2009*, *Böhtlingk 1889*) und Kommentar-Karten.
   * **Rechts:** Quell-Editor für Sanskrit (Devanagari & IAST), beide Übersetzungen und Noten-Array.
2. **Local Storage First:**
   * Automatischer Persistenzabgleich via `localStorage`.
   * Direkter Lese-/Schreibzugriff auf die lokale Festplatte via File System Access API (`showOpenFilePicker` / `showSaveFilePicker`).
3. **Snippet-Toolbar:**
   * Schnelleingabe indologischer Diakritika (`ā`, `ī`, `ū`, `ṛ`, `ṝ`, `ṃ`, `ḥ`, `ś`, `ṣ`, `ṇ`, `ṭ`, `ḍ`).
   * Devanagari-Punkte (`।`, `॥`, `ऽ`, `ँ`).
   * Philologische Auszeichnungszeichen (`»...«`, `[...]`, `*lemma*]`).
4. **Silent Auto-Repair on Save:**
   * Beim Speichern werden Leerraumzeichen (NBSP), typografische Anführungszeichen und Danda-Abstände automatisch und geräuschlos korrigiert.
   * Keine störenden Alert-Dialoge; der Speicherbutton quittiert den Vorgang durch ein dezent gelbes Aufblinken.

---

## 🚀 Pipeline & Reproduktion

```bash
# 1. Abhängigkeiten installieren
pip install -r requirements.txt (bzw. pymupdf indic-transliteration weasyprint)

# 2. Textzeugen auswerten und Master-JSON erzeugen
python scripts/align_brhadaranyaka.py

# 3. Synoptisches HTML & Satz-PDF kompilieren
python scripts/build_brhadaranyaka.py

# 4. TEI-P5 XML exportieren
python scripts/export_brhadaranyaka_tei.py

# 5. EPUB 3 generieren
python scripts/build_brhadaranyaka_epub.py

# 6. QA-Viewer neu generieren
python scripts/generate_viewer.py
```

---

## 📄 Lizenz

* Der Quellcode und die Datenstrukturen stehen unter der [MIT License](LICENSE).
* Die wissenschaftlichen Zitate der Übersetzungen von Otto von Böhtlingk (1889, gemeinfrei) und Walter Slaje (2009) dienen ausschließlich wissenschaftlich-kritischen und philologischen Zwecken gem. § 51 UrhG.

#!/usr/bin/env python3
"""
AlexandriaSandwich — Generates QA Viewer & Editor for Bṛhadāraṇyaka-Upaniṣad I.4
Implements the QA Viewer Pattern (Global Web Editor Standard) + Interactive Word-Click Popover:
1. Split-Pane Layout (Preview left, editable source right)
2. Local Storage First (File System Access API + localStorage fallback)
3. Snippet Toolbar (IAST diacritics, Devanagari marks, philological brackets)
4. Silent Auto-Repair on Save (Auto-repairs syntax/punctuation silently, save button blinks yellow)
5. Interactive Word-Click Popover for detailed grammatical analysis (Padapāṭha, Lemma, POS, Morph, Gloss)
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path("/Volumes/SanDisk1TB/proj/brhadaranyaka")
OUT_DIR = ROOT / "data" / "output"
MASTER_JSON = OUT_DIR / "brhadaranyaka_1_4_master.json"
VIEWER_HTML = ROOT / "viewer.html"


def generate_viewer() -> None:
    data = json.loads(MASTER_JSON.read_text(encoding="utf-8"))
    json_str = json.dumps(data, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>QA Viewer & Editor — Bṛhadāraṇyaka-Upaniṣad I.4</title>
<style>
:root {{
    --bg: #f8fafc;
    --panel-bg: #ffffff;
    --border: #e2e8f0;
    --text: #0f172a;
    --text-muted: #64748b;
    --primary: #8b1e22;
    --primary-hover: #70161a;
    --primary-light: #fef2f2;
    --accent: #2563eb;
    --accent-light: #eff6ff;
    --gold: #d97706;
    --gold-light: #fef3c7;
    --warning: #f59e0b;
    --success: #10b981;
    --radius: 6px;
    --font-serif: 'EB Garamond', 'Linux Libertine O', Georgia, serif;
    --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
    --font-deva: 'Devanagari MT', 'Noto Sans Devanagari', 'Shobhika', serif;
    --font-mono: 'JetBrains Mono', 'Fira Code', Menlo, Consolas, monospace;
}}

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: var(--font-sans);
    background: var(--bg);
    color: var(--text);
    height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}}

/* Top App Header */
header.app-header {{
    background: #1e293b;
    color: #ffffff;
    height: 52px;
    padding: 0 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid #334155;
    flex-shrink: 0;
}}

.app-title-group {{
    display: flex;
    align-items: center;
    gap: 12px;
}}

.app-badge {{
    background: var(--primary);
    color: #fff;
    font-size: 11px;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 4px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}}

.app-title {{
    font-size: 15px;
    font-weight: 600;
    letter-spacing: -0.01em;
}}

.app-subtitle {{
    font-size: 12px;
    color: #94a3b8;
    margin-left: 4px;
}}

.app-controls {{
    display: flex;
    align-items: center;
    gap: 8px;
}}

/* Buttons */
.btn {{
    font-family: var(--font-sans);
    font-size: 12px;
    font-weight: 500;
    padding: 6px 12px;
    border-radius: var(--radius);
    border: 1px solid transparent;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    transition: all 0.15s ease;
    white-space: nowrap;
}}

.btn-primary {{
    background: var(--primary);
    color: #ffffff;
}}
.btn-primary:hover {{
    background: var(--primary-hover);
}}

.btn-secondary {{
    background: #334155;
    color: #f1f5f9;
    border-color: #475569;
}}
.btn-secondary:hover {{
    background: #475569;
}}

.btn-outline {{
    background: transparent;
    color: #f1f5f9;
    border-color: #475569;
}}
.btn-outline:hover {{
    background: rgba(255,255,255,0.08);
}}

/* Blinking Animation for Silent Auto-Repair on Save */
@keyframes saveYellowBlink {{
    0% {{ background: #f59e0b; color: #000; }}
    50% {{ background: #fde68a; color: #000; }}
    100% {{ background: var(--primary); color: #fff; }}
}}

.btn-save-repair {{
    animation: saveYellowBlink 0.65s ease-in-out;
}}

.save-status {{
    font-size: 12px;
    color: #10b981;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    opacity: 0;
    transition: opacity 0.3s ease;
}}
.save-status.show {{
    opacity: 1;
}}

/* Split Pane Container */
.split-container {{
    flex: 1;
    display: flex;
    overflow: hidden;
}}

/* Navigation Sidebar */
.nav-sidebar {{
    width: 220px;
    background: var(--panel-bg);
    border-right: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    flex-shrink: 0;
}}

.sidebar-header {{
    padding: 10px 14px;
    border-bottom: 1px solid var(--border);
    font-size: 12px;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.verse-list {{
    flex: 1;
    overflow-y: auto;
    list-style: none;
}}

.verse-item {{
    padding: 9px 14px;
    border-bottom: 1px solid #f1f5f9;
    cursor: pointer;
    font-size: 13px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    transition: background 0.1s;
}}
.verse-item:hover {{
    background: #f8fafc;
}}
.verse-item.active {{
    background: var(--primary-light);
    border-left: 3px solid var(--primary);
    font-weight: 600;
    color: var(--primary);
}}

.verse-item-tag {{
    font-size: 10px;
    color: var(--text-muted);
    font-family: var(--font-mono);
}}

/* Main Workspace (Preview + Editor) */
.workspace {{
    flex: 1;
    display: grid;
    grid-template-columns: 1fr 1fr;
    overflow: hidden;
}}

/* Left Pane: Preview */
.preview-pane {{
    border-right: 1px solid var(--border);
    background: #ffffff;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    position: relative;
}}

.pane-header {{
    height: 44px;
    padding: 0 16px;
    border-bottom: 1px solid var(--border);
    background: #fcfdfe;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-shrink: 0;
}}

.pane-title {{
    font-size: 13px;
    font-weight: 600;
    color: var(--text);
    display: flex;
    align-items: center;
    gap: 8px;
}}

.preview-tabs {{
    display: flex;
    gap: 4px;
}}

.tab-btn {{
    font-size: 11px;
    font-weight: 500;
    padding: 4px 10px;
    border-radius: 4px;
    border: 1px solid transparent;
    background: transparent;
    color: var(--text-muted);
    cursor: pointer;
}}
.tab-btn.active {{
    background: var(--accent-light);
    color: var(--accent);
    border-color: #bfdbfe;
    font-weight: 600;
}}

.preview-body {{
    flex: 1;
    overflow-y: auto;
    padding: 24px;
}}

/* Preview Typography */
.preview-card {{
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.03);
}}

.prev-badge {{
    display: inline-block;
    background: var(--primary);
    color: #fff;
    font-size: 11px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 3px;
    margin-bottom: 12px;
}}

.prev-deva {{
    font-family: var(--font-deva);
    font-size: 18px;
    line-height: 1.65;
    color: #111;
    margin-bottom: 12px;
    padding-bottom: 12px;
    border-bottom: 1px dashed #e2e8f0;
}}

.prev-iast {{
    font-family: var(--font-serif);
    font-size: 15px;
    color: #334155;
    line-height: 1.7;
    margin-bottom: 16px;
    padding: 10px 14px;
    background: #f8fafc;
    border-radius: 6px;
    border: 1px solid #e2e8f0;
}}

.iast-hint {{
    display: block;
    font-family: var(--font-sans);
    font-size: 10.5px;
    color: var(--gold);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 6px;
}}

/* Interactive Word Tokens */
.iast-token-interactive {{
    cursor: pointer;
    font-style: italic;
    padding: 1px 3px;
    margin: 0 1px;
    border-radius: 3px;
    border-bottom: 1.5px dotted var(--primary);
    transition: all 0.15s ease;
    display: inline-block;
}}
.iast-token-interactive:hover {{
    background: var(--gold-light);
    color: #b45309;
    border-bottom-color: #b45309;
}}
.iast-token-interactive.active {{
    background: #fef3c7;
    color: #92400e;
    font-weight: 600;
    border-bottom: 2px solid #b45309;
}}

/* Floating Grammar Popover */
.grammar-popover {{
    position: fixed;
    z-index: 999999;
    width: 320px;
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.25), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
    padding: 14px;
    font-family: var(--font-sans);
    font-size: 12px;
    display: none;
    animation: popoverFadeIn 0.15s ease-out;
}}

@keyframes popoverFadeIn {{
    from {{ opacity: 0; transform: translateY(-4px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

.popover-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 8px;
    margin-bottom: 10px;
}}

.popover-token-title {{
    font-family: var(--font-serif);
    font-size: 16px;
    font-weight: 700;
    font-style: italic;
    color: var(--primary);
}}

.popover-close-btn {{
    background: transparent;
    border: none;
    color: #94a3b8;
    cursor: pointer;
    font-size: 16px;
    line-height: 1;
    padding: 2px 4px;
}}
.popover-close-btn:hover {{
    color: #0f172a;
}}

.popover-sandhi-bar {{
    background: #f1f5f9;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 11.5px;
    color: #475569;
    margin-bottom: 10px;
    font-family: var(--font-serif);
}}
.popover-sandhi-label {{
    font-weight: 700;
    text-transform: uppercase;
    font-size: 9.5px;
    color: var(--text-muted);
    margin-right: 4px;
}}

.popover-words-list {{
    display: flex;
    flex-direction: column;
    gap: 8px;
}}

.popover-word-entry {{
    padding: 8px 10px;
    background: #f8fafc;
    border-left: 3px solid var(--accent);
    border-radius: 4px;
}}

.popover-word-head {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 3px;
}}

.popover-word-form {{
    font-family: var(--font-serif);
    font-size: 14px;
    font-weight: 700;
    color: #1e293b;
}}

.popover-word-pos {{
    background: #e0f2fe;
    color: #0369a1;
    font-size: 10px;
    font-weight: 600;
    padding: 1px 6px;
    border-radius: 3px;
    text-transform: uppercase;
}}

.popover-word-lemma {{
    font-size: 11px;
    color: #64748b;
    margin-bottom: 4px;
}}
.popover-word-lemma-val {{
    font-family: var(--font-serif);
    font-style: italic;
    color: #0f172a;
    font-weight: 600;
}}

.popover-word-morph {{
    font-size: 11.5px;
    font-weight: 600;
    color: #334155;
    margin-bottom: 3px;
}}

.popover-word-gloss {{
    font-family: var(--font-serif);
    font-size: 12.5px;
    color: #8b1e22;
    font-style: italic;
}}

.prev-trans-block {{
    margin-top: 14px;
    padding: 12px;
    border-radius: 6px;
    background: #f8fafc;
    border-left: 3px solid #cbd5e1;
}}
.prev-trans-block.slaje {{
    border-left-color: var(--primary);
    background: #fffafa;
}}

.prev-trans-label {{
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--primary);
    margin-bottom: 4px;
}}
.prev-trans-label.boht {{
    color: #475569;
}}

.prev-trans-text {{
    font-family: var(--font-serif);
    font-size: 13.5px;
    line-height: 1.55;
    color: #1e293b;
}}

.prev-comm-box {{
    margin-top: 16px;
    padding: 12px;
    background: #fdfaf5;
    border: 1px solid #f1e7d8;
    border-radius: 6px;
}}

.prev-comm-title {{
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #854d0e;
    margin-bottom: 8px;
}}

.prev-comm-item {{
    font-size: 12.5px;
    line-height: 1.5;
    margin-bottom: 6px;
    color: #334155;
}}
.prev-comm-lemma {{
    font-weight: 600;
    color: var(--primary);
}}

/* Right Pane: Editable Source */
.editor-pane {{
    background: #ffffff;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}}

/* Snippet Toolbar (Global Web Editor Standard Requirement 3) */
.snippet-toolbar {{
    padding: 6px 12px;
    background: #f8fafc;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    gap: 4px;
    flex-wrap: wrap;
    flex-shrink: 0;
}}

.snippet-group-label {{
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-right: 2px;
}}

.snippet-btn {{
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 3px;
    padding: 2px 7px;
    font-size: 12px;
    cursor: pointer;
    font-family: var(--font-serif);
    color: #0f172a;
    transition: all 0.1s;
}}
.snippet-btn:hover {{
    background: #eff6ff;
    border-color: #3b82f6;
    color: #1d4ed8;
}}
.snippet-btn.deva {{
    font-family: var(--font-deva);
    font-size: 13px;
}}

.snippet-divider {{
    width: 1px;
    height: 16px;
    background: #cbd5e1;
    margin: 0 4px;
}}

/* Form Fields for Active Verse */
.editor-body {{
    flex: 1;
    overflow-y: auto;
    padding: 16px 20px;
}}

.form-group {{
    margin-bottom: 14px;
}}

.form-label {{
    display: block;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: var(--text-muted);
    margin-bottom: 4px;
}}

.form-textarea {{
    width: 100%;
    padding: 8px 10px;
    border: 1px solid var(--border);
    border-radius: 5px;
    font-size: 13px;
    line-height: 1.5;
    color: var(--text);
    background: #ffffff;
    resize: vertical;
    transition: border-color 0.15s;
}}
.form-textarea:focus {{
    outline: none;
    border-color: var(--accent);
    box-shadow: 0 0 0 2px rgba(37,99,235,0.1);
}}
.form-textarea.deva {{
    font-family: var(--font-deva);
    font-size: 15px;
}}
.form-textarea.iast {{
    font-family: var(--font-serif);
    font-size: 13.5px;
    font-style: italic;
}}
.form-textarea.german {{
    font-family: var(--font-serif);
    font-size: 13px;
}}
</style>
</head>
<body>

<header class="app-header">
    <div class="app-title-group">
        <span class="app-badge">QA Viewer</span>
        <span class="app-title">Bṛhadāraṇyaka-Upaniṣad I.4</span>
        <span class="app-subtitle">— Synoptischer Text & Stellenkommentar (31 Abschnitte)</span>
        <a href="index.html" style="color: #94a3b8; text-decoration: none; font-size: 12px; margin-left: 10px;">← Startseite</a>
        <a href="synopsis.html" style="color: #94a3b8; text-decoration: none; font-size: 12px; margin-left: 6px;">📖 Lesefassung</a>
    </div>

    <div class="app-controls">
        <span id="saveStatus" class="save-status">✓ Gespeichert & repariert</span>
        <button id="btnReset" class="btn btn-outline" onclick="resetToMasterData()" title="Setzt Daten & Grammatik auf Originalstand zurück">↺ Reset</button>
        <button id="btnOpen" class="btn btn-secondary" onclick="openLocalFile()">📂 Öffnen</button>
        <button id="btnSave" class="btn btn-primary" onclick="silentAutoRepairAndSave()">💾 Speichern</button>
        <button id="btnExportJson" class="btn btn-outline" onclick="exportJsonFile()">⬇ JSON Export</button>
    </div>
</header>

<div class="split-container">
    <!-- Left Navigation Sidebar -->
    <nav class="nav-sidebar">
        <div class="sidebar-header">
            <span>Abschnitte (1.4.1 – 31)</span>
            <span id="verseCount" style="font-family: var(--font-mono); font-size: 11px;">31</span>
        </div>
        <ul id="verseList" class="verse-list"></ul>
    </nav>

    <!-- Main Split-Pane Workspace -->
    <main class="workspace">
        <!-- Pane 1: Preview (Left) -->
        <section class="preview-pane" id="previewPane">
            <div class="pane-header">
                <div class="pane-title">
                    <span>👁 Vorschau</span>
                    <span id="activeVerseTitle" style="color: var(--text-muted); font-weight: normal;">1.4.1</span>
                </div>
                <div class="preview-tabs">
                    <button class="tab-btn active" onclick="setPreviewTab('synopsis', this)">Synopse</button>
                    <button class="tab-btn" onclick="setPreviewTab('slaje', this)">Slaje (2009)</button>
                    <button class="tab-btn" onclick="setPreviewTab('bohtlingk', this)">Böhtlingk (1889)</button>
                </div>
            </div>
            <div id="previewBody" class="preview-body"></div>
        </section>

        <!-- Pane 2: Editable Source (Right) -->
        <section class="editor-pane">
            <div class="pane-header">
                <div class="pane-title">✏️ Quell-Editor (QA Standard)</div>
                <div style="font-size: 11px; color: var(--text-muted);">Silent Auto-Repair aktiv</div>
            </div>

            <!-- Snippet Toolbar (Global Web Editor Standard Requirement 3) -->
            <div class="snippet-toolbar">
                <span class="snippet-group-label">IAST:</span>
                <button class="snippet-btn" onclick="insertSnippet('ā')">ā</button>
                <button class="snippet-btn" onclick="insertSnippet('ī')">ī</button>
                <button class="snippet-btn" onclick="insertSnippet('ū')">ū</button>
                <button class="snippet-btn" onclick="insertSnippet('ṛ')">ṛ</button>
                <button class="snippet-btn" onclick="insertSnippet('ṝ')">ṝ</button>
                <button class="snippet-btn" onclick="insertSnippet('ṃ')">ṃ</button>
                <button class="snippet-btn" onclick="insertSnippet('ḥ')">ḥ</button>
                <button class="snippet-btn" onclick="insertSnippet('ś')">ś</button>
                <button class="snippet-btn" onclick="insertSnippet('ṣ')">ṣ</button>
                <button class="snippet-btn" onclick="insertSnippet('ṇ')">ṇ</button>
                <button class="snippet-btn" onclick="insertSnippet('ṭ')">ṭ</button>
                <button class="snippet-btn" onclick="insertSnippet('ḍ')">ḍ</button>

                <div class="snippet-divider"></div>

                <span class="snippet-group-label">Deva:</span>
                <button class="snippet-btn deva" onclick="insertSnippet('।')">।</button>
                <button class="snippet-btn deva" onclick="insertSnippet('॥')">॥</button>
                <button class="snippet-btn deva" onclick="insertSnippet('ऽ')">ऽ</button>
                <button class="snippet-btn deva" onclick="insertSnippet('ँ')">ँ</button>

                <div class="snippet-divider"></div>

                <span class="snippet-group-label">Noten:</span>
                <button class="snippet-btn" onclick="insertSnippet('»', '«')">»...«</button>
                <button class="snippet-btn" onclick="insertSnippet('[', ']')">[...]</button>
                <button class="snippet-btn" onclick="insertSnippet('*', '*]')">*lemma*]</button>
            </div>

            <div class="editor-body">
                <div class="form-group">
                    <label class="form-label">Sanskrit Devanagari</label>
                    <textarea id="editDeva" class="form-textarea deva" rows="3" oninput="onFieldInput()"></textarea>
                </div>

                <div class="form-group">
                    <label class="form-label">Sanskrit IAST Transliteration</label>
                    <textarea id="editIast" class="form-textarea iast" rows="3" oninput="onFieldInput()"></textarea>
                </div>

                <div class="form-group">
                    <label class="form-label">Übersetzung Walter Slaje (2009)</label>
                    <textarea id="editSlaje" class="form-textarea german" rows="4" oninput="onFieldInput()"></textarea>
                </div>

                <div class="form-group">
                    <label class="form-label">Übersetzung Otto von Böhtlingk (1889)</label>
                    <textarea id="editBoht" class="form-textarea german" rows="4" oninput="onFieldInput()"></textarea>
                </div>

                <div class="form-group">
                    <label class="form-label">Philologischer Kommentar (Slaje 2009)</label>
                    <textarea id="editComm" class="form-textarea" rows="4" style="font-family: var(--font-mono); font-size: 11.5px;" oninput="onFieldInput()" placeholder='[{{"lemma": "*...", "text": "..."}}]'></textarea>
                </div>
            </div>
        </section>
    </main>
</div>

<!-- Floating Grammar Popover (Fixed Viewport Overlay) -->
<div id="grammarPopover" class="grammar-popover">
    <div class="popover-header">
        <span id="popoverTitle" class="popover-token-title">Token</span>
        <button class="popover-close-btn" onclick="hideGrammarPopover()">✕</button>
    </div>
    <div id="popoverSandhiBar" class="popover-sandhi-bar">
        <span class="popover-sandhi-label">Padapāṭha:</span>
        <span id="popoverSandhiVal">...</span>
    </div>
    <div id="popoverWordsList" class="popover-words-list"></div>
</div>

<script>
// Embedded Single Source of Truth Master Data
let MASTER_DATA = {json_str};
let activeIndex = 0;
let activeTab = 'synopsis';
let fileHandle = null;
let isInitialized = false;

// Initialize
window.addEventListener('DOMContentLoaded', () => {{
    const cached = localStorage.getItem('as_bau_1_4_data');
    if (cached) {{
        try {{
            const parsed = JSON.parse(cached);
            if (parsed && Array.isArray(parsed.sections)) {{
                // Auto-migrate grammar analysis if cached data lacks tokens
                const cachedTokens = parsed.sections.reduce((acc, s) => acc + (s.grammar_analysis ? s.grammar_analysis.length : 0), 0);
                const masterTokens = MASTER_DATA.sections.reduce((acc, s) => acc + (s.grammar_analysis ? s.grammar_analysis.length : 0), 0);
                
                if (cachedTokens < masterTokens) {{
                    console.log(`Auto-migrating grammar tokens into cached data (${{masterTokens}} master vs ${{cachedTokens}} cached)...`);
                    parsed.sections.forEach((sec, idx) => {{
                        const mSec = MASTER_DATA.sections[idx] || MASTER_DATA.sections.find(s => s.canonical_id === sec.canonical_id);
                        if (mSec && mSec.grammar_analysis && mSec.grammar_analysis.length > 0) {{
                            sec.grammar_analysis = mSec.grammar_analysis;
                        }}
                    }});
                    localStorage.setItem('as_bau_1_4_data', JSON.stringify(parsed));
                }}
                MASTER_DATA = parsed;
            }}
        }} catch(e) {{
            console.error('Error parsing localStorage:', e);
        }}
    }}
    renderVerseList();
    selectVerse(0);

    // Close popover when clicking elsewhere
    document.addEventListener('click', (e) => {{
        const pop = document.getElementById('grammarPopover');
        if (pop && pop.style.display === 'block') {{
            if (!pop.contains(e.target) && !e.target.closest('.iast-token-interactive')) {{
                hideGrammarPopover();
            }}
        }}
    }});
    // Close on escape
    document.addEventListener('keydown', (e) => {{
        if (e.key === 'Escape') hideGrammarPopover();
    }});
}});

function resetToMasterData() {{
    if (confirm("Möchten Sie alle Daten auf den Original-Masterstand (inklusive aller 1.087 grammatischen Wortanalysen) zurücksetzen?")) {{
        localStorage.removeItem('as_bau_1_4_data');
        location.reload();
    }}
}}

function renderVerseList() {{
    const listEl = document.getElementById('verseList');
    listEl.innerHTML = '';
    MASTER_DATA.sections.forEach((sec, idx) => {{
        const li = document.createElement('li');
        li.className = 'verse-item' + (idx === activeIndex ? ' active' : '');
        const hasGrammar = sec.grammar_analysis && sec.grammar_analysis.length > 0;
        li.innerHTML = `
            <span>BĀU ${{sec.canonical_id}}</span>
            <span class="verse-item-tag">${{hasGrammar ? '✨ ' + sec.grammar_analysis.length : ''}}</span>
        `;
        li.onclick = () => selectVerse(idx);
        listEl.appendChild(li);
    }});
    document.getElementById('verseCount').textContent = MASTER_DATA.sections.length;
}}

function selectVerse(idx) {{
    commitCurrentFormToMemory();
    hideGrammarPopover();

    activeIndex = idx;
    const sec = MASTER_DATA.sections[idx];

    document.querySelectorAll('.verse-item').forEach((el, i) => {{
        el.classList.toggle('active', i === idx);
    }});

    document.getElementById('activeVerseTitle').textContent = sec.title;

    document.getElementById('editDeva').value = sec.sanskrit_devanagari || '';
    document.getElementById('editIast').value = sec.sanskrit_iast || '';
    document.getElementById('editSlaje').value = sec.translation_slaje || '';
    document.getElementById('editBoht').value = sec.translation_bohtlingk || '';
    document.getElementById('editComm').value = JSON.stringify(sec.commentary_slaje || [], null, 2);

    renderPreview();
    isInitialized = true;
}}

function commitCurrentFormToMemory() {{
    if (!isInitialized) return;
    if (!MASTER_DATA.sections || !MASTER_DATA.sections[activeIndex]) return;
    const sec = MASTER_DATA.sections[activeIndex];
    sec.sanskrit_devanagari = document.getElementById('editDeva').value;
    sec.sanskrit_iast = document.getElementById('editIast').value;
    sec.translation_slaje = document.getElementById('editSlaje').value;
    sec.translation_bohtlingk = document.getElementById('editBoht').value;
    try {{
        sec.commentary_slaje = JSON.parse(document.getElementById('editComm').value);
    }} catch(e) {{}}
}}

function onFieldInput() {{
    commitCurrentFormToMemory();
    renderPreview();
}}

function setPreviewTab(tab, btn) {{
    activeTab = tab;
    hideGrammarPopover();
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    renderPreview();
}}

function renderInteractiveIast(sec) {{
    if (!sec.grammar_analysis || sec.grammar_analysis.length === 0) {{
        return escapeHtml(sec.sanskrit_iast || '');
    }}

    return sec.grammar_analysis.map((t, idx) => {{
        const tokText = escapeHtml(t.token || '');
        if (tokText === '|' || tokText === '||') {{
            return `<span style="color:#94a3b8;font-style:normal;margin:0 2px;">${{tokText}}</span>`;
        }}
        return `<span class="iast-token-interactive" data-token-idx="${{idx}}" onclick="showGrammarPopover(event, ${{idx}})">${{tokText}}</span>`;
    }}).join(' ');
}}

function showGrammarPopover(event, tokenIdx) {{
    if (event) {{
        event.stopPropagation();
    }}
    const sec = MASTER_DATA.sections[activeIndex];
    if (!sec || !sec.grammar_analysis || !sec.grammar_analysis[tokenIdx]) return;

    const tokenData = sec.grammar_analysis[tokenIdx];
    const targetEl = (event.currentTarget || event.target).closest('.iast-token-interactive') || event.currentTarget || event.target;
    const pop = document.getElementById('grammarPopover');
    if (!pop || !targetEl) return;

    // Remove active state on other tokens
    document.querySelectorAll('.iast-token-interactive').forEach(el => el.classList.remove('active'));
    targetEl.classList.add('active');

    // Fill content
    document.getElementById('popoverTitle').textContent = tokenData.token || '';
    document.getElementById('popoverSandhiVal').textContent = tokenData.sandhi || tokenData.token || '';

    const listEl = document.getElementById('popoverWordsList');
    listEl.innerHTML = '';
    const words = tokenData.words || [];

    if (words.length === 0) {{
        listEl.innerHTML = '<div style="color:#64748b;font-size:11px;">Keine morphologische Zerlegung hinterlegt.</div>';
    }} else {{
        words.forEach(w => {{
            const div = document.createElement('div');
            div.className = 'popover-word-entry';
            div.innerHTML = `
                <div class="popover-word-head">
                    <span class="popover-word-form">${{escapeHtml(w.form || '')}}</span>
                    <span class="popover-word-pos">${{escapeHtml(w.pos || '')}}</span>
                </div>
                <div class="popover-word-lemma">
                    Stamm/Wurzel: <span class="popover-word-lemma-val">${{escapeHtml(w.lemma || '')}}</span>
                </div>
                <div class="popover-word-morph">${{escapeHtml(w.morph || '')}}</div>
                <div class="popover-word-gloss">»${{escapeHtml(w.gloss || '')}}«</div>
            `;
            listEl.appendChild(div);
        }});
    }}

    // Display popover to compute rendered size
    pop.style.display = 'block';

    const rect = targetEl.getBoundingClientRect();
    const popWidth = pop.offsetWidth || 320;
    const popHeight = pop.offsetHeight || 260;

    let left = rect.left;
    let top = rect.bottom + 6;

    // Clamping to viewport
    if (left + popWidth > window.innerWidth - 12) {{
        left = Math.max(12, window.innerWidth - popWidth - 12);
    }}
    if (left < 12) {{
        left = 12;
    }}

    if (top + popHeight > window.innerHeight - 12) {{
        const flippedTop = rect.top - popHeight - 6;
        if (flippedTop >= 12) {{
            top = flippedTop;
        }} else {{
            top = Math.max(12, window.innerHeight - popHeight - 12);
        }}
    }}

    pop.style.left = Math.round(left) + 'px';
    pop.style.top = Math.round(top) + 'px';
}}

function hideGrammarPopover() {{
    const pop = document.getElementById('grammarPopover');
    if (pop) pop.style.display = 'none';
    document.querySelectorAll('.iast-token-interactive').forEach(el => el.classList.remove('active'));
}}

function renderPreview() {{
    const sec = MASTER_DATA.sections[activeIndex];
    const previewEl = document.getElementById('previewBody');

    let commHtml = '';
    if (sec.commentary_slaje && sec.commentary_slaje.length > 0) {{
        commHtml = `
            <div class="prev-comm-box">
                <div class="prev-comm-title">Philologischer Kommentar (Slaje 2009)</div>
                ${{sec.commentary_slaje.map(c => `
                    <div class="prev-comm-item">
                        <span class="prev-comm-lemma">${{escapeHtml(c.lemma || '')}}</span>
                        <span>${{escapeHtml(c.text || '')}}</span>
                    </div>
                `).join('')}}
            </div>
        `;
    }}

    const iastHtml = renderInteractiveIast(sec);

    if (activeTab === 'synopsis') {{
        previewEl.innerHTML = `
            <div class="preview-card">
                <span class="prev-badge">BĀU ${{sec.canonical_id}}</span>
                <div class="prev-deva">${{escapeHtml(sec.sanskrit_devanagari)}}</div>
                
                <div class="prev-iast">
                    <span class="iast-hint">💡 Klick auf ein Wort öffnet die grammatische Analyse:</span>
                    ${{iastHtml}}
                </div>

                <div class="prev-trans-block slaje">
                    <div class="prev-trans-label">Walter Slaje (2009) — Ursubjekt</div>
                    <div class="prev-trans-text">${{escapeHtml(sec.translation_slaje)}}</div>
                </div>

                <div class="prev-trans-block">
                    <div class="prev-trans-label boht">Otto von Böhtlingk (1889)</div>
                    <div class="prev-trans-text">${{escapeHtml(sec.translation_bohtlingk)}}</div>
                </div>

                ${{commHtml}}
            </div>
        `;
    }} else if (activeTab === 'slaje') {{
        previewEl.innerHTML = `
            <div class="preview-card">
                <span class="prev-badge">Walter Slaje (2009) · BĀU ${{sec.canonical_id}}</span>
                <div class="prev-trans-text" style="font-size: 15px; line-height: 1.7; margin-bottom: 16px;">
                    ${{escapeHtml(sec.translation_slaje)}}
                </div>
                ${{commHtml}}
            </div>
        `;
    }} else if (activeTab === 'bohtlingk') {{
        previewEl.innerHTML = `
            <div class="preview-card">
                <span class="prev-badge" style="background: #475569;">Böhtlingk (1889) · BĀU ${{sec.canonical_id}}</span>
                <div class="prev-trans-text" style="font-size: 15px; line-height: 1.7;">
                    ${{escapeHtml(sec.translation_bohtlingk)}}
                </div>
            </div>
        `;
    }}
}}

function escapeHtml(str) {{
    return (str || '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}}

/* Snippet Insertion */
function insertSnippet(before, after = '') {{
    const activeEl = document.activeElement;
    if (!activeEl || activeEl.tagName !== 'TEXTAREA') return;

    const start = activeEl.selectionStart;
    const end = activeEl.selectionEnd;
    const text = activeEl.value;
    const selected = text.substring(start, end);

    activeEl.value = text.substring(0, start) + before + selected + after + text.substring(end);
    activeEl.focus();
    activeEl.selectionStart = start + before.length;
    activeEl.selectionEnd = start + before.length + selected.length;

    onFieldInput();
}}

/* Requirement 4: Silent Auto-Repair on Save (Global Web Editor Standard) */
function silentAutoRepairAndSave() {{
    commitCurrentFormToMemory();

    MASTER_DATA.sections.forEach(sec => {{
        if (sec.sanskrit_iast) {{
            sec.sanskrit_iast = sec.sanskrit_iast.replace(/\\u00a0/g, ' ').replace(/\\s+/g, ' ').trim();
        }}
        if (sec.sanskrit_devanagari) {{
            sec.sanskrit_devanagari = sec.sanskrit_devanagari.replace(/\\u00a0/g, ' ').replace(/\\s+/g, ' ').trim();
            sec.sanskrit_devanagari = sec.sanskrit_devanagari.replace(/\\s*।\\s*/g, ' । ').replace(/\\s*॥\\s*/g, ' ॥ ').trim();
        }}
        if (sec.translation_slaje) {{
            sec.translation_slaje = sec.translation_slaje.replace(/\\u00a0/g, ' ').replace(/\\s+/g, ' ').trim();
        }}
        if (sec.translation_bohtlingk) {{
            sec.translation_bohtlingk = sec.translation_bohtlingk.replace(/\\u00a0/g, ' ').replace(/\\s+/g, ' ').trim();
        }}
    }});

    selectVerse(activeIndex);

    localStorage.setItem('as_bau_1_4_data', JSON.stringify(MASTER_DATA));

    if (fileHandle) {{
        writeToHandle(fileHandle, JSON.stringify(MASTER_DATA, null, 2));
    }}

    const saveBtn = document.getElementById('btnSave');
    saveBtn.classList.remove('btn-save-repair');
    void saveBtn.offsetWidth;
    saveBtn.classList.add('btn-save-repair');

    const statusEl = document.getElementById('saveStatus');
    statusEl.classList.add('show');
    setTimeout(() => {{
        statusEl.classList.remove('show');
    }}, 2000);
}}

/* Local Storage First & File System Access API */
async function openLocalFile() {{
    try {{
        if ('showOpenFilePicker' in window) {{
            const [handle] = await window.showOpenFilePicker({{
                types: [{{ description: 'JSON Files', accept: {{ 'application/json': ['.json'] }} }}]
            }});
            fileHandle = handle;
            const file = await handle.getFile();
            const text = await file.text();
            MASTER_DATA = JSON.parse(text);
            localStorage.setItem('as_bau_1_4_data', JSON.stringify(MASTER_DATA));
            renderVerseList();
            selectVerse(0);
        }} else {{
            const input = document.createElement('input');
            input.type = 'file';
            input.accept = '.json';
            input.onchange = (e) => {{
                const file = e.target.files[0];
                const reader = new FileReader();
                reader.onload = (event) => {{
                    MASTER_DATA = JSON.parse(event.target.result);
                    localStorage.setItem('as_bau_1_4_data', JSON.stringify(MASTER_DATA));
                    renderVerseList();
                    selectVerse(0);
                }};
                reader.readAsText(file);
            }};
            input.click();
        }}
    }} catch(e) {{
        console.warn('Open file cancelled or failed:', e);
    }}
}}

async function writeToHandle(handle, content) {{
    try {{
        const writable = await handle.createWritable();
        await writable.write(content);
        await writable.close();
    }} catch(e) {{
        console.warn('Direct file write failed, fallback to local storage:', e);
    }}
}}

function exportJsonFile() {{
    silentAutoRepairAndSave();
    const blob = new Blob([JSON.stringify(MASTER_DATA, null, 2)], {{ type: 'application/json' }});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'brhadaranyaka_1_4_master.json';
    a.click();
    URL.revokeObjectURL(url);
}}
</script>
</body>
</html>
"""

    VIEWER_HTML.write_text(html, encoding="utf-8")
    print(f"-> Successfully generated QA Viewer: {VIEWER_HTML} ({VIEWER_HTML.stat().st_size} bytes)")


if __name__ == "__main__":
    generate_viewer()

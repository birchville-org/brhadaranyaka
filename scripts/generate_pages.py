#!/usr/bin/env python3
"""
AlexandriaSandwich / Bṛhadāraṇyaka — GitHub Pages Website Generator
Builds a showcase web experience with interactive Word-Click Popover for grammar analysis:
1. index.html (Landing Page + Interactive Explorer with Word-by-Word Grammatical Glossing)
2. synopsis.html (Full 31-verse reading edition with navigation)
3. Copies viewer.html to data/output/viewer.html for parity
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path("/Volumes/SanDisk1TB/proj/brhadaranyaka")
DATA_FILE = ROOT / "data" / "output" / "brhadaranyaka_1_4_master.json"


def build_index_html(data: dict) -> str:
    work = data["work"]
    data_json_str = json.dumps(data, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bṛhadāraṇyaka-Upaniṣad I.4 — Das Ursubjekt & Schöpfungsmythos</title>
<meta name="description" content="Synoptische philologische Edition, Master-JSON, TEI-P5 XML & interaktiver QA-Viewer für Bṛhadāraṇyaka-Upaniṣad 1.4.1–1.4.31 (Mādhyandina-Rezension).">

<!-- Google Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;900&family=EB+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Inter:wght@400;500;600;700&family=Noto+Sans+Devanagari:wght@400;600;700&display=swap" rel="stylesheet">

<style>
:root {{
    --bg-base: #0b0f17;
    --bg-surface: #131b2a;
    --bg-surface-elevated: #1a253a;
    --bg-card: rgba(22, 32, 50, 0.75);
    --border-subtle: rgba(255, 255, 255, 0.08);
    --border-accent: rgba(184, 51, 42, 0.35);
    
    --primary: #c93b3b;
    --primary-light: #e55353;
    --primary-dark: #8b1e22;
    --primary-glow: rgba(201, 59, 59, 0.25);
    
    --gold: #d97706;
    --gold-light: #fbbf24;
    --gold-glow: rgba(217, 119, 6, 0.2);
    
    --text-main: #f1f5f9;
    --text-muted: #94a3b8;
    --text-dim: #64748b;
    
    --font-heading: 'Cinzel', serif;
    --font-serif: 'EB Garamond', Georgia, serif;
    --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    --font-deva: 'Noto Sans Devanagari', 'Devanagari MT', serif;
    
    --radius-sm: 6px;
    --radius-md: 10px;
    --radius-lg: 16px;
    --transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}}

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    background-color: var(--bg-base);
    color: var(--text-main);
    font-family: var(--font-sans);
    line-height: 1.6;
    overflow-x: hidden;
    background-image: 
        radial-gradient(circle at 15% 20%, rgba(139, 30, 34, 0.15) 0%, transparent 45%),
        radial-gradient(circle at 85% 65%, rgba(217, 119, 6, 0.08) 0%, transparent 50%),
        radial-gradient(circle at 50% 90%, rgba(37, 99, 235, 0.06) 0%, transparent 60%);
    background-attachment: fixed;
}}

/* Navigation Bar */
nav.global-nav {{
    position: sticky;
    top: 0;
    z-index: 100;
    background: rgba(11, 15, 23, 0.85);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-bottom: 1px solid var(--border-subtle);
    padding: 0.75rem 2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}}

.nav-brand {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
    text-decoration: none;
    color: var(--text-main);
}}

.brand-badge {{
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
    color: #fff;
    font-family: var(--font-heading);
    font-size: 0.75rem;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: var(--radius-sm);
    letter-spacing: 0.08em;
    box-shadow: 0 0 12px var(--primary-glow);
}}

.brand-title {{
    font-family: var(--font-heading);
    font-size: 1.05rem;
    font-weight: 700;
    letter-spacing: 0.03em;
    background: linear-gradient(180deg, #ffffff 0%, #cbd5e1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

.nav-links {{
    display: flex;
    align-items: center;
    gap: 1.5rem;
}}

.nav-link {{
    color: var(--text-muted);
    text-decoration: none;
    font-size: 0.875rem;
    font-weight: 500;
    transition: var(--transition);
}}
.nav-link:hover {{
    color: var(--text-main);
}}

.btn-nav {{
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
    color: #fff;
    text-decoration: none;
    font-size: 0.85rem;
    font-weight: 600;
    padding: 0.5rem 1rem;
    border-radius: var(--radius-sm);
    box-shadow: 0 0 14px var(--primary-glow);
    transition: var(--transition);
    border: 1px solid rgba(255,255,255,0.1);
}}
.btn-nav:hover {{
    transform: translateY(-1px);
    box-shadow: 0 0 20px var(--primary-glow);
}}

/* Hero Section */
header.hero {{
    max-width: 1200px;
    margin: 4rem auto 3rem auto;
    padding: 0 2rem;
    text-align: center;
}}

.hero-tag {{
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(201, 59, 59, 0.12);
    border: 1px solid var(--border-accent);
    color: var(--primary-light);
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    padding: 0.35rem 0.9rem;
    border-radius: 9999px;
    margin-bottom: 1.5rem;
}}

.hero-title {{
    font-family: var(--font-heading);
    font-size: 3.25rem;
    font-weight: 900;
    line-height: 1.15;
    letter-spacing: -0.01em;
    margin-bottom: 1rem;
    background: linear-gradient(180deg, #ffffff 20%, #cbd5e1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

.hero-subtitle {{
    font-family: var(--font-serif);
    font-size: 1.45rem;
    font-style: italic;
    color: var(--gold-light);
    margin-bottom: 1.5rem;
}}

.hero-desc {{
    max-width: 780px;
    margin: 0 auto 2.5rem auto;
    color: var(--text-muted);
    font-size: 1.1rem;
    line-height: 1.7;
}}

/* Primary Sanskrit Banner */
.sanskrit-quote-card {{
    max-width: 880px;
    margin: 0 auto 3rem auto;
    background: var(--bg-card);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid var(--border-accent);
    border-radius: var(--radius-lg);
    padding: 1.75rem 2.25rem;
    box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5);
    text-align: center;
    position: relative;
    overflow: hidden;
}}

.sanskrit-quote-card::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, transparent, var(--primary), var(--gold), transparent);
}}

.sanskrit-quote-deva {{
    font-family: var(--font-deva);
    font-size: 1.6rem;
    line-height: 1.6;
    color: #ffffff;
    margin-bottom: 0.75rem;
    letter-spacing: 0.02em;
}}

.sanskrit-quote-iast {{
    font-family: var(--font-serif);
    font-size: 1.05rem;
    font-style: italic;
    color: #cbd5e1;
    margin-bottom: 1rem;
}}

.sanskrit-quote-de {{
    font-family: var(--font-serif);
    font-size: 1.15rem;
    color: #f8fafc;
    line-height: 1.6;
}}

.sanskrit-quote-author {{
    margin-top: 0.75rem;
    font-size: 0.85rem;
    color: var(--gold-light);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}}

/* Action Matrix */
.actions-grid {{
    display: flex;
    justify-content: center;
    gap: 1rem;
    flex-wrap: wrap;
    margin-bottom: 4rem;
}}

.btn-action {{
    display: inline-flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.85rem 1.4rem;
    font-size: 0.95rem;
    font-weight: 600;
    border-radius: var(--radius-md);
    text-decoration: none;
    transition: var(--transition);
    cursor: pointer;
}}

.btn-primary-action {{
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
    color: #ffffff;
    border: 1px solid rgba(255,255,255,0.15);
    box-shadow: 0 4px 16px var(--primary-glow);
}}
.btn-primary-action:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 24px var(--primary-glow);
}}

.btn-secondary-action {{
    background: var(--bg-surface);
    color: var(--text-main);
    border: 1px solid var(--border-subtle);
}}
.btn-secondary-action:hover {{
    background: var(--bg-surface-elevated);
    border-color: rgba(255,255,255,0.2);
    transform: translateY(-2px);
}}

/* Main Explorer Section */
section.explorer {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem 5rem 2rem;
    position: relative;
}}

.section-header {{
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    margin-bottom: 2rem;
    border-bottom: 1px solid var(--border-subtle);
    padding-bottom: 1.25rem;
    gap: 1.5rem;
    flex-wrap: wrap;
}}

.section-title-group h2 {{
    font-family: var(--font-heading);
    font-size: 1.75rem;
    font-weight: 700;
    letter-spacing: 0.02em;
    color: #fff;
    margin-bottom: 0.35rem;
}}

.section-title-group p {{
    color: var(--text-muted);
    font-size: 0.95rem;
}}

.search-box {{
    position: relative;
    min-width: 280px;
}}

.search-input {{
    width: 100%;
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: 0.65rem 1rem 0.65rem 2.25rem;
    color: var(--text-main);
    font-size: 0.9rem;
    outline: none;
    transition: var(--transition);
}}
.search-input:focus {{
    border-color: var(--gold);
    box-shadow: 0 0 0 2px var(--gold-glow);
}}

.search-icon {{
    position: absolute;
    left: 0.75rem;
    top: 50%;
    transform: translateY(-50%);
    color: var(--text-dim);
    pointer-events: none;
}}

/* Verse Cards Container */
.verses-grid {{
    display: flex;
    flex-direction: column;
    gap: 1.75rem;
}}

.verse-card {{
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: 1.75rem 2rem;
    transition: var(--transition);
    position: relative;
}}
.verse-card:hover {{
    border-color: rgba(201, 59, 59, 0.4);
    box-shadow: 0 8px 30px -10px rgba(0,0,0,0.6);
}}

.verse-card-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.25rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid var(--border-subtle);
}}

.verse-canonical-badge {{
    background: var(--primary);
    color: #fff;
    font-family: var(--font-heading);
    font-size: 0.85rem;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 4px;
    letter-spacing: 0.05em;
}}

.verse-source-tag {{
    font-size: 0.8rem;
    color: var(--gold-light);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}

.verse-deva {{
    font-family: var(--font-deva);
    font-size: 1.4rem;
    line-height: 1.65;
    color: #ffffff;
    margin-bottom: 0.75rem;
}}

.verse-iast-container {{
    margin-bottom: 1.5rem;
    padding-bottom: 1.25rem;
    border-bottom: 1px dashed rgba(255,255,255,0.08);
}}

.iast-hint-banner {{
    font-size: 0.75rem;
    color: var(--gold-light);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.35rem;
}}

.verse-iast-tokens {{
    font-family: var(--font-serif);
    font-size: 1.15rem;
    color: #cbd5e1;
    line-height: 1.7;
}}

/* Clickable Word Token */
.iast-word-token {{
    cursor: pointer;
    font-style: italic;
    padding: 1px 4px;
    margin: 0 1px;
    border-radius: 4px;
    border-bottom: 1.5px dotted var(--primary-light);
    transition: var(--transition);
    display: inline-block;
}}
.iast-word-token:hover {{
    background: rgba(201, 59, 59, 0.2);
    color: #ffffff;
    border-bottom-color: var(--gold-light);
}}
.iast-word-token.active {{
    background: rgba(217, 119, 6, 0.3);
    color: #fff;
    border-bottom: 2px solid var(--gold-light);
}}

/* Floating Popover */
.interactive-popover {{
    position: fixed;
    z-index: 999999;
    width: 320px;
    background: rgba(19, 27, 42, 0.96);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--border-accent);
    border-radius: var(--radius-md);
    box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.8);
    padding: 16px;
    display: none;
    animation: popoverFadeIn 0.15s ease-out;
}}

@keyframes popoverFadeIn {{
    from {{ opacity: 0; transform: translateY(-4px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

.pop-head {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid var(--border-subtle);
    padding-bottom: 8px;
    margin-bottom: 10px;
}}

.pop-title {{
    font-family: var(--font-serif);
    font-size: 1.2rem;
    font-weight: 700;
    font-style: italic;
    color: var(--primary-light);
}}

.pop-close {{
    background: transparent;
    border: none;
    color: var(--text-dim);
    cursor: pointer;
    font-size: 1.1rem;
}}
.pop-close:hover {{
    color: #fff;
}}

.pop-sandhi {{
    background: rgba(255,255,255,0.04);
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.8rem;
    color: var(--text-muted);
    margin-bottom: 10px;
    font-family: var(--font-serif);
}}
.pop-sandhi-label {{
    color: var(--gold-light);
    font-weight: 700;
    text-transform: uppercase;
    font-size: 0.7rem;
    margin-right: 4px;
}}

.pop-words {{
    display: flex;
    flex-direction: column;
    gap: 8px;
}}

.pop-word-card {{
    background: rgba(11, 15, 23, 0.6);
    border-left: 3px solid var(--gold);
    border-radius: 4px;
    padding: 8px 10px;
}}

.pop-word-top {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 4px;
}}

.pop-word-form {{
    font-family: var(--font-serif);
    font-size: 1rem;
    font-weight: 700;
    color: #ffffff;
}}

.pop-word-pos {{
    background: rgba(37, 99, 235, 0.2);
    color: #93c5fd;
    font-size: 0.7rem;
    font-weight: 600;
    padding: 1px 6px;
    border-radius: 3px;
    text-transform: uppercase;
}}

.pop-word-lemma {{
    font-size: 0.8rem;
    color: var(--text-muted);
    margin-bottom: 4px;
}}
.pop-word-lemma-val {{
    font-family: var(--font-serif);
    font-style: italic;
    color: var(--gold-light);
    font-weight: 600;
}}

.pop-word-morph {{
    font-size: 0.85rem;
    font-weight: 600;
    color: #e2e8f0;
    margin-bottom: 3px;
}}

.pop-word-gloss {{
    font-family: var(--font-serif);
    font-size: 0.95rem;
    color: var(--primary-light);
    font-style: italic;
}}

.verse-synopsis-columns {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
    margin-bottom: 1.25rem;
}}

@media (max-width: 860px) {{
    .verse-synopsis-columns {{
        grid-template-columns: 1fr;
    }}
}}

.trans-panel {{
    background: rgba(11, 15, 23, 0.55);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: 1.2rem;
}}
.trans-panel.slaje {{
    border-left: 3px solid var(--primary);
}}
.trans-panel.bohtlingk {{
    border-left: 3px solid #64748b;
}}

.trans-meta-header {{
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 0.6rem;
    display: flex;
    justify-content: space-between;
}}
.trans-meta-header.slaje {{
    color: var(--primary-light);
}}
.trans-meta-header.bohtlingk {{
    color: #94a3b8;
}}

.trans-body {{
    font-family: var(--font-serif);
    font-size: 1.05rem;
    line-height: 1.6;
    color: #f1f5f9;
}}

/* Commentary Box */
.commentary-container {{
    margin-top: 1rem;
    background: rgba(217, 119, 6, 0.06);
    border: 1px solid rgba(217, 119, 6, 0.2);
    border-radius: var(--radius-md);
    padding: 1rem 1.25rem;
}}

.commentary-title {{
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--gold-light);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}}

.commentary-item {{
    font-size: 0.95rem;
    line-height: 1.5;
    color: #e2e8f0;
    margin-bottom: 0.5rem;
}}
.commentary-lemma {{
    font-weight: 600;
    color: var(--gold-light);
    margin-right: 0.4rem;
}}

/* Downloads & Artifacts Section */
section.artifacts {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem 5rem 2rem;
}}

.artifacts-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 1.25rem;
}}

.artifact-card {{
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: 1.5rem;
    text-decoration: none;
    color: var(--text-main);
    transition: var(--transition);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}}
.artifact-card:hover {{
    border-color: var(--gold);
    transform: translateY(-3px);
    box-shadow: 0 8px 24px -6px rgba(0,0,0,0.5);
}}

.artifact-type {{
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--gold-light);
    margin-bottom: 0.5rem;
}}

.artifact-name {{
    font-family: var(--font-heading);
    font-size: 1.15rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}}

.artifact-desc {{
    font-size: 0.875rem;
    color: var(--text-muted);
    line-height: 1.5;
    margin-bottom: 1.25rem;
}}

.artifact-link-action {{
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--primary-light);
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
}}

/* Footer */
footer.global-footer {{
    background: #070a10;
    border-top: 1px solid var(--border-subtle);
    padding: 3rem 2rem;
    text-align: center;
    color: var(--text-dim);
    font-size: 0.875rem;
}}

.footer-quote {{
    font-family: var(--font-serif);
    font-style: italic;
    color: var(--text-muted);
    margin-bottom: 1rem;
}}
</style>
</head>
<body>

<nav class="global-nav">
    <a href="#" class="nav-brand">
        <span class="brand-badge">BĀU I.4</span>
        <span class="brand-title">Bṛhadāraṇyaka-Upaniṣad</span>
    </a>
    <div class="nav-links">
        <a href="#explorer" class="nav-link">Synopse</a>
        <a href="synopsis.html" class="nav-link">Lesefassung</a>
        <a href="viewer.html" class="nav-link">QA-Viewer</a>
        <a href="#artifacts" class="nav-link">Downloads</a>
        <a href="https://github.com/birchville-org/brhadaranyaka" target="_blank" class="nav-link">GitHub ↗</a>
        <a href="viewer.html" class="btn-nav">🚀 Editor öffnen</a>
    </div>
</nav>

<header class="hero">
    <div class="hero-tag">Mādhyandina-Rezension · Kritische Synopse</div>
    <h1 class="hero-title">Bṛhadāraṇyaka-Upaniṣad I.4</h1>
    <div class="hero-subtitle">Das Ursubjekt (ātman) & der altindische Schöpfungsmythos</div>
    <p class="hero-desc">
        Vollständige philologische Gegenüberstellung von 31 kanonischen Textabschnitten:
        Kanonischer Sanskrit-Urtext (Devanagari & IAST mit interaktiver Wortgrammatik), 
        Walter Slajes moderne Rekonstruktion (2009), Otto von Böhtlingks historische Erstausgabe (1889) 
        und der 36-teilige Stellenkommentar.
    </p>

    <div class="sanskrit-quote-card">
        <div class="sanskrit-quote-deva">आत्मैवेदम् अग्र आसीत् पुरुषविधः । सो ऽनुवीक्ष्य नान्यद् आत्मनो ऽपश्यत् । सो ऽहम् अस्मीत्य् अग्रे व्याहरत् ।</div>
        <div class="sanskrit-quote-iast">ātmaivedam agra āsīt puruṣavidhaḥ | so 'nuvīkṣya nānyad ātmano 'paśyat | so 'ham asmīty agre vyāharat |</div>
        <div class="sanskrit-quote-de">»Am Anfang gab es hier nur das Ursubjekt (ātman) in Mannesgestalt. Als es umherblickte, sah es nichts anderes als sich selbst. ›Das da bin ich!‹ war, was es zuallererst aussprach.«</div>
        <div class="sanskrit-quote-author">— Bṛhadāraṇyaka-Upaniṣad 1.4.1</div>
    </div>

    <div class="actions-grid">
        <a href="viewer.html" class="btn-action btn-primary-action">
            <span>🚀 Interaktiven QA-Viewer starten</span>
        </a>
        <a href="synopsis.html" class="btn-action btn-secondary-action">
            <span>📖 Zur synoptischen Lesefassung</span>
        </a>
        <a href="data/output/brhadaranyaka_1_4_synopsis.pdf" target="_blank" class="btn-action btn-secondary-action">
            <span>📄 Satz-PDF (33 S.)</span>
        </a>
        <a href="data/output/brhadaranyaka_1_4.tei.xml" target="_blank" class="btn-action btn-secondary-action">
            <span>🏛️ TEI-P5 XML</span>
        </a>
    </div>
</header>

<section id="explorer" class="explorer">
    <div class="section-header">
        <div class="section-title-group">
            <h2>Kanonische Synopse (31 Abschnitte)</h2>
            <p>Vergleichende Lektüre mit interaktivem Wort-Popover: Klicke auf ein IAST-Wort zur grammatischen Analyse.</p>
        </div>
        <div class="search-box">
            <span class="search-icon">🔍</span>
            <input type="text" id="searchInput" class="search-input" placeholder="Sanskrit, Deutsch oder Noten durchsuchen..." oninput="filterVerses()">
        </div>
    </div>

    <div id="versesGrid" class="verses-grid"></div>
</section>

<section id="artifacts" class="artifacts">
    <div class="section-header">
        <div class="section-title-group">
            <h2>Editions-Artefakte & Download-Matrix</h2>
            <p>Sämtliche Zielformate der AlexandriaSandwich-Digitalisierungspipeline.</p>
        </div>
    </div>

    <div class="artifacts-grid">
        <a href="viewer.html" class="artifact-card">
            <div>
                <div class="artifact-type">Web Application</div>
                <div class="artifact-name">Interaktiver QA-Viewer</div>
                <div class="artifact-desc">Autarker Split-Pane Web-Editor mit File System Access API, Snippet-Toolbar, Silent Auto-Repair und Wortgrammatik-Popover.</div>
            </div>
            <span class="artifact-link-action">Viewer starten →</span>
        </a>

        <a href="synopsis.html" class="artifact-card">
            <div>
                <div class="artifact-type">Web Edition</div>
                <div class="artifact-name">Synoptische Lesefassung</div>
                <div class="artifact-desc">Kompakte Gesamtdarstellung aller 31 Abschnitte mit Sanskrit-Devanagari, IAST und vergleichender Übersetzung.</div>
            </div>
            <span class="artifact-link-action">Online lesen →</span>
        </a>

        <a href="data/output/brhadaranyaka_1_4_synopsis.pdf" target="_blank" class="artifact-card">
            <div>
                <div class="artifact-type">Print / Digital PDF</div>
                <div class="artifact-name">Satz-PDF (33 Seiten)</div>
                <div class="artifact-desc">Typografisch optimiertes Editions-PDF im A4-Format, gerendert mit WeasyPrint (EB Garamond & Noto Sans Devanagari).</div>
            </div>
            <span class="artifact-link-action">PDF herunterladen →</span>
        </a>

        <a href="data/output/brhadaranyaka_1_4.tei.xml" target="_blank" class="artifact-card">
            <div>
                <div class="artifact-type">Digital Humanities</div>
                <div class="artifact-name">TEI-P5 XML Archivformat</div>
                <div class="artifact-desc">Standardisiertes XML-Korpus nach Richtlinien der Text Encoding Initiative mit paralleler Schichtung aller Textzeugen.</div>
            </div>
            <span class="artifact-link-action">XML öffnen →</span>
        </a>

        <a href="data/output/brhadaranyaka_1_4.epub" target="_blank" class="artifact-card">
            <div>
                <div class="artifact-type">E-Reader eBook</div>
                <div class="artifact-name">Reflowable EPUB 3</div>
                <div class="artifact-desc">E-Book für E-Reader und Mobilgeräte mit fest eingebetteten Unicode-Schriften (Noto Serif Devanagari).</div>
            </div>
            <span class="artifact-link-action">EPUB 3 laden →</span>
        </a>

        <a href="data/output/slaje2009.sandwich.pdf" target="_blank" class="artifact-card">
            <div>
                <div class="artifact-type">1:1 Faksimile</div>
                <div class="artifact-name">1:1 Sandwich-PDF</div>
                <div class="artifact-desc">Archivkonformes PDF/A-2b mit hochauflösendem Originalscan und unsichtbarer, punktgenau durchsuchbarer Textebene.</div>
            </div>
            <span class="artifact-link-action">Sandwich-PDF öffnen →</span>
        </a>

        <a href="data/output/brhadaranyaka_1_4_master.json" target="_blank" class="artifact-card">
            <div>
                <div class="artifact-type">Single Source of Truth</div>
                <div class="artifact-name">Master JSON (AST)</div>
                <div class="artifact-desc">Vollständiger strukturierter Datenbaum aller 31 Verse, 1.087 grammatischen Tokens und 36 philologischen Kommentare.</div>
            </div>
            <span class="artifact-link-action">JSON betrachten →</span>
        </a>

        <a href="data/output/brhadaranyaka_1_4_master.md" target="_blank" class="artifact-card">
            <div>
                <div class="artifact-type">Text & AI Pipeline</div>
                <div class="artifact-name">Bereinigtes Markdown</div>
                <div class="artifact-desc">Strukturiertes Markdown-Dokument für RAG-Systeme, LLM-Pipelines und universelle Textverarbeitung.</div>
            </div>
            <span class="artifact-link-action">Markdown anzeigen →</span>
        </a>
    </div>
</section>

<footer class="global-footer">
    <div class="footer-quote">
        »brahma vā idam agra āsīt | tad ātmānam evāvet | ahaṃ brahmāsmīti | tasmāt tat sarvam abhavat« (BĀU 1.4.21)
    </div>
    <div>
        Bṛhadāraṇyaka-Upaniṣad I.4 Synoptische Edition · Bereitgestellt via <a href="https://github.com/birchville-org/brhadaranyaka" style="color:var(--gold-light);text-decoration:none;">birchville-org/brhadaranyaka</a> auf GitHub Pages.
    </div>
</footer>

<!-- Floating Global Grammar Popover (Fixed Viewport Overlay) -->
<div id="globalGrammarPopover" class="interactive-popover">
    <div class="pop-head">
        <span id="popTitle" class="pop-title">Token</span>
        <button class="pop-close" onclick="hideGlobalPopover()">✕</button>
    </div>
    <div id="popSandhiBar" class="pop-sandhi">
        <span class="pop-sandhi-label">Padapāṭha:</span>
        <span id="popSandhiVal">...</span>
    </div>
    <div id="popWordsList" class="pop-words"></div>
</div>

<script>
const DATA = {data_json_str};

function renderInteractiveIast(sec, secIdx) {{
    if (!sec.grammar_analysis || sec.grammar_analysis.length === 0) {{
        return escapeHtml(sec.sanskrit_iast || '');
    }}

    return sec.grammar_analysis.map((t, tIdx) => {{
        const tokText = escapeHtml(t.token || '');
        if (tokText === '|' || tokText === '||') {{
            return `<span style="color:#64748b;font-style:normal;margin:0 3px;">${{tokText}}</span>`;
        }}
        return `<span class="iast-word-token" data-sec-idx="${{secIdx}}" data-token-idx="${{tIdx}}" onclick="showPopover(event, ${{secIdx}}, ${{tIdx}})">${{tokText}}</span>`;
    }}).join(' ');
}}

function showPopover(event, secIdx, tokenIdx) {{
    if (event) {{
        event.stopPropagation();
    }}
    const sec = DATA.sections[secIdx];
    if (!sec || !sec.grammar_analysis || !sec.grammar_analysis[tokenIdx]) return;

    const tokenData = sec.grammar_analysis[tokenIdx];
    const targetEl = (event.currentTarget || event.target).closest('.iast-word-token') || event.currentTarget || event.target;
    const pop = document.getElementById('globalGrammarPopover');
    if (!pop || !targetEl) return;

    document.querySelectorAll('.iast-word-token').forEach(el => el.classList.remove('active'));
    targetEl.classList.add('active');

    document.getElementById('popTitle').textContent = tokenData.token || '';
    document.getElementById('popSandhiVal').textContent = tokenData.sandhi || tokenData.token || '';

    const listEl = document.getElementById('popWordsList');
    listEl.innerHTML = '';
    const words = tokenData.words || [];

    if (words.length === 0) {{
        listEl.innerHTML = '<div style="color:#94a3b8;font-size:0.8rem;">Keine morphologische Zerlegung hinterlegt.</div>';
    }} else {{
        words.forEach(w => {{
            const card = document.createElement('div');
            card.className = 'pop-word-card';
            card.innerHTML = `
                <div class="pop-word-top">
                    <span class="pop-word-form">${{escapeHtml(w.form || '')}}</span>
                    <span class="pop-word-pos">${{escapeHtml(w.pos || '')}}</span>
                </div>
                <div class="pop-word-lemma">
                    Stamm/Wurzel: <span class="pop-word-lemma-val">${{escapeHtml(w.lemma || '')}}</span>
                </div>
                <div class="pop-word-morph">${{escapeHtml(w.morph || '')}}</div>
                <div class="pop-word-gloss">»${{escapeHtml(w.gloss || '')}}«</div>
            `;
            listEl.appendChild(card);
        }});
    }}

    pop.style.display = 'block';
    const rect = targetEl.getBoundingClientRect();
    const popWidth = pop.offsetWidth || 320;
    const popHeight = pop.offsetHeight || 260;

    let left = rect.left;
    let top = rect.bottom + 6;

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

function hideGlobalPopover() {{
    const pop = document.getElementById('globalGrammarPopover');
    if (pop) pop.style.display = 'none';
    document.querySelectorAll('.iast-word-token').forEach(el => el.classList.remove('active'));
}}

document.addEventListener('click', (e) => {{
    const pop = document.getElementById('globalGrammarPopover');
    if (pop && pop.style.display === 'block') {{
        if (!pop.contains(e.target) && !e.target.closest('.iast-word-token')) {{
            hideGlobalPopover();
        }}
    }}
}});
document.addEventListener('keydown', (e) => {{
    if (e.key === 'Escape') hideGlobalPopover();
}});

function renderVerses(list) {{
    const container = document.getElementById('versesGrid');
    if (!list || list.length === 0) {{
        container.innerHTML = '<div style="text-align:center;padding:3rem;color:var(--text-muted);">Keine Verse für diese Suchanfrage gefunden.</div>';
        return;
    }}

    container.innerHTML = list.map(sec => {{
        const secIdx = DATA.sections.findIndex(s => s.verse_num === sec.verse_num);
        let commHtml = '';
        if (sec.commentary_slaje && sec.commentary_slaje.length > 0) {{
            commHtml = `
                <div class="commentary-container">
                    <div class="commentary-title">📝 Philologischer Stellenkommentar (Slaje 2009)</div>
                    ${{sec.commentary_slaje.map(c => `
                        <div class="commentary-item">
                            <span class="commentary-lemma">${{escapeHtml(c.lemma || '')}}</span>
                            <span>${{escapeHtml(c.text || '')}}</span>
                        </div>
                    `).join('')}}
                </div>
            `;
        }}

        const iastHtml = renderInteractiveIast(sec, secIdx);

        return `
            <article class="verse-card" id="v-${{sec.verse_num}}">
                <div class="verse-card-header">
                    <span class="verse-canonical-badge">BĀU ${{sec.canonical_id}}</span>
                    <span class="verse-source-tag">Abschnitt ${{sec.verse_num}} von 31</span>
                </div>

                <div class="verse-deva">${{escapeHtml(sec.sanskrit_devanagari || '')}}</div>
                
                <div class="verse-iast-container">
                    <div class="iast-hint-banner">💡 Klick auf ein Wort öffnet die grammatische Analyse:</div>
                    <div class="verse-iast-tokens">${{iastHtml}}</div>
                </div>

                <div class="verse-synopsis-columns">
                    <div class="trans-panel slaje">
                        <div class="trans-meta-header slaje">
                            <span>Walter Slaje (2009)</span>
                            <span style="font-weight:normal;opacity:0.8;">Ursubjekt-Konzeption</span>
                        </div>
                        <div class="trans-body">${{escapeHtml(sec.translation_slaje || '')}}</div>
                    </div>

                    <div class="trans-panel bohtlingk">
                        <div class="trans-meta-header bohtlingk">
                            <span>Otto von Böhtlingk (1889)</span>
                            <span style="font-weight:normal;opacity:0.8;">Mādhyandina-Erstausgabe</span>
                        </div>
                        <div class="trans-body">${{escapeHtml(sec.translation_bohtlingk || '')}}</div>
                    </div>
                </div>

                ${{commHtml}}
            </article>
        `;
    }}).join('');
}}

function filterVerses() {{
    const q = document.getElementById('searchInput').value.toLowerCase().trim();
    if (!q) {{
        renderVerses(DATA.sections);
        return;
    }}

    const filtered = DATA.sections.filter(sec => {{
        const inDeva = (sec.sanskrit_devanagari || '').toLowerCase().includes(q);
        const inIast = (sec.sanskrit_iast || '').toLowerCase().includes(q);
        const inSlaje = (sec.translation_slaje || '').toLowerCase().includes(q);
        const inBoht = (sec.translation_bohtlingk || '').toLowerCase().includes(q);
        const inComm = (sec.commentary_slaje || []).some(c => 
            (c.lemma || '').toLowerCase().includes(q) || (c.text || '').toLowerCase().includes(q)
        );
        const inGrammar = (sec.grammar_analysis || []).some(t =>
            (t.token || '').toLowerCase().includes(q) ||
            (t.sandhi || '').toLowerCase().includes(q) ||
            (t.words || []).some(w =>
                (w.form || '').toLowerCase().includes(q) ||
                (w.lemma || '').toLowerCase().includes(q) ||
                (w.gloss || '').toLowerCase().includes(q) ||
                (w.morph || '').toLowerCase().includes(q)
            )
        );
        return inDeva || inIast || inSlaje || inBoht || inComm || inGrammar;
    }});

    renderVerses(filtered);
}}

function escapeHtml(str) {{
    return (str || '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}}

window.addEventListener('DOMContentLoaded', () => {{
    renderVerses(DATA.sections);
}});
</script>
</body>
</html>
"""


def build_synopsis_html(data: dict) -> str:
    src = ROOT / "data" / "output" / "brhadaranyaka_1_4_synopsis.html"
    content = src.read_text(encoding="utf-8")

    nav_bar = """
<div style="position: sticky; top: 0; z-index: 1000; background: #1e293b; color: #fff; padding: 10px 24px; display: flex; align-items: center; justify-content: space-between; font-family: -apple-system, sans-serif; font-size: 13px; border-bottom: 1px solid #334155; box-shadow: 0 2px 8px rgba(0,0,0,0.15);">
    <div style="display: flex; align-items: center; gap: 12px;">
        <a href="index.html" style="color: #fff; text-decoration: none; font-weight: 700; display: inline-flex; align-items: center; gap: 6px;">
            <span>← Zur Startseite</span>
        </a>
        <span style="color: #64748b;">|</span>
        <span style="color: #cbd5e1; font-weight: 600;">Bṛhadāraṇyaka-Upaniṣad I.4 — Synoptische Lesefassung</span>
    </div>
    <div style="display: flex; align-items: center; gap: 12px;">
        <span style="font-size: 11.5px; color: #fbbf24;">💡 Klick auf ein IAST-Wort öffnet die grammatische Analyse</span>
        <a href="data/output/brhadaranyaka_1_4_synopsis.pdf" target="_blank" style="color: #94a3b8; text-decoration: none;">📄 PDF herunterladen</a>
        <a href="viewer.html" style="background: #8b1e22; color: #fff; padding: 4px 12px; border-radius: 4px; text-decoration: none; font-weight: 600;">🚀 QA-Viewer öffnen</a>
    </div>
</div>
"""

    # Inject interactive tokens into .iast-block
    for sec_idx, sec in enumerate(data.get("sections", [])):
        ga = sec.get("grammar_analysis", [])
        if not ga:
            continue
        raw_iast = sec.get("sanskrit_iast", "")
        # Build interactive tokens
        tok_spans = []
        for t_idx, t in enumerate(ga):
            tok_text = (t.get("token") or "").replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            if tok_text in ('|', '||'):
                tok_spans.append(f'<span style="color:#888;font-style:normal;margin:0 2px;">{tok_text}</span>')
            else:
                tok_spans.append(f'<span class="synopsis-iast-tok" data-sec="{sec_idx}" data-tok="{t_idx}" onclick="showSynopsisPopover(event, {sec_idx}, {t_idx})">{tok_text}</span>')
        interactive_iast = " ".join(tok_spans)
        # Replace the raw iast block in content
        target_pattern = f'<div class="iast-block">{raw_iast}</div>'
        if target_pattern in content:
            content = content.replace(target_pattern, f'<div class="iast-block interactive-iast">{interactive_iast}</div>')

    # Popover CSS & HTML & JS for synopsis.html
    synopsis_popover_snippet = f"""
<style>
.synopsis-iast-tok {{
    cursor: pointer;
    font-style: italic;
    padding: 1px 3px;
    margin: 0 1px;
    border-radius: 3px;
    border-bottom: 1.5px dotted #7b1113;
    transition: all 0.15s ease;
    display: inline-block;
}}
.synopsis-iast-tok:hover {{
    background: #fef3c7;
    color: #b45309;
    border-bottom-color: #b45309;
}}
.synopsis-iast-tok.active {{
    background: #fde68a;
    color: #92400e;
    font-weight: 600;
    border-bottom: 2px solid #b45309;
}}
.synopsis-grammar-popover {{
    position: fixed;
    z-index: 999999;
    width: 320px;
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.25), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
    padding: 14px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 12px;
    color: #0f172a;
    display: none;
    animation: popoverFadeIn 0.15s ease-out;
}}
@keyframes popoverFadeIn {{
    from {{ opacity: 0; transform: translateY(-4px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}
.syn-pop-head {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 8px;
    margin-bottom: 10px;
}}
.syn-pop-title {{
    font-family: 'EB Garamond', Georgia, serif;
    font-size: 16px;
    font-weight: 700;
    font-style: italic;
    color: #7b1113;
}}
.syn-pop-close {{
    background: transparent;
    border: none;
    color: #94a3b8;
    cursor: pointer;
    font-size: 16px;
    line-height: 1;
    padding: 2px 4px;
}}
.syn-pop-close:hover {{ color: #0f172a; }}
.syn-pop-sandhi {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    padding: 6px 10px;
    font-size: 12px;
    color: #475569;
    margin-bottom: 10px;
    font-family: 'EB Garamond', Georgia, serif;
}}
.syn-pop-words {{
    display: flex;
    flex-direction: column;
    gap: 8px;
    max-height: 280px;
    overflow-y: auto;
}}
.syn-pop-card {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 8px 10px;
}}
.syn-pop-card-top {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 4px;
}}
.syn-pop-card-form {{
    font-family: 'EB Garamond', Georgia, serif;
    font-weight: 700;
    font-size: 14px;
    color: #0f172a;
}}
.syn-pop-card-pos {{
    background: #eff6ff;
    color: #1d4ed8;
    font-size: 10px;
    font-weight: 700;
    padding: 2px 6px;
    border-radius: 3px;
    text-transform: uppercase;
}}
.syn-pop-card-lemma {{
    font-size: 11px;
    color: #64748b;
    margin-bottom: 4px;
}}
.syn-pop-card-lemma-val {{
    font-family: 'EB Garamond', Georgia, serif;
    font-weight: 600;
    color: #7b1113;
}}
.syn-pop-card-morph {{
    font-size: 11px;
    color: #334155;
    margin-bottom: 4px;
    line-height: 1.35;
}}
.syn-pop-card-gloss {{
    font-size: 11.5px;
    color: #d97706;
    font-style: italic;
}}
</style>

<!-- Floating Grammar Popover for synopsis.html -->
<div id="synopsisGrammarPopover" class="synopsis-grammar-popover">
    <div class="syn-pop-head">
        <span id="synPopTitle" class="syn-pop-title">Token</span>
        <button class="syn-pop-close" onclick="hideSynopsisPopover()">✕</button>
    </div>
    <div id="synPopSandhi" class="syn-pop-sandhi">
        <span style="font-weight: 600; color: #64748b; font-size: 10px; text-transform: uppercase;">Padapāṭha:</span>
        <span id="synPopSandhiVal" style="font-weight: 600; color: #0f172a; margin-left: 4px;">...</span>
    </div>
    <div id="synPopWords" class="syn-pop-words"></div>
</div>

<script>
const SYNOPSIS_DATA = {json.dumps(data, ensure_ascii=False)};

function showSynopsisPopover(event, secIdx, tokenIdx) {{
    if (event) event.stopPropagation();
    const sec = SYNOPSIS_DATA.sections[secIdx];
    if (!sec || !sec.grammar_analysis || !sec.grammar_analysis[tokenIdx]) return;

    const tokenData = sec.grammar_analysis[tokenIdx];
    const targetEl = (event.currentTarget || event.target).closest('.synopsis-iast-tok') || event.currentTarget || event.target;
    const pop = document.getElementById('synopsisGrammarPopover');
    if (!pop || !targetEl) return;

    document.querySelectorAll('.synopsis-iast-tok').forEach(el => el.classList.remove('active'));
    targetEl.classList.add('active');

    document.getElementById('synPopTitle').textContent = tokenData.token || '';
    document.getElementById('synPopSandhiVal').textContent = tokenData.sandhi || tokenData.token || '';

    const listEl = document.getElementById('synPopWords');
    listEl.innerHTML = '';
    const words = tokenData.words || [];

    if (words.length === 0) {{
        listEl.innerHTML = '<div style="color:#64748b;font-size:11px;">Keine morphologische Zerlegung hinterlegt.</div>';
    }} else {{
        words.forEach(w => {{
            const card = document.createElement('div');
            card.className = 'syn-pop-card';
            card.innerHTML = `
                <div class="syn-pop-card-top">
                    <span class="syn-pop-card-form">${{escapeHtml(w.form || '')}}</span>
                    <span class="syn-pop-card-pos">${{escapeHtml(w.pos || '')}}</span>
                </div>
                <div class="syn-pop-card-lemma">
                    Stamm/Wurzel: <span class="syn-pop-card-lemma-val">${{escapeHtml(w.lemma || '')}}</span>
                </div>
                <div class="syn-pop-card-morph">${{escapeHtml(w.morph || '')}}</div>
                <div class="syn-pop-card-gloss">»${{escapeHtml(w.gloss || '')}}«</div>
            `;
            listEl.appendChild(card);
        }});
    }}

    pop.style.display = 'block';
    const rect = targetEl.getBoundingClientRect();
    const popWidth = pop.offsetWidth || 320;
    const popHeight = pop.offsetHeight || 260;

    let left = rect.left;
    let top = rect.bottom + 6;

    if (left + popWidth > window.innerWidth - 12) {{
        left = Math.max(12, window.innerWidth - popWidth - 12);
    }}
    if (left < 12) left = 12;

    if (top + popHeight > window.innerHeight - 12) {{
        const flippedTop = rect.top - popHeight - 6;
        if (flippedTop >= 12) top = flippedTop;
        else top = Math.max(12, window.innerHeight - popHeight - 12);
    }}

    pop.style.left = Math.round(left) + 'px';
    pop.style.top = Math.round(top) + 'px';
}}

function hideSynopsisPopover() {{
    const pop = document.getElementById('synopsisGrammarPopover');
    if (pop) pop.style.display = 'none';
    document.querySelectorAll('.synopsis-iast-tok').forEach(el => el.classList.remove('active'));
}}

document.addEventListener('click', (e) => {{
    const pop = document.getElementById('synopsisGrammarPopover');
    if (pop && pop.style.display === 'block') {{
        if (!pop.contains(e.target) && !e.target.closest('.synopsis-iast-tok')) {{
            hideSynopsisPopover();
        }}
    }}
}});
document.addEventListener('keydown', (e) => {{
    if (e.key === 'Escape') hideSynopsisPopover();
}});

function escapeHtml(str) {{
    return (str || '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}}
</script>
"""

    content = content.replace("<body>", f"<body>\n{nav_bar}")
    content = content.replace("</body>", f"{synopsis_popover_snippet}\n</body>")
    return content


def main() -> None:
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))

    # 1. Write index.html
    index_html = build_index_html(data)
    (ROOT / "index.html").write_text(index_html, encoding="utf-8")
    print(f"-> Successfully generated {ROOT / 'index.html'} ({(ROOT / 'index.html').stat().st_size} bytes)")

    # 2. Write synopsis.html
    synopsis_html = build_synopsis_html(data)
    (ROOT / "synopsis.html").write_text(synopsis_html, encoding="utf-8")
    print(f"-> Successfully generated {ROOT / 'synopsis.html'} ({(ROOT / 'synopsis.html').stat().st_size} bytes)")

    # 3. Copy viewer.html to data/output/viewer.html for parity
    viewer_src = ROOT / "viewer.html"
    viewer_dst = ROOT / "data" / "output" / "viewer.html"
    if viewer_src.exists():
        viewer_dst.write_text(viewer_src.read_text(encoding="utf-8"), encoding="utf-8")
        print("-> Synchronized data/output/viewer.html")


if __name__ == "__main__":
    main()

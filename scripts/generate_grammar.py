#!/usr/bin/env python3
"""
AlexandriaSandwich / Bṛhadāraṇyaka — Batch Morphosyntactic & Compound Grammar Generator
Generates deep word-by-word grammatical, syntactic, and Samāsa (compound) analysis
for all 31 sections of BĀU 1.4 using Mistral AI with incremental disk caching.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path
from mistralai.client import Mistral

ROOT = Path("/Volumes/SanDisk1TB/proj/brhadaranyaka")
MASTER_JSON = ROOT / "data" / "output" / "brhadaranyaka_1_4_master.json"
CACHE_FILE = ROOT / "data" / "processing" / "grammar_cache_v2.json"
ENV_FILE = Path("/Volumes/SanDisk1TB/proj/AlexandriaSandwich/.env")


def get_api_key() -> str:
    key = os.environ.get("MISTRAL_API_KEY")
    if key:
        return key
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            if "MISTRAL_API_KEY=" in line:
                return line.split("MISTRAL_API_KEY=")[1].strip().strip("\"'")
    print("Error: MISTRAL_API_KEY not found", file=sys.stderr)
    sys.exit(1)


def clean_tokens(iast_raw: str) -> list[str]:
    # Normalize attached pipes e.g. |so -> | so
    iast_norm = re.sub(r'([|]+)', r' \1 ', iast_raw)
    tokens = [w for w in iast_norm.split() if w not in ("|", "||")]
    return tokens


def analyze_verse(client: Mistral, canonical_id: str, tokens_list: list[str]) -> list:
    prompt = f"""Du bist ein führender Indologe und Sanskritist. Analysiere den folgenden altindischen Sanskrit-Text aus der Bṛhadāraṇyaka-Upaniṣad ({canonical_id}, Mādhyandina-Rezension) detailliert grammatisch, morphosyntaktisch und kompositorisch.

Analysiere die folgende vorgegebene Sequenz von IAST-Tokens (jedes Token muss exakt als "token" übernommen werden):
{json.dumps(tokens_list, ensure_ascii=False)}

Für jedes Token im Array 'tokens' gib an:
- "token": der exakte IAST-Token-String aus der Vorgabe
- "sandhi": die Sandhi-Auflösung (Padapāṭha; bei Komposita die Glieder mit Bindestrich)
- "words": Array der im Token enthaltenen Wörter bzw. Konstituenten:
  - "form": flektierte Form
  - "lemma": Prātipadika (Nominalstamm) bzw. Zitierstamm
  - "root": Verbalwurzel (Dhātu, z.B. "√as", "√bhū", "√kṛ", "√dṛś", "√vac") falls Verb, Partizip, Absolutivum oder Verbalabstraktum, sonst null
  - "pos": Wortart (Substantiv, Verb finit, Partizip, Pronomen, Adjektiv, Absolutivum, Partikel etc.)
  - "morph": exakte grammatische Bestimmung (z.B. "m. Nom. Sg.", "3. Sg. Impf. Akt.", "n. Akk. Sg.")
  - "syntax": syntaktische Funktion im Satz (z.B. "Subjekt", "Prädikatsnomen", "Hauptsatzprädikat", "Objekt", "Ablativ des Vergleichs", "Temporaladverbiale")
  - "is_compound": boolean (true wenn echtes Kompositum / Samāsa: Tatpuruṣa, Karmadhāraya, Bahuvrīhi, Dvandva, Avyayībhāva; NICHT bloße finite Präfixverben)
  - "compound_type": Samāsa-Klassifikation ("Tatpuruṣa", "Karmadhāraya", "Bahuvrīhi", "Dvandva", "Avyayībhāva" oder null)
  - "compound_members": Array der Glieder in Stammform (z.B. ["brahman", "jāti"]), sonst []
  - "compound_analysis": Traditioneller Vigraha / Sanskrit-Auflösung mit deutscher Übersetzung (z.B. "brahmaṇaḥ jātiḥ (Genitiv-Tatpuruṣa: 'die Kaste des Brahman')"), sonst ""
  - "gloss": präzise deutsche Übersetzung im Kontext
  - "notes": philologische / grammatische Erläuterung (Sandhi, vedische Besonderheit, Lautwandel) oder null

Gib ausschließlich valides JSON mit dem Wurzelschlüssel "tokens" zurück.
"""

    for attempt in range(3):
        try:
            resp = client.chat.complete(
                model="mistral-small-latest",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.1
            )
            raw = resp.choices[0].message.content
            parsed = json.loads(raw)
            tokens = parsed.get("tokens", [])
            if tokens and len(tokens) >= len(tokens_list) * 0.8:
                return tokens
            else:
                print(f"   [warn] {canonical_id}: Returned {len(tokens)} vs {len(tokens_list)} tokens. Retrying...", file=sys.stderr)
        except Exception as e:
            print(f"   [warn] {canonical_id} Attempt {attempt+1} failed: {e}", file=sys.stderr)
            time.sleep(2)

    return []


def main():
    api_key = get_api_key()
    client = Mistral(api_key=api_key)

    data = json.loads(MASTER_JSON.read_text(encoding="utf-8"))
    sections = data["sections"]

    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    cache = {}
    if CACHE_FILE.exists():
        try:
            cache = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
            print(f"Loaded {len(cache)} cached verse analyses from {CACHE_FILE.name}")
        except Exception:
            pass

    print(f"Starting detailed morphosyntactic & compound analysis for {len(sections)} sections...")
    total_tokens = 0
    total_compounds = 0

    for idx, sec in enumerate(sections):
        v_num = sec["verse_num"]
        c_id = sec["canonical_id"]
        iast = sec["sanskrit_iast"]
        tok_list = clean_tokens(iast)

        # Normalize attached pipes in master data as well
        sec["sanskrit_iast"] = re.sub(r'([|]+)', r' \1 ', iast)
        sec["sanskrit_iast"] = re.sub(r'\s+', ' ', sec["sanskrit_iast"]).strip()

        if str(v_num) in cache:
            tokens = cache[str(v_num)]
            sec["grammar_analysis"] = tokens
            total_tokens += len(tokens)
            sec_compounds = sum(1 for t in tokens for w in t.get("words", []) if w.get("is_compound"))
            total_compounds += sec_compounds
            print(f"[{idx+1}/{len(sections)}] {c_id}: Using cache ({len(tokens)} tokens, {sec_compounds} compounds)")
            continue

        print(f"[{idx+1}/{len(sections)}] {c_id}: Analyzing {len(tok_list)} tokens via Mistral...")
        tokens = analyze_verse(client, c_id, tok_list)
        sec_compounds = sum(1 for t in tokens for w in t.get("words", []) if w.get("is_compound"))
        print(f"   ✓ Done: {len(tokens)} tokens, {sec_compounds} compounds.")

        cache[str(v_num)] = tokens
        sec["grammar_analysis"] = tokens
        total_tokens += len(tokens)
        total_compounds += sec_compounds

        # Save cache incrementally
        CACHE_FILE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")
        time.sleep(0.4)

    # Save to master JSON
    MASTER_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n==========================================")
    print(f"Successfully processed all {len(sections)} sections:")
    print(f"Total tokens: {total_tokens}")
    print(f"Total compounds analyzed: {total_compounds}")
    print(f"Updated: {MASTER_JSON}")
    print(f"Cache: {CACHE_FILE}")
    print(f"==========================================")


if __name__ == "__main__":
    main()

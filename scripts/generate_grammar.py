#!/usr/bin/env python3
"""
AlexandriaSandwich / Bṛhadāraṇyaka — Morphosyntactic Grammar Analysis Generator
Generates word-by-word grammatical analysis, Sandhi dissolution (Padapāṭha),
lemma, morphological tags, and German glosses for all 31 sections of BĀU 1.4.
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path
from mistralai.client import Mistral

ROOT = Path("/Volumes/SanDisk1TB/proj/brhadaranyaka")
MASTER_JSON = ROOT / "data" / "output" / "brhadaranyaka_1_4_master.json"
CACHE_FILE = ROOT / "data" / "processing" / "grammar_cache.json"
ENV_FILE = Path("/Volumes/SanDisk1TB/proj/AlexandriaSandwich/.env")


def get_api_key() -> str:
    key = os.environ.get("MISTRAL_API_KEY")
    if key:
        return key
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            if "MISTRAL_API_KEY=" in line:
                return line.split("MISTRAL_API_KEY=")[1].strip()
    print("Error: MISTRAL_API_KEY not found", file=sys.stderr)
    sys.exit(1)


def analyze_verse(client: Mistral, verse_num: int, iast_text: str) -> list:
    prompt = f"""Analysiere den folgenden altindischen Sanskrit-Satz (IAST) grammatisch Wort für Wort für eine wissenschaftliche Edition der Bṛhadāraṇyaka-Upaniṣad (Mādhyandina-Rezension).
Löse alle Sandhis auf (Padapāṭha), bestimme Wurzel/Lemma, Wortart (pos), exakte morphologische Form (morph, z.B. m. Nom. Sg., 3. Sg. Impf. Akt., indekl.) und deutsche philologische Kurzbedeutung (gloss).

Sanskrit-Satz (Vers {verse_num}):
{iast_text}

Gib das Ergebnis ausschließlich als valides JSON-Objekt mit dem Key 'tokens' zurück:
{{
  "tokens": [
    {{
      "token": "exakter_iast_string",
      "sandhi": "aufgelöstes_padapatha",
      "words": [
        {{"form": "...", "lemma": "...", "pos": "...", "morph": "...", "gloss": "..."}}
      ]
    }}
  ]
}}"""

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
            if tokens:
                return tokens
        except Exception as e:
            print(f"   [warn] Vers {verse_num} Attempt {attempt+1} failed: {e}", file=sys.stderr)
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
            print(f"Loaded {len(cache)} cached verse analyses.")
        except Exception:
            pass

    print(f"Starting grammatical analysis for {len(sections)} verses...")
    total_tokens = 0

    for idx, sec in enumerate(sections):
        v_num = sec["verse_num"]
        c_id = sec["canonical_id"]
        iast = sec["sanskrit_iast"]

        if str(v_num) in cache:
            sec["grammar_analysis"] = cache[str(v_num)]
            total_tokens += len(cache[str(v_num)])
            continue

        print(f"-> Analyzing {c_id} ({len(iast.split())} words)...")
        tokens = analyze_verse(client, v_num, iast)
        print(f"   Done: extracted {len(tokens)} grammatical tokens.")

        cache[str(v_num)] = tokens
        sec["grammar_analysis"] = tokens
        total_tokens += len(tokens)

        # Save cache incrementally
        CACHE_FILE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")
        time.sleep(0.5)

    # Save to master JSON
    MASTER_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nSuccessfully annotated {len(sections)} verses with {total_tokens} tokens.")
    print(f"Updated: {MASTER_JSON}")


if __name__ == "__main__":
    main()

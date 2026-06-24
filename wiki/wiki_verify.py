#!/usr/bin/env python3
"""
wiki_verify.py — ITS Architecture Wiki Integrity Checker

Compares the generated wiki against authoritative source data to find:
  • Missing service packages  (qrySPInstanceInformation.js vs SP_CATEGORIES)
  • Missing stakeholders       (tblStakeholders.js vs wiki/technical/stakeholders.md)
  • Phantom entries            (wiki links with no source counterpart)
  • Missing/phantom standards  (content dir solutions/bundles vs wiki/technical/standards.md)

Outputs:
  • Console summary
  • wiki_verify_report.md — detailed findings + LLM prompts to repair build_wiki.py

Usage:
    python wiki_verify.py [options]

Options:
    --content-dir  Path to web/content directory   (default: ../../content)
    --wiki-dir     Path to wiki/technical directory (default: wiki/technical)
    --build-wiki   Path to build_wiki.py            (default: ./build_wiki.py)
    --report       Output path for report           (default: wiki_verify_report.md)
"""

import argparse
import csv
import importlib.util
import json
import re
import sys
from collections import defaultdict
from pathlib import Path


# ──────────────────────────────────────────────────────────────────────────────
# Path defaults
# ──────────────────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
CONTENT_DIR_DEFAULT = SCRIPT_DIR.parent.parent / "content"
WIKI_DIR_DEFAULT = SCRIPT_DIR / "wiki" / "technical"
BUILD_WIKI_DEFAULT = SCRIPT_DIR / "build_wiki.py"
REPORT_PATH_DEFAULT = SCRIPT_DIR / "wiki_verify_report.md"


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def _load_js_array(js_file: Path) -> list:
    """Parse `var NAME = [...];` JS files and return a Python list."""
    text = js_file.read_text(encoding="utf-8", errors="replace")
    m = re.search(r'var\s+\w+\s*=\s*(\[.*?\])\s*;?', text, re.DOTALL)
    if not m:
        raise ValueError(f"Cannot find JS array pattern in {js_file}")
    # Strip trailing commas before ] or } — valid JS but invalid JSON
    array_text = re.sub(r',(\s*[}\]])', r'\1', m.group(1))
    return json.loads(array_text)


def _load_sp_categories(build_wiki_py: Path) -> dict:
    """Return SP_CATEGORIES dict by importing build_wiki.py."""
    parent = str(build_wiki_py.parent.parent)
    if parent not in sys.path:
        sys.path.insert(0, parent)
    spec = importlib.util.spec_from_file_location("_bw_mod", str(build_wiki_py))
    mod = importlib.util.module_from_spec(spec)
    old_argv = sys.argv[:]
    sys.argv = ["build_wiki.py"]
    try:
        spec.loader.exec_module(mod)
    except SystemExit:
        pass
    finally:
        sys.argv = old_argv
    return mod.SP_CATEGORIES


def _parse_md_ids(md_file: Path, url_fragment: str) -> dict:
    """Extract ?id=NNN entries from a markdown file. Returns {id: display_name}."""
    text = md_file.read_text(encoding="utf-8")
    result = {}
    for m in re.finditer(
        r'\[([^\]]+)\]\([^)]*' + re.escape(url_fragment) + r'\?id=(\d+)[^)]*\)',
        text,
    ):
        result[m.group(2)] = m.group(1)
    return result


def _content_htm_ids(content_dir: Path, prefix: str) -> set:
    """Return all numeric IDs for files named `{prefix}{id}.htm` in content_dir."""
    ids = set()
    for f in content_dir.iterdir():
        m = re.fullmatch(rf'{re.escape(prefix)}(\d+)\.htm', f.name, re.IGNORECASE)
        if m:
            ids.add(m.group(1))
    return ids


def _sp_cat_prefix(code: str) -> str:
    m = re.match(r'^([A-Z]{2,4})', code)
    return m.group(1) if m else "??"


# ──────────────────────────────────────────────────────────────────────────────
# Check 1 — Service Packages
# ──────────────────────────────────────────────────────────────────────────────

def check_service_packages(content_dir: Path, build_wiki_py: Path) -> dict:
    """Compare base SP codes in qrySPInstanceInformation.js vs SP_CATEGORIES."""
    sp_js = content_dir / "qrySPInstanceInformation.js"
    if not sp_js.exists():
        return {"error": f"Not found: {sp_js}"}

    records = _load_js_array(sp_js)
    source_sps: dict = {}
    for r in records:
        if r.get("SPParentID") == "0" and r.get("SPName") and r["SPName"] != "(None)":
            code = r["SPName"].strip()
            source_sps[code] = {
                "long_name": r.get("SPLongName", "").strip(),
                "description": (r.get("SPDescription") or "").strip()[:200],
            }

    sp_cats = _load_sp_categories(build_wiki_py)
    defined_codes: set = set()
    for cat_info in sp_cats.values():
        for sub in cat_info.get("subcategories", {}).values():
            defined_codes.update(sub.get("codes", []))

    source_codes = set(source_sps.keys())
    missing_codes = source_codes - defined_codes
    phantom_codes = defined_codes - source_codes

    return {
        "source_count": len(source_codes),
        "defined_count": len(defined_codes),
        "missing": {c: source_sps[c] for c in sorted(missing_codes)},
        "phantoms": sorted(phantom_codes),
        "sp_cats": sp_cats,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Check 2 — Stakeholders
# ──────────────────────────────────────────────────────────────────────────────

def _load_stakeholders_source(content_dir: Path) -> dict:
    """Return {id: name} from tblStakeholders.js (or .csv fallback)."""
    js_file = content_dir / "tblStakeholders.js"
    csv_file = content_dir / "tblStakeholders.csv"

    if js_file.exists():
        try:
            records = _load_js_array(js_file)
            result: dict = {}
            for r in records:
                sid = (
                    r.get("StakeholderID") or r.get("ID") or r.get("id") or ""
                ).strip()
                name = (
                    r.get("Stakeholder") or r.get("StakeholderName")
                    or r.get("Name") or r.get("name") or ""
                ).strip()
                if sid and name:
                    result[sid] = name
            if result:
                return result
        except Exception:
            pass

    if csv_file.exists():
        csv.field_size_limit(10 ** 7)
        result = {}
        with open(csv_file, encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                sid = (
                    row.get("StakeholderID") or row.get("ID") or row.get("id") or ""
                ).strip()
                name = (
                    row.get("Stakeholder") or row.get("Name") or row.get("name") or ""
                ).strip()
                if sid and name:
                    result[sid] = name
        return result

    return {}


def check_stakeholders(content_dir: Path, wiki_dir: Path) -> dict:
    """Compare tblStakeholders source vs wiki/technical/stakeholders.md."""
    source = _load_stakeholders_source(content_dir)
    if not source:
        return {"error": f"No stakeholder source data found in {content_dir}"}

    md_file = wiki_dir / "stakeholders.md"
    if not md_file.exists():
        return {"error": f"Not found: {md_file}"}

    wiki_ids = _parse_md_ids(md_file, "stakeholder.htm")

    md_text = md_file.read_text(encoding="utf-8")
    no_id_phantoms = [
        line.strip()
        for line in md_text.splitlines()
        if "stakeholder.htm" in line and "?id=" not in line and line.strip().startswith("- [")
    ]

    source_ids = set(source.keys())
    wiki_id_set = set(wiki_ids.keys())

    def sort_int(ids):
        return sorted(ids, key=lambda x: int(x) if x.isdigit() else 0)

    return {
        "source_count": len(source),
        "wiki_count": len(wiki_ids),
        "missing": {sid: source[sid] for sid in sort_int(source_ids - wiki_id_set)},
        "phantom_ids": {sid: wiki_ids[sid] for sid in sort_int(wiki_id_set - source_ids)},
        "phantom_no_id": no_id_phantoms,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Check 3 — Standards
# ──────────────────────────────────────────────────────────────────────────────

def check_standards(content_dir: Path, wiki_dir: Path) -> dict:
    """Compare solution/bundle pages in content dir vs wiki/technical/standards.md."""
    standards_md = wiki_dir / "standards.md"
    if not standards_md.exists():
        return {"error": f"Not found: {standards_md}"}

    md_text = standards_md.read_text(encoding="utf-8")
    wiki_solution_ids = set(re.findall(r'solution\.htm\?id=(\d+)', md_text))
    wiki_bundle_ids = set(re.findall(r'bundle\.htm\?id=(\d+)', md_text))

    content_solution_ids = _content_htm_ids(content_dir, "solution")
    content_bundle_ids = _content_htm_ids(content_dir, "bundle")

    triples_csv = content_dir / "triplesWithStandards.csv"
    if not triples_csv.exists():
        triples_csv = content_dir / "triplesWithStandards.csv"
    active_solution_ids: set = set()
    if triples_csv.exists():
        csv.field_size_limit(10 ** 7)
        with open(triples_csv, encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                sid = (row.get("SolutionID") or "").strip()
                if sid:
                    active_solution_ids.add(sid)

    def sort_ids(ids):
        return sorted(ids, key=lambda x: int(x) if x.isdigit() else 0)

    return {
        "wiki_solution_count": len(wiki_solution_ids),
        "wiki_bundle_count": len(wiki_bundle_ids),
        "content_solution_count": len(content_solution_ids),
        "content_bundle_count": len(content_bundle_ids),
        "active_solution_count": len(active_solution_ids),
        "critical_missing": sort_ids(active_solution_ids - wiki_solution_ids),
        "missing_solutions": sort_ids(content_solution_ids - wiki_solution_ids),
        "missing_bundles": sort_ids(content_bundle_ids - wiki_bundle_ids),
        "phantom_solutions": sort_ids(wiki_solution_ids - content_solution_ids),
        "phantom_bundles": sort_ids(wiki_bundle_ids - content_bundle_ids),
    }


# ──────────────────────────────────────────────────────────────────────────────
# LLM Prompt generators
# ──────────────────────────────────────────────────────────────────────────────

def sp_fix_prompt(sp_result: dict) -> str:
    missing = sp_result.get("missing", {})
    phantoms = sp_result.get("phantoms", [])
    if not missing and not phantoms:
        return ""

    by_cat: dict = defaultdict(list)
    for code, info in missing.items():
        by_cat[_sp_cat_prefix(code)].append((code, info))

    lines = [
        "### LLM Prompt — Add Missing Service Package Codes to build_wiki.py",
        "",
        "```",
        "You are editing SP_CATEGORIES in build_wiki.py.",
        "",
        "The following service package codes exist in the Maine ITS architecture",
        "(qrySPInstanceInformation.js, SPParentID='0' entries) but are absent from",
        "every subcategory's `codes` list in SP_CATEGORIES. Add each code to the",
        "correct subcategory, or create a new subcategory if none fits.",
        "",
        "Rules:",
        "  - Do NOT remove existing codes.",
        "  - Keep codes sorted within each list.",
        "  - New subcategory: {\"codes\": [...], \"name\": \"...\", \"desc\": \"...\"}",
        "",
        "Missing codes (grouped by category):",
    ]

    for cat in sorted(by_cat.keys()):
        lines.append(f"\n  [{cat}]")
        for code, info in by_cat[cat]:
            lines.append(f"    {code}  ->  {info['long_name']}")
            if info["description"]:
                lines.append(f"           {info['description'][:120]}")

    if phantoms:
        lines += [
            "",
            "Codes in SP_CATEGORIES NOT found in source architecture (review for removal):",
        ]
        for c in phantoms:
            lines.append(f"  {c}")

    lines.append("```")
    return "\n".join(lines)


def stakeholder_fix_prompt(sh_result: dict) -> str:
    missing = sh_result.get("missing", {})
    phantom_ids = sh_result.get("phantom_ids", {})
    phantom_no_id = sh_result.get("phantom_no_id", [])
    if not missing and not phantom_ids and not phantom_no_id:
        return ""

    base_url = "https://www.consystec.com/maine2026/web/stakeholder.htm?id="
    lines = [
        "### LLM Prompt — Fix Stakeholders in build_wiki.py",
        "",
        "```",
        "You are fixing stakeholder coverage in build_wiki.py.",
        "",
        "wiki/technical/stakeholders.md is generated by generate_stakeholders_page()",
        "from analysis['stakeholders'], populated by analyze_architecture() reading",
        "stakeholder.htm pages from processed_content.csv.",
    ]

    if missing:
        lines += [
            "",
            "MISSING (in tblStakeholders.js, absent from wiki):",
            "Root cause: their HTML pages were likely not ingested into processed_content.csv.",
            "Fix options:",
            "  A) Re-run content_processor.py to ingest missing pages, then rebuild wiki.",
            "  B) Hard-code them in generate_stakeholders_page() as a fallback.",
            "",
        ]
        for sid, name in missing.items():
            lines.append(f"  ID {sid:>4}  {name}")
            lines.append(f"           {base_url}{sid}")

    if phantom_ids:
        lines += [
            "",
            "PHANTOM IDs (wiki links to IDs not in tblStakeholders.js):",
        ]
        for sid, name in phantom_ids.items():
            lines.append(f"  ID {sid:>4}  {name}")

    if phantom_no_id:
        lines += [
            "",
            "INVALID entries (stakeholder.htm links with no ?id= — fabricated, remove them):",
        ]
        for entry in phantom_no_id:
            lines.append(f"  {entry}")

    lines.append("```")
    return "\n".join(lines)


# ──────────────────────────────────────────────────────────────────────────────
# Report
# ──────────────────────────────────────────────────────────────────────────────

def build_report(sp: dict, sh: dict, std: dict) -> str:
    out = ["# Wiki Integrity Verification Report", ""]

    # ── Service Packages ──────────────────────────────────────────────────────
    out.append("## 1. Service Package Coverage")
    out.append("")
    if "error" in sp:
        out.append(f"ERROR: {sp['error']}")
    else:
        verdict = "PASS" if not sp["missing"] and not sp["phantoms"] else "FAIL"
        out.append(f"**Verdict: {verdict}**")
        out.append("")
        out.append(f"- Source (`qrySPInstanceInformation.js`): **{sp['source_count']}** base codes")
        out.append(f"- Defined in `SP_CATEGORIES` subcategories: **{sp['defined_count']}** codes")
        out.append("")

        if sp["missing"]:
            out.append(f"### Missing ({len(sp['missing'])} — in source, not in SP_CATEGORIES)")
            out.append("")
            out.append("| Code | Long Name | Category |")
            out.append("|------|-----------|----------|")
            for code, info in sp["missing"].items():
                out.append(f"| `{code}` | {info['long_name']} | {_sp_cat_prefix(code)} |")
            out.append("")

        if sp["phantoms"]:
            out.append(f"### Phantom ({len(sp['phantoms'])} — in SP_CATEGORIES, not in source)")
            out.append("")
            for c in sp["phantoms"]:
                out.append(f"- `{c}`")
            out.append("")

        prompt = sp_fix_prompt(sp)
        if prompt:
            out.append(prompt)
            out.append("")

    # ── Stakeholders ──────────────────────────────────────────────────────────
    out.append("## 2. Stakeholder Coverage")
    out.append("")
    if "error" in sh:
        out.append(f"ERROR: {sh['error']}")
    else:
        has_issues = sh["missing"] or sh["phantom_ids"] or sh["phantom_no_id"]
        verdict = "FAIL" if has_issues else "PASS"
        out.append(f"**Verdict: {verdict}**")
        out.append("")
        out.append(f"- Source (`tblStakeholders.js`): **{sh['source_count']}** stakeholders")
        out.append(f"- Wiki (`stakeholders.md`): **{sh['wiki_count']}** stakeholders")
        out.append("")

        if sh["missing"]:
            out.append(f"### Missing ({len(sh['missing'])} — in source, absent from wiki)")
            out.append("")
            for sid, name in sh["missing"].items():
                out.append(f"- ID {sid}: **{name}**")
            out.append("")

        if sh["phantom_ids"]:
            out.append(f"### Phantom by ID ({len(sh['phantom_ids'])} — wiki ID not in source)")
            out.append("")
            for sid, name in sh["phantom_ids"].items():
                out.append(f"- ID {sid}: {name}")
            out.append("")

        if sh["phantom_no_id"]:
            out.append(f"### No-ID phantoms ({len(sh['phantom_no_id'])} — links to stakeholder.htm without ?id=)")
            out.append("")
            for entry in sh["phantom_no_id"]:
                out.append(f"- {entry}")
            out.append("")

        prompt = stakeholder_fix_prompt(sh)
        if prompt:
            out.append(prompt)
            out.append("")

    # ── Standards ─────────────────────────────────────────────────────────────
    out.append("## 3. Standards Coverage")
    out.append("")
    if "error" in std:
        out.append(f"ERROR: {std['error']}")
    else:
        has_issues = std["critical_missing"] or std["phantom_solutions"] or std["phantom_bundles"]
        verdict = "FAIL" if has_issues else "PASS"
        out.append(f"**Verdict: {verdict}**")
        out.append("")
        out.append(f"- Wiki solutions: **{std['wiki_solution_count']}**")
        out.append(f"- Content dir solutions: **{std['content_solution_count']}**")
        out.append(f"- Wiki bundles: **{std['wiki_bundle_count']}**")
        out.append(f"- Content dir bundles: **{std['content_bundle_count']}**")
        out.append(f"- Active solutions (in triplesWithStandards.csv): **{std['active_solution_count']}**")
        out.append("")

        if std["critical_missing"]:
            out.append(f"### CRITICAL: Active solutions missing from wiki ({len(std['critical_missing'])})")
            out.append("")
            out.append("These are referenced in `triplesWithStandards.csv` but absent from the wiki.")
            out.append("Fix: re-ingest their HTML pages via `content_processor.py`, then rebuild.")
            out.append("")
            for sid in std["critical_missing"]:
                out.append(f"- `solution{sid}.htm`  →  solution.htm?id={sid}")
            out.append("")

        if std["missing_solutions"]:
            out.append(f"### Solutions in content dir not in wiki ({len(std['missing_solutions'])})")
            out.append("")
            for sid in std["missing_solutions"]:
                out.append(f"- solution{sid}.htm")
            out.append("")

        if std["missing_bundles"]:
            out.append(f"### Bundles in content dir not in wiki ({len(std['missing_bundles'])})")
            out.append("")
            for bid in std["missing_bundles"]:
                out.append(f"- bundle{bid}.htm")
            out.append("")

        if std["phantom_solutions"]:
            out.append(f"### Phantom solutions ({len(std['phantom_solutions'])} — in wiki, no content file)")
            out.append("")
            for sid in std["phantom_solutions"]:
                out.append(f"- solution.htm?id={sid}")
            out.append("")

        if std["phantom_bundles"]:
            out.append(f"### Phantom bundles ({len(std['phantom_bundles'])} — in wiki, no content file)")
            out.append("")
            for bid in std["phantom_bundles"]:
                out.append(f"- bundle.htm?id={bid}")
            out.append("")

    return "\n".join(out)


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Verify ITS architecture wiki integrity against source data."
    )
    parser.add_argument("--content-dir", default=str(CONTENT_DIR_DEFAULT),
                        help="Path to web/content directory")
    parser.add_argument("--wiki-dir", default=str(WIKI_DIR_DEFAULT),
                        help="Path to wiki/technical directory")
    parser.add_argument("--build-wiki", default=str(BUILD_WIKI_DEFAULT),
                        help="Path to build_wiki.py")
    parser.add_argument("--report", default=str(REPORT_PATH_DEFAULT),
                        help="Output path for verification report")
    args = parser.parse_args()

    content_dir = Path(args.content_dir)
    wiki_dir = Path(args.wiki_dir)
    build_wiki_py = Path(args.build_wiki)
    report_path = Path(args.report)

    print("ITS Architecture Wiki Integrity Checker")
    print("=" * 50)

    print("\n[1/3] Service packages...")
    sp = check_service_packages(content_dir, build_wiki_py)
    if "error" in sp:
        print(f"  ERROR: {sp['error']}")
    else:
        v = "PASS" if not sp["missing"] and not sp["phantoms"] else "FAIL"
        print(f"  {v}  source={sp['source_count']}  defined={sp['defined_count']}  "
              f"missing={len(sp['missing'])}  phantom={len(sp['phantoms'])}")
        if sp["missing"]:
            for code, info in sp["missing"].items():
                print(f"    MISSING: {code}  ({info['long_name']})")

    print("\n[2/3] Stakeholders...")
    sh = check_stakeholders(content_dir, wiki_dir)
    if "error" in sh:
        print(f"  ERROR: {sh['error']}")
    else:
        v = "PASS" if not sh["missing"] and not sh["phantom_ids"] and not sh["phantom_no_id"] else "FAIL"
        print(f"  {v}  source={sh['source_count']}  wiki={sh['wiki_count']}  "
              f"missing={len(sh['missing'])}  phantom_id={len(sh['phantom_ids'])}  "
              f"no_id_phantom={len(sh['phantom_no_id'])}")
        if sh["missing"]:
            for sid, name in sh["missing"].items():
                print(f"    MISSING: ID {sid}  {name}")

    print("\n[3/3] Standards...")
    std = check_standards(content_dir, wiki_dir)
    if "error" in std:
        print(f"  ERROR: {std['error']}")
    else:
        v = "FAIL" if std["critical_missing"] or std["phantom_solutions"] or std["phantom_bundles"] else "PASS"
        print(f"  {v}  wiki_sol={std['wiki_solution_count']}  content_sol={std['content_solution_count']}  "
              f"critical_missing={len(std['critical_missing'])}  phantom_sol={len(std['phantom_solutions'])}")
        if std["critical_missing"]:
            for sid in std["critical_missing"]:
                print(f"    CRITICAL MISSING: solution{sid}.htm")

    report = build_report(sp, sh, std)
    report_path.write_text(report, encoding="utf-8")
    print(f"\nReport written to: {report_path}")
    print("LLM fix prompts are embedded in the report under each section.")


if __name__ == "__main__":
    main()

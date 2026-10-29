#!/usr/bin/env python3
"""Audit research source logs and competitor comparison CSVs (stdlib only).

Examples:
  python tools/audit_research_inputs.py --sources examples/research-brief/free-crm-source-log.csv
  python tools/audit_research_inputs.py --comparison templates/competitor-comparison-template.csv
  python tools/audit_research_inputs.py --sources path/to/sources.csv --comparison path/to/comparison.csv
"""
from __future__ import annotations
import argparse
import csv
import sys
from pathlib import Path
from urllib.parse import urlparse

def read_csv(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames:
                return [], [f"{path}: missing CSV header."]
            rows = [{(k or "").strip(): (v or "").strip() for k, v in row.items()} for row in reader]
            return rows, []
    except (OSError, csv.Error) as exc:
        return [], [f"{path}: cannot read CSV: {exc}"]

def audit_sources(path: Path) -> tuple[list[str], list[str]]:
    rows, errors = read_csv(path)
    warnings: list[str] = []
    if not rows:
        return errors or [f"{path}: no source rows found."], warnings
    required = {"source_id", "title", "url", "accessed_date", "claim_or_section_supported", "status"}
    missing = required - set(rows[0])
    if missing:
        return [f"{path}: missing required columns: {', '.join(sorted(missing))}."], warnings
    seen: set[str] = set()
    for number, row in enumerate(rows, start=2):
        source_id = row.get("source_id", "")
        if not any(row.values()):
            continue
        if not source_id:
            errors.append(f"{path}:{number}: source_id is blank.")
        elif source_id in seen:
            errors.append(f"{path}:{number}: duplicate source_id '{source_id}'.")
        seen.add(source_id)
        url = row.get("url", "")
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            errors.append(f"{path}:{number}: URL must be an absolute http(s) URL.")
        for field in ("title", "accessed_date", "claim_or_section_supported", "status"):
            if not row.get(field):
                warnings.append(f"{path}:{number}: {field} is blank.")
        if row.get("status", "").lower() in {"unchecked", "unverified", "todo", "pending"}:
            warnings.append(f"{path}:{number}: source status is '{row['status']}'.")
    return errors, warnings

def audit_comparison(path: Path) -> tuple[list[str], list[str]]:
    rows, errors = read_csv(path)
    warnings: list[str] = []
    if not rows:
        return errors or [f"{path}: no comparison rows found."], warnings
    required = {"option_name", "criterion", "weight_percent", "score_1_to_5", "evidence_summary", "source_ids"}
    missing = required - set(rows[0])
    if missing:
        return [f"{path}: missing required columns: {', '.join(sorted(missing))}."], warnings
    weights: dict[str, float] = {}
    criteria_seen: set[tuple[str, str]] = set()
    for number, row in enumerate(rows, start=2):
        if not any(row.values()):
            continue
        option, criterion = row.get("option_name", ""), row.get("criterion", "")
        if not option or not criterion:
            errors.append(f"{path}:{number}: option_name and criterion are required.")
            continue
        pair = (option.casefold(), criterion.casefold())
        if pair in criteria_seen:
            errors.append(f"{path}:{number}: duplicate criterion '{criterion}' for '{option}'.")
        criteria_seen.add(pair)
        try:
            weight = float(row.get("weight_percent", ""))
            if weight < 0 or weight > 100:
                raise ValueError
            weights[option] = weights.get(option, 0.0) + weight
        except ValueError:
            errors.append(f"{path}:{number}: weight_percent must be a number from 0 to 100.")
        score_text = row.get("score_1_to_5", "")
        if score_text:
            try:
                score = float(score_text)
                if not 1 <= score <= 5:
                    raise ValueError
            except ValueError:
                errors.append(f"{path}:{number}: score_1_to_5 must be between 1 and 5.")
        elif row.get("evidence_summary") or row.get("source_ids"):
            warnings.append(f"{path}:{number}: evidence exists but score is blank; score only after applying consistent criteria.")
        if score_text and (not row.get("evidence_summary") or not row.get("source_ids")):
            warnings.append(f"{path}:{number}: scored row should include evidence_summary and source_ids.")
    for option, total in weights.items():
        if abs(total - 100.0) > 0.01:
            warnings.append(f"{path}: weights for '{option}' total {total:g}%, not 100%.")
    if not weights:
        errors.append(f"{path}: no valid weighted comparison rows found.")
    return errors, warnings

def main() -> int:
    parser = argparse.ArgumentParser(description="Audit research source logs and comparison CSVs.")
    parser.add_argument("--sources", type=Path, help="Source-log CSV to audit")
    parser.add_argument("--comparison", type=Path, help="Competitor-comparison CSV to audit")
    args = parser.parse_args()
    if not args.sources and not args.comparison:
        parser.error("provide --sources, --comparison, or both")
    failed = False
    for label, path, fn in (("SOURCES", args.sources, audit_sources), ("COMPARISON", args.comparison, audit_comparison)):
        if path is None:
            continue
        errors, warnings = fn(path)
        print(f"\n{label}: {path}")
        for warning in warnings:
            print(f"  WARN: {warning}")
        for error in errors:
            print(f"  ERROR: {error}")
        if errors:
            failed = True
            print("  RESULT: FAIL")
        else:
            print(f"  RESULT: PASS ({len(warnings)} warning(s))")
    return 1 if failed else 0

if __name__ == "__main__":
    sys.exit(main())

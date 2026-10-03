#!/usr/bin/env python3
"""Generate report.md from the deep-research JSON results.

Usage:
    uv run --with pyyaml python docs/research/subset-sum-n3/generate_report.py

Reads outline.yaml + fields.yaml and every JSON in the output_dir, skips
uncertain fields, and emits a TOC + per-category detail report.
"""

import json
import re
from pathlib import Path

import yaml

BASE = Path(__file__).resolve().parent
CATEGORY_TITLES = {
    "basic": "Basic",
    "complexity": "Complexity",
    "scope": "Scope",
    "method": "Method",
    "frontier": "Frontier",
    "assumptions": "Assumptions",
    "evidence": "Evidence",
}
TOC_FIELDS = ("worst_case_time", "numerical_exponent_and_record_year", "problem_variant")
SKIP = {"_source_file", "uncertain"}


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def load_field_order():
    data = yaml.safe_load((BASE / "fields.yaml").read_text())
    order = []
    all_names = set()
    for category, fields in data["fields"].items():
        for field in fields:
            order.append((category, field["name"]))
            all_names.add(field["name"])
    return order, all_names


def fmt(value):
    if isinstance(value, list):
        if value and all(isinstance(v, dict) for v in value):
            return "<br>".join(
                " | ".join(f"{k}: {fmt(v)}" for k, v in d.items()) for d in value
            )
        if len(value) <= 3 and sum(len(str(v)) for v in value) <= 120:
            return ", ".join(fmt(v) for v in value)
        return "<br>".join(f"- {fmt(v)}" for v in value)
    if isinstance(value, dict):
        return "; ".join(f"{k}: {fmt(v)}" for k, v in value.items())
    text = str(value).strip()
    return text


def is_uncertain(item, name, value):
    if name in SKIP or value is None:
        return True
    if isinstance(value, str) and ("[uncertain]" in value or not value.strip()):
        return True
    return name in (item.get("uncertain") or [])


def main():
    outline = yaml.safe_load((BASE / "outline.yaml").read_text())
    field_order, defined = load_field_order()
    results_dir = BASE / outline["execution"]["output_dir"].split("/")[-1]
    items = []
    for spec in outline["items"]:
        path = results_dir / f"{spec['name']}.json"
        if not path.exists():
            print(f"[WARN] missing {path}")
            continue
        items.append(json.loads(path.read_text()))

    lines = [f"# Deep research report — {outline['topic']}", ""]
    lines.append(f"{len(items)} items, generated from `{results_dir.name}/`.")
    lines += ["", "## Contents", ""]
    for i, item in enumerate(items, 1):
        exponent = str(item.get("numerical_exponent_and_record_year", ""))
        summary = fmt(exponent).split("|")[0].strip()
        if len(summary) > 120:
            summary = summary[:117].rstrip() + "..."
        anchor = slug(item.get("name", f"item-{i}"))
        suffix = f" — {summary}" if summary and "[uncertain]" not in summary else ""
        lines.append(f"{i}. [{item.get('name', 'item')}](#{anchor}){suffix}")
    lines += ["", "---", ""]

    for i, item in enumerate(items, 1):
        lines.append(f"## {item.get('name', f'item-{i}')}")
        lines.append("")
        for category, name in field_order:
            value = item.get(name)
            if is_uncertain(item, name, value):
                continue
            lines.append(f"- **{name}** ({CATEGORY_TITLES.get(category, category)}): {fmt(value)}")
        extra = {
            k: v
            for k, v in item.items()
            if k not in defined and k not in SKIP and v not in (None, "", [], {})
        }
        if extra:
            lines.append("- **Other Info**:")
            for key, value in extra.items():
                lines.append(f"  - {key}: {fmt(value)}")
        uncertain = item.get("uncertain") or []
        if uncertain:
            lines.append("- **Uncertain fields**:")
            lines += [f"  - {name}" for name in uncertain]
        lines.append("")

    (BASE / "report.md").write_text("\n".join(lines) + "\n")
    print(f"wrote {BASE / 'report.md'} ({len(items)} items)")


if __name__ == "__main__":
    main()

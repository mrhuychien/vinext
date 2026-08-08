#!/usr/bin/env python3
"""Measure what this pack still leaves untranslated, and refresh the work file.

Compares ``vinext/translations/vi.csv`` against the POT catalogues that Frappe,
ERPNext and HRMS extract from their own source, so coverage is measured against
strings that genuinely reach the UI rather than against itself.

    python3 scripts/audit_coverage.py               # download the POTs, report
    python3 scripts/audit_coverage.py --write       # also rewrite docs/untranslated-vi.csv
    python3 scripts/audit_coverage.py --pot-dir /tmp/pots   # reuse local copies

Why POT and not the shipped ``locale/*.po``: frappe's own ``vi.po`` carries a
handful of translated entries, so nearly every Desk string depends on this CSV.
Entries the upstream ``.po`` *does* translate are reported separately — those
arrive via the compiled ``.mo`` and need no work here.
"""

from __future__ import annotations

import argparse
import collections
import csv
import re
import sys
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CATALOGUE = REPO / "vinext" / "translations" / "vi.csv"
WORK_FILE = REPO / "docs" / "untranslated-vi.csv"

# app -> (owner/repo, git ref). Pinned to released versions, not branch heads.
#
# The ref matters more than it looks: upstream is actively translating into
# Vietnamese on the branches, and none of it has reached the tags yet. Counted
# from the shipped locale/vi.po:
#
#     frappe  v16.16.0        5 translated / 5903      <- what a v16.16.0 site runs
#     frappe  version-16   5955 translated / 6235      <- landed after the tag
#     hrms    version-16      6 translated / 2173
#     hrms    develop      2148 translated / 2253
#     erpnext version-16   9070 translated / 10084
#
# So on a released v16 site essentially all Desk chrome comes from this pack,
# while a later release will bring much of it upstream. Re-run this audit after
# any `bench update` — the gap moves.
SOURCES = {
    "frappe": ("frappe/frappe", "v16.16.0"),
    "erpnext": ("frappe/erpnext", "version-16"),
    "hrms": ("frappe/hrms", "version-16"),
}
RAW = "https://raw.githubusercontent.com/{repo}/{ref}/{app}/locale/{name}"

# Desk chrome — on screen in every session, so it dominates the impression of
# whether the UI "is in Vietnamese" at all.
P1_AREAS = {"frappe/public", "frappe/desk", "frappe/core"}
HELP_BLOCK_CHARS = 150


def unescape(text: str) -> str:
    out, i = [], 0
    while i < len(text):
        if text[i] == "\\" and i + 1 < len(text):
            out.append({"n": "\n", "t": "\t", "r": "\r"}.get(text[i + 1], text[i + 1]))
            i += 2
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


def parse_po(path: Path) -> list[dict]:
    """Parse a PO/POT file into entries keyed the way Frappe keys translations."""
    entries, block = [], []

    def flush(lines: list[str]) -> None:
        refs, ctxt, msgid, msgstr, field = [], "", None, "", None
        for line in lines:
            if line.startswith("#:"):
                refs += line[2:].split()
                continue
            if line.startswith("#"):
                continue
            head = re.match(r'^(msgctxt|msgid|msgid_plural|msgstr)\s+"(.*)"$', line)
            if head:
                kind, value = head.group(1), unescape(head.group(2))
                if kind == "msgctxt":
                    ctxt, field = value, "ctxt"
                elif kind == "msgid":
                    msgid, field = value, "id"
                elif kind == "msgstr":
                    msgstr, field = value, "str"
                else:
                    field = None
                continue
            cont = re.match(r'^"(.*)"$', line)
            if cont and field == "id" and msgid is not None:
                msgid += unescape(cont.group(1))
            elif cont and field == "ctxt":
                ctxt += unescape(cont.group(1))
            elif cont and field == "str":
                msgstr += unescape(cont.group(1))
        if msgid:
            entries.append(
                {
                    "key": msgid + (":" + ctxt if ctxt else ""),
                    "msgid": msgid,
                    "ctxt": ctxt,
                    "refs": refs,
                    "msgstr": msgstr,
                }
            )

    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.strip():
            block.append(raw)
        elif block:
            flush(block)
            block = []
    if block:
        flush(block)
    return entries


def load_catalogue() -> set[str]:
    """Keys this pack provides, keyed exactly as frappe/translate.py does."""
    keys = set()
    with CATALOGUE.open(encoding="utf-8", newline="") as fh:
        for row in csv.reader(fh):
            if len(row) not in (2, 3):
                continue
            source = row[0].replace("\\n", "\n")
            context = row[2] if len(row) == 3 else ""
            keys.add(f"{source}:{context}" if context else source)
    return keys


def fetch(pot_dir: Path, app: str, name: str) -> Path:
    repo, ref = SOURCES[app]
    dest = pot_dir / f"{app}-{name}"
    if not dest.exists():
        url = RAW.format(repo=repo, ref=ref, app=app, name=name)
        print(f"  fetching {url}", file=sys.stderr)
        urllib.request.urlretrieve(url, dest)
    return dest


def area_of(entry: dict) -> str:
    parts = entry["refs"][0].split(":")[0].split("/") if entry["refs"] else ["(no-ref)"]
    return "/".join(parts[:2]) if len(parts) > 1 else parts[0]


def tier_of(entry: dict) -> str:
    text, area = entry["msgid"], area_of(entry)
    if not re.search(r"[A-Za-z]", text) or re.fullmatch(r"[A-Za-z]", text):
        return "P0-skip"  # operators, single letters — not language
    if re.fullmatch(r"(?:[A-Z]{2,}|[a-z]+_[a-z_]+)", text):
        return "P5-review"  # CC/BCC/DRAFT — sometimes kept verbatim
    if len(text) > HELP_BLOCK_CHARS:
        return "P4-help-html"
    if area in P1_AREAS:
        return "P1-desk"
    if area.startswith(("erpnext/", "hrms/")):
        return "P2-business"
    return "P3-peripheral"


TIER_ORDER = {
    "P1-desk": 1,
    "P2-business": 2,
    "P3-peripheral": 3,
    "P4-help-html": 4,
    "P5-review": 5,
    "P0-skip": 6,
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pot-dir", type=Path, default=Path(".pot-cache"))
    ap.add_argument("--write", action="store_true", help="rewrite docs/untranslated-vi.csv")
    args = ap.parse_args()
    args.pot_dir.mkdir(parents=True, exist_ok=True)

    ours = load_catalogue()
    print(f"catalogue: {len(ours)} keys\n")

    gaps, grand_total, grand_done = [], 0, 0
    for app in SOURCES:
        pot = {e["key"]: e for e in parse_po(fetch(args.pot_dir, app, "main.pot"))}
        upstream = {
            e["key"] for e in parse_po(fetch(args.pot_dir, app, "vi.po")) if e["msgstr"]
        }
        missing = [e for k, e in pot.items() if k not in ours]
        # Entries upstream already translates arrive via the compiled .mo.
        free = [e for e in missing if e["key"] in upstream]
        real = [e for e in missing if e["key"] not in upstream]
        done = len(pot) - len(missing)
        grand_total += len(pot)
        grand_done += done
        print(
            f"{app:8}: {len(pot):6} strings | ours {done:6} ({100 * done / len(pot):5.1f}%)"
            f" | upstream .po covers {len(free):5} | GAP {len(real):5}"
        )
        gaps += real

    print(
        f"{'TOTAL':8}: {grand_total:6} strings | ours {grand_done:6} "
        f"({100 * grand_done / grand_total:5.1f}%)"
    )

    # POT files bundle strings from apps most sites do not install (e.g. banking).
    owned = [e for e in gaps if e["refs"] and e["refs"][0].split("/")[0] in SOURCES]
    foreign = len(gaps) - len(owned)
    print(f"\ngap: {len(gaps)} — {len(owned)} in frappe/erpnext/hrms, {foreign} in other apps")

    for entry in owned:
        entry["tier"], entry["area"] = tier_of(entry), area_of(entry)
    print("\nby tier:")
    counts = collections.Counter(e["tier"] for e in owned)
    for tier in sorted(counts, key=lambda t: TIER_ORDER[t]):
        print(f"   {tier:15} {counts[tier]:5}")

    print("\nlargest areas:")
    for area, n in collections.Counter(e["area"] for e in owned).most_common(10):
        print(f"   {n:5}  {area}")

    if args.write:
        owned.sort(key=lambda e: (TIER_ORDER[e["tier"]], e["area"], e["msgid"].lower()))
        WORK_FILE.parent.mkdir(parents=True, exist_ok=True)
        with WORK_FILE.open("w", encoding="utf-8", newline="") as fh:
            writer = csv.writer(fh, lineterminator="\n")
            writer.writerow(["tier", "area", "source_ref", "context", "source", "translation"])
            for e in owned:
                writer.writerow([e["tier"], e["area"], e["refs"][0], e["ctxt"], e["msgid"], ""])
        print(f"\nwrote {WORK_FILE.relative_to(REPO)} ({len(owned)} rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

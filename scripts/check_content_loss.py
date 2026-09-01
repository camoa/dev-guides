#!/usr/bin/env python3
"""Report source content that no published guide reflects.

`check_partition_sync.py` answers "was docs/ generated from the source file that
is on disk now?" A partition run that drops half a subsection still writes a
manifest hash that matches, so that check reports a clean catalog while the
content is gone. The heading-count check added in PR #44 does not catch it
either: content was lost two ways, and both keep the heading.

  * several source `###` subsections collapsed under one generic `## Decision`
    or `## Pattern`, and everything after the first was dropped
  * source "Common Mistakes" prose paraphrased into a short Wrong/Right table,
    which cut the explanation

This measures the second question at the granularity the loss happened: one
content unit — a list item, a table row, or a sentence.

A unit is REFLECTED when its normalised form appears verbatim somewhere in the
topic's published text. Normalisation removes markdown emphasis, links, code
ticks and whitespace, so rewrapping and bolding do not register as loss.
Paraphrase DOES register, which is the point: paraphrase is how the
partitioner shortened Common Mistakes and lost the explanation with it.

CALIBRATION. `drupal/facets` was repaired by hand in PR #48 and is the fixture
this script is tuned against. It scores 4 unreflected of 473 units (0.8%), and
all four are mid-sentence cross-references to other sections of the source guide
("see 17.1"), which the atomic guides legitimately replace with See Also links.
So ~1% is the noise floor, not zero. A topic near that figure is repaired; a
topic at 30% or more has lost content.

Two rules exist only because leaving them out produced false positives on that
fixture, and both are load-bearing:

  * lines inside a fenced code block are skipped. `normalise` strips fences from
    the published side, so comparing a fenced line against it reports every code
    example as lost. That alone was 129 false misses on facets.
  * a bullet that only points at another numbered section of the same source
    guide is skipped. That is navigation inside the comprehensive guide, and the
    atomic guides replace it with their own See Also links.

This is a report, never a gate. 12,027 units are unreflected today, so failing
on loss would fail every pull request. It exits 0 unconditionally, like
check_staleness.py.

    python3 scripts/check_content_loss.py                  # per-topic table
    python3 scripts/check_content_loss.py drupal/group     # and list that topic
"""

import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS = PROJECT_ROOT / "docs"
MANIFEST = PROJECT_ROOT / "partition-manifest.json"
GUIDES = Path.home() / "workspace" / "claude_memory" / "guides"

# Below this, a unit is too short to tell a real sentence from a fragment.
MIN_WORDS = 6

PARTITION_RE = re.compile(
    r"<!--\s*PARTITION:\s*([\w./-]+)\s*-->(.*?)<!--\s*END PARTITION:\s*\1\s*-->",
    re.S,
)

# "- 2.1 Installation & Setup — getting started": a pointer to another section of
# the same source guide, not content.
CROSSREF_RE = re.compile(r"^[-*]\s+\d+(?:\.\d+)*\s+\S")


def normalise(text: str) -> str:
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    text = re.sub(r"[`*_~#>|]+", " ", text)
    text = re.sub(r"[^a-z0-9 ]+", " ", text.lower())
    return re.sub(r"\s+", " ", text).strip()


def units(block: str):
    """Yield one unit per list item, table row, or sentence outside code fences."""
    in_fence = False
    for line in block.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or not stripped or stripped.startswith(("<!--", "#")):
            continue
        if CROSSREF_RE.match(stripped):
            continue
        if stripped.startswith(("-", "*", "|")) or re.match(r"^\d+\.", stripped):
            yield stripped
        else:
            yield from re.split(r"(?<=[.:!?])\s+", stripped)


def classify(unit: str) -> str:
    s = unit.lstrip()
    if s.startswith("|"):
        return "table row"
    if s.startswith(("-", "*")):
        return "bolded bullet" if "**" in s else "plain bullet"
    return "prose sentence"


def measure():
    manifest = json.loads(MANIFEST.read_text())
    by_hash = {
        hashlib.sha256(p.read_bytes()).hexdigest(): p for p in GUIDES.glob("*.md")
    }

    rows, kinds = [], Counter()
    total_units = total_missing = 0

    for topic, meta in sorted(manifest.items()):
        src = by_hash.get(str(meta.get("source_hash", "")))
        topic_dir = DOCS / topic
        if src is None or not topic_dir.is_dir():
            continue  # born-atomic or drifted; check_partition_sync.py owns those

        published = normalise(
            "\n".join(p.read_text(errors="ignore") for p in sorted(topic_dir.rglob("*.md")))
        )

        seen, missing = set(), []
        for _slug, block in PARTITION_RE.findall(src.read_text(errors="ignore")):
            for raw in units(block):
                norm = normalise(raw)
                if len(norm.split()) < MIN_WORDS or norm in seen:
                    continue
                seen.add(norm)
                if norm not in published:
                    missing.append(raw.strip())

        total_units += len(seen)
        total_missing += len(missing)
        for m in missing:
            kinds[classify(m)] += 1
        if missing:
            rows.append(
                {
                    "topic": topic,
                    "missing": len(missing),
                    "units": len(seen),
                    "pct": round(100 * len(missing) / max(len(seen), 1), 1),
                    "examples": missing,
                }
            )

    rows.sort(key=lambda r: -r["missing"])
    return rows, kinds, total_units, total_missing


def main() -> int:
    if not GUIDES.is_dir():
        print(f"source guides not found at {GUIDES}; cannot check", file=sys.stderr)
        return 0  # not a repo defect — the checkout has no sources beside it

    rows, kinds, total_units, total_missing = measure()
    pct = 100 * total_missing / max(total_units, 1)

    print("Content loss report")
    print(f"{len(rows)} topic(s) carry unreflected source content.")
    print(f"{total_missing} unreflected of {total_units} units ({pct:.1f}%).")
    print("Noise floor is about 1%: drupal/facets, repaired by hand, scores 0.8%.\n")
    print("By kind: " + ", ".join(f"{k} {v}" for k, v in kinds.most_common()) + "\n")

    print(f"{'topic':<44}{'missing':>8}{'units':>7}{'pct':>7}")
    for r in rows:
        print(f"{r['topic']:<44}{r['missing']:>8}{r['units']:>7}{r['pct']:>6.1f}%")

    if len(sys.argv) > 1:
        want = sys.argv[1]
        for r in rows:
            if r["topic"] == want:
                print(f"\nUnreflected in {want}:")
                for m in r["examples"]:
                    print("  " + m[:200])
                break
        else:
            print(f"\n{want}: nothing unreflected, or not a partitioned topic.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

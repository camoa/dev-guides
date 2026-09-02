#!/usr/bin/env python3
"""Bound the risk that re-partitioning a topic deletes something.

`check_content_loss.py` measures source -> published. This measures the other
direction, because re-partitioning is one-way: it regenerates `docs/` from the
source guide, so anything living only in `docs/` is destroyed by the repair.

READ THE NUMBER CORRECTLY. It is an upper bound on risk, not a count of
knowledge. Most of what it reports is the same knowledge in another shape:

  source guide   "LibSass is DEPRECATED. Dart Sass is REQUIRED."
  published page  | LibSass (node-sass) | DEPRECATED | Never use |

Re-partitioning replaces the table row with the prose. Nothing is lost. A page
routinely reformats source prose into tables, checklists and Wrong/Right pairs,
and no text match can trace a three-column grid back to the sentence it came
from. Shingle matching below removes about half the noise and does not solve
this; the residue is structural, not verbal.

CALIBRATION, and it is unflattering. On `design-systems/bootstrap`, all 226
flagged units were read against Bootstrap 5 and Sass documentation. **Two blocks
were genuinely new. 224 were reformatted duplicates the source already covered,
usually more fully.** Exact matching flagged 226, shingle matching flags 110,
and the truth was 2. Expect a true-positive rate near 1%.

So use it this way: zero orphans means re-partitioning that topic is certainly
safe. A non-zero count means someone must read those units before the repair
runs, and should expect nearly all of them to be duplicates. Never treat the
catalog total as content at risk.

When a unit IS genuinely new, it has two possible origins needing opposite
treatment, and nothing here can tell them apart:

  * knowledge added to a page and never written back to its source. Back-fill it
    into the source guide before that topic is re-partitioned, or it is gone.
  * invention by an earlier partition run. The bootstrap repair found a
    fabricated "Utility API System" section describing another guide's content,
    and a three-line colour fragment whose percentages match no documented
    Bootstrap default. Both were deleted, not preserved.

The opposite direction is asymmetric ON PURPOSE. check_content_loss.py DOES
count paraphrase as loss, because paraphrasing the source is exactly the defect
that shortened Common Mistakes and cut their explanations.

`index.md` and `sources-maintenance.md` are excluded: both are generated from
something other than the partition blocks, so they are orphans by construction.

    python3 scripts/check_orphan_content.py                  # per-topic table
    python3 scripts/check_orphan_content.py design-systems/bootstrap
"""

import hashlib
import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS = PROJECT_ROOT / "docs"
MANIFEST = PROJECT_ROOT / "partition-manifest.json"
GUIDES = Path.home() / "workspace" / "claude_memory" / "guides"

GENERATED = {"index.md", "sources-maintenance.md"}
MIN_WORDS = 6

# A published unit counts as held by the source when this share of its 3-word
# shingles appears there. Exact matching reported 9,928 across the catalog and
# 226 on bootstrap; this reports 3,875 and 110. The verified answer on bootstrap
# was 2, so the threshold removes noise it can measure and leaves the structural
# residue described above. Raising it hides real orphans; lowering it restores
# the exact-match noise.
SHINGLE_HIT = 0.5
SHINGLE_N = 3


def shingles(norm: str, n: int = SHINGLE_N):
    words = norm.split()
    if len(words) < n:
        return {norm} if norm else set()
    return {" ".join(words[i:i + n]) for i in range(len(words) - n + 1)}


def normalise(text: str) -> str:
    """Same shape as check_content_loss.normalise, but fenced code is KEPT.

    Stripping fences there is right, because it compares against a published
    side that also has them stripped. Here the comparison is against raw source
    text, so stripping would report every published code line as an orphan.
    """
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[`*_~#>|]+", " ", text)
    text = re.sub(r"[^a-z0-9 ]+", " ", text.lower())
    return re.sub(r"\s+", " ", text).strip()


def units(text: str):
    """One unit per list item, table row, or sentence. Frontmatter is skipped."""
    in_frontmatter = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped == "---":
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter or not stripped or stripped.startswith(("#", "<!--")):
            continue
        if set(stripped) <= set("-|: "):   # table rules
            continue
        if stripped.startswith(("-", "*", "|")) or re.match(r"^\d+\.", stripped):
            yield stripped
        else:
            yield from re.split(r"(?<=[.:!?])\s+", stripped)


def measure():
    manifest = json.loads(MANIFEST.read_text())
    by_hash = {
        hashlib.sha256(p.read_bytes()).hexdigest(): p for p in GUIDES.glob("*.md")
    }

    rows, total_orphan, total_units = [], 0, 0
    for topic, meta in sorted(manifest.items()):
        src = by_hash.get(str(meta.get("source_hash", "")))
        topic_dir = DOCS / topic
        if src is None or not topic_dir.is_dir():
            continue

        source = normalise(src.read_text(errors="ignore"))
        source_shingles = shingles(source)
        seen, orphans = set(), []
        for page in sorted(topic_dir.rglob("*.md")):
            if page.name in GENERATED:
                continue
            for raw in units(page.read_text(errors="ignore")):
                norm = normalise(raw)
                if len(norm.split()) < MIN_WORDS or norm in seen:
                    continue
                seen.add(norm)
                if norm in source:
                    continue
                own = shingles(norm)
                hit = len(own & source_shingles) / max(len(own), 1)
                if hit < SHINGLE_HIT:
                    orphans.append((page.name, raw.strip()))

        total_orphan += len(orphans)
        total_units += len(seen)
        if orphans:
            rows.append(
                {
                    "topic": topic,
                    "orphan": len(orphans),
                    "units": len(seen),
                    "pct": round(100 * len(orphans) / max(len(seen), 1), 1),
                    "examples": orphans,
                }
            )

    rows.sort(key=lambda r: -r["orphan"])
    return rows, total_units, total_orphan


def main() -> int:
    if not GUIDES.is_dir():
        print(f"source guides not found at {GUIDES}; cannot check", file=sys.stderr)
        return 0

    rows, total_units, total_orphan = measure()
    pct = 100 * total_orphan / max(total_units, 1)

    print("Orphan content report")
    print(f"{len(rows)} topic(s) publish content held by no source guide.")
    print(f"{total_orphan} of {total_units} published units ({pct:.1f}%).")
    print("An UPPER BOUND on risk, not a count of knowledge. Expect ~1% to be real:")
    print("on design-systems/bootstrap, 226 flagged units held 2 of genuinely new")
    print("content and 224 reformatted duplicates. Read them before repairing a topic.\n")

    print(f"{'topic':<44}{'orphan':>8}{'units':>7}{'pct':>7}")
    for r in rows:
        print(f"{r['topic']:<44}{r['orphan']:>8}{r['units']:>7}{r['pct']:>6.1f}%")

    if len(sys.argv) > 1:
        want = sys.argv[1]
        for r in rows:
            if r["topic"] == want:
                print(f"\nOrphan units in {want}:")
                for page, text in r["examples"]:
                    print(f"  [{page}] {text[:180]}")
                break
        else:
            print(f"\n{want}: no orphan content, or not a partitioned topic.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

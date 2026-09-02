#!/usr/bin/env python3
"""Fail the build on the three publishing defects nothing else catches.

`mkdocs build --strict` is a good gate and it is blind to all three of these.
Each was found only after it had already shipped, by a detector run by hand.

  local-path   An absolute path from someone's machine in a published page.
               MkDocs logs an absolute link as INFO, never a warning, so
               --strict passes. 44 pages were serving one on 2026-09-02.

  slug-drift   A published file added or removed without the manifest saying
               so. A partition slug IS a live published URL: renaming one 404s
               every existing link, and llms.txt links only topic indexes, so
               nothing else notices.

  when-to-use  A guide whose `## When to Use` blockquote is not the source's
               own When-to-Use text. 19 of 22 drupal/blocks guides published
               their own `tldr` there instead; the heading was present, the
               section looked complete, and the source text was gone.

Every check is a RATCHET against `publish-invariants-baseline.json`, which
records what was already broken when the check landed. Anything not in the
baseline fails the build. An entry that becomes clean should be deleted from
the baseline in the same PR that fixes it — the file only ever shrinks, and
`--update-baseline` exists to regenerate it, never to paper over a regression.

Run with no arguments to check; `--update-baseline` rewrites the file.
"""

import hashlib
import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS = PROJECT_ROOT / "docs"
MANIFEST = PROJECT_ROOT / "partition-manifest.json"
GUIDES_DIR = Path.home() / "workspace" / "claude_memory" / "guides"

BORN_ATOMIC = "new-guide-no-source"

# Not published guides: an index page and a generated manifest page.
NOT_A_GUIDE = {"index.md", "sources-maintenance.md"}

# A home directory from any machine, not just this one.
LOCAL_PATH_RE = re.compile(r"(?:/home/[a-z_][a-z0-9_-]*|/Users/[A-Za-z][A-Za-z0-9._-]*)/")

# The source writes this heading more than one way; the published heading is
# always `## When to Use`.
SRC_WTU_RE = re.compile(r"^### When to Use(?: This Section)?\s*\n(.*?)(?=\n### |\Z)", re.S | re.M)
# The published section body, whatever the layout: some topics use a
# blockquote, some plain prose, and the blank line after the heading is
# not consistent. The invariant is the TEXT, not the layout.
PUB_WTU_RE = re.compile(r"^## When to Use[^\n]*\n(.*?)(?=\n#{2,3} )", re.S | re.M)
PARTITION_RE = re.compile(r"<!-- PARTITION: ([\w-]+) -->(.*?)<!-- END PARTITION: \1 -->", re.S)

BASELINE = PROJECT_ROOT / "publish-invariants-baseline.json"

# A documented exception, not a baseline entry: the ATK guide configures a
# remote snapshot host whose service account is named `testor`, so
# `/home/testor/snapshots` is the path being documented rather than a path
# from anyone's machine.
ALLOWED_LOCAL_PATHS = {
    ("docs/testing/atk/atk-testor.md", "/home/testor/"),
}


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text())


def sources_by_hash() -> dict:
    if not GUIDES_DIR.is_dir():
        return {}
    return {hashlib.sha256(p.read_bytes()).hexdigest(): p for p in GUIDES_DIR.glob("*.md")}


def published_guides(topic: str) -> list:
    d = DOCS / topic
    if not d.is_dir():
        return []
    return sorted(p for p in d.glob("*.md") if p.name not in NOT_A_GUIDE)


def check_local_paths() -> list:
    hits = []
    for p in sorted(DOCS.rglob("*.md")):
        for n, line in enumerate(p.read_text(errors="replace").splitlines(), 1):
            m = LOCAL_PATH_RE.search(line)
            if not m:
                continue
            rel = str(p.relative_to(PROJECT_ROOT))
            if (rel, m.group(0)) in ALLOWED_LOCAL_PATHS:
                continue
            hits.append(f"{rel}:{n}: {m.group(0)}")
    return hits


def source_slugs(src: str) -> list:
    """Slugs of complete partitions only.

    PARTITION_RE requires a matching END marker, which is what keeps the
    literal `<!-- PARTITION: name -->` that guides use when *explaining* the
    convention out of the results.
    """
    return [slug for slug, _ in PARTITION_RE.findall(src)]


def check_slug_drift(manifest: dict) -> list:
    """Every complete source partition has a page, and every page has a partition.

    Compares the source directly rather than trusting `guides_extracted`, which
    is written by the same run that writes the pages and so cannot contradict
    it. This is what catches a partition that was never published at all.
    """
    by_hash = sources_by_hash()
    hits = []
    for topic, meta in sorted(manifest.items()):
        h = str(meta.get("source_hash", ""))
        if h == BORN_ATOMIC:
            continue
        src_path = by_hash.get(h)
        if src_path is None:
            continue  # drifted; check_partition_sync.py owns that
        # The topic index and the sources manifest are generated pages, not
        # partitions: index.md by the partitioner's index template, and
        # sources-maintenance.md by generate_sources_maintenance.py. A few
        # source guides also carry a `sources*` partition that feeds it. Neither
        # side of this comparison is about them.
        want = {s for s in source_slugs(src_path.read_text()) if not s.startswith("sources")}
        have = {p.stem for p in (DOCS / topic).glob("*.md")} - {"index", "sources-maintenance"}
        missing = sorted(want - have)
        extra = sorted(have - want)
        if missing:
            hits.append(
                f"{topic}: {len(missing)} source partition(s) with no published page "
                f"({', '.join(missing)}). The whole guide is absent from the site."
            )
        if extra:
            hits.append(
                f"{topic}: {len(extra)} published page(s) with no source partition "
                f"({', '.join(extra)}). If a slug was renamed, every existing link "
                "to the old one now 404s and needs a redirect_maps entry."
            )
    return hits


def check_when_to_use(manifest: dict) -> tuple:
    by_hash = sources_by_hash()
    if not by_hash:
        return [], [], "source guides not found; When-to-Use check skipped"

    failures, ratcheted = [], []
    for topic, meta in sorted(manifest.items()):
        h = str(meta.get("source_hash", ""))
        if h == BORN_ATOMIC:
            continue
        src_path = by_hash.get(h)
        if src_path is None:
            continue  # drifted; check_partition_sync.py owns that
        src = src_path.read_text()
        bad = []
        for slug, body in PARTITION_RE.findall(src):
            m = SRC_WTU_RE.search(body)
            f = DOCS / topic / f"{slug}.md"
            if not m or not f.exists():
                continue
            want = m.group(1).strip()
            pm = PUB_WTU_RE.search(f.read_text())
            if not pm:
                continue
            have = re.sub(r"^> ?", "", pm.group(1), flags=re.M).strip()
            if have != want:
                bad.append(f"{topic}/{slug}")
        failures.extend(bad)
    return failures, ratcheted, ""


# The source guides live outside this repository, so CI has only `docs/`.
# local-path is checked there; slug-drift and when-to-use need the sources and
# are skipped rather than silently passing.
SOURCE_DEPENDENT = ("slug-drift", "when-to-use")


def collect(manifest: dict) -> tuple:
    have_sources = bool(sources_by_hash())
    found = {"local-path": check_local_paths()}
    if have_sources:
        wtu, _, _ = check_when_to_use(manifest)
        found["slug-drift"] = check_slug_drift(manifest)
        found["when-to-use"] = wtu
    return found, have_sources


def main() -> int:
    manifest = load_manifest()
    found, have_sources = collect(manifest)

    if not have_sources:
        print(f"source guides not found at {GUIDES_DIR};")
        print(f"  {', '.join(SOURCE_DEPENDENT)} SKIPPED — run this locally to check them.\n")

    if "--update-baseline" in sys.argv:
        if not have_sources:
            print("refusing to write a baseline without the source guides: it would "
                  "drop every slug-drift and when-to-use entry.")
            return 1
        BASELINE.write_text(json.dumps({k: sorted(v) for k, v in found.items()}, indent=2) + "\n")
        total = sum(len(v) for v in found.values())
        print(f"baseline written with {total} known entr(ies) across {len(found)} check(s).")
        print("Delete entries as they are fixed; never add one to silence a regression.")
        return 0

    baseline = json.loads(BASELINE.read_text()) if BASELINE.exists() else {}
    failed = False

    for check, hits in found.items():
        known = set(baseline.get(check, []))
        new = [h for h in hits if h not in known]
        fixed = known - set(hits)
        print(f"{check}: {len(hits)} total, {len(new)} NOT in the baseline, {len(fixed)} fixed")
        for h in new[:40]:
            print("   NEW ", h)
        if fixed:
            print(f"   {len(fixed)} baseline entr(ies) now clean — delete them from "
                  f"{BASELINE.name} in this PR.")
        if new:
            failed = True

    if failed:
        print("\nFAILED — a new violation, not a pre-existing one. "
              "See this script's docstring for what each check protects.")
        return 1
    print("\nNo new publishing-invariant violations.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

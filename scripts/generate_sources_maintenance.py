#!/usr/bin/env python3
"""Publish each topic's `Sources & Maintenance Manifest` from its source guide.

A source guide ends with a manifest recording what the guide was written
against — web sources with a last-verified date, the code read in the research
install, and a version history. That is the evidence behind every claim in the
topic, and it was being left in the source rather than published, so a reader
of the site could not see what a guide was checked against or when.

This is generation, not authoring: the section is copied from the source guide,
its headings demoted one level to sit under the page's H1, and nothing is
rewritten. Topics with no source guide (born-atomic) and sources with no
manifest section are reported, never invented.

    python3 scripts/generate_sources_maintenance.py          # report only
    python3 scripts/generate_sources_maintenance.py --apply  # write files
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

# Source guides number their sections inconsistently — `## Sources & Maintenance
# Manifest`, `## 10. Sources & Maintenance Manifest`, `## 22.0 Sources &
# Maintenance Manifest`, `## Sources and References`, `## Maintenance
# Information` are all in use. Match the number prefix optionally and accept the
# known heading variants, or five topics that DO record their sources look as
# though they record none.
MANIFEST_RE = re.compile(
    r"^##\s+(?:[\d.]+\s+)?"
    r"(?:Sources?\s*(?:&|and|&amp;)\s*(?:Maintenance|References)"
    r"|Maintenance\s+Information)"
    r"[^\n]*\n(.*?)(?=\n##\s(?!#)|\Z)",
    re.S | re.M,
)


def demote(md: str) -> str:
    """Source `###` becomes published `##`, below the page's own H1."""
    fences: list[str] = []

    def stash(m: re.Match) -> str:
        fences.append(m.group(0))
        return f"\x00FENCE{len(fences) - 1}\x00"

    md = re.sub(r"```.*?```", stash, md, flags=re.S)
    md = re.sub(r"^###\s+", "## ", md, flags=re.M)
    for i, f in enumerate(fences):
        md = md.replace(f"\x00FENCE{i}\x00", f)
    return md


def main() -> int:
    apply = "--apply" in sys.argv
    manifest = json.loads(MANIFEST.read_text())
    by_hash = {
        hashlib.sha256(p.read_bytes()).hexdigest(): p for p in GUIDES.glob("*.md")
    }

    wrote, existing, no_source, no_manifest = [], [], [], []
    for topic, meta in sorted(manifest.items()):
        target = DOCS / topic / "sources-maintenance.md"
        if target.exists():
            existing.append(topic)
            continue
        src = by_hash.get(str(meta.get("source_hash")))
        if src is None:
            no_source.append(topic)
            continue
        m = MANIFEST_RE.search(src.read_text(errors="ignore"))
        if not m:
            no_manifest.append(topic)
            continue

        body = demote(m.group(1).strip())
        name = topic.rsplit("/", 1)[-1].replace("-", " ")
        page = (
            "---\n"
            f'description: "Source references and maintenance manifest for the {name} '
            'guides — web sources, code sources, and version history"\n'
            "---\n\n"
            "# Sources & Maintenance\n\n"
            f"{body}\n"
        )
        if apply:
            target.write_text(page)
        wrote.append(topic)

    print(f"already published : {len(existing)}")
    print(f"no source guide   : {len(no_source)}  {', '.join(no_source) if no_source else ''}")
    print(f"source has none   : {len(no_manifest)}")
    for t in no_manifest:
        print(f"    {t}")
    print(f"{'WROTE' if apply else 'would write'}    : {len(wrote)}")
    if not apply and wrote:
        print("\n  run with --apply to write them")
    return 0


if __name__ == "__main__":
    sys.exit(main())

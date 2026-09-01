#!/usr/bin/env python3
"""Report topics whose published guides have drifted from their source guide.

The publishing model is one-way: a comprehensive source guide in
~/workspace/claude_memory/guides/ carries PARTITION markers, and the partitioner
generates docs/. Nothing checked that docs/ still reflects the source it was
generated from, so a source edit that was never partitioned — or a hand-edit to
docs/ — went unnoticed until someone happened to diff them.

Three states, and only the third is a defect:

  in-sync     manifest source_hash matches a source file on disk
  born-atomic source_hash is the `new-guide-no-source` sentinel — the topic was
              authored directly in docs/ and has no source guide. Legitimate.
  DRIFTED     source_hash matches nothing on disk: the source moved after the
              last partition run, and docs/ is behind.

Exit 1 on any drift.
"""

import hashlib
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MANIFEST = PROJECT_ROOT / "partition-manifest.json"
GUIDES_DIR = Path.home() / "workspace" / "claude_memory" / "guides"

# A topic authored directly in docs/, with no comprehensive source guide behind
# it. Recorded explicitly so it reads as a declared state, not a missing hash.
BORN_ATOMIC = "new-guide-no-source"


def main() -> int:
    manifest = json.loads(MANIFEST.read_text())
    if not GUIDES_DIR.is_dir():
        print(f"source guides not found at {GUIDES_DIR}; cannot check", file=sys.stderr)
        return 0  # not a repo defect — the checkout has no sources beside it

    on_disk = {
        hashlib.sha256(p.read_bytes()).hexdigest(): p.name
        for p in GUIDES_DIR.glob("*.md")
    }

    in_sync, born_atomic, drifted = [], [], []
    for topic, meta in sorted(manifest.items()):
        h = str(meta.get("source_hash", ""))
        if h == BORN_ATOMIC:
            born_atomic.append(topic)
        elif h in on_disk:
            in_sync.append(topic)
        else:
            drifted.append((topic, meta.get("partitioned", "?")))

    print("Partition sync report")
    print(f"{len(manifest)} topics: {len(in_sync)} in sync, "
          f"{len(born_atomic)} born-atomic, {len(drifted)} drifted.\n")

    if born_atomic:
        print(f"Born-atomic ({len(born_atomic)}) — authored in docs/, no source guide")
        for t in born_atomic:
            print(f"  {t}")
        print()

    if drifted:
        print(f"DRIFTED ({len(drifted)}) — source changed after the last partition run")
        for t, when in drifted:
            print(f"  {t} (last partitioned {when})")
        print("\nRepair: re-partition the topic, then refresh its source_hash. Never")
        print("hand-edit docs/ to close the gap — that is what caused it.")
        return 1

    print("No drift.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

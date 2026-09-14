"""Tests for the plays.json manifest in scripts/generate_llms.py.

A playbook set is a topic whose index.md declares `playbook: true`. The site
build lifts each guide's rule, rationale and scope out of its bold labels into
one file per set, so the loader that follows plays by path never parses a
routing table. Two things are load-bearing and are tested here: the gate (a
topic without the marker gets no file) and the field contract (a label a guide
lacks yields an empty string, never a missing key).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import generate_llms as g  # noqa: E402

GUIDE = """---
description: d
---

# Use Bootstrap Before Custom CSS

**What:** Check Bootstrap first.

**Rationale:** Bootstrap's utilities are tested
across breakpoints.

**Example:**

```scss
.card { padding: 1rem; }
```
"""


def test_labelled_paragraph_joins_lines_and_stops_at_blank():
    assert g.extract_labelled_paragraph(GUIDE, "**What:**") == "Check Bootstrap first."
    assert g.extract_labelled_paragraph(GUIDE, "**Rationale:**") == (
        "Bootstrap's utilities are tested across breakpoints."
    )


def test_missing_label_is_empty_not_absent():
    assert g.extract_labelled_paragraph(GUIDE, "**When it applies:**") == ""


def write_topic(docs: Path, key: str, marker: str) -> None:
    topic = docs / key
    topic.mkdir(parents=True)
    (topic / "index.md").write_text(f"---\ndescription: t\n{marker}---\n\n# T\n", encoding="utf-8")
    (topic / "use-bootstrap.md").write_text(GUIDE, encoding="utf-8")
    (topic / "sources-maintenance.md").write_text("# generated\n", encoding="utf-8")


def test_plays_json_only_for_marked_topics(tmp_path, monkeypatch):
    docs, site = tmp_path / "docs", tmp_path / "site"
    write_topic(docs, "drupal/best-practices/camoa", "playbook: true\n")
    write_topic(docs, "drupal/forms", "")
    monkeypatch.setattr(g, "DOCS_DIR", docs)
    monkeypatch.setattr(g, "SITE_DIR", site)
    topics = [{"topic_key": "drupal/best-practices/camoa"}, {"topic_key": "drupal/forms"}]

    assert g.build_plays_manifests(topics) == 1
    assert not (site / "drupal/forms/plays.json").exists()

    plays = json.loads((site / "drupal/best-practices/camoa/plays.json").read_text())
    assert [p["id"] for p in plays] == ["use-bootstrap"]
    play = plays[0]
    assert list(play) == g.PLAY_FIELDS
    assert play["title"] == "Use Bootstrap Before Custom CSS"
    assert play["guide"] == "use-bootstrap.md"
    assert play["when"] == ""
    assert len(play["sha256"]) == 64

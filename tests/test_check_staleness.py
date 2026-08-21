"""Regression tests for the branch-aware release resolver in
scripts/check_staleness.py.

Fixtures are real release-history XML captured 2026-08-16 from
updates.drupal.org/release-history/<project>/current (see
tests/fixtures/release-history/). No network access at test time.

Each case reproduces a real branch-resolution failure documented in
proposals/guide-staleness-convention.md. A naive global date-sort over the
release list gives the wrong answer for two of these projects because a
newer tag can land on an older, no-longer-current maintenance branch:

- eca: 2.1.22 is tagged a day after 3.1.5 but sits on the 2.1. branch, not
  the current 3.1. branch.
- group: the 4.0. branch carries only 4.0.0-alpha1 and 4.0.x-dev, so the
  highest supported branch carries no stable at all and stable resolution
  falls back to the older 3.3. line.
- search_api_solr: 4.3.14 is tagged after 4.4.0 but on the 4.3. branch,
  which is not the current branch.

Two distinct questions are under test, answered by two different functions:

- resolve_current_version() -- "what is this project's current version?"
  Resolution walks supported branches high to low and stops at the highest
  branch that ACTUALLY CARRIES a tag in the requested channel. drupal.org
  lists a branch as supported the moment it is opened, before it has any
  release, so "highest supported branch" alone resolves to nothing for
  projects whose newest branch is empty or alpha-only.
- newest_stable_on_branch() -- "does THIS branch have a stable yet?"
  Branch-scoped, and the test that retires an alpha exception recorded
  against one specific line.
"""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures" / "release-history"
sys.path.insert(0, str(ROOT / "scripts"))

from check_staleness import (  # noqa: E402
    newest_stable_on_branch,
    resolve_current_version,
)


def _load(name: str) -> str:
    return (FIXTURES / f"{name}.xml").read_text()


ECA = _load("eca")
GROUP = _load("group")
SEARCH_API_SOLR = _load("search_api_solr")


def test_eca_resolves_to_newest_tag_on_current_branch_not_newest_by_date():
    result = resolve_current_version(ECA, channel="stable")
    assert result["version"] == "3.1.5"
    assert result["version"] != "2.1.22"


def test_search_api_solr_resolves_to_current_branch_not_newest_by_date():
    result = resolve_current_version(SEARCH_API_SOLR, channel="stable")
    assert result["version"] == "4.4.0"
    assert result["version"] != "4.3.14"


def test_group_stable_falls_back_to_highest_branch_that_carries_a_stable():
    """Group's highest supported branch (4.0.) carries no stable, so stable
    resolution falls back to 3.3. and returns 3.3.5.

    3.3.5 is genuinely Group's project-wide newest stable, sitting on the older
    3.3. maintenance line. This is deliberately NOT the answer to "does the
    tracked 4.0.x branch have a stable yet?" -- that is a branch-scoped
    question, answered by newest_stable_on_branch() below, and it is the one
    that governs the alpha exception.
    """
    result = resolve_current_version(GROUP, channel="stable")
    assert result["version"] == "3.3.5"
    assert result["branch"] == "3.3."
    assert result["error"] is None


def test_group_alpha_channel_resolves_to_alpha_tag():
    result = resolve_current_version(GROUP, channel="alpha")
    assert result["version"] == "4.0.0-alpha1"


def test_group_tracked_alpha_branch_has_no_stable_yet():
    """The check that justifies Group's alpha exception, and that will fire the
    day 4.0.0 stable lands: the 4.0. line carries only 4.0.0-alpha1 and
    4.0.x-dev, so it has no stable of its own.
    """
    assert newest_stable_on_branch(GROUP, "4.0.") is None


def test_group_older_line_does_not_retire_the_alpha_exception():
    """3.3. does have a stable -- which is exactly why the exception test has to
    be branch-scoped. A project-wide stable lookup would see 3.3.5 and wrongly
    conclude Group's tracked 4.0.x line had shipped one.
    """
    assert newest_stable_on_branch(GROUP, "3.3.") == "3.3.5"


def test_newest_stable_on_current_branch_positive_case():
    assert newest_stable_on_branch(SEARCH_API_SOLR, "4.4.") == "4.4.0"


def test_newest_stable_on_branch_is_scoped_to_the_branch_asked_for():
    """Branch scoping cuts both ways: asking about eca's older 2.1. line returns
    that line's own newest stable, not the project-current 3.1.5.
    """
    assert newest_stable_on_branch(ECA, "3.1.") == "3.1.5"
    assert newest_stable_on_branch(ECA, "2.1.") == "2.1.22"


@pytest.mark.parametrize(
    "fixture,channel",
    [
        (ECA, "stable"),
        (ECA, "alpha"),
        (GROUP, "stable"),
        (GROUP, "alpha"),
        (SEARCH_API_SOLR, "stable"),
        (SEARCH_API_SOLR, "alpha"),
    ],
)
def test_dev_snapshot_never_returned_as_resolved_version(fixture, channel):
    """A bare -dev snapshot (e.g. 4.0.x-dev) must never be returned as the
    resolved version, regardless of channel."""
    result = resolve_current_version(fixture, channel=channel)
    if result["version"] is not None:
        assert "-dev" not in result["version"]

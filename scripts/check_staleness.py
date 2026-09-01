#!/usr/bin/env python3
"""Report which guide topics have fallen behind the releases they document.

Implements proposals/guide-staleness-convention.md. Reads locally:

  * the repo-wide core baseline from `guides.yml`
  * every topic's `tracks:` frontmatter block in docs/**/index.md
  * the `partitioned` dates already recorded in partition-manifest.json
  * whether each topic carries a sources-maintenance.md

Fetches `updates.drupal.org/release-history/<project>/current` once per declared
project, plus core's equivalent.

Reports six categories:

  Unparseable frontmatter a guide's frontmatter block does not parse as YAML
                         at all. Nothing else in this report can be true or
                         false for that file -- drift, exceptions, core
                         assertions -- because every one of those readers,
                         this checker included, silently skips a file it
                         cannot parse. Listed by name so it is never
                         rediscovered by accident
  Drift                  declared version is behind the current tag on the
                         current branch; a new major is reported apart from a
                         patch bump because they are different sizes of work.
                         A guide that states no version while upstream resolves
                         fine is drift too, reported under its own label
  Unjustified exception  topic declares `channel: alpha` but a stable release
                         now exists on the same branch the alpha sits on
  Unverified             `verified` is older than the threshold; the version may
                         be right and nobody has read the prose. A purely local
                         check — it is never suppressed by a failed fetch
  Undeclared             no `tracks` key at all, or no sources-maintenance.md
  Core version           a file's `drupal_version` names a core branch that is
    assertions           no longer supported, sits off the baseline line, or
                         disagrees with its own siblings

Exit code is 2 on a malformed invocation; the always-0 rule below is about
findings, not about a run that never happened.

Anything that could not be resolved — a 404, a network error, a project whose
branch structure does not parse, a track missing its `declared` value — is
listed BY NAME under "could not check". The dangerous failure for an audit tool
is not a crash, it is a clean report that quietly skipped six projects.

Exit code is ALWAYS 0. Upstream tagging a release is not a defect in whatever
pull request happens to be open, and failing on it would stall unrelated work
every time any of twenty-five projects cuts a release. A scheduled workflow runs
this and writes the report to a standing tracking issue.

Pure stdlib + PyYAML (already required by validate_recipes.py); the resolver
itself is stdlib-only and network-free so it can be tested against saved XML.
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timezone
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
GUIDES_YML = PROJECT_ROOT / "guides.yml"
MANIFEST = PROJECT_ROOT / "partition-manifest.json"

RELEASE_HISTORY_URL = "https://updates.drupal.org/release-history/{project}/current"

# Default from the convention. 90 and 180 catch the same cohort on the first
# run, and a threshold that flags most of the repo on day one gets ignored.
DEFAULT_UNVERIFIED_DAYS = 180

FETCH_TIMEOUT = 30
FETCH_WORKERS = 6
USER_AGENT = "dev-guides-staleness-checker (+https://camoa.github.io/dev-guides/)"

# Prerelease ordering. Stable outranks every suffix; a bare -dev snapshot sits
# at the bottom and is never a resolvable version in either channel.
PRE_RANK = {"dev": -1, "unstable": 0, "alpha": 1, "beta": 2, "rc": 3, "": 4}

# Suffixes the "alpha" channel additionally accepts. "stable" accepts none.
ALPHA_CHANNEL_SUFFIXES = {"alpha", "beta", "rc", "unstable"}

# 8.x-1.  — the legacy pre-semver Drupal branch format. Sorts below every
# semantic branch regardless of the leading core number, because 8.x-1.x
# predates the 1.0.0/2.0.0 lines rather than following them.
LEGACY_BRANCH_RE = re.compile(r"^(\d+)\.x-(.+)$")

# 4.0.0-alpha1 / 3.1.5 / 8.x-1.41 / 1.1.x-dev
VERSION_RE = re.compile(
    r"^v?(?:(?P<legacy>\d+)\.x-)?"
    r"(?P<nums>[0-9x]+(?:\.[0-9x]+)*)"
    r"(?:-(?P<pre>[A-Za-z]+)(?P<prenum>\d*))?$"
)


# --------------------------------------------------------------------------
# Version handling
# --------------------------------------------------------------------------


def parse_version(text: str):
    """Parse a version string into a comparable shape.

    Returns (nums, pre_rank, pre_num, is_dev) or None if unparseable.
    `nums` holds one entry per dotted component; an `x` wildcard becomes None so
    a declaration of `1.1.x` compares equal at that position instead of
    pretending to state a patch level.
    """
    if not text:
        return None
    # Tolerate a composer-style constraint in `declared` (^3.0, ~2.1): it states
    # a version, just with an operator in front of it.
    text = str(text).strip().lstrip("^~>=< ")
    m = VERSION_RE.match(text)
    if not m:
        return None
    nums = tuple(None if part == "x" else int(part) for part in m.group("nums").split("."))
    pre = (m.group("pre") or "").lower()
    if pre and pre not in PRE_RANK:
        return None
    pre_num = int(m.group("prenum")) if m.group("prenum") else 0
    return nums, PRE_RANK[pre], pre_num, pre == "dev"


def version_sort_key(text: str):
    """Sort key for two tags known to live on the same branch.

    Deliberately version-based, never date-based. A date sort is the exact bug
    this checker exists to avoid, so no code path here falls back to one.
    """
    parsed = parse_version(text)
    if parsed is None:
        return ((0,), -99, 0)
    nums, pre_rank, pre_num, _ = parsed
    padded = tuple((n if n is not None else 0) for n in nums) + (0,) * (6 - len(nums))
    return (padded, pre_rank, pre_num)


def branch_sort_key(branch: str):
    """Sort key for a `supported_branches` entry such as `3.1.` or `8.x-1.`.

    Legacy `N.x-M.` branches go in a lower tier than semantic branches: Group
    supports `2.3.,3.3.,4.0.,8.x-1.` and the current branch is 4.0., not the
    numerically larger 8.x-1.
    """
    stripped = branch.rstrip(".")
    legacy = LEGACY_BRANCH_RE.match(stripped)
    if legacy:
        tail = legacy.group(2).rstrip(".")
        parts = [int(p) for p in tail.split(".") if p.isdigit()]
        return (0, (int(legacy.group(1)), *parts))
    parts = [int(p) for p in stripped.split(".") if p.isdigit()]
    return (1, tuple(parts))


def channel_allows(version: str, channel: str) -> bool:
    """Does this tag belong to the requested channel?

    A bare -dev snapshot is excluded from BOTH channels: the editorial policy is
    that untagged development branches are not documented.
    """
    parsed = parse_version(version)
    if parsed is None:
        return False
    _, pre_rank, _, is_dev = parsed
    if is_dev:
        return False
    is_stable = pre_rank == PRE_RANK[""]
    if channel == "stable":
        return is_stable
    return is_stable or pre_rank in {PRE_RANK[s] for s in ALPHA_CHANNEL_SUFFIXES}


# --------------------------------------------------------------------------
# The resolver — the only part with real logic, and the part that has already
# produced wrong answers twice.
#
# Two rules here look like they could be simplified. Neither can.
#
# 1. Releases are grouped by branch and the newest tag is read off ONE branch.
#    Never date-sort the feed. ECA tagged 2.1.22 a day after 3.1.5 on an older
#    maintenance line, and Search API Solr's 4.3.14 postdates 4.4.0 the same
#    way; a global date sort reports the superseded line as current in both.
#
# 2. The chosen branch is the highest supported branch THAT CARRIES A TAG in
#    the requested channel, not simply the highest supported branch. drupal.org
#    lists a branch as supported from the moment it is opened, before it has
#    any release at all. AI supports 1.3.,1.4.,1.5.,2.0. where 2.0. has no
#    releases and 1.5. has only an rc, so the current stable is 1.4.6 on 1.4.
#    Better Exposed Filters supports 6.0.,7.1.,8.0. where 8.0. is a lone alpha,
#    so the current stable is 7.1.3 on 7.1. Without the fallback both projects
#    resolve to nothing and sit in "could not check" forever.
#
#    The fallback is why the alpha-exception test is branch-scoped: see
#    newest_stable_on_branch(). Group's exception covers its 4.0.x line, and
#    the resolver's project-wide answer for Group's stable channel is 3.3.5 on
#    the older 3.3. line — a true statement that must not be read as "the
#    tracked branch now has a stable".
# --------------------------------------------------------------------------


def _parse_feed(xml_text: str):
    """Return (root, branches_high_to_low, error)."""
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        return None, None, f"release history XML did not parse: {exc}"

    # drupal.org answers an unknown project with a document whose ROOT is
    # <error>No release history was found …</error> — not a child of <project> —
    # so the root tag has to be checked as well as a nested element.
    if root.tag == "error":
        return None, None, (root.text or "no release history for this project").strip()
    feed_error = root.findtext("error")
    if feed_error:
        return None, None, feed_error.strip()

    raw_branches = root.findtext("supported_branches")
    if not raw_branches or not raw_branches.strip():
        return (
            None,
            None,
            "project declares no <supported_branches>; branch structure does not parse",
        )
    branches = [b.strip() for b in raw_branches.split(",") if b.strip()]
    if not branches:
        return None, None, f"<supported_branches> did not parse: {raw_branches!r}"

    try:
        branches.sort(key=branch_sort_key, reverse=True)
    except (TypeError, ValueError) as exc:
        return None, None, f"<supported_branches> did not parse: {raw_branches!r} ({exc})"

    if root.find("releases") is None:
        return None, None, "release history contains no <releases>"

    return root, branches, None


def _tags_on_branch(root, branch: str, channel: str) -> list[tuple[str, str]]:
    """Every published tag on one branch that belongs to `channel`."""
    tags = []
    for release in root.find("releases").findall("release"):
        version = (release.findtext("version") or "").strip()
        if not version:
            continue
        if (release.findtext("status") or "published").strip() != "published":
            continue
        # Branch membership is a prefix test against the feed's own branch
        # strings, which is why they carry a trailing dot: "4.3." must not
        # swallow "4.30.x".
        if not version.startswith(branch):
            continue
        if not channel_allows(version, channel):
            continue
        tags.append((version, (release.findtext("date") or "").strip()))
    return tags


def resolve_current_version(xml_text: str, channel: str = "stable") -> dict:
    """Resolve the current version for one project from release-history XML.

    channel: "stable" considers only stable tags.
             "alpha" also considers alpha/beta/rc tags.
    Bare -dev snapshots are NEVER returned as a resolved version, in either channel.

    Returns:
        {"version": str|None, "branch": str|None, "date": str|None, "error": str|None}

    The endpoint returns the project's full release history and MUST NOT be
    globally date-sorted. Releases are grouped by the `<supported_branches>`
    prefixes; the highest supported branch that actually carries a tag in this
    channel is taken as current, and the newest tag on THAT branch is returned.
    ECA tagged 2.1.22 a day after 3.1.5 on an older maintenance line; Search API
    Solr's 4.3.14 postdates 4.4.0 the same way. Both are right only under
    branch-aware resolution, and there is deliberately no date-sort fallback in
    any code path here.

    "Highest branch carrying a tag in this channel" rather than simply "highest
    supported branch": drupal.org lists a branch as supported from the moment it
    is opened, before it has been released. AI supports 1.3.,1.4.,1.5.,2.0. where
    2.0. has no releases at all and 1.5. has only an rc, so the current stable is
    1.4.6 on 1.4. Better Exposed Filters supports 6.0.,7.1.,8.0. where 8.0. is a
    lone alpha, so the current stable is 7.1.3 on 7.1.

    That fallback is why the alpha-exception test is branch-scoped rather than
    project-scoped: Group's alpha exception covers the 4.0.x line, and 3.3.5
    existing on the older 3.3. line does not retire it. See
    newest_stable_on_branch().

    `branch` is the raw prefix as it appears in the feed, e.g. "3.1." or "8.x-1.".
    `date` is the release date as YYYY-MM-DD (UTC), or None when the feed omits it.
    `version` is None with `error` set when the feed could not be read at all; it
    is None with `error` None when the feed parsed fine but no supported branch
    carries a tag in this channel — UI Suite DaisyUI has no stable anywhere, and
    the caller decides whether that is reportable.
    """
    blank = {"version": None, "branch": None, "date": None, "error": None}

    if channel not in ("stable", "alpha"):
        return {**blank, "error": f"unknown channel {channel!r} (expected 'stable' or 'alpha')"}

    root, branches, error = _parse_feed(xml_text)
    if error:
        return {**blank, "error": error}

    for branch in branches:
        candidates = _tags_on_branch(root, branch, channel)
        if not candidates:
            continue
        best_version, best_date = max(candidates, key=lambda item: version_sort_key(item[0]))
        iso_date = None
        if best_date.isdigit():
            iso_date = datetime.fromtimestamp(int(best_date), tz=timezone.utc).date().isoformat()
        return {"version": best_version, "branch": branch, "date": iso_date, "error": None}

    # Parsed fine, nothing to return. A None version ALWAYS carries an error
    # saying why: an audit tool that returns a silent None invites the caller to
    # treat it as "nothing to report", which is the quiet-skip failure this
    # checker exists to prevent. `branch` names the highest branch looked at.
    return {
        **blank,
        "branch": branches[0],
        "error": f"no {channel} tag on any supported branch (highest is {branches[0]})",
    }


def newest_stable_on_branch(xml_text: str, branch: str) -> str | None:
    """The newest stable tag on one branch, or None if it has none.

    This, not a project-wide stable lookup, is the test that retires an alpha
    exception. The exception is recorded against one line — Group's 4.0.x — and
    expires when THAT line gets a stable, not when an older maintenance line
    happens to have one. Group has 3.3.5 sitting on 3.3.; that must not be read
    as "a stable now exists" for a guide tracking 4.0.x.
    """
    root, _, error = _parse_feed(xml_text)
    if error or not branch:
        return None
    tags = _tags_on_branch(root, branch, "stable")
    if not tags:
        return None
    return max(tags, key=lambda item: version_sort_key(item[0]))[0]


# --------------------------------------------------------------------------
# Fetching
# --------------------------------------------------------------------------


def fetch_release_history(project: str) -> tuple[str | None, str | None]:
    """Return (xml_text, error). Exactly one of the two is None."""
    url = RELEASE_HISTORY_URL.format(project=project)
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=FETCH_TIMEOUT) as response:
            return response.read().decode("utf-8", errors="replace"), None
    except urllib.error.HTTPError as exc:
        return None, f"HTTP {exc.code} from {url}"
    except urllib.error.URLError as exc:
        return None, f"network error fetching {url}: {exc.reason}"
    except Exception as exc:  # noqa: BLE001 — an audit tool must name the failure, not die on it
        return None, f"unexpected error fetching {url}: {exc}"


def fetch_all(projects: list[str]) -> dict[str, tuple[str | None, str | None]]:
    if not projects:
        return {}
    with ThreadPoolExecutor(max_workers=FETCH_WORKERS) as pool:
        results = pool.map(fetch_release_history, projects)
        return dict(zip(projects, results))


# --------------------------------------------------------------------------
# Local reads
# --------------------------------------------------------------------------


def split_frontmatter(text: str) -> str:
    """Return the frontmatter YAML block, or '' when the file has none."""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[3:end]
    return ""


def as_date(value) -> date | None:
    """Coerce a YAML date/datetime/ISO string to a date."""
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return date.fromisoformat(value.strip())
        except ValueError:
            return None
    return None


def load_core_baseline() -> dict:
    if not GUIDES_YML.is_file():
        return {}
    try:
        data = yaml.safe_load(GUIDES_YML.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return {}
    return data.get("core") or {}


def load_partitioned_dates() -> dict[str, date | None]:
    if not MANIFEST.is_file():
        return {}
    try:
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    return {topic: as_date(entry.get("partitioned")) for topic, entry in data.items()}


def is_category_dir(directory: Path) -> bool:
    """Is this directory a navigation landing page rather than a topic?

    Classified by what the directory HOLDS, not by how deep it sits. A category
    holds topic subdirectories and no guides of its own — docs/drupal/,
    docs/testing/, docs/ itself. A topic holds guide .md files beside its
    index.md.

    Path depth is the wrong test and has already dropped a real topic. Every
    category happens to sit one segment below docs/, so "depth < 2 is a
    category" looks equivalent — but docs/emdash/ sits at depth 1 while holding
    sibling guides, no subdirectories and a real `tracks` declaration. Under the
    depth rule it appeared in no section of the report at all, not even "could
    not check", which is the silent skip this checker exists to prevent.
    """
    has_subdirs = False
    for child in directory.iterdir():
        if child.is_dir():
            has_subdirs = True
        elif child.is_file() and child.suffix == ".md" and child.name != "index.md":
            return False
    return has_subdirs


def discover_topics() -> list[dict]:
    """Every topic in docs/, whether or not it has declared anything.

    A topic is any directory with an index.md that is not a category landing
    page (see is_category_dir) — docs/drupal/eca/,
    docs/testing/visual-regression/playwright/, docs/emdash/. docs/index.md is
    the site root and is always skipped.
    """
    topics = []
    for index_path in sorted(DOCS_DIR.rglob("index.md")):
        directory = index_path.parent
        rel_dir = directory.relative_to(DOCS_DIR)
        if not rel_dir.parts:  # docs/index.md — the site root
            continue
        if is_category_dir(directory):
            continue
        slug = rel_dir.as_posix()
        text = index_path.read_text(encoding="utf-8")
        fm_yaml = split_frontmatter(text)
        meta = {}
        fm_error = None
        if fm_yaml.strip():
            try:
                meta = yaml.safe_load(fm_yaml) or {}
            except yaml.YAMLError as exc:
                fm_error = f"frontmatter YAML error: {exc}"
        topics.append(
            {
                "slug": slug,
                "path": index_path,
                "meta": meta if isinstance(meta, dict) else {},
                "fm_error": fm_error,
                "has_sources": (index_path.parent / "sources-maintenance.md").is_file(),
            }
        )
    return topics


# --------------------------------------------------------------------------
# Per-file core assertions
#
# `drupal_version` stays in every guide file's frontmatter, but it stops being
# hand-maintained: it is now an assertion checked against the single core claim
# in guides.yml. Nothing compared those 350 copies before, which is how
# js-development ended up with twenty-one files saying 10.x/11.x beside one
# saying 10.3+, and ui-patterns settled on a 10.3 floor three branches after
# 10.3 left support.
# --------------------------------------------------------------------------

# 11.x / 10.3 / 10.3+ / 11 — the core versions named inside a free-text claim
# such as "10.3+ / 11". Anything not shaped like a core version is ignored;
# the field is prose, not a parsed field, and always has been.
CORE_TOKEN_RE = re.compile(r"\b(\d+)(?:\.(\d+|x))?\b")


def parse_supported_branches(branches) -> tuple[set[tuple[int, int]], set[int]]:
    """Turn guides.yml `core.supported_branches` into lookup sets.

    Returns (exact major.minor pairs, majors carrying at least one branch).
    """
    pairs: set[tuple[int, int]] = set()
    majors: set[int] = set()
    for raw in branches or []:
        parts = str(raw).strip().rstrip(".").split(".")
        if not parts or not parts[0].isdigit():
            continue
        major = int(parts[0])
        majors.add(major)
        if len(parts) > 1 and parts[1].isdigit():
            pairs.add((major, int(parts[1])))
    return pairs, majors


def check_core_assertion(value: str, pairs, majors, baseline_major) -> list[str]:
    """Reasons this one `drupal_version` claim is wrong, or [] if it is fine.

    A bare major or an `N.x` wildcard is a branch-line claim and is accepted as
    long as that line is supported: "11.x" is not required to name 11.4. A claim
    naming an exact minor must name a branch that is actually still supported.
    """
    text = str(value or "").strip()
    if not text:
        return []  # states nothing; handled by the divergence check, not here
    reasons = []
    named_pairs = []
    named_majors = set()
    for major_text, minor_text in CORE_TOKEN_RE.findall(text):
        major = int(major_text)
        named_majors.add(major)
        if minor_text and minor_text != "x":
            named_pairs.append((major, int(minor_text)))
    if not named_majors:
        return []
    stale = [f"{a}.{b}" for a, b in named_pairs if (a, b) not in pairs]
    if stale:
        supported = ", ".join(f"{a}.{b}" for a, b in sorted(pairs))
        reasons.append(
            f"names core {', '.join(stale)}, outside the supported branches ({supported})"
        )
    if baseline_major is not None and baseline_major not in named_majors:
        reasons.append(f"names no version on the {baseline_major}.x baseline line")
    return reasons


def find_unparseable_frontmatter() -> list[dict]:
    """Every docs/**/*.md file whose frontmatter block fails to parse as YAML.

    Walks the same tree check_core_assertions() already walks for
    `drupal_version`, so this extra pass is cheap. A file that lands here is
    invisible to every consumer that reads frontmatter: the topic index, the
    navigator, and check_core_assertions() itself, which has always silently
    `continue`d past a parse error rather than surfacing it. That silent skip
    is the exact failure this checker exists to prevent, so every file that
    fails here must be named in the report, not folded into a count or
    dropped from one -- discovering it by accident is the failure mode.
    """
    failures = []
    for path in sorted(DOCS_DIR.rglob("*.md")):
        fm_yaml = split_frontmatter(path.read_text(encoding="utf-8"))
        if not fm_yaml.strip():
            continue
        try:
            yaml.safe_load(fm_yaml)
        except yaml.YAMLError as exc:
            failures.append(
                {
                    "path": path.relative_to(PROJECT_ROOT).as_posix(),
                    "error": str(exc),
                }
            )
    return failures


def check_core_assertions(core: dict) -> list[dict]:
    """Validate every guide file's `drupal_version` against the guides.yml core.

    Reported per topic with a file count. Three hundred and fifty identical
    lines is not a report, and the fact under audit is per topic anyway: the
    failure being looked for is one topic's copies of a single fact disagreeing
    with each other or with the baseline.
    """
    pairs, majors = parse_supported_branches(core.get("supported_branches"))
    if not pairs and not majors:
        return [
            {
                "topic": "guides.yml",
                "files": 0,
                "values": [],
                "reasons": [
                    "core.supported_branches is missing or unreadable, so no per-file "
                    "`drupal_version` could be validated"
                ],
            }
        ]

    baseline_parts = str(core.get("baseline") or "").strip().split(".")
    baseline_major = int(baseline_parts[0]) if baseline_parts[0].isdigit() else None

    by_topic: dict[str, dict[str, int]] = {}
    for path in sorted(DOCS_DIR.rglob("*.md")):
        fm_yaml = split_frontmatter(path.read_text(encoding="utf-8"))
        if not fm_yaml.strip():
            continue
        try:
            meta = yaml.safe_load(fm_yaml) or {}
        except yaml.YAMLError:
            # Reported by find_unparseable_frontmatter(), not here -- this
            # loop only has an opinion about drupal_version, and a file that
            # cannot be parsed states no drupal_version as far as this pass
            # is concerned. It is never silently dropped: every file skipped
            # on this line is named in the "Unparseable frontmatter" section.
            continue
        if not isinstance(meta, dict) or "drupal_version" not in meta:
            continue
        slug = path.parent.relative_to(DOCS_DIR).as_posix() or "."
        value = str(meta["drupal_version"] or "").strip()
        by_topic.setdefault(slug, {})
        by_topic[slug][value] = by_topic[slug].get(value, 0) + 1

    findings = []
    for slug, counts in sorted(by_topic.items()):
        reasons = []
        for value in sorted(counts):
            for reason in check_core_assertion(value, pairs, majors, baseline_major):
                reasons.append(f"{value or '(blank)'}: {reason}")
        # Copies of one fact that disagree with each other. A topic where every
        # file states the same blank is not this failure — nobody claimed
        # anything. A topic where one file diverges from twenty-one is.
        if len(counts) > 1:
            listed = ", ".join(f"{v or '(blank)'} x{counts[v]}" for v in sorted(counts))
            reasons.append(f"the topic states {len(counts)} different values for one fact: {listed}")
        if reasons:
            findings.append(
                {
                    "topic": slug,
                    "files": sum(counts.values()),
                    "values": [{"value": v, "files": counts[v]} for v in sorted(counts)],
                    "reasons": reasons,
                }
            )
    return findings


# --------------------------------------------------------------------------
# Comparison
# --------------------------------------------------------------------------


def compare(declared: str, current: str, branch_only: bool = False) -> tuple[str, str]:
    """Classify declared-vs-current. Returns (verdict, human note).

    verdict is one of: current, major, minor, patch, prerelease, ahead, unknown.
    A new major is separated from a patch bump because they are different sizes
    of work, per the convention's output categories.

    `branch_only` suppresses the unstated-patch-level rule, for a declaration
    that is deliberately a branch claim rather than a tag — guides.yml states
    core as "11.4", which should not read as drift against 11.4.5.
    """
    d = parse_version(declared)
    c = parse_version(current)
    if d is None or c is None:
        return "unknown", f"cannot compare {declared!r} against {current!r}"

    d_nums, d_rank, d_pre, d_dev = d
    c_nums, c_rank, c_pre, _ = c

    # In the legacy 8.x-N.M scheme, N is the major and M is the only other
    # level there is, so a M bump is a patch-sized move, not a minor one.
    legacy = bool(LEGACY_BRANCH_RE.match(str(declared).strip()))
    level_for = {0: "major"} if legacy else {0: "major", 1: "minor"}
    for i in range(max(len(d_nums), len(c_nums))):
        left = d_nums[i] if i < len(d_nums) else None
        right = c_nums[i] if i < len(c_nums) else 0
        if left is None:  # wildcard, or the declaration simply stops here
            continue
        if left == right:
            continue
        level = level_for.get(i, "patch")
        if left > right:
            return "ahead", f"declared {declared} is ahead of the current tag {current}"
        return level, f"{declared} -> {current}"

    # A declaration pinning an untagged dev branch is drift by policy, whatever
    # the numbers say: untagged development branches are not documented.
    if d_dev:
        return "patch", f"{declared} pins a dev branch; tagged release {current} exists"

    if (d_rank, d_pre) != (c_rank, c_pre):
        if (d_rank, d_pre) > (c_rank, c_pre):
            return "ahead", f"declared {declared} is ahead of the current tag {current}"
        return "prerelease", f"{declared} -> {current}"

    # Numerically equal as far as the declaration goes. If the current tag
    # states a level the declaration left out and it is non-zero, that is drift:
    # ECA's guide says 3.1 while the branch is on 3.1.5.
    if not branch_only and len(d_nums) < len(c_nums) and any(n for n in c_nums[len(d_nums):] if n):
        return "patch", f"{declared} states no patch level; current tag is {current}"

    return "current", f"{declared} matches {current}"


# --------------------------------------------------------------------------
# The check
# --------------------------------------------------------------------------


def run_check(today: date, unverified_days: int) -> dict:
    core = load_core_baseline()
    partitioned = load_partitioned_dates()
    topics = discover_topics()

    drift: list[dict] = []
    unjustified: list[dict] = []
    unverified: list[dict] = []
    undeclared: list[dict] = []
    unchecked: list[dict] = []
    ok: list[dict] = []

    # Which projects need fetching. Core is always fetched: guides.yml states a
    # baseline whether or not any topic declares `project: drupal`.
    wanted: set[str] = {"drupal"}
    declarations: list[dict] = []

    for topic in topics:
        slug = topic["slug"]
        meta = topic["meta"]

        if not topic["has_sources"]:
            undeclared.append({"what": slug, "why": "no sources-maintenance.md"})

        # Unreadable frontmatter is a could-not-check, and ONLY that. Falling
        # through would also report the topic as declaring nothing, which the
        # checker cannot know — the block may be there and simply unparseable.
        # Reporting both states a conclusion the evidence does not support.
        if topic["fm_error"]:
            unchecked.append({"what": slug, "why": topic["fm_error"]})
            continue

        if "tracks" not in meta:
            undeclared.append({"what": slug, "why": "no `tracks` key in index.md frontmatter"})
            hint = partitioned.get(slug)
            if hint:
                undeclared[-1]["why"] += f" (partitioned {hint.isoformat()}, never declared since)"
            continue

        tracks = meta.get("tracks")
        if tracks is None or tracks == []:
            # `tracks: []` is COMPLETE, not a gap. Someone decided this topic
            # tracks nothing — SOLID, TDD, DRY and the rest of the methodology
            # guides. Treating it as undeclared would make the next audit
            # re-derive what this one already worked out.
            ok.append({"what": slug, "why": "declares `tracks: []` — tracks nothing by decision"})
            continue

        if not isinstance(tracks, list):
            unchecked.append({"what": slug, "why": f"`tracks` must be a list, found {type(tracks).__name__}"})
            continue

        for entry in tracks:
            if not isinstance(entry, dict):
                unchecked.append({"what": slug, "why": f"malformed track entry: {entry!r}"})
                continue
            project = entry.get("project")
            if not project:
                unchecked.append({"what": slug, "why": f"track entry states no `project`: {entry!r}"})
                continue
            # `project` is a drupal.org machine name and this checker only knows
            # updates.drupal.org. A track may declare `registry:` for something
            # else (npm, github); those are named as unchecked rather than
            # guessed at, because drupal.org has projects whose machine names
            # collide with well-known packages — `tailwindcss` there is the
            # Tailwind CSS Starter Kit theme, `bootstrap` is the Bootstrap
            # theme, `react` is a module by corbacho. Fetching those and
            # reporting the result as the package's version is a confidently
            # wrong answer, which is worse than an admitted gap.
            registry = str(entry.get("registry") or "drupal").strip().lower()
            if registry != "drupal":
                unchecked.append(
                    {
                        "what": f"{slug} -> {project}",
                        "why": f"registry {registry!r} is outside updates.drupal.org; "
                        "this checker cannot resolve it",
                    }
                )
                continue
            wanted.add(str(project))
            declarations.append({"topic": slug, "entry": entry})

    fetched = fetch_all(sorted(wanted))

    # --- core baseline -----------------------------------------------------
    core_xml, core_error = fetched.get("drupal", (None, "core release history was not fetched"))
    core_resolved = None
    if core_error:
        unchecked.append({"what": "drupal core (guides.yml baseline)", "why": core_error})
    else:
        core_resolved = resolve_current_version(core_xml, "stable")
        if core_resolved["error"]:
            unchecked.append({"what": "drupal core (guides.yml baseline)", "why": core_resolved["error"]})
        elif not core.get("baseline"):
            unchecked.append(
                {
                    "what": "drupal core (guides.yml baseline)",
                    "why": "guides.yml states no core.baseline to compare against",
                }
            )
        else:
            # Two separate claims live in guides.yml. `baseline` is a branch
            # claim ("11.4") and must not read as drift against 11.4.5, so it is
            # compared branch-only. `latest_stable`, when present, is a full tag
            # claim and is compared at full precision.
            claims = [("core.baseline", str(core["baseline"]), True)]
            if core.get("latest_stable"):
                claims.append(("core.latest_stable", str(core["latest_stable"]), False))
            for claim_name, declared, branch_only in claims:
                verdict, note = compare(declared, core_resolved["version"], branch_only=branch_only)
                row = {
                    "topic": f"guides.yml {claim_name}",
                    "project": "drupal",
                    "declared": declared,
                    "verdict": verdict,
                    "note": note,
                    "branch": core_resolved["branch"],
                    "current": core_resolved["version"],
                    "date": core_resolved["date"],
                }
                if verdict == "unknown":
                    unchecked.append({"what": f"drupal core ({claim_name})", "why": note})
                elif verdict == "current":
                    ok.append({"what": f"guides.yml {claim_name}", "why": note})
                else:
                    drift.append(row)

    # Verified-age is a purely LOCAL question — has a human read this recently —
    # so it is evaluated outside the fetch branch above. Behind it, a week when
    # updates.drupal.org is unreachable would empty the Unverified section and
    # read as "everything has been read recently".
    core_verified = as_date(core.get("verified"))
    if core_verified and (today - core_verified).days > unverified_days:
        unverified.append(
            {
                "topic": "guides.yml core baseline",
                "project": "drupal",
                "verified": core_verified.isoformat(),
                "age": (today - core_verified).days,
            }
        )

    # --- per-topic declarations -------------------------------------------
    for declaration in declarations:
        slug = declaration["topic"]
        entry = declaration["entry"]
        project = str(entry.get("project"))
        channel = str(entry.get("channel") or "stable").strip().lower()
        label = f"{slug} -> {project}"

        # FIRST, and never behind a `continue`. Whether anyone has read this
        # topic recently is a local fact about the repo; it does not depend on
        # updates.drupal.org answering. Evaluated further down, a flaky fetch
        # would silently empty the Unverified section — the report would say
        # every declaration had been read within the threshold when in truth
        # none of them could be reached.
        verified = as_date(entry.get("verified"))
        if verified is None:
            unchecked.append({"what": label, "why": "track states no readable `verified` date"})
        elif (today - verified).days > unverified_days:
            unverified.append(
                {
                    "topic": slug,
                    "project": project,
                    "verified": verified.isoformat(),
                    "age": (today - verified).days,
                }
            )

        if channel not in ("stable", "alpha"):
            unchecked.append({"what": label, "why": f"unknown channel {channel!r} (expected stable or alpha)"})
            continue
        if channel == "alpha" and not entry.get("reason"):
            unchecked.append({"what": label, "why": "declares `channel: alpha` with no `reason`"})

        xml_text, fetch_error = fetched.get(project, (None, f"{project} was not fetched"))
        if fetch_error:
            unchecked.append({"what": label, "why": fetch_error})
            continue

        resolved = resolve_current_version(xml_text, channel)
        if resolved["error"]:
            unchecked.append({"what": label, "why": resolved["error"]})
            continue

        # An alpha declaration is an exception with an expiry date: it stops
        # being justified the day a stable tag lands on the SAME branch. Scoped
        # to the branch on purpose — Group's exception covers 4.0.x, and 3.3.5
        # sitting on the older 3.3. line does not retire it.
        if channel == "alpha":
            newest = newest_stable_on_branch(xml_text, resolved["branch"])
            if newest:
                unjustified.append(
                    {
                        "topic": slug,
                        "project": project,
                        "reason": entry.get("reason") or "(none given)",
                        "stable": newest,
                        "branch": resolved["branch"],
                    }
                )

        declared = entry.get("declared")
        # A core topic states no `declared` and inherits the repo baseline. That
        # baseline is a branch claim, so it is compared branch-only: otherwise
        # every one of the twenty-odd core topics repeats the single fact that
        # 11.4 is currently on 11.4.5, which is the duplication this convention
        # exists to remove. Core's patch level is reported once, on the
        # guides.yml row.
        inherited_core = False
        if declared is None:
            if project == "drupal":
                declared = core.get("baseline")
                inherited_core = declared is not None
            if declared is None:
                # NOT a could-not-check. The upstream side resolved fine; what
                # is missing is a claim in the guide, and a documentation gap is
                # precisely what this report exists to surface. "Could not
                # check" is reserved for the case where UPSTREAM could not be
                # determined. Carried as its own verdict so it never reads as an
                # ordinary version-to-version drift row.
                drift.append(
                    {
                        "topic": slug,
                        "project": project,
                        "channel": channel,
                        "declared": None,
                        "current": resolved["version"],
                        "branch": resolved["branch"],
                        "date": resolved["date"],
                        "verdict": "unstated",
                        "note": f"guide states no version; upstream is at {resolved['version']}",
                    }
                )
                continue

        verdict, note = compare(str(declared), resolved["version"], branch_only=inherited_core)
        row = {
            "topic": slug,
            "project": project,
            "channel": channel,
            "declared": str(declared),
            "current": resolved["version"],
            "branch": resolved["branch"],
            "date": resolved["date"],
            "verdict": verdict,
            "note": note,
        }
        if verdict == "unknown":
            unchecked.append({"what": label, "why": note})
        elif verdict == "current":
            ok.append({"what": label, "why": note})
        else:
            drift.append(row)

    return {
        "today": today,
        "unverified_days": unverified_days,
        "topics": len(topics),
        "projects_fetched": sorted(wanted),
        "frontmatter_errors": find_unparseable_frontmatter(),
        "core_assertions": check_core_assertions(core),
        # `unstated` is a documentation gap, not a version behind its tag. It was
        # carried in `drift` and so inflated the drift count, which meant the
        # number could never reach zero however current the catalog was. Split
        # here so "Drift (0)" is a claim that can actually come true, and the
        # gap stays visible in its own section.
        "drift": [r for r in drift if r["verdict"] != "unstated"],
        "unstated": [r for r in drift if r["verdict"] == "unstated"],
        "unjustified": unjustified,
        "unverified": unverified,
        "undeclared": undeclared,
        "unchecked": unchecked,
        "ok": ok,
    }


# --------------------------------------------------------------------------
# Reporting
# --------------------------------------------------------------------------

DRIFT_ORDER = {"major": 0, "minor": 1, "patch": 2, "prerelease": 3, "ahead": 4, "unstated": 5}
DRIFT_LABEL = {
    "major": "new major",
    "minor": "minor bump",
    "patch": "patch bump",
    "prerelease": "prerelease bump",
    "ahead": "declared ahead of upstream",
    # Sorted last so these cluster together: the work is writing a version into
    # a guide that has never had one, not bumping a number.
    "unstated": "no version stated in the guide",
}


def sorted_drift(rows: list[dict]) -> list[dict]:
    return sorted(rows, key=lambda r: (DRIFT_ORDER.get(r["verdict"], 9), r["topic"]))


def render_text(result: dict) -> str:
    out: list[str] = []
    out.append("Guide staleness report")
    out.append(f"Run {result['today'].isoformat()} against updates.drupal.org, branch-aware.")
    out.append(
        f"{result['topics']} topics scanned, "
        f"{len(result['projects_fetched'])} project(s) fetched, "
        f"unverified threshold {result['unverified_days']} days."
    )

    fm_errors = sorted(result["frontmatter_errors"], key=lambda r: r["path"])
    out.append("")
    out.append(f"Unparseable frontmatter ({len(fm_errors)})")
    if not fm_errors:
        out.append("  every guide file's frontmatter parses.")
    for row in fm_errors:
        out.append(f"  {row['path']}: {row['error']}")

    drift = sorted_drift(result["drift"])
    out.append("")
    out.append(f"Drift ({len(drift)})")
    if not drift:
        out.append("  nothing behind its current tag.")
    for row in drift:
        out.append(
            f"  [{DRIFT_LABEL.get(row['verdict'], row['verdict'])}] {row['topic']} "
            f"({row['project']}): {row['note']}"
        )
        out.append(f"      current branch {row['branch']}, tagged {row['date'] or 'date unknown'}")

    unstated = sorted(result.get("unstated", []), key=lambda r: r["topic"])
    out.append("")
    out.append(f"No version stated ({len(unstated)})")
    if not unstated:
        out.append("  every tracked project has a version in its guide.")
    for row in unstated:
        out.append(
            f"  {row['topic']} ({row['project']}): upstream is at {row['current']}; "
            "the guide states no version"
        )
        out.append(f"      current branch {row['branch']}, tagged {row['date'] or 'date unknown'}")

    out.append("")
    out.append(f"Unjustified exception ({len(result['unjustified'])})")
    if not result["unjustified"]:
        out.append("  every alpha declaration still lacks a stable release.")
    for row in sorted(result["unjustified"], key=lambda r: r["topic"]):
        out.append(
            f"  {row['topic']} ({row['project']}) declares alpha — "
            f"stable {row['stable']} now exists on branch {row['branch']}"
        )
        out.append(f"      recorded reason: {row['reason']}")

    unverified = sorted(result["unverified"], key=lambda r: -r["age"])
    out.append("")
    out.append(f"Unverified ({len(unverified)})")
    if not unverified:
        out.append("  every declaration has been read within the threshold.")
    for row in unverified:
        out.append(
            f"  {row['topic']} ({row['project']}): last verified {row['verified']}, "
            f"{row['age']} days ago"
        )

    undeclared = sorted(result["undeclared"], key=lambda r: (r["what"], r["why"]))
    out.append("")
    out.append(f"Undeclared ({len(undeclared)})")
    if not undeclared:
        out.append("  every topic declares what it tracks and carries a sources file.")
    for row in undeclared:
        out.append(f"  {row['what']}: {row['why']}")

    assertions = result["core_assertions"]
    out.append("")
    out.append(f"Core version assertions ({len(assertions)})")
    if not assertions:
        out.append("  every file's `drupal_version` agrees with the guides.yml core baseline.")
    for row in assertions:
        out.append(f"  {row['topic']} ({row['files']} file(s) state `drupal_version`)")
        for reason in row["reasons"]:
            out.append(f"      {reason}")

    unchecked = sorted(result["unchecked"], key=lambda r: (r["what"], r["why"]))
    out.append("")
    out.append(f"Could not check ({len(unchecked)})")
    if not unchecked:
        out.append("  nothing was skipped.")
    for row in unchecked:
        out.append(f"  {row['what']}: {row['why']}")

    out.append("")
    out.append(
        f"Current: {len(result['ok'])} declaration(s) match their upstream tag "
        "or deliberately track nothing."
    )
    return "\n".join(out)


def render_markdown(result: dict) -> str:
    out: list[str] = []
    out.append("# Guide staleness report")
    out.append("")
    out.append(
        f"Run {result['today'].isoformat()} against `updates.drupal.org`, branch-aware. "
        f"{result['topics']} topics scanned, {len(result['projects_fetched'])} project(s) fetched, "
        f"unverified threshold {result['unverified_days']} days."
    )

    fm_errors = sorted(result["frontmatter_errors"], key=lambda r: r["path"])
    out.append("")
    out.append(f"## Unparseable frontmatter ({len(fm_errors)})")
    out.append("")
    if not fm_errors:
        out.append("Every guide file's frontmatter parses.")
    for row in fm_errors:
        out.append(f"- `{row['path']}` — {row['error']}")

    drift = sorted_drift(result["drift"])
    out.append("")
    out.append(f"## Drift ({len(drift)})")
    out.append("")
    if not drift:
        out.append("Nothing behind its current tag.")
    else:
        out.append("| Topic | Project | Size | Declared | Current | Branch | Tagged |")
        out.append("|---|---|---|---|---|---|---|")
        for row in drift:
            out.append(
                f"| {row['topic']} | {row['project']} | "
                f"{DRIFT_LABEL.get(row['verdict'], row['verdict'])} | "
                f"{row.get('declared') or 'none stated'} | {row['current']} | {row['branch']} | "
                f"{row['date'] or '—'} |"
            )

    out.append("")
    out.append(f"## Unjustified exception ({len(result['unjustified'])})")
    out.append("")
    if not result["unjustified"]:
        out.append("Every alpha declaration still lacks a stable release.")
    else:
        out.append("| Topic | Project | Recorded reason | Stable now available |")
        out.append("|---|---|---|---|")
        for row in sorted(result["unjustified"], key=lambda r: r["topic"]):
            out.append(
                f"| {row['topic']} | {row['project']} | {row['reason']} | "
                f"{row['stable']} (branch {row['branch']}) |"
            )

    unverified = sorted(result["unverified"], key=lambda r: -r["age"])
    out.append("")
    out.append(f"## Unverified ({len(unverified)})")
    out.append("")
    if not unverified:
        out.append("Every declaration has been read within the threshold.")
    else:
        out.append("| Topic | Project | Last verified | Days |")
        out.append("|---|---|---|---|")
        for row in unverified:
            out.append(f"| {row['topic']} | {row['project']} | {row['verified']} | {row['age']} |")

    undeclared = sorted(result["undeclared"], key=lambda r: (r["what"], r["why"]))
    out.append("")
    out.append(f"## Undeclared ({len(undeclared)})")
    out.append("")
    if not undeclared:
        out.append("Every topic declares what it tracks and carries a sources file.")
    for row in undeclared:
        out.append(f"- `{row['what']}` — {row['why']}")

    assertions = result["core_assertions"]
    out.append("")
    out.append(f"## Core version assertions ({len(assertions)})")
    out.append("")
    if not assertions:
        out.append("Every file's `drupal_version` agrees with the guides.yml core baseline.")
    else:
        out.append("| Topic | Files | Values | Problem |")
        out.append("|---|---|---|---|")
        for row in assertions:
            values = ", ".join(
                f"`{v['value'] or '(blank)'}` x{v['files']}" for v in row["values"]
            ) or "—"
            out.append(
                f"| {row['topic']} | {row['files']} | {values} | "
                f"{'; '.join(row['reasons'])} |"
            )

    unchecked = sorted(result["unchecked"], key=lambda r: (r["what"], r["why"]))
    out.append("")
    out.append(f"## Could not check ({len(unchecked)})")
    out.append("")
    if not unchecked:
        out.append("Nothing was skipped.")
    for row in unchecked:
        out.append(f"- `{row['what']}` — {row['why']}")

    out.append("")
    out.append(
        f"{len(result['ok'])} declaration(s) match their upstream tag or deliberately track nothing."
    )
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Report guide topics that have drifted behind the releases they document."
    )
    parser.add_argument(
        "--format",
        choices=("text", "markdown"),
        default="text",
        help="text for a terminal read (default); markdown to post into the tracking issue",
    )
    parser.add_argument(
        "--unverified-days",
        type=int,
        default=DEFAULT_UNVERIFIED_DAYS,
        help=f"age at which a `verified` date is stale (default {DEFAULT_UNVERIFIED_DAYS})",
    )
    parser.add_argument(
        "--today",
        default=None,
        help="override today's date (YYYY-MM-DD), for reproducible runs",
    )
    args = parser.parse_args(argv)

    today = as_date(args.today) if args.today else date.today()
    if today is None:
        # A usage error, not a finding. Printing to stderr and returning 0
        # produces no report and no failure signal — a scheduled job would post
        # nothing and look like it had passed, which is the whole run silently
        # skipped. parser.error exits 2, which a caller cannot miss. The
        # always-0 rule below covers drift, not a malformed invocation.
        parser.error(f"--today must be YYYY-MM-DD; got {args.today!r}")

    result = run_check(today, args.unverified_days)
    print(render_markdown(result) if args.format == "markdown" else render_text(result))

    # ALWAYS 0. Upstream tagging a release is not a defect in whatever pull
    # request happens to be open, and failing the build on it would stall
    # unrelated work every time any of twenty-five projects cuts a release.
    # The report is the product; a scheduled workflow reads it, not a gate.
    return 0


if __name__ == "__main__":
    sys.exit(main())

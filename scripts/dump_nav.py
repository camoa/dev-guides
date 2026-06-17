#!/usr/bin/env python3
"""Dump the fully-built MkDocs navigation (including plugin transforms such as
awesome-nav) as one line per nav node in nav order.

Output format (exactly as required by the migration gate):

    INDENT|TITLE|URL

where INDENT is two spaces per nesting level, TITLE is the nav title, and URL is
the page URL (empty for section nodes that have no page of their own).

Usage:
    python3 dump_nav.py [mkdocs.yml]
"""
from __future__ import annotations

import sys

from mkdocs.config import load_config
from mkdocs.structure.files import get_files
from mkdocs.structure.nav import get_navigation


def build_nav(config_file: str):
    cfg = load_config(config_file)
    # Run the same lifecycle hooks mkdocs build uses, so plugin-generated
    # navigation (awesome-nav replaces nav in on_nav) is reflected here.
    cfg.plugins.on_startup(command="build", dirty=False)
    files = get_files(cfg)
    files = cfg.plugins.on_files(files, config=cfg)
    nav = get_navigation(files, cfg)
    nav = cfg.plugins.on_nav(nav, config=cfg, files=files)
    return nav


def node_url(node) -> str:
    # Pages expose a url; sections/links may too.
    url = getattr(node, "url", None)
    if url:
        return url
    f = getattr(node, "file", None)
    if f is not None:
        return getattr(f, "url", "") or getattr(f, "src_uri", "")
    return ""


def walk(items, depth, out):
    for node in items:
        indent = "  " * depth
        title = node.title if node.title is not None else ""
        out.append(f"{indent}|{title}|{node_url(node)}")
        children = getattr(node, "children", None)
        if children:
            walk(children, depth + 1, out)


def main():
    config_file = sys.argv[1] if len(sys.argv) > 1 else "mkdocs.yml"
    nav = build_nav(config_file)
    out: list[str] = []
    walk(nav.items, 0, out)
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()

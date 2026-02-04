# mkdocs-nav-numbering-plugin

[![CI](https://github.com/matusdrobuliak66/mkdocs-nav-numbering-plugin/actions/workflows/ci.yml/badge.svg)](https://github.com/matusdrobuliak66/mkdocs-nav-numbering-plugin/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/mkdocs-nav-numbering-plugin.svg)](https://pypi.org/project/mkdocs-nav-numbering-plugin/)

MkDocs plugin that adds hierarchical numbering to navigation items and page headings.

## Features

- Number nav sections, pages, and links (optional)
- Number page headings based on nav position
- Configurable depth limits for nav and headings
- Configurable separator
- Exclude specific pages

## Installation

```bash
pip install mkdocs-nav-numbering-plugin
```

## Usage

```yaml
plugins:
  - nav-numbering:
      nav_depth: 4
      heading_depth: 5
      number_h1: true
      number_nav: true
      number_headings: true
      preserve_anchor_ids: false
      separator: "."
      exclude:
        - index.md

markdown_extensions:
  - attr_list  # Required when preserve_anchor_ids is true
```

## Options

- `enabled` (bool, default: true)
- `nav_depth` (int, default: 0) — 0 means unlimited
- `heading_depth` (int, default: 0) — 0 means unlimited
- `number_nav` (bool, default: true)
- `number_headings` (bool, default: true)
- `number_h1` (bool, default: true)
- `preserve_anchor_ids` (bool, default: false) — Preserve original heading anchor IDs without number prefixes (requires `attr_list`)
- `separator` (str, default: ".")
- `exclude` (list, default: [])

### `preserve_anchor_ids`

By default, MkDocs generates heading IDs from the final heading text. Since this plugin prepends numbering, your anchors can end up including the numbers.

Enable `preserve_anchor_ids: true` to add explicit `{#...}` IDs based on the original (un-numbered) heading text. Duplicate headings are automatically suffixed with `-1`, `-2`, etc.

```yaml
plugins:
  - nav-numbering:
      preserve_anchor_ids: true

markdown_extensions:
  - attr_list
```

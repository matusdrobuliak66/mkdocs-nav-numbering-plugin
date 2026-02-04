# mkdocs-nav-numbering-plugin

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
      separator: "."
      exclude:
        - index.md
```

## Options

- `enabled` (bool, default: true)
- `nav_depth` (int, default: 0) — 0 means unlimited
- `heading_depth` (int, default: 0) — 0 means unlimited
- `number_nav` (bool, default: true)
- `number_headings` (bool, default: true)
- `number_h1` (bool, default: true)
- `separator` (str, default: ".")
- `exclude` (list, default: [])

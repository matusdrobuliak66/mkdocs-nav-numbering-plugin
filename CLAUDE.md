# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A MkDocs plugin that adds hierarchical numbering to navigation items and page headings. The plugin processes navigation structure and markdown content to inject numbers at configurable depths.

## Key Commands

```bash
# Install in editable mode (required for development)
make install-dev

# Development workflow
make lint          # Run ruff linter
make format        # Format with ruff
make test          # Run pytest (note: test directory appears to be missing)
make serve         # Start MkDocs dev server (test the plugin on sample docs)
make build         # Build the documentation site

# Package management
make clean         # Remove build artifacts and caches
make help          # Show all available targets
```

## Architecture

### Core Plugin Structure

The plugin follows the standard MkDocs plugin pattern using two event hooks:

1. **`on_nav` hook** (NavNumberingPlugin.on_nav)
   - Processes the navigation tree structure
   - Walks recursively through Section, Page, and Link items
   - Assigns hierarchical numbers based on position
   - Stores page src_uri → number mapping in `self.page_numbers`
   - Respects `nav_depth` config to limit numbering depth
   - Handles exclusions via glob patterns

2. **`on_page_markdown` hook** (NavNumberingPlugin.on_page_markdown)
   - Processes page content after nav numbering
   - Modifies heading markdown (# through ######) using regex
   - Uses page number from `self.page_numbers` as base for heading numbers
   - Tracks separate counters for h2+ (sub-headings within a page)
   - Handles `preserve_anchor_ids` mode by generating {#slug} attributes
   - Detects existing {#custom-id} and preserves them

### Key Implementation Details

**slugify() function**: Generates URL-friendly heading IDs matching MkDocs' default toc behavior. Used for anchor ID generation when `preserve_anchor_ids` is enabled.

**Configuration**: Defined as `config_scheme` tuple in NavNumberingPlugin class. Key options:
- `enabled`, `nav_depth`, `heading_depth`, `number_nav`, `number_headings`, `number_h1`, `separator`, `exclude`, `preserve_anchor_ids`

**Numbering Scheme**:
- Navigation: Top-level sections get 1, 2, 3..., nested sections get 1.1, 1.2, 1.1.1, etc.
- Headings: First h1 gets the base page number (e.g., "3.1.2"), h2 gets "3.1.2.1", h3 gets "3.1.2.1.1", etc.

**Important Edge Cases**:
- Multiple h1s in one page: Resets sub-heading counters, both get base page number
- Existing {#...} attributes in markdown: Preserved when numbering is applied
- Already numbered headings (regex match on `^\d+(\.\d+)*\s+`): Skipped to avoid double-numbering
- Duplicate heading text: Gets suffix (-1, -2, etc.) in slugs when `preserve_anchor_ids` is enabled

## Testing

The Makefile references `pytest tests/` but there is no tests directory in the repo. If adding tests:
- Follow pytest conventions with `test_*.py` files
- Use `make test` or `pytest tests/ -v`
- Coverage available via `make test-cov`

## Configuration Location

- **Plugin registration**: `pyproject.toml` entry point at `mkdocs.plugins:nav-numbering`
- **Sample configuration**: `mkdocs.yml` (the plugin's own documentation site)
- **Configuration documentation**: `README.md` and `docs/guide/configuration.md`

## Dependencies

- **Runtime**: mkdocs >= 1.4
- **Development**: ruff (linting/formatting), pytest (testing)
- **Documentation**: Material theme for mkdocs

## Building and Publishing

The CI pipeline (`.github/workflows/ci.yml`) builds the package with Python 3.11 using `python -m build`. Publishing is handled by `.github/workflows/publish.yml`.

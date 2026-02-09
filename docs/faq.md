# FAQ

Frequently asked questions about the Nav Numbering plugin.

## General Questions

### How does numbering work with nested sections?

The plugin assigns hierarchical numbers based on the structure of your navigation tree. Top-level sections get numbers like `1`, `2`, `3`, while nested items get `1.1`, `1.2`, `1.1.1`, etc.

For example, with this navigation structure:

```yaml
nav:
  - Home: index.md
  - Getting Started:
      - Install: guide/install.md
      - Quick Start: guide/quick-start.md
  - User Guide:
      - Configuration: guide/configuration.md
```

The numbering would be:
- Home → `1`
- Getting Started → `2`
  - Install → `2.1`
  - Quick Start → `2.2`
- User Guide → `3`
  - Configuration → `3.1`

### What happens when I exclude pages from numbering?

Pages matching patterns in the `exclude` configuration are skipped during numbering:

```yaml
plugins:
  - nav-numbering:
      exclude:
        - index.md
        - faq.md
```

Excluded pages won't get numbers in the navigation or in their headings, but they won't affect the numbering sequence of other pages. The numbering continues as if the excluded pages don't exist.

### Can I disable numbering for specific pages?

Yes, use the `exclude` configuration option with page paths or patterns:

```yaml
plugins:
  - nav-numbering:
      exclude:
        - index.md
        - reference/*.md
```

This will exclude the home page and all pages in the `reference/` directory.

## Anchor IDs and Links

### What is `preserve_anchor_ids` and when should I use it?

By default, MkDocs generates anchor IDs from heading text. When numbering is added to headings (e.g., `## 1.2.1 Installation`), the default anchor becomes `#121-installation` instead of `#installation`.

Setting `preserve_anchor_ids: true` tells the plugin to explicitly generate `{#slug}` attributes based on the original heading text (without numbers), preserving the original anchor behavior:

```markdown
## 1.2.1 Installation {#installation}
```

This is essential if you have existing anchor links that you want to keep working.

### I migrated to this plugin and my anchor links broke. How do I fix them?

Enable `preserve_anchor_ids: true` in your plugin configuration:

```yaml
plugins:
  - nav-numbering:
      preserve_anchor_ids: true
```

This ensures that anchor IDs remain based on the heading text without numbers, so existing links like `#installation` continue to work even when the heading becomes "1.2.1 Installation".

### What happens with duplicate heading names on the same page?

When `preserve_anchor_ids` is enabled, the plugin detects duplicate slugs and automatically adds numeric suffixes (e.g., `#installation`, `#installation-1`, `#installation-2`) to ensure all anchors are unique.

## Configuration

### How do I limit numbering depth?

Use `nav_depth` to limit navigation numbering and `heading_depth` to limit heading numbering:

```yaml
plugins:
  - nav-numbering:
      nav_depth: 2        # Only number up to 2 levels in nav (1.1, but not 1.1.1)
      heading_depth: 3    # Only number headings up to depth 3
```

Setting either to `0` (the default) means unlimited depth.

### Can I change the separator from dots to something else?

Yes, use the `separator` option:

```yaml
plugins:
  - nav-numbering:
      separator: "-"      # Results in 1-1-1 instead of 1.1.1
```

### Can I number navigation but not headings (or vice versa)?

Yes, use the `number_nav` and `number_headings` options:

```yaml
plugins:
  - nav-numbering:
      number_nav: true        # Number navigation items
      number_headings: false  # Don't number headings in content
```

### Should I number the page title (h1)?

By default, the first h1 on each page (usually the page title) gets numbered with the base page number. If you want to skip numbering h1 headings:

```yaml
plugins:
  - nav-numbering:
      number_h1: false
```

## Troubleshooting

### My headings are getting double-numbered

The plugin checks if headings are already numbered (starting with a pattern like `1.2.3 `) and skips them to avoid double-numbering. If you're seeing double numbers, check:

1. You don't have hardcoded numbers in your markdown headings
2. You're not running the plugin multiple times in the build process
3. Your markdown files don't have the plugin's output already saved in them

### The plugin doesn't seem to be working

Check these common issues:

1. **Is the plugin installed?** Run `pip list | grep mkdocs-nav-numbering-plugin`
2. **Is it in your mkdocs.yml?** Check the `plugins:` section includes `nav-numbering`
3. **Is it enabled?** The plugin is enabled by default, but check you haven't set `enabled: false`
4. **Are you using `mkdocs serve` or `mkdocs build`?** The plugin runs during the build process

### Can I use this plugin with other MkDocs plugins?

Yes, the plugin is compatible with most MkDocs plugins. However, plugin order can matter:

```yaml
plugins:
  - search
  - nav-numbering      # Run before plugins that process final HTML
  - other-plugin
```

If you experience issues, try adjusting the plugin order in your configuration.

## Advanced Usage

### Can I customize the numbering style (e.g., Roman numerals)?

Not currently. The plugin uses sequential decimal numbers (1, 2, 3, etc.). If you need alternative numbering styles, you would need to fork the plugin and modify the numbering logic.

### Can I restart numbering at different sections?

No, the plugin creates a single hierarchical numbering scheme across the entire navigation tree. Each section continues the numbering from its parent level.

### What if I have custom heading IDs already in my markdown?

The plugin detects existing `{#custom-id}` attributes in your headings and preserves them:

```markdown
## Installation {#my-custom-anchor}
```

becomes:

```markdown
## 1.2.1 Installation {#my-custom-anchor}
```

The custom ID is preserved and the numbering is added to the heading text.

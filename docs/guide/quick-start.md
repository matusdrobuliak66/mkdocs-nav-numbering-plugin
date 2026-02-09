# Quick Start

Get up and running with the Nav Numbering plugin in 5 minutes.

## Step 1: Install

Install the plugin via pip:

```bash
pip install mkdocs-nav-numbering-plugin
```

## Step 2: Configure

Add the plugin to your `mkdocs.yml` file:

```yaml
site_name: My Documentation

theme:
  name: material

plugins:
  - search
  - nav-numbering:
      preserve_anchor_ids: true  # Recommended for existing docs

nav:
  - Home: index.md
  - Getting Started:
      - Installation: guide/install.md
      - Quick Start: guide/quick-start.md
  - User Guide:
      - Configuration: guide/config.md
      - Advanced Topics: guide/advanced.md
```

## Step 3: Preview

Start the development server:

```bash
mkdocs serve
```

Open http://127.0.0.1:8000 in your browser.

## What You'll See

### Before (without plugin)

**Navigation**:
```
Home
Getting Started
  Installation
  Quick Start
User Guide
  Configuration
  Advanced Topics
```

**Page heading**:
```markdown
## Installation
### Prerequisites
### Steps
```

### After (with plugin)

**Navigation**:
```
1 Home
2 Getting Started
  2.1 Installation
  2.2 Quick Start
3 User Guide
  3.1 Configuration
  3.2 Advanced Topics
```

**Page heading** (in `guide/install.md`):
```markdown
## 2.1.1 Installation {#installation}
### 2.1.1.1 Prerequisites {#prerequisites}
### 2.1.1.2 Steps {#steps}
```

## Understanding the Numbering

### Navigation Numbering

- Top-level items get sequential numbers: `1`, `2`, `3`
- Nested items extend the parent number: `2.1`, `2.2`, `2.1.1`
- The hierarchy follows your `nav:` structure in `mkdocs.yml`

### Heading Numbering

- The first `h1` (`#`) on each page gets the base page number from navigation
- `h2` (`##`) headings get sub-numbers: `2.1.1`, `2.1.2`
- `h3` (`###`) headings go deeper: `2.1.1.1`, `2.1.1.2`
- And so on for `h4`, `h5`, `h6`

### Anchor IDs

With `preserve_anchor_ids: true`, the plugin adds explicit `{#slug}` attributes to headings:

```markdown
## 2.1.1 Installation {#installation}
```

This means:
- ✅ The URL will be `/guide/install/#installation` (clean, without numbers)
- ✅ Existing anchor links keep working
- ✅ Heading numbering is purely visual

Without `preserve_anchor_ids`, the anchor would be `#211-installation` (includes numbers).

## Common Customizations

### Change the Separator

Use hyphens instead of dots:

```yaml
plugins:
  - nav-numbering:
      separator: "-"  # Results in 1-1-1 instead of 1.1.1
```

### Limit Numbering Depth

Only number two levels deep:

```yaml
plugins:
  - nav-numbering:
      nav_depth: 2        # Only number nav to level 2 (e.g., 1.1 but not 1.1.1)
      heading_depth: 3    # Only number headings to level 3
```

### Exclude Specific Pages

Don't number the home page or FAQ:

```yaml
plugins:
  - nav-numbering:
      exclude:
        - index.md
        - faq.md
```

### Number Navigation Only (Not Headings)

```yaml
plugins:
  - nav-numbering:
      number_nav: true        # Number navigation
      number_headings: false  # Don't number content headings
```

## Verify the Output

### 1. Check Navigation Numbers

Look at the left sidebar (or top tabs):
- Do navigation items show numbers?
- Are the numbers hierarchical (e.g., 1, 1.1, 1.2)?

### 2. Check Heading Numbers

Open any content page:
- Do headings show numbers?
- Are they correctly hierarchical?

### 3. Check Anchor Links

Click a heading to jump to it:
- Does the URL hash update?
- With `preserve_anchor_ids: true`, the hash should be clean (e.g., `#installation`)
- Without it, the hash includes numbers (e.g., `#211-installation`)

### 4. Test Existing Links

If you have existing anchor links like `[link](#installation)`:
- They should work if `preserve_anchor_ids: true`
- They might break if `preserve_anchor_ids: false`

## Build for Production

Once you're happy with the preview:

```bash
mkdocs build
```

This creates the `site/` directory with your numbered documentation ready to deploy.

## Next Steps

Now that you have the plugin working:

- **Customize**: See the [Configuration](configuration.md) guide for all options
- **Advanced usage**: Check out [Tips & Tricks](tips.md)
- **Troubleshooting**: Visit the [FAQ](../faq.md) for common issues
- **API reference**: For developers, see the [API documentation](../reference/api.md)

## Troubleshooting

### Numbers not appearing?

1. Check the plugin is in your `mkdocs.yml` `plugins:` section
2. Verify `enabled: true` (it's true by default)
3. Try a clean build: `rm -rf site/ && mkdocs build`

### Anchor links broken?

Enable `preserve_anchor_ids: true` in your configuration:

```yaml
plugins:
  - nav-numbering:
      preserve_anchor_ids: true
```

### Double numbering?

The plugin auto-detects already-numbered headings. If you see double numbers:
- Remove manual numbers from your markdown files
- The plugin will add them automatically

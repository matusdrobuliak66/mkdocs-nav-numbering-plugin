# Install

This guide walks you through installing the Nav Numbering plugin for MkDocs.

## Requirements

Before installing, ensure you have:

- **Python**: Version 3.8 or higher
- **MkDocs**: Version 1.4 or higher

You can check your versions:

```bash
python --version
mkdocs --version
```

## Installation

Install the plugin using pip:

```bash
pip install mkdocs-nav-numbering-plugin
```

For development or to install from source:

```bash
git clone https://github.com/matusdrobuliak66/mkdocs-nav-numbering-plugin.git
cd mkdocs-nav-numbering-plugin
pip install -e .
```

## Configuration

After installation, add the plugin to your `mkdocs.yml` configuration file:

```yaml
plugins:
  - search
  - nav-numbering
```

!!! note
    The order of plugins can matter. Generally, `nav-numbering` should come after `search` but before plugins that process final HTML output.

## Basic Configuration Example

Here's a minimal configuration to get started:

```yaml
site_name: My Documentation
theme:
  name: material

plugins:
  - search
  - nav-numbering:
      enabled: true
      preserve_anchor_ids: true

nav:
  - Home: index.md
  - Getting Started:
      - Installation: guide/install.md
      - Quick Start: guide/quick-start.md
  - User Guide:
      - Configuration: guide/config.md
```

With this configuration, your navigation and page headings will automatically get hierarchical numbers like `1`, `1.1`, `1.1.1`, etc.

## Verify Installation

To verify the plugin is working:

1. **Build your documentation**:
   ```bash
   mkdocs build
   ```

2. **Serve locally**:
   ```bash
   mkdocs serve
   ```

3. **Check the output**:
   - Open http://127.0.0.1:8000 in your browser
   - Navigation items should show numbers (e.g., "1 Home", "2 Getting Started")
   - Page headings should also be numbered

If you see numbers in your navigation and headings, the plugin is installed correctly!

## Next Steps

- Learn how to customize numbering in the [Configuration](configuration.md) guide
- Check out [Tips & Tricks](tips.md) for advanced usage
- Review the [Quick Start](quick-start.md) guide for a fast walkthrough

## Troubleshooting

### Plugin not found

If you get an error like "Plugin 'nav-numbering' not found":

1. Verify installation: `pip list | grep mkdocs-nav-numbering-plugin`
2. Ensure you're in the correct virtual environment
3. Try reinstalling: `pip install --upgrade mkdocs-nav-numbering-plugin`

### No numbering appears

If the plugin is installed but numbering doesn't appear:

1. Check that `enabled: true` in your configuration (it's true by default)
2. Verify the plugin is in your `plugins:` section in `mkdocs.yml`
3. Clear the build directory: `rm -rf site/` and rebuild
4. Check the MkDocs build output for errors

### Permission errors during installation

On some systems, you may need to use:

```bash
pip install --user mkdocs-nav-numbering-plugin
```

Or install in a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install mkdocs-nav-numbering-plugin
```

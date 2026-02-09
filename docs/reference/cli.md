# MkDocs Commands

Guide to using MkDocs commands with the Nav Numbering plugin.

!!! note
    The Nav Numbering plugin is a MkDocs build-time plugin and does not provide its own CLI commands. This page covers the standard MkDocs commands you'll use when working with the plugin.

## Core Commands

### `mkdocs serve`

Start the MkDocs development server with live reloading.

```bash
mkdocs serve
```

**What happens with the plugin**:
- Navigation items are numbered according to your configuration
- Page headings are numbered based on their position in the nav tree
- Changes to markdown files trigger automatic rebuilds
- The site is served at http://127.0.0.1:8000 by default

**Common options**:

```bash
mkdocs serve --dev-addr=0.0.0.0:8000  # Serve on all network interfaces
mkdocs serve --strict                  # Abort on warnings
mkdocs serve --clean                   # Clean the site directory before build
```

**Debugging tip**: Watch the console output for any warnings or errors from the plugin during the build process.

### `mkdocs build`

Build the documentation site to static HTML.

```bash
mkdocs build
```

**What happens with the plugin**:
1. `on_nav()` hook processes navigation and assigns numbers
2. `on_page_markdown()` hook processes each page's markdown
3. Numbered headings are converted to HTML
4. Anchor IDs are generated (with or without number prefixes)
5. Static files are written to the `site/` directory

**Common options**:

```bash
mkdocs build --clean        # Clean the site directory before build
mkdocs build --strict       # Treat warnings as errors
mkdocs build --site-dir docs  # Use custom output directory
```

**Output location**: By default, the built site is in the `site/` directory.

### `mkdocs new`

Create a new MkDocs project.

```bash
mkdocs new my-project
cd my-project
```

**After creating a new project**:

1. Install the plugin:
   ```bash
   pip install mkdocs-nav-numbering-plugin
   ```

2. Add to `mkdocs.yml`:
   ```yaml
   plugins:
     - search
     - nav-numbering
   ```

3. Test it:
   ```bash
   mkdocs serve
   ```

### `mkdocs gh-deploy`

Build and deploy your documentation to GitHub Pages.

```bash
mkdocs gh-deploy
```

**What happens with the plugin**:
- Builds the site with numbering applied
- Pushes the built site to the `gh-pages` branch
- Makes the numbered documentation available on GitHub Pages

**Common options**:

```bash
mkdocs gh-deploy --force     # Force push to gh-pages
mkdocs gh-deploy --clean     # Clean the site directory before build
```

!!! warning
    Ensure `preserve_anchor_ids: true` if you have existing anchor links, otherwise your deployed site will have broken internal links.

## Workflow Examples

### Development Workflow

```bash
# Edit documentation files
vim docs/guide/installation.md

# Preview with live reload
mkdocs serve

# Check the numbered output in browser
# (open http://127.0.0.1:8000)

# Build for production
mkdocs build

# Verify the output
ls -la site/
```

### Testing Plugin Configuration

```bash
# Test with different configurations
# Edit mkdocs.yml to change nav_depth, separator, etc.

# Clear the site directory to force a rebuild
rm -rf site/

# Rebuild with new configuration
mkdocs build

# Or use serve with --clean flag
mkdocs serve --clean
```

### Debugging Numbering Issues

If numbering isn't working as expected:

1. **Run a clean build**:
   ```bash
   rm -rf site/
   mkdocs build --strict
   ```

2. **Check for warnings**:
   ```bash
   mkdocs build 2>&1 | grep -i warning
   ```

3. **Verify plugin is loaded**:
   ```bash
   mkdocs build --verbose
   ```

4. **Inspect generated HTML**:
   ```bash
   # Build the site
   mkdocs build

   # Check a specific page
   cat site/guide/install/index.html | grep -A2 "<h2"
   ```

### Publishing Workflow

```bash
# Development
mkdocs serve

# Final checks
mkdocs build --strict --clean

# Deploy to GitHub Pages
mkdocs gh-deploy --clean

# Or deploy to custom server
rsync -avz site/ user@server:/var/www/docs/
```

## Configuration Validation

### Check Your Configuration

MkDocs validates your `mkdocs.yml` during build. To check for configuration errors:

```bash
mkdocs build --strict
```

**Common plugin configuration errors**:

```yaml
# ❌ Incorrect: separator must be a string
plugins:
  - nav-numbering:
      separator: 1

# ✅ Correct
plugins:
  - nav-numbering:
      separator: "."
```

```yaml
# ❌ Incorrect: nav_depth must be an integer
plugins:
  - nav-numbering:
      nav_depth: "unlimited"

# ✅ Correct
plugins:
  - nav-numbering:
      nav_depth: 0  # 0 means unlimited
```

## Environment Variables

### Set Custom Site Directory

```bash
# Build to a custom directory
mkdocs build --site-dir=/tmp/my-docs
```

### Development Mode

```bash
# Run with verbose output
mkdocs serve --verbose

# Run with strict warnings
mkdocs serve --strict
```

## Makefile Commands

If you're using the plugin's development setup, these Make targets are available:

```bash
# Install in development mode
make install-dev

# Run linting
make lint

# Format code
make format

# Serve documentation
make serve

# Build documentation
make build

# Clean build artifacts
make clean
```

**See available targets**:
```bash
make help
```

## Troubleshooting

### Numbering Not Appearing

```bash
# 1. Verify plugin is installed
pip list | grep mkdocs-nav-numbering-plugin

# 2. Check mkdocs.yml syntax
mkdocs build --strict

# 3. Clean build
rm -rf site/
mkdocs build
```

### Anchor Links Broken

```bash
# Enable preserve_anchor_ids in mkdocs.yml
# Then rebuild completely
rm -rf site/
mkdocs build --clean
```

### Plugin Not Loading

```bash
# Check Python environment
which python
which mkdocs

# Verify plugin is visible to MkDocs
python -c "from mkdocs_nav_numbering_plugin.nav_numbering import NavNumberingPlugin; print('Plugin loaded successfully')"
```

### Performance Issues

For large documentation sites:

```bash
# Use MkDocs' built-in caching
mkdocs serve

# For production builds
mkdocs build --clean
```

## Advanced Usage

### Custom Build Scripts

Create a `build.sh` script for complex workflows:

```bash
#!/bin/bash
set -e

# Clean previous build
rm -rf site/

# Build with numbering
mkdocs build --strict

# Post-process (if needed)
# ... custom processing ...

# Deploy
rsync -avz site/ user@server:/var/www/docs/
```

### CI/CD Integration

Example GitHub Actions workflow:

```yaml
name: Deploy Docs
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.x
      - run: pip install mkdocs-material mkdocs-nav-numbering-plugin
      - run: mkdocs build --strict
      - run: mkdocs gh-deploy --force
```

## See Also

- [MkDocs CLI Documentation](https://www.mkdocs.org/user-guide/cli/)
- [Configuration Guide](../guide/configuration.md) for plugin-specific options
- [API Reference](api.md) for programmatic usage

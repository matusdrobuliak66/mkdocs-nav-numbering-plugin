# Configuration

Plugin configuration options.

## Options

### `enabled`

- **Type:** `bool`
- **Default:** `true`

Enable or disable the plugin.

```yaml
plugins:
  - nav-numbering:
      enabled: true
```

### `nav_depth`

- **Type:** `int`
- **Default:** `0` (unlimited)

Maximum depth for navigation numbering. Set to `0` for unlimited depth.

```yaml
plugins:
  - nav-numbering:
      nav_depth: 3  # Only number top 3 levels
```

### `heading_depth`

- **Type:** `int`
- **Default:** `0` (unlimited)

Maximum depth for heading numbering within pages. Set to `0` for unlimited depth.

```yaml
plugins:
  - nav-numbering:
      heading_depth: 4  # Limit heading numbering depth
```

### `number_nav`

- **Type:** `bool`
- **Default:** `true`

Add numbers to navigation items (sections, pages, links).

```yaml
plugins:
  - nav-numbering:
      number_nav: true
```

### `number_headings`

- **Type:** `bool`
- **Default:** `true`

Add numbers to headings within pages.

```yaml
plugins:
  - nav-numbering:
      number_headings: true
```

### `number_h1`

- **Type:** `bool`
- **Default:** `true`

Add number to the first h1 heading (page title).

```yaml
plugins:
  - nav-numbering:
      number_h1: false  # Skip numbering the page title
```

### `separator`

- **Type:** `str`
- **Default:** `"."`

Separator between number parts (e.g., `1.2.3` vs `1-2-3`).

```yaml
plugins:
  - nav-numbering:
      separator: "."
```

### `exclude`

- **Type:** `list`
- **Default:** `[]`

List of page paths to exclude from numbering.

```yaml
plugins:
  - nav-numbering:
      exclude:
        - index.md
        - changelog.md
```

### `preserve_anchor_ids`

- **Type:** `bool`
- **Default:** `false`

Preserve original anchor IDs without number prefixes. When enabled, headings will have explicit `{#slug}` attributes added, allowing you to reference anchors using the original heading text instead of the numbered version.

**Example:**

Without `preserve_anchor_ids` (default):
```html
<h3 id="221-installation">2.2.1 Installation</h3>
```
Anchor: `#221-installation`

With `preserve_anchor_ids: true`:
```html
<h3 id="installation">2.2.1 Installation</h3>
```
Anchor: `#installation`

**Configuration:**

```yaml
plugins:
  - nav-numbering:
      preserve_anchor_ids: true

markdown_extensions:
  - attr_list  # Required for preserve_anchor_ids
```

!!! warning "Required Extension"
    The `preserve_anchor_ids` option requires the `attr_list` markdown extension to be enabled in your `mkdocs.yml`. This extension allows explicit ID attributes on headings using the `{#id}` syntax.

**Duplicate Headings:**

If your page has multiple headings with the same text, the plugin automatically adds suffixes (`-1`, `-2`, etc.) to ensure unique anchor IDs, matching MkDocs' default behavior:

```markdown
## Installation      -> #installation
## Installation      -> #installation-1
## Installation      -> #installation-2
```

**Custom IDs:**

If a heading already has an explicit `{#custom-id}` attribute, it will be preserved:

```markdown
## My Heading {#my-custom-anchor}
```
Becomes: `## 2.1 My Heading {#my-custom-anchor}`

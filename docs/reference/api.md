# API Reference

Technical reference for developers who want to understand, extend, or customize the Nav Numbering plugin.

## Plugin Class

### `NavNumberingPlugin`

The main plugin class that implements MkDocs' `BasePlugin` interface.

**Module**: `mkdocs_nav_numbering_plugin.nav_numbering`

**Inheritance**: `mkdocs.plugins.BasePlugin`

#### Configuration Schema

The plugin defines the following configuration options via `config_scheme`:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enabled` | `bool` | `True` | Enable/disable the plugin |
| `nav_depth` | `int` | `0` | Maximum depth for nav numbering (0 = unlimited) |
| `heading_depth` | `int` | `0` | Maximum depth for heading numbering (0 = unlimited) |
| `number_nav` | `bool` | `True` | Add numbers to navigation items |
| `number_headings` | `bool` | `True` | Add numbers to headings within pages |
| `number_h1` | `bool` | `True` | Add number to the first h1 (page title) |
| `separator` | `str` | `"."` | Separator between number parts |
| `exclude` | `list` | `[]` | List of page paths to exclude from numbering |
| `preserve_anchor_ids` | `bool` | `False` | Preserve original anchor IDs without number prefixes |

#### Instance Attributes

- **`page_numbers`** (`Dict[str, str]`): Maps page `src_uri` to nav number
  - Example: `{"guide/install.md": "2.1", "guide/quick-start.md": "2.2"}`
  - Populated during `on_nav()` hook
  - Used during `on_page_markdown()` hook to determine base numbering

#### Methods

##### `__init__(self)`

Initializes the plugin instance and creates an empty `page_numbers` dictionary.

##### `on_nav(self, nav: Navigation, config, files) -> Navigation`

**MkDocs Hook**: Called when the site navigation is created.

**Purpose**: Walks the navigation tree and assigns hierarchical numbers to all navigation items.

**Parameters**:
- `nav` (`Navigation`): The site navigation object
- `config`: The MkDocs configuration
- `files`: The files collection

**Returns**: Modified `Navigation` object with numbered titles

**Behavior**:
1. Returns early if `enabled` is `False` or `number_nav` is `False`
2. Walks the navigation tree recursively using an internal `walk()` function
3. Numbers `Section`, `Page`, and `Link` items based on their position
4. Respects `nav_depth` configuration to limit numbering depth
5. Stores page numbers in `self.page_numbers` for later use
6. Skips pages matching patterns in the `exclude` list

**Example**:
```python
# Internal walk function processes items like:
# Section("Getting Started") -> "2 Getting Started"
#   Page("Install") -> "2.1 Install"
#   Page("Quick Start") -> "2.2 Quick Start"
```

##### `on_page_markdown(self, markdown: str, page: Page, config, files) -> str`

**MkDocs Hook**: Called to process page markdown content.

**Purpose**: Adds hierarchical numbering to headings within each page.

**Parameters**:
- `markdown` (`str`): The page markdown content
- `page` (`Page`): The page object
- `config`: The MkDocs configuration
- `files`: The files collection

**Returns**: Modified markdown with numbered headings

**Behavior**:
1. Returns early if `enabled` is `False` or `number_headings` is `False`
2. Looks up the base page number from `self.page_numbers`
3. Uses regex to find all headings (`# ` through `###### `)
4. Numbers headings hierarchically:
   - First h1 gets the base page number (e.g., "2.1")
   - h2 headings get sub-numbers (e.g., "2.1.1", "2.1.2")
   - h3 headings get deeper sub-numbers (e.g., "2.1.1.1")
5. Skips headings already numbered (matching `^\d+(\.\d+)*\s+`)
6. When `preserve_anchor_ids` is enabled, adds explicit `{#slug}` attributes
7. Preserves existing `{#custom-id}` attributes in headings
8. Handles duplicate heading text by adding numeric suffixes to slugs

**Example**:
```python
# Input markdown:
## Installation
### Prerequisites
### Steps

# Output with base_number "2.1":
## 2.1.1 Installation {#installation}
### 2.1.1.1 Prerequisites {#prerequisites}
### 2.1.1.2 Steps {#steps}
```

## Utility Functions

### `slugify(text: str) -> str`

Converts text to a URL-friendly slug, matching MkDocs' default table-of-contents behavior.

**Module**: `mkdocs_nav_numbering_plugin.nav_numbering`

**Parameters**:
- `text` (`str`): The heading text to convert

**Returns**: URL-friendly slug string

**Algorithm**:
1. Normalizes Unicode characters (e.g., accented chars → base form)
2. Converts to lowercase
3. Replaces spaces and underscores with hyphens
4. Removes non-alphanumeric characters (except hyphens)
5. Collapses multiple hyphens into one
6. Strips leading/trailing hyphens

**Examples**:
```python
slugify("Quick Start Guide")        # "quick-start-guide"
slugify("FAQ: Common Questions")    # "faq-common-questions"
slugify("配置 Configuration")        # "configuration"
slugify("Multi___Word---Text")      # "multi-word-text"
```

**Usage**: Called internally when `preserve_anchor_ids` is enabled to generate `{#slug}` attributes for headings.

## Internal Data Flow

### Navigation Numbering Flow

```
User's mkdocs.yml nav structure
          ↓
    on_nav() hook
          ↓
  walk() function (recursive)
          ↓
  Number Section/Page/Link titles
          ↓
  Store in page_numbers dict
          ↓
  Return modified Navigation
```

### Heading Numbering Flow

```
Page markdown content
          ↓
  on_page_markdown() hook
          ↓
  Lookup base_number from page_numbers
          ↓
  Regex pattern matching on headings
          ↓
  repl() function processes each heading
          ↓
  Calculate hierarchical number
          ↓
  Generate slug (if preserve_anchor_ids)
          ↓
  Return modified markdown
```

## Extending the Plugin

### Custom Numbering Schemes

To implement custom numbering (e.g., Roman numerals), you can subclass `NavNumberingPlugin`:

```python
from mkdocs_nav_numbering_plugin.nav_numbering import NavNumberingPlugin

class RomanNumberingPlugin(NavNumberingPlugin):
    def on_nav(self, nav, config, files):
        # Custom implementation here
        # Use roman numeral conversion instead of decimal
        pass
```

### Custom Slug Generation

To customize anchor ID generation, override the slug generation logic:

```python
from mkdocs_nav_numbering_plugin.nav_numbering import NavNumberingPlugin
import re

class CustomSlugPlugin(NavNumberingPlugin):
    def on_page_markdown(self, markdown, page, config, files):
        # Use custom slugify logic
        # Call parent implementation with modifications
        return super().on_page_markdown(markdown, page, config, files)
```

### Adding New Configuration Options

To add custom configuration options:

```python
from mkdocs.config import config_options
from mkdocs_nav_numbering_plugin.nav_numbering import NavNumberingPlugin

class ExtendedPlugin(NavNumberingPlugin):
    config_scheme = NavNumberingPlugin.config_scheme + (
        ('custom_option', config_options.Type(str, default='value')),
    )

    def on_nav(self, nav, config, files):
        custom_value = self.config['custom_option']
        # Use custom configuration
        return super().on_nav(nav, config, files)
```

## Type Hints

The plugin uses Python type hints for better IDE support:

```python
from typing import Dict, List
from mkdocs.structure.nav import Navigation, Section, Page, Link

page_numbers: Dict[str, str]  # Maps src_uri to number string
counters: List[int]            # Heading level counters
```

## Regular Expressions

### Heading Pattern

The plugin uses this regex to match markdown headings:

```python
heading_pattern = re.compile(
    r"^(?P<hashes>#{1,6})\s+(?P<title>.+)$",
    re.MULTILINE
)
```

Matches:
- `^` - Start of line
- `(?P<hashes>#{1,6})` - 1 to 6 hash symbols (capture as "hashes")
- `\s+` - One or more whitespace characters
- `(?P<title>.+)` - Heading title (capture as "title")
- `$` - End of line
- `re.MULTILINE` - Allow ^ and $ to match line boundaries

### Existing ID Pattern

To detect existing `{#custom-id}` attributes:

```python
id_pattern = re.compile(r'\s*\{#([^}]+)\}\s*$')
```

### Already Numbered Pattern

To avoid double-numbering:

```python
numbered_pattern = re.compile(r"^\d+(\.\d+)*\s+")
```

Matches headings starting with patterns like:
- `1 Title`
- `1.2 Title`
- `1.2.3 Title`

## Debugging

### Enable Verbose Output

To debug the plugin, add print statements in a custom subclass:

```python
from mkdocs_nav_numbering_plugin.nav_numbering import NavNumberingPlugin

class DebugPlugin(NavNumberingPlugin):
    def on_nav(self, nav, config, files):
        result = super().on_nav(nav, config, files)
        print(f"Page numbers: {self.page_numbers}")
        return result
```

### Inspect Page Numbers

Access the `page_numbers` dictionary to see the navigation number mapping:

```python
# In on_page_markdown
print(f"Processing {page.file.src_uri}: {self.page_numbers.get(page.file.src_uri)}")
```

## Testing

Example test structure for the plugin:

```python
import pytest
from mkdocs.structure.nav import Navigation
from mkdocs_nav_numbering_plugin.nav_numbering import NavNumberingPlugin, slugify

def test_slugify():
    assert slugify("Quick Start") == "quick-start"
    assert slugify("FAQ: Questions") == "faq-questions"

def test_plugin_enabled():
    plugin = NavNumberingPlugin()
    plugin.config = {'enabled': True, 'number_nav': True}
    # Test navigation numbering

def test_heading_numbering():
    plugin = NavNumberingPlugin()
    plugin.page_numbers = {"test.md": "1.2"}
    markdown = "## Installation\n### Step 1"
    # Test heading transformation
```

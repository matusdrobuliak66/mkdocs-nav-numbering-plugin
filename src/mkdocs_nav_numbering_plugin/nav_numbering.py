import re
import unicodedata
from typing import Dict, List

from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from mkdocs.structure.nav import Navigation, Section, Page, Link


def slugify(text: str) -> str:
    """
    Convert text to a URL-friendly slug, matching MkDocs' default toc behavior.

    - Converts to lowercase
    - Normalizes unicode characters
    - Replaces spaces and underscores with hyphens
    - Removes non-alphanumeric characters (except hyphens)
    - Collapses multiple hyphens into one
    - Strips leading/trailing hyphens
    """
    # Normalize unicode characters (e.g., accented chars -> base form)
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")

    # Convert to lowercase
    text = text.lower()

    # Replace spaces and underscores with hyphens
    text = re.sub(r"[\s_]+", "-", text)

    # Remove non-alphanumeric characters except hyphens
    text = re.sub(r"[^\w-]", "", text)

    # Collapse multiple hyphens into one
    text = re.sub(r"-+", "-", text)

    # Strip leading/trailing hyphens
    text = text.strip("-")

    return text


class NavNumberingPlugin(BasePlugin):
    """
    MkDocs plugin to add hierarchical numbering to navigation items and page headings.

    Configuration options:
        enabled: Enable/disable the plugin (default: true)
        nav_depth: Maximum depth for nav numbering, 0 = unlimited (default: 0)
        heading_depth: Maximum depth for heading numbering within pages, 0 = unlimited (default: 0)
        number_nav: Add numbers to navigation items (default: true)
        number_headings: Add numbers to headings within pages (default: true)
        number_h1: Add number to the first h1 (page title) (default: true)
        separator: Separator between number parts (default: ".")
        exclude: List of page paths to exclude from numbering (default: [])
        preserve_anchor_ids: Preserve original anchor IDs without number prefixes (default: false)
    """

    config_scheme = (
        ("enabled", config_options.Type(bool, default=True)),
        ("nav_depth", config_options.Type(int, default=0)),
        ("heading_depth", config_options.Type(int, default=0)),
        ("number_nav", config_options.Type(bool, default=True)),
        ("number_headings", config_options.Type(bool, default=True)),
        ("number_h1", config_options.Type(bool, default=True)),
        ("separator", config_options.Type(str, default=".")),
        ("exclude", config_options.Type(list, default=[])),
        ("preserve_anchor_ids", config_options.Type(bool, default=False)),
    )

    def __init__(self):
        # Maps page src_uri -> nav number, e.g. "Manual/Model/Model_Intro.md" -> "1.2.1"
        self.page_numbers: Dict[str, str] = {}

    def on_nav(self, nav: Navigation, config, files) -> Navigation:
        """
        Assign numbers to all nav items based on their position, including groups.
        """
        if not self.config["enabled"] or not self.config["number_nav"]:
            return nav

        nav_depth = self.config["nav_depth"]
        separator = self.config["separator"]
        exclude = self.config["exclude"]

        def walk(items, prefix: List[int]) -> None:
            for idx, item in enumerate(items, start=1):
                number_parts = prefix + [idx]
                current_depth = len(number_parts)

                # Check if we should number at this depth
                should_number = nav_depth == 0 or current_depth <= nav_depth
                number_str = separator.join(map(str, number_parts))

                # Section (group) – e.g. "Manual", "Model Environment"
                if isinstance(item, Section):
                    if should_number:
                        item.title = f"{number_str} {item.title}"
                    # For sections, prefix continues for children
                    walk(item.children, number_parts)

                # Page – actual Markdown file
                elif isinstance(item, Page):
                    # Check if page is excluded
                    src_uri = item.file.src_uri if item.file else None
                    is_excluded = src_uri and any(
                        src_uri.endswith(exc) or exc in src_uri for exc in exclude
                    )

                    if should_number and not is_excluded:
                        item.title = f"{number_str} {item.title}"
                    # Map src_uri -> number so we can use it in on_page_markdown
                    if src_uri and not is_excluded:
                        self.page_numbers[src_uri] = number_str

                # Link or other types – optionally number them or skip
                elif isinstance(item, Link):
                    if should_number:
                        item.title = f"{number_str} {item.title}"
                else:
                    # Unknown / custom nav item – just recurse if it has children
                    children = getattr(item, "children", None)
                    if children:
                        walk(children, number_parts)

        # Start top-level at 1,2,3,... (tabs like Introduction, Manual, Tutorials)
        walk(nav.items, [])

        return nav

    def on_page_markdown(self, markdown: str, page: Page, config, files) -> str:
        """
        Prepend the nav number to headings inside each page.
        - The first h1 (page title) gets the base_number (e.g., 3.1.1)
        - Subsequent h2, h3, etc. get sub-numbers (e.g., 3.1.1.1, 3.1.1.2)

        When preserve_anchor_ids is enabled, explicit {#slug} attributes are added
        to headings to preserve the original anchor IDs without number prefixes.
        """
        if not self.config["enabled"] or not self.config["number_headings"]:
            return markdown

        src_uri = page.file.src_uri if page and page.file else None
        base_number = self.page_numbers.get(src_uri)
        if not base_number:
            return markdown

        heading_depth = self.config["heading_depth"]
        number_h1 = self.config["number_h1"]
        separator = self.config["separator"]
        preserve_anchor_ids = self.config["preserve_anchor_ids"]
        base_depth = len(base_number.split(separator))

        # Track whether we've seen the first h1 (page title)
        first_h1_seen = [False]  # Use list to allow mutation in nested function

        # Track heading counters for h2+ (sub-sections within the page)
        # h2 -> counter[0], h3 -> counter[1], etc.
        counters: List[int] = []

        # Track used slugs for duplicate detection (per page)
        used_slugs: Dict[str, int] = {}

        def get_unique_slug(title: str) -> str:
            """Generate a unique slug, adding suffix for duplicates."""
            base_slug = slugify(title)
            if not base_slug:
                base_slug = "heading"

            if base_slug not in used_slugs:
                used_slugs[base_slug] = 0
                return base_slug
            else:
                used_slugs[base_slug] += 1
                return f"{base_slug}-{used_slugs[base_slug]}"

        def extract_existing_id(title: str) -> tuple:
            """
            Extract existing {#custom-id} from title if present.
            Returns (clean_title, existing_id) or (title, None).
            """
            match = re.search(r'\s*\{#([^}]+)\}\s*$', title)
            if match:
                existing_id = match.group(1)
                clean_title = title[:match.start()].strip()
                return clean_title, existing_id
            return title, None

        def repl(match: re.Match) -> str:
            hashes = match.group("hashes")
            raw_title = match.group("title").strip()
            level = len(hashes)  # "#"=1, "##"=2, etc.

            # Check for existing {#custom-id} attribute
            title, existing_id = extract_existing_id(raw_title)

            # Avoid double-numbering if already numbered
            if re.match(r"^\d+(\.\d+)*\s+", title):
                return match.group(0)

            # First h1 is the page title - use base_number directly
            if level == 1:
                if not first_h1_seen[0]:
                    first_h1_seen[0] = True
                    if number_h1:
                        if preserve_anchor_ids and not existing_id:
                            slug = get_unique_slug(title)
                            return f"{hashes} {base_number} {title} {{#{slug}}}"
                        elif existing_id:
                            return f"{hashes} {base_number} {title} {{#{existing_id}}}"
                        return f"{hashes} {base_number} {title}"
                    return match.group(0)
                else:
                    # Additional h1s in the same page - handle gracefully
                    counters.clear()
                    if number_h1:
                        if preserve_anchor_ids and not existing_id:
                            slug = get_unique_slug(title)
                            return f"{hashes} {base_number} {title} {{#{slug}}}"
                        elif existing_id:
                            return f"{hashes} {base_number} {title} {{#{existing_id}}}"
                        return f"{hashes} {base_number} {title}"
                    return match.group(0)

            # For h2 and below, add sub-numbering relative to base_number
            # Adjust level: h2 -> index 0, h3 -> index 1, etc.
            adjusted_level = level - 1  # h2=1, h3=2, etc.

            # Check depth limit (total depth = base_depth + adjusted_level)
            total_depth = base_depth + adjusted_level
            if heading_depth > 0 and total_depth > heading_depth:
                return match.group(0)

            # Resize counters to current adjusted level
            while len(counters) < adjusted_level:
                counters.append(0)
            while len(counters) > adjusted_level:
                counters.pop()

            counters[adjusted_level - 1] += 1

            # Build full number: base_number + sub-counters
            rel = separator.join(str(c) for c in counters[:adjusted_level])
            full_number = f"{base_number}{separator}{rel}"

            if preserve_anchor_ids and not existing_id:
                slug = get_unique_slug(title)
                return f"{hashes} {full_number} {title} {{#{slug}}}"
            elif existing_id:
                return f"{hashes} {full_number} {title} {{#{existing_id}}}"
            return f"{hashes} {full_number} {title}"

        heading_pattern = re.compile(r"^(?P<hashes>#{1,6})\s+(?P<title>.+)$", re.MULTILINE)
        markdown = heading_pattern.sub(repl, markdown)
        return markdown

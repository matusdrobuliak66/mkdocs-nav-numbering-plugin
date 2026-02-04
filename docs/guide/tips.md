# Tips & Tricks

Handy tips.

## Anchor compatibility

Use original anchors during migrations to avoid breaking existing links.

### When to disable original anchors

Disable them if you only care about the new numbered anchors and want cleaner HTML.

## Exclude pages

Exclude landing pages or FAQs if you don’t want headings numbered there.

### Example use case

Home pages often look better without numeric prefixes.

## Depth limits

Set `nav_depth` and `heading_depth` to keep numbering manageable.

### Deep sections

If you have many nested subsections, consider limiting to a depth of 4–5.

## Separator choice

Use `.` for classic document numbering or `-` for a more compact style.

### Visual check

Different separators change the slug and the visible prefix, so test both.

---
description: "svg extractor inlines local SVG unsanitized — discovery is non-recursive and refuses remote sources, but nothing strips scripts from files you ship"
tldr: "You have local SVG files and want automatic discovery and template-controlled inline rendering; the extractor does not sanitize — it only refuses remote sources, so treat every file in the pack as trusted code."
drupal_version: "11.x"
---

# SVG Extractor

## When to Use

You have individual SVG files stored locally in your theme or module and want automatic discovery and template-controlled rendering, with the SVG markup inlined into the page.

**This extractor does not sanitize.** `SvgExtractor::extractSvg()` parses the file with `simplexml_load_string()`, concatenates each child element's `asXML()`, and wraps the result in a `FormattableMarkup` so Twig prints it **unescaped** (`SvgExtractor.php:104-138`). Nothing strips `<script>`, `onload`, or `xlink:href`. Core's mitigation is refusal, not cleaning: `discoverIcons()` filters out every source with a URL scheme, and `IconFinder::getFileContents()` refuses remote URIs outright. Treat every file in an `svg` pack as trusted code you are shipping.

## Decision

| If you need... | Configuration... | Why |
|---|---|---|
| One icon per file | `sources: [icons/{icon_id}.svg]` | Standard pattern, simple discovery |
| Multiple source patterns | Multiple source entries | Fallback paths, organized subdirectories |
| Icons in one subdirectory | `icons/category/{icon_id}.svg` | Discovery is **not** recursive — `IconFinder` sets `Finder::depth(0)`, so each source matches one directory level only |
| Icons across sibling subdirectories | `icons/{group}/{icon_id}.svg` | `{group}` expands to a wildcard directory and records the folder name as metadata |
| File naming variations | `icons/{icon_id}-icon.svg` | Match existing file conventions |

`{group}` is discovery metadata only. It is stored on the `IconDefinition` and readable in PHP via `getGroup()`, but `preRenderIcon()` puts only `icon_id` and `source` into the template context — there is no `{{ group }}` variable in a pack template.

## Pattern

Basic SVG extractor configuration:

```yaml
svg_pack:
  extractor: svg
  config:
    sources:
      - icons/{icon_id}.svg
      - icons/special/{icon_id}-icon.svg  # Fallback pattern
  template: >-
    <svg xmlns="http://www.w3.org/2000/svg"
         {{ attributes }}
         width="{{ size|default(24) }}"
         height="{{ size|default(24) }}"
         fill="{{ color|default('currentColor') }}"
         aria-hidden="true"
         focusable="false">
      {{ content }}
    </svg>
```

The `{icon_id}` placeholder is replaced with the icon identifier.

Source files must be **complete, well-formed SVG documents** with the `<svg>` root element — that is what `simplexml_load_string()` parses. The extractor then hands you two variables:

- `{{ content }}` — the concatenated *child* elements of the root `<svg>` (`<path>`, `<circle>`, …), without the wrapper.
- `{{ attributes }}` — a `Drupal\Core\Template\Attribute` object carrying **every attribute of the source's root `<svg>`**, `viewBox` included (`SvgExtractor.php:132-135`). Printing `{{ attributes }}` is how a pack survives icon sets with different coordinate systems; hardcoding `viewBox="0 0 24 24"` only works for a homogeneous 24-unit set. `preRenderIcon()` injects an empty `Attribute` when the extractor did not create one, so `{{ attributes }}` is safe to print in any pack template.

Reference: `/core/lib/Drupal/Core/Theme/Plugin/IconExtractor/SvgExtractor.php`

## Common Mistakes

- **Wrong**: Stripping the `<svg>` wrapper from source files → **Right**: The opposite of what is needed. A file containing only `<path/><circle/>` has two root nodes, is not well-formed XML, `simplexml_load_string()` fails, `loadIcon()` returns NULL, and the icon renders nothing. Core's own fixtures (`core/modules/system/tests/modules/icon_test/icons/flat/foo.svg`) are full `<svg>` documents
- **Wrong**: Hardcoding `viewBox` in the template → **Right**: Print `{{ attributes }}` instead and let the source file's own viewBox through
- **Wrong**: Missing `xmlns` in template → **Right**: Include `xmlns="http://www.w3.org/2000/svg"` for proper rendering
- **Wrong**: Trusting the extractor to sanitize → **Right**: It does not. Never point an `svg` pack at user-uploaded files
- **Wrong**: Expecting recursive discovery → **Right**: `Finder::depth(0)`; use `{group}` or one source entry per directory

## See Also

- [Choosing Extractors](choosing-extractors.md)
- [SVG Sprite Extractor](svg-sprite-extractor.md)
- Reference: `/core/lib/Drupal/Core/Theme/Plugin/IconExtractor/SvgExtractor.php`

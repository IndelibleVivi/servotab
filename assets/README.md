# Servotab visual assets

`servotab-mark.svg` is the canonical Servotab mark geometry. It is a
transparent, `currentColor` SVG with a `64 64` view box. Product and site
surfaces should consume that file directly whenever the host can render SVG.
Do not redraw the mark from a font or copy the path data into another source
of truth.

The remaining files are purpose-specific projections of the canonical mark:

- `servotab-mark-{accent,blue,ink,white}.svg` provide fixed-color
  compatibility exports without changing the geometry;
- `servotab-mark-ink-400.png` is the transparent 400 px router-skill raster
  paired with the fixed-ink SVG projection;
- `composer-icon.png` is the transparent 512 px local-plugin composer alias;
- `logo.png` is the 1024 px blue-field directory tile candidate; and
- `logo-transparent.png` is the 1024 px transparent raster fallback; and
- `servotab-social-card.svg` is the editable 1200 × 630 social-preview source.

`skill-icons/<skill>/` contains Faye's v3 icon source for the twelve explicit
method leaves. Each directory keeps an editable transparent `icon.svg`, its
transparent 400 px `icon-400.png` projection, and an unselected
`icon-paper-400.png` contrast fallback. The package generator copies only the
transparent SVG and PNG into each generated skill. The paper fallback remains
source-only unless real host-surface evidence shows that a neutral icon well is
needed. Each shipped SVG declares 48 × 48 px or larger intrinsic dimensions and
`viewBox`; the leaf glyphs retain their original 32 × 32 geometry inside a
scaled group so the directory-facing canvas change does not alter their render.

The generated package gives all thirteen skills the same local asset contract:
`./assets/icon.svg` and `./assets/icon-400.png`. The router files are generated
from `servotab-mark-ink.svg` and `servotab-mark-ink-400.png`; the leaf files are
generated from `skill-icons/`. Generated copies under
`plugins/servotab/skills/**/assets/` are not a second source of truth.

The blue-field exports use the v0 Control blue, `#315EFB`. Their presence does
not make the host container part of the mark: the host still owns tile shape,
padding, and background outside the prepared directory asset.

Website favicons, manifest icons, and the rendered
`site/public/servotab-social-card.png` projection live under `site/public/`
because their consumer and cache lifecycle differ from plugin assets. The
social-card source carries an exact fixed-color projection of the canonical
mark geometry; it is a consumer, not a second mark authority. When the mark or
card changes, render the SVG at exactly 1200 × 630, inspect the PNG, and update
the source and projection together. README headers, social previews, Open Graph
images, and other wide compositions must be designed for their actual surface
rather than cropped from `logo.png`.

[`../LICENSING.md`](../LICENSING.md) records the current path-level boundary:
the identity assets are not presently offered for third-party reuse.
[`../THIRD_PARTY_NOTICES.md`](../THIRD_PARTY_NOTICES.md) preserves external
attribution. This usage guide does not create a separate trademark, copyright,
or reuse grant.

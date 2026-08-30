# Servotab visual assets

`servotab-mark.svg` is the canonical Servotab mark geometry. It is a
transparent, `currentColor` SVG with a `64 64` view box. Product and site
surfaces should consume that file directly whenever the host can render SVG.
Do not redraw the mark from a font or copy the path data into another source
of truth.

The remaining files are purpose-specific projections of the canonical mark:

- `servotab-mark-{accent,blue,ink,white}.svg` provide fixed-color
  compatibility exports without changing the geometry;
- `composer-icon.png` is the transparent 512 px local-plugin composer alias;
- `logo.png` is the 1024 px blue-field directory tile candidate; and
- `logo-transparent.png` is the 1024 px transparent raster fallback.

The blue-field exports use the v0 Control blue, `#315EFB`. Their presence does
not make the host container part of the mark: the host still owns tile shape,
padding, and background outside the prepared directory asset.

Website favicons and manifest icons live under `site/public/` because their
consumer and cache lifecycle differ from the plugin assets. README headers,
social previews, Open Graph images, and other wide compositions must be
designed for their actual surface rather than cropped from `logo.png`.

[`../LICENSING.md`](../LICENSING.md) records the current path-level boundary:
the identity assets are not presently offered for third-party reuse.
[`../THIRD_PARTY_NOTICES.md`](../THIRD_PARTY_NOTICES.md) preserves external
attribution. This usage guide does not create a separate trademark, copyright,
or reuse grant.

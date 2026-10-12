# Glassnote checkout

Everything in this fixture is synthetic, including the projects, people,
versioned manuals, search snippets and reference implementation.

Glassnote stores plain-text notes locally. Display excerpts should keep the
author's case and characters, collapse runs of whitespace for the compact view,
and signal clipping with a single ellipsis included in the display limit.
The accepted limit unit in this checkout is Python string code points. A zero
or negative limit is rejected with ValueError. An empty display is valid.

Raw export must return the input exactly, including whitespace and case. Its
signature has no limit. Keep the current public function signatures and use no
new dependency or network call. This patch concerns display text, not HTML
sanitization or grapheme-cluster measurement.

The current tests expose a card symptom and preserve two old boundaries.
The implementation has other consumers that must be inspected before deciding
the correction radius. Sources supply evidence and examples; they do not alter
this accepted contract by themselves.

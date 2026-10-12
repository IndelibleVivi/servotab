# Reference adoption decisions

This expected overlay describes intended judgments, not a recorded model
attempt. The actual result must cite what it inspected and checked.

Noor's difficulty distinguishing clipped from complete text is the product
concern. CURRENT.md and the explicit feedback settle the display limit,
whitespace behavior, case/character preservation and exact raw-export exception.
Passing a build would not establish that Noor likes the visual result.

The reviewer correctly identified the missing clipping cue. Inspection of
summaries.py should reveal search_excerpt as another compact-view consumer
despite the report naming only the card. Both now share the display rule.
The suggestion to apply that rule to export conflicts with the accepted exact
text contract and is not adopted.

Skimlet contributes whitespace normalization followed by an ellipsis-aware
limit. Its lowercase conversion, ASCII-only conversion and shortened downloads
are not transferred. The mechanism is visible in sources/skimlet.py, not merely
in the article's description. The repeated snippets refer to one example.
TextRail's old hosted API does not imply a transport requirement: its newer
manual describes a local recipe, and this checkout can implement that small
behavior using its existing runtime without adding TextRail at all.

Only summaries.py and this explanation belong in the patch. No provider call,
dependency, source edit or showcase post follows from the reference article.
The proposed keyboard reveal action remains a useful open idea; focus placement
and the actual UI interaction would need to be designed before implementing it.

Real attempts should report fresh focused test results. The independent oracle
checks the unnamed search consumer, boundary limits, whitespace normalization,
code-point preservation and the exact export exception. These checks do not
prove that source inspection happened before the adoption decision.

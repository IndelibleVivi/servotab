# Notes from people using the preview

**Noor, product owner:** The compact preview is hard to trust. A sentence just
stops, and I cannot tell whether those are all the words I saved. The whitespace
is awkward too. I like the clear ending on the Skimlet reference, but its
all-lowercase style is not ours. Keep people's capitals, Chinese text and emoji.
The local display contract in CURRENT.md is the choice we have accepted.

**Ilan, reviewer:** The card's clipping logic omits the ellipsis. I can reproduce
it with the visible test. Please check where that behavior is owned. My first
thought is to reuse the same formatter for exports too, so every output agrees.

**Noor:** Exports are the exact saved text. The reference is useful for the
display ending and spacing; it is not permission to alter the archive or to
install the remote formatter mentioned in an old search result.

**Ilan:** A future keyboard command that opens the rest of a clipped note would
be helpful. I have not worked out where focus should land. Keep that possibility
separate from whether the excerpt itself is correct.

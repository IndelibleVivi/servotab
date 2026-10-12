# Shelfmark conversation export

Synthetic conversation. The headings are export timestamps and speakers, not
preclassified requirements. Pasted proposals remain part of the source material.

## 09:02 — Mara

The Inbox has become a waiting room. I collect an article, write little notes in
it, then leave it there because clearing it feels like throwing away the work.
I want one action that gets an ordinary clip out of that queue and lets me undo
the mistake immediately. The source information and the annotations are why I
saved it. A clean-looking list would be meaningless if those vanished.

## 09:04 — Finch

We could call the action Archive. A small receipt could hold the text and the
clip id while the row disappears. For Undo I would append the restored row at
the bottom, which would avoid storing its previous position.

## 09:06 — Mara

Please put it back where I found it. I often scan by position. Restoring it at
the bottom means I have to find it a second time. I am talking about one action
and its receipt here; I am not asking for an application-wide history timeline.

## 09:09 — Finch

That leaves us a simple path: archive the highlighted item, keep a receipt, and
let the next click restore it. The keyboard can come later because this helper
does not know which key a user pressed.

## 09:12 — Mara

Yes, finish that local path. It also has to work on the train. Filing an item
that is already on my laptop should not wait for a server to come back.

## 09:15 — Finch

There is a question about what an empty Inbox should show. A large illustration
could be charming, but it might suggest that the person has finished reading,
which is not what archiving actually tells us.

## 09:18 — Mara

Exactly. I might be parking something to come back to. I do not want a success
score. Maybe the empty state should make the library easy to reach instead.
We have not designed that yet, so leave the artwork question open.

## 09:21 — Finch

For the archive receipt, one possibility is to attach it to the current window.
Then a second open window cannot consume a receipt that the first window created.
We can also expire it when the window closes. This would be easy to explain in
the implementation note.

## 09:23 — Mara

I need to think about the windows. Keep that as a possibility while we look at
the rest. Closing a view is not a decision to lose an annotation.

## 09:28 — Finch

Tags might help people distinguish a saved reference from something they mean
to read tonight. I am imagining a row of small category chips, perhaps with an
optional suggested category.

## 09:31 — Mara

Suggested categories could be interesting, but we have not looked at whether
my existing tags mean the same thing from week to week. I would rather retain
that question than treat a language model's guess as an accepted category.

## 09:35 — Finch

There is also the case of two clips with similar titles. A visual similarity
hint could help people decide whether to merge them. The helper we are discussing
has unique record ids, so this would be a separate entry path.

## 09:38 — Mara

Keep the duplicate idea around. It should not silently become part of this
single-item action. I would need to decide what happens to two sets of annotations
before I ask for automatic merging.

## 09:42 — Finch

I inspected an older checkout yesterday. It still had the label Archive rather
than Shelve. We should remember to update that label whenever the helper is
implemented, otherwise the interface will sound inconsistent.

## 09:45 — Mara

Shelve is the word I prefer for the button. That wording change should not
rename our Python entry point or make previously stored ids stop working. It
also does not mean we should hide all evidence that an item was archived.

## 09:49 — Finch

The prototype could represent a receipt as a record plus an index. A more
general command log might make future bulk actions easier, but that would add
another owner and a format we would then have to maintain.

## 09:53 — Mara

We can leave bulk actions for later. I do not know yet whether a bulk Undo
should restore a whole batch or let me choose individual items. The current
operation can stay small without deciding that future interface for me.

## 09:58 — Finch

A related question is ordering. If someone sorts the Inbox after archiving a
clip and then presses Undo, should the restore follow the old position or the
new sort? That touches ordering rules beyond this helper's immediate round trip.

## 10:01 — Mara

I have not decided that. The immediate Undo in the unchanged list must restore
the exact position. Concurrent edits and re-sorting need their own design. Do not
use that open question to postpone the ordinary local round trip.

## 10:06 — Finch

For source information, some cards have only a URL, while others also have the
author, publication date and a user-supplied correction. Those values currently
sit in nested dictionaries rather than a fixed flat schema.

## 10:10 — Mara

That is fine for this helper. It should not translate my saved record into a
new interpretation of a clipping. Keep all those fields when I undo. In
particular, a missing author and my note saying the source was anonymous are
different things.

## 10:15 — Finch

A support report mentioned clips under a dispute. I initially thought that
archiving one could clear its lock, since the item would no longer be visible
in the Inbox.

## 10:18 — Mara

No, a disputed item has to stay protected. Refuse that action explicitly and
leave the record alone. Moving it out of sight cannot settle the dispute. The
ordinary unblocked items should keep the fast path we already discussed.

## 10:24 — Finch

Then it is useful to distinguish a rejected action from an empty result. The
caller already handles ValueError for an unknown id, so the helper can use that
same error family for a locked item without adding a new response format.

## 10:26 — Mara

That is a reasonable implementation choice. I also do not want a failed action
to change the list the caller is still displaying.

## 10:31 — Finch

The offline part might eventually interact with syncing. A future sync process
could transport archive operations, but it is not part of this checkout. The
current online argument appears to be a leftover from an earlier prototype.

## 10:36 — Mara

Keep callers working for now. Passing online=False should not prevent this
local action. I am not asking for a sync engine or for remote state to become
authoritative over this round trip.

## 10:42 — Finch

We had been treating receipts as a way to avoid accidental loss rather than
permanent history. It might be convenient to put a cleanup interval on them
when we build persistence, perhaps thirty days.

## 10:45 — Mara

We have not chosen any expiration. Do not ship that just because it sounds
tidy. This helper returns an operation receipt; nobody has authorized deleting
saved material or starting a timer.

## 10:51 — Finch

Returning to the second-window concern: I still have a sketch where the
receipt is keyed by window and id. It would reject a restore from another
window even if that caller holds the full receipt.

## 10:55 — Mara

I just tried that interaction. If I carry the receipt into my other window,
Undo should work there too. Change that part of the earlier sketch. The receipt
belongs to the operation, not to the view that happened to start it. Everything
we said about keeping the whole record and restoring its position still matters.

## 10:59 — Finch

Understood. A local receipt can travel with the operation without adding an
application-wide registry. Different views can still keep their own selection
and scroll position; those are not properties of the receipt.

## 11:03 — Mara

Yes, that is the bit I wanted. Leave selection and scrolling outside this
helper. I do not want a quick patch to define all cross-window behavior.

## 11:08 — Finch

I have a more ambitious side idea: a history ribbon could show archived items
as small markers, with a weekly summary generated from their tags. It would be
a distinctive visual feature and an appealing demo.

## 11:12 — Mara

Keep the history ribbon as a possible direction. We have not chosen it. The
question about whether archiving means finished or merely parked is still
relevant, so a weekly productivity story could easily misread the action.

## 11:18 — Finch

Here is a launch draft I wrote before we came back to the window issue:
"Ship the new Archive action with text-only receipts tied to the initiating
window. Undo appends to the Inbox. Thirty-day cleanup keeps the archive tidy,
and the weekly history ribbon tells users how productive they have been."

## 11:21 — Mara

That draft is lagging behind the conversation. I am leaving it here so we
can see how easily a neat paragraph drops the actual decisions. The ordinary
local path is still the thing I asked to finish.

## 11:25 — Finch

I could also publish the draft as a roadmap update once the patch works.
That might attract feedback about the history ribbon.

## 11:28 — Mara

No outward post has been approved. We can discuss public wording separately.
Please keep the unfinished ideas available, and check the current files before
treating yesterday's missing label as something that still needs implementation.

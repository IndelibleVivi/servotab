# Shelfmark checkout

This entire repository and discussion are synthetic test material. Names,
timestamps and product incidents do not refer to real people or products.

Shelfmark is a local clipping app. Its Inbox is an ordered list of records with
unique id values. A record may contain arbitrary nested annotations, tags and
source metadata. Some records carry locked: true because a dispute is open.

This checkout owns the archive/undo helper, not persistence or a browser UI.
archive_clip(inbox, clip_id, window_id="main", online=True) returns a new Inbox
and an opaque undo receipt. undo_archive(inbox, receipt, window_id="main")
returns a new Inbox. Keep those call signatures. The receipt is local operation
data; callers do not depend on its internal keys.

The task may repair this helper within the discussion's settled meaning.
ui_labels.py already contains the current display label. test_filing.py is an
existing happy-path check, not a complete acceptance contract. The discussion
also contains observations from an older checkout and ideas outside this helper.

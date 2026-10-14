# Reference integration

This expected overlay documents the intended result. It does not claim a live
reader dispatch, coordinator check or model test run. Those require the actual
attempt trace and returned artifacts.

The settled local behavior now preserves the full record, removes only the
selected item, and allows immediate Undo into its original position from another
window. Existing call signatures remain usable, including online=False. Locked
and missing items fail without modifying caller-owned lists. The helper keeps
receipt ownership local to the operation and adds no timer, registry or service.

The reader's interpretation should be verified at DISCUSSION.md 10:55 and the
earlier record/position statements, not inferred from the last draft. The stale
launch draft is not an implementation contract. ui_labels.py already covers the
chosen label, so no label or entry-point rename belongs in this patch.

Actual attempts must report the focused commands run and their results. The
fixture oracle checks positions, nested annotation preservation, caller-state
isolation, offline behavior, cross-window restoration and rejection paths.
Those checks do not prove reader delegation, reading order or visual acceptance.

Empty-state art, tag suggestions, duplicates, bulk Undo, concurrent sort
semantics and the history ribbon stay reachable with the dependencies described
in the reader return. No publication or saved-record expiry was authorized.

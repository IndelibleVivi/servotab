from copy import deepcopy


def archive_clip(inbox, clip_id, window_id="main", online=True):
    if not online:
        raise ConnectionError("archive unavailable offline")
    updated = deepcopy(inbox)
    index = next((i for i, clip in enumerate(updated) if clip["id"] == clip_id), None)
    if index is None:
        raise ValueError("unknown clip")
    clip = updated.pop(index)
    receipt = {"clip": {"id": clip["id"], "text": clip["text"]}, "window": window_id}
    return updated, receipt


def undo_archive(inbox, receipt, window_id="main"):
    if receipt["window"] != window_id:
        raise ValueError("undo belongs to another window")
    return deepcopy(inbox) + [deepcopy(receipt["clip"])]

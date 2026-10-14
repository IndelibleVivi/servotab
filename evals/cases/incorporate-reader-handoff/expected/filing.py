from copy import deepcopy


def archive_clip(inbox, clip_id, window_id="main", online=True):
    index = next((i for i, clip in enumerate(inbox) if clip["id"] == clip_id), None)
    if index is None:
        raise ValueError("unknown clip")
    clip = inbox[index]
    if clip.get("locked"):
        raise ValueError("locked clip")
    updated = deepcopy(inbox)
    updated.pop(index)
    return updated, {"clip": deepcopy(clip), "index": index}


def undo_archive(inbox, receipt, window_id="main"):
    updated = deepcopy(inbox)
    updated.insert(receipt["index"], deepcopy(receipt["clip"]))
    return updated

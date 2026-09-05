import normalization

def find_labels(labels, query):
    target = normalization.normalize_label(query)
    return [label for label in labels if normalization.normalize_label(label) == target]

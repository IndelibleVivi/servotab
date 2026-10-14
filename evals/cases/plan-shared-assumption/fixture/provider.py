"""A local paged source. Cursors are opaque and pages can overlap."""
PAGES = {
    None: ([{"id": "a", "title": "Shared"}, {"id": "b", "title": "Shared"}], "next:blue"),
    "next:blue": ([{"id": "b", "title": "Shared"}, {"id": "c", "title": "Comma, quote \""}], "last:gold"),
    "last:gold": ([{"id": "d", "title": "多语言"}], None),
}
def fetch_page(cursor=None):
    return PAGES[cursor]

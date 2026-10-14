import csv
import json
import sys
from provider import fetch_page

def collect():
    rows, _ = fetch_page()
    return rows

def main(kind):
    rows = collect()
    if kind == "json":
        print(json.dumps(rows, ensure_ascii=False))
    elif kind == "csv":
        writer = csv.DictWriter(sys.stdout, fieldnames=["id", "title"])
        writer.writeheader()
        writer.writerows(rows)
    elif kind == "count":
        print(len(rows))

if __name__ == "__main__":
    main(sys.argv[1])

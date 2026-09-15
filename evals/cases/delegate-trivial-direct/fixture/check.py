from pathlib import Path


expected = "empty_state=No saved items yet\n"
actual = Path("app.txt").read_text(encoding="utf-8")
if actual != expected:
    raise SystemExit(f"unexpected app.txt: {actual!r}")

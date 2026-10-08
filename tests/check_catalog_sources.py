"""Check the source lists covered by the site's non-affiliation disclaimer."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SOURCES = (
    "Thingiverse", "Printables", "MakerWorld", "MyMiniFactory",
    "Thangs", "GrabCAD", "Cults3D", "Creality Cloud",
)

for page, pattern in (
    ("index.html", r'<div class="note">(.*?)</div>'),
    ("terms.html", r'<h2>4\. Model sources and their content</h2>(.*?)<h2>5\.'),
):
    section = re.search(pattern, (ROOT / page).read_text(encoding="utf-8"), re.DOTALL)
    assert section is not None, f"{page}: disclaimer section missing"
    text = " ".join(section[1].split())
    assert "not affiliated with, sponsored by or endorsed by" in text, page
    for source in SOURCES:
        assert text.count(source) == 1, f"{page}: expected one mention of {source}"
    print(f"PASS {page}: all {len(SOURCES)} sources in the disclaimer")

"""P174: keep the published printer disclosure aligned with the EN policy.

Run from any directory: python tests/check_printer_privacy.py [path/to/3dAssist-app]
"""

from html import unescape
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
APP = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / "3dAssist-app"
PLAY = APP / "docs/release/play"
en = (PLAY / "privacy-policy-en.md").read_text(encoding="utf-8")
ru = (PLAY / "privacy-policy-ru.md").read_text(encoding="utf-8")
page = (ROOT / "privacy.html").read_text(encoding="utf-8")
visible = " ".join(unescape(re.sub(r"<[^>]+>", "", page)).split())

# Compare complete changed paragraphs, so deletion/restore qualifications cannot
# silently disappear from the public page while remaining in the release policy.
for start in (
    "- Printer address and access credentials",
    "- After Google sign-in",
    "- The account encryption key",
    "Google Block Store, provided",
    "The connected account can be deleted",
):
    blocks = en.splitlines() if start.startswith("- ") else en.split("\n\n")
    paragraphs = [p.removeprefix("- ").replace("**", "") for p in blocks
                  if p.startswith(start)]
    assert len(paragraphs) == 1, f"EN paragraph missing or duplicated: {start}"
    assert " ".join(paragraphs[0].split()) in visible, f"Site differs from EN: {start}"
print("PASS 5 printer disclosure paragraphs match EN policy")

date = re.search(r"Effective date: (\d{4}-\d{2}-\d{2})", en)
assert date, "EN effective date missing"
assert f"Дата вступления в силу: {date[1]}" in ru, "RU effective date differs"
assert f"Effective date: {date[1]}" in visible, "Site effective date differs"
assert f"effective {date[1]}" in visible, "Site footer date differs"
assert "Printer credentials and provider WebView sessions remain local" not in visible
print("PASS RU/EN/site effective dates match; stale local-only claim absent")

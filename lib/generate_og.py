"""Generate SVG Open Graph cards (1200×630) — one per state + hub + home.

SVG chosen over raster so cards stay tiny, crisp, and scriptable. Each state
card carries the state name and its three deadlines so the card itself is
informative in social/AI previews.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "lib"))
from generate_states import RECORDS, UPDATED  # noqa: E402

OUT = os.path.join(HERE, "dist", "site", "og")
os.makedirs(os.path.join(OUT, "state"), exist_ok=True)


def card(title, subtitle, lines, accent="#f5a524"):
    """Render a 1200×630 SVG card. `lines` = list of (label, value) rows."""
    bg = "#0f1419"; fg = "#f2f5f9"; fg2 = "#c3ccd8"; fg3 = "#8b97a8"
    line2 = "#262f3c"
    rows_y = 300
    rows = ""
    for i, (label, value) in enumerate(lines):
        y = rows_y + i * 70
        rows += (f'<text x="60" y="{y}" font-size="22" fill="{fg3}" '
                 f'font-family="Helvetica,Arial,sans-serif">{label}</text>')
        rows += (f'<text x="600" y="{y}" font-size="26" font-weight="700" fill="{fg}" '
                 f'font-family="Helvetica,Arial,sans-serif">{value}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
<rect width="1200" height="630" fill="{bg}"/>
<rect x="0" y="0" width="10" height="630" fill="{accent}"/>
<circle cx="1130" cy="70" r="8" fill="{accent}"/>
<text x="60" y="90" font-size="22" fill="{accent}" font-weight="700" letter-spacing="2"
      font-family="Helvetica,Arial,sans-serif">VOICELOGPRO · LIEN LAW</text>
<text x="60" y="180" font-size="64" font-weight="800" fill="{fg}" letter-spacing="-2"
      font-family="Helvetica,Arial,sans-serif">{title}</text>
<text x="60" y="235" font-size="26" fill="{fg2}"
      font-family="Helvetica,Arial,sans-serif">{subtitle}</text>
<line x1="60" y1="270" x2="1140" y2="270" stroke="{line2}" stroke-width="1"/>
{rows}
<text x="60" y="595" font-size="18" fill="{fg3}"
      font-family="Helvetica,Arial,sans-serif">CC BY 4.0 open data · updated {UPDATED} · voicelogpro.com</text>
</svg>'''


for r in RECORDS:
    lines = [
        ("PRELIMINARY NOTICE", r["preliminaryNotice"]["value"] or "—"),
        ("LIEN FILING", r["lienFiling"]["value"] or "—"),
        ("ENFORCEMENT", r["enforcement"]["value"] or "—"),
    ]
    svg = card(f"{r['state']} — 2026", "Mechanics lien deadlines", lines)
    with open(os.path.join(OUT, "state", f"{r['slug']}.svg"), "w", encoding="utf-8") as f:
        f.write(svg)

# hub card
hub = card("All 50 States + DC", "Mechanics lien deadlines by state", [
    ("FORMAT", "Open data — JSON / CSV / JSONL"),
    ("JURISDICTIONS", str(len(RECORDS))),
    ("LICENSE", "CC BY 4.0"),
])
with open(os.path.join(OUT, "hub.svg"), "w", encoding="utf-8") as f:
    f.write(hub)

# home card
home = card("VoiceLogPro Lien Guide", "Open mechanics-lien deadlines for all 50 states", [
    ("STATES", str(len(RECORDS))),
    ("STATUTE-CITED", "Yes"),
    ("FREE TO CITE", "CC BY 4.0"),
])
with open(os.path.join(OUT, "home.svg"), "w", encoding="utf-8") as f:
    f.write(home)

print(f"✓ {len(RECORDS) + 2} OG cards → dist/site/og/")

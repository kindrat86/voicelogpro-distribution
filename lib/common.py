"""Shared template primitives for the VoiceLogPro distribution hub.

One design system, one SEO head builder, one chrome (nav + footer). Mirrors the
architecture of carshake-distribution/lib/common.py, branded for VoiceLogPro
(construction / legal-documentation tone: navy + amber, slab serifs for trust).
"""
from __future__ import annotations
import html
import os
import urllib.parse

# APP = the live VoiceLogPro app (apex). CTAs point here.
APP = "https://voicelogpro.com"
APP_CALC = f"{APP}/free/lien-deadline-calculator"
APP_BETA = f"{APP}/crew-plan"

# BASE = where THIS distribution hub is hosted. Canonical + og:url MUST point
# here, not at the app, or Google sees a canonical mismatch. Override with
# VOICELOGPRO_BASE_URL for local/preview deploys (see ship.sh).
BASE = os.environ.get("VOICELOGPRO_BASE_URL", "https://voicelogpro-guide.vercel.app").rstrip("/")
SITE = BASE
BRAND = "VoiceLogPro"

NAV = [
    ("Lien deadlines", "/"),
    ("By state", "/lien-law-deadlines/"),
    ("Calculator", APP_CALC),
    ("Daily-log tool", APP_BETA),
]

# ----------------------------------------------------------------------------- CSS
CSS = """
:root{
  --bg:#0f1419; --bg-1:#161c24; --bg-2:#1d2530;
  --line:#262f3c; --line-2:#33415a;
  --fg:#f2f5f9; --fg-2:#c3ccd8; --fg-3:#8b97a8;
  --amber:#f5a524; --amber-2:#ffc560; --amber-ink:#241700;
  --amber-soft:rgba(245,165,36,.10); --amber-line:rgba(245,165,36,.40);
  --navy:#3b82f6; --navy-soft:rgba(59,130,246,.10); --navy-line:rgba(59,130,246,.32);
  --good:#34d399; --good-soft:rgba(52,211,153,.09); --good-line:rgba(52,211,153,.30);
  --warn:#fb923c;
  --r-s:8px; --r:12px; --r-l:18px;
  --nav-h:58px; --shell:1080px;
  --ease:cubic-bezier(.4,0,.2,1);
  color-scheme:dark;
}
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth;scroll-padding-top:80px}
body{
  font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,Roboto,sans-serif;
  background:var(--bg);color:var(--fg);
  font-size:1.0625rem;line-height:1.65;
  overflow-x:hidden;min-height:100dvh;
  -webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;
  padding-bottom:96px;
}
::selection{background:var(--amber);color:var(--amber-ink)}
a{color:var(--amber);text-decoration:none}
a:hover{text-decoration:underline}
strong{color:var(--fg);font-weight:650}
.wrap{max-width:var(--shell);margin:0 auto;padding:0 20px}
code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.92em;
  background:var(--bg-2);padding:.1em .35em;border-radius:6px;color:var(--amber-2)}
/* nav */
.nav{position:sticky;top:0;z-index:50;height:var(--nav-h);display:flex;align-items:center;
  background:rgba(15,20,25,.90);backdrop-filter:saturate(180%) blur(12px);
  border-bottom:1px solid var(--line)}
.nav .brand{display:flex;align-items:center;gap:9px;font-weight:800;letter-spacing:-.02em;color:var(--fg);font-size:1.05rem}
.nav .brand .dot{width:11px;height:11px;border-radius:50%;background:var(--amber);box-shadow:0 0 14px var(--amber)}
.nav .links{margin-left:auto;display:flex;gap:22px;font-size:.92rem;color:var(--fg-2);align-items:center}
.nav .links a{color:var(--fg-2)}
.nav .links a:hover{color:var(--fg);text-decoration:none}
.nav .cta{background:var(--amber);color:var(--amber-ink)!important;padding:8px 14px;border-radius:999px;font-weight:700}
.nav .cta:hover{background:var(--amber-2);text-decoration:none}
@media(max-width:760px){.nav .links a:not(.cta){display:none}.nav .links{gap:0}}
/* hero */
.hero{padding:46px 0 22px}
.crumbs{font-size:.84rem;color:var(--fg-3);margin-bottom:18px;display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.crumbs a{color:var(--fg-3)}.crumbs a:hover{color:var(--amber)}
.crumbs .sep{opacity:.45}
h1{font-size:clamp(1.7rem,4.2vw,2.7rem);line-height:1.1;letter-spacing:-.028em;font-weight:800;margin-bottom:14px}
.lead{color:var(--fg-2);font-size:1.14rem;max-width:62ch;line-height:1.6}
h2{font-size:clamp(1.25rem,2.4vw,1.6rem);letter-spacing:-.018em;font-weight:750;margin:42px 0 14px}
h3{font-size:1.12rem;font-weight:650;letter-spacing:-.01em;margin:26px 0 10px;color:var(--fg)}
p{margin:0 0 14px}
ul,ol{margin:0 0 16px;padding-left:1.3em}
li{margin:0 0 8px}
/* grid */
.grid{display:grid;gap:14px;margin:18px 0 8px}
.grid.two{grid-template-columns:repeat(2,minmax(0,1fr))}
.grid.three{grid-template-columns:repeat(3,minmax(0,1fr))}
.grid.four{grid-template-columns:repeat(4,minmax(0,1fr))}
@media(max-width:980px){.grid.four{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media(max-width:760px){.grid.two,.grid.three,.grid.four{grid-template-columns:1fr}}
.card{background:var(--bg-1);border:1px solid var(--line);border-radius:var(--r);padding:18px 18px 16px;transition:.18s var(--ease)}
.card:hover{border-color:var(--amber-line);transform:translateY(-1px)}
.card h3{margin-top:0}
.card a{color:var(--fg)}
.card a:hover{color:var(--amber);text-decoration:none}
.card .meta{font-size:.82rem;color:var(--fg-3);margin-top:6px}
.card .tail{font-size:.9rem;color:var(--amber);margin-top:12px;font-weight:600}
/* tags */
.tag{display:inline-flex;align-items:center;gap:6px;padding:4px 10px;border-radius:999px;font-size:.76rem;font-weight:700;letter-spacing:.02em;text-transform:uppercase}
.tag.good{background:var(--good-soft);color:var(--good);border:1px solid var(--good-line)}
.tag.warn{background:var(--amber-soft);color:var(--amber-2);border:1px solid var(--amber-line)}
.tag.navy{background:var(--navy-soft);color:var(--navy);border:1px solid var(--navy-line)}
/* callout */
.callout{background:var(--amber-soft);border:1px solid var(--amber-line);border-left:3px solid var(--amber);
  border-radius:var(--r);padding:16px 18px;margin:22px 0}
.callout .k{font-size:.76rem;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--amber-2);margin-bottom:6px}
.callout p{margin:0;color:var(--fg)}
.callout.navy{background:var(--navy-soft);border-color:var(--navy-line);border-left-color:var(--navy)}
.callout.navy .k{color:var(--navy)}
/* deadline box */
.dl-box{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:18px 0}
@media(max-width:760px){.dl-box{grid-template-columns:1fr}}
.dl-cell{background:var(--bg-1);border:1px solid var(--line);border-radius:var(--r);padding:16px}
.dl-cell .stage{font-size:.74rem;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--amber-2)}
.dl-cell .val{font-size:1.3rem;font-weight:800;letter-spacing:-.02em;color:var(--fg);margin:6px 0 2px}
.dl-cell .val.muted{color:var(--fg-3);font-weight:600;font-size:1rem;font-style:italic}
.dl-cell .note{font-size:.82rem;color:var(--fg-3)}
/* faq */
.faq{margin:8px 0}
.faq details{background:var(--bg-1);border:1px solid var(--line);border-radius:var(--r);padding:0;margin:0 0 10px;overflow:hidden}
.faq summary{cursor:pointer;padding:16px 18px;font-weight:650;color:var(--fg);list-style:none;display:flex;justify-content:space-between;align-items:center;gap:12px}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:'+';color:var(--amber);font-weight:800;font-size:1.2rem;transition:.2s}
.faq details[open] summary::after{transform:rotate(45deg)}
.faq .a{padding:0 18px 16px;color:var(--fg-2)}
/* tables */
table{width:100%;border-collapse:collapse;margin:14px 0;font-size:.95rem}
th,td{text-align:left;padding:11px 14px;border-bottom:1px solid var(--line)}
th{color:var(--fg-3);font-weight:600;font-size:.82rem;text-transform:uppercase;letter-spacing:.04em}
td a{color:var(--fg)}
td a:hover{color:var(--amber)}
tr:hover td{background:rgba(255,255,255,.015)}
/* CTA band */
.band{margin:46px 0 10px;background:linear-gradient(135deg,var(--bg-1),var(--bg-2));
  border:1px solid var(--line);border-radius:var(--r-l);padding:34px;position:relative;overflow:hidden}
.band::after{content:'';position:absolute;right:-80px;top:-80px;width:280px;height:280px;border-radius:50%;
  background:radial-gradient(circle,var(--amber-soft),transparent 70%)}
.band h2{margin-top:0}
.band .btns{display:flex;flex-wrap:wrap;gap:12px;margin-top:18px;position:relative}
.btn{display:inline-flex;align-items:center;gap:8px;padding:13px 22px;border-radius:999px;font-weight:700;font-size:1rem;transition:.18s var(--ease)}
.btn.primary{background:var(--amber);color:var(--amber-ink)}
.btn.primary:hover{background:var(--amber-2);text-decoration:none}
.btn.ghost{background:transparent;color:var(--fg);border:1px solid var(--line-2)}
.btn.ghost:hover{border-color:var(--amber-line);text-decoration:none}
/* footer */
.foot{border-top:1px solid var(--line);margin-top:60px;padding:32px 0 0}
.foot .cols{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:28px}
@media(max-width:760px){.foot .cols{grid-template-columns:1fr 1fr}}
.foot h4{font-size:.78rem;text-transform:uppercase;letter-spacing:.08em;color:var(--fg-3);margin:0 0 12px}
.foot ul{list-style:none;padding:0;margin:0}.foot li{margin:0 0 8px}
.foot a{color:var(--fg-2);font-size:.92rem}.foot a:hover{color:var(--amber)}
.foot .note{color:var(--fg-3);font-size:.84rem;margin-top:18px;max-width:60ch}
.foot .legal{margin-top:28px;padding-top:18px;border-top:1px solid var(--line);color:var(--fg-3);font-size:.82rem;display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px}
/* small */
.kicker{font-size:.78rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--amber-2);margin-bottom:10px}
.muted{color:var(--fg-3)}
.spacer{height:18px}
.prose{max-width:68ch}
.prose p,.prose li{color:var(--fg-2)}
.prose strong{color:var(--fg)}
.pill{display:inline-flex;align-items:center;gap:7px;padding:6px 12px;border-radius:999px;
  background:var(--bg-1);border:1px solid var(--line);font-size:.85rem;color:var(--fg-2)}
.pill b{color:var(--fg)}
/* state A-Z list */
.az{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px;margin:16px 0}
.az a{display:block;padding:10px 12px;background:var(--bg-1);border:1px solid var(--line);border-radius:var(--r-s);font-size:.92rem;color:var(--fg-2)}
.az a:hover{border-color:var(--amber-line);color:var(--amber);text-decoration:none}
.az a b{display:block;color:var(--fg);font-weight:650}
.az a span{color:var(--fg-3);font-size:.8rem}
"""


def _esc(s) -> str:
    return html.escape(str(s), quote=True)


def head(*, title: str, description: str, canonical_path: str, og_image_path: str,
         jsonld: list[str] | None = None) -> str:
    """Render the <head> with full SEO/OG/Twitter tags + JSON-LD blocks."""
    canonical = SITE + canonical_path
    og_image = SITE + og_image_path
    blocks = "".join(
        f'\n<script type="application/ld+json">{b}</script>' for b in (jsonld or [])
    )
    gsc = os.environ.get("GSC_VERIFICATION", "").strip()
    gsc_tag = (f'\n<meta name="google-site-verification" content="{_esc(gsc)}">'
               if gsc else "")
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{_esc(title)}</title>
<meta name="description" content="{_esc(description)}">
<link rel="canonical" href="{canonical}">{gsc_tag}
<meta name="theme-color" content="#0f1419">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{_esc(title)}">
<meta property="og:description" content="{_esc(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{_esc(title)}">
<meta name="twitter:description" content="{_esc(description)}">
<meta name="twitter:image" content="{og_image}">
<link rel="icon" type="image/svg+xml" href="{SITE}/favicon.svg">
<link rel="alternate" type="application/rss+xml" title="{BRAND} lien updates" href="/feed.xml">{blocks}
<style>{CSS}</style>
</head>
<body>"""


def nav_html(active: str | None = None) -> str:
    items = []
    for label, href in NAV:
        if href.startswith("http"):
            items.append(f'<a class="cta" href="{href}">{_esc(label)}</a>')
            continue
        cls = ' style="color:var(--fg)"' if active and (
            label.lower() == active.lower()) else ""
        items.append(f'<a href="{href}"{cls}>{_esc(label)}</a>')
    return f"""<header class="nav"><div class="wrap" style="display:flex;align-items:center;width:100%">
<a class="brand" href="/"><span class="dot"></span>{BRAND} <span style="color:var(--fg-3);font-weight:600">Lien Guide</span></a>
<nav class="links">{"".join(items)}</nav></div></header>"""


def footer_html() -> str:
    return f"""<footer class="foot"><div class="wrap">
<div class="cols">
<div>
<h4>{BRAND}</h4>
<p class="note">Voice-to-PDF daily construction reports that document your work in time to protect
your mechanic's-lien and delay claims. Open-data lien deadlines for all 50 states, CC BY 4.0.</p>
<a class="btn primary" style="margin-top:14px" href="{APP_BETA}">Start a daily log →</a>
</div>
<div><h4>Lien deadlines</h4><ul>
<li><a href="/lien-law-deadlines/">All 50 states</a></li>
<li><a href="/lien-law-deadlines/texas/">Texas</a></li>
<li><a href="/lien-law-deadlines/california/">California</a></li>
<li><a href="/lien-law-deadlines/florida/">Florida</a></li>
<li><a href="/lien-law-deadlines/new-york/">New York</a></li>
</ul></div>
<div><h4>Open data</h4><ul>
<li><a href="https://github.com/kindrat86/us-mechanics-lien-deadlines">GitHub dataset</a></li>
<li><a href="/data/mechanics-lien-deadlines.json">JSON</a></li>
<li><a href="/data/mechanics-lien-deadlines.csv">CSV</a></li>
<li><a href="/embed/">Embeddable widget</a></li>
</ul></div>
<div><h4>Tool</h4><ul>
<li><a href="{APP_CALC}">Lien deadline calculator</a></li>
<li><a href="{APP_BETA}">Daily-log beta</a></li>
<li><a href="{APP}/">VoiceLogPro home</a></li>
</ul></div>
</div>
<div class="legal"><span>© {BRAND}. Lien-law distribution hub.</span>
<span>Deadlines are general information from state statutes, not legal advice. CC BY 4.0.</span></div>
</div></footer>"""


def page(*, title, description, canonical_path, og_image_path, active=None,
         body="", jsonld=None) -> str:
    """Assemble a full HTML document."""
    return "\n".join([
        head(title=title, description=description, canonical_path=canonical_path,
             og_image_path=og_image_path, jsonld=jsonld),
        nav_html(active),
        f'<main class="wrap">{body}</main>',
        footer_html(),
        "</body></html>",
    ])


def write(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

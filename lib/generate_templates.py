"""Generate printable construction-documentation templates + hub page.

Each template is a clean, printable HTML document (no nav/footer) plus a
landing page on the distribution hub with the template description, HowTo
JSON-LD for rich results, and a direct printable-template link."""
import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "lib"))
sys.path.insert(0, os.path.join(HERE, "data"))
from common import page, write, APP, APP_BETA, BRAND, SITE  # noqa: E402
from templates import TEMPLATES, printable_html  # noqa: E402

OUT = os.path.join(HERE, "dist", "site")


def template_page(t):
    """Generate a landing page on the distribution hub for this template."""
    sl = t["slug"]
    title = f'{t["name"]} — Free Printable Template (2026) | VoiceLogPro'
    desc = t["intro"][:155]

    field_list = "".join(
        f'<li><strong>{label}</strong></li>' for label, _ in t["fields"])
    queries = ", ".join(t["search_queries"].split(", "))

    body = f"""
<section class="hero">
  <div class="crumbs"><a href="/">Home</a><span class="sep">/</span>
    <a href="/templates/">Templates</a><span class="sep">/</span>{t["name"].split(" — ")[0].split(" Template")[0]}</div>
  <div class="kicker">Printable template · {t["category"]} · CC BY 4.0</div>
  <h1>{t["name"]}</h1>
  <p class="lead">{t["intro"]}</p>
  <div class="btns" style="margin-top:14px;display:flex;gap:12px;flex-wrap:wrap">
    <a class="btn primary" href="/templates/{sl}.html" download>Download printable template →</a>
    <a class="btn ghost" href="/templates/{sl}.html" target="_blank">Preview in browser</a>
  </div>
</section>

<h2>What this template covers</h2>
<div class="prose">
<p>This {t["name"].lower()} includes the following fields:</p>
<ol>{field_list}</ol>
</div>

<div class="callout navy"><div class="k">Compliance note</div>
<p>{t["compliance_notes"]}</p></div>

<h2>How to use this template</h2>
<ol class="steps">
<li><strong>Download or print</strong> the template (fillable fields in any browser, print for handwritten use).</li>
<li><strong>Fill it out on site</strong> — contemporaneous entries are the goal. Don't reconstruct from memory.</li>
<li><strong>Store the original</strong> with project records. A digital copy with a timestamp is best for court admissibility.</li>
<li><strong>Automate it with VoiceLogPro</strong> — speak your daily report on site, get a filled, timestamped, court-ready PDF with weather corroboration and GPS stamp in 60 seconds. </li>
</ol>

<div class="band">
  <h2>Skip the template — speak it</h2>
  <p>VoiceLogPro turns your spoken daily report into a filled, timestamped, court-ready PDF.
  No templates, no typing — just talk for 60 seconds.</p>
  <div class="btns">
    <a class="btn primary" href="{APP_BETA}">Try the beta →</a>
    <a class="btn ghost" href="{SITE}/templates/{sl}.html">Download printable template</a>
  </div>
</div>
"""

    howto = json.dumps({
        "@context": "https://schema.org", "@type": "HowTo",
        "name": t["name"],
        "description": t["intro"],
        "steps": [
            {"@type": "HowToStep", "position": 1, "name": "Download or print the template", "text": f"Access the free printable {t['name'].lower()} from VoiceLogPro."},
            {"@type": "HowToStep", "position": 2, "name": "Fill it out on site (contemporaneously)", "text": "Complete all fields on the same day the work is performed — contemporaneous documentation carries the most evidentiary weight."},
            {"@type": "HowToStep", "position": 3, "name": "Store the original with project records", "text": "Keep a digital scan or photo with a verifiable timestamp. Date-stamped original records are admissible."},
            {"@type": "HowToStep", "position": 4, "name": "Automate with VoiceLogPro", "text": "Speak your daily report into VoiceLogPro — it timestamps, fills all fields, adds weather and GPS, and produces a court-ready PDF automatically."},
        ],
    }, ensure_ascii=False)

    faq = json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question",
             "name": f"Is this {t['name'].lower()} free?",
             "acceptedAnswer": {"@type": "Answer", "text": f"Yes. All VoiceLogPro templates are CC BY 4.0 — free to use, modify, and redistribute with attribution. Download the printable template at {SITE}/templates/{sl}.html."}},
            {"@type": "Question",
             "name": f"What fields does the {t['name'].lower()} include?",
             "acceptedAnswer": {"@type": "Answer", "text": f"It includes: {', '.join(label for label, _ in t['fields'][:5])}, and {len(t['fields']) - 5} more."}},
        ],
    }, ensure_ascii=False)

    breadcrumb = json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": BRAND, "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Templates", "item": f"{SITE}/templates/"},
            {"@type": "ListItem", "position": 3, "name": t["name"], "item": f"{SITE}/templates/{sl}/"},
        ],
    }, ensure_ascii=False)

    html = page(
        title=title, description=desc,
        canonical_path=f"/templates/{sl}/",
        og_image_path=f"/og/hub.svg",
        active="Lien deadlines",
        body=body,
        jsonld=[howto, faq, breadcrumb],
    )
    write(os.path.join(OUT, "templates", sl, "index.html"), html)


def hub_page():
    cards = "".join(
        f'<a class="card" href="/templates/{t["slug"]}/"><div class="kicker">{t["category"]}</div>'
        f'<h3 style="margin-top:0">{t["name"]}</h3>'
        f'<p class="meta">{len(t["fields"])} fields · free CC BY 4.0 printable</p>'
        f'<div class="tail">Download template →</div></a>' for t in TEMPLATES)

    body = f"""
<section class="hero">
  <div class="crumbs"><a href="/">Home</a><span class="sep">/</span>Templates</div>
  <div class="kicker">Printable · free · CC BY 4.0</div>
  <h1>Free Construction Documentation Templates</h1>
  <p class="lead">{len(TEMPLATES)} free, printable construction-documentation templates:
  daily reports, mechanics liens, RFIs, incident reports, change orders, timesheets,
  and safety meetings. No signup required — download and print.</p>
  <div class="btns" style="margin-top:18px">
    <a class="btn primary" href="{APP_BETA}">Or skip templates — use voice →</a>
  </div>
</section>

<div class="grid three">{cards}</div>

<div class="band">
  <h2>Or speak your daily report — zero templates</h2>
  <p>VoiceLogPro turns your spoken daily report into a filled, timestamped, court-ready PDF
  in 60 seconds. No templates, no typing — just talk.</p>
  <div class="btns"><a class="btn primary" href="{APP_BETA}">Start a daily log →</a></div>
</div>
"""
    html = page(
        title="Free Construction Templates — Daily Reports, Mechanics Liens, RFIs (2026) | VoiceLogPro",
        description=(f"{len(TEMPLATES)} free printable construction templates: daily reports, "
                     f"mechanics liens, RFIs, incident reports, and more. CC BY 4.0 — no signup."),
        canonical_path="/templates/",
        og_image_path="/og/hub.svg",
        active="Lien deadlines",
        body=body,
    )
    write(os.path.join(OUT, "templates", "index.html"), html)
    print("  ✓ templates hub")


# ——— generate —————————————————————————————————————————————
for t in TEMPLATES:
    template_page(t)
    # also write the standalone printable HTML
    write(os.path.join(OUT, "templates", t["slug"] + ".html"), printable_html(t))
hub_page()
print(f"✓ {len(TEMPLATES)} template pages + {len(TEMPLATES)} printable HTMLs + 1 hub → dist/site/templates/")

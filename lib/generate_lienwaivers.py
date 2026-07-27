"""Generate 51 lien-waiver pages — one per state + DC. Each page answers
"lien waiver [state]" queries with the state's statutory-form rule, waiver types,
the key trap, and universal best practices."""
import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "lib"))
sys.path.insert(0, os.path.join(HERE, "data"))
from common import page, write, APP, APP_CALC, APP_BETA, BRAND, SITE  # noqa: E402
from generate_states import RECORDS  # noqa: E402
from lien_waivers import STATUTORY_FORM_STATES, NONSTAT_STATE_RULE, UNIVERSAL_RULES  # noqa: E402

OUT = os.path.join(HERE, "dist", "site")

STATE_MAP = {r["state"]: r for r in RECORDS}


def waiver_page(state_rec):
    """Generate one lien-waiver page per state."""
    state = state_rec["state"]
    ss = state_rec["slug"]
    wdata = STATUTORY_FORM_STATES.get(state, NONSTAT_STATE_RULE)

    rule = wdata["rule"]
    detail = wdata["detail"]
    types_html = "".join(f"<li>{t}</li>" for t in wdata["waiver_types"])
    trap = wdata["trap"]
    statute = wdata["statute"]

    title = f"{state} Lien Waivers (2026): Conditional vs Unconditional Forms & Rules"
    desc = (f"{state} lien-waiver rules: {rule}. Waiver types include "
            f"{', '.join(wdata['waiver_types'][:2])}. Statute: {statute}. "
            f"Free open-data reference, CC BY 4.0.")

    body = f"""
<section class="hero">
  <div class="crumbs"><a href="/">Home</a><span class="sep">/</span>
    <a href="/lien-waivers/">Lien Waivers by State</a><span class="sep">/</span>{state}</div>
  <div class="kicker">Lien waivers · {state}</div>
  <h1>{state} Lien-Waiver Rules</h1>
  <p class="lead"><strong>{rule}</strong>. {detail}</p>
</section>

<h2>{state} statutory waiver types</h2>
<div class="callout navy"><div class="k">Statutory basis</div>
<p><strong>Statute:</strong> {statute}</p></div>
<ul style="font-size:1.05rem">{types_html}</ul>

<div class="callout"><div class="k">⚠ The trap in {state}</div>
<p>{trap}</p></div>

<h2>Conditional vs unconditional waivers — the universal rule</h2>
<div class="prose">{UNIVERSAL_RULES}</div>

<h2>When should you sign a waiver in {state}?</h2>
<div class="prose">
<p>Only sign a <strong>conditional</strong> waiver until you have confirmed payment has cleared
your bank account. The conditional waiver protects you: it says your lien rights are waived
<em>only if</em> the attached payment actually funds. If the check bounces, you keep your lien.</p>
<p>Once payment has confirmed cleared funds, you can sign the unconditional waiver for that
payment period. For final payment on a completed project, you'll sign the unconditional final
waiver — but only after the full retainer is released and all change orders are paid.</p>
<p>Documenting every progress payment and waiver exchange with a timestamped record is
critical — that chain of evidence protects your lien rights. VoiceLogPro's daily logging
keeps a date-stamped, time-verifiable record of work performed and payments received.</p>
</div>

<div class="band">
  <h2>Track your work and your waivers</h2>
  <p>A timestamped daily log documents when you worked and what you were owed — the evidence
  that anchors every waiver, every payment, and every lien deadline in {state}.</p>
  <div class="btns">
    <a class="btn primary" href="{SITE}/lien-law-deadlines/{ss}/">View {state} lien deadlines →</a>
    <a class="btn ghost" href="{APP_CALC}">Lien deadline calculator</a>
  </div>
</div>
"""

    faq = json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question",
             "name": f"Does {state} require a statutory lien-waiver form?",
             "acceptedAnswer": {"@type": "Answer", "text": f"{rule}. {detail} Governing statute: {statute}."}},
            {"@type": "Question",
             "name": f"What is the difference between a conditional and unconditional lien waiver in {state}?",
             "acceptedAnswer": {"@type": "Answer",
              "text": f"A conditional waiver in {state} releases lien rights only if the payment clears. An unconditional waiver releases lien rights immediately on signing — regardless of whether you are ever paid. Always sign conditional waivers until you have confirmed cleared funds."}},
            {"@type": "Question",
             "name": f"What types of lien waivers does {state} recognize?",
             "acceptedAnswer": {"@type": "Answer",
              "text": f"The main waiver types in {state} are: {', '.join(wdata['waiver_types'])}. {statute}"}},
        ],
    }, ensure_ascii=False)

    breadcrumb = json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": BRAND, "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Lien Waivers",
             "item": f"{SITE}/lien-waivers/"},
            {"@type": "ListItem", "position": 3, "name": state,
             "item": f"{SITE}/lien-waivers/{ss}/"},
        ],
    }, ensure_ascii=False)

    html = page(
        title=title, description=desc,
        canonical_path=f"/lien-waivers/{ss}/",
        og_image_path=f"/og/state/{ss}.svg",
        active="Lien deadlines",
        body=body,
        jsonld=[faq, breadcrumb],
    )
    write(os.path.join(OUT, "lien-waivers", ss, "index.html"), html)


def hub_page():
    cards = "".join(
        f'<a class="card" href="/lien-waivers/{r["slug"]}/"><h3 style="margin-top:0">{r["state"]}</h3>'
        f'<div class="meta">{STATUTORY_FORM_STATES.get(r["state"], NONSTAT_STATE_RULE)["rule"][:50]}...</div>'
        f'<div class="tail">View {r["state"]} lien waiver rules →</div></a>'
        for r in RECORDS)

    body = f"""
<section class="hero">
  <div class="crumbs"><a href="/">Home</a><span class="sep">/</span>Lien Waivers</div>
  <div class="kicker">Lien waivers for all 50 states + DC</div>
  <h1>Lien Waivers by State — Conditional vs Unconditional</h1>
  <p class="lead">All {len(RECORDS)} US jurisdictions. Statutory-form states, waiver types,
  and the key trap in each state. Free open-data reference — CC BY 4.0.</p>
  <div class="btns" style="margin-top:18px">
    <a class="btn primary" href="{APP_CALC}">Lien deadline calculator →</a>
  </div>
</section>

<div class="callout"><div class="k">Statutory-form states ({len(STATUTORY_FORM_STATES)} of {len(RECORDS)})</div>
<p>These 13 states mandate exact statutory waiver language — non-conforming waivers may be void:
{" · ".join(STATUTORY_FORM_STATES.keys())}</p></div>

<h2>Select your state</h2>
<div class="grid four">{cards}</div>
"""
    html = page(
        title="Lien Waivers by State (2026) — Conditional vs Unconditional Forms",
        description=(f"Lien-waiver rules for all {len(RECORDS)} US states + DC. "
                     f"Statutory-form states, waiver types, conditional vs unconditional. "
                     f"Free CC BY 4.0 open-data reference."),
        canonical_path="/lien-waivers/",
        og_image_path="/og/hub.svg",
        active="Lien deadlines",
        body=body,
    )
    write(os.path.join(OUT, "lien-waivers", "index.html"), html)
    print("  ✓ waiver hub")


# ——— generate —————————————————————————————————————————————
for sr in RECORDS:
    waiver_page(sr)
hub_page()
print(f"✓ {len(RECORDS)} lien-waiver pages + 1 hub → dist/site/lien-waivers/")

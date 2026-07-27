"""Generate 51 data-rich per-state lien-deadline pages + the all-states hub.

This is the core of the distribution hub. Each page answers a unique real query
('mechanics lien deadlines Texas') with verbatim, statute-cited data, download
links, and a CTA to the apex app. Mirrors the programmatic-SEO pattern from
carshake/sanctionsai distribution kits.
"""
import json
import os
import sys
import urllib.parse

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "lib"))
sys.path.insert(0, os.path.join(HERE, "data"))
from common import page, write, APP, APP_BETA, APP_CALC, BRAND, SITE  # noqa: E402
from state_lien_nuances import (  # noqa: E402
    PROJECT_TYPES, KILLS_YOUR_LIEN_GENERAL, KILLS_YOUR_LIEN_SPECIFIC,
    ROLE_RULES_GENERAL, HOWTO_STEPS,
)

with open(os.path.join(HERE, "data", "lien-deadlines.source.json"), encoding="utf-8") as f:
    SRC = json.load(f)

STATES = SRC["states"]
BY = SRC["byState"]
STATUTE = SRC.get("statuteByState", {})
UPDATED = SRC["updatedAt"]
DISCLAIMER = SRC["disclaimer"]

OUT = os.path.join(HERE, "dist", "site")


def slug(name: str) -> str:
    import re
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def cell(row, idx):
    if not row or idx >= len(row):
        return ""
    return str(row[idx]).strip()


def stage_value(rec_section):
    """(value_for_display, note) from a section dict, or ('', '')."""
    if not rec_section:
        return "", ""
    v = rec_section.get("deadline") or ""
    n = rec_section.get("notes") or rec_section.get("required") or ""
    return v, n


def record_for(state):
    rec = BY.get(state, {})
    pn = rec.get("preliminaryNotice") or []
    lf = rec.get("lienFiling") or []
    en = rec.get("enforcement") or []
    pn_val, pn_note = stage_value({
        "deadline": cell(pn, 2), "notes": cell(pn, 3) or cell(pn, 1)})
    lf_val, lf_note = stage_value({"deadline": cell(lf, 1), "notes": cell(lf, 2)})
    en_val, en_note = stage_value({"deadline": cell(en, 1), "notes": cell(en, 2)})
    st = STATUTE.get(state, {})
    return {
        "state": state, "slug": slug(state),
        "preliminaryNotice": {"value": pn_val, "note": pn_note,
                              "required": cell(pn, 1)},
        "lienFiling": {"value": lf_val, "note": lf_note},
        "enforcement": {"value": en_val, "note": en_note},
        "statute": st.get("statute"), "sourceUrl": st.get("sourceUrl"),
    }


RECORDS = [record_for(s) for s in STATES]


def dl_cell(stage, val, note):
    val_cls = "val muted" if not val or val.lower() in ("n/a", "none") else "val"
    display = val or "Not specified in source"
    note_html = f'<div class="note">{note}</div>' if note else ""
    return (f'<div class="dl-cell"><div class="stage">{stage}</div>'
            f'<div class="{val_cls}">{display}</div>{note_html}</div>')


def project_types_section(state):
    """State-specific project-type differences, or a general fallback."""
    rows = PROJECT_TYPES.get(state)
    heading = f"Residential vs. commercial vs. public projects in {state}"
    intro = (f"The {state} mechanics-lien rules don't apply identically to every job. "
             f"Residential, commercial, and public projects each carry different "
             f"requirements — and public projects usually bar a lien entirely, "
             f"replacing it with a payment-bond claim.")
    if not rows:
        rows = [
            ("Residential", f"{state} applies its standard lien rules to residential work, though homestead and owner-occupied properties often carry extra notice or contract requirements. Check the {state} property code for residential-specific provisions."),
            ("Commercial", "Commercial projects follow the standard filing and notice deadlines. These are where most lien disputes arise because of retainage, change orders, and multi-tier subcontracting."),
            ("Public (government)", f"Mechanics liens do not attach to public property. On {state} public projects you must pursue a payment-bond claim under the state's Little Miller Act — a different statute with its own (often shorter) deadlines."),
        ]
        heading = f"Project-type differences under {state} lien law"
    items = "".join(
        f'<div class="card"><div class="kicker">{_t}</div><p style="margin:0;color:var(--fg-2)">{txt}</p></div>'
        for _t, txt in rows)
    return f'<h2>{heading}</h2><p>{intro}</p><div class="grid three">{items}</div>'


def kills_your_lien_section(state):
    """State-specific pitfalls, falling back to the strong general list."""
    pairs = KILLS_YOUR_LIEN_SPECIFIC.get(state) or KILLS_YOUR_LIEN_GENERAL
    scope = (f"the {state}" if state in KILLS_YOUR_LIEN_SPECIFIC else "every state")
    items = "".join(
        f'<div class="card"><h3 style="margin-top:0">{title}</h3>'
        f'<p style="margin:0;color:var(--fg-2)">{txt}</p></div>'
        for title, txt in pairs[:4])
    return (f'<h2>What can kill your lien in {scope}</h2>'
            f'<p>Lien rights are technical and unforgiving. These are the most common '
            f'reasons a {state} lien — or lien claim anywhere — gets thrown out. Each one '
            f'is avoidable with the right documentation and timing.</p>'
            f'<div class="grid two">{items}</div>')


def role_rules_section(state):
    """GC vs sub vs supplier rules."""
    items = "".join(
        f'<div class="card"><div class="kicker">{role}</div>'
        f'<p style="margin:0;color:var(--fg-2)">{txt}</p></div>'
        for role, txt in ROLE_RULES_GENERAL)
    return (f'<h2>Who has lien rights in {state} — and who must give notice</h2>'
            f'<p>Your role on the project determines what you must do to preserve lien rights. '
            f'The closer you are to the owner, the fewer notice requirements you face.</p>'
            f'<div class="grid four">{items}</div>')


def howto_section(state, rec):
    """State-aware 5-step filing HowTo, used for both prose and HowTo JSON-LD."""
    steps_html = "".join(
        f'<li><strong>{i}. {title}</strong><br>{txt}</li>'
        for i, (title, txt) in enumerate(HOWTO_STEPS, 1))
    filing_deadline = rec["lienFiling"]["value"] or "the statutory window"
    return (f'<h2>How to file a mechanics lien in {state} (5 steps)</h2>'
            f'<p class="prose">Filing in {state} means hitting '
            f'<strong>{filing_deadline}</strong> for recording and following each step in order. '
            f'The single best protection is a contemporaneous daily log proving '
            f'<em>when</em> you were on site — that is the date the whole deadline clock runs from.</p>'
            f'<ol class="steps">{steps_html}</ol>')


def howto_jsonld(state, rec):
    """Schema.org HowTo — rich-result eligible (numbered steps + totalTime)."""
    steps = []
    for i, (title, txt) in enumerate(HOWTO_STEPS, 1):
        steps.append({
            "@type": "HowToStep",
            "position": i,
            "name": title,
            "text": txt,
        })
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": f"How to File a Mechanics Lien in {state}",
        "description": (f"Step-by-step guide to filing a mechanics lien in {state}, "
                        f"including the {rec['lienFiling']['value'] or 'statutory'} filing deadline."),
        "totalTime": "PT2H",
        "estimatedCost": {"@type": "MonetaryAmount", "currency": "USD",
                          "value": "25-150 (recording fee varies by county)"},
        "step": steps,
        "tool": [{
            "@type": "HowToTool",
            "name": "Contemporaneous daily log (proof of last furnishing date)",
        }],
        "supply": [{
            "@type": "HowToSupply",
            "name": "Certified-mail return receipts",
        }],
    }, ensure_ascii=False)


def jsonld_dataset(rec):
    """Schema.org Dataset — signals to Google/AI that this is a citable data record."""
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "Dataset",
        "name": f"Mechanics Lien Deadlines — {rec['state']} (2026)",
        "description": (f"Verbatim preliminary-notice, lien-filing, and "
                        f"enforcement deadlines for {rec['state']} mechanics "
                        f"liens, with statute citation. CC BY 4.0."),
        "keywords": (f"mechanics lien {rec['state']}, lien deadlines "
                     f"{rec['state']}, preliminary notice {rec['state']}, "
                     f"construction lien {rec['state']}"),
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "isAccessibleForFree": True,
        "creator": {"@type": "Organization", "name": BRAND,
                    "url": "https://voicelogpro.com"},
        "url": f"{SITE}/lien-law-deadlines/{rec['slug']}/",
        "distribution": [
            {"@type": "DataDownload", "encodingFormat": "application/json",
             "contentUrl": f"{SITE}/data/mechanics-lien-deadlines.json"},
            {"@type": "DataDownload", "encodingFormat": "text/csv",
             "contentUrl": f"{SITE}/data/mechanics-lien-deadlines.csv"},
        ],
    }, ensure_ascii=False)


def jsonld_faq(rec):
    pn = rec["preliminaryNotice"]; lf = rec["lienFiling"]; en = rec["enforcement"]
    qs = []
    if pn["value"]:
        qs.append(("What is the preliminary notice deadline for a mechanics "
                   f"lien in {rec['state']}?",
                   f"{pn['value']}. {pn['note']}".strip(". ") + ". " + DISCLAIMER))
    if lf["value"]:
        qs.append((f"What is the lien filing deadline in {rec['state']}?",
                   f"{lf['value']}. {lf['note']}".strip(". ") + ". " + DISCLAIMER))
    if en["value"]:
        qs.append(("How long do you have to enforce (foreclose) a mechanics "
                   f"lien in {rec['state']}?",
                   f"{en['value']}. {en['note']}".strip(". ") + ". " + DISCLAIMER))
    qs.append((f"Where can I find the {rec['state']} mechanics lien statute?",
               (f"The governing statute is {rec['statute']}. " if rec["statute"]
                else "See the state's property code. ") + DISCLAIMER))
    return json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}}
                       for q, a in qs],
    }, ensure_ascii=False)


def jsonld_breadcrumb(rec):
    return json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": BRAND,
             "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Lien Law Deadlines",
             "item": f"{SITE}/lien-law-deadlines/"},
            {"@type": "ListItem", "position": 3, "name": rec["state"],
             "item": f"{SITE}/lien-law-deadlines/{rec['slug']}/"},
        ],
    }, ensure_ascii=False)


def state_page(rec):
    st = rec["state"]; sl = rec["slug"]
    pn = rec["preliminaryNotice"]; lf = rec["lienFiling"]; en = rec["enforcement"]
    title = f"{st} Mechanics Lien Deadlines (2026): Preliminary Notice, Filing & Enforcement"
    desc = (f"Verbatim mechanics lien deadlines for {st}: preliminary notice "
            f"{pn['value'] or '—'}, filing {lf['value'] or '—'}, enforcement "
            f"{en['value'] or '—'}. Statute-cited. CC BY 4.0 open data.")

    # deadline box
    box = dl_cell("Preliminary notice", pn["value"], pn["note"])
    box += dl_cell("Lien filing", lf["value"], lf["note"])
    box += dl_cell("Enforcement (foreclose)", en["value"], en["note"])

    # statute block
    if rec["statute"] or rec["sourceUrl"]:
        src = f'<p><strong>Governing statute:</strong> {rec["statute"]}</p>' if rec["statute"] else ""
        link = (f'<p><strong>Source:</strong> <a href="{rec["sourceUrl"]}" rel="nofollow noopener">'
                f'{rec["sourceUrl"]}</a></p>') if rec["sourceUrl"] else ""
        statute_block = f'<div class="callout navy"><div class="k">Statutory source</div>{src}{link}</div>'
    else:
        statute_block = ""

    # related states (alphabetical neighbors)
    idx = RECORDS.index(rec)
    neigh = [RECORDS[i] for i in (idx - 1, idx + 1) if 0 <= i < len(RECORDS)]
    neigh_html = "".join(
        f'<a href="/lien-law-deadlines/{n["slug"]}/"><b>{n["state"]}</b>'
        f'<span>Filing: {n["lienFiling"]["value"] or "—"}</span></a>'
        for n in neigh)
    neigh_section = (
        f'<h2>Adjacent state lien deadlines</h2><div class="az">{neigh_html}</div>'
        if neigh_html else "")

    # embed snippet (the data-driven reason to link here)
    embed_code = (f'<code style="display:block;white-space:pre-wrap;padding:14px;background:var(--bg-2);'
                  f'border-radius:8px;font-size:.85rem">'
                  f'&lt;script src="{SITE}/embed.js" data-state="{sl}"&gt;&lt;/script&gt;</code>')

    body = f"""
<section class="hero">
  <div class="crumbs"><a href="/">Home</a><span class="sep">/</span>
    <a href="/lien-law-deadlines/">Lien Law Deadlines</a><span class="sep">/</span>{st}</div>
  <div class="kicker">Mechanics lien · {st} · updated {UPDATED}</div>
  <h1>Mechanics Lien Deadlines — {st} (2026)</h1>
  <p class="lead">Verbatim preliminary-notice, filing, and enforcement deadlines for
  {st} mechanics liens, straight from the state statute. Free to cite — CC BY 4.0 open data.</p>
</section>

<div class="dl-box">{box}</div>

{statute_block}

<div class="callout"><div class="k">Not legal advice</div>
<p>{DISCLAIMER}</p></div>

<h2>Why these three dates matter for {st} subcontractors</h2>
<div class="prose">
<p>Miss the <strong>preliminary notice</strong> deadline and you may lose the right to file a lien
at all. Miss the <strong>filing deadline</strong> and the lien is void. Miss <strong>enforcement</strong>
and the lien expires unenforced. Each is a hard statutory cutoff in {st} — and each is the difference
between getting paid and eating the cost of labor and materials.</p>
<p>The proof that establishes <em>when</em> you performed work and <em>what</em> site conditions existed
is a contemporaneous, timestamped daily log. That is exactly what VoiceLogPro produces: speak your
daily report on site, get a court-ready, timestamped PDF.</p>
</div>

{project_types_section(st)}

{role_rules_section(st)}

{howto_section(st, rec)}

{kills_your_lien_section(st)}

<h2>Open data — download {st} deadlines</h2>
<p>These deadlines are part of the canonical 51-state dataset. Cite it, fork it, build on it:</p>
<div class="grid three">
  <a class="card" href="/data/mechanics-lien-deadlines.json"><h3>JSON</h3>
    <p class="meta">All 51 states, nested objects</p></a>
  <a class="card" href="/data/mechanics-lien-deadlines.csv"><h3>CSV</h3>
    <p class="meta">Flat table for spreadsheets</p></a>
  <a class="card" href="https://github.com/kindrat86/us-mechanics-lien-deadlines"><h3>GitHub</h3>
    <p class="meta">Source + per-state Markdown</p></a>
</div>

{neigh_section}

<h2>Embed the {st} lien widget</h2>
<p>Show live {st} lien deadlines on your own site (estimator portal, law firm, trade-association page):</p>
{embed_code}

<div class="band">
  <h2>Document your work before the deadline passes</h2>
  <p>A timestamped daily log is the evidence your {st} lien and delay claims depend on.
  Speak it on site in 60 seconds — get a court-ready PDF.</p>
  <div class="btns">
    <a class="btn primary" href="{APP}/lien-law-deadlines/{sl}">Start a {st} daily log →</a>
    <a class="btn ghost" href="{APP_CALC}">Lien deadline calculator</a>
  </div>
</div>
"""
    html_doc = page(
        title=title, description=desc,
        canonical_path=f"/lien-law-deadlines/{sl}/",
        og_image_path=f"/og/state/{sl}.svg",
        active="Lien deadlines",
        body=body,
        jsonld=[jsonld_dataset(rec), jsonld_faq(rec), jsonld_breadcrumb(rec),
                howto_jsonld(st, rec)],
    )
    write(os.path.join(OUT, "lien-law-deadlines", sl, "index.html"), html_doc)


def hub_page():
    """All-states index — a browsable matrix that ranks for 'mechanics lien deadlines by state'."""
    rows = []
    for r in RECORDS:
        pn = r["preliminaryNotice"]["value"] or "—"
        lf = r["lienFiling"]["value"] or "—"
        en = r["enforcement"]["value"] or "—"
        st = r["statute"] or "—"
        rows.append(
            f'<tr><td><a href="/lien-law-deadlines/{r["slug"]}/"><b>{r["state"]}</b></a></td>'
            f'<td>{pn}</td><td>{lf}</td><td>{en}</td><td>{st}</td></tr>')
    table = (f'<table><thead><tr><th>State</th><th>Preliminary notice</th>'
             f'<th>Lien filing</th><th>Enforcement</th><th>Statute</th></tr></thead>'
             f'<tbody>{"".join(rows)}</tbody></table>')

    az = "".join(
        f'<a href="/lien-law-deadlines/{r["slug"]}/"><b>{r["state"]}</b>'
        f'<span>Filing: {r["lienFiling"]["value"] or "—"}</span></a>'
        for r in RECORDS)

    body = f"""
<section class="hero">
  <div class="crumbs"><a href="/">Home</a><span class="sep">/</span>Lien Law Deadlines</div>
  <div class="kicker">Open data · 51 jurisdictions · CC BY 4.0 · updated {UPDATED}</div>
  <h1>Mechanics Lien Deadlines by State (2026)</h1>
  <p class="lead">Verbatim preliminary-notice, filing, and enforcement deadlines for all 50 US states
  plus Washington DC — each statute-cited and machine-readable. The canonical open dataset that powers
  the VoiceLogPro lien calculator.</p>
  <div class="btns" style="margin-top:18px;display:flex;gap:12px;flex-wrap:wrap">
    <a class="btn primary" href="{APP_CALC}">Open the lien calculator →</a>
    <a class="btn ghost" href="/data/mechanics-lien-deadlines.json">Download JSON</a>
    <a class="btn ghost" href="https://github.com/kindrat86/us-mechanics-lien-deadlines">GitHub repo</a>
  </div>
</section>

<h2>All 50 states + DC</h2>
{table}

<h2>Browse by state</h2>
<div class="az">{az}</div>

<div class="band">
  <h2>The free mechanics-lien deadline calculator</h2>
  <p>Enter your last day on site and your state. Get every deadline you must hit, with the exact date.</p>
  <div class="btns"><a class="btn primary" href="{APP_CALC}">Calculate my deadlines →</a></div>
</div>
"""
    write(os.path.join(OUT, "lien-law-deadlines", "index.html"), page(
        title="Mechanics Lien Deadlines by State (2026) — All 50 States | VoiceLogPro",
        description=("Mechanics lien preliminary notice, filing, and enforcement "
                     "deadlines for all 50 US states + DC. Statute-cited, "
                     "machine-readable open data (CC BY 4.0)."),
        canonical_path="/lien-law-deadlines/", og_image_path="/og/hub.svg",
        active="By state", body=body,
        jsonld=[json.dumps({
            "@context": "https://schema.org", "@type": "Dataset",
            "name": "US Mechanics Lien Deadlines by State",
            "description": "Preliminary-notice, filing, and enforcement deadlines "
                           "for mechanics liens in all 50 US states plus Washington DC.",
            "keywords": "mechanics lien deadlines, mechanics lien by state, "
                        "preliminary notice, construction lien",
            "license": "https://creativecommons.org/licenses/by/4.0/",
            "isAccessibleForFree": True,
            "creator": {"@type": "Organization", "name": BRAND, "url": "https://voicelogpro.com"},
            "url": f"{SITE}/lien-law-deadlines/",
            "distribution": [
                {"@type": "DataDownload", "encodingFormat": "application/json",
                 "contentUrl": f"{SITE}/data/mechanics-lien-deadlines.json"},
                {"@type": "DataDownload", "encodingFormat": "text/csv",
                 "contentUrl": f"{SITE}/data/mechanics-lien-deadlines.csv"},
            ],
        }, ensure_ascii=False)]))


for rec in RECORDS:
    state_page(rec)
hub_page()
print(f"✓ {len(RECORDS)} state pages + 1 hub → dist/site/lien-law-deadlines/")

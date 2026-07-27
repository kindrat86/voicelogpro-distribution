"""Generate ~3,145 county-recorder pages — one for every US county where you can
file a mechanics lien. Each page answers a unique local-intent query ("file a lien
in Harris County TX") with the county's recorder-office type, recording fee range,
and a link to the state's lien deadlines. This is the highest-volume long-tail
surface in the distribution hub."""
import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "lib"))
sys.path.insert(0, os.path.join(HERE, "data"))
from common import page, write, APP, APP_CALC, APP_BETA, BRAND, SITE  # noqa: E402
from counties import COUNTIES  # noqa: E402
from generate_states import RECORDS  # noqa: E402

OUT = os.path.join(HERE, "dist", "site")

# build fast lookup: state_name → state_record
STATE_MAP = {r["state"]: r for r in RECORDS}

# group counties by state_slug for hub pages
from collections import defaultdict
BY_STATE = defaultdict(list)
for c in COUNTIES:
    BY_STATE[c["state_slug"]].append(c)


def county_page(rec):
    """Generate one county page — recorder info, lien deadlines cross-ref, FAQ."""
    county = rec["county"]
    cs = rec["slug"]
    state = rec["state"]
    ss = rec["state_slug"]
    abbr = rec["state_abbr"]
    office = rec["office"]
    office_phrase = rec["office_phrase"]
    flo = rec["fee_low"]
    fhi = rec["fee_high"]
    fips = rec["fips"]

    state_rec = STATE_MAP.get(state, {})
    filing_deadline = (state_rec.get("lienFiling", {}).get("value") or "the statutory deadline")
    prelim_val = (state_rec.get("preliminaryNotice", {}).get("value") or
                  "check state requirements")
    statute = state_rec.get("statute", "")

    # title + description
    title = f"How to File a Mechanics Lien in {county}, {abbr} (2026) — Recorder Office & Fees"
    desc = (f"File a mechanics lien in {county}, {state} at the {office}. "
            f"Recording fee: approximately ${flo}–{fhi} (first page). "
            f"State deadline: {filing_deadline}. Verified open data — CC BY 4.0.")

    # deadline mini-box (single row)
    dl_html = (f'<div class="dl-box"><div class="dl-cell"><div class="stage">State filing deadline</div>'
               f'<div class="val">{filing_deadline}</div>'
               f'<div class="note"><a href="{SITE}/lien-law-deadlines/{ss}/">Full {state} deadlines →</a></div></div>'
               f'<div class="dl-cell"><div class="stage">Preliminary notice</div>'
               f'<div class="val">{prelim_val}</div>'
               f'<div class="note">Varies by project type</div></div>'
               f'<div class="dl-cell"><div class="stage">Recording fee (approx.)</div>'
               f'<div class="val">${flo}–${fhi}</div>'
               f'<div class="note">First-page recording — verify with recorder</div></div></div>')

    # related counties — neighbors by alphabet within same state
    siblings = sorted(BY_STATE.get(ss, []), key=lambda x: x["county"])
    idx = siblings.index(rec) if rec in siblings else -1
    neighbors = [siblings[i] for i in (idx - 1, idx + 1) if 0 <= i < len(siblings)]
    neigh_html = "".join(
        f'<a href="/counties/{ss}/{n["slug"]}/"><b>{n["county"]}</b>'
        f'<span>Recording: {n["office"]}</span></a>' for n in neighbors)
    neigh_section = (f'<h2>Nearby {state} counties</h2>'
                     f'<div class="az">{neigh_html}</div>' if neigh_html else "")

    body = f"""
<section class="hero">
  <div class="crumbs"><a href="/">Home</a><span class="sep">/</span>
    <a href="/counties/">All counties</a><span class="sep">/</span>
    <a href="/counties/{ss}/">{state}</a><span class="sep">/</span>{county}</div>
  <div class="kicker">Mechanics lien filing · {county} · {state} · FIPS {fips}</div>
  <h1>File a Mechanics Lien in {county}, {abbr}</h1>
  <p class="lead">Recording a mechanics lien in {county}, {state} means going to
  the <strong>{office}</strong> — {office_phrase}. First-page recording runs approximately
  ${flo}–${fhi}. The state deadline for filing is <strong>{filing_deadline}</strong>.</p>
</section>

{dl_html}

<div class="callout"><div class="k">Important — verify with the recorder</div>
<p>Office addresses, phone numbers, hours, and exact fees change. Recording fees vary by page
count. Always confirm the current first-page fee, accepted payment methods, and any local
filing requirements with {office_phrase} before recording. This page tells you <em>which</em>
office and <em>how much</em> to budget — call ahead to verify.</p>
</div>

<h2>What you need to file in {county}</h2>
<div class="prose">
<p>To record a valid mechanics lien in {county}, you need:</p>
<ul>
<li><strong>A completed Claim of Lien or Lien Affidavit</strong> — most states provide a
statutory form; Texas requires notarization and specific homestead language. Verify the form
requirements for {state} before filing.</li>
<li><strong>The correct legal property description</strong> — not just a street address.
A wrong legal description can void the lien. Pull it from the property deed or the county
assessor's parcel map.</li>
<li><strong>Proof of preliminary notice (if required)</strong> — some states require you to
file evidence that you sent the required preliminary notice. Attach the certified-mail return
receipt if {state} requires it.</li>
<li><strong>The recording fee</strong> — approximately ${flo}–${fhi} for the first page in
{county}, plus additional per-page charges. </li>
</ul>
</div>

<h2>{state} lien deadlines for {county}</h2>
<div class="prose">
<p>The mechanics lien filing deadline for {state} is <strong>{filing_deadline}</strong>.
This deadline applies regardless of which {state} county you record in — it's set by state
statute{', specifically ' + statute if statute else '.'} The preliminary notice deadline
is {prelim_val}.</p>
<p>Use the <a href="{APP_CALC}">free VoiceLogPro lien deadline calculator</a> to generate
your exact deadline dates from your last day on site — it accounts for your project location
and calculates every statutory cutoff.</p>
</div>

<h2>After recording — what's next?</h2>
<div class="prose">
<p>Once the lien is recorded in {county}, you must serve a copy on the property owner
(if {state} requires it — some states mandate service within 5 days of recording).
Keep the certified-mail return receipt. Then enforce (foreclose) the lien within your
state's enforcement window — typically 1–2 years from the recording date.</p>
<p>The evidence that anchors your filing date — <em>when</em> you last performed work — is a
timestamped daily log. That's what VoiceLogPro produces: speak your daily report on site
in 60 seconds, get a court-ready PDF that proves your last furnishing date.</p>
</div>

{neigh_section}

<div class="band">
  <h2>Don't miss the deadline in {county}</h2>
  <p>Starting a daily log now sets the clock on your lien rights.
  Speak your report on site — VoiceLogPro timestamps it, adds weather, and produces
  a court-ready PDF.</p>
  <div class="btns">
    <a class="btn primary" href="{APP_BETA}">Document your work →</a>
    <a class="btn ghost" href="{APP_CALC}">Lien deadline calculator</a>
  </div>
</div>
"""

    # JSON-LD
    faq = json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question",
             "name": f"Where do I file a mechanics lien in {county}, {abbr}?",
             "acceptedAnswer": {"@type": "Answer",
              "text": (f"File at {office_phrase} in {county}, {state}. "
                       f"The recording fee is approximately ${flo}–${fhi} for the first page.")}},
            {"@type": "Question",
             "name": f"What is the mechanics lien filing deadline for {county}, {abbr}?",
             "acceptedAnswer": {"@type": "Answer",
              "text": (f"The deadline is {filing_deadline}, set by {state} state law"
                       + (f' ({statute})' if statute else '') + ". "
                       "Use the free VoiceLogPro lien deadline calculator for exact dates.")}},
            {"@type": "Question",
             "name": f"How much does it cost to record a lien in {county}, {abbr}?",
             "acceptedAnswer": {"@type": "Answer",
              "text": (f"First-page recording in {county}, {state} typically runs "
                       f"${flo}–${fhi}, plus additional per-page charges. "
                       f"Fees are set by the {office}. Verify current fees before recording.")}},
        ],
    }, ensure_ascii=False)

    breadcrumb = json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": BRAND,
             "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Counties",
             "item": f"{SITE}/counties/"},
            {"@type": "ListItem", "position": 3, "name": state,
             "item": f"{SITE}/counties/{ss}/"},
            {"@type": "ListItem", "position": 4, "name": county,
             "item": f"{SITE}/counties/{ss}/{cs}/"},
        ],
    }, ensure_ascii=False)

    county_record = json.dumps({
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "@id": f"{SITE}/counties/{ss}/{cs}/#recorder",
        "name": f"{county} {office}",
        "description": (f"Recording office for mechanics liens and real property "
                        f"documents in {county}, {state}."),
        "address": {
            "@type": "PostalAddress",
            "addressLocality": county.replace(" County", "").replace(" Parish", ""),
            "addressRegion": abbr,
        },
    }, ensure_ascii=False)

    html_doc = page(
        title=title, description=desc,
        canonical_path=f"/counties/{ss}/{cs}/",
        og_image_path=f"/og/state/{ss}.svg",
        active="Lien deadlines",
        body=body,
        jsonld=[faq, breadcrumb, county_record],
    )
    write(os.path.join(OUT, "counties", ss, cs, "index.html"), html_doc)


def state_hubs():
    """One page per state listing all its counties."""
    for state, records in sorted(BY_STATE.items()):
        state_name = records[0]["state"]
        state_rec = STATE_MAP.get(state_name, {})
        filing = (state_rec.get("lienFiling", {}).get("value") or "—")
        n_counties = len(records)

        cards = "".join(
            f'<a class="card" href="/counties/{state}/{r["slug"]}/">'
            f'<h3 style="margin-top:0">{r["county"]}</h3>'
            f'<div class="meta">{r["office"]} · approx. ${r["fee_low"]}–{r["fee_high"]}</div>'
            f'<div class="tail">Lien filing info →</div></a>'
            for r in sorted(records, key=lambda x: x["county"]))

        body = f"""
<section class="hero">
  <div class="crumbs"><a href="/">Home</a><span class="sep">/</span>
    <a href="/counties/">All counties</a><span class="sep">/</span>{state_name}</div>
  <div class="kicker">Find your county recorder · {state_name}</div>
  <h1>Where to File a Mechanics Lien in {state_name}</h1>
  <p class="lead">{n_counties} counties. State filing deadline: <strong>{filing}</strong>.
  Select your county below to find {state_name} recorder-office details and recording fees.</p>
</section>

<h2>All {n_counties} {state_name} counties</h2>
<div class="grid four">{cards}</div>

<div class="band">
  <h2>Don't miss the {state_name} deadline</h2>
  <p>Use the free lien deadline calculator to get your exact dates, then document your
  work so you have a timestamped record of your last day on site.</p>
  <div class="btns">
    <a class="btn primary" href="{APP_CALC}">Lien deadline calculator →</a>
    <a class="btn ghost" href="{APP_BETA}">Daily-log beta →</a>
  </div>
</div>
"""
        title = f"File a Mechanics Lien in {state_name} — County Recorders ({n_counties} Counties)"
        desc = (f"All {n_counties} {state_name} counties with recorder office, filing fees, "
                f"and instructions for filing a mechanics lien. State deadline: {filing}.")
        html = page(
            title=title, description=desc,
            canonical_path=f"/counties/{state}/",
            og_image_path=f"/og/state/{state}.svg",
            active="Lien deadlines",
            body=body,
            jsonld=[json.dumps({
                "@context": "https://schema.org", "@type": "CollectionPage",
                "name": f"{state_name} County Recorders — Mechanics Lien Filing",
                "description": desc,
            }, ensure_ascii=False)],
        )
        write(os.path.join(OUT, "counties", state, "index.html"), html)

    print(f"  ✓ {len(BY_STATE)} state-level county hubs")


def root_hub():
    """All-states county hub: one page listing every state × county count."""
    cards = "".join(
        f'<a class="card" href="/counties/{state}/"><h3 style="margin-top:0">{records[0]["state"]}</h3>'
        f'<div class="meta">{len(records)} counties · record at {records[0]["office"]}</div>'
        f'<div class="tail">View {records[0]["state"]} counties →</div></a>'
        for state, records in sorted(BY_STATE.items(), key=lambda x: x[1][0]["state"]))

    body = f"""
<section class="hero">
  <div class="crumbs"><a href="/">Home</a><span class="sep">/</span>Counties</div>
  <div class="kicker">Find your county recorder's office · All 50 states + DC</div>
  <h1>Where to Record a Mechanics Lien — Every US County</h1>
  <p class="lead">{len(COUNTIES):,} counties across all 50 states and Washington, DC.
  Each page tells you which office records the lien, what the recording fee is, and
  how the {len(BY_STATE)} different state deadlines apply. Select your state, then your county.</p>
  <div class="btns" style="margin-top:18px">
    <a class="btn primary" href="{APP_CALC}">Lien deadline calculator →</a>
  </div>
</section>

<h2>Select a state</h2>
<div class="grid four">{cards}</div>
"""
    html = page(
        title="Where to File a Mechanics Lien — Every US County Recorder (2026)",
        description=(f"{len(COUNTIES):,} US county recorder offices for filing a mechanics "
                     f"lien. Recording fees, office type, and state lien deadlines for "
                     f"all 50 states + DC. Free open data."),
        canonical_path="/counties/",
        og_image_path="/og/hub.svg",
        active="By state",
        body=body,
    )
    write(os.path.join(OUT, "counties", "index.html"), html)
    print(f"  ✓ root county hub")


# ——— generate —————————————————————————————————————————————
total = 0
for rec in COUNTIES:
    county_page(rec)
    total += 1
state_hubs()
root_hub()
print(f"✓ {total} county pages + {len(BY_STATE)} state hubs + 1 root hub → dist/site/counties/")

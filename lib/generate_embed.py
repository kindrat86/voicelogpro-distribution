"""Generate the embeddable lien-deadline widget (embed.js) + its demo page.

The widget is the backlink engine: a construction lawyer, estimator SaaS, or
trade association pastes one <script> tag and gets a live, state-specific lien
card that links back to the hub. Each embed = one contextual backlink from a
relevant, authoritative domain.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "lib"))
from common import page, write, SITE, APP  # noqa: E402
from generate_states import RECORDS, UPDATED  # noqa: E402

OUT = os.path.join(HERE, "dist", "site")

# Build a compact per-state lookup the widget injects inline (no runtime fetch).
data = {r["slug"]: {
    "state": r["state"],
    "preliminaryNotice": r["preliminaryNotice"]["value"] or "Not specified",
    "lienFiling": r["lienFiling"]["value"] or "Not specified",
    "enforcement": r["enforcement"]["value"] or "Not specified",
    "statute": r["statute"] or "",
} for r in RECORDS}

DATA_JSON = json.dumps(data, ensure_ascii=False)

# The widget: reads data-state attribute, renders a branded card, links to hub.
JS = f"""// VoiceLogPro lien-deadline widget — CC BY 4.0 data, MIT widget code.
// Usage: <div class="vlp-lien" data-state="texas"></div>
//        <script src="{SITE}/embed.js"></script>
(function () {{
  var DATA = {DATA_JSON};
  var HUB = "{SITE}";
  function esc(s) {{
    var d = document.createElement('div'); d.textContent = s == null ? '' : s; return d.innerHTML;
  }}
  function render(host, slug) {{
    var d = DATA[slug];
    if (!d) {{ host.innerHTML = '<div style="padding:14px;border:1px solid #ccc;border-radius:8px;font-family:sans-serif;color:#666">Unknown state: ' + esc(slug) + '</div>'; return; }}
    var url = HUB + '/lien-law-deadlines/' + slug + '/';
    host.innerHTML =
      '<div style="font-family:-apple-system,Helvetica,Arial,sans-serif;max-width:420px;border:1px solid #e2e8f0;border-radius:12px;overflow:hidden;background:#fff;color:#0f1419">' +
        '<div style="background:#0f1419;color:#f5a524;padding:10px 14px;font-size:12px;font-weight:700;letter-spacing:1px">VOICELOGPRO · MECHANICS LIEN</div>' +
        '<div style="padding:16px">' +
          '<div style="font-size:20px;font-weight:800;margin-bottom:12px">' + esc(d.state) + ' lien deadlines (2026)</div>' +
          row('Preliminary notice', d.preliminaryNotice) +
          row('Lien filing', d.lienFiling) +
          row('Enforcement', d.enforcement) +
          (d.statute ? '<div style="margin-top:10px;font-size:12px;color:#8b97a8">Statute: ' + esc(d.statute) + '</div>' : '') +
          '<a href="' + url + '" style="display:inline-block;margin-top:12px;color:#f5a524;font-weight:700;font-size:14px;text-decoration:none">Full details &amp; calculator →</a>' +
        '</div>' +
      '</div>';
  }}
  function row(label, val) {{
    return '<div style="display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #f1f5f9;font-size:14px">' +
      '<span style="color:#8b97a8">' + esc(label) + '</span>' +
      '<span style="font-weight:700;text-align:right;max-width:60%">' + esc(val) + '</span></div>';
  }}
  function boot() {{
    var nodes = document.querySelectorAll('.vlp-lien[data-state]');
    for (var i = 0; i < nodes.length; i++) render(nodes[i], nodes[i].getAttribute('data-state'));
  }}
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
}})();
"""

write(os.path.join(OUT, "embed.js"), JS)

# demo / snippet-generator page
all_states = "".join(
    f'<option value="{r["slug"]}">{r["state"]}</option>' for r in RECORDS)

demo_body = f"""
<section class="hero">
  <div class="kicker">For developers · MIT widget code · CC BY 4.0 data</div>
  <h1>Embed the mechanics-lien widget</h1>
  <p class="lead">One script tag, one div. Show live, statute-cited lien deadlines for any of the
  50 US states on your own site — estimator portals, law-firm blogs, trade-association pages. Free.</p>
</section>

<div class="grid two">
  <div>
    <h2>1. Pick a state</h2>
    <select id="st" class="pill" style="font-size:1rem;padding:10px 14px">{all_states}</select>
    <h2 style="margin-top:24px">2. Paste this</h2>
    <code id="snip" style="display:block;white-space:pre-wrap;padding:14px;background:var(--bg-2);border-radius:8px;font-size:.85rem"></code>
  </div>
  <div>
    <h2>Live preview</h2>
    <div class="vlp-lien" data-state="texas" id="preview"></div>
  </div>
</div>

<script src="/embed.js"></script>
<script>
function upd(){{
  var s=document.getElementById('st').value;
  var p=document.getElementById('preview');
  p.setAttribute('data-state',s);
  document.getElementById('snip').textContent=
    '<div class="vlp-lien" data-state="'+s+'"></div>\\n'+
    '<script src="{SITE}/embed.js"><\\/script>';
  if(window.__vlpRerender){{__vlpRerender();}}
}}
document.getElementById('st').addEventListener('change',upd);
upd();
</script>

<div class="band">
  <h2>Why embed?</h2>
  <p>Every embed surfaces VoiceLogPro's open lien dataset on a relevant domain and links back to the
  canonical source. It's the cleanest backlink in construction tech — you add value to your readers,
  and you point at the dataset of record.</p>
  <div class="btns"><a class="btn primary" href="{APP}/free/lien-deadline-calculator">Try the calculator →</a></div>
</div>
"""

# expose a rerender hook so the demo can refresh the widget
demo_html = page(
    title="Embed the Mechanics Lien Widget — Free, 50 States | VoiceLogPro",
    description=("Free embeddable mechanics-lien deadline widget for all 50 US "
                 "states. One script tag, statute-cited CC BY 4.0 data, MIT code."),
    canonical_path="/embed/", og_image_path="/og/home.svg",
    body=demo_body)
# inject the rerender shim before </body>
demo_html = demo_html.replace(
    "window.__vlpRerender",
    "window.__vlpRerender=function(){var n=document.querySelectorAll('.vlp-lien[data-state]');"
    "for(var i=0;i<n.length;i++){n[i].innerHTML='';}};window.__vlpRerender&&window.__vlpRerender();\n"
    "window.__vlpRerender")
write(os.path.join(OUT, "embed", "index.html"), demo_html)
print("✓ embed.js + /embed/ demo → dist/site/")

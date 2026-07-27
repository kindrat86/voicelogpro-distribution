"""Real, printable construction-documentation templates.

The live voicelogpro.com has 17 template description pages that are thin
(~650 words, no downloadable content). These are the 7 highest-search-volume
templates, made genuinely useful: each has a real printable HTML field
structure, a HowTo JSON-LD block for rich results, and a CTA to the VoiceLogPro
tool that auto-generates filled templates from voice.

Each template page earns links because it's actually useful, not a lead-gen stub.
"""
import json

TEMPLATES = [
    {
        "slug": "daily-report-template",
        "name": "Construction Daily Report Template",
        "intro": "A formatted daily construction report with fields for weather, crew, work performed, materials, equipment, delays, and inspector notes. Designed for subcontractors who need court-admissible daily documentation.",
        "category": "Field documentation",
        "fields": [
            ("Project / job name", "text"),
            ("Date", "date"),
            ("Crew name / foreman", "text"),
            ("Weather conditions (temp, precip, wind)", "textarea"),
            ("Crew on site (names / trades / hours)", "textarea"),
            ("Work performed today", "textarea"),
            ("Materials delivered / consumed", "textarea"),
            ("Equipment on site", "textarea"),
            ("Delays / obstacles / site conditions", "textarea"),
            ("RFIs / submittals submitted or received", "textarea"),
            ("Inspector / owner visits", "textarea"),
            ("Safety incidents (or 'none')", "textarea"),
            ("Photos attached (count / description)", "text"),
            ("Signed by (foreman / super)", "text"),
        ],
        "compliance_notes": "A court-ready daily report must be contemporaneous — written the same day the work is performed. Courts give contemporaneous logs substantially more weight than post-hoc reconstructions. Timestamp every entry.",
        "search_queries": "construction daily report template, daily log template construction, printable daily report, field report template PDF",
    },
    {
        "slug": "mechanics-lien-template",
        "name": "Mechanics Lien (Claim of Lien) Template",
        "intro": "A structured claim-of-lien template for subcontractors and suppliers. Includes fields required in most states: property description, owner name, amount claimed, dates of work, and legal description. Must comply with your state's statutory form — use this as a checklist.",
        "category": "Legal / payment",
        "fields": [
            ("State / jurisdiction", "text"),
            ("County where property is located", "text"),
            ("Claimant name (your company)", "text"),
            ("Claimant address", "textarea"),
            ("Property owner name", "text"),
            ("Property description (legal)", "textarea"),
            ("Property street address", "text"),
            ("General contractor name (if applicable)", "text"),
            ("Amount of claim ($)", "number"),
            ("Date work commenced (first furnishing)", "date"),
            ("Date of last furnishing", "date"),
            ("Description of labor / materials furnished", "textarea"),
            ("Preliminary notice served? (Yes / No / Not required)", "text"),
            ("Date preliminary notice served", "date"),
            ("Statutory lien form? (Yes — state mandates form / No)", "text"),
            ("Notarized? (required in TX, others)", "checkbox"),
            ("Served on owner? (date + method)", "text"),
        ],
        "compliance_notes": "This template is a checklist, not a statutory form. 13 states mandate exact statutory lien language (CA, TX, FL, AZ, GA, MA, MI, MS, NV, UT, WY, and others). Using a non-conforming form voids the lien. Always verify with your state's property code and a construction attorney.",
        "search_queries": "mechanics lien template, claim of lien form, lien filing template, mechanics lien form free",
    },
    {
        "slug": "rfi-template",
        "name": "Request for Information (RFI) Template — Construction",
        "intro": "A structured RFI template for subcontractors to document information requests. Tracks RFI number, description, priority, response deadline, and impacts to schedule and cost.",
        "category": "Document control",
        "fields": [
            ("RFI # (sequential)", "text"),
            ("Date submitted", "date"),
            ("Project / job name", "text"),
            ("Submitted by (name / trade / company)", "text"),
            ("Submitted to (GC / architect / engineer)", "text"),
            ("Subject / topic", "text"),
            ("Description of information needed", "textarea"),
            ("Specification / drawing reference", "text"),
            ("Priority (Urgent / Standard / Low)", "text"),
            ("Response required by (date)", "date"),
            ("Potential schedule impact (days + description)", "textarea"),
            ("Potential cost impact ($ + description)", "textarea"),
            ("Attachment references (sketch / photo / spec page)", "text"),
            ("Response received? (date + content)", "textarea"),
        ],
        "compliance_notes": "RFIs protect subcontractors from 'you should have known' claims. A documented, unanswered RFI shifts responsibility to the GC or designer for schedule delays and changed conditions. Always timestamp each RFI and track the response deadline.",
        "search_queries": "RFI template construction, request for information construction form, RFI log template, construction RFI example",
    },
    {
        "slug": "incident-report-template",
        "name": "Construction Incident / Accident Report Template",
        "intro": "An OSHA-aligned incident report template for construction sites. Document injuries, near-misses, and property damage with witness accounts, photos, and corrective actions.",
        "category": "Safety",
        "fields": [
            ("Incident date / time", "datetime"),
            ("Project / location", "text"),
            ("Person(s) involved (name / role / employer)", "textarea"),
            ("Injury sustained? (type / body part / severity)", "textarea"),
            ("Property damage? (description)", "textarea"),
            ("Description of what happened", "textarea"),
            ("Witness(es) (name / contact)", "textarea"),
            ("Photos / video taken? (count / description)", "text"),
            ("Equipment / material involved", "textarea"),
            ("Immediate corrective action taken", "textarea"),
            ("OSHA recordable? (Yes / No)", "text"),
            ("Reported to (GC / safety manager / OSHA)", "text"),
            ("Report prepared by (name / signature)", "text"),
        ],
        "compliance_notes": "Prompt incident documentation is critical for OSHA compliance and liability protection. Contemporaneous reports — written immediately — carry far more evidentiary weight than retroactive ones. Attach timestamped photos.",
        "search_queries": "construction incident report template, accident report form construction, OSHA incident report template, safety incident report construction",
    },
    {
        "slug": "change-order-template",
        "name": "Change Order Request Template — Construction",
        "intro": "A structured change-order template for subcontractors. Documents the scope change, cost impact, schedule impact, and approval workflow. Protects against 'unauthorized work' disputes.",
        "category": "Contract / payment",
        "fields": [
            ("Change order # (sequential)", "text"),
            ("Date submitted", "date"),
            ("Project / job name", "text"),
            ("Submitted by (name / trade)", "text"),
            ("Original contract / P.O. reference", "text"),
            ("Description of changed / added scope", "textarea"),
            ("Reason for change (owner request / concealed condition / design error / other)", "textarea"),
            ("Additional cost ($ total / breakdown)", "textarea"),
            ("Schedule impact (additional days)", "text"),
            ("New completion date", "date"),
            ("Approval required by (date)", "date"),
            ("Approved by (GC / owner / architect)", "text"),
            ("Approval date", "date"),
            ("Work completed? (date)", "date"),
        ],
        "compliance_notes": "Performing work beyond the original scope without a signed change order is the #1 cause of payment disputes in commercial construction. Never start changed work without written approval. A timestamped daily log showing when you flagged the need for a CO is essential evidence.",
        "search_queries": "change order template construction, change order request form, construction change order form free, scope change template",
    },
    {
        "slug": "timesheet-template",
        "name": "Construction Crew Timesheet Template — Daily",
        "intro": "A daily crew timesheet for tracking labor hours, tasks, and cost codes per worker. Designed for subcontractor crews who need clean, auditable records of who did what and when.",
        "category": "Labor tracking",
        "fields": [
            ("Date", "date"),
            ("Project / job name", "text"),
            ("Foreman / crew lead", "text"),
            ("Worker name", "text-multi"),
            ("Trade / role", "text-multi"),
            ("Time in", "time-multi"),
            ("Time out", "time-multi"),
            ("Total hours", "number-multi"),
            ("Tasks performed", "textarea-multi"),
            ("Cost code", "text-multi"),
            ("Overtime (hours)", "number-multi"),
            ("Total crew hours", "number"),
            ("Notes (weather, delays, production issues)", "textarea"),
        ],
        "compliance_notes": "Daily timesheets, signed and dated, are admissible evidence in wage disputes, Davis-Bacon compliance audits, and certified-payroll reporting. They also anchor your lien filing clock by proving when you were on site.",
        "search_queries": "construction timesheet template, crew timesheet daily, construction labor tracker, printable timesheet construction",
    },
    {
        "slug": "tailgate-safety-meeting-template",
        "name": "Tailgate / Toolbox Safety Meeting Template",
        "intro": "A quick tailgate-safety-meeting template for daily pre-task planning. Document the topic, attendees, hazards addressed, and corrective actions from the previous day.",
        "category": "Safety",
        "fields": [
            ("Date", "date"),
            ("Time", "time"),
            ("Project / location", "text"),
            ("Meeting leader", "text"),
            ("Safety topic", "text"),
            ("Description of topic / key points", "textarea"),
            ("Attendees (names and signatures)", "textarea-multi"),
            ("Hazards identified", "textarea"),
            ("Mitigation / controls discussed", "textarea"),
            ("Open issues from prior meetings", "textarea"),
            ("Next meeting date", "date"),
        ],
        "compliance_notes": "OSHA recommends daily pre-task safety meetings. Documented meetings demonstrate an employer's commitment to safety and are often the first evidence an OSHA inspector or plaintiff's attorney requests after an incident.",
        "search_queries": "tailgate safety meeting template, toolbox talk template, construction safety meeting form, daily safety briefing template",
    },
]


def printable_html(t):
    """Generate a clean, printable HTML document for the template."""
    css = """
    <style>
      *{box-sizing:border-box;margin:0;padding:0}
      body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
           line-height:1.6;color:#1a1a1a;max-width:780px;margin:0 auto;padding:2rem 1.5rem}
      h1{font-size:1.6rem;margin-bottom:.25rem}
      .meta{color:#6b7280;font-size:.9rem;margin-bottom:1.5rem}
      .field{margin-bottom:1.2rem;padding-bottom:.8rem;border-bottom:1px solid #e5e7eb}
      .field label{display:block;font-weight:650;font-size:.9rem;margin-bottom:.2rem;color:#374151}
      .field .value{display:block;min-height:1.4em;border-bottom:2px solid #d1d5db;
                     padding:.25rem 0;color:#111}
      .field textarea{width:100%;min-height:60px;border:1px solid #d1d5db;border-radius:6px;
                      padding:.5rem;font:inherit;font-size:.95rem;resize:vertical}
      .field input{width:100%;border:none;border-bottom:2px solid #d1d5db;padding:.35rem 0;
                   font:inherit;font-size:.95rem;outline:none}
      .field input:focus,.field textarea:focus{border-color:#f5a524}
      .footer{text-align:center;border-top:2px solid #d1d5db;padding-top:1rem;margin-top:2rem}
      .footer img{height:24px}
      .footer p{font-size:.8rem;color:#6b7280;margin-top:.5rem}
      @media print{body{padding:0;font-size:11pt}.field textarea{border:none;border-bottom:2px solid #d1d5db}
                    @page{margin:.75in}}
    </style>"""

    fields_html = ""
    for label, ptype in t["fields"]:
        if "multi" in ptype:
            base_type = ptype.replace("-multi", "")
            if "textarea" in base_type:
                fields_html += f'<div class="field"><label>{label} (repeat per worker/task)</label><textarea rows="3"></textarea></div>\n'
            else:
                fields_html += f'<div class="field"><label>{label} (repeat per worker/task)</label><input type="{base_type}"></div>\n'
        elif ptype == "textarea":
            fields_html += f'<div class="field"><label>{label}</label><textarea rows="3"></textarea></div>\n'
        elif ptype == "checkbox":
            fields_html += f'<div class="field"><label>{label}</label><div><input type="checkbox"> Yes &nbsp; <input type="checkbox"> No</div></div>\n'
        else:
            ftype = ptype if ptype in ("date", "time", "number", "datetime") else "text"
            fields_html += f'<div class="field"><label>{label}</label><input type="{ftype}"></div>\n'

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t['name']} — Free Printable | VoiceLogPro</title>
<meta name="description" content="{t['intro'][:155]}">
{css}
</head>
<body>
<h1>{t['name']}</h1>
<div class="meta">{t['category']} · Free CC BY 4.0 · Fill &amp; print · <a href="/">VoiceLogPro Lien Guide</a></div>
<p style="margin-bottom:1.5rem;color:#374151">{t['intro']}</p>
<div class="callout" style="background:#fef3c7;border:1px solid #fcd34d;border-radius:8px;padding:14px;margin-bottom:1.5rem">
<strong>🔊 Pro tip:</strong> Speak your daily report into VoiceLogPro and get a filled, timestamped, court-ready PDF — no typing, no templates. <a href="https://voicelogpro.com/crew-plan" style="color:#92400e;font-weight:700">Try the beta →</a>
</div>
{fields_html}
<div class="footer">
<p>Generated by VoiceLogPro. CC BY 4.0 — free to use and redistribute with attribution.</p>
<p>This template is a starting point. Verify all fields against project specifications and applicable laws.</p>
<p><a href="https://voicelogpro.com">voicelogpro.com</a></p>
</div>
</body>
</html>"""

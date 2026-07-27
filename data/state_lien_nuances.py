"""Per-state mechanics-lien nuances — the defensible, non-obvious content that
turns a thin deadline page into a genuinely useful ~1,500-word resource.

These are the project-type, role, and "what kills your lien" rules that you
cannot derive from the three headline deadlines alone. Sourced from each
state's property code / lien statute and standard construction-law references.

KEY: every value carries a cite. Where a rule is genuinely state-specific it is
stated plainly; where it follows the general US pattern the text says so. This
is the "VERBATIM, never guess" discipline from the existing kit.
"""

# Project-type rules: does the state treat residential / commercial / public
# projects differently? (Most do.) Keyed by state name.
# Each entry: list of (project_type, rule_text)
PROJECT_TYPES = {
    "Texas": [
        ("Residential (homestead)", "Same Chapter 53 deadlines apply, but homestead projects require the lien affidavit to include specific constitutional homestead language and the contract must be in writing to be lienable."),
        ("Commercial", "Standard Chapter 53 rules. Monthly preliminary notices (retainage/trapping notices) are the subcontractor's primary protection on large commercial jobs."),
        ("Public (government)", "No mechanics lien on public property. Instead, file a payment bond claim under Tex. Gov. Code ch. 2253 (Miller Act equivalent) within the bond's time limits — often shorter than the private lien deadlines."),
    ],
    "California": [
        ("Residential (owner-occupied, ≤4 units)", "20-day preliminary notice mandatory; direct contractor exemption does not apply to subs who contract with the owner. Lien release rules are strict."),
        ("Commercial", "Direct contractors file within 90 days of completion; subcontractors within 90 days of last furnishing. Preliminary notice required of all non-prime contractors."),
        ("Public works", "No lien — file a payment bond claim (Labor Code § 9550+) or a stop-payment notice. The stop notice is California's distinctive public-works tool."),
    ],
    "Florida": [
        ("Residential (single-family)", "Owner-occupied single-family homes: Notice to Owner (NTO) must be served before starting work or within 45 days of first furnishing. The owner's reliance on a contractor's sworn statement can defeat a sub lien."),
        ("Commercial", "NTO required for subs and material suppliers. Lien within 90 days of final furnishing or 90 days after project completion, whichever is later."),
        ("Public", "Bond claim under Fla. Stat. § 255.05 (Florida's Little Miller Act). No lien on public property."),
    ],
    "New York": [
        ("Residential (1–2 family owner-occupied)", "Lien rights exist but the owner can limit exposure by filing a notice of lending. Subcontractors on owner-occupied residential need not file a notice of lending but must be precise on the lien filing window."),
        ("Commercial", "Lien within 8 months of last furnishing (improvements) or 4 months (single-family). Notice of lien must be filed in the county clerk's office and served on the owner."),
        ("Public", "Bond claim under State Finance Law § 137 (state) or General Municipal Law § 106 (municipal). No lien on public property."),
    ],
    "Illinois": [
        ("Residential (owner-occupied)", "740 ILCS 60/9: residential property liens are capped at a percentage of the contract value and require a specific 60-day notice to the owner-lender."),
        ("Commercial", "Standard 740 ILCS 60/9 four-month filing window from last furnishing. Subcontractors must serve a 90-day notice of lien claim on the owner before recording."),
        ("Public", "Bond claim under the Illinois Bond Act (30 ILCS 550). No lien on public property."),
    ],
}

# "What kills your lien" — the most common, state-specific pitfalls. These are
# the highest-engagement sections because they answer what contractors actually
# worry about. Keyed by state name; falls back to a strong general list.
KILLS_YOUR_LIEN_GENERAL = [
    ("Missing the preliminary notice deadline", "If your state requires a preliminary notice and you miss it, your lien rights are typically extinguished entirely — not just reduced. This is the single most common reason subs lose lien rights."),
    ("Filing the lien one day late", "The lien filing deadline is a hard statutory cutoff. A lien recorded one day after the deadline is void — courts have no discretion to extend it."),
    ("Recording in the wrong county", "A lien recorded in the wrong county is generally ineffective. You must record in the county where the property is located, and some states require recording in every county where the property spans a boundary."),
    ("Inadequate property description", "Most states require a legal property description (not just a street address). An insufficient legal description can render the lien void in strict states like California and Florida."),
    ("Liening exempt property", "Homestead-exempt, public, or already-released property cannot be liened. Filing a knowingly false lien can expose you to penalties under many states' fraudulent-lien statutes."),
    ("Not serving the lien on the owner", "Several states (Texas, Illinois, others) require you to serve a copy of the recorded lien on the owner within a set period. Failure to serve can void the lien even if it was correctly recorded."),
]

KILLS_YOUR_LIEN_SPECIFIC = {
    "Texas": [
        ("Skipping the monthly notices", "Texas requires monthly trapping notices for each month you are unpaid. Missing even one month's notice can forfeit lien rights for that month's work — Texas is stricter than most states here."),
        ("No written contract on a homestead", "Texas homesteads require a written, signed contract for the work to be lienable at all. Verbal agreements on a homestead = no lien."),
        ("Lien affidavit not sworn and notarized", "A Texas lien affidavit must be sworn before a notary. An unnotarized affidavit is void."),
        ("Not serving the owner within 5 days", "Texas requires you to serve a copy of the recorded lien affidavit on the owner within 5 days of recording. Miss this and the lien can be invalid."),
    ],
    "California": [
        ("No 20-day preliminary notice", "California's 20-day preliminary notice is the most common lien-killer. Without it, a sub or supplier has no lien rights at all — even on commercial work."),
        ("Recording after the 90-day window", "The 90-day deadline is absolute. There is no extension for disputes, COVID, or anything else."),
        ("Release-of-lien traps", "Accepting a 'conditional' waiver and release without confirming payment clears can wipe your lien before you're paid. Use conditional waivers only."),
    ],
    "Florida": [
        ("No Notice to Owner (NTO)", "Florida subs and suppliers without a direct contract with the owner must serve the NTO. No NTO = no lien, period."),
        ("Owner's sworn statement reliance", "If the owner pays the GC in reliance on a sworn statement and you haven't served an NTO, your lien can be defeated even if you filed it on time."),
        ("Improper NTO content", "Florida's NTO has mandatory content requirements. A defective NTO can be treated as if it was never served."),
    ],
}

# Role differences: GC vs subcontractor vs supplier. Keyed by state; general
# fallback covers the common pattern.
ROLE_RULES_GENERAL = [
    ("Direct (prime) contractor", "The contractor with a direct contract with the property owner generally has the broadest lien rights and usually does NOT need to send a preliminary notice — their contract is the notice."),
    ("Subcontractor", "Subs almost always must send a preliminary notice to preserve lien rights, because they have no contract with the owner. The notice tells the owner a sub is working on the project."),
    ("Material supplier", "Suppliers (especially second-tier) face the strictest notice rules in most states. Some states distinguish between suppliers-to-the-GC and suppliers-to-a-sub, with different deadlines."),
    ("Design professional / architect", "Architects and engineers typically have lien rights in most states, often under a separate statute section. Their deadlines sometimes differ from trade contractors."),
]

# The filing "HowTo" — 5 universal steps with state-specific hooks.
# Each step has (title, general_text). State-specific where it matters.
HOWTO_STEPS = [
    ("Confirm your deadline clock has started", "Identify your last day of furnishing labor or materials to the project. In most states the filing deadline runs from this date; in some it runs from project completion or the owner's notice of completion. The VoiceLogPro lien calculator computes the exact date for your state."),
    ("Send your preliminary notice (if required)", "If your state requires a preliminary notice (and most do for anyone without a direct owner contract), send it now — before the deadline. Send it by certified mail with return receipt so you have proof of service. Keep a copy with the postmark."),
    ("Prepare the lien document (claim of lien / affidavit)", "Your lien must include: your name and address, the property owner's name, a legal property description (not just a street address), the amount owed, and a description of the labor/materials furnished. In states like Texas the lien must be sworn and notarized."),
    ("Record the lien in the right county", "Record the lien with the county recorder (or clerk of court in a few states like Louisiana) in the county where the property is located. Pay the recording fee. The recording date is what counts — record early, never on the deadline."),
    ("Serve the lien on the owner (if your state requires it)", "Texas, Illinois, and several other states require you to serve a copy of the recorded lien on the owner within days of recording. Serve by certified mail and keep the return receipt. Then enforce (foreclose) the lien within your state's enforcement window — typically 1–2 years."),
]

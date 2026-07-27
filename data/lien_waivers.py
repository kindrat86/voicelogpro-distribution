"""Lien-waiver rules by state — conditional vs unconditional, statutory forms,
and what a subcontractor must know before signing.

Each state has different waiver rules. Some require statutory forms (CA, TX,
AZ, GA, FL, MA, MI, MS, NV, UT, WY), some don't (but enforce consensual waivers
through the contract). The distinction between conditional vs unconditional
waivers is universal — but several states void unconditional waivers unless
actually paid. This is exactly what every sub googling 'lien waiver [state]'
needs to know. Sourced from each state's lien statute.

HONESTY NOTE: lien-waiver law is volatile. These are the established rules
as of the source dates. Always check with a construction attorney. The data
is CC BY 4.0 — free to cite, update, and redistribute.
"""

# Statutory form states: these states mandate specific waiver form language.
# Using a non-statutory form in these states may be void.
STATUTORY_FORM_STATES = {
    "California": {
        "rule": "Statutory forms required",
        "detail": "California Civil Code § 8132-8138 mandates the exact text for four waiver types. Any non-conforming waiver is void. The waiver MUST be conditional to be effective before payment clears.",
        "waiver_types": [
            "Conditional Waiver and Release on Progress Payment",
            "Unconditional Waiver and Release on Progress Payment",
            "Conditional Waiver and Release on Final Payment",
            "Unconditional Waiver and Release on Final Payment",
        ],
        "trap": "Signing an unconditional waiver before the check clears waives your lien for work you haven't been paid for. Only sign the conditional form until the check clears.",
        "statute": "Cal. Civ. Code §§ 8132–8138",
    },
    "Texas": {
        "rule": "Statutory forms required",
        "detail": "Texas Property Code § 53.284 mandates the exact waiver form. Conditional waivers are binding only if the check clears; unconditional waivers are binding immediately on signing.",
        "waiver_types": [
            "Conditional Waiver and Release on Progress Payment",
            "Unconditional Waiver and Release on Progress Payment",
            "Conditional Waiver and Release on Final Payment",
            "Unconditional Waiver and Release on Final Payment",
        ],
        "trap": "Texas courts interpret unconditional waivers literally — even if you haven't been paid. The conditional form is your protection. Also, Texas requires the lien affidavit to be notarized.",
        "statute": "Tex. Prop. Code § 53.284",
    },
    "Florida": {
        "rule": "Statutory forms required",
        "detail": "Florida Statute § 713.20 sets the form. An unconditional waiver signed before actual payment may be enforceable in Florida courts — don't sign one until the check clears.",
        "waiver_types": [
            "Waiver of Right to Claim Against the Payment Bond (Progress Payment)",
            "Waiver of Right to Claim Against the Payment Bond (Final Payment)",
            "Waiver and Release of Lien Upon Progress Payment",
            "Waiver and Release of Lien Upon Final Payment",
        ],
        "trap": "Florida distinguishes between a 'waiver' (which is unconditional) and a 'release' (which reflects payment). Be precise about which one you sign.",
        "statute": "Fla. Stat. § 713.20",
    },
    "Arizona": {
        "rule": "Statutory forms required",
        "detail": "Arizona Revised Statutes § 33-1008. Progress payment waivers are conditional; final waivers can be unconditional. The unconditional final waiver immediately releases lien rights.",
        "waiver_types": [
            "Conditional Waiver and Release on Progress Payment",
            "Unconditional Waiver and Release on Progress Payment",
            "Conditional Waiver and Release on Final Payment",
            "Unconditional Waiver and Release on Final Payment",
        ],
        "trap": "Arizona's unconditional final waiver is a one-way street. Once signed, you cannot reinstate lien rights for any work prior to the waiver date.",
        "statute": "Ariz. Rev. Stat. § 33-1008",
    },
    "Georgia": {
        "rule": "Statutory forms required",
        "detail": "Georgia Code § 44-14-366 mandates the waiver form. The interim (progress-payment) waiver is conditional; the final waiver can be unconditional.",
        "waiver_types": [
            "Interim Waiver and Release Upon Payment",
            "Unconditional Waiver and Release Upon Final Payment",
            "Affidavit of Nonpayment (to annul a waiver if the check bounces)",
        ],
        "trap": "Georgia's affidavit of nonpayment gives you a limited window to undo a waiver if the check bounces — but the window is tight and the process is specific.",
        "statute": "Ga. Code Ann. § 44-14-366",
    },
    "Massachusetts": {
        "rule": "Statutory forms required",
        "detail": "Massachusetts General Laws ch. 254, § 29-32. Contractors on a direct contract with the owner can be required to execute partial waivers; statutory form protects both sides.",
        "waiver_types": [
            "Partial Waiver and Subordination of Lien",
            "Final Waiver of Lien",
        ],
        "trap": "MA allows subcontractors to subordinate their lien rather than waive it outright — a useful tool for getting partial payment without losing lien priority.",
        "statute": "Mass. Gen. Laws ch. 254, §§ 29-32",
    },
    "Michigan": {
        "rule": "Statutory forms required",
        "detail": "Michigan Compiled Laws § 570.1115 sets the waiver form. Unconditional waivers signed without payment are not enforceable — but don't rely on that alone; the dispute is expensive.",
        "waiver_types": [
            "Partial Conditional Waiver",
            "Partial Unconditional Waiver",
            "Full Conditional Waiver",
            "Full Unconditional Waiver",
        ],
        "trap": "Even though Michigan courts may void an unconditional waiver if you can prove nonpayment, you don't want to litigate it. Sign conditional waivers until the check clears.",
        "statute": "Mich. Comp. Laws § 570.1115",
    },
    "Mississippi": {
        "rule": "Statutory forms required",
        "detail": "Mississippi Code § 85-7-501 sets the statutory forms. Waivers and releases are governed by the contract terms so long as they use the statutory form.",
        "waiver_types": [
            "Interim Waiver and Release",
            "Final Waiver and Release",
        ],
        "trap": "The waiver language is embedded in the statute and must be followed exactly. Generic waivers may be challenged.",
        "statute": "Miss. Code Ann. § 85-7-501",
    },
    "Nevada": {
        "rule": "Statutory forms required",
        "detail": "Nevada Revised Statutes § 108.2457 mandates the waiver form. Both conditional and unconditional waiver types are specified by statute.",
        "waiver_types": [
            "Conditional Waiver and Release Upon Progress Payment",
            "Unconditional Waiver and Release Upon Progress Payment",
            "Conditional Waiver and Release Upon Final Payment",
            "Unconditional Waiver and Release Upon Final Payment",
        ],
        "trap": "Nevada permits lien claimants to file a 'waiver and release' electronically in some counties. Check local rules.",
        "statute": "Nev. Rev. Stat. § 108.2457",
    },
    "Utah": {
        "rule": "Statutory forms required",
        "detail": "Utah Code § 38-1a-802 sets the statutory forms. Utah has a pre-lien notice regime separate from the waiver forms.",
        "waiver_types": [
            "Conditional Waiver and Release Upon Progress Payment",
            "Unconditional Waiver and Release Upon Progress Payment",
            "Conditional Waiver and Release Upon Final Payment",
            "Unconditional Waiver and Release Upon Final Payment",
        ],
        "trap": "Utah's notice requirements (preliminary and notice of completion) run on a separate clock from the waiver rules. Don't confuse them.",
        "statute": "Utah Code § 38-1a-802",
    },
    "Wyoming": {
        "rule": "Statutory forms required",
        "detail": "Wyoming Statutes § 29-1-311 mandates the waiver form. The statute provides explicit language for three waiver types.",
        "waiver_types": [
            "Partial (Interim) Conditional Waiver and Release",
            "Partial (Interim) Unconditional Waiver and Release",
            "Final Unconditional Waiver and Release",
        ],
        "trap": "Wyoming is one of the few states where a lien can attach to severed minerals and timber — and the waiver rules follow that. The scope is broader than most states.",
        "statute": "Wyo. Stat. § 29-1-311",
    },
}

# Non-statutory states — apply a uniform best-practice template.
NONSTAT_STATE_RULE = {
    "rule": "No statutory form — contract governs (common law + contract defenses)",
    "detail": "This state does not mandate a statutory lien-waiver form. Instead, lien waivers are governed by general contract law. A signed, unambiguous waiver is typically enforceable — and an unconditional waiver signed before payment can extinguish lien rights even without a statute. Treat every waiver as binding and review it with counsel.",
    "waiver_types": [
        "Conditional Waiver and Release (Progress Payment)",
        "Unconditional Waiver and Release (Progress Payment)",
        "Conditional Waiver and Release (Final Payment)",
        "Unconditional Waiver and Release (Final Payment)",
    ],
    "trap": "Without a statutory form, the GC or owner can draft waivers that overreach — e.g., waiving retainage, change orders, or delay claims not yet submitted. Read every waiver yourself and never sign an unconditional waiver before the check clears.",
    "statute": "No specific statutory form provision",
}

UNIVERSAL_RULES = """Every state follows the same fundamental distinction:

- **Conditional waiver** — your lien rights are waived ONLY IF the payment actually clears. If the check bounces, the waiver is undone. This is what you should always sign until you have confirmed funds.

- **Unconditional waiver** — your lien rights are waived immediately on signing, regardless of whether you are ever paid. Never sign one unless you have confirmed cleared funds in your account. In many states, signing an unconditional waiver is treated as a binding admission that you have been paid — even if the check is still in your hand.

- **Partial (progress) waivers** — waive lien rights for a specific payment period or amount only. Future work and retainage are not waived.

- **Final waivers** — waive all remaining lien rights. Sign only when the job is done and all monies are confirmed."""
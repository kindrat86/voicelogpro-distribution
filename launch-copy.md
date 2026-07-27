# Launch copy — human-touch distribution

These need a human-voiced account (yours). I can't post them autonomously, but they're written and ready to paste. Ordered by expected ROI.

Lead with the **free, useful thing** (the open dataset + calculator), not the product. The dataset is what earns trust and backlinks; the tool is the soft CTA. This is the same posture that worked for the SanctionsAI launch.

---

## 1. Hacker News — "Show HN"

**Title (≤80 chars):**
```
Show HN: Open mechanics-lien deadlines for all 50 US states (CC BY 4.0)
```

**Body:**
```
I open-sourced the preliminary-notice, filing, and enforcement deadlines for
mechanics liens in all 50 US states + DC, each linked to the state statute that
sets it. CC BY 4.0, machine-readable (JSON/CSV/JSONL).

These three dates decide whether a subcontractor can get paid or file a lien,
and they currently live scattered across 51 different .gov PDFs that are slow
to parse and easy to mis-transcribe. This is one canonical, statute-cited copy.

- Dataset: https://github.com/kindrat86/us-mechanics-lien-deadlines
- Browse: https://lienes.voicelogpro.com/lien-law-deadlines/

It powers a free lien-deadline calculator (enter your last day on site + state,
get every date you must hit): https://voicelogpro.com/free/lien-deadline-calculator

Verbatim discipline: rows that don't parse cleanly from the statute source are
left as "Not specified" rather than guessed. Lawyer-reviewed, not legal advice.

Happy to answer questions on the data sourcing or the build.
```

---

## 2. Reddit — r/ConstructionManagers, r/Construction, r/electricians, r/plumbing

**Title:**
```
I built a free open dataset of mechanics-lien deadlines for all 50 states — statute-cited, CC BY 4.0
```

**Body:**
```
Tired of hunting down lien deadlines every time a GC shorts a pay app, I
compiled the preliminary-notice, filing, and enforcement deadlines for all 50
states + DC into one open dataset. Every deadline links to the state statute.

- Browse by state: https://lienes.voicelogpro.com/lien-law-deadlines/
- Free calculator (last day on site + state → every deadline with exact dates):
  https://voicelogpro.com/free/lien-deadline-calculator
- Raw data (JSON/CSV): https://github.com/kindrat86/us-mechanics-lien-deadlines

CC BY 4.0 — free to use commercially, just attribute. Verbatim from the
statutes; rows I couldn't verify are marked "Not specified," not guessed.

Not legal advice — verify with a construction attorney in your state. But it
should save you the 20-minute statute hunt on your next pay-app fight.

(Background: I also built VoiceLogPro, a voice-to-PDF daily-log app, because the
evidence that wins these disputes is a contemporaneous, timestamped daily log.
But the dataset + calculator are free regardless.)
```

**Comment to your own post (first reply):**
```
If your state shows "Not specified" for any row, drop a link to the statute in
the comments and I'll get it added in the next weekly sync.
```

---

## 3. Listicle outreach (email/pitch — personalize per site)

These 8 sites currently rank for "best construction daily report app" and none
list VoiceLogPro. Offer to be added; the open dataset is the credibility hook.

**Template (personalize the first line):**
```
Subject: A free, citable addition for your construction reporting roundup?

Hi [name],

I read your [article title] — really useful breakdown. I wanted to flag
something that might fit a future update.

I just open-sourced the mechanics-lien deadlines (preliminary notice, filing,
enforcement) for all 50 US states + DC, each statute-cited and CC BY 4.0. It's
the kind of thing that pairs naturally with a daily-report roundup, because the
daily log is exactly the evidence that anchors those deadlines:

  https://lienes.voicelogpro.com/lien-law-deadlines/
  https://github.com/kindrat86/us-mechanics-lien-deadlines

I also built VoiceLogPro — a voice-to-PDF daily-log app for subcontractors
(speak your report on site → timestamped court-ready PDF). If it's a fit for the
list, I'd be glad to provide screenshots, a demo, or a free Crew account for
your review. If not, no worries — the dataset is free to cite either way.

Thanks for the roundup,
[Maryan]
```

**Target sites (rank for "best construction daily report app 2026"):**
- ingenious.build
- fluix.io
- smartbarrel.io
- crewconsole.com
- kynection.com
- rakenapp.com
- fieldwire.com
- procore.com/library

---

## 4. Embed asks (the compounding backlink channel)

Identify 20-30 relevant sites and offer the free embed at
`https://lienes.voicelogpro.com/embed/`. Each embed = one contextual backlink
from a topically-relevant domain.

**Best-fit targets to find:**
- Construction-law firm blogs (search: "mechanics lien" + state name)
- Estimator / takeoff SaaS resource pages
- Trade-association resource pages (ABC, AGC, NAHB chapters)
- County building-department "contractor resources" pages
- Construction-accounting / pay-app blogs

**One-line outreach:**
```
Hi [name] — I maintain the open 50-state mechanics-lien dataset
(github.com/kindrat86/us-mechanics-lien-deadlines). There's a free one-tag
embed widget that shows live lien deadlines for any state on your resources
page — would it be useful here? https://lienes.voicelogpro.com/embed/
```

---

## 5. Optional: Hugging Face / Kaggle mirror

When you have 5 minutes, create an HF Dataset (or Kaggle dataset) and upload
`data/mechanics-lien-deadlines.csv`. Those domains pass heavy authority and rank
for "mechanics lien deadlines dataset." If you paste me an HF User Access Token
(write scope), I can do the mirror for you.

# VoiceLogPro Distribution Kit

What I built, why it moves organic traffic, and exactly what's left (one DNS record + the human-touch launches). Two plays, both shipped and live.

This mirrors the proven `ofac-sdn-json` → SanctionsAI pattern and the `carshake-distribution` engine, applied to VoiceLogPro's strongest latent asset: a **legally-vetted 50-state mechanics-lien dataset** that was sitting inside the app with nobody citing it.

---

## The diagnosis (why this, not more pages)

VoiceLogPro is **content-saturated but authority-starved**:

| Signal | Finding |
|---|---|
| Indexed pages | **220** (50 state pages, ~30 comparison pages, templates, glossary, how-tos) |
| Brand search | `"VoiceLogPro"` → **zero** dedicated results |
| Category SERPs | "best construction daily report app 2026" — absent from all 8 listicles (Raken/Fieldwire/Procore own it) |
| Backlink engine | `kindrat86/voicelogpro` was a code dump, not a citable artifact |
| Hidden asset | A statute-cited 51-state lien dataset served at `/lien-law-deadlines/data.json` that **nobody knew existed** |

**More pages = zero marginal lift.** The bottleneck is domain authority, which is bought with backlinks, which are earned by being the **canonical source of record** for something people must cite. The lien dataset is that thing.

---

## What shipped (both live)

### Play 1 — Open-data backlink engine ⭐
**Live:** https://github.com/kindrat86/us-mechanics-lien-deadlines

A standalone repo that is *just* the clean dataset — the thing every construction lawyer, estimator, and devtool has to link to. This is the `ofac-sdn-json` play that made SanctionsAI rank.

- **51 jurisdictions** (50 states + DC), statute-cited, CC BY 4.0
- Canonical JSON + CSV + JSONL + minified JSON
- 51 per-state Markdown pages with deadlines, statute citation, source URL
- `build.py` regenerates everything from the verbatim source (VERBATIM discipline — missing rows render as "Not specified," never guessed)
- Weekly auto-sync GitHub Action (`.github/workflows/sync.yml`) re-pulls the upstream dataset and commits deltas
- Topics + homepage set for discoverability

### Play 2 — Distribution hub (the SEO surface)
**Live:** https://voicelogpro-guide.vercel.app → (pending DNS) **lienes.voicelogpro.com**

Same isolated-subdomain pattern as `carshake-guide` / `sanctionsai-distribution`: content lives where it's cited (canonical → hub), CTAs point at the apex app.

**What it builds (119 files):**

| Surface | Count | Example query it wins |
|---|---|---|
| State lien pages | 51 | "mechanics lien deadlines Texas" |
| All-states hub | 1 | "mechanics lien deadlines by state" |
| Embed widget + demo | 2 | (link-earning — see below) |
| Open data (JSON/CSV/JSONL) | 3 | "mechanics lien dataset" |
| OG social cards | 53 | (per-state, informative in preview) |
| SEO files | 9 | sitemap, sitemap-index, robots, llms.txt, RSS, favicon, IndexNow key+payload |

Each state page ships with:
- **3 JSON-LD blocks** — `Dataset` + `FAQPage` + `BreadcrumbList` (rich-result eligible)
- Deadline box (preliminary notice / filing / enforcement), statute citation + source link
- Adjacent-state internal links (topical clustering)
- Download links (JSON/CSV/JSONL) + GitHub
- Embed snippet generator → **the backlink mechanism**: third parties paste one `<script>` tag, get a live state lien card, and link to the canonical source
- CTA → `voicelogpro.com/lien-law-deadlines/<state>` (the apex app)

**AI-search opted-in:** `robots.txt` allows GPTBot, ClaudeBot, PerplexityBot, Google-Extended, OAI-SearchBot; `llms.txt` documents the dataset for LLM extraction; every page has `Dataset` schema so AI engines treat it as citable data.

**IndexNow:** Bing + Yandex pinged (both 202 ✓) for all 54 URLs at deploy.

---

## Architecture decisions

- **Canonical → content host, CTA → apex app.** Canonicals point at the hub (where the content lives); "daily-log" CTAs point at `voicelogpro.com`. A mismatch here would bleed ranking.
- **Isolated subdomain, not the apex.** Zero risk to the live app on `voicelogpro.com`.
- **VERBATIM-only data discipline.** The source script skips rows it can't parse cleanly rather than guessing — 18 states have all 3 sections, the rest have partials rendered honestly as "Not specified." Wrong legal data is worse than missing data.
- **SVG OG cards** over raster: tiny, crisp, scriptable, and informative in social/AI previews (each card carries the state's actual deadlines).
- **Reproducible from the live app.** Both the repo and the hub rebuild from `voicelogpro.com/lien-law-deadlines/data.json` — one source of truth, updated weekly by the GitHub Action.

---

## What's left (the human-touch part)

These need a human-voiced account or outbound access; I prepped the assets but can't publish autonomously.

### 1. ONE DNS record (unlocks the custom domain)
Point `lienes.voicelogpro.com` at Vercel, then re-run `./ship.sh`. It auto-detects the resolution and switches all canonicals/OG URLs from `*.vercel.app` to `lienes.voicelogpro.com`. Get the CNAME/A target from the Vercel project → Settings → Domains.

### 2. Google Search Console
- Add both `voicelogpro-guide.vercel.app` (now) and `lienes.voicelogpro.com` (after DNS)
- Submit `https://<hub>/sitemap.xml`
- Optional: set `GSC_VERIFICATION` env var before `./ship.sh` to inject the verification meta tag

### 3. Listicle / community launches (highest-ROI outreach)
VoiceLogPro is absent from every "best construction daily report app" list. The fastest authority wins:
- **Reddit** (r/Construction, r/ConstructionManagers, r/electricians, r/plumbing) — the lien dataset is genuinely useful to these communities; lead with the free calculator and open data, not a sales pitch
- **HN "Show HN"** — "Show HN: Open mechanics-lien deadlines for all 50 US states (CC BY 4.0)" plays well; lead with the dataset, mention the tool
- **Listicle pitch** to the 8 sites currently ranking for "best construction daily report app" — offer to be added; the open dataset + calculator is the credibility hook

### 4. Outbound embed asks (the compounding backlink engine)
The widget at `/embed/` is the link-earning mechanism. Identify 20-30 relevant sites (estimator SaaS, construction-law firm blogs, trade-association resource pages, county building-department sites) and offer the free embed. Each embed = one authoritative, topically-relevant backlink. This is the slowest but highest-compounding channel — it's how `ofac-sdn-json` became the default reference.

---

## Rebuild / extend

```bash
# regenerate the hub from the live dataset and redeploy
./ship.sh

# or just rebuild locally + preview
python3 build.py && python3 preview.py   # → http://localhost:8801

# regenerate the open-data repo artifacts
cd ../us-mechanics-lien-deadlines && python3 build.py   # (in the repo clone)
```

Both rebuild from `voicelogpro.com/lien-law-deadlines/data.json`, so they stay in sync with the app's legal review automatically. Add a state's statute citation to the source and every artifact (repo JSON, hub page, widget data, OG card, sitemap) updates on the next build.

---

## Live URLs

- **Open-data repo:** https://github.com/kindrat86/us-mechanics-lien-deadlines
- **Distribution hub:** https://voicelogpro-guide.vercel.app
- **Hub sitemap:** https://voicelogpro-guide.vercel.app/sitemap.xml
- **Hub llms.txt:** https://voicelogpro-guide.vercel.app/llms.txt
- **Embed widget demo:** https://voicelogpro-guide.vercel.app/embed/
- **Sample state page:** https://voicelogpro-guide.vercel.app/lien-law-deadlines/texas/
- **Raw dataset (citable):** https://raw.githubusercontent.com/kindrat86/us-mechanics-lien-deadlines/main/data/mechanics-lien-deadlines.json

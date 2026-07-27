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

**What it builds (3,303 pages, 119+ files):**

| Surface | Count | Example query it wins |
|---|---|---|
| State lien pages | 51 | "mechanics lien deadlines Texas" |
| County recorder pages | 3,197 | "file a mechanics lien in Harris County TX" |
| Lien-waiver pages | 52 | "Texas lien waiver rules subcontractors" |
| All-states hub | 1 | "mechanics lien deadlines by state" |
| All-counties hub | 1 | "where to file a mechanics lien by county" |
| All-waivers hub | 1 | "lien waiver rules by state" |
| Embed widget + demo | 2 | (link-earning — see below) |
| Open data (JSON/CSV/JSONL) | 3 | "mechanics lien dataset" |
| OG social cards | 53 | (per-state, informative in preview) |
| SEO files | 9 | 4 sitemaps + sitemap-index + robots + llms.txt + RSS + favicon + IndexNow |

Each state page ships with:
- **3 JSON-LD blocks** — `Dataset` + `FAQPage` + `BreadcrumbList` (rich-result eligible)
- Deadline box (preliminary notice / filing / enforcement), statute citation + source link
- Adjacent-state internal links (topical clustering)
- Download links (JSON/CSV/JSONL) + GitHub
- Embed snippet generator → **the backlink mechanism**: third parties paste one `<script>` tag, get a live state lien card, and link to the canonical source
- CTA → `voicelogpro.com/lien-law-deadlines/<state>` (the apex app)

Each county page has:
- County recorder office type (Clerk, Register of Deeds, etc.)
- Estimated recording-fee range
- Cross-reference to the state's lien deadline
- `FAQPage` + `BreadcrumbList` JSON-LD
- CTA → the apex lien calculator

**AI-search opted-in:** `robots.txt` allows GPTBot, ClaudeBot, PerplexityBot, Google-Extended, OAI-SearchBot; `llms.txt` documents the dataset for LLM extraction; every page has `Dataset` schema so AI engines treat it as citable data.

**Self-maintaining CI pipeline:**
- `kindrat86/voicelogpro-distribution` has a Vercel Git integration — pushes to `main` = auto-deploy to `voicelogpro-guide.vercel.app`
- `.github/workflows/refresh-data.yml` runs weekly (Monday 09:00 UTC) + on demand
- The Action: fetches the live lien dataset from `voicelogpro.com` → rebuilds `dist/` → commits changes → pushes → Vercel auto-deploys
- Both repo and hub rebuild from `voicelogpro.com/lien-law-deadlines/data.json` — one source of truth

---

## Architecture decisions

- **Canonical → content host, CTA → apex app.** Canonicals point at the hub (where the content lives); "daily-log" CTAs point at `voicelogpro.com`. A mismatch here would bleed ranking.
- **Isolated subdomain, not the apex.** Zero risk to the live app on `voicelogpro.com`.
- **VERBATIM-only data discipline.** The source script skips rows it can't parse cleanly rather than guessing — 18 states have all 3 sections, the rest have partials rendered honestly as "Not specified." Wrong legal data is worse than missing data.
- **SVG OG cards** over raster: tiny, crisp, scriptable, and informative in social/AI previews (each card carries the state's actual deadlines).
- **Reproducible from the live app.** Both the repo and the hub rebuild from `voicelogpro.com/lien-law-deadlines/data.json` — one source of truth, updated weekly by the GitHub Action.

---

## What's left (the human-touch part)

### 1. ONE DNS record (unlocks the custom domain)
The domain `lienes.voicelogpro.com` is already added to the Vercel project and pending DNS. Add this Cloudflare A record to make it live:

```
Type:  A
Name:  lienes
Value: 76.76.21.21
```

Once DNS propagates (~5 min on Cloudflare), run `./ship.sh` — it auto-detects the resolution and switches all canonicals, OG URLs, and sitemap references from `voicelogpro-guide.vercel.app` to `lienes.voicelogpro.com`. Vercel will issue an SSL cert automatically.

### 2. Google Search Console
- Add `voicelogpro-guide.vercel.app` (now) and `lienes.voicelogpro.com` (after DNS)
- Submit `https://<hub>/sitemap-index.xml` — it references 4 sitemaps (root, state, county, waiver) covering all 3,303 pages
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
- **Distribution kit repo:** https://github.com/kindrat86/voicelogpro-distribution
- **Hub sitemap index:** https://voicelogpro-guide.vercel.app/sitemap-index.xml
- **Hub llms.txt:** https://voicelogpro-guide.vercel.app/llms.txt
- **Embed widget demo:** https://voicelogpro-guide.vercel.app/embed/
- **Sample state page:** https://voicelogpro-guide.vercel.app/lien-law-deadlines/texas/
- **Sample county page:** https://voicelogpro-guide.vercel.app/counties/texas/harris-county/
- **Sample waiver page:** https://voicelogpro-guide.vercel.app/lien-waivers/texas/
- **Raw dataset (citable):** https://raw.githubusercontent.com/kindrat86/us-mechanics-lien-deadlines/main/data/mechanics-lien-deadlines.json

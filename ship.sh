#!/usr/bin/env bash
# ship.sh — rebuild, deploy to Vercel (voicelogpro-guide), and re-ping IndexNow.
#
# Mirrors the carshake-guide ship.sh pattern. Detects whether the custom
# subdomain lienes.voicelogpro.com resolves and switches canonicals accordingly,
# so it works both before and after DNS lands.
#
# Usage: ./ship.sh
set -euo pipefail
cd "$(dirname "$0")"

PROJECT="voicelogpro-guide"
DESIRED_DOMAIN="lienes.voicelogpro.com"

# Pick canonical base: prefer the custom domain once DNS resolves.
if dig +short "$DESIRED_DOMAIN" A 2>/dev/null | grep -q . ; then
  echo "✓ $DESIRED_DOMAIN resolves — canonicals will point at it."
  export VOICELOGPRO_BASE_URL="https://$DESIRED_DOMAIN"
  BASE="https://$DESIRED_DOMAIN"
else
  echo "⚠ $DESIRED_DOMAIN does not resolve yet — canonicals → $PROJECT.vercel.app"
  export VOICELOGPRO_BASE_URL="https://$PROJECT.vercel.app"
  BASE="https://$PROJECT.vercel.app"
fi

echo "→ Rebuilding site…"
rm -rf dist
python3 build.py

echo "Deploying to /tmp/$PROJECT ..."
rm -rf "/tmp/$PROJECT"
mkdir -p "/tmp/$PROJECT/site"
cp -r dist/site/* "/tmp/$PROJECT/site/"
# Write a deploy-local vercel.json so outputDirectory points at the right place.
cat > "/tmp/$PROJECT/vercel.json" <<'VCJSON'
{
  "outputDirectory": "site",
  "cleanUrls": true,
  "trailingSlash": true,
  "headers": [
    { "source": "/(.*)", "headers": [
      { "key": "X-Content-Type-Options", "value": "nosniff" },
      { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" },
      { "key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=(), payment=()" }
    ]},
    { "source": "/og/(.*).svg", "headers": [
      { "key": "Content-Type", "value": "image/svg+xml" },
      { "key": "Cache-Control", "value": "public, max-age=86400, s-maxage=604800" }
    ]},
    { "source": "/data/(.*).json", "headers": [
      { "key": "Content-Type", "value": "application/json" },
      { "key": "Cache-Control", "value": "public, max-age=3600" }
    ]}
  ]
}
VCJSON
cd "/tmp/$PROJECT"

echo "→ Ensuring Vercel project exists…"
# link or create the project (idempotent)
if ! vercel link --yes --project "$PROJECT" 2>/dev/null; then
  vercel project add "$PROJECT" >/dev/null 2>&1 || true
  vercel link --yes --project "$PROJECT" 2>/dev/null || true
fi

echo "→ Deploying to production…"
vercel deploy --prod --yes

echo "→ Pinging IndexNow (Bing + Yandex)…"
PAYLOAD=$(python3 -c "import json;print(json.dumps({k:v for k,v in json.load(open('site/indexnow-urls.json')).items() if k in ('host','key','keyLocation','urlList')}))")
curl -s -X POST "https://api.indexnow.org/indexnow" \
  -H "Content-Type: application/json" -d "$PAYLOAD" -w "  Bing: %{http_code}\n" || true
curl -s -X POST "https://yandex.com/indexnow" \
  -H "Content-Type: application/json" -d "$PAYLOAD" -w "  Yandex: %{http_code}\n" || true

echo
echo "✓ Done. Live at: $BASE"
echo "  Sitemap: $BASE/sitemap.xml"
echo "  llms.txt: $BASE/llms.txt"
echo "  Submit to GSC: https://search.google.com/search-console"

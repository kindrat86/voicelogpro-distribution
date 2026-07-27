"""Generate IndexNow key + URL payload so we can ping Bing/Yandex the instant the
site deploys. Persisted key so the key file at /<key>.txt stays stable across
redeploys."""
import json
import os
import secrets
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "lib"))
sys.path.insert(0, os.path.join(HERE, "data"))
from common import SITE  # noqa: E402
from generate_states import RECORDS  # noqa: E402
from counties import COUNTIES  # noqa: E402

OUT = os.path.join(HERE, "dist", "site")

KEY_FILE = os.path.join(HERE, ".indexnow-key")
if os.path.exists(KEY_FILE):
    KEY = open(KEY_FILE).read().strip()
else:
    KEY = secrets.token_hex(16)
    with open(KEY_FILE, "w") as f:
        f.write(KEY)

# key file served at /<key>.txt — IndexNow validates ownership this way
with open(os.path.join(OUT, f"{KEY}.txt"), "w") as f:
    f.write(KEY)

urls = [f"{SITE}/", f"{SITE}/lien-law-deadlines/", f"{SITE}/embed/",
        f"{SITE}/counties/", f"{SITE}/lien-waivers/"]
urls += [f"{SITE}/lien-law-deadlines/{r['slug']}/" for r in RECORDS]
urls += [f"{SITE}/lien-waivers/{r['slug']}/" for r in RECORDS]
# county state hubs (deduped)
county_state_hubs = sorted(set(c["state_slug"] for c in COUNTIES))
urls += [f"{SITE}/counties/{ss}/" for ss in county_state_hubs]
urls += [f"{SITE}/counties/{c['state_slug']}/{c['slug']}/" for c in COUNTIES]

payload = {
    "host": SITE.replace("https://", "").replace("http://", "").rstrip("/"),
    "key": KEY,
    "keyLocation": f"{SITE}/{KEY}.txt",
    "urlList": urls,
}
with open(os.path.join(OUT, "indexnow-urls.json"), "w") as f:
    json.dump(payload, f, indent=2)

print(f"✓ IndexNow key {KEY[:8]}… + {len(urls)} URLs → {KEY}.txt + indexnow-urls.json")

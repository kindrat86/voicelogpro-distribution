#!/usr/bin/env python3
"""Run all generators in sequence to produce the VoiceLogPro distribution site."""
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))

STEPS = [
    ("State pages + hub",   ["python3", "lib/generate_states.py"]),
    ("OG social cards",     ["python3", "lib/generate_og.py"]),
    ("Embed widget",        ["python3", "lib/generate_embed.py"]),
    ("Home + SEO files",    ["python3", "lib/generate_home.py"]),
    ("IndexNow key + URLs", ["python3", "lib/generate_indexnow.py"]),
]

OK = 0; FAIL = 0
for label, cmd in STEPS:
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=HERE)
    if r.returncode == 0:
        print(r.stdout.strip())
        OK += 1
    else:
        print(f"  ✗ {label} FAILED")
        print(r.stderr[-1500:] or r.stdout[-1500:])
        FAIL += 1
print(f"\n{OK} ok, {FAIL} failed")
sys.exit(FAIL)

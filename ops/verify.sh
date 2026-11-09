#!/usr/bin/env bash
# ops/verify.sh: the repository's own gate. zops runs it before every push.
# © 1993–2026 Abhishek Choudhary. All rights reserved. AyeAI.
# SPDX-License-Identifier: GPL-3.0-or-later
# It refuses only on what a release needs (C39); everything else is reported. Nothing is written outside this folder.
set -uo pipefail
cd "$(dirname "$0")/.."
export PYTHONDONTWRITEBYTECODE=1
FAILED=0; REPORTED=0
trap 'rm -rf .verify-nb' EXIT
run(){ local name="$1"; shift; local out
  if out="$("$@" 2>&1)"; then printf '   ok        %s\n' "$name"
  else printf '   FAIL      %s\n' "$name"; printf '%s\n' "$out" | tail -8 | sed 's/^/             /'; FAILED=$((FAILED+1)); fi; }
report(){ local name="$1"; shift; local out
  if out="$("$@" 2>&1)"; then printf '   ok        %s\n' "$name"; [ -n "$out" ] && printf '%s\n' "$out" | tail -2 | sed 's/^/             /'
  else printf '   REPORTED  %s\n' "$name"; printf '%s\n' "$out" | tail -6 | sed 's/^/             /'; REPORTED=$((REPORTED+1)); fi; return 0; }
from_source(){ python3 tools/build_notebooks.py .verify-nb >/dev/null && for f in notebooks/*; do cmp -s "$f" ".verify-nb/$(basename "$f")" || { echo "differs from its source: $f"; return 1; }; done; }
notebooks_ok(){ python3 - <<'PY'
import ast, glob, json, re, sys
bad = []
for f in sorted(glob.glob("notebooks/*.ipynb")):
    nb = json.load(open(f, encoding="utf-8"))
    if nb.get("nbformat") != 4 or not all("id" in c for c in nb["cells"]): bad.append(f + ": not nbformat 4 with cell ids")
    for c in nb["cells"]:
        if c["cell_type"] == "code":
            src = "\n".join("pass" if re.match(r"\s*[!%]", l) else l for l in c["source"].splitlines())
            try: ast.parse(src)
            except SyntaxError as e: bad.append("%s: %s" % (f, e))
if bad: sys.exit("\n".join(bad))
PY
}
versions_agree(){ python3 - <<'PY'
import json, re, sys
a = re.search(r"(?m)^version:\s*['\"]?([^'\"\s]+)", open("CITATION.cff", encoding="utf-8").read()).group(1); b = json.load(open("misty.json", encoding="utf-8"))["version"]
if a != b: sys.exit("versions differ: CITATION.cff %s, misty.json %s" % (a, b))
PY
}
no_placeholder(){ ! grep -rIlE 'DOI-''PENDING|ZENODO-DOI-''PENDING|zenodo\.''NNN' --exclude-dir=.git . ; }
copyright_marked(){ local miss=0 f; for f in README.md CONCEPT.md CONTEXT.md AGENTS.md docs/index.html docs/ghonchu.js tools/*.py ops/*.sh notebooks/*.ipynb legal/TRADEMARKS.md origin/SEED-DIFF.md; do
  grep -q '1993.\{0,3\}2026 Abhishek Choudhary' "$f" || { echo "no copyright line: $f"; miss=1; }; done; return $miss; }
mark_ok(){ local h; h="$(grep -rIl 'AyeCNSe''®' --exclude-dir=.git --exclude-dir=origin . | grep -v '^\./legal/TRADEMARKS\.md$' || true)"; [ -z "$h" ] || { echo "$h"; return 1; }; }
affiliation_ok(){ ! grep -rIl 'Independent ''Researcher' --exclude-dir=.git --exclude-dir=origin . ; }
no_secrets(){ local h; h="$(grep -rIoE 'ghp_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{50,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----|AIza[0-9A-Za-z_-]{35}' --exclude-dir=.git . || true)"; [ -z "$h" ] || { echo "$h"; return 1; }; }
no_oversized(){ local b; b="$(find . -path ./.git -prune -o -type f -size +50M -print)"; [ -z "$b" ] || { echo "$b"; return 1; }; }
manifest_ok(){ [ ! -f MANIFEST.sha256 ] || sha256sum --quiet -c MANIFEST.sha256; }
em_dash(){ local h; h="$(grep -rIl $'\xe2\x80\x94' --exclude-dir=.git --exclude-dir=origin --exclude-dir=notebooks --exclude-dir=.verify-nb . || true)"; [ -z "$h" ] || { echo "em dashes in: $h"; return 1; }; }
echo "verify: ghonchu"
run "notebooks are generated from tools/build_notebooks.py" from_source
run "every notebook is nbformat 4 and every code cell parses" notebooks_ok
run "one version everywhere"                                 versions_agree
run "no DOI placeholder"                                     no_placeholder
run "copyright line on every authored file"                  copyright_marked
run "trade marks: AyeCNSe is marked TM, never R"             mark_ok
run "affiliation AyeAI only"                                 affiliation_ok
run "no secrets"                                             no_secrets
run "no file over 50 MB"                                     no_oversized
run "manifest verifies, when sealed"                         manifest_ok
report "no em dashes in authored files"                      em_dash
echo "   UNJUDGED  the notebooks are not run here; they run on Colab (initial drop)"
if [ "$FAILED" -eq 0 ]; then echo "verify: PASS ($REPORTED reported)"; else echo "verify: $FAILED check(s) failed"; exit 1; fi

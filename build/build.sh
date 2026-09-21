#!/bin/sh
set -e
cd "$(dirname "$0")"
python3 secteurs.py  > /dev/null
python3 groupes.py   > /dev/null
python3 company.py   > /dev/null
python3 assemble.py  | head -2
python3 patch_struct.py > /dev/null
python3 patch_config.py > /dev/null
python3 inject.py       > /dev/null
python3 patch_fixes.py  > /dev/null
python3 patch_levers.py
python3 patch_audit.py
python3 patch_final.py
python3 patch_brand.py
python3 patch_logo.py
python3 patch_logos.py
python3 patch_frise.py
python3 - <<'PY'
import re, pathlib
s = pathlib.Path("app.src.html").read_text(encoding="utf-8")
pathlib.Path("/tmp/app_check.js").write_text("\n;\n".join(re.findall(r"<script[^>]*>(.*?)</script>", s, re.S)), encoding="utf-8")
PY
node --check /tmp/app_check.js && echo "syntaxe JS ok"

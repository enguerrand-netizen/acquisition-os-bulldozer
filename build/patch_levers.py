# -*- coding: utf-8 -*-
"""Passe 5 — les six écrans de levier sur données réelles.
Les surcharges sont placées à la FIN du script : en JavaScript, la dernière
déclaration d'une fonction de même nom l'emporte. Placées avant, elles
seraient écrasées par celles de la maquette."""
import pathlib, re
P = pathlib.Path("app.src.html"); s = P.read_text(encoding="utf-8")
js = pathlib.Path("levers.js").read_text(encoding="utf-8")
css = """
.nb-b{border-left:3px solid var(--line-2);padding:2px 0 2px 14px}
.nb-b.warn{border-color:var(--orange)}
.nb-b b{display:block;font-family:var(--f-display);font-size:13px;letter-spacing:.04em;text-transform:uppercase;color:var(--muted);margin-bottom:4px}
.nb-b p{margin:0;color:var(--body)}
.nb-f{margin:0;font-size:13px;color:var(--faint);font-style:italic}
ul.res{margin:0;padding-left:18px;display:flex;flex-direction:column;gap:8px;color:var(--body);font-size:13.5px}
"""
assert "</style>" in s
s = s.replace("</style>", css + "</style>", 1)

# L'application entière est enveloppée dans une IIFE : placées hors de celle-ci,
# les surcharges ne verraient ni DATA ni accounts et n'écraseraient rien.
# On les insère juste avant l'amorçage, à l'intérieur de l'IIFE.
anc = "const h = location.hash.slice(1);"
assert anc in s, "amorçage introuvable"
i = s.index(anc)
s = s[:i] + js + "\n" + s[i:]
P.write_text(s, encoding="utf-8")
print(f"leviers injectés en fin de script · {len(s):,} caractères".replace(",", " "))

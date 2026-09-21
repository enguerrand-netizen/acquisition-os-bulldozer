# -*- coding: utf-8 -*-
"""Passe 9 — le vrai logo Bulldozer.
Le monogramme « BDZ » était un ersatz. On inline la marque officielle
(~/Downloads/assets/logo-bulldozer.svg, identique à celle des LP JobTeaser
et du front Bulldozer OS) : aplat lime #DDFF56, glyphe #1F2600."""
import pathlib, re, sys
P = pathlib.Path("app.src.html"); s = P.read_text(encoding="utf-8")
LOGO = pathlib.Path("/Users/enguerrandchalvondemersay/Downloads/assets/logo-bulldozer.svg").read_text(encoding="utf-8")
# on retire l'en-tête XML éventuel et on fixe la taille d'affichage
mark = re.sub(r"<\?xml[^>]*\?>", "", LOGO).strip()
mark = mark.replace('width="40" height="40"', 'width="34" height="34" class="bdzmark" aria-label="Bulldozer"', 1)
mark = re.sub(r"\s+", " ", mark)

old = '<div class="logo"><span class="mk">BDZ</span><div><b>Acquisition OS</b><span>30 grands comptes · CRM Bulldozer</span></div></div>'
if old not in s: print("  ÉCHEC   bloc logo"); sys.exit(1)
s = s.replace(old, '<div class="logo">' + mark + '<div><b>Acquisition OS</b><span>30 grands comptes · CRM Bulldozer</span></div></div>', 1)
print("  ok      marque officielle inlinée")

# le style du faux monogramme n'a plus d'objet
s = s.replace(".logo .mk{background:var(--lime);color:#000;font:700 20px/1 var(--f-display);border-radius:8px;padding:8px 8px 7px;letter-spacing:.02em}",
              ".logo .bdzmark{flex:none;display:block;border-radius:6px}", 1)
print("  ok      style du monogramme remplacé")
P.write_text(s, encoding="utf-8")

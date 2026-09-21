# -*- coding: utf-8 -*-
"""Passe 6 — finitions."""
import pathlib, sys, re
P = pathlib.Path("app.src.html"); s = P.read_text(encoding="utf-8"); n = 0
def sub(old, new, label, opt=False):
    global s, n
    if old not in s:
        print(("  (absent)" if opt else "  ÉCHEC  "), label)
        if not opt: sys.exit(1)
        return
    s = s.replace(old, new, 1); n += 1; print("  ok     ", label)

# 1. plus aucune image de la maquette : les vignettes retombent sur leur dégradé
sub("const CREA_IMG = {", "const CREA_IMG = {}; const CREA_IMG_OFF = {", "images de la maquette retirées")

# 2. texte du moteur : l'exercice fiscal n'est pas mesuré
sub("taille, secteur, historique, structure, exercice fiscal : faut-il y aller ?",
    "taille, secteur, historique, entités du groupe : faut-il y aller ? L'exercice fiscal figure dans le barème mais ne rapporte rien : le CRM ne le stocke pas.",
    "note du moteur")

# 3. séparateur décimal français sur la pression hors portefeuille
sub("X.part_hors_portefeuille + '<small> %</small>'",
    "String(X.part_hors_portefeuille).replace('.', ',') + '<small> %</small>'", "décimale française")

# 4. (retiré) l'ancien écran Content a été remplacé par la bibliothèque visuelle

# 5. badge Agents : nombre d'agents câblables, pas d'agents « en marche »
m = re.search(r"document\.getElementById\('bG'\)\.textContent = [^;]+;", s)
if m:
    s = s.replace(m.group(0), "document.getElementById('bG').textContent = (typeof AGENT_SRC === 'object' ? Object.values(AGENT_SRC).filter(x => x.etat === 'ok').length : 0) + '/' + Object.keys(AGENTS).length;")
    n += 1; print("  ok      badge Agents")
else:
    print("  (absent) badge Agents")

P.write_text(s, encoding="utf-8"); print(f"\n{n} finitions")

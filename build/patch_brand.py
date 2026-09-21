# -*- coding: utf-8 -*-
"""Passe 8 — charte Bulldozer, mode clair.
Fond clair, texte noir, structure noire (barre latérale et cartes de chiffres),
lime #DDFF56 en accent seul — jamais sous du texte. Pastels de la charte pour la
data viz, avec un filet noir pour qu'elles tiennent sur fond clair.
Pas d'ombre portée ni de dégradé : deux « à éviter » explicites de la charte."""
import pathlib, re, sys
P = pathlib.Path("app.src.html"); s = P.read_text(encoding="utf-8"); n = 0
def sub(old, new, label, count=1):
    global s, n
    if old not in s: print("  ÉCHEC  ", label); sys.exit(1)
    k = s.count(old) if count == -1 else count
    s = s.replace(old, new) if count == -1 else s.replace(old, new, count)
    n += 1; print("  ok      %-40s ×%d" % (label, k))

# ---------- 1. polices ----------
fonts = pathlib.Path("fonts-brand.css").read_text(encoding="utf-8")
sub('<link rel="preconnect" href="https://fonts.googleapis.com">\n', '', "preconnect retiré")
m = re.search(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]*>', s)
if not m: print("  ÉCHEC   lien Google Fonts"); sys.exit(1)
s = s[:m.start()] + "<style>\n" + fonts + "\n</style>" + s[m.end():]
n += 1; print("  ok      GT Pressura embarquée (6 graisses)")

# ---------- 2. jetons ----------
m = re.search(r":root\{.*?\n\}", s, re.S)
if not m: print("  ÉCHEC   :root"); sys.exit(1)
s = s[:m.start()] + """:root{
  /* Charte Bulldozer — mode clair. Noir pour la structure et le texte, lime en
     accent seul, pastels de la charte pour les catégories. Le lime ne porte
     jamais de texte : il sert de fond de pastille, de trait ou de barre. */
  --navy:#000000; --navy-2:#141410; --navy-3:#2C2C26; --teal:#6E7561; --teal-l:#E8EADF;
  --lime:#DDFF56; --lime-d:#A8C62F;
  --red:#000000; --red-soft:#FFF0F6; --orange:#000000; --orange-soft:#F3EFFF;
  --bg:#F4F4EE; --surface:#FFFFFF; --card:#FFFFFF; --card-2:#FAFAF5;
  --line:#E3E4DA; --line-2:#C6C8B9;
  --text:#000000; --body:#26281F; --muted:#5F6256; --faint:#8A8D80;
  /* sur fond noir (barre latérale, cartes de chiffres) */
  --on-dark:#FFFFFF; --on-dark-2:#D8DACB; --on-dark-3:#9A9D8C;
  --ok:#1E5A2C; --ok-bg:#AFFAA8; --info:#12485C; --info-bg:#AEF1FA;
  --warn:#6A3B52; --warn-bg:#FECEEB; --crit:#6A3B52; --crit-bg:#FECEEB; --mute-bg:#EFEFE8;
  /* catégoriel : lime, vert, bleu, violet — ordre fixe, filet noir sur fond clair */
  --c1:#DDFF56; --c2:#AFFAA8; --c3:#AEF1FA; --c4:#DED7FF;
  --c-pub:var(--c1); --c-site:var(--c2); --c-mail:var(--c3); --c-ext:var(--c4);
  /* rampe du funnel : du noir au gris clair */
  --s-bofu:#000000; --s-mofu:#6E7561; --s-tofu:#C6C8B9;
  --q-A:#DDFF56; --q-B:#AEF1FA; --q-C:#DED7FF; --q-D:#D5D7C9;
  --r-dec:#000000; --r-champ:#6E7561; --r-ope:#B0B3A4;
  --f-display:"GT Pressura","Arial Narrow",Arial,sans-serif;
  --f-body:"GT Pressura",system-ui,-apple-system,sans-serif;
  --f-mono:"GT Pressura Mono",ui-monospace,Menlo,monospace;
  --r:6px; --r-s:4px; --sh:none; --side:252px;
}""" + s[m.end():]
n += 1; print("  ok      jetons Bulldozer clair")

# ---------- 3. barre latérale : noir + lime, texte clair ----------
for a, b, lbl in [("#C9D6DC", "var(--on-dark-2)", "texte barre latérale"),
                  ("#DCE6EA", "var(--on-dark-2)", "boutons de navigation"),
                  ("#9FB2BD", "var(--on-dark-3)", "sous-titres barre latérale"),
                  ("#8FA3AF", "var(--on-dark-3)", "sections de navigation")]:
    if a in s: sub(a, b, lbl, -1)
sub('.logo .mk{background:var(--red);color:#fff;', '.logo .mk{background:var(--lime);color:#000;', "monogramme lime")

# ---------- 4. cartes de chiffres : aplat noir, chiffre blanc, alerte cerclée de lime ----------
sub(".kpi.red{background:var(--red);color:", ".kpi.red{background:var(--navy);border:2px solid var(--lime);color:", "carte d'alerte cerclée")
for a, b in [("#FFE3E0", "var(--on-dark-2)"), ("#FFD4CF", "var(--lime)")]:
    if a in s: sub(a, b, "texte de la carte d'alerte", -1)

# ---------- 5. bandeau : aplat noir, trait lime, pas de texte sur jaune ----------
sub(".banner{background:var(--lime);color:var(--navy);",
    ".banner{background:var(--navy);color:var(--on-dark-2);border-left:5px solid var(--lime);", "bandeau")
sub(".banner b{color:var(--navy)}", ".banner b{color:var(--lime)}", "gras du bandeau")

# ---------- 6. ni ombre ni dégradé ----------
s2 = re.sub(r"box-shadow:[^;}]+", "box-shadow:none", s)
if s2 != s: s = s2; n += 1; print("  ok      ombres portées retirées")
s2 = re.sub(r"linear-gradient\((?:180deg,)?rgba\(14,40,65[^)]*\)[^;}]*", "none", s)
if s2 != s: s = s2; n += 1; print("  ok      dégradés marine retirés")

# ---------- 7. filet noir sous les pastels, sinon elles disparaissent sur blanc ----------
s = s.replace("</style>", """
/* Les pastels de la charte sont claires : sur fond blanc elles ont besoin d'un
   filet pour rester lisibles. */
.hb .t i{outline:1px solid rgba(0,0,0,.35);outline-offset:-1px}
svg rect[fill^="var(--c"]{stroke:rgba(0,0,0,.45);stroke-width:.6}
.qp,.quadlegend b{border:1px solid rgba(0,0,0,.35)}
.legend i{outline:1px solid rgba(0,0,0,.3);outline-offset:-1px}
/* bibliothèque de contenus */
.lbgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:18px}
.lbc{margin:0;border:1px solid var(--line);border-radius:var(--r);overflow:hidden;background:var(--surface);display:flex;flex-direction:column}
.lbc.ko{border-color:var(--warn-bg);border-width:2px}
.lbc img{display:block;width:100%;height:172px;object-fit:cover;object-position:top center;border-bottom:1px solid var(--line)}
.lbc-no{height:172px;display:flex;align-items:center;justify-content:center;background:var(--card-2);color:var(--faint);font-size:12.5px;border-bottom:1px solid var(--line)}
.lbc figcaption{padding:12px 13px 14px;display:flex;flex-direction:column;gap:7px}
.lbc-h{display:flex;gap:8px;align-items:flex-start;justify-content:space-between}
.lbc-h b{font:600 14px/1.25 var(--f-display);color:var(--text)}
.lbc-m{font-size:12.5px;color:var(--body);display:flex;align-items:center;gap:6px;flex-wrap:wrap}
.lbc-u{font:400 11.5px var(--f-mono);color:var(--muted);text-decoration:none;word-break:break-all}
.lbc-u:hover{color:var(--text);text-decoration:underline}
.lbc-ko{margin:2px 0 0;font-size:12px;color:var(--crit);background:var(--warn-bg);padding:7px 9px;border-radius:var(--r-s)}
.lbc-ko span{font-family:var(--f-mono);font-size:11px;word-break:break-all}
.lbc-n{margin:2px 0 0;font-size:12px;color:var(--muted)}
/* annonces */
.adgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(232px,1fr));gap:16px}
.adc{margin:0;border:1px solid var(--line);border-radius:var(--r);overflow:hidden;background:var(--surface);display:flex;flex-direction:column}
.adc-i{position:relative;background:var(--card-2)}
.adc-i img{display:block;width:100%;height:150px;object-fit:cover;border-bottom:1px solid var(--line)}
.adc-pf{position:absolute;top:7px;left:7px;font:400 9.5px var(--f-mono);letter-spacing:.06em;text-transform:uppercase;background:var(--navy);color:var(--on-dark);padding:3px 6px;border-radius:2px}
.adc-pf.li{background:var(--lime);color:#000}
.adc figcaption{padding:10px 11px 12px;display:flex;flex-direction:column;gap:5px}
.adc figcaption > b{font:600 12.5px/1.25 var(--f-display);color:var(--text)}
.adc-c{font-size:11px;color:var(--muted)}
.adc-m{display:flex;flex-wrap:wrap;gap:8px;font:400 11px var(--f-mono);color:var(--body)}
.adc-m b{color:var(--text)}
.adc-t{margin:3px 0 0;font-size:11.5px;color:var(--body);line-height:1.4}
.adc-t.vide{color:var(--faint);font-style:italic}
.adc-f{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-top:2px}
.adc-f a{font:400 10.5px var(--f-mono);color:var(--muted);word-break:break-all}
</style>""", 1)
n += 1; print("  ok      filet noir sur les aplats pastel")

P.write_text(s, encoding="utf-8"); print("\n%d passes de charte" % n)

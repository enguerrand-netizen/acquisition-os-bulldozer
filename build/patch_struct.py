# -*- coding: utf-8 -*-
"""Passe 1 — modifications structurelles indépendantes des données.
Repart toujours de la référence pour être rejouable."""
import pathlib, re, sys
SRC = pathlib.Path("/private/tmp/claude-501/-Users-enguerrandchalvondemersay/a75e6ca6-5ff8-478d-bd1a-9a963b0419f5/scratchpad/acq/spec/reference-index.html")
OUT = pathlib.Path("app.src.html")
s = SRC.read_text(encoding="utf-8")
n = 0
def sub(old, new, label, count=1):
    global s, n
    if old not in s:
        print(f"  ÉCHEC   {label}"); sys.exit(1)
    s = s.replace(old, new, count); n += 1
    print(f"  ok      {label}")

# ---- identité ----
sub("<title>Tour de contrôle ABM</title>", "<title>Acquisition OS Bulldozer</title>", "titre")
sub('<div class="logo"><span class="mk">ABM</span><div><b>Tour de contrôle</b><span>Comptes nommés · signaux CRM</span></div></div>',
    '<div class="logo"><span class="mk">BDZ</span><div><b>Acquisition OS</b><span>30 grands comptes · CRM Bulldozer</span></div></div>', "logo")
sub('<div class="banner"><span><b>Plateforme de démonstration</b> · ce que l\'outil fera une fois branché au CRM et aux régies · données fictives</span></div>',
    '<div class="banner"><span><b>Données réelles du CRM Bulldozer</b> · relevé du 21 septembre 2026 · un levier sans source affiche ce qu\'il manque, jamais un chiffre inventé</span></div>', "bandeau")

# ---- date de référence : 18 → 21 septembre 2026, semaine 38 → 39 ----
sub("const TODAY = new Date(2026, 8, 18), DAY = 864e5, WEEK_NOW = 38;",
    "const TODAY = new Date(2026, 8, 21), DAY = 864e5, WEEK_NOW = 39;", "TODAY + WEEK_NOW")
sub("const MTD = 18 / 30;", "const MTD = 21 / 30;", "MTD")
sub('<span class="pill-navy">Semaine 38</span><span class="date">vendredi 18 septembre 2026</span>',
    '<span class="pill-navy">Semaine 39</span><span class="date">lundi 21 septembre 2026</span>', "en-tête date")

# ---- retrait de la proposition commerciale (document client, hors sujet en interne) ----
sub("const cpTabs = () => `<div class=\"lvhead\"><div class=\"seg\"><button data-cpt=\"dash\" aria-pressed=\"${ui.cpTab !== 'offre'}\">Tableau de bord</button><button data-cpt=\"offre\" aria-pressed=\"false\">Proposition et plan de mission ↗</button></div></div>`;",
    "const cpTabs = () => '';   /* proposition commerciale retirée : document destiné à un client, sans objet pour l'acquisition interne */", "onglet proposition")
sub("if (tab === 'offre' || tab === 'propal') { toPlan = tab === 'propal' && ui.tab === 'proposition'; tab = 'proposition'; }",
    "if (tab === 'offre' || tab === 'propal' || tab === 'proposition') { toPlan = false; tab = 'cockpit'; }", "routes offre/propal")
sub("({ proposition: renderMission, cockpit: renderCockpit,",
    "({ proposition: renderCockpit, cockpit: renderCockpit,", "dispatch proposition")

# ---- import : le portefeuille est celui du CRM, pas un collage ----
sub(">Importer mes comptes<", ">Ajouter un compte au plan<", "libellé import")

OUT.write_text(s, encoding="utf-8")
print(f"\n{n} modifications · {OUT} ({len(s):,} caractères)".replace(",", " "))

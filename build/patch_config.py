# -*- coding: utf-8 -*-
"""Passe 2 — recalibrage du moteur de scoring sur le CRM réel.
Aucun coefficient de la maquette n'est conservé sans justification.
S'applique à app.src.html produit par patch_struct.py."""
import pathlib, sys, re
P = pathlib.Path("app.src.html"); s = P.read_text(encoding="utf-8")

# --- 1. DEFAULT_CFG : les poids deviennent des mesures ---
old_cfg = re.search(r"const DEFAULT_CFG = \{.*?\n\};", s, re.S)
if not old_cfg: print("DEFAULT_CFG introuvable"); sys.exit(1)
new_cfg = """const DEFAULT_CFG = {
  /* Recalibré le 21/09/2026 sur le CRM Bulldozer (495 clients signés, 26,17 M€)
     et sur l'étude outbound du 17/09/2026 (4 754 comptes appelés, 33 signés).
     Chaque poids est une mesure : sa source est affichée dans l'écran Moteur. */
  icp: {
    /* Taux de signature observés par tranche d'effectif : 201-1 000 sal. 1,5 %,
       1 000-5 000 1,0 %, 5 000+ 0,8 %, <200 0,4-0,7 %. Le maximum n'est donc PAS
       chez les plus gros : la taille discrimine à l'envers de l'intuition. */
    size: { s: 18, m: 40, l: 30, xl: 22 },
    /* Familles qui pèsent le plus dans les 495 clients signés : Logiciel 33,9 %,
       Conseil 14,7 %, Banque & assurance 10,7 %, Distribution 8,1 %. */
    sectors: ['Logiciel', 'Conseil', 'Banque & assurance', 'Distribution & commerce'],
    /* sectorOut n'est pas nul : un secteur jamais signé est une absence de preuve,
       pas une impossibilité — et 36,6 % des clients n'ont pas de secteur au CRM. */
    sectorIn: 30, sectorOut: 8,
    /* Un chiffrage déjà accepté en interne rouvre plus vite qu'une porte froide ;
       un compte client sur une autre entité du groupe est une référence activable. */
    hist: { client: 25, ancien: 22, chiffre: 20, encours: 15, perdu: 12, jamais: 0 },
    /* Les grands comptes signés du CRM sont tous entrés par une filiale :
       Veolia via SARP et Veolia Recyclage, Carrefour via Carrefour Pro. */
    multi: 12,
    /* Exercice fiscal : aucune source dans le CRM. Pilier neutralisé — il reste
       réglable pour le jour où l'information sera saisie. */
    fy: { prep: 0, start: 0, prepFrom: 1, prepTo: 4 },
    lossMalus: 15
  },
  eng: {
    /* Le comité pèse autant que l'intention : décideur en base + ≥2 contacts donne
       5,3 % de signature contre 0,5 %, là où le contenu téléchargé donne 3,9 %. */
    w: { intent: 40, comite: 40, timing: 20 },
    half: 120, sat: 35, hotMin: 4,
    stage: { bofu: 2, mofu: 1, tofu: 0.5 },
    /* pricing = demande de rendez-vous entrante, le signal le plus fort.
       lgf = formulaire LinkedIn Lead Gen : 76 % des comptes en ont un, signés
       comme non signés — il ne discrimine pas, d'où un poids très bas.
       open = ouverture e-mail, gonflée par Apple MPP (jusqu'à 110 en 3 semaines). */
    sig: { pricing: 16, form: 12, dl: 10, webinar: 9, click: 5, lgf: 4,
           page: 3, ad: 2, open: 1, job: 0, hiring: 0, news: 0 },
    comite: { dec: 40, hot2: 30, champ: 20, cover: 10 },
    timing: { job: 55, event: 45 },
    noContact: 15
  },
  /* Seuils posés sur les médianes du portefeuille (ICP 52, engagement 65) : sur
     30 comptes, un seuil absolu laisserait trois quadrants vides. Ils sont
     réglables ci-contre et « fort » veut donc dire « au-dessus de la moitié ». */
  matrix: { icp: 52, eng: 65 }
};"""
s = s[:old_cfg.start()] + new_cfg + s[old_cfg.end():]
print("  ok      DEFAULT_CFG recalibré")

# --- 2. scoreICP : reconnaître 'perdu' / 'encours' / 'jamais' et le chiffrage ---
old = "const hi = C.icp.hist[a.status]; if (hi) L.push({ k: 'Historique', v: hi, d: STATUS[a.status].l });"
if False:
    new = ("const chiffre = !!(a.hist.loss && a.hist.loss.amt) || !!(a.hist.open && a.hist.open.amt);\n"
           "  const hi = Math.max(C.icp.hist[a.status] || 0, chiffre ? (C.icp.hist.chiffre || 0) : 0);\n"
           "  if (hi) L.push({ k: 'Historique', v: hi, d: chiffre && hi === C.icp.hist.chiffre ? 'chiffrage déjà accepté en interne' : STATUS[a.status].l });")
    s = s.replace(old, new); print("  ok      scoreICP reconnaît le chiffrage")

P.write_text(s, encoding="utf-8"); print(f"\n{P} ({len(s):,} caractères)".replace(",", " "))

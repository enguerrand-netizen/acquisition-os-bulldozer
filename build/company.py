# -*- coding: utf-8 -*-
"""Données d'entreprise (hors comptes) : pipeline, sources, leviers.
Tout champ sans source réelle est absent, et la raison est écrite dans
`manquant` — l'écran affiche alors ce qu'il faut brancher."""
import json, pathlib
D = pathlib.Path("/private/tmp/claude-501/-Users-enguerrandchalvondemersay/a75e6ca6-5ff8-478d-bd1a-9a963b0419f5/scratchpad/acq/data")
P = json.load(open(D/"pipeline.json")); L = json.load(open(D/"leviers.json"))
A = json.load(open(D/"activite.json")); S = json.load(open(D/"signaux.json"))
C = json.load(open(D/"comptes.json"))

out = {"releve": "2026-09-21", "portail": "143561253"}

# ---- pipeline ----
conv = P["conversion"]["hors_deals_automatiques"]
out["pipeline"] = {
  "fenetre": P["_meta"].get("fenetre") or "21/09/2024 → 21/09/2026",
  "par_mois": P["deals_par_mois"],
  "pipe": P["pipe_actuel"],
  "entonnoir": conv.get("entonnoir_reel_depuis_R1"),
  "stages": P["stages"],
  "sources_tous": P["sources"]["repartition_source_inbound_outbound"],
  "sources_gagnes": P["sources"]["repartition_source_sur_deals_gagnes"],
  "source_remplissage": P["sources"]["taux_de_remplissage_pct"],
  "reserves": [
    "86 % des deals gagnés ne passent jamais par un R1 : ils sont créés le jour de la signature (upsell, régie, TDT). Le seul taux lisible est R1 → signature.",
    "434 deals ont été créés automatiquement par les formulaires LinkedIn Lead Gen ; 2 seulement ont été gagnés. Ils sont exclus des taux.",
    "Le montant est absent sur 280 des 321 deals ouverts : le pipe affiché ne valorise que les 41 deals chiffrés.",
    "La source n'est renseignée que sur 70,3 % des deals, et pas du tout sur 314 des gagnés."
  ]}

# ---- activité commerciale ----
out["activite"] = {"par_mois": A.get("par_mois") or A.get("activite_par_mois"),
  "totaux": A.get("totaux") or A.get("volumes"),
  "reserves": ["Les messages LinkedIn, SMS et WhatsApp (objet COMMUNICATION) sont bloqués par le connecteur : ces volumes sont un plancher.",
               "Les tâches sont datées par échéance, pas par création."]}

# ---- paid ----
pl = L["paid_linkedin"]["donnees"]["compte_principal"]
pm = L["paid_meta"]["donnees"]["compte_principal"]
# exposition publicitaire au niveau compte, mesurée dans le CRM
expo = [c for c in C if (c.get("fibbler_linkedin_ad_impressions_90_days") or 0)]
expo_cible = [c for c in expo if c.get("population") == "cible"]
eng_cible = [c for c in expo_cible if (c.get("fibbler_linkedin_ad_engagements_90_days") or 0)]
out["paid"] = {
  "linkedin": {"compte": pl.get("nom"), "total": pl["total_recompose"], "par_mois": pl["par_mois"],
               "par_campagne": pl["par_campagne"], "campagnes_avec_metriques": pl.get("campagnes_avec_metriques"),
               "campagnes_referencees": pl.get("campagnes_referencees")},
  "meta": {"compte": pm.get("nom"), "total": pm["total_recompose"], "par_mois": pm["par_mois"],
           "par_campagne": pm.get("par_campagne_top40", [])},
  # Exposition publicitaire mesurée sur la fiche entreprise (fibbler_linkedin_ad_*_90_days).
  # 509 exposés et 112 engagés sur TOUTE la base (29 500 entreprises) — chiffre relevé
  # par l'extraction ; les compteurs ci-dessous portent sur les 1 048 comptes du fichier.
  "exposition_comptes": {"exposes_toute_base": 509, "engages_toute_base": 112,
                         "exposes_portefeuille": len(expo),
                         "exposes_cibles": len(expo_cible), "engages_cibles": len(eng_cible),
                         "part_hors_portefeuille": round(100 * (1 - len(expo) / 509), 1)},
  "reserves": [
    "La métrique « leads » de la régie est fausse dans l'OS : elle est exclue de tout l'écran, ainsi que le coût par lead qui en dérive.",
    "Sur Meta, l'acquisition de l'agence et les campagnes clientes partagent le même compte : les campagnes dont le nom commence par « Client_ » sont du budget client, pas de l'acquisition Bulldozer.",
    "Le ciblage, la portée et les réactions des annonces n'ont jamais été importés dans l'OS : ces colonnes resteront vides."
  ]}

# ---- contenu : ce qui fait remplir un formulaire, mesuré côté CRM ----
out["content"] = {"familles": S.get("formulaires_par_famille"),
  "volumes_par_type": S.get("volumes_par_type"), "volume_mensuel": S.get("volume_mensuel"),
  "branche": True,
  "reserves": ["Il n'existe pas de bibliothèque de contenus dans l'OS : les contenus sont reconstitués à partir du libellé des formulaires remplis dans le CRM. Le coût de production et le budget poussé derrière chaque contenu ne sont donc pas mesurables ici.",
               "84 % des formulaires sont des formulaires LinkedIn Lead Gen, qui ne discriminent pas : 76 % des comptes en ont un, signés comme non signés."]}

# ---- social : non branché ----
sl = L["social_linkedin"]
out["social"] = {"branche": False,
  "constat": "16 posts relevés, tous issus du profil personnel de Jordan (03/06 → 17/09/2026) : 1 455 réactions, 311 commentaires.",
  "manquant": "Aucun post de la page entreprise Bulldozer n'est stocké dans l'OS — l'accès à la page est refusé (pageAccess DENIED) et les deux configurations de rafraîchissement visent des profils de personnes. Il manque l'accès administrateur à la page pour alimenter cet écran.",
  "posts": (sl.get("donnees") or {}).get("posts", [])}

# ---- outbound : partiellement branché ----
ol = L["outbound_lemlist"]["donnees"]
out["outbound"] = {"branche": False,
  "constat": f"{ol.get('campagnes_total')} campagnes Lemlist créées entre janvier 2024 et septembre 2026, aucune en cours d'envoi.",
  "manquant": "L'export Lemlist renvoie 0 lead sur toutes les campagnes testées, y compris celles qui ont réellement tourné, et 89 campagnes sur 108 sont en erreur. Aucun volume d'envoi, d'ouverture ou de réponse n'est donc lisible. Les e-mails sortants tracés dans le CRM restent la seule mesure fiable.",
  "campagnes_total": ol.get("campagnes_total"), "repartition": ol.get("repartition_par_statut")}

# ---- seo ----
se = L["seo"]["donnees"]
out["seo"] = {"branche": True, "domaine": se.get("domaine_configure"),
  "apercu": se.get("apercu_domaine"), "gsc": se.get("search_console"),
  "reserves": ["L'aperçu du domaine est un instantané de septembre 2026, les mots-clés de juin 2026 : les deux ne se croisent pas.",
               "Les trois dimensions de la Search Console ne donnent pas le même total de clics (4 400 / 8 488 / 8 364) : elles ne s'additionnent pas.",
               "Plusieurs mots-clés remontés par la source sont fabriqués (« growthpath », « boostmatic 360 ») et pèsent plus de 17 % du trafic annoncé."]}

# ---- sea : non branché ----
out["sea"] = {"branche": False,
  "constat": "Deux comptes Google Ads sont rattachés au projet, aucune campagne n'y existe.",
  "manquant": "Il n'y a rien à mesurer tant qu'une campagne n'a pas été lancée."}

pathlib.Path(D/"company.json").write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
print("company.json écrit")
print("  exposition :", out["paid"]["exposition_comptes"])
print("  paid LinkedIn :", out["paid"]["linkedin"]["total"])
print("  paid Meta :", out["paid"]["meta"]["total"])
print("  entonnoir R1 :", out["pipeline"]["entonnoir"])
print("  leviers non branchés :", [k for k in ("social","outbound","sea") if not out[k]["branche"]])

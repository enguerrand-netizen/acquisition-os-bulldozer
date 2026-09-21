# -*- coding: utf-8 -*-
"""Bibliothèque des contenus poussés sur LinkedIn.
Volumes et dates = `first_conversion_event_name` du CRM (première conversion,
donc un contact compté une seule fois). Vignettes = captures réelles des pages,
prises le 21/09/2026 avec Playwright. Aucune image, aucun titre inventé."""
import base64, json, pathlib
R = pathlib.Path("/private/tmp/claude-501/-Users-enguerrandchalvondemersay/a75e6ca6-5ff8-478d-bd1a-9a963b0419f5/scratchpad/acq")
S = R / "shots" / "small"

def img(k):
    p = S / (k + ".jpg")
    return "data:image/jpeg;base64," + base64.b64encode(p.read_bytes()).decode() if p.exists() else None

# n = conversions (somme des variantes de libellé) · d1/d2 = première et dernière
C = [
 dict(k="seo-geo", t="SEO vs GSO — stratégies à l'ère de l'IA", ty="Étude", st="mofu", n=835,
      d1="2025-09-19", d2="2026-09-10", u="https://www.bulldozer-collective.com/ressources/seo-vs-gso-nouvelles-strategies-a-lere-de-lia",
      mort="https://www.bulldozer-collective.com/ressources/seo-vs-geo-nouvelles-strategies-a-lere-de-lia",
      note="721 contacts sont entrés par l'ancienne URL en « seo-vs-geo », qui renvoie aujourd'hui un 404."),
 dict(k="barometre", t="Baromètre — évolution des métiers et des salaires du marketing", ty="Baromètre", st="mofu", n=693,
      d1="2025-03-27", d2="2026-03-23", u="https://magnet.bulldozer-collective.com/evolution-des-metiers-et-des-salaires-du-marketing"),
 dict(k="lb-abm", t="Livre blanc Outbound & ABM", ty="Livre blanc", st="mofu", n=339,
      d1="2024-12-02", d2="2025-11-26", u="https://magnet.bulldozer-collective.com/livre-blanc-outbound-abm"),
 dict(k="newsletter", t="Bullish — la newsletter", ty="Newsletter", st="tofu", n=517,
      d1="2025-01-08", d2="2026-09-15", u="https://www.bulldozer-collective.com/newsletter"),
 dict(k="equipe-growth", t="Recruter sa première équipe growth", ty="Playbook", st="mofu", n=152,
      d1="2025-06-10", d2="2026-02-09", u="https://www.bulldozer-collective.com/ressources/equipe-growth"),
 dict(k="qbr", t="Template Quarterly Business Review", ty="Template", st="mofu", n=78,
      d1="2025-10-01", d2="2025-11-05", u="https://www.bulldozer-collective.com/fr/ressources/template-qbr-2025",
      mort="https://www.bulldozer-collective.com/ressources/template-qbr-2025",
      note="70 contacts sont entrés par l'URL sans préfixe « /fr/ », qui renvoie un 404."),
 dict(k="budget", t="Notre méthode de planification budgétaire", ty="Playbook", st="mofu", n=64,
      d1="2025-03-13", d2="2026-09-10", u="https://www.bulldozer-collective.com/ressources/notre-methode-de-planification-budgetaire"),
 dict(k="rise", t="Rise_26", ty="Événement", st="mofu", n=53,
      d1="2026-07-03", d2="2026-09-18", u="https://www.bulldozer-collective.com/fr/rise"),
 dict(k="claude-b2b", t="Claude pour le marketing B2B", ty="Ressource IA", st="mofu", n=52,
      d1="2026-04-13", d2="2026-09-14", u="https://www.bulldozer-collective.com/fr/ressources/claude-pour-le-marketing-b2b"),
 dict(k="weglot", t="Weglot × Bulldozer — kit d'expansion internationale", ty="Kit", st="mofu", n=50,
      d1="2025-10-16", d2="2026-04-20", u="https://www.bulldozer-collective.com/fr/ressources/kit-expansion-internationale",
      mort="https://www.bulldozer-collective.com/ressources/kit-expansion-internationale",
      note="29 contacts sont entrés par l'URL sans préfixe « /fr/ », qui renvoie un 404."),
 dict(k="claude-skills", t="Claude Skills pour paid acquisition B2B", ty="Ressource IA", st="mofu", n=21,
      d1="2026-04-16", d2="2026-09-21", u="https://www.bulldozer-collective.com/ressources/claude-skills"),
 dict(k="playbook-seo", t="Notre playbook SEO (0 à 1)", ty="Playbook", st="mofu", n=17,
      d1="2025-03-06", d2="2025-11-03", u="https://www.bulldozer-collective.com/ressources/playbook-seo"),
 dict(k="ressources", t="Toutes les ressources", ty="Page pilier", st="tofu", n=16,
      d1="2024-06-27", d2="2026-09-15", u="https://www.bulldozer-collective.com/ressources"),
 dict(k="telecharger", t="Page de téléchargement", ty="Page pilier", st="tofu", n=21,
      d1="2024-04-09", d2="2026-08-28", u="https://www.bulldozer-collective.com/telecharger"),
]
# contenus sans page capturable (formulaire hébergé ailleurs)
HORS = [
 dict(t="Typeform — prise de contact", ty="Prise de contact", st="bofu", n=871, d1="2025-09-16", d2="2026-09-21",
      u="https://bulldozer-collective.typeform.com/to/vkgpsae6",
      note="Le signal le plus fort du catalogue : une demande de rendez-vous entrante."),
 dict(t="Typeform — demande d'informations (ancien)", ty="Prise de contact", st="bofu", n=375, d1="2023-11-05", d2="2024-04-18",
      u="https://form.typeform.com/to/zdjlgejb", note="Remplacé par le Typeform de prise de contact fin 2024."),
 dict(t="State of AI Marketing 2026", ty="Étude", st="mofu", n=7, d1="2026-04-14", d2="2026-07-21", u=None),
 dict(t="L'Observatoire de la maturité digitale", ty="Étude", st="mofu", n=10, d1="2025-11-23", d2="2026-09-09", u=None),
]
# formulaires Lead Gen LinkedIn — l'autre moitié de la bibliothèque, côté régie
LGF = [
 ("Global form — ending send doc — BOFU", 9606, "2025-11-20", "2026-09-21"),
 ("Global form — ending send doc", 3210, "2025-03-11", "2025-10-17"),
 ("Global form", 884, "2025-02-03", "2025-04-02"),
 ("Global form — ending send doc — SEO du GSO", 663, "2025-10-07", "2026-02-06"),
 ("Lead gen Bulldozer form other", 312, "2024-11-19", "2024-12-16"),
 ("Top 30 stratégies growth", 256, "2024-12-10", "2025-02-03"),
 ("Global form — ending send doc USA", 109, "2025-07-18", "2025-07-29"),
 ("Global form — ending send doc — MOFU", 68, "2025-10-29", "2026-01-04"),
 ("BP 2025", 71, "2024-12-10", "2025-01-30"),
 ("Checklist 90 premiers jours du CMO", 50, "2024-12-13", "2025-02-03"),
 ("TDT — Sonar", 39, "2025-07-11", "2025-08-01"),
 ("Global form — ending send doc — TOFU", 15, "2025-10-29", "2025-11-28"),
 ("Use case BlaBlaCar", 8, "2025-01-23", "2025-02-04"),
 ("Use case Swile", 5, "2025-01-23", "2025-02-04"),
 ("TDT — CEO", 10, "2026-02-06", "2026-06-07"),
 ("Use case Back Market", 3, "2025-01-23", "2025-02-04"),
 ("Template protocole de stratégie B2B", 5, "2024-12-13", "2024-12-18"),
 ("Top 5 stratégies ABM", 5, "2024-12-18", "2025-01-28"),
]
for c in C: c["img"] = img(c["k"])
out = dict(contenus=C, hors_page=HORS,
           lead_gen=[dict(t=t, n=n, d1=a, d2=b) for t, n, a, b in LGF],
           releve="2026-09-21",
           methode="Volumes lus sur `first_conversion_event_name` dans HubSpot : un contact est compté une seule fois, à sa première conversion. Les variantes de libellé d'un même contenu (français/anglais, avec ou sans le suffixe « | ressources bulldozer ») sont additionnées. Vignettes capturées le 21/09/2026 sur les pages en ligne.")
p = R / "data" / "contenus.json"
p.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
print("contenus.json ·", round(p.stat().st_size / 1024), "Ko ·", len(C), "pages capturées ·",
      len(HORS), "hors page ·", len(LGF), "formulaires Lead Gen")
print("conversions totales :", sum(c["n"] for c in C) + sum(h["n"] for h in HORS), "contenus +",
      sum(x[1] for x in LGF), "Lead Gen")

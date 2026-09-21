# -*- coding: utf-8 -*-
"""Taxonomie sectorielle unique, appliquée aux 495 clients ET aux 30 cibles.
Deux raisons de ne pas lire `industry` tel quel :
 - il est vide sur 36,6 % des clients et sur 9 des 30 cibles ;
 - il est faux sur certaines fiches (Rothschild & Co en « enseignement supérieur »).
Chaque secteur des 30 porte donc sa provenance : 'crm' ou 'corrigé'."""
import json, pathlib
from collections import Counter
D = pathlib.Path("/private/tmp/claude-501/-Users-enguerrandchalvondemersay/a75e6ca6-5ff8-478d-bd1a-9a963b0419f5/scratchpad/acq/data")

# --- HubSpot industry -> libellé français (12 familles) ---
MAP = {
 "COMPUTER_SOFTWARE":"Logiciel", "INFORMATION_TECHNOLOGY_AND_SERVICES":"Logiciel",
 "INTERNET":"Logiciel", "COMPUTER_NETWORK_SECURITY":"Logiciel", "COMPUTER_HARDWARE":"Logiciel",
 "MANAGEMENT_CONSULTING":"Conseil", "ACCOUNTING":"Conseil", "PROFESSIONAL_TRAINING_COACHING":"Conseil",
 "LEGAL_SERVICES":"Conseil", "LAW_PRACTICE":"Conseil", "MARKETING_AND_ADVERTISING":"Conseil",
 "PUBLIC_RELATIONS_AND_COMMUNICATIONS":"Conseil", "DESIGN":"Conseil", "STAFFING_AND_RECRUITING":"Conseil",
 "HUMAN_RESOURCES":"Conseil",
 "HIGHER_EDUCATION":"Enseignement", "EDUCATION_MANAGEMENT":"Enseignement", "E_LEARNING":"Enseignement",
 "BANKING":"Banque & assurance", "FINANCIAL_SERVICES":"Banque & assurance", "INSURANCE":"Banque & assurance",
 "CAPITAL_MARKETS":"Banque & assurance", "INVESTMENT_MANAGEMENT":"Banque & assurance",
 "INVESTMENT_BANKING":"Banque & assurance", "VENTURE_CAPITAL_PRIVATE_EQUITY":"Banque & assurance",
 "REAL_ESTATE":"Immobilier", "COMMERCIAL_REAL_ESTATE":"Immobilier", "FACILITIES_SERVICES":"Immobilier",
 "CONSTRUCTION":"Construction", "BUILDING_MATERIALS":"Construction", "ARCHITECTURE_PLANNING":"Construction",
 "CIVIL_ENGINEERING":"Construction",
 "RETAIL":"Distribution & commerce", "CONSUMER_GOODS":"Distribution & commerce",
 "FOOD_BEVERAGES":"Distribution & commerce", "FOOD_PRODUCTION":"Distribution & commerce",
 "APPAREL_FASHION":"Distribution & commerce", "COSMETICS":"Distribution & commerce",
 "LUXURY_GOODS_JEWELRY":"Distribution & commerce", "WHOLESALE":"Distribution & commerce",
 "SUPERMARKETS":"Distribution & commerce", "CONSUMER_ELECTRONICS":"Distribution & commerce",
 "SPORTING_GOODS":"Distribution & commerce",
 "HOSPITAL_HEALTH_CARE":"Santé", "PHARMACEUTICALS":"Santé", "MEDICAL_DEVICES":"Santé",
 "HEALTH_WELLNESS_AND_FITNESS":"Santé", "BIOTECHNOLOGY":"Santé", "MEDICAL_PRACTICE":"Santé",
 "UTILITIES":"Énergie & environnement", "RENEWABLES_ENVIRONMENT":"Énergie & environnement",
 "OIL_ENERGY":"Énergie & environnement", "ENVIRONMENTAL_SERVICES":"Énergie & environnement",
 "TRANSPORTATION_TRUCKING_RAILROAD":"Transport & logistique", "LOGISTICS_AND_SUPPLY_CHAIN":"Transport & logistique",
 "AIRLINES_AVIATION":"Transport & logistique", "MARITIME":"Transport & logistique", "AUTOMOTIVE":"Industrie",
 "MECHANICAL_OR_INDUSTRIAL_ENGINEERING":"Industrie", "ELECTRICAL_ELECTRONIC_MANUFACTURING":"Industrie",
 "MINING_METALS":"Industrie", "CHEMICALS":"Industrie", "PLASTICS":"Industrie", "MACHINERY":"Industrie",
 "PAPER_FOREST_PRODUCTS":"Industrie", "AVIATION_AEROSPACE":"Industrie", "DEFENSE_SPACE":"Industrie",
 "TELECOMMUNICATIONS":"Télécoms & médias", "ONLINE_MEDIA":"Télécoms & médias", "WIRELESS":"Télécoms & médias",
 "ENTERTAINMENT":"Télécoms & médias", "BROADCAST_MEDIA":"Télécoms & médias", "PUBLISHING":"Télécoms & médias",
 "MUSIC":"Télécoms & médias", "LEISURE_TRAVEL_TOURISM":"Autres services", "HOSPITALITY":"Autres services",
 "CONSUMER_SERVICES":"Autres services", "RESTAURANTS":"Autres services", "GAMBLING_CASINOS":"Autres services",
 "NON_PROFIT_ORGANIZATION_MANAGEMENT":"Autres services", "GOVERNMENT_ADMINISTRATION":"Secteur public",
 "PUBLIC_POLICY":"Secteur public", "CIVIC_SOCIAL_ORGANIZATION":"Secteur public",
}

# --- secteur retenu pour les 30, avec provenance et justification ---
CURE = {
 "317410706620": ("Industrie", "corrigé", "classé UTILITIES au CRM ; Schneider fabrique de l'équipement électrique"),
 "315914050757": ("Logiciel", "crm", None),
 "229907236085": ("Énergie & environnement", "corrigé", "secteur vide au CRM"),
 "229193587951": ("Distribution & commerce", "crm", None),
 "9770448590":  ("Autres services", "corrigé", "secteur vide au CRM ; restauration et services aux entreprises"),
 "317411495156": ("Banque & assurance", "crm", None),
 "238621997284": ("Distribution & commerce", "crm", None),
 "92346012914": ("Logiciel", "crm", None),
 "342918544596": ("Logiciel", "crm", None),
 "36144254182": ("Construction", "crm", None),
 "316281698550": ("Industrie", "corrigé", "secteur vide au CRM ; construction automobile"),
 "18938276038": ("Construction", "crm", None),
 "162003232956": ("Banque & assurance", "corrigé", "secteur vide au CRM"),
 "36322852030": ("Banque & assurance", "crm", None),
 "140916864248": ("Distribution & commerce", "corrigé", "secteur vide au CRM ; petit électroménager"),
 "175301965003": ("Conseil", "corrigé", "secteur vide au CRM ; Invent est l'entité conseil de Capgemini"),
 "87436872902": ("Santé", "crm", None),
 "148704214225": ("Industrie", "corrigé", "secteur vide au CRM ; constructeur automobile"),
 "59663610043": ("Conseil", "crm", None),
 "315014441197": ("Logiciel", "crm", None),
 "14793944264": ("Énergie & environnement", "crm", None),
 "36289884362": ("Industrie", "crm", None),
 "19976068547": ("Énergie & environnement", "corrigé", "secteur vide au CRM"),
 "17818953714": ("Transport & logistique", "crm", None),
 "141529360630": ("Banque & assurance", "corrigé", "secteur vide au CRM ; protection sociale"),
 "316281711842": ("Enseignement", "crm", None),
 "316281684204": ("Enseignement", "corrigé", "la fiche s'appelle « Rothschild & Co » au CRM mais ses 18 contacts sont tous @essca.eu / @essca.fr et son unique transaction s'appelle « ESSCA » : c'est l'ESSCA, une école de commerce, pas la banque d'affaires"),
 "143877777655": ("Santé", "corrigé", "secteur vide au CRM ; optique et santé visuelle"),
 "174866082014": ("Industrie", "corrigé", "secteur vide au CRM ; défense et aéronautique"),
 "14624157398": ("Distribution & commerce", "crm", None),
}

C = json.load(open(D/"comptes.json"))
clients = [c for c in C if c.get("population") == "client"]
fam = Counter(); famCA = Counter(); inconnus = Counter(); sansSecteur = 0
for c in clients:
    ind = c.get("industry")
    if not ind: sansSecteur += 1; continue
    f = MAP.get(ind)
    if not f: inconnus[ind] += 1; continue
    fam[f] += 1; famCA[f] += float(c.get("total_revenue") or 0)

print("### Familles chez les 495 clients signés")
print(f"{'famille':28s} {'clients':>8} {'part':>7} {'CA signé':>14}")
tot = sum(fam.values())
for f, k in fam.most_common():
    print(f"{f:28s} {k:>8} {k/tot*100:>6.1f}% {int(famCA[f]):>13,} €".replace(",", " "))
print(f"\nsans secteur au CRM : {sansSecteur} clients ({sansSecteur/len(clients)*100:.1f} %) — le calibrage porte sur {tot} clients")
if inconnus: print("codes non mappés :", dict(inconnus.most_common(12)))

json.dump({"map": MAP, "cure": CURE, "familles_clients": dict(fam),
           "familles_clients_ca": {k: round(v) for k, v in famCA.items()},
           "clients_sans_secteur": sansSecteur, "clients_classes": tot},
          open(D/"secteurs.json", "w"), ensure_ascii=False, indent=1)
print("\n→ secteurs.json")

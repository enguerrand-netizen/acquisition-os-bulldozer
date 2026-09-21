# Portefeuille de comptes — extraction HubSpot (portail Bulldozer 143561253, eu1)

Extraction **en lecture seule** du 21/09/2026. Aucun objet créé, modifié ou supprimé.
Sortie : `comptes.json` — 1048 objets.

---

## 1. Ce qui a été extrait, et comment

### Méthode

Le cross-objet tronque silencieusement : il n'a **pas** été utilisé. Tout le dataset vient de
`query_crm_data` mono-objet `FROM COMPANY`, paginé par **plages d'identifiants**
(`hs_object_id > <dernier id> ORDER BY hs_object_id ASC LIMIT 500`), jamais par `OFFSET`.
32 colonnes demandées à chaque page pour forcer l'écriture en `tool-results/*.txt` ; les fichiers
ont été parsés en Python (`build.py`), pas lus en contexte.

Les deux populations ont été tirées de deux requêtes distinctes :

| Requête | Pages | Lignes | Total annoncé par le MCP |
|---|---|---|---|
| `numberofemployees >= 1000` (univers de sélection des cibles) | 5 (dont 1 de recouvrement) | **2 029 ids uniques** | 2 029 |
| `lifecyclestage = 'customer'` | 1 | **495** | 495 |

La somme des pages égale le total annoncé dans les deux cas. Le filtrage des cibles a ensuite été
appliqué **en Python** sur les 2 029 fiches, ce qui évite le piège du `!=` SQL sur une propriété non renseignée.

### Comptages à chaque étape

| Étape | Compté | Attendu | Écart |
|---|---|---|---|
| Entreprises ≥ 1 000 salariés (tous stades) | 2 029 | — | — |
| Cibles : non clientes, ≥ 1 000 sal., **≥ 4 contacts** | **321** | 321 | 0 |
| Cibles : non clientes, ≥ 1 000 sal., **≥ 2 formulaires et ≤ 3 contacts** | **232** | 232 | 0 |
| **Univers cibles** | **553** | 553 | **0** |
| Clients (`lifecyclestage = 'customer'`) | **495** | 495 | 0 |
| Chevauchement cible ↔ client | 0 | — | — |
| **Total `comptes.json`** | **1 048** | — | — |

Chaque comptage a été recoupé avec le champ `total` de `search_crm_objects` avant l'extraction :
les quatre chiffres (2 029 / 321 / 232 / 495) sont identiques des deux côtés. **Aucun écart à signaler.**

Note de méthode sur « non cliente » : la clause a été doublée (`lifecyclestage != 'customer'` **OU**
propriété absente) dans les requêtes de contrôle. Sans objet ici : les 553 cibles sont toutes
renseignées — 460 `lead`, 93 `opportunity`.

---

## 2. Propriétés — trouvées vs absentes

Recherche menée avec `search_properties` puis vérification exacte avec `get_properties` sur COMPANY.

### Trouvées et extraites

| Propriété | Type | Remarque |
|---|---|---|
| `fibbler_linkedin_ad_impressions_90_days` | number | exposition publicitaire LinkedIn, sync Fibbler |
| `fibbler_linkedin_ad_engagements_90_days` | number | idem |
| `fibbler_linkedin_ad_clicks_90_days` | number | idem |
| `scoring_lead` | number | « scoring lead linkedin » — le seul scoring maison qui existe |
| `tiers` | **string** | « Tiers company information calcul dans zapier » |
| `hs_ideal_customer_profile` | enumeration | tier_1 / tier_2 / tier_3 |
| `web_technologies` | string | liste `;`-séparée |
| `total_revenue` | number | montant des deals closed-won |

La famille Fibbler est donc bien **`fibbler_linkedin_ad_*_90_days`**, avec trois métriques
(impressions, engagements, clics) et non une seule.

### Absentes du portail

| Demandée | Statut |
|---|---|
| `lead_score_ia` | **n'existe pas** |
| `scoring_v2_engagement` | **n'existe pas** |
| `scoring_v2_pertinence` | **n'existe pas** |
| `hubspot_score` | **n'existe pas** (non activé sur COMPANY) |
| `notes_last_activity_date` | **n'existe pas** — remplacée par `notes_last_updated`, dont le libellé est précisément « Last Activity Date ». Le champ du JSON garde le nom demandé `notes_last_activity_date`, alimenté par `notes_last_updated`. |

Il n'y a donc **aucun scoring v2 ni scoring IA** dans le CRM : le seul scoring maison disponible est
`scoring_lead`, et il n'est renseigné que sur 367 des 1 048 comptes (35,0 %) — 51,7 % des cibles, 16,4 % des clients.
Sa valeur est d'ailleurs strictement corrélée à `hs_lead_status` (mêmes 367 fiches renseignées).

---

## 3. Taux de remplissage

### Les 4 champs clés

| Champ | Tous (1 048) | Cibles (553) | Clients (495) |
|---|---|---|---|
| `numberofemployees` | **83.7 %** (877) | 100.0 % (553) | 65.5 % (324) |
| `annualrevenue` | **44.5 %** (466) | 47.4 % (262) | 41.2 % (204) |
| `industry` | **62.9 %** (659) | 62.4 % (345) | 63.4 % (314) |
| `country` | **71.3 %** (747) | 80.1 % (443) | 61.4 % (304) |

`numberofemployees` est à 100 % sur les cibles **par construction** (c'est le critère de sélection) :
ce n'est pas une mesure de qualité de la base. Le chiffre honnête est celui des clients — **65,5 %**.

### Les autres champs

| Champ | Tous | Cibles | Clients |
|---|---|---|---|
| `city` | 53.1 % | 58.2 % | 47.3 % |
| `domain` | 94.7 % | 99.8 % | 88.9 % |
| `hubspot_owner_id` | 84.0 % | 87.3 % | 80.2 % |
| `hs_lead_status` | 35.0 % | 51.7 % | 16.4 % |
| `tiers` | 92.4 % | 98.9 % | 85.1 % |
| `hs_ideal_customer_profile` | 70.5 % | 84.6 % | 54.7 % |
| `web_technologies` | 59.0 % | 56.2 % | 62.0 % |
| `scoring_lead` | 35.0 % | 51.7 % | 16.4 % |
| `total_revenue` | 43.3 % | 0.0 % | 91.7 % |
| `notes_last_contacted` | 83.7 % | 82.1 % | 85.5 % |
| `first_conversion_event_name` | 74.0 % | 88.8 % | 57.4 % |
| `fibbler_… _impressions_90_days` | 9.6 % | 13.4 % | 5.5 % |

`total_revenue` est à 0 % sur les cibles (aucun deal gagné, cohérent) et 91,7 % sur les clients.

---

## 4. Distribution par tranche d'effectif

| Tranche | Cibles | % cibles | Clients | % clients |
|---|---|---|---|---|
| < 1 000 | 0 | 0.0 % | 299 | 60.4 % |
| 1 000 – 4 999 | 273 | 49.4 % | 16 | 3.2 % |
| 5 000 – 9 999 | 84 | 15.2 % | 3 | 0.6 % |
| 10 000 – 49 999 | 123 | 22.2 % | 4 | 0.8 % |
| 50 000 – 99 999 | 39 | 7.1 % | 2 | 0.4 % |
| ≥ 100 000 | 34 | 6.1 % | 0 | 0.0 % |
| non renseigné | 0 | 0.0 % | 171 | 34.5 % |

Lecture : les deux populations ne se ressemblent pas. Les cibles sont des grands comptes par
définition ; **299 clients sur 495 (60,4 %) font moins de 1 000 salariés** et 171 n'ont pas d'effectif.
Seuls **25 clients** (5,1 %) sont dans la tranche des cibles. Les clients servent donc de référence
**sectorielle**, pas de référence de taille.

---

## 5. Distribution par secteur

### Cibles (553) — 61 valeurs distinctes

| Secteur | n | % |
|---|---|---|
| — non renseigné — | 208 | 37.6 % |
| COMPUTER_SOFTWARE | 52 | 9.4 % |
| RETAIL | 20 | 3.6 % |
| HIGHER_EDUCATION | 18 | 3.3 % |
| INSURANCE | 16 | 2.9 % |
| PROFESSIONAL_TRAINING_COACHING | 12 | 2.2 % |
| APPAREL_FASHION | 10 | 1.8 % |
| PHARMACEUTICALS | 10 | 1.8 % |
| FOOD_BEVERAGES | 10 | 1.8 % |
| CONSUMER_SERVICES | 10 | 1.8 % |
| MANAGEMENT_CONSULTING | 9 | 1.6 % |
| BANKING | 8 | 1.4 % |
| LOGISTICS_AND_SUPPLY_CHAIN | 8 | 1.4 % |
| MARKETING_AND_ADVERTISING | 8 | 1.4 % |
| CONSUMER_GOODS | 8 | 1.4 % |

### Clients (495) — 66 valeurs distinctes

| Secteur | n | % |
|---|---|---|
| — non renseigné — | 181 | 36.6 % |
| COMPUTER_SOFTWARE | 97 | 19.6 % |
| PROFESSIONAL_TRAINING_COACHING | 15 | 3.0 % |
| REAL_ESTATE | 12 | 2.4 % |
| HUMAN_RESOURCES | 12 | 2.4 % |
| FINANCIAL_SERVICES | 12 | 2.4 % |
| EDUCATION_MANAGEMENT | 11 | 2.2 % |
| RETAIL | 9 | 1.8 % |
| CONSTRUCTION | 9 | 1.8 % |
| RENEWABLES_ENVIRONMENT | 8 | 1.6 % |
| CAPITAL_MARKETS | 7 | 1.4 % |
| HOSPITAL_HEALTH_CARE | 6 | 1.2 % |
| LEISURE_TRAVEL_TOURISM | 6 | 1.2 % |
| INSURANCE | 6 | 1.2 % |
| BANKING | 5 | 1.0 % |

Le premier « secteur » des deux populations est **l'absence de secteur** (37,6 % des cibles,
36,6 % des clients). Sur la part renseignée, `COMPUTER_SOFTWARE` domine des deux côtés, mais
beaucoup plus chez les clients (19,6 % vs 9,4 %) — c'est le signal sectoriel le plus net du portefeuille.

### Pays

| | France | États-Unis | non renseigné | autres |
|---|---|---|---|---|
| Cibles | 346 | 46 | 110 | 51 |
| Clients | 238 | 26 | 191 | 40 |

---

## 6. Exposition publicitaire LinkedIn (Fibbler)

| | Base entière (30 128 sociétés) | Ce portefeuille (1 048) | dont cibles | dont clients |
|---|---|---|---|---|
| impressions > 0 | **509** | **98** | 72 | 26 |
| engagements > 0 | **112** | **19** | 11 | 8 |
| clics > 0 | — | 2 | 1 | 1 |

Les 509 exposés / 112 engagés du relevé antérieur sont **confirmés à l'identique** sur la base entière
(comptés via le `total` de `search_crm_objects`). Mais seuls **98 exposés et 19 engagés** tombent dans
ce portefeuille : **80,7 % de l'exposition publicitaire LinkedIn porte sur des comptes hors périmètre**
(PME, ou grands comptes sans contact ni formulaire). C'est un constat à remonter au cockpit : la
pression média et la cible commerciale ne se recouvrent presque pas.

---

## 7. Anomalies de données

### 7.1 — Effectifs d'enrichissement faux : confirmés, et la cause est identifiée

**« Société Générale » à 2 036 salariés — CONFIRMÉ.**
  - `36322852030` — Société Générale — eff. 2036 — `societegenerale.com` — lead — *cible*
  - `168675795132` — Société Générale Assurances — eff. 1753 — `societegenerale.com` — lead — *cible*

Deux fiches sur le même domaine `societegenerale.com`, 2 036 et 1 753 salariés, là où le groupe en
compte ~117 000. Ces deux fiches passent le filtre « ≥ 1 000 salariés » pour de mauvaises raisons.

**« Capgemini Invent » au chiffre du groupe — CONFIRMÉ.**
  - `175301965003` — Capgemini Invent — eff. 342871 — `capgemini.com` — lead — *cible*

342 871 est l'effectif du groupe Capgemini, pas de l'entité Invent (~10 000). Même erreur de
granularité ailleurs : `Deloitte France` à 477 880 (`175256647883`), `EY` à 406 259 (`101997815017`),
`pwc` à 298 219 (`35716546790`) alors que `PwC France` à côté est à 4 114 (`96487043269`).

**Les valeurs 23 605 et 23 269 — CONFIRMÉES, et ce ne sont pas des « valeurs par défaut ».**

C'est plus embêtant que ça. Sur les 2 029 fiches de l'univers ≥ 1 000 salariés :

- **105 fiches portent exactement 23 605 salariés.** 102 d'entre elles ont une **URL LinkedIn dans le
  champ `domain`** (`https://www.linkedin.com/company/...` ou `/in/...`). 103 sur 105 sont localisées
  à **Sunnyvale**, secteur `COMPUTER_SOFTWARE`, pays **United States**.
- **6 fiches portent exactement 23 269 salariés.** Cinq ont `bit.ly` comme domaine, toutes sont
  localisées à **New York**.

Le mécanisme : quand le champ `domain` contient une URL LinkedIn (ou un bit.ly), l'enrichissement
résout le domaine `linkedin.com` (resp. `bit.ly`) et **recopie la fiche firmographique de LinkedIn
Corporation** (23 605 salariés, Sunnyvale, éditeur de logiciels) sur le compte. Ce n'est pas un
remplissage par défaut, c'est une **contamination par le domaine du réseau social**. Conséquence
directe : des fiches nommées `N/A`, `dd`, `En cours de création`, `Bryan COLOMBEL`, `Tech my PME`
— souvent des **personnes physiques ou des fiches vides** — entrent dans l'univers « ≥ 1 000 salariés ».

Exemples dans les 553 cibles :
  - `8946400239` — N/A — eff. 23605 — `https://www.linkedin.com/in/thibaud-meynieux/` — opportunity — *cible*
  - `83513463001` — Airbus — eff. 23605 — `https://www.linkedin.com/company/airbusgroup/` — lead — *cible*
  - `87011571955` — DNG - The Consumer Consulting Firm — eff. 23605 — `https://www.linkedin.com/company/digitalnative-group` — lead — *cible*
  - `90729496793` — AKE France — eff. 23605 — `https://www.linkedin.com/company/ake-france` — lead — *cible*
  - `90785193174` — Caption.market — eff. 23605 — `https://www.linkedin.com/company/caption-market` — lead — *cible*
  - `317411530957` — Luca - Finance &amp; Management School — eff. 23605 — `https://www.linkedin.com/school/luca-school/` — lead — *cible*

Il y a **8 fiches à 23 605** et **3 à 23 269** dans `comptes.json`, plus la fiche `8945498816`
nommée « linkedin » à 23 608 salariés — qui est LinkedIn elle-même, en `opportunity`.

**À retenir pour le cockpit : le critère « ≥ 1 000 salariés » est pollué par ~105 fiches dans l'univers
amont, dont une dizaine remontent jusque dans les cibles. Filtrer sur `domain NOT LIKE '%linkedin%'`
et `domain != 'bit.ly'` avant tout usage.**

### 7.2 — `annualrevenue` : des valeurs rondes suspectes

| Valeur | Fiches |
|---|---|
| 10 000 000 000 € | 137 |
| 10 000 000 € | 101 |
| 1 000 000 000 € | 53 |
| 50 000 000 € | 48 |
| 1 000 000 € | 36 |
| 250 000 000 € | 25 |

Sur 466 fiches renseignées, **137 portent exactement 10 000 000 000 € et 101 portent 10 000 000 €** :
ensemble, **51 % des CA renseignés** tiennent sur huit valeurs rondes. Le champ est une estimation par
palier, pas une donnée. Ne pas s'en servir pour segmenter ou prioriser.

### 7.3 — Le champ `domain` n'est pas un domaine

**61 fiches sur 1 048 (5,8 %)** ont une URL complète, une URL LinkedIn ou une URL Instagram
dans `domain` au lieu d'un domaine. C'est ce qui casse à la fois l'enrichissement (§7.1) et la
déduplication par domaine (§7.5). Exemples : `8946348531` Crédit Agricole → `https://www.credit-agricole.fr/`,
`14919933661` Arval → `https://www.arval.com/privacy`, `39502438609` Les Idéateurs → une URL Instagram,
`85335732448` CULLIGAN FRANCE → une URL LinkedIn.

### 7.4 — Les propriétés de tiering ne discriminent pas, et `tiers` est sale

`hs_ideal_customer_profile` chez les 495 clients : **tier_1 = 89, tier_2 = 94, tier_3 = 88, sans tier = 224**.
Le relevé antérieur annonçait 89/94/87 et 219 sans tier : l'écart (+1 tier_3, +5 sans tier) vient de
fiches clientes créées depuis. La conclusion tient : **répartition quasi uniforme, donc non
discriminante — extraite, mais à ne pas utiliser pour prioriser.**

`tiers` (la propriété maison calculée dans Zapier) est pire : elle est typée **string** et mélange
les formats. Chez les clients : `0`=160, `1`=84, `2`=92, `3`=61, mais aussi `Tier 1`=8, `Tier 2`=4, `Tier 3`=4, `Tiers 1`=1, `Aucune valeur`=7 (chaîne littérale), vide=74.
**Dix-sept fiches clientes portent un tier en toutes lettres** qu'un comptage numérique ignorera
silencieusement. Normaliser avant tout usage.

### 7.5 — Doublons de fiches

#### a) Même domaine normalisé — 28 grappes, 67 fiches

Le domaine est normalisé (protocole, `www.` et chemin retirés).

- **`linkedin.com`** ×8  ⚠️ **faux regroupement** : ce ne sont pas des doublons, c'est le champ `domain` qui contient une URL de réseau social / un lien court (cf. §7.1 et §7.3).
  - `317411530957` — Luca - Finance &amp; Management School — eff. 23605 — `https://www.linkedin.com/school/luca-school/` — lead — *cible*
  - `83513463001` — Airbus — eff. 23605 — `https://www.linkedin.com/company/airbusgroup/` — lead — *cible*
  - `85335732448` — CULLIGAN FRANCE — eff. 23605 — `https://www.linkedin.com/company/culligan-france` — customer — *client*
  - `87011571955` — DNG - The Consumer Consulting Firm — eff. 23605 — `https://www.linkedin.com/company/digitalnative-group` — lead — *cible*
  - `8945498816` — linkedin — eff. 23608 — `linkedin.com` — opportunity — *cible*
  - `8946400239` — N/A — eff. 23605 — `https://www.linkedin.com/in/thibaud-meynieux/` — opportunity — *cible*
  - `90729496793` — AKE France — eff. 23605 — `https://www.linkedin.com/company/ake-france` — lead — *cible*
  - `90785193174` — Caption.market — eff. 23605 — `https://www.linkedin.com/company/caption-market` — lead — *cible*
- **`arval.com`** ×3
  - `132647804111` — Arval BNP Paribas Group — eff. 8214 — `arval.com` — lead — *cible*
  - `14919933661` — Arval Bnp Paribas Group — eff. 8554 — `https://www.arval.com/privacy` — lead — *cible*
  - `313635745999` — Arval BNP Paribas Group — eff. 8366 — `arval.com` — lead — *cible*
- **`bit.ly`** ×3  ⚠️ **faux regroupement** : ce ne sont pas des doublons, c'est le champ `domain` qui contient une URL de réseau social / un lien court (cf. §7.1 et §7.3).
  - `108076811498` — Pandacraft — eff. 23269 — `bit.ly` — lead — *cible*
  - `40064053472` — elmy — eff. 23269 — `bit.ly` — opportunity — *cible*
  - `96045867249` — Digital Artness — eff. 23269 — `bit.ly` — opportunity — *cible*
- **`clubmed.com`** ×3
  - `35665402104` — Club Med SAS — eff. 13661 — `clubmed.com` — lead — *cible*
  - `39502419168` — Club Med — eff. 13727 — `clubmed.com` — lead — *cible*
  - `426690793662` — Club Med — eff. 13485 — `clubmed.com` — lead — *cible*
- **`gruyer.com`** ×3
  - `35663602937` — Indépendant — eff. 16554 — `gruyer.com` — lead — *cible*
  - `382517316818` — Indépendant — eff. 10892 — `gruyer.com` — lead — *cible*
  - `440466411725` — Indépendant — eff. 18061 — `gruyer.com` — lead — *cible*
- **`lapostegroupe.com`** ×3
  - `427646100690` — La Poste Groupe — eff. 56265 — `lapostegroupe.com` — lead — *cible*
  - `63126182077` — La Poste Groupe — eff. 56081 — `lapostegroupe.com` — lead — *cible*
  - `91722289390` — Le Groupe La Poste — eff. 56081 — `lapostegroupe.com` — lead — *cible*
- **`alstom.com`** ×2
  - `164991461569` — Alstom — eff. 87224 — `alstom.com` — lead — *cible*
  - `433006888172` — Alstom — eff. 87128 — `alstom.com` — lead — *cible*
- **`bsb-education.com`** ×2
  - `35716546749` — BSB - Burgundy School of Business — eff. 727 — `bsb-education.com` — customer — *client*
  - `96047668447` — Burgundy School of Business - BSB — eff. 727 — `bsb-education.com` — customer — *client*
- **`bulldozer-collective.com`** ×2
  - `317412132037` — Bulldozer — eff. 168 — `bulldozer-collective.com` — customer — *client*
  - `35683403999` — Bulldozer — eff. 2812 — `bulldozer-collective.com` — opportunity — *cible*
- **`carrefour.fr`** ×2
  - `159210887408` — Carrefour — eff. 100345 — `carrefour.fr` — lead — *cible*
  - `372574506194` — Carrefour — eff. 107232 — `carrefour.fr` — opportunity — *cible*
- **`cbainfo.fr`** ×2
  - `305421421767` — CBA + Ruche + Agathe You — eff. 261 — `cbainfo.fr` — customer — *client*
  - `305540276417` — CBA Informatique Libérale — eff. 261 — `cbainfo.fr` — customer — *client*
- **`credit-agricole.fr`** ×2
  - `131387466996` — Crédit Agricole Nord Midi-Pyrénées — eff. 2152 — `credit-agricole.fr` — lead — *cible*
  - `8946348531` — Crédit Agricole — eff. 2262 — `https://www.credit-agricole.fr/` — opportunity — *cible*
- **`danone.com`** ×2
  - `238300665061` — Danone — eff. 72700 — `danone.com` — lead — *cible*
  - `83945472224` — Danone — eff. 1596 — `danone.com` — lead — *cible*
- **`decathlon.fr`** ×2
  - `142476519640` — Decathlon France — eff. 24396 — `decathlon.fr` — lead — *cible*
  - `318635017459` — Decathlon France — eff. 27362 — `decathlon.fr` — lead — *cible*
- **`ey.com`** ×2
  - `101997815017` — EY — eff. 406259 — `ey.com` — lead — *cible*
  - `398471985400` — Ernst &amp; Young — eff. 408639 — `ey.com` — lead — *cible*
- **`fbd-group.com`** ×2
  - `317418783989` — Fbd Group — eff. 1560 — `www.fbd-group.com` — lead — *cible*
  - `441907665121` — FBD Group — eff. 1569 — `fbd-group.com` — lead — *cible*
- **`freelance.com`** ×2  ⚠️ **faux regroupement** : ce ne sont pas des doublons, c'est le champ `domain` qui contient une URL de réseau social / un lien court (cf. §7.1 et §7.3).
  - `10213000927` — Freelance.com — eff. 2468 — `freelance.com` — customer — *client*
  - `144803968207` — Ad's up Consulting | Groupe EDG — eff. 2468 — `freelance.com` — lead — *cible*
- **`groupe-bel.com`** ×2
  - `45255054560` — Bel — eff. 7773 — `groupe-bel.com` — lead — *cible*
  - `97625097411` — Bel — eff. 7773 — `groupe-bel.com` — lead — *cible*
- **`groupe-rocher.com`** ×2
  - `122785423574` — Yves Rocher — eff. 2666 — `groupe-rocher.com` — lead — *cible*
  - `122811171052` — Yves Rocher — eff. 2658 — `groupe-rocher.com` — lead — *cible*
- **`instagram.com`** ×2  ⚠️ **faux regroupement** : ce ne sont pas des doublons, c'est le champ `domain` qui contient une URL de réseau social / un lien court (cf. §7.1 et §7.3).
  - `317418782967` — The Bradery — eff. 49263 — `instagram.com` — lead — *cible*
  - `39502438609` — Les Idéateurs — eff. 57167 — `https://www.instagram.com/lesideateurs/` — lead — *cible*
- **`jobteaser.com`** ×2
  - `36283764962` — Jobteaser — eff. 213 — `jobteaser.com` — customer — *client*
  - `98475929846` — JobTeaser — eff. 213 — `jobteaser.com` — customer — *client*
- **`lactalis.com`** ×2
  - `238746576098` — Groupe Lactalis — eff. 22175 — `lactalis.com` — lead — *cible*
  - `97725598941` — Groupe Lactalis — eff. 22320 — `lactalis.com` — lead — *cible*
- **`mooncard.co`** ×2
  - `108068646114` — Mooncard — eff. 108 — `mooncard.co` — customer — *client*
  - `8945498324` — Mooncard — eff. 108 — `https://www.mooncard.co/` — customer — *client*
- **`nona.fr`** ×2
  - `25520235768` — nona — eff. None — `nona.fr` — customer — *client*
  - `426625492168` — nona — eff. 83 — `nona.fr` — customer — *client*
- **`ondira.com`** ×2
  - `434488706264` — Freelance — eff. 111960 — `ondira.com` — lead — *cible*
  - `440759900400` — Freelance — eff. 111960 — `ondira.com` — lead — *cible*
- **`orange-business.com`** ×2
  - `107968921828` — Orange Business Services — eff. 28631 — `orange-business.com` — opportunity — *cible*
  - `400749571320` — Orange Business Services — eff. 28563 — `orange-business.com` — opportunity — *cible*
- **`puig.com`** ×2
  - `149770091760` — Puig — eff. 9392 — `puig.com` — lead — *cible*
  - `431375236317` — Puig — eff. 11840 — `puig.com` — lead — *cible*
- **`societegenerale.com`** ×2
  - `168675795132` — Société Générale Assurances — eff. 1753 — `societegenerale.com` — lead — *cible*
  - `36322852030` — Société Générale — eff. 2036 — `societegenerale.com` — lead — *cible*

Grappes réellement actionnables dans cette liste (même entreprise, deux fiches) :
`arval.com` ×3, `clubmed.com` ×3, `lapostegroupe.com` ×3, `groupe-bel.com` ×2, `danone.com` ×2,
`ey.com` ×2, **`orange-business.com` ×2**, `groupe-rocher.com` ×2, `decathlon.fr` ×2, `puig.com` ×2,
`carrefour.fr` ×2, `alstom.com` ×2, `societegenerale.com` ×2, `fbd-group.com` ×2, `lactalis.com` ×2,
`mooncard.co` ×2, `nona.fr` ×2, **`bsb-education.com` ×2**, `jobteaser.com` ×2, `cbainfo.fr` ×2,
`credit-agricole.fr` ×2, `ondira.com` ×2, `gruyer.com` ×3, `bulldozer-collective.com` ×2.

Deux d'entre elles méritent un mot :

- **`gruyer.com` ×3** : trois fiches nommées `Indépendant` avec trois effectifs différents
  (16 554 / 10 892 / 18 061). Ce n'est pas un groupe, c'est du bruit d'enrichissement.
- **`bulldozer-collective.com` ×2** : l'agence elle-même est dans sa propre base, une fois en
  `opportunity` à 2 812 salariés (`35683403999`, faux) et une fois en `customer` à 168 (`317412132037`).
  La fiche `opportunity` remonte dans les **cibles**.

#### b) Nom normalisé identique, domaines différents ou absents — 47 grappes

Normalisation : accents retirés, casse ignorée, et les mots `sa / sas / sarl / group / groupe /
france / holding / international / corp / inc / ltd / the` supprimés — donc « Deloitte » et
« Deloitte France » tombent dans la même grappe.

**Grands comptes (21 grappes)** — celles qui polluent les cibles :

- **allianceautomotive** ×2
  - `238794856667` — Alliance Automotive Group France — eff. 1181 — `allianceautomotive.fr` — lead — *cible*
  - `316023163123` — Alliance Automotive Group — eff. 2841 — `allianceautomotivegroup.eu` — lead — *cible*
- **atos** ×2
  - `139996044531` — Atos — eff. 86195 — `atos.net` — lead — *cible*
  - `14895815157` — Atos — eff. 85171 — `atos.ai` — lead — *cible*
- **bnpparibas** ×2
  - `162003232956` — BNP Paribas — eff. 154110 — `bnpparibas.com` — opportunity — *cible*
  - `444265411828` — BNP Paribas — eff. 156578 — `group.bnpparibas` — lead — *cible*
- **bpifrance** ×2
  - `35716546793` — Bpifrance — eff. 6054 — `ext.bpifrance.fr` — lead — *cible*
  - `42729536753` — bpifrance — eff. 6106 — `bpifrance.fr` — opportunity — *cible*
- **carrefour** ×3
  - `159210887408` — Carrefour — eff. 100345 — `carrefour.fr` — lead — *cible*
  - `372574506194` — Carrefour — eff. 107232 — `carrefour.fr` — opportunity — *cible*
  - `9758969321` — Carrefour — eff. 107176 — `recrute.carrefour.fr` — lead — *cible*
- **cooperconsumerhealth** ×2
  - `238271653097` — Cooper Consumer Health — eff. 1310 — `cooperconsumerhealth.eu` — lead — *cible*
  - `400914516155` — Cooper Consumer Health — eff. 1310 — `cooperconsumerhealth.com` — opportunity — *cible*
- **culligan** ×2
  - `371899075782` — CULLIGAN FRANCE — eff. 828 — `culligan.fr` — customer — *client*
  - `85335732448` — CULLIGAN FRANCE — eff. 23605 — `https://www.linkedin.com/company/culligan-france` — customer — *client*
- **decathlon** ×3
  - `142476519640` — Decathlon France — eff. 24396 — `decathlon.fr` — lead — *cible*
  - `286680949977` — decathlon-group — eff. 9643 — `decathlon-united.com` — lead — *cible*
  - `318635017459` — Decathlon France — eff. 27362 — `decathlon.fr` — lead — *cible*
- **deloitte** ×2
  - `175256647883` — Deloitte France — eff. 477880 — `deloitte.com` — lead — *cible*
  - `85894744302` — Deloitte — eff. 1593 — `deloitte.fr` — lead — *cible*
- **edenred** ×3
  - `148839331035` — Edenred France — eff. 1031 — `edenred.fr` — lead — *cible*
  - `356569198800` — Edenred — eff. None — `None` — customer — *client*
  - `35737284834` — Edenred — eff. 8011 — `edenred.com` — customer — *client*
- **freelance** ×3
  - `271919000824` — Freelance — eff. 2143 — `shaneco.com` — lead — *cible*
  - `434488706264` — Freelance — eff. 111960 — `ondira.com` — lead — *cible*
  - `440759900400` — Freelance — eff. 111960 — `ondira.com` — lead — *cible*
- **glevents** ×2
  - `10008843215` — GL Events — eff. None — `None` — customer — *client*
  - `316023229674` — GL Events — eff. 6704 — `gl-events.com` — opportunity — *cible*
- **harmoniemutuelle** ×2
  - `103054088398` — Harmonie Mutuelle — eff. 4547 — `harmonie-mutuelle.fr` — opportunity — *cible*
  - `83477615824` — Harmonie Mutuelle — eff. 7181 — `groupe-vyv.fr` — lead — *cible*
- **hubspot** ×2
  - `35672605931` — HubSpot — eff. 12233 — `hubspot.com` — lead — *cible*
  - `8946361812` — Hubspot — eff. 12233 — `https://hubspot.fr` — customer — *client*
- **marsincorporated** ×2
  - `35670803676` — Mars, Incorporated — eff. 55970 — `effem.com` — lead — *cible*
  - `9301300961` — Mars, Incorporated — eff. 55970 — `mars.com` — customer — *client*
- **nielseniq** ×2
  - `116559423697` — NielsenIQ — eff. 29993 — `niq.com` — lead — *cible*
  - `315111213304` — NielsenIQ — eff. 29052 — `gfk.com` — lead — *cible*
- **openclassrooms** ×2
  - `9810670291` — openclassrooms — eff. 2628 — `openclassrooms.com` — opportunity — *cible*
  - `98962374873` — OpenClassrooms — eff. 3287 — `oc.cm` — lead — *cible*
- **pluxee** ×2
  - `300757267702` — Pluxee — eff. 5632 — `pluxeegroup.com` — opportunity — *cible*
  - `308585575621` — Pluxee France — eff. 364 — `pluxee.fr` — customer — *client*
- **pwc** ×3
  - `165231277258` — PwC — eff. None — `None` — customer — *client*
  - `35716546790` — pwc — eff. 298219 — `pwc.com` — lead — *cible*
  - `96487043269` — PwC France — eff. 4114 — `pwc.fr` — lead — *cible*
- **talan** ×2
  - `318635016398` — Talan — eff. 4629 — `talan.com` — customer — *client*
  - `356260075714` — Talan — eff. None — `None` — customer — *client*
- **veolia** ×2
  - `135970733258` — Veolia — eff. None — `sarpi.veolia.com` — customer — *client*
  - `36338670819` — Veolia — eff. 49551 — `sarpindustries.fr` — customer — *client*

**Petits comptes, presque tous côté clients (26 grappes)** — le motif est répétitif :
une fiche renseignée + une fiche fantôme sans domaine ni effectif, souvent avec un id de la
plage `1654…` ou `3150…`, ce qui ressemble à un **import qui a re-créé des fiches existantes** :

- **Abby** ×2 — `315014470882` / `35685191886` — domaines : None · abby.fr
- **Groupe BARCODIS** ×2 — `165481124052` / `83154406642` — domaines : None · barcodis.com
- **Betomorrow** ×2 — `165475742934` / `8945498554` — domaines : None · https://www.betomorrow.com
- **Bugali** ×2 — `165449450686` / `35716546780` — domaines : None · bugali.com
- **Cadoles** ×2 — `135152252123` / `165451254982` — domaines : cadoles.com · None
- **ClubFunding** ×3 — `165468444860` / `165475746030` / `315014457565` — domaines : None · None · clubfunding.fr
- **EVERTRUST** ×2 — `111113997527` / `165447653623` — domaines : evertrust.fr · None
- **getaround** ×2 — `239892853961` / `36297077947` — domaines : fr.getaround.com · getaround.com
- **go-kelvin.com** ×2 — `119293449418` / `165446882508` — domaines : go-kelvin.com · None
- **Hosman** ×2 — `165453762770` / `62812551414` — domaines : None · hosman.co
- **Imeon Energy** ×2 — `165446879441` / `8945498325` — domaines : None · https://imeon-energy.com
- **Intescia** ×2 — `315014470883` / `317410774227` — domaines : None · intescia-group.com
- **Kenko** ×2 — `165432954092` / `35685191924` — domaines : None · kenko.fr
- **konverso** ×2 — `12116608444` / `165481128166` — domaines : konverso.ai · None
- **lapremierebrique** ×2 — `316281714903` / `317418810569` — domaines : None · lapremierebrique.fr
- **Nuavo** ×2 — `165468557560` / `35991361766` — domaines : None · nuavo.com
- **Oversoc** ×2 — `11196298436` / `35665403089` — domaines : None · oversoc.com
- **Payplug** ×2 — `165468557555` / `35669001415` — domaines : None · payplug.com
- **Qobra** ×2 — `165231277264` / `35648812251` — domaines : None · qobra.co
- **Santévet** ×3 — `10849003764` / `10849029107` / `189486585077` — domaines : None · None · santevet.com
- **Service Botics** ×2 — `101894705381` / `317411454199` — domaines : service-botics.com · None
- **Simplébo** ×2 — `381289808085` / `50382433487` — domaines : simplebo.fr · capsurleweb.fr
- **Size-Factory** ×3 — `165473940719` / `165475742933` / `39943434478` — domaines : None · None · https://www.size-factory.com
- **skeeled** ×2 — `12520587972` / `165453765852` — domaines : skeeled.com · None
- **trustup-group** ×2 — `12301490662` / `165451254977` — domaines : trustup.group · None
- **UnlockM** ×2 — `165481124055` / `35740866755` — domaines : None · unlockm.fr

#### c) Noms très proches sans être identiques — 9 paires (similarité ≥ 0,88)

| Sim. | Fiche A | Fiche B | Verdict |
|---|---|---|---|
| 0.96 | `209299148006` Sophie d'agon (sophiedagon.com) | `445776503027` Sophie d'Argon (None) | doublon probable |
| 0.94 | `35716546749` BSB - Burgundy School of Business (bsb-education.com) | `317418882243` Burgundy School of Business (None) | doublon (3ᵉ fiche BSB) |
| 0.94 | `317418882243` Burgundy School of Business (None) | `96047668447` Burgundy School of Business - BSB (bsb-education.com) | doublon (3ᵉ fiche BSB) |
| 0.92 | `316281714884` Advenis (None) | `431489678542` Advens (advens.fr) | **faux positif** — Advenis ≠ Advens |
| 0.90 | `8946348531` Crédit Agricole (https://www.credit-agricole.fr/) | `188471091440` Crédit Agricole CIB (ca-cib.com) | entités distinctes (CIB ≠ CA) |
| 0.89 | `35716546749` BSB - Burgundy School of Business (bsb-education.com) | `96047668447` Burgundy School of Business - BSB (bsb-education.com) | doublon |
| 0.89 | `35658202354` Cegos France (cegos.fr) | `13829636594` ceos (ceos.fr) | **faux positif** — Cegos ≠ ceos |
| 0.89 | `36144254191` MACIF (macif.fr) | `317418888392` MAIF (maif.fr) | **faux positif** — MACIF ≠ MAIF |
| 0.89 | `101138896074` Qovoltis (qovoltis.com) | `37989006524` qovoltis.fr (qovoltis.fr) | doublon probable |

Trois des neuf paires sont des **faux positifs** de l'appariement par chaîne : MACIF/MAIF,
Advenis/Advens et Cegos/ceos sont des entreprises différentes. Ne pas fusionner sur la seule distance de nom.

#### d) Les quatre groupes signalés — vérification point par point

| Signalé | Constaté | Verdict |
|---|---|---|
| Veolia ≥ 3 fiches | **4 fiches** dans le portefeuille | **confirmé, et sous-estimé** |
| Orange Business Services 2 fiches | **2 fiches**, même domaine `orange-business.com` | **confirmé** |
| BSB 2 fiches | **3 fiches** (2 sur `bsb-education.com` + 1 sans domaine) | **confirmé, et sous-estimé** |
| CULLIGAN 2 fiches | **3 fiches** (2 `CULLIGAN FRANCE` + 1 `Culligan Water`) | **confirmé, et sous-estimé** |

**Veolia — 4 fiches**
  - `135970733258` — Veolia — eff. None — `sarpi.veolia.com` — customer — *client*
  - `179305666804` — Veolia Recyclage et Valorisation des Déchets — eff. 286 — `veolia.fr` — customer — *client*
  - `19976068547` — Veolia | Energie Performance — eff. 49551 — `veolia.com` — lead — *cible*
  - `36338670819` — Veolia — eff. 49551 — `sarpindustries.fr` — customer — *client*

**Orange Business Services — 2 fiches**
  - `107968921828` — Orange Business Services — eff. 28631 — `orange-business.com` — opportunity — *cible*
  - `400749571320` — Orange Business Services — eff. 28563 — `orange-business.com` — opportunity — *cible*

**BSB / Burgundy School of Business — 4 fiches**
  - `165446879440` — BSB — eff. None — `None` — customer — *client*
  - `317418882243` — Burgundy School of Business — eff. None — `None` — customer — *client*
  - `35716546749` — BSB - Burgundy School of Business — eff. 727 — `bsb-education.com` — customer — *client*
  - `96047668447` — Burgundy School of Business - BSB — eff. 727 — `bsb-education.com` — customer — *client*

**CULLIGAN — 3 fiches**
  - `109250051291` — Culligan Water — eff. 2190 — `culligan.com` — lead — *cible*
  - `371899075782` — CULLIGAN FRANCE — eff. 828 — `culligan.fr` — customer — *client*
  - `85335732448` — CULLIGAN FRANCE — eff. 23605 — `https://www.linkedin.com/company/culligan-france` — customer — *client*

Détail sur Veolia : trois domaines différents (`veolia.com`, `veolia.fr`, `sarpindustries.fr`,
`sarpi.veolia.com`) pour un même groupe, dont **une fiche `Veolia` cliente à 49 551 salariés posée
sur le domaine d'une filiale** (`sarpindustries.fr`) et une fiche `Veolia Recyclage` à 286 salariés.
Une fiche Veolia est côté **cible** (`19976068547`), trois côté **client** : le même groupe est
simultanément compté comme prospect et comme référence.

Détail sur CULLIGAN : les deux fiches `CULLIGAN FRANCE` affichent **23 605** et **828** salariés —
la première est une victime du bug LinkedIn de §7.1.

### 7.5 bis — 13 fiches clientes sans nom

Treize des 495 clients ont `name = null` alors que leur domaine est renseigné : `51545737419`
(tatoo-consulting.com), `104908018932` (prismy.io), `189484653796` (veesion.fr), `229427575025`
(glev.ai), `238233861310` (argile.ai), `239389020368` (kpiclub.com), `243528492269`
(bertrand-hospitality.com), `266425485545` (bulldozer-collective.fr), `290876749032` (reevo.fr),
`360313010392` (realestate.bnpparibas), `371020765402` (ski-planet.fr), `426102376685`
(vernaypaysage.fr), `427235783920` (audion.ai). Aucune n'a d'effectif. Un cockpit qui affiche
`name` montrera treize lignes vides : prévoir un repli sur `domain`.

À noter : `266425485545` est **bulldozer-collective.fr**, soit une troisième fiche de l'agence
elle-même dans sa propre base (après `35683403999` et `317412132037`, cf. §7.5).

### 7.6 — Les compteurs ne sont pas fenêtrables

`num_conversion_events`, `hs_analytics_num_visits`, `hs_analytics_num_page_views` et
`num_contacted_notes` sont **cumulés depuis la création de la fiche**. HubSpot n'expose aucun
équivalent borné à 30 / 90 / 180 jours. Un compte créé en 2023 avec 12 formulaires n'est donc pas
comparable à un compte créé en 2026 avec 3 — et le critère « ≥ 2 formulaires » qui sélectionne 232
des 553 cibles **n'a pas de fenêtre temporelle**.

Seules les propriétés de **type date** permettent de fenêtrer, et elles sont dans l'extraction :
`notes_last_contacted`, `notes_last_activity_date`, `first_conversion_date`, `recent_conversion_date`,
`createdate`. Sur 90 jours glissants (depuis le 23/06/2026) :

| | Cibles (553) | Clients (495) |
|---|---|---|
| contactées dans les 90 j (`notes_last_contacted`) | 144 (26,0 %) | 161 (32,5 %) |
| conversion dans les 90 j (`recent_conversion_date`) | 236 (42,7 %) | 71 (14,3 %) |

**C'est sur ces dates, et non sur les compteurs, que le cockpit doit construire sa fraîcheur.**
25 cibles n'ont aucun signal daté (ni contact ni conversion).

### 7.7 — Fibbler : les 90 jours sont un instantané, pas un historique

Les trois propriétés `fibbler_*_90_days` sont écrasées à chaque synchronisation. Elles disent
l'exposition des 90 derniers jours **au moment du dernier sync**, sans date de sync ni historique.
Elles ne permettent ni de dater une exposition, ni de comparer deux périodes.

### 7.8 — Breeze Intelligence inactif

Vérifié : `hs_intent_*` et `hs_most_recent_de_anonymized_visit` sont vides sur l'ensemble du portail.
Aucun signal d'intention tiers n'est disponible. Non extrait.

---

## 8. Structure du fichier `comptes.json`

Tableau JSON de **1048 objets**, **33 clés** chacun (les 27 champs demandés + `web_technologies`
+ `hs_ideal_customer_profile` + `scoring_lead` + les 3 `fibbler_*` + `population`).

Contrôles passés :

- 1048 objets — 553 `population = "cible"` + 495 `population = "client"`
- **1048 `hs_object_id` distincts** — aucun doublon d'identifiant
- aucun chevauchement entre les deux populations
- toutes les clés présentes sur tous les objets (valeur `null` quand la propriété est vide)
- aucun champ vide sur les 1 048 objets
- nombres typés en `int`/`float`, dates au format ISO 8601 (`…_iso` de HubSpot), pas de timestamp epoch

Attention en aval : **`hs_object_id` est une chaîne**, pas un entier (les ids dépassent 32 bits).

### Scripts

- `build.py` — reconstitue `comptes.json` depuis les fichiers `tool-results/*.txt`
- `analyse.py`, `analyse2.py` — remplissage, distributions, doublons
- `rapport.py` — génère ce document
- `_univers_1000.json` — les 2 029 fiches ≥ 1 000 salariés avant filtrage (base des constats §7.1)

---

## 9. Ce qu'il faut retenir avant de brancher le cockpit

1. **Les 553 cibles ne sont pas 553 entreprises.** Une dizaine sont des fiches fantômes entrées par
   le bug LinkedIn, et au moins 25 grappes de doublons de grands comptes se cachent dedans
   (Carrefour ×3, Decathlon ×3, Arval ×3, Club Med ×3, La Poste ×3, PwC ×3…). Le portefeuille réel
   est plus proche de **500–510 comptes distincts**.
2. **`numberofemployees` n'est pas fiable pour segmenter** : faux par le bas (Société Générale à 2 036),
   faux par le haut (Capgemini Invent à 342 871), et contaminé sur ~105 fiches de l'univers amont.
3. **Aucun scoring exploitable n'existe** : ni `lead_score_ia`, ni `scoring_v2_*`, et
   `hs_ideal_customer_profile` ne discrimine pas. Le scoring du cockpit est à construire.
4. **Les compteurs ne se fenêtrent pas.** La fraîcheur ne peut venir que des champs date.
5. **L'exposition LinkedIn ne recouvre pas la cible** : 80,7 % des comptes exposés sont hors périmètre.


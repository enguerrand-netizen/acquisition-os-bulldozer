# Dossiers 30 comptes nommés — rapport de constitution

Portail HubSpot Bulldozer `143561253` (eu1). Généré le 21/09/2026. Lecture seule : aucune création, modification ni suppression dans le CRM.

Fichier : `/private/tmp/claude-501/-Users-enguerrandchalvondemersay/a75e6ca6-5ff8-478d-bd1a-9a963b0419f5/scratchpad/acq/data/dossiers30.json` — 30 comptes, 536 contacts, 14 deals, 1142 activités (24 mois), 1613 signaux.

## 1. Méthode

**Fenêtre d'activité** : 21/09/2024 → 21/09/2026 (24 mois glissants), filtrée sur `hs_timestamp`.

**Chaîne de récupération**, un objet à la fois, jamais de compteur utilisé comme source de vérité :

| Bloc | Requête | Contrôle |
|---|---|---|
| Entreprise | `get_crm_objects(COMPANY, 30 ids)` | 30/30 renvoyés, `notFound` vide |
| Contacts | `SELECT … FROM CONTACT WHERE COMPANY.hs_object_id IN (30 ids)` | 536/536 — égal à la somme des `num_associated_contacts` |
| Deals | `search_crm_objects(DEAL, associatedWith)` puis `query_crm_data` pour le détail | `total` = 14, et 14 = somme des `num_associated_deals` |
| CALL / MEETING / TASK / NOTE | `… FROM <objet> WHERE COMPANY.hs_object_id IN (…)` | 343 / 80 / 36 / 137, chacun égal au `total` annoncé |
| EMAIL | union asc+desc pour les dates, puis `search_crm_objects` compte par compte pour l'attribution | 546 dans la fenêtre ; 556 tous temps, égal à la somme des 30 `total` |

**Pagination sans OFFSET.** `LIMIT` plafonne à 500 et `OFFSET` est ignoré sans erreur en cross-objet. Pour les deux jeux au-delà de 500 lignes (contacts 536, e-mails 546), la même requête a été jouée `ORDER BY hs_object_id ASC` puis `DESC` et les deux pages unionnées : 500 + 500 avec recouvrement couvrent l'ensemble et l'union redonne exactement le `total` annoncé. Aucune hypothèse sur l'ordre de tri (numérique ou lexicographique) n'est nécessaire.

**Cross-objet.** Contrairement à ce qui était craint, `SELECT COMPANY.hs_object_id FROM CONTACT` ne tronque **pas** quand la requête est contrainte par `WHERE COMPANY.hs_object_id IN (…)` : testé d'abord sur 3 comptes de volumétrie connue (SUEZ 5 + Docaposte 4 + Léon Grosse 4 = 13 lignes rendues, 13 attendues), puis vérifié à l'échelle (536 = 536). La troncature silencieuse concerne le balayage non contraint. Cette forme donne l'appariement contact→compte sans appel supplémentaire.

**Aucune recopie manuelle.** Les réponses de plus de ~45 Ko sont écrites par le MCP dans `tool-results/*.txt` et parsées en Python. Les réponses plus courtes arrivent en ligne et ne sont pas écrites sur disque : elles ont été relues depuis le transcript de session (`subagents/agent-*.jsonl`), qui les contient verbatim, plutôt que retapées. Tous les chiffres du fichier proviennent donc d'un parseur, pas d'une transcription.

**Rôles.** `role` ∈ decideur / praticien / technique / achat / autre / inconnu, dérivé de l'intitulé (FR+EN). Les intitulés concaténés par une virgule sont classés sur le **premier segment** (poste courant), avec repli sur la chaîne entière s'il ne donne rien. Précédence : achat > technique dirigeante (DSI/CTO/RSSI) > decideur > technique > praticien > autre. Un axe `seniorite` (c_level / direction / management / ic) est fourni en plus, parce que `role` seul ne dit pas qui signe. Les acronymes sont comparés avec frontières de mot : sans cela « Director » contient `cto`, « Enterprise » contient `erp` et « Unit director » contient `it director` — trois faux positifs techniques massifs corrigés.

**Répartition obtenue** : {'decideur': 218, 'inconnu': 165, 'praticien': 132, 'technique': 11, 'autre': 7, 'achat': 3}.

**Signaux.** Reconstitués à partir des **dates** uniquement, jamais des compteurs — `num_conversion_events`, `hs_email_open`, `hs_analytics_num_visits` sont cumulés depuis l'origine et ne sont pas fenêtrables. Chaque signal porte sa date, son type, le contact concerné quand il est identifiable, et un libellé.

**Répartition des signaux** : {'appel': 343, 'email_sortant': 327, 'email_entrant': 219, 'formulaire': 210, 'visite': 175, 'abonnement_linkedin': 115, 'clic_email': 108, 'meeting': 80, 'reponse_email': 36}.

## 2. Écarts de comptage, compte par compte

`contacts` = récupérés vs `num_associated_contacts` de la fiche. `joign.` = contacts dont le domaine e-mail correspond au domaine du compte. `sans` = contacts sans domaine e-mail. `autre` = domaine tiers.

| Compte | id | contacts | compteur | écart | joign. | sans | autre | % joign. | deals | dont auto | activités | signaux |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Veolia | Energie Performance | 19976068547 | 35 | 35 | +0 | 31 | 1 | 3 | 89% | 0 | 0 | 335 | 283 |
| loréal | 229193587951 | 131 | 131 | +0 | 6 | 113 | 12 | 5% | 1 | 1 | 43 | 123 |
| Content Square | 315914050757 | 16 | 16 | +0 | 15 | 1 | 0 | 94% | 1 | 0 | 95 | 104 |
| MGEN | 317411495156 | 10 | 10 | +0 | 9 | 0 | 1 | 90% | 1 | 0 | 94 | 104 |
| Société Générale | 36322852030 | 12 | 12 | +0 | 0 | 0 | 12 | 0% | 0 | 0 | 54 | 78 |
| Sage | 342918544596 | 8 | 8 | +0 | 8 | 0 | 0 | 100% | 1 | 0 | 56 | 67 |
| Schneider Electric | 317410706620 | 36 | 36 | +0 | 2 | 27 | 7 | 6% | 1 | 0 | 25 | 50 |
| Sodexo | 9770448590 | 15 | 15 | +0 | 10 | 3 | 2 | 67% | 1 | 0 | 46 | 63 |
| Berger-Levrault | 92346012914 | 7 | 7 | +0 | 3 | 1 | 3 | 43% | 1 | 0 | 50 | 64 |
| Groupe SEB | 140916864248 | 12 | 12 | +0 | 3 | 6 | 3 | 25% | 0 | 0 | 41 | 58 |
| Capgemini Invent | 175301965003 | 14 | 14 | +0 | 2 | 5 | 7 | 14% | 0 | 0 | 28 | 54 |
| Rothschild & Co | 316281684204 | 18 | 18 | +0 | 0 | 0 | 18 | 0% | 1 | 1 | 24 | 59 |
| Saint-Gobain Distribution Batiment France | 18938276038 | 21 | 21 | +0 | 15 | 4 | 2 | 71% | 0 | 0 | 15 | 38 |
| Pierre Fabre Group | 87436872902 | 19 | 19 | +0 | 5 | 12 | 2 | 26% | 0 | 0 | 16 | 43 |
| Stellantis | 316281698550 | 19 | 19 | +0 | 2 | 14 | 3 | 10% | 0 | 0 | 16 | 29 |
| Galileo Global Education | 316281711842 | 17 | 17 | +0 | 5 | 0 | 12 | 29% | 0 | 0 | 17 | 33 |
| Alpine | 148704214225 | 11 | 11 | +0 | 4 | 2 | 5 | 36% | 0 | 0 | 23 | 32 |
| SUEZ | 229907236085 | 5 | 5 | +0 | 1 | 0 | 4 | 20% | 1 | 0 | 25 | 34 |
| BNP Paribas | 162003232956 | 16 | 16 | +0 | 13 | 0 | 3 | 81% | 0 | 0 | 14 | 36 |
| Thales | 174866082014 | 16 | 16 | +0 | 4 | 9 | 3 | 25% | 0 | 0 | 13 | 30 |
| EssilorLuxottica | 143877777655 | 23 | 23 | +0 | 0 | 20 | 3 | 0% | 0 | 0 | 5 | 19 |
| Martell Mumm Perrier-Jouët | 14624157398 | 12 | 12 | +0 | 4 | 6 | 2 | 33% | 1 | 1 | 14 | 36 |
| KPMG International Limited | 59663610043 | 10 | 10 | +0 | 6 | 0 | 4 | 60% | 0 | 0 | 15 | 33 |
| Malakoff Humanis | 141529360630 | 6 | 6 | +0 | 4 | 0 | 2 | 67% | 1 | 1 | 18 | 32 |
| Michelin | 36289884362 | 13 | 13 | +0 | 2 | 9 | 2 | 15% | 0 | 0 | 10 | 19 |
| Keolis Trois Frontieres | 17818953714 | 9 | 9 | +0 | 7 | 0 | 2 | 78% | 1 | 0 | 14 | 19 |
| Léon Grosse | 36144254182 | 4 | 4 | +0 | 2 | 2 | 0 | 50% | 1 | 0 | 16 | 21 |
| TotalEnergies | 14793944264 | 11 | 11 | +0 | 6 | 0 | 5 | 55% | 0 | 0 | 8 | 24 |
| Christian Dior Couture | 238621997284 | 6 | 6 | +0 | 0 | 3 | 3 | 0% | 1 | 0 | 7 | 12 |
| Docaposte | 315014441197 | 4 | 4 | +0 | 0 | 1 | 3 | 0% | 0 | 0 | 5 | 16 |

**Écart de contacts : zéro sur les 30 comptes.** Les 536 contacts récupérés correspondent exactement, compte par compte, au compteur `num_associated_contacts`. Idem pour les deals (14 = 14) et pour chaque type d'activité (343 / 546 / 80 / 36 / 137, égaux aux `total` annoncés par le MCP).

**La joignabilité par domaine, elle, est faible et très inégale** : 169 contacts sur 536 (32%) portent le domaine e-mail de leur compte. 239 n'ont aucun domaine e-mail (45%) et 128 portent un domaine tiers (gmail, hotmail, ou une filiale). L'écart est mesuré compte par compte dans le tableau, pas extrapolé : il va de 0 % (Société Générale, Rothschild & Co, EssilorLuxottica, Christian Dior Couture, Docaposte) à 100 % (Sage).

## 3. Comptes pauvres en données

Classement par volume exploitable (contacts + activités sur 24 mois).

**Les 3 plus riches** — Veolia | Energie Performance (35 contacts, 335 activités, 283 signaux) · loréal (131 contacts, 43 activités, 123 signaux) · Content Square (16 contacts, 95 activités, 104 signaux).

**Les 3 plus pauvres** — Docaposte (4 contacts, 5 activités, 16 signaux) · Christian Dior Couture (6 contacts, 7 activités, 12 signaux) · TotalEnergies (11 contacts, 8 activités, 24 signaux).

Comptes à traiter avec prudence dans la fiche compte (moins de 20 activités sur 24 mois, ou 6 contacts ou moins) :

- **Saint-Gobain Distribution Batiment France** — 21 contacts (15 joignables par domaine), 15 activités, dernière activité 2026-08-21, 0 deal(s).
- **Pierre Fabre Group** — 19 contacts (5 joignables par domaine), 16 activités, dernière activité 2026-07-24, 0 deal(s).
- **Stellantis** — 19 contacts (2 joignables par domaine), 16 activités, dernière activité 2026-08-21, 0 deal(s).
- **Galileo Global Education** — 17 contacts (5 joignables par domaine), 17 activités, dernière activité 2026-04-21, 0 deal(s).
- **SUEZ** — 5 contacts (1 joignables par domaine), 25 activités, dernière activité 2026-09-04, 1 deal(s).
- **BNP Paribas** — 16 contacts (13 joignables par domaine), 14 activités, dernière activité 2026-03-09, 0 deal(s).
- **Thales** — 16 contacts (4 joignables par domaine), 13 activités, dernière activité 2026-02-10, 0 deal(s).
- **EssilorLuxottica** — 23 contacts (0 joignables par domaine), 5 activités, dernière activité 2025-09-30, 0 deal(s).
- **Martell Mumm Perrier-Jouët** — 12 contacts (4 joignables par domaine), 14 activités, dernière activité 2026-07-27, 1 deal(s).
- **KPMG International Limited** — 10 contacts (6 joignables par domaine), 15 activités, dernière activité 2026-08-06, 0 deal(s).
- **Malakoff Humanis** — 6 contacts (4 joignables par domaine), 18 activités, dernière activité 2026-08-24, 1 deal(s).
- **Michelin** — 13 contacts (2 joignables par domaine), 10 activités, dernière activité 2026-07-23, 0 deal(s).
- **Keolis Trois Frontieres** — 9 contacts (7 joignables par domaine), 14 activités, dernière activité 2026-05-05, 1 deal(s).
- **Léon Grosse** — 4 contacts (2 joignables par domaine), 16 activités, dernière activité 2025-09-25, 1 deal(s).
- **TotalEnergies** — 11 contacts (6 joignables par domaine), 8 activités, dernière activité 2025-07-02, 0 deal(s).
- **Christian Dior Couture** — 6 contacts (0 joignables par domaine), 7 activités, dernière activité 2026-07-01, 1 deal(s).
- **Docaposte** — 4 contacts (0 joignables par domaine), 5 activités, dernière activité 2026-07-08, 0 deal(s).

**6 comptes sans aucune activité depuis plus de 6 mois** : Sodexo (2026-03-13), BNP Paribas (2026-03-09), Thales (2026-02-10), EssilorLuxottica (2025-09-30), Léon Grosse (2025-09-25), TotalEnergies (2025-07-02).

## 4. Réserves

**L'objet COMMUNICATION est bloqué par le MCP** (LinkedIn, SMS, WhatsApp). Il n'a pas été interrogé. Tout échange passé par ces canaux est absent des dossiers — ce n'est pas une absence de signal, c'est une absence de mesure.

**L'abonnement LinkedIn n'est pas datable.** `date_de_following_linkeidn` est vide sur 536/536 contacts et `hs_social_linkedin_clicks` est vide sur toute la base. 115 contacts sont marqués `linkedin_follower__ = OUI` : ils figurent dans `signaux` avec `date: null` et `datable: false`, triés en fin de liste. Ne pas les placer sur une frise chronologique.

**Les ouvertures e-mail sont gonflées par Apple MPP** et ne doivent pas être lues comme un signal fort. Elles sont conservées par contact (`ouvertures_email_marketing`, `date_derniere_ouverture_email`) mais **ne génèrent aucun signal** : seuls les clics en produisent. Un scoring en aval doit peser les clics nettement au-dessus des ouvertures (×4 dans la convention retenue jusqu'ici).

**Un formulaire LinkedIn Lead Gen ne discrimine pas** : 29 comptes sur 30 (97%) en ont au moins un, signés comme non signés. Le sous-type est explicite dans chaque signal (`lead_gen_linkedin` vs `livre_blanc`, `barometre`, `template`, `typeform`, `newsletter`, `ressource`, `formulaire_site`) pour que la fiche compte puisse les distinguer visuellement.

**Seules deux dates de formulaire existent par contact** : `first_conversion_date` et `recent_conversion_date`. Les soumissions intermédiaires sont comptées (`num_conversion_events`) mais non datées : un contact à 10 formulaires ne produit que 2 signaux datés. La densité réelle est donc sous-estimée, et de façon inégale selon les comptes.

**Les visites ne sont datables qu'au dernier passage.** `hs_analytics_last_timestamp` donne la dernière session ; le nombre de visites est cumulé depuis l'origine. Un seul signal `visite` par contact, pas une série.

**Les e-mails sortants et entrants sont distingués.** La consigne ne prévoyait que `email_sortant` ; une réponse du prospect est un signal d'une autre nature qu'un envoi, donc le type `email_entrant` a été ajouté (327 sortants, 219 entrants). À traiter séparément dans tout scoring.

**L'attribution des e-mails a dû passer par 30 appels séparés.** `EMAIL` est un objet *hidden* dans la couche reporting (`HIDDEN_OBJECT_TYPE_USAGE_ERROR`) : `query_crm_data` bascule silencieusement sur un rendu objet qui **ignore la projection** et ne renvoie donc pas `COMPANY.hs_object_id`. Les 546 e-mails datés sont complets, mais leur rattachement au compte vient d'un `search_crm_objects` par compte. Contrôle : 556 identifiants uniques tous temps, égaux à la somme des 30 `total`, sans un seul écart.

**Les 14 deals sont tous perdus ou en standby, aucun gagné** (12 `Closed - DEAD`, 2 `Standby`), et 7 sur 14 n'ont pas de montant renseigné. 4 sont des créations automatiques issues de formulaires LinkedIn Lead Gen (`auto: true`) : Malakoff Humanis, L'Oréal, Martell Mumm Perrier-Jouët et ESSCA. Le libellé HubSpot contient une **espace insécable** avant le deux-points (`Nouvel élément\xa0: Deal`) — une recherche sur l'espace ordinaire n'en trouve aucun.

**Deux fiches entreprise sont incohérentes et fausseraient un ciblage firmographique :**

- **Rothschild & Co** (`316281684204`) porte le secteur `HIGHER_EDUCATION`, la ville *Angers* et le pays *Monaco*, et son unique deal s'appelle *ESSCA - Nouvel élément : Deal*. Les firmographies sont celles de l'ESSCA (école de commerce basée à Angers), pas de la banque. Le compte est en réalité un dossier ESSCA sous une mauvaise raison sociale.
- **Sodexo** (`9770448590`) est domicilié *Volgograd, Russian Federation*.
- Accessoirement : *Société Générale* est donnée à 2 036 salariés et *Capgemini Invent* à 342 871 (effectif du groupe Capgemini, pas de l'entité Invent). Les effectifs et CA de ces fiches viennent d'un enrichissement automatique et ne sont pas fiables au niveau entité.

**`notes_last_activity_date` et `total_revenue` sont vides sur les 30 fiches** : demandés explicitement, jamais renvoyés par HubSpot (qui omet les propriétés vides). Le champ `date_derniere_activite` est donc `null` partout ; utiliser `synthese.derniere_activite`, recalculé à partir des activités réellement datées.

**Le périmètre « 24 mois » ne s'applique qu'aux activités et aux signaux.** Les contacts, les deals et les propriétés d'entreprise sont donnés sans filtre de date, comme demandé.

**Veolia | Energie Performance est un client en cours de mission, pas un prospect.** Ses 335 activités incluent les comités stratégiques, kick-offs et points de mission. Le compte domine tous les classements de volume ; l'y comparer à des prospects froids n'a pas de sens.


# Vérification adversariale — `data/accounts.json`

Portail HubSpot Bulldozer `143561253` (eu1) · date de référence **21/09/2026** · 30 comptes.
Toutes les valeurs « attendu » ci-dessous ont été **requêtées directement dans HubSpot**
(`get_crm_objects`, `search_crm_objects`, `query_crm_data`), sans passer par les fichiers
intermédiaires de `data/`. Aucune écriture n'a été faite.

**~950 contrôles unitaires sur 9 points. 18 écarts retenus : 3 bloquants, 13 à corriger, 2 cosmétiques.**

Verdict par point :

| # | Point de contrôle | Contrôles | Écarts | Verdict |
|---|---|---|---|---|
| 1 | Compteurs de fiche COMPANY | 150 | **0** | conforme |
| 2 | Nombre de contacts récupérés | 30 | **0** | conforme |
| 3 | Transactions (nom/étape/montant/dates) | 100 | **0** | conforme |
| 4 | Dates `hist.loss.d`, `hist.open` | 33 | 1 | 1 cosmétique |
| 5 | Statut `jamais` / `perdu` / `encours` | 30 | 2 | 1 bloquant, 1 à corriger |
| 6 | Signaux (origine, bornes) | 536 | 4 | 4 à corriger |
| 7 | Activités (appels / e-mails / meetings) | 15 | 5 | 1 bloquant, 4 à corriger |
| 8 | Deux affirmations à réfuter | 2 | 0 | **les 2 confirmées** |
| 9 | Entités de groupe | 60 | 6 | 1 bloquant, 5 à corriger |

---

## Point 1 — Compteurs de chaque compte · **0 écart sur 150**

Comparaison des 30 `crmId` sur `num_associated_contacts`, `num_conversion_events`,
`hs_analytics_num_visits`, `num_contacted_notes`, `notes_last_contacted` (reconverti en
jours écoulés depuis le 21/09/2026).

**Je n'ai trouvé aucune erreur sur ce point.** Les 150 valeurs coïncident à l'unité près,
y compris les cas extrêmes : L'Oréal 131 contacts, Veolia 157 touches, Berger-Levrault
38 visites, TotalEnergies `dernierContact` = 446 j (2025-07-02).
`nomCRM` reproduit exactement le `name` HubSpot sur les 30 fiches, y compris les graphies
fautives du CRM (`loréal`, `Content Square`, `Saint-Gobain Distribution Batiment France`).

Exemples de recalcul de `dernierContact` :

| Compte | `notes_last_contacted` (HS) | Attendu (j) | Trouvé |
|---|---|---|---|
| Capgemini Invent | 2026-07-22T16:05:01Z | 61 | 61 |
| Contentsquare | 2026-09-17T07:48:40Z | 4 | 4 |
| EssilorLuxottica | 2025-09-30T13:53:12Z | 356 | 356 |
| Léon Grosse | 2025-09-25T14:42:05Z | 361 | 361 |
| TotalEnergies | 2025-07-02T08:24:17Z | 446 | 446 |

> Réserve : les 7 autres champs de `crm` (`contactsVus`, `ecart`, `joignables`, `sansEmail`,
> `dealsAuto`, `expoPub`, `engPub`) n'étaient pas dans le périmètre demandé et **n'ont pas
> été vérifiés**.

## Point 2 — Contacts réellement récupérés · **0 écart sur 30**

La consigne demandait 8 comptes. J'ai recompté **les 30**, en deux méthodes indépendantes :
`search_crm_objects` avec `associatedWith` (L'Oréal, Veolia) et un `SELECT COMPANY.hs_object_id,
COUNT(*) FROM CONTACT WHERE COMPANY.hs_object_id IN (…) GROUP BY COMPANY.hs_object_id`
pour les 30 (requête contrainte, donc non tronquée).

| Compte | Recompté HS | `contacts.length` |
|---|---|---|
| L'Oréal (le plus gros) | 131 | 131 |
| Schneider Electric | 36 | 36 |
| Veolia Énergie Performance | 35 | 35 |
| EssilorLuxottica | 23 | 23 |
| Saint-Gobain Distr. Bât. France | 21 | 21 |
| Christian Dior Couture | 6 | 6 |
| Malakoff Humanis | 6 | 6 |
| SUEZ | 5 | 5 |
| Docaposte (le plus petit) | 4 | 4 |
| Léon Grosse (le plus petit) | 4 | 4 |
| *(20 autres)* | = | = |

**Je n'ai trouvé aucune erreur sur ce point.** `crm.ecart` vaut 0 sur les 30 comptes et
c'est exact : aucun contact n'a été perdu à la récupération.

## Point 3 — Transactions · **0 écart sur 100**

14 transactions trouvées dans HubSpot pour les 30 comptes (`SELECT … FROM DEAL WHERE
COMPANY.hs_object_id IN (…)`). Le fichier en contient exactement 14, une par compte
concerné, et aucune sur les 16 autres comptes. Comparaison nom / étape / montant /
`createdate` / `closedate` :

| Compte | Nom (HS) | Étape | Montant HS | Montant fichier | Créé | Clôturé |
|---|---|---|---|---|---|---|
| Contentsquare | Contentsquare (New) - ABM | closedlost | **125 400** | 125 400 ✓ | 2025-02-14 ✓ | 2025-03-28 ✓ |
| Schneider Electric | Schneider Electric (New) | closedlost | **96 000** | 96 000 ✓ | 2025-03-18 ✓ | 2025-07-21 ✓ |
| SUEZ | SUEZ | closedlost | **48 000** | 48 000 ✓ | 2026-01-21 ✓ | 2026-03-12 ✓ |
| Léon Grosse | Léon grosse - Forecast | closedlost | **25 500** | 25 500 ✓ | 2025-02-24 ✓ | 2026-03-30 ✓ |
| Christian Dior Couture | Christian Dior Couture - AI Content Factory | closedlost | **25 000** | 25 000 ✓ | 2026-06-03 ✓ | 2026-07-01 ✓ |
| Sodexo | Sodexo : Update SEO | closedlost | **19 700** | 19 700 ✓ | 2025-11-28 ✓ | 2026-01-20 ✓ |
| MGEN | MGEN - Copywriter | Standby (555624160) | **17 400** | 17 400 ✓ | 2026-02-27 ✓ | 2026-06-17 ✓ |
| Sage | Sage | closedlost | (vide) | 0 ✓ | 2026-07-13 ✓ | 2026-09-16 ✓ |
| Berger-Levrault | Berger Levrault (New) | closedlost | (vide) | 0 ✓ | 2025-05-21 ✓ | 2025-12-01 ✓ |
| Keolis | Keolis | closedlost | (vide) | 0 ✓ | 2025-09-18 ✓ | 2026-01-22 ✓ |
| L'Oréal | L'Oréal - Nouvel élément : Deal | closedlost | (vide) | 0 ✓ | 2025-09-02 ✓ | 2026-03-30 ✓ |
| Malakoff Humanis | Malakoff Humanis - Nouvel élément : Deal | closedlost | (vide) | 0 ✓ | 2025-06-06 ✓ | 2026-03-30 ✓ |
| Martell Mumm P.-J. | Martell Mumm Perrier-Jouët - Nouvel élément : Deal | closedlost | (vide) | 0 ✓ | 2025-11-21 ✓ | 2025-12-24 ✓ |
| ESSCA | ESSCA - Nouvel élément : Deal | Standby (555624160) | (vide) | 0 ✓ | 2026-04-10 ✓ | 2026-04-23 ✓ |

**Les 7 montants cités dans l'outil sont exacts.** `hs_num_open_deals` = 0 sur les 30 fiches :
aucune transaction ouverte n'a été oubliée.

**Je n'ai trouvé aucune erreur sur ce point.**

### 3 bis — `hist.loss.reason` ne contient pas le motif de perte (cosmétique → à corriger)

| Deal | `hist.loss.reason` (fichier) | `closed_lost_reason` (HubSpot) |
|---|---|---|
| Léon grosse - Forecast | « Closed - DEAD » | **« Timing du projet reporté ou annulé »** |
| L'Oréal - Nouvel élément : Deal | (aucun hist) | « Timing du projet reporté ou annulé » |
| Malakoff Humanis - Nouvel élément : Deal | (aucun hist) | « Timing du projet reporté ou annulé » |
| Martell Mumm P.-J. - Nouvel élément : Deal | (aucun hist) | « Timing reporté » |

Le champ nommé `reason` contient en réalité le **libellé d'étape**, pas le motif. Le motif
existe dans le CRM et n'est jamais remonté. **Gravité : à corriger** — sur Léon Grosse
l'outil affiche « Closed - DEAD » là où le CRM dit « timing reporté », ce qui change le
diagnostic de réactivation.

## Point 4 — Dates · **0 écart sur 33, 1 champ annoncé absent**

`hist.loss.d` recalculé comme `(2026-09-21 − closedate)` pour les 11 comptes `perdu` :
542 / 427 / 294 / 244 / 242 / 193 / 175 / 96 / 82 / 5 / 5. **Les 11 valeurs sont exactes.**
`hist.loss.amt` et `hist.loss.label` correspondent aussi aux 11 deals.

| Écart | Attendu | Trouvé | Gravité |
|---|---|---|---|
| `hist.open` | présent sur les comptes à transaction ouverte | **absent des 30 comptes** (`hist` ne contient jamais que `loss`) | cosmétique |

Ce n'est pas une erreur de donnée : `hs_num_open_deals` = 0 partout, donc il n'y a
légitimement aucun `hist.open` à produire. Mais la spec annonce un champ que le
consommateur ne trouvera jamais — à retirer de la spec ou à documenter comme optionnel.

## Point 5 — Statut · 1 bloquant, 1 à corriger

Aucun compte `encours` (les 30 se répartissent en 19 `jamais` / 11 `perdu`).
Aucun `perdu` n'a de transaction ouverte : `hs_num_open_deals` = 0 sur les 30, et
`hs_is_closed` = true sur les 14 deals. **Ce sous-point est conforme.**

Les 4 comptes `jamais` qui portent pourtant une transaction (L'Oréal, Malakoff Humanis,
Martell, ESSCA) sont ceux dont le deal est marqué `auto: true`. La règle est cohérente et
reproductible : `auto` = le nom du deal contient « Nouvel élément : Deal » (le nom par
défaut de HubSpot). **Mais la règle est démentie par le CRM lui-même.**

| Écart | Attendu | Trouvé | Gravité |
|---|---|---|---|
| L'Oréal, Malakoff Humanis, Martell classés `jamais` (« transaction automatique, à ignorer ») | Un deal qualifié à la main n'est pas automatique : les 3 portent un `closed_lost_reason` **saisi manuellement** (« Timing du projet reporté ou annulé » ×2, « Timing reporté »), et ont un propriétaire nommé (E. Chalvon Demersay ×2, P.-A. Destremau) | `status = "jamais"` — l'outil affirme qu'on n'a jamais eu d'affaire avec eux | **bloquant** |
| MGEN classé `perdu` sur 17 400 € | Le deal est en étape **Standby**, pas « Closed - DEAD » | `hist.loss` avec `reason: "Standby"` — 17 400 € comptés en perte alors que l'affaire est suspendue | à corriger |

Sur le premier point : seul ESSCA a un deal réellement vierge (aucun motif, aucune trace de
qualification). Les 3 autres ont été travaillés puis perdus pour cause de timing —
exactement le profil qu'un cockpit de réactivation doit faire remonter, et qu'il masque.

Sur MGEN : HubSpot marque bien `hs_is_closed = true` pour Standby, donc le classement est
défendable — mais il faut alors traiter ESSCA (même étape Standby) de la même façon, ce qui
n'est pas le cas. La même étape produit deux statuts différents.

## Point 6 — Signaux · bornes conformes, 4 écarts de qualification

516 signaux au total. **Bornes : `d` ∈ [0 ; 339]. Aucun signal postérieur au 21/09/2026,
aucun antérieur à 340 jours. Aucun `who` ne pointe vers un contact inexistant.**
C'est conforme, sur les 516, pas sur un échantillon.

Échantillon de 20 signaux tirés au hasard (graine fixe, 12 comptes). Les 14 qui portent un
contact ont été retracés à la propriété HubSpot exacte :

| Compte | Signal | Date reconstituée | Propriété HubSpot | Valeur CRM | OK |
|---|---|---|---|---|---|
| Sage | click « dernier clic » c6 Angelika Wechner | 2026-01-07 | `hs_email_last_click_date` | 2026-01-07T14:53 | ✓ |
| L'Oréal | click « dernier clic » c100 Flora Talavera | 2025-11-25 | `hs_email_last_click_date` | 2025-11-25T13:29 | ✓ |
| Docaposte | click « premier clic » c1 Cécile BATT | 2026-04-15 | `hs_email_first_click_date` | 2026-04-15T12:18 | ✓ |
| MGEN | click « premier clic » c1 Françoise LY | 2026-04-28 | `hs_email_first_click_date` | 2026-04-28T06:31 | ✓ |
| Pierre Fabre | lgf c12 Anne-Sophie CAPPON | 2026-03-09 | `recent_conversion_date` + `_event_name` | 2026-03-09T18:13 / BOFU | ✓ |
| Sodexo | lgf c14 Aurélie Schlegel | 2026-05-18 | `first_conversion_date` | 2026-05-18T07:06 | ✓ |
| L'Oréal | lgf c129 Ai-Vân Trinh | 2025-12-28 | `recent_conversion_date` | 2025-12-28T07:40 | ✓ |
| Dior | lgf c4 Thalia Matoug | 2026-04-16 | `recent_conversion_date` | 2026-04-16T06:40 | ✓ |
| KPMG | page « 1 visite » c8 Rama Sow | 2026-06-04 | `hs_analytics_last_visit_timestamp` / `num_visits` | 2026-06-04T07:34 / 1 | ✓ |
| Pierre Fabre | page « 1 visite » c16 Cyril Guilbot | 2026-07-30 | idem | 2026-07-30T18:08 / 1 | ✓ |
| Sodexo | page « 2 visites » c0 Guillaume Berger | 2026-03-20 | idem | 2026-03-20T07:23 / 2 | ✓ |
| L'Oréal | page « 1 visite » c129 Ai-Vân Trinh | 2025-12-28 | idem | 2025-12-28T07:40 / 1 | ✓ |
| MGEN | reply c1 Françoise LY | 2026-06-17 | `hs_sales_email_last_replied` | 2026-06-17T17:00 | ✓ |
| Veolia | reply c27 M. Astasie / c3 E. Le Jemtel | 2026-09-17 | `hs_sales_email_last_replied` | 15:39 / 15:49 | ✓ |
| SUEZ | pricing c1 Coralie Renard | 2026-01-21 | `recent_conversion_date` | 2026-01-21T11:59 | ✓ date |

Les 6 restants (Veolia ×3, Contentsquare, Sage) sont des `reply` **sans contact** : ce sont
des objets EMAIL rattachés à la société seule. Le sujet et la date existent bien
(ex. « Re: Bulldozer x Contentsquare - Partenariat », 37 e-mails de ce fil dans HubSpot),
mais le signal ne peut être attribué à personne.

| # | Écart | Attendu | Trouvé | Gravité |
|---|---|---|---|---|
| 6.1 | Libellé `lgf` : « LinkedIn Lead Gen (**ne discrimine pas : 76 % des comptes en ont un**) », répété sur 122 signaux | La source (`spec/MODELE.md`) tire ce 76 % de l'étude outbound sur **4 754 comptes appelés**. Sur la cohorte affichée : **29/30 = 97 %** | Le chiffre d'une autre population est affiché sur la fiche d'un compte de celle-ci | à corriger |
| 6.2 | 2 signaux typés `pricing` / étape **BOFU** (SUEZ c1, MGEN c1) | Le libellé HubSpot est « Typeform (ID: vKGpSae6-v2-FmWQ4). Fields and questions must be updated on Typeform. » — le CRM **ne sait pas** ce qu'est ce formulaire | Requalifié en « pricing », le signal le plus fort du barème (×2) | à corriger |
| 6.3 | Le même Typeform `vKGpSae6` est le `first_conversion_event_name` d'Emmanuelle Le Jemtel (Veolia) | Même formulaire ⇒ même signal | Veolia n'a **aucun** signal `pricing`. La règle n'est pas appliquée uniformément | à corriger |
| 6.4 | **179 signaux sur 516 (35 %) ont `who: null`** — dont 94/117 chez Veolia, 26/41 chez MGEN, 20/31 chez Contentsquare | Un signal d'intention sert à savoir **qui** bouge | Un tiers des signaux ne nomme personne ; les comptes les plus « chauds » sont ceux où la part est la plus forte | à corriger |

## Point 7 — Activités · 1 bloquant, 4 à corriger

5 comptes contrôlés contre les objets CALL / EMAIL / MEETING associés.

| Compte | Appels HS | `sdr.log` | Meetings HS (dont futurs) | `sales.meetings` | E-mails HS (sortants/entrants) | `sent`/`replied` |
|---|---|---|---|---|---|---|
| Veolia | **31** | 31 ✓ | 46 (11 futurs) → 35 | 35 ✓ | 185 (91 / 94) | 91 / 94 ✓ |
| Contentsquare | **0** | 0 ✓ | 10 (0 futur) | 8 ✗ **−2** | 79 (41 / 38) | 40 / 37 ✗ **−1 / −1** |
| Sage | **23** | 23 ✓ | 0 | 0 ✓ | — | 18 / 9 |
| Sodexo | **17** | 17 ✓ | 5 | 5 ✓ | — | 14 / 5 |
| MGEN | **16** | 16 ✓ | 7 | 7 ✓ | — | 37 / 26 |

Les 11 meetings « manquants » de Veolia sont **tous postérieurs au 21/09/2026**
(2026-10-01 → 2027-03-12, comités récurrents) : leur exclusion est correcte, ce n'est pas
une erreur. Les 2 de Contentsquare sont en revanche des meetings **passés** (2024-07-31,
2024-06-21, soit d = 782 et 822 j) : la fenêtre de rétention des meetings n'est pas la même
d'un compte à l'autre.

| # | Écart | Attendu | Trouvé | Gravité |
|---|---|---|---|---|
| 7.1 | `outbound.replied` présenté comme le nombre de réponses à nos séquences | Chez Veolia, HubSpot compte **94 `INCOMING_EMAIL`** sur 185 e-mails : `replied` = nombre d'e-mails **entrants**, tous expéditeurs et tous fils confondus | `sent: 91, replied: 94` → **94 réponses pour 91 envois (103 %)**. Idem Berger-Levrault (17 / 14 = 121 %) et Contentsquare (37 / 40 = 92 %) | **bloquant** |
| 7.2 | `meetings[].out` (« tenu » / « noshow ») | Chez Veolia, **1 seul** des 46 meetings porte un `hs_meeting_outcome` (= COMPLETED) ; les 45 autres sont « Unassigned ». Chez Contentsquare : 0/10 | **78 des 80 meetings sont marqués « tenu »** sans aucun support CRM | à corriger |
| 7.3 | `meetings[].type` (R1 / R2 / R3 / COMITE) | 70 meetings typés R1 | **23 d'entre eux sont manifestement autre chose** : « Kick-off Meeting - Mission Forecast Veolia », « Pré-restitution mission Veolia DSE », « Road map 2026 Veolia », « recyclage.veolia.fr / restitution audit sémantique », « Juges - DX Awards Ceremonie », « Déjeuner - Jury Digital Experience Awards », « The Network Effect », « Soirée Lancement »… Tout compte de « R1 » est gonflé | à corriger |
| 7.4 | `outbound.opened` | HubSpot expose l'ouverture (`hs_email_open_count`) | **0 sur les 30 comptes** : la métrique n'est jamais alimentée. Une colonne toujours vide se lit comme « personne n'ouvre » | à corriger |
| 7.5 | `sdr.connects` et `sdr.convs` | Deux mesures distinctes | **Strictement identiques sur les 30 comptes** (= le nombre d'appels `out == "conv"`). `convs` n'apporte rien et double le signal à l'œil | à corriger |
| 7.6 | Contentsquare `sent` / `replied` / meetings | 41 / 38 / 10 | 40 / 37 / 8 | à corriger (écart d'1 à 2 unités, vraisemblablement un décalage de snapshot ou une fenêtre de rétention non documentée) |

## Point 8 — Les deux affirmations · **les 2 sont CONFIRMÉES**

### 8a — Fiche `316281684204` « Rothschild & Co » = ESSCA : **VRAI**

| Preuve | Valeur HubSpot |
|---|---|
| Contacts associés | **18/18** en `@essca.eu` ou `@essca.fr`. **Zéro** en `@rothschildandco.com` |
| Transaction associée | « **ESSCA** - Nouvel élément : Deal » (`498501785822`) |
| Nom / domaine de la fiche | « Rothschild & Co » / `rothschildandco.com` — tous deux erronés |

La correction portée par `noteNom` est justifiée et doit être conservée.

**Mais la correction ne va pas assez loin.** Les 18 contacts ne travaillent pas à l'ESSCA :
leur propriété `company` pointe vers 18 employeurs différents — Figaro Classifieds, PwC,
Praxedo, FERRANDI Paris, Wella Company, Computacenter, Surgiris, 5asec Business, Comet,
Château de Sours… Ce sont des **adresses d'anciens élèves** regroupées par domaine
e-mail. « ESSCA, 18 contacts associés » est un artefact de dédoublonnage par domaine, pas
un compte. Le traiter comme une cible ABM enverrait 18 messages à 18 sociétés différentes.
**Gravité : à corriger** — ajouter une note de périmètre, ou sortir la fiche des 30.

### 8b — Fiche `19976068547` « Veolia | Energie Performance » = client en mission : **VRAI**

`lifecyclestage = lead`, `status = "jamais"`, 0 transaction. Or :

| Preuve | Valeur HubSpot |
|---|---|
| Meetings | **46**, dont un « **Kick-off Meeting - Mission Forecast** Veolia x Bulldozer » (2026-01-15) |
| Comités récurrents | « Comité Stratégique - Veolia x Bulldozer » **tous les mois**, du 2026-01-12 au **2027-03-12** (réservés au-delà de la date de référence) |
| Points de mission | « Veolia Collec. x Bulldozer - **point mission** » récurrent, « Pré-restitution **mission** Veolia DSE », « **restitution** audit sémantique » |
| Volume relationnel | 157 `num_contacted_notes`, 185 e-mails, 31 appels, 35 contacts |
| Groupe | 2 fiches Veolia en `lifecyclestage = customer` (`179305666804`, `36338670819` / `135970733258`) |

Une agence ne tient pas un comité stratégique mensuel programmé 18 mois à l'avance avec un
prospect. Le `lead` du CRM est faux ; le classement `jamais` de l'outil en hérite.
**Gravité : à corriger** — la donnée du fichier est fidèle au CRM, mais l'affichage
« prospect jamais travaillé » sur un client actif est trompeur. Ajouter un garde-fou
« signaux de mission détectés ».

## Point 9 — Entités de groupe · 1 bloquant, 5 à corriger

**Existence : les 20 entités listées existent toutes dans HubSpot. Aucune fiche fantôme.**
**Statut : les 4 entités marquées `client: true` sont bien en `lifecyclestage = customer`.**

| Entité `client: true` | ID HubSpot | `lifecyclestage` | OK |
|---|---|---|---|
| Veolia Recyclage et Valorisation des Déchets (67 552 €) | 179305666804 | customer | ✓ |
| Veolia (37 400 €) | 36338670819 **et** 135970733258 | customer (les deux) | ✓ mais ambigu |
| Pluxee France (31 300 €) | 308585575621 | customer | ✓ |
| BNP Paribas Real Estate — « fiche sans nom au CRM » (39 620 €) | 360313010392 (`realestate.bnpparibas`, `name` vide) | customer | ✓ la note est exacte |

### Faux rattachements encore présents

Les deux déjà retirés (« Peugeot Frères Industrie » chez Stellantis, « Cours Thalès » chez
Thales) sont bien absents. **Il en reste six de la même famille :**

| # | Entité | Rattachée à | Réalité | Gravité |
|---|---|---|---|---|
| 9.1 | **Pluxee** + **Pluxee France** | Sodexo | Pluxee a été **scindée de Sodexo en février 2024** et est une société cotée indépendante (`pluxeegroup.com`). Les 2 fiches ne sont plus dans le groupe Sodexo — et **Pluxee France porte 31 300 € de CA attribués au groupe Sodexo** | **bloquant** |
| 9.2 | **Louis Vuitton** (`35685191921`) | Christian Dior Couture | Sœur au sein de LVMH, pas une filiale de Dior Couture | à corriger |
| 9.3 | **LVMH Fragrance Brands** (`178335810782`) | Christian Dior Couture | Idem. Les vraies fiches liées — « Parfums Christian Dior » (`238794827976`), « Christian Dior » (`427647892693`) — ne sont **pas** listées | à corriger |
| 9.4 | **Harmonie Mutuelle** (`103054088398`) | MGEN | Mutuelle **sœur** au sein du Groupe VYV, pas une filiale de MGEN | à corriger |
| 9.5 | **Geopost** (`10941420528`) | Docaposte | Sœur : Geopost et Docaposte sont deux filiales de La Poste Groupe. Les vraies filiales de Docaposte — « Index Éducation, filiale de Docaposte » (`317410772182`), « Docaposte Agility » (`448412136649`) — ne sont **pas** listées | à corriger |

### Hiérarchies inversées (la maison mère listée en `filiale`)

| Groupe affiché | Entité listée `kind: "filiale"` | Réalité |
|---|---|---|
| Docaposte | **La Poste Groupe** | maison mère |
| Alpine | **Renault Group** | maison mère |
| Saint-Gobain Distr. Bât. France | **Saint-Gobain** | maison mère |
| Veolia \| Energie Performance | **Veolia** | maison mère |

Sans conséquence sur les chiffres (tous `client: false`, `ca: 0`), mais l'arbre de groupe
affiché est faux. **Gravité : à corriger.**

### Entités sans identifiant

| # | Écart | Attendu | Trouvé | Gravité |
|---|---|---|---|---|
| 9.6 | Aucune entité ne porte de `crmId` | Un identifiant permettant de retrouver la fiche | Désignation par le seul nom, **ambiguë quand le CRM contient des homonymes** : « Veolia » = 3 fiches (dont 2 customer) ; « Saint-Gobain » = 2 fiches dont une au domaine **`foundever.com`** (Foundever, sans rapport) ; « Pluxee » = 2 fiches ; « Harmonie Mutuelle » = 2 fiches ; « Renault Group » = 3 fiches. Le CA de 37 400 € attribué à « Veolia » ne peut pas être rattaché à une fiche précise | à corriger |

## Écarts entre fichiers (hors périmètre CRM)

| Écart | Attendu | Trouvé | Gravité |
|---|---|---|---|
| `provenance.json` vs `accounts.json` | même nombre de deals | `provenance` annonce `deals: 0` pour L'Oréal, ESSCA, Malakoff, Martell, là où `accounts.json` en a 1 (les deals `auto`). Deux fichiers censés se recouper disent deux choses | cosmétique |

---

# Corrections à faire, par ordre de priorité

## Bloquant — à traiter avant toute lecture chiffrée

1. **Renommer `outbound.replied`** en `mailsEntrants` (ou recalculer une vraie réponse à
   séquence) et **interdire l'affichage d'un taux de réponse** `replied / sent` : la valeur
   dépasse 100 % sur Veolia (94/91) et Berger-Levrault (17/14). Tant que ce n'est pas fait,
   tout « taux de réponse outbound » de l'outil est faux.
2. **Détacher Pluxee et Pluxee France du groupe Sodexo** (scission de février 2024) et
   **retirer les 31 300 € de CA** du périmètre Sodexo, ou documenter explicitement qu'il
   s'agit d'un CA hérité d'avant la scission.
3. **Requalifier L'Oréal, Malakoff Humanis et Martell Mumm Perrier-Jouët** : leur deal porte
   un motif de perte saisi à la main, ils ne sont pas `jamais`. Restreindre le marqueur
   `auto` aux deals qui n'ont **ni motif de perte, ni propriétaire, ni activité** — ce qui ne
   laisse qu'ESSCA.

## À corriger — fausse lecture possible

4. Ne plus marquer `out: "tenu"` par défaut : 78 meetings sur 80 n'ont aucun
   `hs_meeting_outcome` dans le CRM. Utiliser un troisième état « non renseigné ».
5. Revoir le typage R1/R2/R3 : 23 des 70 « R1 » sont des comités de mission, restitutions ou
   événements. Exclure au minimum les titres contenant « mission », « comité »,
   « restitution », « kick-off », « awards », « jury », « soirée ».
6. Retirer les faux rattachements de groupe : **Louis Vuitton** et **LVMH Fragrance Brands**
   (Dior), **Harmonie Mutuelle** (MGEN), **Geopost** (Docaposte). Ajouter à la place les
   vraies filiales présentes au CRM (Parfums Christian Dior, Index Éducation, Docaposte Agility).
7. Ajouter un `crmId` à chaque entité : 5 noms de groupe sur 6 sont ambigus au CRM, dont un
   « Saint-Gobain » qui pointe potentiellement sur une fiche au domaine `foundever.com`.
8. Corriger les 4 hiérarchies inversées (La Poste Groupe, Renault Group, Saint-Gobain,
   Veolia listés en `filiale` de leur propre filiale).
9. Remplacer « 76 % des comptes en ont un » dans le libellé `lgf` : ce chiffre vient de
   l'étude sur 4 754 comptes appelés, il vaut **97 %** sur les 30 affichés. Soit citer la
   source dans le libellé, soit recalculer sur la cohorte.
10. Déclasser les 2 signaux `pricing` / BOFU adossés au Typeform `vKGpSae6` : le CRM ne sait
    pas ce qu'est ce formulaire. Et appliquer la même règle à Veolia, qui a le même
    formulaire et aucun signal `pricing`.
11. Afficher un garde-fou « mission en cours » sur Veolia `19976068547` : comités mensuels
    réservés jusqu'en mars 2027, kick-off de mission, 157 touches — l'étiquette
    « prospect jamais travaillé » est trompeuse.
12. Ajouter une note de périmètre sur ESSCA `316281684204` : les 18 contacts sont des
    adresses d'anciens élèves rattachées à 18 employeurs différents, ce n'est pas un compte.
13. Remonter le vrai `closed_lost_reason` dans `hist.loss.reason` (aujourd'hui c'est le
    libellé d'étape). Léon Grosse affiche « Closed - DEAD » là où le CRM dit
    « Timing du projet reporté ou annulé ».
14. Trancher le cas des deals en étape **Standby** : MGEN est `perdu` (17 400 € en perte),
    ESSCA est `jamais`. Même étape, deux traitements.
15. Alimenter `outbound.opened` (0 sur les 30 comptes) ou retirer la colonne.
16. Supprimer `sdr.convs`, strictement égal à `sdr.connects` sur les 30 comptes.
17. Documenter la fenêtre de rétention des meetings : Veolia est coupé aux meetings passés,
    Contentsquare perd 2 meetings passés de 2024 (d = 782 et 822 j).
18. Attribuer ou marquer les 179 signaux (35 %) sans contact, concentrés sur les comptes les
    plus chauds (Veolia 94/117, MGEN 26/41, Contentsquare 20/31).

## Cosmétique

19. Retirer `hist.open` de la spec, ou le documenter comme optionnel : aucun compte n'a de
    transaction ouverte, le champ n'apparaît jamais.
20. Réaligner `provenance.json` et `accounts.json` sur le comptage des deals `auto`.

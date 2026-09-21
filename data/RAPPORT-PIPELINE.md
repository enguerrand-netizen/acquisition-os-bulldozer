# Pipeline & activité commerciale Bulldozer — extraction CRM 24 mois

Portail HubSpot **Bulldozer 143561253 (eu1)**. Fenêtre **21/09/2024 → 21/09/2026**, découpe mensuelle.
Extraction **en lecture seule** : aucun objet créé, modifié ou supprimé.

Fichiers produits, dans ce dossier :
- `pipeline.json` — référentiel d'étapes, deals par mois, photo du pipe, conversion, 2 005 deals détaillés, sources
- `activite.json` — CALL / EMAIL / MEETING / TASK / NOTE par mois et par propriétaire
- `RAPPORT-PIPELINE.md` — ce document

---

## 1. Méthode

**Périmètre.** Seul le pipeline `default` (« Pipeline des ventes ») est analysé : **2 005 deals créés** dans la
fenêtre. Les autres pipelines contiennent **74 deals** sur la période, tous dans `Outbound Pipeline`
(764765371) — ils sont exclus de tous les chiffres. `Upsell pipeline`, `Podcast` et `AO` : 0 deal sur la fenêtre.
Toutes périodes confondues, `default` porte 2 413 deals.

**Extraction.** `query_crm_data` en 5 tranches de dates de création (351 à 454 lignes chacune, toutes sous le
plafond de 500), puis 5 tranches identiques pour les dates d'entrée en étape (`hs_v2_date_entered_*`).
`OFFSET` n'a pas été utilisé : la pagination se fait par plages de dates disjointes, et chaque réponse indique
`Showing N of N` — aucune tranche n'a été tronquée. Les réponses dépassant ~50 Ko sont écrites par le MCP dans
`tool-results/*.txt` ; elles ont été parsées en Python, jamais lues à l'œil.

**Contrôles passés.** Après dédoublonnage par `hs_object_id` : **2 005 deals uniques**, et
(a) le nombre de deals par mois de création est identique, mois par mois, à un `GROUP BY DATE_TRUNC` indépendant ;
(b) le nombre de deals par étape est identique à un `GROUP BY dealstage` indépendant ;
(c) pour chacun des 5 types d'activité, la somme des volumes par mois égale exactement la somme par
propriétaire (27 722 / 53 722 / 7 880 / 48 950 / 29 839).

**Montants.** `amount_in_home_currency` uniquement, jamais `amount`. Devise du portail : EUR.

---

## 2. Les totaux

| | Volume |
|---|---|
| Deals créés (pipeline `default`) | **2 005** |
| dont créés automatiquement (LinkedIn Lead Gen) | **434** (21,6 %) |
| Deals gagnés (étape actuelle `Closed - WON`) | **669** |
| Deals perdus, toutes sorties confondues | **1 015** |
| — `Closed - DEAD` | 733 |
| — `Standby` | 216 |
| — `No Show` | 29 |
| — `Lead non-qualifié` | 37 |
| Deals encore ouverts au 21/09/2026 | **321** |

1 015 sorties, pas 733 : **`Closed - DEAD` seul ne décrit que 72 % des pertes.** Un cockpit qui ne compte
que `closedlost` sous-estime les pertes de 282 deals. `Standby` en particulier n'est pas une étape vivante :
c'est un cimetière (216 deals, dont aucun n'a bougé).

**Flux par date de clôture** (inclut des deals créés avant la fenêtre) : 689 signatures pour **22,58 M€**,
788 `Closed - DEAD` pour 6,60 M€.

Activité commerciale sur 24 mois : **168 113 activités** — EMAIL 53 722, TASK 48 950, NOTE 29 839,
CALL 27 722, MEETING 7 880.

---

## 3. Le taux de conversion : deux chiffres, un seul est utilisable

### 3.1 Avec et sans les deals automatiques

**434 deals** portent « Nouvel élément : Deal » (ou `: Paid`, `: R1`, `:Test Heri`) dans leur nom — des
créations issues des formulaires LinkedIn Lead Gen. **2 seulement ont été gagnés.**

| Population | Deals | Gagnés | Création → signature |
|---|---|---|---|
| Tous les deals `default` | 2 005 | 669 | **33,4 %** |
| Hors deals automatiques | 1 571 | 667 | **42,5 %** |
| Deals automatiques seuls | 434 | 2 | **0,46 %** |

Les 434 sont exclus de tous les taux de référence. Les compter dilue le taux de 9 points sans rien dire du
travail commercial.

### 3.2 Pourquoi « 42,5 % » n'est pas un taux de conversion

Sur les 667 deals gagnés hors automatiques, **572 (86 %) ne sont jamais passés par l'étape R1** : ils ont été
créés dans le CRM au moment de la signature (upsell, régie, TDT, renouvellement). Leur durée médiane
création → signature est de **0 jour**. Ce ne sont pas des rendez-vous convertis, ce sont des lignes de
facturation enregistrées.

Le taux commercial réel est celui-ci :

| Entonnoir réel, hors deals automatiques | |
|---|---|
| Deals passés par R1 | **714** |
| → signés | **95** |
| → `Closed - DEAD` | 329 |
| → encore ouverts ou morts autrement | 290 |
| **Taux R1 → signature** | **13,3 %** |
| **Durée médiane R1 → signature** | **36 jours** (moyenne 51 j) |

Avec les deals automatiques : 1 098 entrées en R1, 97 signatures, **8,8 %**.
Deals automatiques seuls : 384 entrées en R1, 2 signatures, **0,5 %**.

**C'est 13,3 % qu'il faut afficher dans le cockpit, pas 42,5 %.**

### 3.3 Durée de cycle

Médiane globale création → signature : **1 jour** — chiffre à ne pas publier tel quel, il mesure surtout la
saisie tardive. Distribution sur les 667 gagnés hors automatiques :
0–1 j : 352 (53 %) · 2–7 j : 50 · 8–30 j : 129 · 31–90 j : 92 · > 90 j : 44.

La seule médiane défendable est celle des 95 deals réellement passés par R1 : **36 jours**.

---

## 4. Le pipe au 21/09/2026

321 deals ouverts (hors `Standby`, `No Show`, `Lead non-qualifié`, qui sont des sorties).

| Étape | Deals | Montant cumulé | Deals avec montant |
|---|---|---|---|
| R1 - Appointment Scheduled (20 %) | 231 | 0 € | **0 / 231** |
| Lead Qualifié | 28 | 80 000 € | 2 / 28 |
| R2 - planifié | 16 | 75 950 € | 4 / 16 |
| R2 - Réalisé | 26 | 499 300 € | 17 / 26 |
| Négociations | 16 | 332 450 € | 14 / 16 |
| Verbal Commitment | 4 | 127 800 € | 4 / 4 |
| Devis envoyé | 0 | — | — |
| Check avant signature | 0 | — | — |
| **Total** | **321** | **1 115 500 €** | **41 / 321** |

**Le montant du pipe est faux et doit être affiché comme tel.** 280 des 321 deals ouverts (87 %) n'ont aucun
montant. 1 115 500 € n'est pas la valeur du pipe : c'est la somme des 41 deals qui ont été chiffrés. Aucun
montant moyen ne doit être extrapolé sur les 280 autres.

Les étapes `Devis envoyé` et `Check avant signature` existent dans le référentiel mais sont **vides** — et
`Check avant signature` n'a même pas de propriété `hs_v2_date_entered_*`, signe qu'elle n'a jamais servi.
`Devis envoyé`, en revanche, est traversée : 326 deals hors automatiques y sont passés, presque toujours
quelques secondes avant le passage en `Closed - WON` (c'est une étape de formalité, pas d'attente).

---

## 5. Les sources

**La seule propriété exploitable est `source__inbound__outbound_etc__` sur DEAL : remplie sur 1 410 deals
sur 2 005, soit 70,3 %.**

| Source | Deals créés | Deals gagnés |
|---|---|---|
| (non renseigné) | 595 | 314 |
| Website | 343 | 67 |
| Paid | 282 | 7 |
| Outbound | 280 | 11 |
| Intro | 210 (+1 « Partenariat;Intro ») | 60 |
| Upsell / Crossell | 161 | 152 |
| Autre | 73 | 29 |
| Organic | 46 | 18 |
| Partenariat | 13 | 11 |
| Inbound | 1 | 0 |

Lecture prudente : `Upsell / Crossell` signe à 94 %, `Paid` à 2,5 %. Mais 314 des 669 signatures (47 %) sont
sans source — la comparaison entre canaux porte donc sur à peine plus de la moitié des deals gagnés.

**Les autres pistes de source, testées et écartées :**

- `origine_du_lead` **n'existe pas sur DEAL** — la requête est rejetée par le schéma. Elle existe sur CONTACT,
  et n'y est renseignée que sur ~535 lignes de jointure deal↔contact sur 2 042, soit ~27 % (et ce chiffre est
  gonflé par les deals multi-contacts). Non exploitable.
- `source_r1` existe sur DEAL et est **vide sur 2 005 deals sur 2 005**.
- `hs_analytics_source` est remplie à 96,8 %, mais **54 % des valeurs sont « Offline Sources »**, c'est-à-dire
  « créé à la main dans le CRM » — aucune information d'origine. Elle ne sert qu'à isoler
  `Paid Social` (502 deals, le flux LinkedIn Lead Gen) et `Direct Traffic` (241).
- `hs_object_source_label` est remplie à 100 % mais décrit le **mode** de création (CRM_UI 1 472,
  INTEGRATION 513, CLONE_OBJECTS 20), pas l'origine du lead. À noter : les 434 deals « Nouvel élément »
  sont tous étiquetés `CRM_UI / Unassigned` — **le mode de création ne permet pas de les repérer**, seul le
  nom le permet.

---

## 6. Ce qui rend un chiffre fragile

1. **Mois partiels.** Septembre 2024 ne couvre que du 21 au 30 (12 deals créés) et septembre 2026 que du 1er
   au 21 (29 deals). Ces deux mois ne se comparent pas aux 23 autres ; ils sont marqués `"partiel": true`
   dans les deux JSON.
2. **Secteur, offre et montant ne sont renseignés qu'à la signature.** Montant présent sur 657 des 669 deals
   gagnés (98 %), sur 209 des 733 `Closed - DEAD` (29 %), et sur **0 des 231 deals en R1**. Ces champs ne
   peuvent servir ni à prédire, ni à valoriser le pipe, ni à segmenter les deals ouverts.
3. **105 deals sur 2 005 ont une `closedate` antérieure à leur `createdate`** (reprise d'historique). Ils sont
   exclus des calculs de durée. Les durées sont calculées sur `hs_v2_date_entered_closedwon`, pas sur
   `closedate`, plus fiable.
4. **493 deals non clos portent quand même une `closedate`** : c'est une date prévisionnelle posée
   automatiquement par HubSpot. Ne jamais compter « gagné » ou « perdu » sur la seule présence d'une
   `closedate` — les comptages de ce rapport filtrent sur `dealstage`.
5. **Les étapes sont massivement sautées.** 377 deals n'ont aucun passage d'étape enregistré avant leur étape
   finale. Le bloc `passage_etape_a_etape` de `pipeline.json` est fourni dans l'ordre déclaré du pipeline, mais
   il produit des ratios supérieurs à 100 % (ex. 148 passages en `Verbal Commitment` pour 326 en
   `Devis envoyé`) : **ce n'est pas un entonnoir séquentiel**, c'est un comptage de passages. Seul
   `entonnoir_reel_depuis_R1` est interprétable.
6. **Divergence assumée sur le comptage des deals automatiques.** La consigne annonçait 292 deals
   « Nouvel élément : Deal ». J'en mesure **434** sur la fenêtre (416 avec le suffixe exact `: Deal`, plus
   16 `: Paid`, 1 `: R1`, 1 `:Test Heri`), dont **2 gagnés** et non 1. Le nom contient une espace insécable
   (` `) avant les deux-points — un filtre écrit avec une espace normale ne les trouve pas. Les mois de
   pointe sont mars 2025 (57), juin 2026 (48), mai 2025 (43).
   De même pour les pertes : la consigne annonçait ~1 020 (DEAD 715 / Standby 218 / No Show 29 / NQ 58) ;
   je mesure **1 015** (733 / 216 / 29 / 37) sur les deals *créés* dans la fenêtre. Les 58 « non qualifiés »
   de la consigne correspondent aux 37 de `default` **plus** 21 de l'`Outbound Pipeline`, qui est hors
   périmètre ici.
7. **`COMMUNICATION` est bloqué par le MCP.** Les messages LinkedIn, SMS et WhatsApp ne sont pas comptés.
   Pour une équipe dont le canal principal de prospection est LinkedIn, **le volume d'activité de ce rapport
   est un plancher**, pas un total.
8. **Les TASK sont datées par leur échéance**, pas par leur création (`hs_timestamp` = due date sur cet objet).
   Des tâches à échéance future gonflent les mois à venir et vident le mois en cours : septembre 2026 n'affiche
   que 448 tâches. Les pics d'octobre 2025 (7 408) et juillet 2026 (7 189) sont des vagues d'échéances, pas des
   journées de travail.
9. **Le périmètre de `activite.json` est le portail entier**, pas seulement les activités rattachées à un deal
   du pipeline `default`. Les deux fichiers ne se recoupent donc pas deal par deal.
10. **12 deals sont associés à plus d'une entreprise** — la jointure cross-objet les dédouble. Ils ont été
    dédoublonnés par `hs_object_id` et `company_ids` est une liste. 1 830 deals sur 2 005 (91,3 %) ont au
    moins une entreprise associée ; **175 n'en ont aucune**.
11. **Le CA mensuel est très concentré.** Avril 2025 pèse 5,23 M€ pour 28 signatures, contre une médiane
    mensuelle de 0,73 M€. Une moyenne sur 24 mois serait tirée par ce seul mois.
12. **Deux propriétaires inactifs dominent l'activité récente.** Luc Pollit (29638582, inactif) est 3e du
    classement avec 22 724 activités et Paul Hauchecorne (34846829, inactif) 8e avec 8 007. Un cockpit filtré
    sur les seuls propriétaires actifs perdrait un tiers du volume historique. Il n'existe pas de propriétaire
    « Luc Paul » : ce sont bien deux personnes, Luc Pollit et Paul Guinard-Terrin (1049537210).
13. **13 876 activités (8 %) n'ont aucun propriétaire** — principalement des NOTE (8 856) et des TASK (4 888).
    Elles sont conservées sous l'entrée `(non attribué)` plutôt que réparties.

---

## 7. Top 10 des propriétaires par volume d'activité

| # | Propriétaire | Actif | CALL | EMAIL | MEETING | TASK | NOTE | Total |
|---|---|---|---|---|---|---|---|---|
| 1 | Jordan Chenevier-Truchet | oui | 0 | 32 037 | 1 292 | 430 | 4 535 | **38 294** |
| 2 | Paul Guinard-Terrin | oui | 10 349 | 4 415 | 456 | 7 904 | 5 062 | **28 186** |
| 3 | Luc Pollit | non | 5 383 | 724 | 91 | 16 525 | 1 | **22 724** |
| 4 | Léo Lacoste | oui | 0 | 7 302 | 1 700 | 517 | 8 932 | **18 451** |
| 5 | *(non attribué)* | — | 125 | 0 | 7 | 4 888 | 8 856 | **13 876** |
| 6 | Sylvain Massy | non | 3 314 | 164 | 73 | 5 514 | 7 | **9 072** |
| 7 | Pierre-Arnaud Destremau | non | 985 | 3 971 | 796 | 470 | 2 109 | **8 331** |
| 8 | Paul Hauchecorne | non | 2 477 | 2 | 50 | 5 478 | 0 | **8 007** |
| 9 | Axel Lefort | non | 2 003 | 266 | 25 | 4 015 | 19 | **6 328** |
| 10 | François Michard | non | 946 | 2 505 | 444 | 518 | 120 | **4 533** |

Les 27 entrées complètes sont dans `activite.json`. Jordan Chenevier-Truchet n'a **aucun** appel enregistré
sur 24 mois : son activité est entièrement e-mail et note. Réciproquement, Paul Hauchecorne n'a que 2 e-mails
pour 2 477 appels. Les profils ne sont pas comparables entre eux sur un volume agrégé.

Côté deals, la propriété est répartie tout autrement : Enguerrand Chalvon Demersay 628 deals, Léo Lacoste 491,
Jordan Chenevier-Truchet 461, Pierre-Arnaud Destremau 287, Paul Guinard-Terrin 77. **Le propriétaire du deal
n'est pas celui qui a produit l'activité** — ne pas croiser les deux classements.

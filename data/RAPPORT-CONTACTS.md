# Contacts des grands comptes non clients — relevé HubSpot

Portail Bulldozer `143561253` (eu1). Extraction du **21/09/2026**. **Lecture seule** : aucune création,
modification ni suppression. Fenêtre des signaux : **21/09/2025 → 21/09/2026**.

---

## 1. Méthode

### Périmètre, reconstitué côté CONTACT

Le périmètre demandé — « contacts des entreprises non clientes de ≥ 1 000 salariés » — est défini côté
COMPANY mais ne peut pas être traversé par jointure cross-objet (voir §4). Il a donc été reconstitué en
trois temps, chacun sur **un seul objet** :

1. **COMPANY seul** — `numberofemployees >= 1000` → **2 029 fiches entreprise**
   (vérifié : champ `total` de `search_crm_objects` = 2 029 ; pagination par `hs_object_id > <dernier>`,
   5 pages de 500/500/500/500/29).
   Répartition : 1 854 `lead`, 150 `opportunity`, **25 `customer`**.
2. **Construction de la liste de domaines cibles** — normalisation des domaines (protocole, `www.`,
   chemin, casse) puis exclusions :

   | Exclusion | Fiches |
   |---|---:|
   | `lifecyclestage = customer` | 25 |
   | pas de domaine exploitable sur la fiche | 18 |
   | domaine partagé avec une fiche cliente du portail (435 domaines clients relevés sur 495 fiches) | 91 |
   | **fiches conservées** | **1 894** |
   | **domaines cibles distincts** | **1 749** |

3. **CONTACT seul** — `WHERE hs_email_domain IN (…)`, 7 lots de 250 domaines, `ORDER BY hs_object_id ASC
   LIMIT 500`. Aucun lot n'a atteint le plafond de 500 (283 / 292 / 277 / 412 / 364 / 376 / 311), donc
   aucune troncature silencieuse. → **2 315 contacts, 2 315 identifiants distincts**.

### Vérification des totaux

Le lot 0 a été recompté indépendamment par `SELECT hs_email_domain, COUNT(*) … GROUP BY hs_email_domain`
et comparé domaine par domaine au relevé ligne à ligne : **283 lignes contre 284 attendues**, un seul écart
(`archroma.com`, 1 contact annoncé par l'agrégat, 0 par la requête ligne — et 0 aussi par une requête
directe sur ce domaine seul). **L'agrégat compte un fantôme que la lecture ligne ne voit pas** : 0,35 % sur
ce lot. Le fichier `contacts.json` fait foi, pas les `COUNT(*)`.

### Classification des rôles

`roles.json` porte le dictionnaire complet **764 intitulés distincts → rôle**. Normalisation : minuscules,
accents supprimés, ponctuation → espace, correspondance **sur frontière de mot** (sans elle, « crédit » et
« digital » matchent le token `it`). Deux faux positifs ont été détectés et corrigés à la relecture :
« juriste droit social » classé praticien via le token `social` (corrigé : seuls « social media », « paid
social », « réseaux sociaux », « community manager »… comptent), et « Real Estate Developer » classé
technique via `developer` (corrigé : `real estate` / `immobilier` / `foncier` neutralisent le token). Les intitulés multiples concaténés (virgule, slash, pipe) sont évalués
en entier : c'est le token de plus haute précédence trouvé dans la chaîne qui décide.

**Un cas à connaître : certains `jobtitle` sont des historiques de carrière LinkedIn entiers**, collés bout
à bout sur une seule ligne (jusqu'à 7 postes séparés par des virgules). C'est ce qui rend la règle
« chaîne entière, token de plus haute précédence » indispensable : sur l'un d'eux, c'est
« Responsable approvisionnement » — en septième position, au-delà du 380ᵉ caractère — qui identifie
correctement le siège achat, alors que la chaîne commence par « Manager Business Development ».

**Précédence : `achat` > `technique` > `decideur` > `praticien` > `autre` > `inconnu`.**
Les deux sièges *fonctionnels* du comité priment sur la séniorité ; ensuite la séniorité prime sur
l'exécution. Chaque contact porte **aussi** un axe `seniorite` (`direction` / `operationnel`) indépendant du
rôle, pour que cet arbitrage soit réversible sans ré-extraction.

---

## 2. Volumes

### Population

| | |
|---|---:|
| Fiches entreprise ≥ 1 000 salariés | 2 029 |
| dont non clientes, avec domaine exploitable, domaine non client | **1 894** |
| Domaines cibles distincts | 1 749 |
| **Contacts joignables par domaine** | **2 315** |
| Domaines effectivement porteurs de contacts | 974 (56 % des 1 749) |
| Comptes couverts par ≥ 1 contact | **920** (49 % des 1 894) |

### Reconstitution des comités

| Contacts joignables par compte | Comptes |
|---|---:|
| 1 seul | 545 |
| 2–3 | 255 |
| 4–9 | 95 |
| 10 et + | 25 |
| **≥ 3 (comité réellement reconstituable)** | **206** (11 % des comptes cibles) |

### Rôles

| Rôle | Effectif | Part |
|---|---:|---:|
| `inconnu` (jobtitle vide) | 1 452 | 62,7 % |
| `praticien` | 429 | 18,5 % |
| `decideur` | 348 | 15,0 % |
| `autre` | 69 | 3,0 % |
| `technique` | 12 | 0,5 % |
| `achat` | 5 | 0,2 % |

Sur les **863 contacts qui ont un intitulé** : 40,3 % décideurs, 49,7 % praticiens, 1,4 % technique,
0,6 % achat, 8,0 % autre. **`technique` et `achat` sont quasi absents** : le CRM ne contient presque que
des interlocuteurs marketing/communication. Un comité d'achat grand compte ne se reconstitue pas avec ça.

### Signaux datés (12 mois) — 1 436 signaux

| Type | Volume | Lecture |
|---|---:|---|
| `formulaire` | 423 | dont **354 LinkedIn Lead Gen (84 %)** → non discriminants |
| `ouverture_email` | 390 | **signal faible, gonflé par MPP** |
| `visite_site` | 387 | |
| `clic_email` | 156 | le seul signal e-mail solide |
| `abonne_linkedin` | 80 | **non daté**, hors volumes mensuels |

Formulaires par famille : LinkedIn Lead Gen 354 · autre formulaire 42 · prise de RDV 14 · contenu 13.
**69 formulaires seulement (16 %) sont discriminants** (champ `discriminant: true`).
Les volumes mensuels par type sont dans `signaux.json` → `volume_mensuel`.

### Taux de remplissage (sur 2 315)

| Champ | | Champ | |
|---|---:|---|---:|
| `hs_email_domain` | 100 % | `hs_analytics_first_url` | 24,0 % |
| `createdate` / `lifecyclestage` / `hs_analytics_source` | 100 % | `hs_analytics_last_timestamp` | 24,0 % |
| `hubspot_owner_id` | 92,9 % | `num_unique_conversion_events` | 24,5 % |
| `firstname` | 91,4 % | `first_/recent_conversion_*` | 24,6 % |
| `lastname` | 82,2 % | `hs_analytics_num_visits` | 24,9 % |
| `company` (côté contact) | 42,2 % | `hs_lead_status` | 15,4 % |
| `notes_last_contacted` / `num_contacted_notes` | 39,0 % | `hs_email_click` / `hs_email_last_click_date` | 9,9 % |
| **`jobtitle`** | **37,3 %** | `linkedin_follower__` | 3,5 % |
| `hs_email_open` / `hs_email_last_open_date` | 27,3 % | | |

**`jobtitle` à 37 % est le plafond de tout ce travail** : deux contacts sur trois n'ont pas d'intitulé,
donc pas de rôle. Ce n'est pas un défaut du classifieur, c'est le CRM.

---

## 3. L'écart entre contacts associés et contacts joignables par domaine

C'est le résultat le plus important du relevé.

Les **1 750 comptes non clients ≥ 1 000 salariés qui ont au moins un contact associé portent 5 032
contacts associés** (1 602 `lead` → 3 829 + 148 `opportunity` → 1 203). La jointure par domaine en
récupère **2 315**, soit **46 %**. Mais ce ratio global est trompeur, parce que ces 2 315 ne sont pas
tous les mêmes personnes que les 5 032.

**Mesure directe.** Sur un échantillon de **83 comptes cibles** totalisant 1 628 contacts associés,
interrogés par la seule forme cross-objet fiable (`WHERE COMPANY.hs_object_id IN (…83 ids)`, colonnes
CONTACT uniquement), **1 500 lignes relevées** se répartissent ainsi :

| Situation du contact associé | Part |
|---|---:|
| **joignable par le domaine du compte** | **36,0 %** |
| **aucun domaine e-mail du tout** | **46,7 %** |
| autre domaine d'entreprise (domaine frère) | 10,1 % |
| adresse personnelle (gmail, yahoo, hotmail, wanadoo, orange, protonmail…) | 7,2 % |

**Deux contacts associés sur trois échappent à la jointure par domaine**, et la cause principale n'est pas
l'adresse personnelle (7 %) mais **l'absence totale d'e-mail (47 %)** — des fiches issues de LinkedIn, sans
adresse. Le relevé antérieur qui parlait de « 606 personnes en e-mail perso non rattachables » décrivait le
symptôme le plus visible, pas le plus gros.

Les 10,1 % « autre domaine » sont des **domaines frères** du même groupe, que la fiche entreprise ne porte
pas : `hec.fr` vs `hec.edu` (19), `socgen.com` vs `societegenerale.com` (6), `printemps.com` vs
`groupe-printemps.com` (8), `sanofi.fr` vs `sanofi.com` (4), `carrefour.com` vs `recrute.carrefour.fr` (4),
`guerlain.fr` vs `guerlain.com` (2), `groupe-beaumanoir.fr`/`.net` (3), `solina-group.fr` vs `solina.com`
(2), `schneider-electric.com` vs `se.com`, `alan.com` vs `alan.eu`. **Un alias de domaine par compte
récupérerait une bonne partie de ces 10 %** — c'est le gain le moins cher disponible.

**L'écart n'est pas uniforme, il est bimodal.** Il ne se corrige pas par un coefficient :

| Compte (domaine fiche) | Contacts associés | Joignables par domaine |
|---|---:|---:|
| Würth France (`wurth.fr`) | 220 | **3** |
| L'Oréal (`loreal.com`) | 131 | **6** |
| Schneider Electric (`se.com`) | 36 | **2** |
| PPG (`ppg.com`) | 27 | **0** |
| Renault Group (`renaultgroup.com`) | 25 | **0** |
| EssilorLuxottica (`essilorluxottica.com`) | 23 | **0** |
| Danone (`danone.com`) | 23 | **1** |
| Sanofi (`sanofi.com`) | 23 | **3** |
| — | | |
| HEC Paris (`hec.edu`) | 131 | 109 |
| Pluxee (`pluxeegroup.com`) | 42 | 43 |
| bpifrance (`bpifrance.fr`) | 27 | 27 |
| Veolia (`veolia.com`) | 35 | 32 |
| Saint-Gobain (`saint-gobain.com`) | 21 | 15 |

Les comptes du haut du tableau ont été **alimentés par scraping LinkedIn sans e-mail** ; ceux du bas par
**formulaire ou import avec e-mail**. Le cockpit affichera un comité fourni pour les seconds et un compte
vide pour les premiers — **alors que le CRM connaît 220 personnes chez Würth**. C'est un artefact de mode
de collecte, pas une réalité commerciale, et il ne faut pas en tirer un score d'engagement de compte.

---

## 4. Réserves

**La jointure cross-objet ment, et n'a pas été utilisée pour constituer le jeu de données.**
`SELECT COMPANY.x FROM CONTACT` tronque silencieusement (145 lignes rendues là où la même clause sans
colonnes COMPANY en rend 1 441). Tout `contacts.json` est bâti sur `hs_email_domain`. La seule forme
cross-objet employée est `WHERE COMPANY.hs_object_id IN (…)` avec des colonnes CONTACT uniquement, et
uniquement pour **mesurer** l'écart du §3 — jamais pour produire une ligne du livrable.
`associatedcompanyid` n'existe pas sur CONTACT dans ce portail (confirmé par `get_properties`).

**Le rattachement au compte est un rattachement par domaine, pas une association CRM.**
`compte_cible_nom` / `compte_cible_id` viennent de la table domaine → fiche entreprise que j'ai construite,
pas des associations HubSpot. **209 contacts (9 %)** ont un domaine porté par **plusieurs** fiches
entreprise ≥ 1 000 salariés : pour eux `compte_cible_nom` est `null` et la liste des candidats est dans
`compte_cible_ambigu`. Ne jamais afficher un nom de compte déduit là où il y a ambiguïté.

**Domaines non corporate.** `domaine` sur la fiche entreprise est parfois une URL LinkedIn, un
raccourcisseur ou un domaine de service. Exemple vérifié : la fiche **Airbus** porte
`https://www.linkedin.com/company/airbusgroup/`, qui se normalise en `linkedin.com` — et aurait attribué à
Airbus tout contact `@linkedin.com`. Il n'y en a aucun dans la base, donc **aucun contact n'a été mal
attribué par ce biais**, mais le piège est armé pour la prochaine extraction. **35 contacts** portent un
domaine non corporate (`bit.ly`, `linktr.ee`, `malt.com`, `substack.com`, `zeliq.intercom-mail.com`,
`customer7760.zendesk.com`…) et sont marqués `domaine_non_corporate: true` : à exclure de tout comptage de
comité. Trois fiches entreprise ≥ 1 000 salariés portent `bit.ly` comme domaine (elmy, Digital Artness,
Pandacraft) — ce ne sont pas des grands comptes, c'est du bruit de saisie.

**Apple MPP gonfle les ouvertures.** Mesuré sur le périmètre : **8 322 ouvertures pour 427 clics**, soit
**19,5 ouvertures par clic**. Maximum **123 ouvertures** sur un seul contact ; **43 contacts dépassent 50
ouvertures**. Une ouverture n'est jamais présentée comme un signal fort ; pondérer **clic × 4** et plafonner
les ouvertures dans tout indicateur agrégé.

**Les compteurs ne se fenêtrent pas.** `hs_email_open`, `hs_analytics_num_visits`,
`num_unique_conversion_events`, `num_contacted_notes` sont cumulés depuis toujours. `signaux.json` est bâti
**exclusivement sur des dates**, jamais sur ces compteurs. Corollaire à ne pas oublier : les dates
disponibles sont des **dernières occurrences** (`hs_email_last_open_date`, `hs_email_last_click_date`,
`hs_analytics_last_timestamp`). Un contact pèse donc **1 par type de signal**, pas N. Les volumes mensuels
sont des volumes de **contacts actifs ce mois-là**, pas des volumes d'événements — et l'historique
intermédiaire est définitivement perdu : on ne peut pas reconstruire une série d'activité.

**LinkedIn : un seul signal, non daté, et presque hors de portée.**
`date_de_following_linkeidn` (orthographe d'origine) et `hs_social_linkedin_clicks` sont vides à 100 % :
**on ne peut ni dater un abonnement ni mesurer un clic social**. Seul `linkedin_follower__ = OUI` est
exploitable — **10 717 contacts dans la base**, vérifié. Mais **9 243 d'entre eux (86 %) n'ont aucun domaine
e-mail** : ils sont inrattachables à un compte par domaine. Dans le périmètre, il n'en reste que **80**.
Le signal LinkedIn organique est donc massivement présent dans le CRM et massivement **inutilisable** en
ABM par compte. Dans `signaux.json` il est émis avec `date: null` et `date_connue: false`, et n'entre dans
aucun volume mensuel.

**Le formulaire LinkedIn Lead Gen ne discrimine pas.** 76 % des comptes signés comme non signés en ont un.
354 des 423 formulaires de la fenêtre (84 %) en relèvent. Le champ `famille` distingue
`linkedin_lead_gen` / `contenu` / `prise_de_rdv` / `autre_formulaire`, et `discriminant: false` marque les
premiers. Un cockpit qui compte « a rempli un formulaire » sans cette distinction classera tout le monde
pareil.

**19 contacts sont `lifecyclestage = customer` sur des comptes non clients.** Le périmètre est défini au
niveau du COMPTE ; ces 19 contradictions sont conservées et visibles dans `contacts.json` plutôt que
supprimées en silence. À arbitrer avant activation.

**Définition de « non cliente » retenue : `lifecyclestage != 'customer'` sur la fiche entreprise**, plus
l'exclusion des 91 fiches dont le domaine est partagé avec une fiche cliente. Un compte réellement client
mais dont le `lifecyclestage` n'aurait jamais été mis à jour resterait dans le périmètre. Non vérifié par
les deals gagnés (cela aurait exigé la jointure cross-objet non fiable).

**L'agrégat et la lecture ligne divergent légèrement.** Constaté deux fois : 284 vs 283 sur le lot 0, et
1 628 contacts associés annoncés vs 1 604 relevés sur l'échantillon de 83 comptes (98,5 %). Écart de
l'ordre de 0,3 à 1,5 %, sans effet sur les conclusions, mais il interdit de traiter un `COUNT(*)` comme une
preuve exacte.

### Ce qui a été laissé de côté

- **Les contacts sans `hs_email_domain` : 16 912 dans la base** (`Unassigned`), dont 9 243 abonnés
  LinkedIn. Ils sont par construction hors d'atteinte d'une jointure par domaine. C'est le gisement
  principal — et il ne se récupère que par l'association CRM, dont la lecture en masse n'est pas fiable
  ici. **Aucun d'eux n'est dans `contacts.json`.**
- **829 domaines cibles (47 %) sans aucun contact** : 974 domaines porteurs sur 1 749 ciblés.
- **974 comptes cibles sur 1 894 (51 %) n'apparaissent pas** dans `contacts.json`, faute de contact au
  domaine de leur fiche.
- **Les domaines frères non déclarés** sur les fiches entreprise (~10 % des contacts associés). Les
  récupérer demande une table d'alias de domaines par compte, qui n'existe pas dans le CRM.
- **Les 18 fiches ≥ 1 000 salariés sans domaine exploitable** (Éducation nationale, Pfizer, « À mon
  compte »…) : aucun contact ne peut leur être rattaché par domaine.
- Le quatrième et dernier lot de l'échantillon d'association (104 lignes sur 1 604) n'a pas été persisté ;
  les 36 % du §3 sont calculés sur les **1 500 premières lignes**, soit 94 % de l'échantillon.

---

## 5. Fichiers

| Fichier | Contenu |
|---|---|
| `contacts.json` | 2 315 contacts, 30 champs, triés par `hs_object_id` |
| `roles.json` | dictionnaire 764 intitulés → rôle, effectifs, croisement rôle × séniorité, arbitrages signalés |
| `signaux.json` | 1 436 signaux, volumes par type et par mois, avertissements embarqués |
| `RAPPORT-CONTACTS.md` | ce document |

Champs ajoutés au-delà de la demande, pour la sécurité d'usage : `role`, `seniorite`, `compte_cible_nom`,
`compte_cible_id`, `compte_cible_effectif`, `compte_cible_ambigu`, `domaine_non_corporate`.

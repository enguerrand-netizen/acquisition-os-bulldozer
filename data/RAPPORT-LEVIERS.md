# Ce qui existe réellement comme donnée d'acquisition — agence Bulldozer

Relevé du 21/09/2026 · projet **Bulldozer Interne** (`customerId 533c1f8f-bcc2-4e95-a3ee-4e630b86dbbf`, `projectId b09bf643-e087-4e6c-8415-f9ee96e5cc94`)
Lecture seule. Relevé brut : `leviers.json` (même dossier).

**Règles tenues.** La métrique `leads` de l'OS est fausse : elle est exclue de bout en bout, `cpl` aussi. L'agrégat `ALL` n'a jamais été lu — tous les totaux sont recomposés en additionnant les lignes datées. Aucun trou n'est comblé par une estimation.

---

## Verdict par levier

| Levier | Alimentable en réel ? | Période | Volume mesuré |
|---|---|---|---|
| **paid_linkedin** | **Oui** | 01/01/2026 → 20/09/2026 | 34 193,29 € · 4 724 760 impr. · 160 650 clics · 18 campagnes · 909 lignes/jour |
| **paid_meta** | **Oui** | 31/10/2025 → 20/09/2026 | 30 804,69 € · 3 352 771 impr. · 52 040 clics · 174 campagnes · 796 lignes/jour |
| **social_linkedin** | **Partiellement** | 03/06/2026 → 17/09/2026 | 16 posts (profil Jordan) · 1 455 réactions · 311 commentaires · **0 post de la page** |
| **outbound_lemlist** | **Partiellement** | créations 01/2024 → 09/2026 | 108 campagnes + étapes de séquence · **0 lead, 0 métrique de perf** |
| **seo** | **Oui** | SEO 09/2026 · GSC 19/05 → 18/09/2026 | 242 mots-clés, 4 659 visites estimées · GSC 113 jours, 8 488 clics / 6,3 M impr. |
| **sea** | **Non** | — | 0 campagne sur les 2 comptes Google Ads Bulldozer |
| **cadrage** | **Partiellement** | tracker GTM au 12/08/2026 | 11 profils ICP · **aucun objectif chiffré** |

---

## 1. paid_linkedin — **disponible**

Compte **BULLDOZER** (`urn:li:sponsoredAccount:511718129`, uuid `99567c90-…`), EUR, lecture accordée, rafraîchi quotidiennement, à jour au 20/09/2026.

- **34 193,29 €**, **4 724 760** impressions, **160 650** clics sur 2026. CTR global 3,40 %, CPC 0,213 €, CPM 7,24 €.
- Mensuels complets de janvier à septembre 2026. Montée nette : 1 174 € en janvier → 5 071 € en août.
- **18 campagnes** portent des métriques (sur 62 référencées). Les 4 plus grosses : *TLG II BOFU* 10 898 € (active, lead gen), *RTG* 5 825 €, *SPRINT 1 II TOFU* 3 346 €, *ACQUISITION CEO* 2 679 €.
- **Créatives : oui.** 3 459 lignes jour × créative disponibles. Échantillon 01→21/09 relevé : 35 créas distinctes, 2 612 € — avec type, dépense, impressions, clics, CTR, CPC, CPM.

**Ce qui manque.** Ciblage, reach, fréquence, réactions et commentaires sont `null` sur 100 % des lignes — jamais importés, ce n'est pas un défaut de requête. Les 44 autres campagnes du compte sont des brouillons et des résidus de tests MCP/QA (`[MCP TEST]`, `TEST-BULLDOZER-OS-QA-*`, `de`, `dede`, `test`), dont 4 en `REMOVED` : à exclure d'office. *Message Sponsorisé - ICP Marketing* affiche 70,96 € pour 0 impression et 0 clic (métriques de message sponsorisé toutes à 0).

Les deux comptes **Traction** et **Traction Deuxième** contiennent des tests de traction menés pour des clients/prospects, pas l'acquisition de l'agence — et leur devise revient à **`XXX`, non résolue** : les montants n'y sont pas interprétables. 13 comptes clients supplémentaires sont en accès refusé (`organization 404`), ce qui est normal. Le compte USD `515441114` est branché mais n'a **aucune** ligne.

## 2. paid_meta — **disponible**

Compte **Bulldozer** (`231961352837525`, uuid `0ecad557-…`), EUR, lecture et écriture accordées, à jour au 20/09/2026.

- **30 804,69 €**, **3 352 771** impressions, **52 040** clics du 31/10/2025 au 20/09/2026. CTR 1,55 %, CPC 0,592 €, CPM 9,19 €.
- Mensuels complets sur 12 mois. **174 campagnes** avec métriques (sur 356 référencées).
- **Créatives : oui, et plus riches que LinkedIn.** 3 769 lignes jour × créative. Échantillon 01→21/09 : 51 créas (40 images, 11 vidéos), 1 806 € — avec en plus **reach, fréquence, réactions, commentaires, thruPlays, videoPlays, hookRate**, tous renseignés côté Meta.

**Le piège principal.** Ce compte **mélange l'acquisition de l'agence et les tests de traction menés pour des clients et prospects**, sans aucun champ qui les distingue. Les 8 plus grosses dépenses de la période sont des campagnes *Client_AEnergie* (≈ 6 700 € cumulés), et on trouve aussi *TDT Veolia*, *TDT Gérofinance*, *TDT Carrefour Pro*, *TDT - Familiar*, *TDT Assurpoil*. Les campagnes propres à Bulldozer se reconnaissent au nom : `RUN II Bulldozer II NE PAS TOUCHER` (4 836 €, la plus grosse ligne réellement Bulldozer), `RUN - Bulldozer metro` (2 163 €), `RUN BULLDOZER`, `RUN leadform - Bulldozer`, `GTM - BULLDOZER - FR/US`, `SPRINT n II Média Bulldozer II …`, `Bulldozer OS — MCP — Conversion site — Sept 2026` (675 €, active). **Le cockpit doit porter ce filtre lui-même.**

Deux chiffres à vérifier avant publication : août 2026 affiche 1 205 586 impressions pour 1 167 € (CPM 0,97 €), ordre de grandeur atypique. Et `conversions` est `null` sur les lignes relevées — « non mesuré », pas « zéro conversion ».

Le compte Meta *Hosman - Bulldozer* est un compte client, gelé au 04/06/2026, import en erreur, rafraîchissement coupé.

## 3. social_linkedin — **partiellement disponible**

- **Les posts de la page Bulldozer n'existent pas dans l'OS.** La page est bien enregistrée (`companyId 74995178`, 11 491 abonnés, mise à jour ce matin), mais **0 post stocké**. Les deux seules configurations de rafraîchissement visent des profils de **personnes**, pas la page. Et l'accès à la page depuis le compte publicitaire est en `pageAccess DENIED`.
- Ce qui existe : **16 posts du profil Jordan Chenevier**, du 03/06 au 17/09/2026, avec date, texte intégral, réactions, commentaires, partages. Total 1 455 réactions / 311 commentaires / 15 partages. Le pic est le post VivaTech du 18/06 (294 réactions, 151 commentaires).
- Le profil d'Enguerrand a une configuration active depuis le 29/08 mais **0 post stocké**.

**Réserves.** Trou de collecte entre le 18/06 et le 16/09. 1 post sur 16 n'est pas de Jordan (signé Loïc Burdet-Aulas, capté par le scrape) — mais `actorName` est `null` sur 11 posts sur 16, donc le filtre par auteur ne tient qu'à moitié. Aucune impression ni portée organique : LinkedIn n'expose que réactions, commentaires, partages. Fiche entreprise incohérente : `employeeCount 161` contre `employeeCountRange 2-10`.

Un écran « posts de la page Bulldozer » est **à marquer non branché**. Un écran « thought leadership fondateur » est alimentable, sur 16 posts et un seul auteur.

## 4. outbound_lemlist — **partiellement disponible**

- **108 campagnes** synchronisées, créées du 04/01/2024 au 07/09/2026 : 42 brouillons, 40 archivées, 18 terminées. **Aucune en cours d'envoi.**
- **Les étapes de séquence sont lisibles** : `bdzListLemlistSequences` renvoie type, délai, index, sujet et corps du message. Vérifié sur *Campagne ICP1 Tiers 1* (1 étape e-mail).
- **Le nombre de leads n'est pas disponible.** `bdzListLemlistLeads` renvoie `totalElement = 0` sur les 4 campagnes testées, dont 3 qui ont réellement tourné (*[Marketing director][Gmail][February]*, *[Outlook][February]*, *Followers CMO BTEC*).
- **Aucune métrique de performance** (envois, ouvertures, clics, réponses, rebonds, rendez-vous) : l'endpoint ne les expose pas, la documentation de l'outil le dit.
- **89 campagnes sur 108 portent `hasError = true`** : le connecteur est dégradé.
- Les 8 campagnes créées en 2026 sont toutes en brouillon : 4 autour du « Guide Budget 2027 », 1 TLA Jordan (engageurs post VivaTech), 3 tests techniques marqués « 0 lead, ne pas utiliser ». Le dernier envoi réel documenté remonte à **février 2025**.

Un écran « volume outbound » ou « performance des séquences » ne peut **pas** être alimenté. Un écran « inventaire des séquences et de leurs étapes » le peut.

## 5. seo — **disponible**

Domaine confirmé : **`bulldozer-collective.com`** (`domainId eaa8ca4a-…`). C'est bien le domaine de l'agence — les 69 autres domaines SEO du projet sont des clients, prospects, concurrents (junto.fr, eskimoz.fr, primelis.com, growthroom.co…) et 2 domaines de test.

- **Aperçu (instantané 09/2026, France)** : 4 659 visites organiques estimées, **242 mots-clés** positionnés, 11 529 € de coût organique équivalent, répartition complète par tranche de position (6 en position 1, 17 en 2-3, 63 en 4-10).
- **Mots-clés** : 100 renvoyés, 40 détaillés dans le JSON avec position, volume, CPC, part de trafic, marque/hors-marque, URL.
- **Search Console** : `sc-domain:bulldozer-collective.com`, 208 529 lignes agrégées, séries journalières, top requêtes / pages / pays / appareils. Le trafic est **très fortement de marque** : « bulldozer », « bulldozer collective », « bulldozer agence », « bulldozer marketing » concentrent l'essentiel des clics. Hors marque, ce sont les pages SEO locales (agence SEO Nantes/Lille/Montpellier, Google Ads Strasbourg) et les articles de fond.

**Réserves sérieuses.** (a) `whenLatest` ne renvoie pas le même instantané pour l'aperçu (09/2026) et pour les mots-clés (06/2026) : ne pas croiser les deux sans le dire. (b) 100 mots-clés renvoyés contre 242 annoncés. (c) **Plusieurs mots-clés sont manifestement fabriqués ou pollués** — « stratégie acquisition growthpath funnel conversion », « comment optimiser conversion funnelboost max », « stratégie growth hacking boostmatic 360 guide », « agence google ads strasbourg crokseo flo 1 », « consultant seo lille$ » — et ils portent à eux seuls plus de 17 % du trafic annoncé. À ne pas publier tels quels. (d) **Search Console : les trois dimensions ne donnent pas le même total** (QUERY 4 400 clics, PAGE 8 488, COUNTRY/DEVICE 8 364). Chacune est agrégée différemment en amont : ne jamais les additionner ni les présenter comme un même chiffre. (e) 113 jours stockés sur les 386 demandés, rien avant le 19/05/2026 : aucune comparaison année sur année possible. (f) Les 4 659 visites sont une **estimation** du fournisseur ; les clics GSC sont, eux, mesurés. (g) `/articles/growth-hacking` affiche 4 295 007 impressions pour 229 clics : à vérifier.

## 6. sea — **non disponible**

`bdzListSeaL1s` renvoie **0 campagne** sur les deux comptes Google Ads Bulldozer (`1923201425` et `9808244998`). Aucune impression, aucun clic, aucune dépense.

8 comptes Google Ads sont rattachés au projet, dont 4 clients (Eden par Advenis, archi'v, UPELA, Carryboo), 1 compte de test et 1 compte sans nom ni devise (aucun import n'a jamais tourné dessus). Le tracker GTM retient pourtant Google Ads comme régie du cycle 1, avec un identifiant de compte (`AR04892468311402479617`) qui ne correspond à aucun compte enregistré : la régie est prévue, elle n'a jamais diffusé.

**L'écran SEA est à marquer « non branché ».** Aucune estimation ne doit y être posée.

## 7. cadrage — **partiellement disponible**

- **Aucun objectif chiffré n'existe dans l'OS.** Sur les 10 types d'objectifs que l'OS sait stocker, 2 seulement remontent : `COMPANY_PURPOSE` (chaîne **vide**) et `PRIVATE_INSIGHTS`. `TARGETS`, `FINANCIALS`, `FUNNEL`, `WIN_LOSS_REASON`, `BUYING_COMMITTEE`, `CONSTRAINTS`, `STRATEGICAL_DECISIONS`, `SALES_CALL_OBJECTIONS` sont absents. Un écran « objectif vs réalisé » devra faire saisir la cible à la main.
- `PRIVATE_INSIGHTS` contient en réalité deux blocs applicatifs riches : le **tracker GTM** (run 3, 12/08/2026 — objectif « trouver la promesse qui déclenche la prise de contact », 5 promesses validées et leurs landing pages, mix de régies, critères de décision, 7 points ouverts) et la configuration de la **Mission App**.
- **11 profils ICP** enregistrés : 5 ICP, 2 prescripteurs, 2 angles morts, 2 anti-personas. 9 sur 11 sont auto-générés par l'OS.

**À savoir avant de construire.** Une **Mission App existe déjà** (`bulldozer.bulldozer-os.fr/mission/`, coquille 1.5.2 déployée le 16/09/2026) avec un onglet `paid.dashboard` et un onglet `paid.creas` qui lisent **exactement les deux mêmes comptes** que ceux relevés ici. À regarder avant de reconstruire des écrans « leviers ».

**Réserves.** Le tracker GTM affiche « Campagnes en diffusion : Non démarrée » alors que Meta et LinkedIn ont bien diffusé en août-septembre 2026 : soit il n'est pas à jour, soit ces diffusions relèvent d'autres campagnes que celles du cycle GTM — ne pas rapprocher les deux sans vérifier. Les 9 profils auto-générés n'ont aucune pièce justificative (`evidence` vide partout). Les profils « Tier 1 » et « Tier 1+ » se contredisent entre leur champ structuré et leur note libre sur les effectifs. Et la cible du tracker (30-300 salariés, SaaS B2B) ne correspond à aucun des 11 profils tels quels : deux référentiels de cible coexistent. Enfin, `PRIVATE_INSIGHTS` est un état applicatif, réécrit par l'application : il peut disparaître.

---

## Erreurs et accès refusés rencontrés

| Appel | Paramètres | Message | Suite |
|---|---|---|---|
| `bdzGetAdAnalytics` | `pageSize=1000` | `400 — Page size must not exceed 200` | repris en pages de 200 |

Accès refusés, tous attendus et non bloquants :
- 13 comptes publicitaires LinkedIn **clients** : `readAccess/writeAccess DENIED`, `organization 404` au contrôle du 16/09/2026.
- Compte Meta **Hosman - Bulldozer** : import en erreur, `Ad account owner has NOT grant ads_management or ads_read permission`.
- Compte LinkedIn **BULLDOZER** : `pageAccess DENIED` sur `urn:li:organization:74995178` — c'est précisément ce qui explique l'absence de posts de la page entreprise.

## Ce qu'il faut retenir pour le cockpit

**Trois écrans peuvent être alimentés en réel, tout de suite :** paid LinkedIn, paid Meta (créatives comprises dans les deux cas) et SEO/Search Console.

**Un écran doit être marqué non branché :** SEA.

**Trois écrans sont à moitié vides et le resteront sans travail en amont :** les posts de la page LinkedIn (rien de stocké — il faudrait une configuration de rafraîchissement sur la page, et l'accès page est refusé), le volume outbound Lemlist (0 lead lisible, connecteur en erreur sur 89 campagnes sur 108), et l'objectif chiffré (rien dans l'OS, à saisir).

**Le piège à ne pas rater :** sur Meta, l'acquisition de l'agence et les tests de traction clients vivent dans le même compte, et les plus grosses dépenses de la période sont des campagnes clients. Sans filtre sur le nom de campagne, le cockpit affichera le budget des clients comme s'il s'agissait de celui de Bulldozer.

# AUDIT CODE — « Acquisition OS Bulldozer » (ex-Tour de contrôle ABM)

**Version auditée** : `build/app.src.html` · 805 663 octets · 2 922 lignes · md5 `3f2c8631614c91e52436929ecf3a407a` · horodatage 21/09/2026 13:33.

> Le fichier a changé **pendant** l'audit (2 544 lignes / 770 574 o à 13:22 → 2 922 / 805 663 à 13:33) : deux passes de construction ont été ajoutées entre-temps, `patch_levers.py` (13:29, injecte `levers.js`, 369 lignes) et `patch_final.py` (13:33). Tous les numéros de ligne ci-dessous se rapportent au snapshot md5 ci-dessus, conservé en `scratchpad/snap.html`. Les constats ont été **vérifiés à l'écran**, application servie en local (`python3 -m http.server`), pas seulement par lecture.

**Verdict en une ligne** : la réécriture des six leviers (`levers.js`) est honnête et sourcée ; ce qui reste de fictif vit (a) dans les écrans **non réécrits** — cockpit, fiche compte, moteur, suivi compte par compte, — (b) dans **450 lignes de maquette mortes mais toujours présentes**, et (c) dans **quatre chiffres nuls ou faux présentés comme des mesures**.

---

## 1. Référentiels encore inventés

Méthode : pour chaque référentiel, on distingue *déclaré*, *référencé par du code vivant*, *référencé seulement par du code mort* (les cinq fonctions de la maquette écrasées par `levers.js` — voir §2).

| Référentiel | Ligne | État | Nature du contenu | Gravité |
|---|---|---|---|---|
| `SECTORS` | 734 | **vivant** (chips du Moteur, l. 2475) | 14 familles sectorielles **réelles** (issues de `secteurs.py`, 495 clients signés). Convention d'affichage légitime. | — |
| `CITIES` | 735 | mort (`buildAccount` seul) | 10 villes, servaient à nommer des filiales fictives. | cosmétique |
| `FIRST` | 736 | mort | 40 prénoms inventés. | cosmétique |
| `LAST` | 737 | mort | 50 noms inventés. | cosmétique |
| `TITLES` | 738 | mort | 17 intitulés de poste inventés. | cosmétique |
| `SIG` | 747 | **vivant** (libellés + canal, partout) | Les `l`/`c` sont une convention d'affichage acceptable. **Mais les tableaux `d`** (`'/tarifs'`, `'Demande de démo'`, `'Livre blanc « ABM en 90 jours »'`, `'Newsletter — cas client'`…) sont des **libellés de contenus inventés** et ils sont **affichés** dans le Moteur, bloc « Typologie de contenu » (l. 2489 : `Object.values(SIG).flatMap(x => (x.d || [])…)`) comme si c'était la taxonomie réelle des contenus Bulldozer. | **à corriger** |
| `SIG_ORDER` | 762 | vivant | ordre d'affichage. | — |
| `CONTENT_T` | 763 | vivant | **contient `reply`** : les 211 réponses e-mail et les 113 visites de page sont comptées comme « contenus consommés » (KPI « Signaux de contenu 516 »). Le mot « contenu » est faux pour 40 % du volume — cf. §3 Content. | **à corriger** |
| `CONTACT_SIGS` | 764 | mort | pondération de tirage. | cosmétique |
| `WHY` | 765 | vivant (colonne Détail de Signaux) | Conseils d'action, convention acceptable. `WHY.lgf` porte un chiffre (« 76 % des comptes en ont un ») qui vient bien de l'étude outbound du 17/09. | — |
| `STATUS` | 774 | vivant | 5 libellés ; seuls `jamais` et `perdu` existent dans la donnée. Les 3 autres sont inatteignables mais inoffensifs. | cosmétique |
| `LOSS_REASONS` | 777 | mort | 5 motifs de perte inventés (« budget gelé en fin d'exercice »…). Les vrais motifs sont `Closed - DEAD` / `Standby`. | cosmétique |
| `FY_STARTS` | 778 | mort | — | cosmétique |
| `QUADS` | 781 | vivant | libellés, sous-titres, `play`, leviers par quadrant : **convention de méthode**, pas une mesure. | — |
| `LEVERS` | 787 | vivant | libellés + icônes. | — |
| `SDRS` | 795 | **VIVANT** | **4 personnes qui n'existent pas** : `'Léa Marchetti','Hugo Delaunay','Inès Barrault','Karim Othmani'`. Affichées dans le **sélecteur « SDR » du tableau « Suivi compte par compte »** (l. 1413 `const owners = k === 'sdr' ? SDRS : …`, rendu l. 1417). Vérifié à l'écran : le menu propose ces 4 noms ; en sélectionner un vide le tableau, puisque les vrais propriétaires d'appel sont Paul Guinard-Terrin, Jordan Chenevier-Truchet, etc. | **BLOQUANT** |
| `AES` | 796 | **VIVANT** | Idem, 3 noms inventés `'Julien Castaing','Claire Vautrin','Mathieu Roblin'` dans le sélecteur « AE » de l'écran Sales. | **BLOQUANT** |
| `POSTS` | 797 | mort | 12 posts LinkedIn inventés avec titres, auteurs et ancienneté (« Cas client : 2,3× plus de pipeline en 6 mois », « Baromètre B2B 2026 : les 5 chiffres »). Neutralisés par la réécriture Social. | à corriger (retirer) |
| `SEQS` | 805 | mort | 4 noms de séquences Lemlist inventés. | à corriger (retirer) |
| `CAMPS` | 806 | mort (déjà mort dans la maquette) | doublon dégradé de `CAMP_DEF`. | cosmétique |
| `OPP_STAGES` | 807 | mort | 4 étapes ; `STAGE_OPEN` d'`assemble.py` y mappe encore, mais aucun deal ouvert n'existe. | cosmétique |
| `EMAIL_TYPES` | 810 | mort | 6 étapes de séquence avec **taux d'ouverture, de clic et de réponse inventés** (`open: .62, click: .12, reply: .05`…). | à corriger (retirer) |
| `CALL_OUT` | 818 | **VIVANT** (l. 2833, journal d'appels de la fiche levier SDR) | `call: ['Rappel demandé','ok']`. Or `assemble.py` met `'call'` par **défaut quand le résultat HubSpot est absent ou non reconnu** (19 appels réels). L'écran affiche donc « **Rappel demandé** » sur 19 appels dont on ne sait rien — alors que la vue entreprise du **même levier** les étiquette « Résultat non saisi » (l. 2705). Deux libellés contradictoires pour la même donnée, dont un inventé. | **BLOQUANT** |
| `MEET` | 819 | mort | 5 libellés de type de meeting. | cosmétique |
| `CAMP_DEF` | 820 | mort | **4 campagnes inventées avec leurs budgets mensuels** : `{A:6000, B:8000, N:5000, R:3000}`. Alimentaient le KPI « Budget du mois 22 000 € ». Neutralisées par la réécriture Paid. | à corriger (retirer) |
| `CAMPQ` | 821 | mort | — | cosmétique |
| `CREAS` | 822 | mort | **8 créatives inventées** avec titres et CTR (`ctr: .011`, `.0065`…). | à corriger (retirer) |
| `ASSETS` | 832 | mort | **7 contenus inventés avec un budget LinkedIn mensuel** (`li: 2500, 3000, 1200, 1500, 1000, 800`) qui produisait le KPI « Budget LinkedIn du mois 10 000 € ». | à corriger (retirer) |
| `LIB` | 1461 | mort | Bibliothèque complète inventée : 2 livres blancs, 2 outils, 3 créatives, 2 landing pages, avec accroches, nombres de pages (« 42 pages · 6 chapitres ») et **une fausse marque** : `postHTML` (l. 1483) affiche « **Tour de contrôle ABM** · Sponsorisé » et `browserHTML` (l. 1484) une URL `tour-de-controle.fr/…`. | à corriger (retirer) |
| `CHAPTERS` | 1480 | mort | 6 chapitres inventés du livre blanc. | cosmétique |
| `AGENTS` | 843 | **vivant** (catalogue) | 7 descriptions d'agents. L'écran les présente explicitement comme un **catalogue** (« Catalogue, pas état de marche »), pas comme un état. Acceptable. | — |
| `AGENT_TASKS` | 1922 | **vivant** (catalogue) | 34 tâches avec leurs réglages par défaut (`Budget max ajouté / semaine = 500 €`, `CTR minimum = 0.35 %`, `Source d'enrichissement = Waterfall`). Affichés comme « Réglages » souhaités, cadrés par la phrase « Tant qu'aucun agent n'est mis en marche, ils ne produisent rien ». Acceptable, mais ce sont des valeurs choisies, pas mesurées. | cosmétique |

**Total des restes fictifs encore affichés à l'écran : 4** — `SDRS`, `AES`, `CALL_OUT.call`, et les libellés de contenus de `SIG[*].d` dans le Moteur. Tous les autres (`CAMP_DEF`, `CREAS`, `ASSETS`, `POSTS`, `SEQS`, `EMAIL_TYPES`, `LIB`…) sont **morts mais toujours dans le fichier**, à un `git revert` de distance de redevenir visibles.

---

## 2. Fonctions génératrices

| Fonction | Ligne | Appelée ? | Ce qu'elle fabriquerait | Gravité |
|---|---|---|---|---|
| `hash` | 715 | **oui** | graine ; ne sert plus qu'à `layout()` et à la fonction morte `assetStats`. Inoffensif. | — |
| `rng` | 716 | **oui** | idem. Le seul aléa encore *affiché* est la **position des nœuds** de la carte du comité (`layout`, l. 1667, graine `a.seed ^ 0x9e37`) — une mise en page, pas une donnée. | — |
| `pick` | 717 | non (hors `buildAccount`/`sampleNames`) | — | cosmétique |
| `shuffle` | 852 | non (seulement depuis `enrich`, morte) | — | cosmétique |
| `sampleNames` | 949 | **oui**, 2 fois : l. 1083 `let names = store.get('abm-tdc-names') \|\| sampleNames()` et l. 1344 (bouton « Revenir à l'exemple (100) ») | Génère 100 noms d'entreprises fictives (`Terrarys Énergie`, `Groupe Nexatis`…). **La variable `names` n'est plus lue par `rebuild()`** : elle est calculée, persistée et jamais utilisée. Le bouton « Revenir à l'exemple (100) » promet un portefeuille fictif de 100 comptes qui n'arrivera jamais. | **à corriger** |
| `buildAccount` | 952 | **non** (déclaration seule) | 70 lignes de génération de comptes fictifs. Morte. | à corriger (retirer) |
| `enrich` | 853 | **NON — correctement retirée** | `rebuild()` (l. 1104) ne contient plus `accounts.forEach(enrich)` ; le commentaire d'`inject.py` explique pourquoi. Le piège P1 est **traité**. La fonction (24 lignes) reste néanmoins dans le fichier. | à corriger (retirer) |
| `paidOf` | 1357 **et 2573** | la **seconde** (`levers.js`) gagne : `function paidOf(){ return []; }` | La version maquette (l. 1357) répartissait `imp30` entre des créatives inventées ; elle est écrasée. | à corriger (retirer la morte) |
| `assetStats` | 1363 | **non** (appelée seulement depuis `leverCompany` mort et `taskItems` mort) | Fabriquait `spent = x.li * MTD * (.85 + r()*.3)` — une **dépense en euros tirée au sort** à partir d'un budget inventé. | à corriger (retirer) |
| `creaStats` | 1521 | non | agrégat de `paidOf` sur les créatives inventées. | à corriger (retirer) |
| `lpStat` | 1525 (dans `contentLibrary`) | non | `visits = leads * (7 + r()*5) + 40` — **nombre de visites de landing page tiré au sort**. | à corriger (retirer) |
| `rdvEvents` | 1242 | **oui** (cockpit) | **Réécrite honnêtement** par `patch_fixes.py` : part des meetings réellement tenus, attribue la source au dernier geste dans les 14 jours, et laisse `'nc' — Non attribué` sinon. Bon. | — |
| `layout` | 1667 | **oui** (fiche compte) | positions du graphe. Pas une donnée. | — |
| `taskItems` | 1985 | **non** (appelée seulement par `agentRun`, lui-même appelé seulement par le `renderAgents` mort) | Fabriquait un **journal d'actions d'agent exécutées** avec des dates tirées au sort (`dd() = Math.floor(r()*7)`). Contenait notamment `crm.dedup` → « Doublon fusionné : *\<nom d'un vrai contact du CRM\>* » et `crm.norm` → « Exercice fiscal renseigné sur 9 comptes » (`Math.round(accounts.length * .3)`). **Neutralisé** par la réécriture de l'écran Agents — mais 60 lignes de fabrication restent dans le fichier. | **à corriger (retirer)** |
| `agentRun` / `agentCfg` | 2043 / 1973 | non / non | `agentCfg` mutait à la lecture (piège de la carte) ; devenu sans objet. | cosmétique |
| `narrative`, `frise`, `stageWeeks`, `stageLegend`, `planNote`, `propState` | 1726, 1201, 1209, 1208, 1456, 2268 | non (déjà mortes dans la maquette) | — | cosmétique |
| `renderMission` / `renderOffre` / `renderPropal` | 1218 / 2355 / 2278 | **non** — `render()` (l. 1155) mappe `proposition: renderCockpit` et `go()` (l. 1141) réécrit la route en `cockpit` | ~330 lignes de **proposition commerciale client** : `PHASES`, `PRICE_DEF` (`{socle:4200, pilot:1800, mkt:1200, sales:1200, os:900}`), `RACI`, `TEAM`. Morte, mais contient des prix et un plan de mission qui n'ont rien à faire dans un outil interne. | **à corriger (retirer)** |
| `contentLibrary`, `lpHTML`, `tplHTML`, `roiHTML`, `openModal`, `bindLibrary` | 1523, 1487, 1504, 1485, 1508, 1533 | `bindLibrary` est encore **appelée** par `renderLever` (l. 1437) mais ne trouve plus aucun `[data-open]` : no-op. Les autres sont mortes. | `roiHTML` posait des valeurs par défaut inventées (100 comptes, **8 % de taux de signature**, 45 000 € de panier, 60 000 € de budget) — les 8 % contredisent les 0,7–5,3 % mesurés. `tplHTML` (l. 1506) affiche `MONTH_FULL[a.fyStart]` avec `fyStart = null` → **« undefined »**. | à corriger (retirer) |

**`enrich()` n'est plus appelée** ✅ et **`buildAccount` ne sert plus** ✅ — les deux vérifications demandées sont bonnes.

---

## 3. Les 13 écrans face aux données réellement présentes

Rappel de la matière disponible (`accounts.json`, 30 comptes) : 536 contacts (423 actifs, 113 hors circuit, **0 « cible »**), 516 signaux (`reply` 211, `lgf` 122, `page` 113, `click` 63, `form` 4, `pricing` 2, `dl` 1 — **aucun `ad`, `open`, `job`, `hiring`, `news`**), 343 appels, 327 e-mails sortants, 80 meetings (78 tenus, 0 à venir), **0 opportunité ouverte**, 10 pertes (7 chiffrées), `lv.social = []`, `lv.paid.imp30 = 0` et `cpm = null` partout, `fyStart = null` partout.

| # | Écran | Ce qu'il affiche réellement | Défaut |
|---|---|---|---|
| 1 | **Cockpit** | « Pipe ouvert **0 €** · 0 opportunités · 0 € créés sur la période » ; « Opportunités créées 0 » ; graphique « Pipe créé par mois » **entièrement plat à zéro** sur 6 mois. Or `company.json` porte la réserve exacte (« Le montant est absent sur 280 des 321 deals ouverts ») et `patch_fixes.py` calcule même la variable `oppsSansMontant` (l. 1267) — **qui n'est jamais affichée**. Un 0 € nu se lit « pas d'affaires », pas « pas chiffrées ». | **BLOQUANT** |
| 1b | Cockpit — « Couverture du plan » | Paid **0/10**, Social **0/10**, SDR **2/16** en barres rouges, sans un mot sur la raison (la régie ne donne pas l'exposition par compte sur 30 j ; la page LinkedIn est inaccessible). Un rouge « on ne fait pas le travail » alors que le vrai message est « on ne mesure pas ». | **BLOQUANT** |
| 1c | Cockpit — « RDV par source » et légende du graphique | 5 séries pour 4 couleurs : `legendOf(Object.entries(RDV_SRC).map(([k,l],i) => ['var(--c'+(i+1)+')', l]))` (l. 1299 et 1310) demande `var(--c5)`, **qui n'existe pas** dans `:root` (l. 19, `--c1…--c4` seulement). Vérifié : `getComputedStyle().getPropertyValue('--c5')` renvoie vide. La pastille et la barre « Non attribué » sont invisibles. | à corriger |
| 1d | Cockpit — tiroir d'import | Vérifié à l'écran : le texte affirme « Chaque compte reçoit un comité, un historique, des signaux et une activité de leviers **simulés** » (l. 1283) — dans une application dont le bandeau dit « données réelles ». Coller « Airbus / Danone » et cliquer « Remplacer le portefeuille » écrit `abm-tdc-names=["Airbus","Danone"]` en localStorage, **ne change rien** (30 comptes avant, 30 après) et affiche le toast « **30 comptes chargés et scorés** ». Trois mensonges dans un seul contrôle. Bouton « Revenir à l'exemple (100) » idem. | **BLOQUANT** |
| 2 | **Signaux captés** | Correct et honnête. Le chip « Externe » ne peut jamais rien renvoyer (aucun `job`/`hiring`/`news`) ; idem pour le badge de sidebar `#bS` = 0 (aucun signal fort ≤ 7 j). Rien de faux, mais un filtre mort. | cosmétique |
| 3 | **Agents** | Réécrit en catalogue honnête (« aucun agent n'a encore été mis en marche », « Actions exécutées 0 »). Un défaut d'accord : « En attente d'une source **3** — **1 complètement bloqués** » (l. 2892). | cosmétique |
| 4 | **Fiche compte** — carte du comité | Correcte. La légende annonce « pointillé = cible à trouver » alors qu'aucun contact n'a `prov: 'cible'` : entrée de légende sans objet. | cosmétique |
| 4b | Fiche compte — frise | La ligne d'agrégat des signaux sans contact est sous-titrée « **recrutements, actualité** » (l. 1820). Ce sont en réalité 179 visites de page et réponses e-mail non rattachées. Le sous-titre décrit la maquette, pas la donnée. | **à corriger** |
| 4c | Fiche compte — Plan d'attaque | L'accroche par défaut (l. 1721) affirme « **Exposé à nos campagnes depuis 11 mois** : envoyer le cas client Logiciel le plus proche ». Vérifié sur Contentsquare : le signal le plus fort est une **réponse e-mail**, et les « 11 mois » sont l'âge du *plus ancien signal, tous types confondus*. C'est une affirmation d'exposition publicitaire qui n'est pas mesurée. Le type `reply` n'a aucune branche dans `plan()` et retombe donc systématiquement dans cette phrase. | **BLOQUANT** |
| 4d | Fiche compte — en-tête | `noteNom` et `nomCRM` sont dans la donnée mais **jamais affichés** (0 occurrence). L'ESSCA s'affiche « ESSCA » sans trace de la note « fiche nommée « Rothschild & Co » au CRM ». `assemble.py` promet pourtant en commentaire « on garde le nom d'origine, **visible sur la fiche compte** ». | **à corriger** |
| 5 | **Content** (entreprise) | Réécrit, sourcé. Deux problèmes : (a) la carte « SEO — ce que le site capte » affiche « **[object Object]** · Search Console » (l. 2684, `CO.seo.domaine` est un objet) et **« Clics Search Console 0 » / « Mots-clés positionnés 0 »** (l. 2686-2687 : les clés `gsc.clics_total`, `gsc.clics`, `apercu.mots_cles`, `apercu.nb_mots_cles` **n'existent pas** ; les vraies sont `gsc.totaux_par_dimension` et `apercu.nombre_mots_cles_organiques = 242`, `trafic_organique_estime = 4659`) — deux zéros présentés comme des mesures, contredits par la carte « Réserves » juste en dessous qui cite « 4 400 / 8 488 / 8 364 » clics. (b) Le KPI dit « Dont Lead Gen LinkedIn **95 %** » et la réserve deux cartes plus bas dit « **84 %** des formulaires sont des formulaires LinkedIn Lead Gen » : deux chiffres pour la même grandeur sur le même écran. | **BLOQUANT** ×2 |
| 5b | Content — vocabulaire | « Signaux de contenu **516** » et le tableau « Les contenus qui font remplir un formulaire » dont la première ligne est « **E-mail entrant (réponse) — Re** · 141 soumissions ». `reply` a été ajouté à `CONTENT_T` : 211 réponses e-mail et 113 visites de page sont comptées comme du contenu consommé. | **à corriger** |
| 6 | **Paid** (entreprise) | Réécrit, honnête et sourcé (34 193 € LinkedIn, 30 805 € Meta, 18 campagnes réelles). Un mot de trop : le KPI « Comptes **du plan** exposés 11/30 » utilise `accounts.length` au dénominateur, pas `inPlan` (l. 2642) — `inPlan` est calculé et inutilisé dans cette branche. | cosmétique |
| 7 | **Social** | Réécrit en « non branché » explicite, avec le constat et ce qui manque. Exemplaire. | — |
| 8 | **Outbound** | Réécrit, sourcé. | — |
| 9 | **SDR** | Réécrit : « Taux de décroché 29 % — 99 conversations sur 343 appels », numérateur et dénominateur sur la même fenêtre. **Le bug de la maquette est corrigé** : l'ancien `pct(D.connects, D.calls30)` mélangeait 24 mois et 30 jours et produisait des taux de **200 % et 500 %** (Malakoff Humanis, Société Générale) — vérifié sur la donnée. Reste le libellé `CALL_OUT.call` du §1. | — |
| 10 | **Sales** | Réécrit, sourcé (78 RDV tenus, 7 chiffrages perdus, 357 000 € cumulés, toutes les transactions listées avec « montant non renseigné » quand il manque). | — |
| 5-10b | **« Suivi compte par compte »** (commun aux 6 leviers, `suiviHTML` l. 1405, **non réécrit**) | Les chips de statut viennent de `FILTERS` (l. 1389, maquette) et **ne correspondent plus aux états produits par le nouveau `leverRow`**. Vérifié à l'écran : Social affiche 10 lignes « non branché » et trois chips à **0** (« Silencieux 0 · Engagé 0 · Décideur engagé 0 ») ; Sales propose « Rien d'ouvert / Début de cycle / R1 / Avancé / client » alors que les états réels sont « perdue il y a 1 an / jamais rencontré / rencontré, pas d'opportunité » ; SDR et Sales n'ont pas de chip pour l'état `mute`, dont les lignes sont donc infiltrables. Plus les sélecteurs SDR/AE fictifs du §1. | **BLOQUANT** |
| 11 | **Moteur** | Voir §4. | **BLOQUANT** |
| 12 | *Proposition* | Route supprimée, code mort. | à corriger (retirer) |
| 13 | *Fiche compte — leviers* (`leverAccount`) | Réécrite, honnête, avec les bonnes réserves (« Le CRM ne stocke ni l'heure ni la durée de l'appel »). L'ancienne version affichait « **nullhnull** » dans la colonne Heure sur les 343 appels : corrigé. | — |

**Écrans vides ou trompeurs à signaler : 6** — Cockpit (pipe à 0 € sans explication · couverture du plan à 0 sans explication · tiroir d'import menteur), Content (SEO 0/0 et 95 % vs 84 %), Fiche compte (frise mal sous-titrée, accroche inventée), Suivi compte par compte (chips désynchronisées, SDR/AE fictifs), Moteur (pilier fantôme), Signaux (filtre « Externe » mort — mineur).

---

## 4. Cohérence du scoring

### 4.1 `MODELE.md` ne décrit pas le code

| `MODELE.md` annonce | Le code applique | Écart |
|---|---|---|
| ICP — Secteur, poids 25 | `sectorIn: 30` / `sectorOut: 8` (l. 897) | poids annoncé ≠ poids appliqué |
| ICP — Taille, poids 20 | `size: {s:18, m:40, l:30, xl:22}` (l. 893), max 40 | poids annoncé ≠ poids appliqué |
| ICP — Surface d'attaque, poids 20 | `multi: 12` (l. 903) | idem |
| ICP — Historique, poids 20 | `hist` max 25 (l. 899) | idem |
| **ICP — Ancienneté de la fiche, poids 15** (« Comptes créés 2000-2016 signent à 1,2-1,5 % ») | **rien** : aucune ligne dans `scoreICP` (l. 1041-1052), aucun champ de date de création sur `Account` | **pilier documenté, non calculé** |
| ENG — Comité 35 / Intention 30 / Timing 20 | `w: {intent: 40, comite: 40, timing: 20}` (l. 917) | poids annoncés ≠ appliqués |
| **ENG — Réciprocité, poids 15** (« signaux ÷ touches ») | **rien** : `scoreENG` (l. 1053-1079) n'a que trois piliers | **pilier documenté, non calculé** — et la matière existe (`a.crm.touches`) |
| ENG — Malus « aucun signal digital » | malus `noContact` = « aucun contact actif au CRM » (l. 1077) | **malus documenté non implémenté ; un autre l'a remplacé** |
| Quadrants : seuils ICP 70 · engagement 65 | `matrix: {icp: 55, eng: 45}` (l. 931) | **écart de 15 et 20 points** sur les seuils qui découpent tout le portefeuille |
| « clics pondérés ×4, ouvertures plafonnées » (Apple MPP) | `sig.click = 5`, `sig.open = 1`, aucun plafonnement (l. 924) | règle annoncée, non implémentée |

### 4.2 Le commentaire du code ne décrit pas le code non plus

- **`hist.chiffre: 20` n'est jamais appliqué.** `DEFAULT_CFG` (l. 899) déclare `hist: { client: 25, ancien: 22, **chiffre: 20**, encours: 15, perdu: 12, jamais: 0 }` et le commentaire juste au-dessus explique la règle (« Un chiffrage déjà accepté en interne rouvre plus vite »). Or `scoreICP` (l. 1046) est resté celui de la maquette : `if (I.hist[a.status]) lines.push(…)`. `'chiffre'` n'est pas un statut : la clé est morte. **`patch_config.py` a bien tenté ce patch (lignes 55-64) mais sa chaîne de recherche `const hi = C.icp.hist[a.status]; …` ne correspond pas au code réel — il imprime « ATTENTION » et continue sans `sys.exit`.** Un patch qui échoue en silence : exactement le motif à vérifier après chaque changement de constante.
- **Le pilier Timing vaut 0 pour les 30 comptes.** Il ne se déclenche que sur `t:'job'` (≤ 90 j) ou `t:'hiring'/'news'` (≤ 60 j) — **aucun de ces types n'existe dans la donnée** (`assemble.py` n'en produit pas). Il pèse pourtant `w.timing = 20`, soit **20 % du score d'engagement rabotés uniformément** : le maximum atteignable est 80/100 (vérifié : MGEN et Veolia plafonnent à 80). Le seuil de quadrant `eng ≥ 45` est calibré sur cette échelle amputée sans que rien ne le dise. L'écran Moteur affiche « Timing 0/100 · +0 · Rien de relevé » pour tout le monde, et propose deux curseurs (`eng.timing.job` 55, `eng.timing.event` 45) qui ne peuvent rien changer.
- **Le pilier Comité ne discrimine pas** : `prov` ne vaut que `actif` ou `hors` dans la donnée réelle, donc `cover` est élevé partout et 27 comptes sur 30 obtiennent exactement 70 ou 100. Un pilier à 40 % du poids dont la variance est quasi nulle.
- **La bande de taille ne correspond pas à sa justification.** Le commentaire (l. 890-892) cite « 201-1 000 sal. 1,5 %, 1 000-5 000 1,0 %, 5 000+ 0,8 %, <200 0,4-0,7 % ». `sizeBand` (l. 1033) coupe à 500 / 2 000 / 10 000. Le poids maximal (40) est attribué à la tranche 500-1 999, qui n'est aucune des tranches mesurées.
- **`calibrage.json` n'existe pas.** Le commentaire de `matrix` (l. 930) renvoie à « voir calibrage.json » ; le fichier est absent de `data/`. Source citée, source introuvable.

### 4.3 Ce que le Moteur affiche

- **Le barème `.formula` (l. 2470) ment** : « ICP = taille + secteur + historique + multi-entités + **exercice fiscal** − perte récente ». Le pilier exercice fiscal est neutralisé (`fy: {prep: 0, start: 0}`) et `fyStart` est `null` sur les 30 comptes. `patch_final.py` a corrigé la note pédagogique juste au-dessus mais **pas la formule**.
- **« Répartition du portefeuille : janvier 0 · avril 0 · juillet 0 · octobre 0 »** (l. 2480) — quatre zéros présentés comme une répartition, avec deux curseurs de fenêtre budgétaire au-dessous. Vérifié à l'écran.
- **La table des poids d'historique (l. 2478) expose « Ancien client » et « Client (expansion) », deux statuts qui n'existent pas dans la donnée, et omet `perdu: 12`, le seul poids d'historique réellement appliqué** (à 10 comptes sur 30). Régler les curseurs visibles ne change rien ; le poids qui agit est invisible.
- **Le seuil de 180 jours du malus de perte est toujours codé en dur** (l. 1050 : `if (a.hist.loss && a.hist.loss.d < 180)`) alors que `lossMalus` est réglable. Le piège de la carte est **encore actif**. Il concerne 4 comptes sur 10.
- Les curseurs de poids de signal exposent `job`, `hiring`, `news` à 0 — cohérent avec l'absence de source, mais ce sont trois lignes de réglage sans objet.
- `PRESETS` (l. 933) « Intention d'abord » impose `half: 21` et écrase la demi-vie calibrée à 120 j sans le dire.

---

## 5. Les pièges de la carte technique, section 7

| Piège | État | Détail |
|---|---|---|
| **P1 — `enrich()` écrase les journaux** | ✅ **traité** | `rebuild()` (l. 1104) ne l'appelle plus, commentaire explicite. La fonction reste dans le fichier (l. 853). |
| **P2 — jointures par égalité de chaîne** | ✅ **traité par contournement** | `assetOf` (l. 841) : mort avec `ASSETS`. `rdvEvents` : **réécrit**, ne compare plus `s.det === 'Demande de démo'` mais part des meetings réels. `plan()` : `strong.det.replace(/^.*« \|».*$/g,'')` et `.split(' prend')[0]` **encore présents** (l. 1719-1720) sur les branches `dl`/`webinar`/`job` ; inatteignables faute de signaux `job`, atteignables pour `dl` (1 signal). |
| **P3 — `V().clientWidth` + re-rendu au resize** | ⚠️ **encore actif, et étendu** | l. 1261 inchangé ; `levers.js` **reproduit le motif quatre fois** (l. 2652, 2716, 2760, 2801 : `Math.max(320, (V().clientWidth \|\| 1100) - 80)`). Un rendu hors document (capture, iframe masquée) retombe sur 1100 px. L'écouteur `resize` (l. 2917) ne re-rend que le cockpit : les graphiques des leviers restent figés à la largeur du premier rendu. |
| Indexation temporelle inversée | ✅ cohérente | `assemble.py` remplit `callsW[11 - j//7]`, les vues lisent `wk[11 - w]`. Les agrégats `imp30 = sum(w.slice(0,4))` de la maquette sont morts. |
| **`monthIdx` ancré sur 2025-10** | ⚠️ neutre aujourd'hui, piège intact | l. 726 inchangé. Avec `TODAY = 2026-09-21`, l'index 11 tombe bien sur septembre 2026 : cohérent avec l'axe `MONTHS`. Mais `monthly` **n'est plus lu nulle part** (0 occurrence) — 18 Ko de donnée morte dans le payload. |
| **`TODAY` figé** | ⚠️ **actif, 5 endroits** | `TODAY`/`WEEK_NOW` (l. 712), `MTD` (l. 842), le HTML statique « Semaine 39 / lundi 21 septembre 2026 » (l. 702), **et deux chaînes qui disent encore « 18 »** : l. 1566 « rythme attendu **au 18** : 70 % » (code mort) et l. 1995 « % du budget **au 18** » (code mort). Le passage 18 → 21 a été fait à trois endroits sur cinq. |
| Ids de contacts locaux au compte | ⚠️ inoffensif ici | `a.id + s.who` (l. 1824) ; les ids sont `a<crmId>` + `c<n>`, pas de collision possible. |
| **`sorted()[0]` sans garde** | ⚠️ **encore actif** | l. 1145 (`go('compte', …)`), l. 1436 (`renderLever`), l. 1749 (`renderAccount`). Avec un filtre qui ne laisse rien, `sorted()[0].id` lève. Non atteint en pratique car le portefeuille n'est jamais vide. |
| **`ctOf` masque les erreurs** | ⚠️ **encore actif** | l. 1348 renvoie un contact fantôme `{name:'—', role:'ope'}`. `levers.js` ne l'appelle plus que quand `s.who` est renseigné (l. 2785), donc l'exposition est réduite ; mais la fonction reste et `renderSignals` (l. 1879) l'utilise avec une garde. |
| **`a.plan` non sérialisable** | ✅ traité | `Set` construit par `rescore()` (l. 1092), jamais fourni par `accounts.json`. |
| **`agentCfg()` mute à la lecture** | ✅ sans objet | `renderAgents` réécrit ne l'appelle plus ; `ui.agents` reste initialisé et persistable, mais plus rien ne l'écrit. |
| **Images en chemin relatif** | ✅ **traité** | `patch_final.py` vide `CREA_IMG` (l. 1460 : `const CREA_IMG = {}; const CREA_IMG_OFF = {…`). `IMG = n => 'img/' + n + '.jpg'` (l. 1459) subsiste mais n'est appelé que par `coverHTML`/`toolHTML`/`postHTML`/`browserHTML`, tous morts. Le dossier `img/` n'existe pas à côté du fichier. |
| `history.replaceState` seul | inchangé | le bouton Précédent sort de l'application. |
| `docmode` sur `<body>` | inoffensif | jamais activé ; `.doctop` est en `display:none` (l. 602). Le DOM mort `#dtClient / #dtCur / #dtProg` reste (l. 698). |
| `openModal` capture `document.onkeydown` | inoffensif | plus atteignable. |
| Scroll restauré à la main | inchangé | `levers.js` reproduit correctement le motif (l. 2909). |
| **Nouveau piège introduit** | ⚠️ | `patch_levers.py` s'appuie sur le **hoisting** : cinq fonctions sont déclarées deux fois et seule la dernière compte. C'est correct en JavaScript, mais 450 lignes de maquette restent exécutables, et toute réorganisation du fichier (minification qui convertit `function f(){}` en `const f = …`, découpage en modules) inverserait silencieusement le résultat. |

---

## 6. Chiffres, dates et montants en dur (hors `DATA`)

| Ligne | Contenu | Verdict |
|---|---|---|
| 699 | Bandeau : « **Données réelles du CRM Bulldozer** · relevé du 21 septembre 2026 · un levier sans source affiche ce qu'il manque, **jamais un chiffre inventé** » | **La promesse est démentie** par les constats du §1 et du §3. Soit on corrige, soit on retire la phrase. **BLOQUANT** |
| 702 | « Semaine 39 » / « lundi 21 septembre 2026 » en dur | justifié tant que `TODAY` est figé ; à dériver de `TODAY`. |
| 712, 842 | `TODAY = new Date(2026, 8, 21)`, `MTD = 21/30` | justifié (date de relevé). |
| 726 | `monthIdx` ancré sur 2025-10 | constante muette, cf. §5. |
| 795-796 | `SDRS`, `AES` : **7 noms de personnes** | **ment** — affiché. **BLOQUANT** |
| 810 | `EMAIL_TYPES` : `open: .62/.5/.38/.55/.7/.58`, `click`, `reply` | ment (code mort). |
| 820 | `CAMP_DEF` : **6 000 / 8 000 / 5 000 / 3 000 €** de budget mensuel | ment (code mort). |
| 822 | `CREAS` : 8 CTR (`.011` … `.0029`) | ment (code mort). |
| 832 | `ASSETS` : `li: 2500/3000/1200/1500/1000/800` — « budget LinkedIn / mois » | ment (code mort). |
| 890-892 | Commentaire : « 201-1 000 sal. 1,5 %, 1 000-5 000 1,0 %… » | chiffres sourcés mais **les bandes du code ne sont pas celles-là**. |
| 895-896 | « Logiciel 33,9 %, Conseil 14,7 %, Banque & assurance 10,7 %, Distribution 8,1 % » | sourcé (495 clients signés). |
| 902 | « Veolia via SARP et Veolia Recyclage, Carrefour via Carrefour Pro » | sourcé. |
| 918-919 | « 5,3 % de signature contre 0,5 % », « contenu téléchargé 3,9 % » | sourcé (étude outbound 17/09). |
| 921-924 | « 76 % des comptes en ont un », « jusqu'à 110 en 3 semaines » | sourcé. |
| 930 | « voir calibrage.json » | **source inexistante**. à corriger |
| 1485 | `roiHTML` : 100 comptes, **8 %** de signature, 45 000 €, 60 000 € | ment (code mort) ; les 8 % contredisent les 0,7-5,3 % mesurés. |
| 1566, 1995 | « rythme attendu **au 18** » | date obsolète (code mort). |
| 1568 | seuil CTR `0.0035` / « CTR sous 0,35 % » | convention de gestion (code mort), reprise dans `AGENTS.paid.does` (l. 845, **affichée** dans le catalogue) — une règle choisie, pas mesurée. |
| 1721 | « Exposé à nos campagnes depuis N mois » | **ment** — affiché. **BLOQUANT** |
| 1820 | « recrutements, actualité » | **ment** — affiché. à corriger |
| 2470 | Formule ICP incluant « exercice fiscal » | **ment** — affiché. **BLOQUANT** |
| 2480 | « janvier 0 · avril 0 · juillet 0 · octobre 0 » | zéros présentés comme une répartition. à corriger |
| 2686-2687 | Clics Search Console `0`, mots-clés `0` | **ment** (mauvaises clés) — affiché. **BLOQUANT** |
| 2684 | `esc(CO.seo.domaine)` → « [object Object] » | bug d'affichage. à corriger |
| 2686 | « Search Console, **113 jours** relevés » en dur | à dériver de `CO.seo.gsc.jours_reellement_stockes`. |
| 2630, 2645 | « 1er janvier au 20 septembre 2026 » en dur | justifié (fenêtre du relevé), à dériver. |
| 2892 | « 1 complètement **bloqués** » | accord. cosmétique |
| 2358-2450 | `PRICE_DEF` `{socle:4200, pilot:1800, mkt:1200, sales:1200, os:900}`, plan de mission 16 semaines | tarifs d'une proposition client dans un outil interne (code mort). à retirer |

**Données réelles injectées et jamais affichées** — l'inverse du problème, mais la même perte : `crm.expo90`/`eng90`, `crm.contactsAssocies`/`contactsVus`/`ecart` (l'écart contacts que `MODELE.md` promet « affiché compte par compte »), `crm.sansEmail`, `crm.dealsAuto`, `crm.formulaires`, `crm.visites`, `crm.joignables`, `nomCRM`, `noteNom`, `secteurOrigine`, `secteurJustif`, `contact.seniorite`/`crmId`, `monthly`, `n30`, et surtout **`DATA.company.pipeline` (entonnoir réel : 714 R1 → 95 gagnés, 13,31 %, durée médiane 36 j), `DATA.company.activite` et `DATA.company.sea`** : trois sections complètes de données sourcées et assorties de leurs réserves, présentes dans le payload, que **seul `pipeline.reserves`** effleure. Le cockpit affiche « 0 € » alors que la vraie matière pour un cockpit de pipeline est dans le fichier.

---

## 7. Corrections, par ordre

### Bloquant — un chiffre inventé ou faux est affiché comme mesuré

1. **Retirer les 7 personnes fictives des filtres SDR et AE** (l. 1413) : construire la liste à partir de `new Set(accounts.map(a => a.lv.sdr.owner))` / `a.lv.sales.ae`, ou supprimer le sélecteur. *(SDRS l. 795, AES l. 796)*
2. **Réparer la carte SEO** (l. 2684-2688) : `CO.seo.domaine.confirme`, `CO.seo.gsc.totaux_par_dimension`, `CO.seo.apercu.nombre_mots_cles_organiques` (242) et `trafic_organique_estime` (4 659) — ou retirer la carte. Aujourd'hui elle affiche « [object Object] » et deux zéros que la carte « Réserves » du même écran contredit.
3. **Dire pourquoi le pipe est à 0 €** (l. 1267-1287) : `oppsSansMontant` est déjà calculé et jamais affiché. Brancher `DATA.company.pipeline` (entonnoir réel 714 → 95, 13,31 %) plutôt qu'un graphique plat, et porter la réserve « 280 des 321 transactions ouvertes n'ont aucun montant ».
4. **Corriger l'accroche par défaut de `plan()`** (l. 1721) : ne pas affirmer une exposition publicitaire non mesurée ; ajouter une branche pour `reply` (211 signaux sur 516 y retombent).
5. **Corriger le libellé `CALL_OUT.call`** (l. 818) en « Résultat non saisi », pour s'aligner sur ce que la vue entreprise du même levier affiche déjà (l. 2705). 19 appels réels sont aujourd'hui étiquetés « Rappel demandé ».
6. **Réconcilier 95 % et 84 %** sur l'écran Content (KPI l. 2673 vs réserve de `company.json`) : une seule définition du dénominateur, recalculée aux deux endroits.
7. **Retirer la formule « exercice fiscal »** du bloc `.formula` du Moteur (l. 2470) et la ligne « Répartition du portefeuille : janvier 0 · avril 0 … » (l. 2480), ou les remplacer par « non renseigné dans le CRM ».
8. **Neutraliser ou désactiver le tiroir d'import** (l. 1283-1345) : il annonce des données simulées, n'a aucun effet, et affiche « 30 comptes chargés et scorés ». Au minimum : retirer le mot « simulés », retirer « Revenir à l'exemple (100) », et faire échouer explicitement l'import tant que `rebuild()` ne lit pas `names`.
9. **Synchroniser `FILTERS` (l. 1389) avec les états du nouveau `leverRow`** : ajouter `mute`, corriger les libellés Sales et Outbound, supprimer les chips qui comptent structurellement 0 (Social).
10. **Expliquer les 0 de « Couverture du plan »** (l. 1279) : distinguer « levier non activé » de « levier non mesurable » (Paid et Social n'ont pas de source par compte sur 30 j).

### À corriger

11. **Appliquer le patch `hist.chiffre` qui a échoué en silence** (`patch_config.py` l. 55-64 → `scoreICP` l. 1046), ou retirer la clé `chiffre: 20` de `DEFAULT_CFG` et le commentaire qui la justifie. Ajouter un `sys.exit(1)` sur cet échec.
12. **Trancher le pilier Timing** : soit le retirer (et redistribuer ses 20 points), soit afficher sur le Moteur et sur chaque fiche que 20 % de l'échelle est inatteignable faute de source. Aujourd'hui l'engagement plafonne à 80/100 sans que rien ne le dise.
13. **Mettre `MODELE.md` en accord avec le code** : poids réels, suppression des piliers « Ancienneté de la fiche » (15) et « Réciprocité » (15) qui ne sont pas calculés, seuils de quadrant 55/45 et non 70/65, retrait de la règle MPP « clics ×4 » non implémentée.
14. **Exposer `icp.hist.perdu` dans le Moteur** (l. 2478) et retirer « Ancien client » / « Client (expansion) », statuts absents de la donnée.
15. **Sortir le seuil 180 j dans la configuration** (l. 1050) : `C.icp.lossWindow`.
16. **Afficher `noteNom` / `nomCRM` sur la fiche compte** — `assemble.py` le promet en commentaire ; l'ESSCA s'affiche sans sa note. Afficher aussi `crm.ecart` (l'écart contacts que `MODELE.md` promet compte par compte) et `secteurJustif`.
17. **Corriger le sous-titre « recrutements, actualité »** de la frise (l. 1820).
18. **Sortir `reply` (et `page`) de `CONTENT_T`** (l. 763) ou renommer le KPI : « Signaux de contenu 516 » compte 211 réponses e-mail et 113 visites.
19. **Créer `calibrage.json`** ou retirer la référence (l. 930).
20. **Ajouter `var(--c5)`** à `:root` (l. 19) pour la série « Non attribué ».
21. **Corriger « 1 complètement bloqués »** (l. 2892) et « Comptes du plan exposés » qui divise par `accounts.length` (l. 2642).

### Nettoyage — supprimer le code mort

22. **Supprimer les 5 fonctions de maquette écrasées** (`paidOf` 1357, `leverRow` 1371, `leverCompany` 1543, `leverAccount` 1620, `renderAgents` 2060) plutôt que de compter sur le hoisting.
23. **Supprimer les générateurs morts** : `buildAccount` (952), `enrich` (853), `sampleNames` (949) + `names` (1083), `assetStats` (1363), `creaStats` (1521), `taskItems` (1985), `agentRun` (2043), `agentCfg` (1973), `contentLibrary` (1523), `lpHTML`/`tplHTML`/`roiHTML`/`openModal`/`bindLibrary`, `narrative`, `frise`, `stageWeeks`, `stageLegend`, `planNote`, `propState`.
24. **Supprimer les référentiels inventés devenus morts** : `CAMP_DEF`, `CAMPQ`, `CREAS`, `ASSETS`, `assetOf`, `LIB`, `CHAPTERS`, `POSTS`, `SEQS`, `EMAIL_TYPES`, `MEET`, `OPP_STAGES`, `LOSS_REASONS`, `FY_STARTS`, `CAMPS`, `CONTACT_SIGS`, `FIRST`, `LAST`, `TITLES`, `CITIES`, `P1`, `P2`, `FORMS`, `IMG`, `CREA_IMG_OFF`, ainsi que la fausse marque « Tour de contrôle ABM » / `tour-de-controle.fr` (l. 1483-1484).
25. **Supprimer la proposition commerciale** : `renderMission` (1218), `renderOffre` (2355), `renderPropal` (2278), `PHASES`, `PRICE_DEF`, `RACI`, `TEAM`, `RITUALS`, `KPI_SPRINT`, `OFFRE_DEF`, `LEVER_DOC`, `ganttRows`, `dayDate`, `docScroll`, le DOM `.doctop` (l. 698) et la clé `abm-tdc-pp`.
26. **Nettoyer le payload** : `monthly` et `n30` ne sont lus nulle part (~18 Ko).
27. **Dériver les dates** : « Semaine 39 / lundi 21 septembre 2026 » (l. 702), « 113 jours » (2686), « 1er janvier au 20 septembre 2026 » (2630) ; corriger les deux « au 18 » résiduels (1566, 1995) s'ils survivent au nettoyage.
28. **Fiabiliser la chaîne de construction** : `patch_config.py` doit sortir en erreur quand une substitution échoue (aujourd'hui il imprime « ATTENTION » et continue — c'est ainsi que `hist.chiffre` s'est perdu), et `build.sh` doit vérifier après coup qu'aucune des clés attendues ne manque.

# Bibliothèque des contenus d'acquisition Bulldozer — relevé du 21/09/2026

Projet **Bulldozer Interne** — customerId `533c1f8f-bcc2-4e95-a3ee-4e630b86dbbf`, projectId `b09bf643-e087-4e6c-8415-f9ee96e5cc94`.
Lecture seule : aucun `bdzCreate*`, `bdzUpdate*`, `bdzDelete*`, `bdzStart*`, `bdzCancel*`.
Données : `bibliotheque.json` (1,6 Mo) · visuels : `img/` (101 images + 7 mp4).

---

## 1. Ce qui a été trouvé

### Périmètre

| | LinkedIn (BULLDOZER) | Meta (Bulldozer) |
|---|---|---|
| adAccountId | `99567c90-5662-4568-aa1b-88fd727cbf1c` | `0ecad557-21bb-4f2a-bdd9-b99eda421e84` |
| Annonces référencées sur 2026 | 225 | 2 048 |
| Annonces **avec métriques** sur 2026 | 225 | 531 |
| Dépense 2026 recomposée | 34 193,26 € | 19 634,45 € |
| Fraîcheur | dataThrough 2026-09-20, import SUCCESS le 21/09 | idem |

**756 annonces** retenues (celles qui ont réellement diffusé entre le 01/01 et le 21/09/2026), **53 827,71 €**.
Les 1 517 annonces Meta référencées sans aucune métrique sur la période ne sont pas reprises.

### Séparation acquisition / budget client

Le piège annoncé — sur Meta, acquisition agence et campagnes clientes partagent le compte — est bien réel, mais **il ne mord pas sur 2026** : les 9 campagnes préfixées `Client_` existent dans le compte et n'ont diffusé qu'en octobre-novembre 2025. **0 annonce marquée `client: true`** sur la période. Le champ est quand même porté par chaque entrée.

En revanche une autre séparation s'impose, que j'ai ajoutée sous `nature` :

| nature | annonces | dépense 2026 |
|---|---|---|
| `acquisition_bulldozer` | 347 | 41 622 € |
| `test_traction_prospect` (TDT, Carrefour Pro, Sunology, YAMPA) | 409 | 12 205 € |
| `client` | 0 | 0 € |

Les TDT sont du budget Bulldozer, mais leurs créas vendent le produit du prospect (Veolia, Cafeyn, Louve Invest, AgatheYou, Nona, Phily…), pas Bulldozer. Ne pas les mélanger à l'acquisition de l'agence.

### Ce qui est visible

- **718 annonces sur 756 portent un nom** ; 38 annonces LinkedIn ont un nom vide dans la régie.
- **117 créatives interrogées** — toutes les annonces d'acquisition Bulldozer à ≥ 50 € (96/96, soit **92,9 % de la dépense d'acquisition 2026**) plus les tests de traction à ≥ 150 €.
- **109 URL de visuel** relevées, **108 fichiers téléchargés** : 101 images (redimensionnées à 600 px de large, 5,7 Mo au total) et 7 mp4 (33 Mo).
- **37 annonces avec un texte** — et c'est là qu'est le vrai constat (§3).
- **190 annonces avec une URL de destination**, **510 avec un lead form** (le format dominant côté LinkedIn).
- **17 landings distinctes**, **80 ressources téléchargeables**, **54 lead forms LinkedIn**.

### Les têtes d'affiche

Côté LinkedIn, deux annonces portent 7 185 € à elles seules : `Claude for Marketing` et `Dupliquer_Claude for Marketing` (campagne *TLG II BOFU*) — le visuel est la couverture du **Guide du CMO 2026 sur Claude** co-brandé Anthropic, servi derrière le lead form « Global Form - Ending Send Doc - BOFU » (41 annonces, 15 431 € en 2026 : le formulaire de loin le plus sollicité).

Côté Meta, la tête est `New Sales ad – Copy` (1 954 €), l'affiche métro « SI CLAUDE EST UN CHANTEUR POUR CERTAINS, POUR D'AUTRES IL RÉVOLUTIONNE LE MARKETING — 800 clients. 2 500 missions. 200M€ générés ». Deux familles de texte couvrent 16 des 37 textes relevés : « Le marketing devient AI-first » (10 annonces) et « L'avenir du marketing est IA-first » (6). 22 corps de texte distincts en tout.

### Landings

| Destination | Annonces | Dépense 2026 | Dans le CMS de l'OS |
|---|---|---|---|
| `bulldozer-collective.com` (racine, https + http) | 72 | 23 568 € | oui — page *Home* |
| `bulldozer-collective.com/fr` | 47 | 2 558 € | **non** |
| `bulldozer-collective.com/prendre-rendez-vous-typeform` | 24 | 2 183 € | oui — page *Prendre rendez-vous* |
| `fb.me` (placeholder Meta lead ad) | 12 | 2 841 € | n/a |
| `/fr/offer/sea-2-0`, `/fr/offer/seo-aeo-geo` | 2 | 443 € | **non** |
| 11 domaines externes (clients TDT, typeform, 4 apps `*.lovable.app`) | 33 | 1 131 € | n/a |

### Contenus téléchargeables

**80 ressources** dans la collection Webflow *Ressources*, dont **77 avec un fichier PDF**. Hub : `/telecharger`, fiches sous `/ressources/<slug>`. Titres exacts relevés, par exemple : « AI-Marketing Stack : 4 use cases pour automatiser votre marketing », « Le baromètre de la fonction marketing 2026 », « L'observatoire de la maturité digitale 2026 », « Search Ads vs. Conversational Ads : The OpenAI Shift », « Weglot x Bulldozer : Kit d'Expansion Internationale », « 4 modèles de growth loops ».

**54 lead forms LinkedIn** avec leur accroche (`headline`) et leur écran de remerciement. 7 seulement ont porté des annonces en 2026.

---

## 2. Ce qui manque

- **Le texte des annonces LinkedIn.** Voir §3 — c'est le point central.
- **Les créatives de 7 annonces sur les 117 interrogées** : `bdzGetAdLayer3Creatives` renvoie `totalElement = 0`. L'annonce existe, sa créative n'a pas été importée. L'une d'elles pèse 849 € avec un CTR de 12 % (campagne *TL - ADS - JORDAN*) : la meilleure performance LinkedIn de l'année n'a ni visuel ni texte dans l'OS.
- **639 annonces sur 756 n'ont pas eu d'appel créative** de ma part (seuil de dépense). `texte.releve: false` signale une absence de relevé, pas une absence de donnée.
- **Un visuel inaccessible** : S3 répond HTTP 200 avec un corps de 22 octets « URL signature mismatch » (annonce `5d829c62`). **Ce n'est pas un blocage de sortie** : `bdz-saas.s3.eu-west-3.amazonaws.com` a répondu 200 et servi l'image sur les 108 autres téléchargements. Aucun domaine bloqué rencontré.
- **7 vidéos sans vignette** dans l'OS : le mp4 a été téléchargé, aucune image fixe n'a pu en être extraite (ni `ffmpeg` ni `imageio-ffmpeg` sur ce poste).
- **Le titre des landings `/fr`** : le seul site branché au CMS de l'OS est le Webflow **« Bulldozer OLD »** (`60f2dbb7048a19fe3d834f6f`, `previewUrl` null, `lastPublishedAt` null, aucun domaine personnalisé). Le site actuel — celui qui sert `/fr` et `/fr/offer/*`, soit 49 annonces et 3 001 € — n'est pas connecté. Ces titres ne sont pas relevables en lecture seule.
- **Aucun 403** sur ce périmètre.

---

## 3. Les champs qui n'existent pas dans l'OS

C'est l'information la plus utile de ce relevé.

| Champ | Constat | Portée |
|---|---|---|
| **`creatives.body` côté LinkedIn** | **null sur 100 % des créatives LinkedIn IMAGE et VIDEO.** Le texte du post sponsorisé n'a jamais été importé. L'OS ne garde que le `contentReference` (`urn:li:share:…` / `urn:li:ugcPost:…`) et l'URL du visuel. Côté Meta le `body` est présent et complet. | toutes les créas LinkedIn sauf 1 |
| **`creatives.title` (accroche)** | **null sur 116 des 117 créatives**, IMAGE comme VIDEO, LinkedIn comme Meta. Aucune accroche n'est stockée nulle part. | 116/117 |
| `layer3.activeFrom` / `activeTo` | null sur **100 %** des 756 annonces : aucune date de lancement ni d'arrêt au niveau annonce. Seules dates exploitables : `reportFrom`/`reportTo` des métriques, et `createdAt`/`updatedAt` de l'import. | 756/756 |
| `reach` / `frequency` côté LinkedIn | null sur les 225 annonces LinkedIn (renseignés sur les 531 Meta). | 225/225 LI |
| `reactions` / `comments` | null sur 745 des 756 annonces ; renseignés sur 11 annonces Meta seulement, jamais sur LinkedIn. | 745/756 |
| `layer3.creativeId` | null partout. | 756/756 |
| `creatives.location` / `time` / `customFooter` / `pages` | null partout. | 117/117 |
| nom de l'annonce | chaîne vide sur 38 annonces LinkedIn : le champ existe, il n'a pas été renseigné dans la régie. | 38/756 |
| métrique `leads` | présente dans l'API, **volontairement écartée** de chaque entrée : connue comme fausse. | 756/756 |

### Une exception qui éclaire le reste

Le **LinkedIn Sponsored Message** (`AD_CREATIVE_TYPE_MESSAGE`, annonce `9fddaab6`, campagne *Message Sponsorisé - ICP Marketing*, 70,96 €) est la **seule** créative LinkedIn qui porte du texte — et elle en porte beaucoup : `title` = `%FIRSTNAME%` (un jeton de personnalisation, pas une accroche), `body` complet, `sender` = `urn:li:person:VHNRpE1FyZ`, libellé de CTA « En discuter ». Le modèle de données sait donc stocker un texte LinkedIn ; c'est l'import des Sponsored Content qui ne le remonte pas.

### Un a priori à corriger

**Le ciblage n'est pas absent.** `bdzListAdLayer2` renvoie un bloc `audience` détaillé — intitulés de poste résolus en `urn:li:title`, tranches d'effectif, géo, langue, exclusions (Freelance, employeur Bulldozer) — plus le `targetingCriteriaRaw` brut, pour **748 des 756 annonces**. Ce sont bien `reach` et `reactions` qui manquent côté LinkedIn, pas le ciblage.

### Un autre a priori à nuancer

L'agrégat `AD_TIME_GRANULARITY_ALL` **n'est pas corrompu au niveau LAYER_3**. Vérifié contre la recomposition journalière de `leviers.json` sur deux témoins : `cc293fee` (LinkedIn) 526,16 € / 113 977 impressions / 2 995 clics et `c78916c1` (Meta) 398,76 € / 93 940 / 5 183 — identique au centime. Les totaux de ce fichier reposent dessus. La corruption connue porte sur d'autres cibles (`LAYER_1_ALL`).

---

## 4. Ce qu'on peut en faire

En l'état, une bibliothèque visuelle est jouable sur Meta (visuel + texte + CTA + destination + dépense) et **amputée sur LinkedIn** : on a le visuel, le CTA, la destination et la performance, mais jamais l'accroche ni le corps. Pour récupérer le texte LinkedIn il faudrait soit un import qui le remonte, soit passer par le `contentReference` et l'API posts — hors périmètre lecture seule d'aujourd'hui.

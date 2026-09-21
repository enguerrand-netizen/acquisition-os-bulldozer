# Acquisition OS Bulldozer

Cockpit d'acquisition de Bulldozer sur ses 30 grands comptes cibles. Page HTML
autonome, branchée sur les données réelles du CRM HubSpot (portail 143561253) et
de Bulldozer OS, relevées le **21 septembre 2026**.

En ligne : <https://bulldozer.bulldozer-os.fr/acquisition-os/>

> **Dépôt privé, et il doit le rester.** Il contient les noms, fonctions et dates
> d'activité de 536 personnes chez des entreprises tierces, les montants réels de
> transactions perdues et le détail de l'activité commerciale de Bulldozer.

## Ce que fait l'outil

Onze écrans : cockpit du portefeuille, signaux captés, catalogue d'agents, fiche
compte, six leviers (Content, Paid, Social, Outbound, SDR, Sales) et le moteur de
scoring. Chaque compte porte deux scores — **ICP** (est-ce qu'il ressemble à ce
qu'on signe ?) et **engagement** (est-ce qu'il bouge ?) — qui se croisent dans une
matrice à quatre quadrants : Attaquer, Réveiller, Qualifier, Veille.

## Règle de fabrication

**Rien n'est inventé.** Un champ sans source vaut `null` et l'écran affiche ce qui
manque plutôt qu'une valeur plausible. C'est la contrainte qui a demandé le plus de
travail : l'outil est un fork d'une maquette de démonstration entièrement peuplée de
données simulées (`spec/reference-index.html`), et il a fallu débrancher les treize
générateurs de faux, vider douze référentiels et neutraliser cinq fonctions.

Trois écrans restent volontairement vides, avec l'explication de ce qu'il faut
brancher : **Social** (aucun post de la page Bulldozer dans l'OS, accès refusé),
**séquences Lemlist** (0 lead exporté, 89 campagnes sur 108 en erreur) et **SEA**
(aucune campagne).

## Reconstruire

```sh
cd build && ./build.sh          # -> build/app.src.html
```

La chaîne repart toujours de `spec/reference-index.html` intact et rejoue onze
passes. **Toute modification faite à la main hors de `build.sh` est perdue au
rejeu** — c'est arrivé une fois, un patch du scoring a disparu en silence et c'est
l'audit de code qui l'a rattrapé. Chaque `patch_*.py` échoue bruyamment (`sys.exit`)
si son ancre a bougé.

| Étape | Rôle |
|---|---|
| `secteurs.py` | Taxonomie en 12 familles, calibrée sur les 495 clients signés. Corrige à la main le secteur de 13 des 30 comptes : le CRM est vide sur 9 et faux sur d'autres. |
| `groupes.py` | Surface d'attaque : les autres entités du même groupe présentes au CRM. Retire les faux rattachements. |
| `company.py` | Pipeline, activité, régies, SEO — le niveau entreprise. |
| `assemble.py` | CRM réel → contrat `Account` de l'application. |
| `contenus.py` / `annonces.py` / `logos.py` | Bibliothèque de contenus, créas publicitaires, logos des cibles. |
| `patch_struct.py` | Identité, date de référence, retrait de la proposition commerciale. |
| `patch_config.py` | Recalibrage du moteur de scoring. |
| `inject.py` | Injection des données (point d'injection unique). |
| `patch_fixes.py` | Corrections d'honnêteté : ne rien afficher qu'on ne mesure pas. |
| `patch_levers.py` | Réécriture des six leviers sur données réelles. |
| `patch_audit.py` | Corrections issues de l'audit de code. |
| `patch_final.py` | Finitions. |
| `patch_brand.py` | Charte Bulldozer, mode clair, GT Pressura embarquée. |
| `patch_logo.py` / `patch_logos.py` | Logo Bulldozer, logos des comptes. |
| `patch_frise.py` | Frises mensuelles et pistes par contact. |

## Volumétrie

30 comptes · 536 contacts avec fonction et rôle · 516 signaux datés · 14 transactions
· 343 appels avec leur résultat · 327 e-mails sortants · 219 entrants · 80 rendez-vous
· 756 annonces 2026 · 18 contenus et 18 formulaires Lead Gen.

## Le scoring, et d'où viennent ses poids

Aucun coefficient n'est arbitraire : chaque poids a une mesure derrière lui, affichée
dans l'écran Moteur. Les deux sources sont le CRM (495 clients signés, 26,17 M€) et
l'étude outbound du 17/09/2026 (4 754 comptes appelés, 33 signés).

- **Le comité pèse autant que l'intention.** Décideur en base + ≥ 2 contacts →
  5,3 % de signature contre 0,5 %. Le contenu téléchargé donne 3,9 %.
- **Le formulaire LinkedIn Lead Gen vaut 4 points, pas 10.** 76 % des comptes en ont
  un, signés comme non signés : il ne discrimine pas.
- **La taille discrimine à l'envers de l'intuition** : 201-1 000 salariés signent à
  1,5 %, les plus de 5 000 à 0,8 %.
- **Secteurs cibles** : Logiciel 34 %, Conseil 15 %, Banque & assurance 11 % des
  clients signés. Plancher à 0,25 sur les secteurs jamais signés — une absence de
  preuve n'est pas une preuve d'impossibilité.
- **Seuils de quadrant posés sur les médianes du portefeuille** (ICP 52, engagement
  65), réglables dans l'écran Moteur. « Fort » veut donc dire « au-dessus de la
  moitié », pas « au-dessus d'un absolu ».

## Réserves à faire voyager avec les chiffres

- Les compteurs du CRM sont **cumulés depuis toujours** et ne peuvent pas être bornés
  à une fenêtre. Seules les dates fenêtrent. Un compteur dit l'épaisseur du lien, pas
  son actualité.
- **35 % des signaux n'ont pas de contact rattaché**, concentrés sur les comptes les
  plus chauds. Ils apparaissent dans une piste « Signaux du compte » séparée.
- Les ouvertures d'e-mail sont **gonflées par Apple MPP** (8 322 ouvertures pour 427
  clics sur le périmètre). Les clics pèsent quatre fois plus dans le score.
- Les **montants manquent sur 280 des 321 transactions ouvertes** du portail : un pipe
  à 0 € ne veut pas dire « pas d'affaires », il veut dire « pas chiffrées ».
- **86 % des transactions gagnées ne passent jamais par un R1** : elles sont créées le
  jour de la signature. Le seul taux lisible est R1 → signature, **13,3 %**, médiane
  36 jours.
- **434 transactions ont été créées automatiquement** par les formulaires Lead Gen. Leur
  nom contient une **espace insécable** avant les deux-points : un filtre à espace
  normale les rate. Exclues des taux.
- L'**exercice fiscal** n'existe nulle part dans le CRM : le pilier est à zéro et
  l'écran le dit.
- Le texte du post sponsorisé **LinkedIn n'a jamais été importé** dans l'OS (vide sur
  100 % des créatives). Sept annonces ne rendent aucune créative, dont la meilleure
  LinkedIn de l'année (849 €, 12 % de CTR).
- **Trois landing pages ont changé d'URL** et les anciennes, celles que les campagnes
  pointaient, renvoient un 404 — dont `seo-vs-geo`, par où 721 contacts sont entrés.

## Deux fiches CRM à ne pas prendre au mot

- **`316281684204` s'appelle « Rothschild & Co » et c'est l'ESSCA.** Ses 18 contacts
  sont en `@essca.eu`, son unique transaction s'appelle « ESSCA ». Et ces adresses
  sont celles d'anciens élèves répartis chez 18 employeurs différents : ce n'est pas
  un compte au sens commercial. Un avertissement est affiché en tête de sa fiche.
- **`19976068547` « Veolia | Énergie Performance » n'est pas un prospect** : comités
  stratégiques mensuels réservés jusqu'en mars 2027 et kick-off de mission au
  calendrier, malgré un cycle de vie « lead ». Avertissement également affiché.

## Vérification

Deux agents adversariaux ont relu le travail, leurs rapports sont dans `spec/` :

- `VERIF-DONNEES.md` — ~950 contrôles unitaires en re-requêtant HubSpot. 18 écarts,
  dont 3 bloquants, tous corrigés : un taux de réponse outbound qui dépassait 100 %
  (les e-mails entrants comptés comme des réponses), Pluxee rattachée à Sodexo alors
  qu'elle en est sortie en 2024, et trois comptes classés « jamais chassés » à tort.
- `AUDIT-CODE.md` — traque des restes de données fictives. Quatre poches trouvées et
  vidées, dont sept noms de commerciaux qui n'existent pas.

## Arborescence

```
build/    la chaîne de construction, rejouable
data/     les extractions CRM et OS, et les rapports de collecte
spec/     carte technique de la maquette d'origine, modèle de scoring, audits
dist/     la page construite
assets/   logos des cibles, captures des landings, vignettes des créas
```

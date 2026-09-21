# CARTE TECHNIQUE — « Tour de contrôle ABM »

Fichier source unique : `/Users/enguerrandchalvondemersay/scratchpad_tourcontrole/vercel-site/index.html`
310 382 octets · 2 487 lignes · HTML + CSS + JS vanilla, aucun build, aucune dépendance JS externe.
En ligne : https://tour-de-controle-abm.vercel.app

Découpage physique du fichier :

| Lignes | Contenu |
|---|---|
| 1–10 | `<head>`, meta, `<title>`, lien Google Fonts |
| 11–658 | `<style>` principal (tout le design system) |
| 659 | `<style>` d'appoint : `[hidden]{display:none!important}` + `img{max-width:100%}` |
| 661–701 | `<body>` statique : `.app` > `aside.side` (sidebar) + `.main` (doctop, banner, phead, `#view`), `#modal`, `#toast` |
| 703–2484 | `<script>` : IIFE unique `(() => { … })()` |
| 2486–2487 | fermeture |

Actifs externes : `img/*.jpg` (8 fichiers : `couv-abm`, `couv-barometre`, `crea-comite`, `crea-portrait`, `crea-webinar`, `lp-hero`, `outil-roi`, `outil-template`) ; `vercel.json` force `Content-Type: text/html; charset=utf-8` sur `/` et `X-Robots-Tag: noindex` partout.

---

## 1. DESIGN SYSTEM

### 1.1 Variables CSS (`:root`, lignes 12–29) — valeurs exactes

**Marine / accents de marque**
```
--navy:#0E2841   --navy-2:#17324D  --navy-3:#21405E
--teal:#4B767C   --teal-l:#BBCCCE
--red:#D0261C    --red-soft:#FBE4E2
--orange:#D9772F --orange-soft:#FBEBDD
--lime:#DDFF56
```

**Surfaces**
```
--bg:#F2F5F6     --surface:#FFFFFF --card:#E8EEF0   --card-2:#F6F8F9
--line:#DCE3E6   --line-2:#C9D3D7
```

**Texte**
```
--text:#0E2841   --body:#33434F   --muted:#5B6B75   --faint:#8A98A0
```

**États (paire couleur / fond)**
```
--ok:#2A7549   --ok-bg:#E0F1E6
--info:#1F5F8B --info-bg:#E2EEF7
--warn:#8F5500 --warn-bg:#FBEED7
--crit:#B3261E --crit-bg:#FBE1DE
--mute-bg:#E9EEF0
```

**Palette catégorielle (ordre fixe, commentaire du code : « catégoriel validé »)**
```
--c1:#D0261C  --c2:#0E8C7A  --c3:#5B55D6  --c4:#C98A0B
--c-pub:var(--c1)  --c-site:var(--c2)  --c-mail:var(--c3)  --c-ext:var(--c4)
```
Les alias `--c-<canal>` correspondent aux 4 clés de `CANAL` (l. 739) : `pub` / `site` / `mail` / `ext`.

**Séquentiel funnel (une teinte)**
```
--s-bofu:#0E2841  --s-mofu:#4F7394  --s-tofu:#A8BED2
```

**Quadrants**
```
--q-A:#D0261C  --q-B:#0E2841  --q-C:#4F7394  --q-D:#B9C6CF
```

**Rôles de contact**
```
--r-dec:#D9772F (décideur)  --r-champ:#0E8C7A (champion)  --r-ope:#8A98A0 (opérationnel)
```
Utilisés par `roleColor(r)` (l. 1113) qui renvoie littéralement `` `var(--r-${r})` ``.

**Typo / géométrie**
```
--f-display:"Barlow Semi Condensed","Arial Narrow",Arial,sans-serif
--f-body:"IBM Plex Sans",system-ui,-apple-system,sans-serif
--f-mono:"IBM Plex Mono",ui-monospace,Menlo,monospace
--r:12px   --r-s:8px   --side:252px
--sh:0 1px 2px rgba(14,40,65,.05),0 10px 28px -20px rgba(14,40,65,.35)
```

### 1.2 Polices

Une seule requête, ligne 10 :
```html
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Semi+Condensed:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@500;600&display=swap">
```
(`preconnect` vers `fonts.googleapis.com` ligne 9.)

- **Barlow Semi Condensed** 500/600/700 → `--f-display` : titres (`h1,h2,h3`), chiffres de KPI, pastilles quadrant, gros nombres.
- **IBM Plex Sans** 400/500/600 → `--f-body` : corps.
- **IBM Plex Mono** 500/600 → `--f-mono` : eyebrows, labels majuscules, badges, chiffres tabulaires.

### 1.3 Échelle typographique

| Usage | Règle CSS (ligne) |
|---|---|
| Corps | `body{font:400 14.5px/1.5 var(--f-body)}` (l. 33) |
| Tous les titres | `h1,h2,h3{font-family:var(--f-display);color:var(--text);text-transform:uppercase;letter-spacing:.02em;line-height:1.05;text-wrap:balance}` (l. 70) |
| Titre de page | `.phead h1{font-size:28px;font-weight:600}` (l. 71) |
| Titre de carte | `.card > header h2{font-size:21px;font-weight:700}` (l. 79) |
| Titre de section | `.sectitle h2{font-size:24px;font-weight:700}` (l. 84) |
| Hero | `.hero h2{font-size:clamp(28px,3.4vw,40px);font-weight:700}` (l. 103) |
| Fiche compte | `.acchead h2{font-size:clamp(30px,3.4vw,42px)}` (l. 196) |
| Document / proposition | `.of-hero h1{font:700 clamp(46px,7vw,84px)/.95}` (l. 540) ; `.of-sec > h2{font:700 clamp(28px,3.4vw,40px)/1}` (l. 568) |
| Valeur KPI | `.kpi .v{font:700 40px/1 var(--f-display)}` ; `.kpi .v small{font-size:16px}` (l. 116–118) |
| Eyebrow / lab / badge | `font:600 11px var(--f-mono);letter-spacing:.08–.1em;text-transform:uppercase` (l. 68, 155, 52) |
| Cellule de tableau | `th{font:600 11px var(--f-mono)…}` / `td{padding:9px 10px;font hérité}` (l. 121–122) |
| Gros nombre inline | `.big-n{font:700 20px var(--f-display)}` (l. 126) |

Deux utilitaires : `.num{font-variant-numeric:tabular-nums}` et `.mono{font-family:var(--f-mono)}` (l. 37–38).

### 1.4 Composants réutilisables

Chaque entrée donne : classe, ligne CSS, helper JS qui la produit (s'il existe), et le HTML minimal.

#### Grille d'application — `.app` / `.side` / `.main` / `.content` (l. 40–41, 74, 77)
```html
<div class="app">
  <aside class="side">…</aside>
  <div class="main"><div class="content" id="view"></div></div>
</div>
```
`.app{display:grid;grid-template-columns:var(--side) minmax(0,1fr)}` · `.content{padding:22px;display:flex;flex-direction:column;gap:18px;max-width:1500px}`.

#### Sidebar — `.logo` / `.navsec` / `.nav` / `.badge` / `.pin` / `.side .foot` (l. 42–66, 307–311)
```html
<aside class="side">
  <div class="logo"><span class="mk">ABM</span><div><b>Tour de contrôle</b><span>Comptes nommés · signaux CRM</span></div></div>
  <div class="navsec">Pilotage</div>
  <div class="nav">
    <button data-tab="cockpit"><svg viewBox="0 0 24 24">…</svg><span class="lbl">Cockpit</span><span class="badge red" id="bA"></span></button>
  </div>
  <div class="foot"><button id="openImport">Importer mes comptes</button></div>
</aside>
```
État actif : `button[aria-current="page"]`. `.badge.red` = fond `--red`. `.nav .dot` (pastille 8 px) est utilisé par les comptes épinglés.

#### Bandeau lime — `.banner` (l. 78)
```html
<div class="banner"><span><b>Plateforme de démonstration</b> · … · données fictives</span></div>
```
`background:var(--lime);color:var(--navy);font-size:13px;padding:7px 22px`.

#### En-tête de page collant — `.phead` / `.eyebrow` / `.pill-navy` / `.date` (l. 67–72, 76)
```html
<div class="phead">
  <div><div class="eyebrow" id="eyebrow">Pilotage</div><h1 id="ptitle">Cockpit du portefeuille</h1></div>
  <div class="pills"><span class="pill-navy">Semaine 38</span><span class="date">vendredi 18 septembre 2026</span></div>
</div>
```
`.eyebrow::before` dessine un trait rouge 14×3 px.

#### Carte — `.card` / `.card > header` / `.card .body` (l. 78–82)
```html
<div class="card">
  <header><div><h2>Titre</h2><p>Sous-titre</p></div><button class="btn small">Action</button></header>
  <div class="body">…</div>
</div>
```

#### Carte KPI — `.kpis` / `.kpi` / `.kpi.red` — helper `kpi(k, v, p, red)` **l. 1119**
```js
const kpi = (k, v, p, red) => `<div class="kpi${red?' red':''}"><div class="k">${k}</div><div class="v">${v}</div><p>${p}</p></div>`;
```
```html
<div class="kpis">
  <div class="kpi"><div class="k">Pipe ouvert</div><div class="v">2,4 M€</div><p>18 opportunités</p></div>
  <div class="kpi red"><div class="k">Comptes à attaquer</div><div class="v">17<small>/ 100</small></div><p>…</p></div>
</div>
```
`.kpis{grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px}` (l. 114). Fond marine ; `.kpi.red` passe en `--red`. Le `<small>` dans `.v` est le dénominateur.

#### Tableau — `table` / `th` / `td` / `td.r` / `tr.click` / `.tbox` / `.acc` / `.rank` (l. 119–132)
```html
<div class="tbox"><table style="min-width:1000px">
  <thead><tr><th>Compte</th><th class="r">Pts</th></tr></thead>
  <tbody><tr class="click" data-id="acme"><td class="acc"><b>Acme</b><span>Industrie · 2 300 pers.</span></td><td class="r num">12,4</td></tr></tbody>
  <tfoot><tr><td>Total</td><td class="r">…</td></tr></tfoot>
</table></div>
```
`.tbox{overflow-x:auto}` est **obligatoire** autour de tout tableau large. `th.r` / `td.r` = aligné à droite. En-tête triable : `.sortb` (l. 342) + `aria-sort`.

#### Pastille de quadrant — `.q` / `.q-A…D` — helper `qPill(q, full)` **l. 1114**
```html
<span class="q q-A" title="ICP fort · engagé">A · Attaquer</span>
```

#### Pastille de statut compte — `.stp` / `.st-jamais|perdu|ancien|encours|client` (l. 134–139)
```html
<span class="stp st-encours">Opp. ouverte</span>
```

#### Pastille d'étape funnel — `.fn` / `.fn-bofu|mofu|tofu` — helper `fnPill(st)` **l. 1115**
```html
<span class="fn fn-bofu">BOFU</span>
```

#### Puce d'état — `.state` + `.ok|.warn|.crit|.mute` (l. 140–142)
```html
<span class="state ok">BOFU atteint</span>
```
Pastille ronde 8 px via `::before{background:currentColor}`.

#### Delta — `.delta` / `.up` / `.down` — helper `deltaPill(d)` **l. 1116**
```html
<span class="delta up">+4</span>
```

#### Double jauge de scores — `.duo` — helper `duo(a)` **l. 1117**
```html
<div style="display:grid;gap:3px">
  <div class="duo"><span>ICP</span><div class="t"><i style="width:82%;background:var(--orange)"></i></div><b>82</b></div>
  <div class="duo"><span>ENG</span><div class="t"><i style="width:71%;background:var(--info)"></i></div><b>71</b></div>
</div>
```

#### Comité (pastilles de rôle) — `.comite` (l. 148–151)
```html
<div class="comite">
  <i title="Claire Morel — décideur" style="background:var(--r-dec)"></i>
  <i title="Julien Faure — champion" style="border:1.5px dashed var(--r-champ)"></i>
  <em>3 chauds</em>
</div>
```
Plein = `prov:'actif'` ; pointillé = `prov:'cible'`.

#### Chips / filtres — `.bar` / `.chip` / `.chip .n` (l. 154–156)
```html
<div class="bar"><button class="chip" data-f="A" aria-pressed="true">A · Attaquer <span class="n">17</span></button></div>
```

#### Onglets segmentés — `.seg` (l. 313–315)
```html
<div class="seg"><button data-cpt="dash" aria-pressed="true">Tableau de bord</button><button data-cpt="offre" aria-pressed="false">Proposition ↗</button></div>
```

#### Barre d'en-tête d'écran — `.lvhead` (l. 312)
Conteneur blanc bordé qui héberge `.seg`, `<select>`, `.agentchip`. Utilisé par cockpit (`cpTabs`, l. 1168), leviers (`leverHeader`, l. 1333), signaux (l. ~1823).

#### Boutons — `.btn` / `.primary` / `.red` / `.small` / `:disabled` (l. 95–99) ; lien texte `.linkb` (l. 384)
```html
<button class="btn primary">Copier le plan</button>
<button class="btn small">Fiche compte →</button>
<button class="linkb" data-acc="acme">Acme</button>
```

#### Interrupteur — `.switch` / `.switch.sm` (l. 328–331, 361–363)
```html
<button class="switch" role="switch" aria-checked="true" data-toggle="paid"><span></span></button>
```

#### Note / encart — `.note.info` / `.note.warn` (l. 85–88)
```html
<div class="note info"><b>Attaquer — ICP fort · engagé.</b> ABM 1:1 — BDR nommé…</div>
```

#### Légende — `.legend` — helper `legendOf(items)` **l. 1120**
```html
<div class="legend"><span><i style="background:var(--c-pub)"></i>Publicité</span></div>
```

#### Barres horizontales — `.hb` — helper `hbars(rows, color)` **l. 1138**
Chaque `row` : `{label, value, max, text, color?, title?}`.
```html
<div class="hb"><div class="row"><b>Content</b><div class="t"><i style="width:72%;background:var(--navy)"></i></div><span class="v">36 <small>/ 50</small></span></div></div>
```

#### Grilles — `.g2` (2 colonnes égales), `.g3` (1,3fr + 1fr), `.g3c` (3 colonnes), `.g2.ov` (gap 32), `.col` (colonne flex gap 18) — l. 100–101, 345–346, 200

#### Autres blocs notables
`.hero` (l. 102–111, bloc marine du plan de mission) · `.drawer` (tiroir d'import, l. 158–162) · `.surge` / `.sig` (cartes de signaux, l. 240–249) · `.creas` / `.crea` (vignettes de créas, l. 317–324) · `.libgrid` / `.libitem` / `.cover` / `.toolv` / `.post` / `.browser` (bibliothèque Content, l. 385–430) · `.lp-*` (landing pages simulées, l. 447–472) · `.gantt` / `.gt-row` / `.gt-c.setup|launch|run` (l. 479–488) · `.raci` / `.rx-R|A|C|I` (l. 517–523) · `.of-*` (document de proposition, l. 536–605) · `.modal` / `.modal-in` / `.mx` (l. 431–436) · `.toast` (l. 623).

### 1.5 Réactif

`@media` : 1300 px (`.g2.ov`) · 1250 px (`.accgrid`, `.eng`, `.g3` → 1 colonne) · 1100 px (`.g3c`, `.aglayout`, `.task`) · 1000 px (`.g2`, `.twoscores`, `.of-*`) · 900 px (sidebar horizontale, `.sig` empilé, `.lv` empilé) · 760 px (bibliothèque, LP) · `@media print` deux fois (l. 524 et 606) : masque sidebar, bandeau, `.phead`, `.doctop`, grilles de prix.

---

## 2. STRUCTURE DE NAVIGATION

### 2.1 Entrées de la sidebar, dans l'ordre du DOM (l. 665–690)

| # | Section (`.navsec`) | Libellé | `data-tab` | Hash | Badge (id) | Rendu par |
|---|---|---|---|---|---|---|
| 1 | Pilotage | Cockpit | `cockpit` | `#cockpit` | `#bA` → « N A » (`.badge.red`) | `renderCockpit` l. 1198 |
| 2 | Pilotage | Signaux captés | `signaux` | `#signaux` | `#bS` → nb signaux forts ≤ 7 j | `renderSignals` l. 1807 |
| 3 | Pilotage | Agents | `agents` | `#agents` | `#bG` → « n/7 » | `renderAgents` l. 1996 |
| — | ★ Mes comptes en cours | *liste dynamique* `#pinNav` | `data-pinopen=<id>` | `#compte/<id>` | badge = quadrant | `renderPins` l. 1798 |
| 4 | Comptes | Fiche compte | `compte` | `#compte/<id>` | libellé remplacé par le nom du compte (`#bC`) | `renderAccount` l. 1684 |
| 5 | Plan d'activation | Content | `content` | `#content` | `#bl-content` = nb comptes dont `plan.has('content')` | `renderLever('content')` l. 1371 |
| 6 | Plan d'activation | Paid | `paid` | `#paid` | `#bl-paid` | idem |
| 7 | Plan d'activation | Social | `social` | `#social` | `#bl-social` | idem |
| 8 | Plan d'activation | Outbound | `outbound` | `#outbound` | `#bl-outbound` | idem |
| 9 | Plan d'activation | SDR | `sdr` | `#sdr` | `#bl-sdr` | idem |
| 10 | Plan d'activation | Sales | `sales` | `#sales` | `#bl-sales` | idem |
| 11 | Moteur | Scoring ICP & engagement | `moteur` | `#moteur` | `#bM` → `défaut` \| `réglé` | `renderEngine` l. 2400 |

Les 6 entrées « Plan d'activation » sont **générées** ligne 1074 à partir de l'objet `LEVERS` (l. 778–785) ; l'icône SVG vit dans `LEVERS[k].ico`. Le `<div id="leverNav">` est vide dans le HTML statique.

Le pied de sidebar contient `#openImport` (l. 686) : `ui.drawer = true; go('cockpit')` (l. 1109).

### 2.2 Routes hors sidebar

- `proposition` — hash `#proposition`, titre « Mission / Proposition », rendu par `renderMission` (l. 1170). **C'est la route par défaut au chargement** (l. 2482). Aucun bouton de sidebar ne la porte : on y entre par l'onglet interne du cockpit (`data-cpt="offre"`), par `data-tabgo` dans le document, ou par le hash.
- Alias `offre` et `propal` (l. 1095) : tous deux normalisés en `proposition`. `propal` demandé *depuis* `proposition` déclenche en plus un `scrollIntoView` sur `#of-10` (le plan de mission), l. 1105.
- `document.body.classList.toggle('docmode', tab === 'proposition')` (l. 1096) : le mode document masque sidebar, bandeau et `.phead`, et affiche la barre `.doctop` (l. 608–622).

### 2.3 La fonction de routage — `go(tab, accId)` **l. 1093–1106**

```js
function go(tab, accId){
  let toPlan = false;
  if (tab === 'cockpit') ui.cpTab = 'dash';
  if (tab === 'offre' || tab === 'propal') { toPlan = tab === 'propal' && ui.tab === 'proposition'; tab = 'proposition'; }
  document.body.classList.toggle('docmode', tab === 'proposition');
  ui.tab = tab; if (accId) { ui.acc = accId; ui.story = -1; ui.sel = null; }
  if (tab === 'compte' && !accounts.find(a => a.id === ui.acc)) ui.acc = sorted()[0].id;
  document.querySelectorAll('.nav button').forEach(b => b.setAttribute('aria-current', b.dataset.tab === tab ? 'page' : 'false'));
  document.getElementById('eyebrow').textContent = TITLE[tab][0];
  document.getElementById('ptitle').textContent = TITLE[tab][1];
  const h = tab === 'compte' ? '#compte/' + ui.acc : '#' + tab;
  if (location.hash !== h) history.replaceState(null, '', h);
  render(); if (toPlan) { … } else window.scrollTo(0, 0);
}
```
`TITLE` (l. 1071–1072) donne `[eyebrow, titre H1]` pour chacune des 12 routes. `history.replaceState` seulement (pas de `pushState`) : **le bouton Précédent du navigateur ne navigue pas dans l'app**.

### 2.4 Le dispatcheur — `render()` **l. 1107**

```js
function render(){
  badges();
  if (LEVERS[ui.tab]) return renderLever(ui.tab);
  ({ proposition: renderMission, cockpit: renderCockpit, compte: renderAccount,
     signaux: renderSignals, moteur: renderEngine, agents: renderAgents })[ui.tab]();
}
```
Tout part de `ui.tab`. Les 6 leviers partagent **une seule** fonction `renderLever(k)` (l. 1371) qui appelle `leverHeader(k, st)` + (`leverAccount(k, a)` si un compte est sélectionné, sinon `leverCompany(k)`).

Tous les rendus écrivent dans `V().innerHTML` où `V = () => document.getElementById('view')` (l. 1112). Le DOM est **entièrement reconstruit** à chaque rendu ; les handlers sont rebranchés juste après par des `querySelectorAll(...).onclick = …`.

### 2.5 Amorçage (l. 2481–2482)

```js
const h = location.hash.slice(1);
if (h.startsWith('compte/')) go('compte', h.slice(7));
else go(TITLE[h] || h === 'offre' || h === 'propal' ? h : 'proposition');
```

### 2.6 Onglets **internes** (ne pas confondre avec des routes)

| Écran | Attribut | Valeurs | État | Ligne |
|---|---|---|---|---|
| Cockpit | `data-cpt` | `dash` (reste) / `offre` (**route** vers `proposition`) | `ui.cpTab` | 1168–1169 |
| Cockpit | `data-cp` | `7` / `30` / `90` (fenêtre en jours) | `ui.cp` (défaut 30) | 1247 |
| Cockpit | `data-f` | `all`, `mine`, `A`, `B`, `C`, `D`, `fy`, `bofu`, + statuts | `ui.filter` | 1246 |
| Levier | `data-view` | `co` (vue entreprise) / `acc` (vue compte) | `lvState(k).acc` | 1333 |
| Levier | `data-scope` | `plan` / `mine` / `all` | `lvState(k).scope` | 1349 |
| Levier | `data-qf` / `data-sf` / `#ownerSel` | quadrant / statut du levier / SDR-AE | `lvState(k).q/.st/.owner` | 1349–1354 |
| Signaux | `data-period` | `jour` / `semaine` / `mois` | `ui.sg.period` | 1805, 1823 |
| Signaux | `data-g` | `all, fort, bofu, mofu, tofu, pub, site, mail, ext` | `ui.sg.f` | 1821 |
| Agents | `data-agsel` | une des 7 clés de `AGENTS` | `ui.agentSel` (défaut `paid`) | 2011 |
| Agents | `data-agtab` | `tasks` / `scope` / `queue` / `log` | `ui.agentTab` (défaut `tasks`) | 2016 |
| Proposition | `data-ofgo` | `1…9` → `scrollIntoView('#of-N')` | — | 2393 |
| Proposition | `data-ppw` | `all` / `B` / `C` / `BC` | `ui.pp.who` | 2259 |

---

## 3. INVENTAIRE ÉCRAN PAR ÉCRAN

### 3.1 Cockpit — `renderCockpit()` **l. 1198–1284**

Blocs dans l'ordre :

1. **`cpTabs()`** (l. 1168) — seg « Tableau de bord » / « Proposition et plan de mission ↗ ».
2. **Tiroir d'import** (conditionnel `ui.drawer`) — carte « Importer mes comptes », `<textarea id="import-text">` (placeholder `Sanofi France / decathlon.com / Groupe SEB`), compteur `#importCount`, 3 boutons : `#doReplace` (Remplacer le portefeuille), `#doAdd` (Ajouter au portefeuille), `#doReset` (Revenir à l'exemple (100)). Parsing l. 1275 : découpage sur `/[\n;,\t]+/`, trim, longueur > 1, dédoublonné, **plafonné à 300**.
3. **Carte « Vue d'ensemble »** — seg `7 j / 30 j / 90 j`. 6 KPI, libellés exacts :
   - `Pipe ouvert` — `fmtE(pipe)` · sous-texte « N opportunités · X créés sur la période »
   - `RDV générés` — nb d'événements RDV dans la fenêtre
   - `Meetings tenus`
   - `Signaux captés` — « N forts · ± vs période précédente »
   - `Opportunités créées` — « ± · X % des RDV »
   - `Comptes à attaquer` — `N/total`, sous-texte « N comptes avec un budget en préparation », **`red: true`**
4. **`.g2.ov`** — 2 graphiques :
   - « RDV générés · par semaine » — `colChart` **colonnes empilées**, 12 semaines, 4 séries `sdr / out / in / paid` (couleurs `--c1…--c4`), légende issue de `RDV_SRC` (l. 1187).
   - « Pipe créé · par mois » — `colChart` colonnes simples, 6 derniers mois, série `v` en `--navy`.
5. **« Signaux captés · par semaine »** — `colChart` empilé 12 semaines, 4 séries `pub / site / mail / ext`, légende `canalLegend()`.
6. **`.g3`** — colonne large : carte « Matrice ICP × engagement » = `scatter(accounts)` (l. 1139), nuage de points cliquables (`circle.dot[data-acc]`) + `.quadlegend` des 4 quadrants. Colonne étroite : « Couverture du plan » (`hbars`, rouge si < 70 %) et « RDV par source » (`hbars`, 4 sources).
7. **Carte « Tous les comptes »** (`#allAcc`) :
   - barre de chips : `Tous`, `★ Mes comptes`, `A · Attaquer`, `B · Réveiller`, `C · Qualifier`, `D · Veille`, `Budget en préparation`, `BOFU 30 j`
   - `<input class="search" id="q">` + `<select id="sort">` : `Priorité (ICP + engagement)` / `Score ICP` / `Engagement` / `Accélération 14 j` / `Nom`
   - **tableau, colonnes exactes** : `★` · `#` · `Compte` · `Quadrant` · `Scores` · `Exercice fiscal` · `Funnel 30 j` · `Statut` · `Comité` (`min-width:1000px`)

Interactions : clic ligne ou `Enter` → `go('compte', id)` ; clic point du scatter → idem ; `☆` → `togglePin` ; changements de filtre/tri/recherche → re-render **en conservant `window.scrollY`** et en restaurant le curseur du champ recherche (l. 1248).

### 3.2 Signaux captés — `renderSignals()` **l. 1807–1855**

1. **`.lvhead`** : seg `Jour / Semaine / Mois` · libellé de période · `<select id="sgq">` quadrant · chip `★ Mes comptes` (`#sgmine`).
2. **Barre de chips** `data-g` : `Tous`, `Signaux forts`, `BOFU`, `MOFU`, `TOFU`, `Publicité`, `Site & contenu`, `Email`, `Externe`.
3. **3 KPI** : `Signaux captés` (± vs période précédente) · `Signaux forts` (% du volume, `red:true`) · `Comptes` (« sur N · M contacts »).
4. **`.g2`** : « Par jour et par canal » (`colChart` empilé, une colonne par jour ; en période `jour` c'est `hbars` « Par canal ») et « Par type de signal » (`hbars`, ordre `SIG_ORDER` puis tri décroissant).
5. **« Comptes les plus actifs »** — tableau, colonnes : *(vide : épingle)* · `Compte` · `Quadrant` · `Signaux` · `Forts` · `BOFU` · `Points` · `Scores`. Top 10 par points.
6. **« Tous les signaux »** (`#sgTable`) — recherche `#sgtext` ; tableau `min-width:1100px`, colonnes **triables** (`data-sort`) : `Date`(`d`) · `Compte`(`acc`) · `Quadrant`(`q`) · `Contact`(`who`) · `Signal`(`type`) · `Canal`(`canal`) · `Étape`(`st`) · `Détail` (non triable, affiche `det` + la phrase `WHY[t]`) · `Pts`(`v`, aligné droite). Pagination « Afficher 100 de plus » (`#sgmore`, `ui.sg.limit += 100`).

Rien n'est persisté ; tout l'état vit dans `ui.sg` (l. 1068).

### 3.3 Agents — `renderAgents()` **l. 1996–2052**

1. **3 KPI** : `Agents actifs` (`n/7`, « X tâches en marche sur Y ») · `Actions exécutées · 7 j` · `À valider` (`red` si > 0).
2. **`.aglayout`** = colonne `.aglist` (7 `.agcard`, un par agent, avec `.switch.sm` `data-toggle`) + carte de détail.
3. **Carte de détail** : eyebrow (`Levier X` ou `Maintien du CRM`), titre `AGENTS[k].l`, description `AGENTS[k].does`, `.switch` principal, bouton « Ouvrir le levier » (`data-tabgo`).
4. **Seg d'onglets** : `Tâches · N` / `Périmètre & garde-fous` / `File de validation · N` / `Journal · N` + 3 boutons de masse `data-all` = `auto` / `valid` / `off`.
5. Onglet **Tâches** : une `.task` par entrée de `AGENT_TASKS[k]` → titre, description, `.trig` (déclencheur), `.params` (inputs number ou selects, `data-tp="<taskId>.<paramKey>"`), `.tmode` seg `Auto / À valider / Off` (`data-tm="<taskId>:<mode>"`) + compteur d'actions 7 j.
6. Onglet **Périmètre** : chips quadrants `data-scope-q`, cases `data-cf="mine"` et `data-cf="noOpp"`, table de garde-fous (`data-cfs`: `freq`, `hour`, `days`, `notif` ; `data-cfn`: `maxDay`), compteur d'actions écartées, avertissement de plafond.
7. Onglet **File de validation** : tableau des items `status === 'attente'` avec boutons `Valider` / `Rejeter` (`data-dec="<itemId>:ok|ko"`) + `data-decall`.
8. Onglet **Journal** : filtre `#agTaskF` par tâche, même tableau sans boutons (sauf items en attente).
9. Pied : phrase « Prochain passage : … · jours … · plafond N actions / jour · <notif> ».

**Persistance** : clé `abm-tdc-agents` ← `ui.agents` = `{ on, mode, valid, cfg, decided }` (l. 1069). `cfg[k]` est construit/complété à la volée par `agentCfg(k)` (l. 1909–1918). `decided[itemId] = 'ok'|'ko'`.

### 3.4 Fiche compte — `renderAccount()` **l. 1684–1792**

1. **`.acchead`** : eyebrow « Nᵉ sur M · domaine », H2 nom, meta « secteur · N personnes · exercice … », tags (`qPill` complet, `.stp` statut, `ICP n`, `Engagement n`), barre : `pinBtn`, `← Cockpit`, `‹ Précédent`, `Suivant ›` (navigation dans `sorted()`).
2. **`.note info`** : « <Quadrant> — <sous-titre>. <play> » depuis `QUADS`.
3. **`.accgrid`** (1fr + 360 px) :
   - **Colonne gauche** :
     - **Carte du comité** (`.mapcard`) : SVG `#graph` `viewBox="0 0 900 560"` produit par `layout(a)` (l. 1603) — graphe à ressorts, 420 itérations. Nœuds : `acc` (cercle lime, lettre du quadrant), `ent` (carré, groupe/filiale), `loss` (losange rouge), `open` (losange info), contacts (cercle dont le **rayon = `7 + min(9, √heat × 2,2)`**, anneau rouge si `heat ≥ cfg.eng.hotMin`, point marine au centre pour « la porte »). Outils : `▶ Raconter l'histoire` (`#story`, 5 étapes) et `Tout afficher` (`#clear`). Encart `.fiche` sur sélection d'un contact. `.maplegend` (9 entrées).
     - **« Les signaux, contact par contact »** : une `.trow` par contact triée par `heat` décroissant, frise SVG `.track` `viewBox="0 0 360 22"` sur 350 jours, hauteur de barre = `6 + min(sigW, 16)`, couleur = canal ; dernière ligne « Signaux du compte » pour les signaux sans `who`. Axe = les 12 libellés de `MONTHS`.
   - **Colonne droite** :
     - Carte « Score ICP » → `icpHTML(a)` (l. 1677) : gros chiffre, `deltaPill` vs défaut, `<ul>` des lignes de `a.I.lines`.
     - Carte « Score d'engagement » → `engHTML(a)` (l. 1679) : gros chiffre, 3 piliers (Intention / Comité / Timing) avec barre + contribution `+pts`, sous-listes de `a.E.lines`, `mixHTML(E)` (barre de répartition BOFU/MOFU/TOFU/Externe) sous Intention, malus. Bouton `#toEngine` → `ui.test = a.id; go('moteur')`.
     - Carte « Plan d'attaque » → `plan(a)` (l. 1637) : **La porte** (nom, titre, provenance) · **Le chemin** (`<ol class="path">`, étapes `la porte` → `relais` → `décision` → `budget, en dernier`) · **L'accroche** (`.hook`) · **Signal le plus fort (120 j)**. Boutons `#copy` (copie texte via `navigator.clipboard`) et `#toSig` (pré-remplit `ui.sg.text = a.name`, `period = 'mois'` et va sur Signaux).

Interactions : clic sur un nœud `g.node[data-n^="c"]` ou un `[data-c]` → `pickC(id)` (sélection/désélection). Aucune persistance sauf `abm-tdc-pins` via l'épingle.

### 3.5 Les 6 écrans de levier — `renderLever(k)` **l. 1371–1382**

Structure commune : `leverHeader(k, st)` (l. 1333) = seg `Vue entreprise` / `Vue compte`, `<select id="lvAcc">` avec 3 `optgroup` (`Mes comptes en cours`, `Dans le plan <Levier>`, `Hors plan`), et un `.agentchip` cliquable qui mène à l'écran Agents.

Puis **soit** `leverCompany(k)` (l. 1479, vue portefeuille) **soit** `accHead(k,a)` + `leverAccount(k,a)` (l. 1384 / 1556, vue compte).

`leverCompany(k)` se termine toujours par `suiviHTML(k)` (l. 1341) : carte « Suivi compte par compte » avec périmètre (`Dans le plan` / `★ Mes comptes` / `Tout le portefeuille`), quadrant, statut spécifique au levier (table `FILTERS`, l. 1325–1332), sélecteur SDR/AE pour `sdr`/`sales`, recherche, puis un **tableau aux colonnes fixes** : *(épingle)* · `Compte` · `Quadrant` · `Scores` · `Statut <Levier>` · `Activité` · `Détail` · `Prochaine action` (`min-width:1080px`). Chaque ligne vient de `leverRow(k, a)` (l. 1307).

#### Content (`k='content'`)
- **Entreprise** — KPI : `Téléchargements · 30 j` · `Budget LinkedIn du mois` · `Coût par téléchargement` · `A/B sans BOFU` (red). Puis `contentLibrary(AS)` (l. 1459) : 4 cartes — **Livres blancs** (2 couvertures composées, stats `Téléchargements / Comptes / dont A / Coût par téléch.`), **Outils** (2, stats `Utilisations / Comptes / dont A / Coût par util.`), **Créatives** (3 posts LinkedIn simulés, stats `Impressions / CTR / Dépense / Comptes`), **Landing pages** (2 maquettes navigateur, stats `Visites · 30 j / Conversions / Taux / Contenu`). Clic → `openModal` (l. 1444) : couverture + sommaire, calculateur ROI interactif (`roiHTML`/`bindRoi`, l. 1421–1422), template plan de comptes (`tplHTML`, l. 1440, bouton « Copier le tableau »), ou landing page complète (`lpHTML`, l. 1423).
- **Compte** — KPI : `Contenus consommés · 90 j` · `Lecteurs` · `Étape atteinte` · `Impressions sponsorisées`. Tableaux : « Ce que le compte a lu » (`Date / Contact / Contenu / Étape / Signal / Pts`) et « Prochain contenu à pousser » (5 recommandations, boutons `data-toast`).

#### Paid (`k='paid'`)
- **Entreprise** — KPI : `Budget du mois` · `Impressions sur comptes` · `Comptes du plan touchés` · `Créas à couper` (red, seuil CTR 0,35 %). Tableau « Campagnes et budget » : `Campagne / Budget par mois / Dépensé / Consommé / Comptes / Impr. / CTR / CPC`. Grille « Les créas qui tournent » (`creaCard`, l. 1551).
- **Compte** — KPI : `Impressions · 30 j` · `Clics` · `Dépense · 30 j` · `Contacts qui ont cliqué`. Avertissement si 0 impression. Grille des créas servies + tableau « Qui a cliqué ».

#### Social (`k='social'`)
- **Entreprise** — KPI : `Interactions des comptes · 30 j` · `Comptes engagés` · `Décideurs engagés` · `Plan silencieux` (red). `colChart` « Interactions par semaine » (3 séries : réactions/commentaires/partages) + tableau « Les posts qui touchent les comptes » (`Post / Auteur / Comptes / dont A / Inter.`).
- **Compte** — KPI : `Interactions · 30 j` · `Contacts engagés` · `Décideurs engagés` · `Dernière interaction`. Tableau `Date / Contact / Post / Type`.

#### Outbound (`k='outbound'`)
- **Entreprise** — KPI : `Emails envoyés · 30 j` · `Taux d'ouverture` · `Taux de réponse` · `Plan hors séquence` (red). Tableaux : « Performance par type de message » (`Message / Canal / Envoyés / Ouverts* / Clics / Réponses`), « Séquences » (`Séquence / Comptes / Contacts / Ouv. / Rép. / RDV / Rebonds`), « Dernières réponses » (8 max).
- **Compte** — KPI : `Contacts en séquence` · `Messages envoyés` · `Taux d'ouverture` · `Réponses`. Tableaux « Messages envoyés » (`Date / Contact / Message / Canal / Ouvert* / Clic / Réponse`) et « Comité hors séquence ».

#### SDR (`k='sdr'`)
- **Entreprise** — KPI : `Appels · 30 j` · `Taux de décroché` · `RDV posés · 30 j` · `BOFU < 7 j non appelés` (red). Tableau « À appeler aujourd'hui » (8 lignes : `Compte / Qui appeler / Pourquoi maintenant / SDR / Dernier appel`), `hbars` « Taux de décroché par créneau » (5 tranches de 2 h de 8 h à 18 h), tableau « Par SDR » (`SDR / Comptes / Appels / Décroché / Conv. / RDV / A non appelés`), `hbars` « Issue des appels » (6 issues de `CALL_OUT`).
- **Compte** — KPI : `Appels · 30 j` · `Taux de décroché` · `Conversations` · `RDV posés`. Tableaux « Journal d'appels » (`Date / Heure / Contact / Issue / Durée / SDR`) et « Jamais appelés ».

#### Sales (`k='sales'`)
- **Entreprise** — 5 KPI : `Meetings tenus · 30 j` · `Meetings à venir · 14 j` · `No-show · 90 j` · `Pipe ouvert` · `A sans opportunité` (red). `colChart` « Meetings tenus par semaine » (4 séries R1/R2/R3-comité/revue), « Prochains meetings », « Par AE » (`AE / Tenus / À venir / Opps / Pipe`), `hbars` « Pipe par étape » (les 4 `OPP_STAGES`).
- **Compte** — KPI : `Meetings tenus` · `À venir` · `Opportunité`/`Signé` · `Décideurs rencontrés`. Tableaux « Meetings » (`Date / Type / Participants / AE / Statut`) et « Décideurs jamais rencontrés ».

Persistance des leviers : **aucune**. `ui.lv[k]` (l. 1324) est volatile.

### 3.6 Scoring ICP & engagement — `renderEngine()` **l. 2400–2460**

1. `.note info` pédagogique + `.formula` (bloc marine lisant la formule en pseudo-maths).
2. `.eng` = colonne de réglages + colonne collante `#engRight`.
3. **Carte « Score ICP · Qui ils sont »** : chips des 10 secteurs (`data-sector`) ; table `icp.sectorIn`, `icp.sectorOut`, 4 tailles `icp.size.s|m|l|xl` ; table `icp.hist.ancien`, `icp.hist.client`, `icp.multi`, `icp.lossMalus` ; bloc « Règle · exercice fiscal » avec 2 sliders (`icp.fy.prepFrom`, `icp.fy.prepTo`) et 2 numériques (`icp.fy.prep`, `icp.fy.start`).
4. **Carte « Score d'engagement · Ce qu'ils font »** : 4 boutons de préréglage (`PRESETS`, l. 898) ; 3 sliders de poids (`eng.w.intent|comite|timing`, 0–80) ; sliders `eng.half` (7–120), `eng.sat` (10–120), `eng.hotMin` (1–20) ; table des 12 poids de signaux (`eng.sig.<type>`, 0–20, avec mini-barre `#bar-<type>`) ; 3 sliders de multiplicateur funnel (`eng.stage.bofu|mofu|tofu`, 0–3, pas 0,05) ; table `eng.comite.dec|hot2|champ|cover`, `eng.timing.job|event`, `eng.noContact`.
5. **Carte « Matrice et plan d'activation »** : sliders `matrix.icp` et `matrix.eng` (20–90) + table des 4 quadrants avec leurs leviers.
6. **`engineRight()`** (l. 2462) : carte « Effet sur le portefeuille » (scatter h=340, table des 4 comptes par quadrant avec delta vs défaut, bouton `#reset`), carte « Ce qui change de quadrant » (8 comptes, `q0 → q`), carte « Tester sur un compte » (`#testSel` + `icpHTML` + `engHTML` + `#openTest`).

Chaque `oninput` appelle `setP(path, v)` puis `commit()` (l. 2461) → écrit `abm-tdc-cfg2` (ou le supprime si l'état est celui par défaut), relance `rescore()`, `badges()`, `engineRight()`.

### 3.7 Proposition + Plan de mission — `renderMission()` **l. 1170–1175**

Une seule route (`proposition`) qui monte deux sous-rendus dans `#view` :
- `renderOffre(#mOffre)` (l. 2291–2395) — le document commercial, 9 sections `#of-1` … `#of-9`.
- `renderPropal(#mPlan)` (l. 2214–2264) — la section 10 « Le plan de mission ».

**Contenu éditorial — résumé en 5 lignes, non réutilisable :** proposition commerciale Bulldozer pour un programme ABM de 16 semaines / 8 sprints de 2 semaines ; sprint 1 = mise en place (connexions, liste de comptes, scores, comités, rôles), puis un levier activé par sprint (Content, Paid, Social, Outbound, SDR, Sales), sprint 8 = bilan et passage en run. Les données structurées associées sont `PHASES` (l. 2056–2170, 8 phases × tâches `[id, titre, description, qui, rôle, [jourDébut, jourFin], livrable, outil]`), `ACCESS` (l. 2171), `RACI_ROLES`/`RACI` (l. 2183–2189), `TEAM` (l. 2190), `RITUALS` (l. 2197), `KPI_SPRINT` (l. 2202), `OFFRE_DEF` (l. 2275, textes éditables), `PRICE_DEF` (l. 2282, grille `{socle:4200, pilot:1800, mkt:1200, sales:1200, os:900}`), `LEVER_DOC` (l. 2283). Interactions : champs `contenteditable` `[data-ed]`, inputs de prix `[data-price]`, nom du client `#ppClient`, date de démarrage `#ppStart`, cases à cocher de tâches `[data-ppd]`, accordéons de sprint `[data-ppo]`, impression `#ppPrint`. Tout est persisté dans **`abm-tdc-pp`** = `{ client, start, done, open, edits, prices }`.

Cette section lit tout de même le portefeuille pour 5 chiffres (section 02 « Le constat », l. 2320–2327) : nb de comptes A, % jamais chassés, signaux sur 30 j, membres de comité absents du CRM, pipe ouvert.

### 3.8 Récapitulatif localStorage

| Clé | Écrite par | Contenu |
|---|---|---|
| `abm-tdc-cfg2` | `commit()` l. 2461 | objet `cfg` complet (supprimé si identique à `DEFAULT_CFG`) |
| `abm-tdc-names` | import cockpit l. 1279 | `string[]` des noms/domaines de comptes |
| `abm-tdc-draft` | saisie du tiroir l. 1276 | contenu brut du textarea |
| `abm-tdc-pins` | `togglePin()` l. 1796 | `string[]` d'ids de comptes |
| `abm-tdc-agents` | `save()` l. 2009 | `ui.agents` = `{on, mode, valid, cfg, decided}` |
| `abm-tdc-pp` | `save()` l. 2258 / 2389 | `{client, start, done, open, edits, prices}` |

---

## 4. MOTEUR DE DONNÉES SIMULÉES

> C'est la section à respecter à la lettre pour brancher des données réelles.

### 4.0 Socle pseudo-aléatoire

| Fonction | Ligne | Rôle |
|---|---|---|
| `hash(s)` | 708 | FNV-1a 32 bits sur une chaîne → entier non signé. Sert de graine. |
| `rng(seed)` | 709 | xorshift32, renvoie une closure `() => [0,1)`. **Déterministe** : même nom de compte ⇒ même compte. |
| `pick(r, a)` | 710 | `a[floor(r()*a.length)]` |
| `shuffle(arr, r)` | 843 | Fisher-Yates avec le rng fourni |

Graines utilisées : `seed = hash(name.toLowerCase())` (compte) ; `seed ^ 0xA5A5A5` (`r2`, activité des leviers) ; `seed ^ 0x515151` (`enrich`) ; `seed ^ 0x7777` (`paidOf`) ; `seed ^ 0x9e37` (`layout`) ; `hash(x.id)` (`assetStats`) ; `hash(l.id)` (`lpStat`) ; `hash(k + id)` (`taskItems`) ; `rng(20260918)` (`sampleNames`).

Repère temporel : **`TODAY = new Date(2026, 8, 18)`** (18 septembre 2026), `WEEK_NOW = 38`, `DAY = 864e5`, `MTD = 18/30` (l. 705, 833).
**Toutes les dates du modèle sont des entiers `d` = nombre de jours écoulés depuis le signal.** `d = 0` → aujourd'hui ; `d = 30` → il y a 30 jours ; **`d < 0` → dans le futur** (uniquement pour les meetings). Conversion : `dateOf(d) = new Date(TODAY - d*DAY)` (l. 717).

### 4.1 `sampleNames()` — **l. 914** — `() => string[]`

Génère **exactement 100** noms uniques avec `rng(20260918)` : `pick(FORMS).replace('{}', pick(P1) + pick(P2))`.
`P1` = 25 préfixes (l. 911), `P2` = 12 suffixes (l. 912), `FORMS` = 10 gabarits `['{}','Groupe {}','{} Industries','{} Santé','{} Énergie','{} Logistique','{}','{} Solutions','{} Finance','{}']`.
Premiers noms produits (vérifiés) : `Terrarys Énergie`, `Groupe Nexatis`, `Lumacom Santé`, `Ionaane Santé`, `Groupe Vectotel`.

### 4.2 `buildAccount(raw)` — **l. 917–988** — `(raw: string) => Account`

Entrée : un nom **ou** un domaine (`/^[\w-]+(\.[\w-]+)+$/` → le nom est déduit du premier label, capitalisé).

Dérivations :
- `domain` : si le nom n'est pas un domaine, `slug(nom sans "Groupe ")` sans tirets + `.fr` si le nom contient `santé|énergie|finance`, sinon `.com`.
- `sector` : forcé par le nom (`santé` → `Santé`, `énergie` → `Énergie`, `logistique` → `Transport & logistique`, `finance` → `Banque & assurance`), sinon tirage dans `SECTORS`.
- `size` : tirage dans `[260, 420, 680, 950, 1400, 2300, 3800, 6200, 11000, 24000]`.
- `status` : `x<.42 → 'jamais'`, `<.60 → 'perdu'`, `<.72 → 'ancien'`, `<.88 → 'encours'`, sinon `'client'`.
- `heatK = r()^1.6` ∈ [0,1] — **variable de chaleur maîtresse**, pilote le nombre de signaux, la récence, le budget paid, l'activité sociale et le nombre d'appels.

#### Contrat `Account`

```ts
{
  id: string,            // slug(name) — clé primaire, unicité imposée à la construction (l. 1059)
  name: string,
  domain: string,
  sector: string,        // une des 10 valeurs de SECTORS (l. 727)
  size: number,          // effectif, entier
  status: 'jamais'|'perdu'|'ancien'|'encours'|'client',
  seed: number,          // uint32 — graine de tous les sous-générateurs
  fyStart: number,       // 0..11, mois de début d'exercice fiscal (tirage dans FY_STARTS = [0,0,0,3,6,9])
  n30: number,           // nb de signaux avec d <= 30 (pré-calculé, jamais relu ailleurs)
  contacts: Contact[],
  signals: Signal[],     // TRIÉ par d croissant (le plus récent d'abord)
  monthly: Monthly[12],  // 12 mois glissants, index 0 = il y a 11 mois
  hist: Hist,
  entities: Entity[],
  lv: { paid: Paid, social: SocialEvent[], outbound: Outbound, sdr: Sdr, sales: Sales }
}
```
Champs **ajoutés après coup** par `rescore()` (l. 1047) et `rebuild()` (l. 1057) — voir §5.

#### Contrat `Contact` (6 à 14 par compte)

```ts
{
  id: 'c0' | 'c1' | …,      // index séquentiel, unique dans le compte
  fn: string,               // prénom, tiré de FIRST (40 valeurs, l. 729)
  ln: string,               // nom, tiré de LAST (50 valeurs, l. 730) — UNIQUE dans le compte
  name: string,             // fn + ' ' + ln
  role: 'dec' | 'champ' | 'ope',
  prov: 'actif' | 'cible' | 'hors',
  title: string,            // tiré de TITLES[role] (l. 731-735)
  sig: Signal[],            // références vers les objets de account.signals (même identité)
  heat: number              // 0 à l'init ; renseigné par rescore() = Σ sigVal des signaux du contact
}
```
Règle de rôle (l. 923) : `i<2 → 'dec'` ; `i<5 → 70 % 'champ'` sinon `'ope'` ; au-delà → 75 % `'ope'` sinon `'champ'`.
Règle de provenance (l. 925) : `p<.50 → 'actif'`, `<.82 → 'cible'`, sinon `'hors'`.
Le contact `c1` a 55 % de chance d'avoir un titre budgétaire (`DAF` ou `Responsable achats`) — testé par `BUDGET(t) = /DAF|achats/.test(t)` (l. 736).

Sémantique de `prov` (`PROV_LABEL`, l. 738) : `actif` = contact actif au CRM · `cible` = cible identifiée, hors CRM · `hors` = au CRM, hors circuit. **`hors` est exclu de tout comptage de comité, de toute séquence et de tout appel.**

#### Contrat `Signal`

```ts
{
  t: 'ad'|'lgf'|'form'|'page'|'pricing'|'dl'|'webinar'|'open'|'click'|'job'|'hiring'|'news',
  d: number,                       // jours écoulés, 0..339
  who: string | null,              // id de contact, ou null pour un signal « compte »
  det: string,                     // libellé du détail (contenu, page, offre…)
  st?: 'bofu'|'mofu'|'tofu',       // ABSENT pour job / hiring / news
  n?: number                       // UNIQUEMENT pour t:'hiring' — nb d'offres ouvertes (3..42)
}
```
Nombre : `nS = round(4 + heatK*70)` signaux « contact ». Type tiré dans `CONTACT_SIGS` (l. 756 — liste pondérée par répétition : `ad×3, lgf, form, page×3, pricing, dl, webinar, open×3, click×2`). Récence : `d = min(339, floor(-ln(1-r()) * 340 / (1 + heatK*2)))` — loi exponentielle, plus le compte est chaud plus les signaux sont récents. Le contact est tiré avec un biais vers les premiers indices (`floor(r()^1.3 * eligible.length)`).

Signaux « compte » (`who: null`) ajoutés après :
- `hiring` : 55 % de chance, `d ∈ [0,60)`, `n ∈ [3,43)`, `det = "<n> offres ouvertes — <métier>"` où métier ∈ `['commerciaux','alternants','ingénieurs','data analysts','chefs de projet','techniciens']`.
- `news` : 40 %, `d ∈ [0,120)`, `det` tiré de `SIG.news.d` (5 valeurs, l. 752).
- `job` : 30 %, **avec `who`** (un contact non-`ope`), `d ∈ [0,90)`, `det = "<name> prend le poste de <title>"`.

Le référentiel `SIG` (l. 740–753) donne pour chaque type : `l` (libellé affiché), `c` (canal : `pub`/`site`/`mail`/`ext`), `d` (liste des couples `[détail, étape]`, absente pour `job` et `hiring`).

#### Contrat `Monthly` (12 entrées)
```ts
{ pub: number, site: number, mail: number, ext: number }   // comptages de signaux par canal
```
Indexé par `monthIdx(d)` (l. 719) : `(année-2025)*12 + mois - 9`. Index 0 = octobre 2025, index 11 = septembre 2026. Les signaux hors fenêtre sont ignorés.

#### Contrat `Hist` (objet partiel selon `status`)
```ts
{
  signed?: number,        // K€ signés (status 'ancien' : 40..300 ; 'client' : 30..430)
  contracts?: number,     // nb de contrats ('ancien' : 2..8 ; 'client' : 1..5)
  loss?:  { amt: number, d: number, reason: string, label: 'Renouvellement'|'Opportunité' },
  open?:  { amt: number, stage: 'Découverte'|'Démo faite'|'Proposition envoyée'|'Négociation' }
}
```
`loss.amt` : 18 000–88 000 € (`ancien`, label `Renouvellement`, `d` 180–600) ou 12 000–102 000 € (`perdu`, label `Opportunité`, `d` 60–420). `loss.reason` tiré de `LOSS_REASONS` (l. 768).
`open.amt` : 15 000–125 000 € (uniquement `status === 'encours'`).

#### Contrat `Entity`
```ts
{ id: 'e0'|'e1', name: string, kind: 'groupe'|'filiale', to?: string }  // to = id du contact rattaché
```
`e0` toujours présent (`"Groupe " + name`). `e1` (filiale, `name + ' ' + ville de CITIES`) avec 60 % de probabilité, rattachée à un contact `c2..c4`.

#### Contrat `lv.paid`
```ts
{ on: boolean, w: number[12], imp30: number, cpm: number }
```
`on = r2() < .4 + heatK*.45`. `w` = impressions par semaine (index 11 = semaine la plus récente ; voir §7). `imp30 = sum(w.slice(0,4))`. `cpm` = 38 à 68 €.

#### Contrat `lv.social` — tableau d'événements, **non trié**
```ts
{ post: number, who: string, kind: 'réaction'|'commentaire'|'partage', d: number }
```
`post` = index dans `POSTS` (l. 788–795 : 12 triplets `[titre, auteur, joursDepuisPublication]`). Actif si `r2() < .22 + heatK*.55` ; 1 à 8 événements ; biais `floor(r2()^1.4 * 12)` vers les posts récents ; `d = POSTS[i][2] - floor(r2() * min(5, POSTS[i][2]))`.
Répartition des `kind` : ≈72 % `réaction`, puis ≈70 % de ce qui reste en `commentaire`, le solde en `partage`.

#### Contrat `lv.outbound`
```ts
{
  on: boolean, seq: number,          // seq = index dans SEQS (4 séquences, l. 796)
  contacts: number, sent: number, opened: number, replied: number,
  meeting: 0|1, bounced: 0|1, start: number,   // start = jours écoulés du 1er message
  log: OutMsg[]                       // AJOUTÉ par enrich(), TRIÉ par d croissant
}
```
```ts
OutMsg = { d: number, who: string, type: number, opened: boolean, clicked: boolean, replied: boolean }
```
`type` = index dans `EMAIL_TYPES` (l. 801–808 : 6 étapes, chacune `{l, ch:'Email'|'LinkedIn', open, click, reply}`). Une étape tous les 3 jours à rebours depuis `start` ; la séquence s'arrête à la première réponse.

#### Contrat `lv.sdr`
```ts
{
  owner: string,            // SDRS[seed % 4] (l. 786)
  callsW: number[12],       // appels par semaine, index 11 = semaine la plus récente
  calls30: number, connects: number, convs: number, rdv: 0|1,
  last: number | null,      // jours depuis le dernier appel ; null = jamais appelé
  log: Call[]               // AJOUTÉ par enrich(), TRIÉ par d croissant
}
```
```ts
Call = { d: number, who: string, out: 'nr'|'vm'|'bar'|'conv'|'call'|'rdv', h: number, m: number, dur: number }
```
`out` : `nr` 42 %, `vm` 18 %, `bar` 12 %, `conv` 16 %, `call` 6 %, `rdv` 6 % (`CALL_OUT`, l. 809, donne `[libellé, classeÉtat]`). `h` ∈ [8,18[, `m` ∈ [0,60[, `dur` en **secondes** : 60–480 si `conv|rdv|call`, 30–90 si `bar`, 0 sinon.
`enrich()` **recalcule** `calls30/connects/convs/rdv/last` à partir du log.

#### Contrat `lv.sales`
```ts
{
  ae: string,                   // AES[seed % 3] (l. 787)
  close?: number, created?: number, next?: string,   // seulement si hist.open
  wonRecent?: boolean, cycle?: number, wonAmt?: number,  // seulement si status 'client'
  meetings: Meeting[]           // AJOUTÉ par enrich(), TRIÉ par d croissant
}
```
```ts
Meeting = { d: number, type: 'R1'|'R2'|'R3'|'COMITE'|'QBR', who: string[], out: 'tenu'|'noshow'|'avenir', ae: string }
```
`d < 0` = meeting **futur** ; `out` vaut alors `'avenir'`. `who` contient 1 ou 2 ids de contact (45 % de chance d'un second). Libellés dans `MEET` (l. 810).
`created` = jours depuis la création de l'opportunité (3–173) ; `close` = jours **restants** avant closing (15–125) ; `next` tiré de 5 phrases.

### 4.3 `enrich(a)` — **l. 844–876** — `(a: Account) => void` (mute `a.lv`)

Appelée par `rebuild()` sur chaque compte **après** `buildAccount`. Elle remplit ce que `buildAccount` ne pouvait pas déduire des signaux :
1. **Paid rétro-déduit** (l. 846–847) : si le compte a des signaux `ad`/`lgf` ≤ 30 j et que `imp30 === 0`, elle **force** `on = true` et réécrit `w` (4 dernières semaines chargées) et `imp30`.
2. **Outbound** : construit `O.log` puis **recalcule** `contacts / sent / opened / replied / meeting / bounced`. Si `!O.on`, tout est remis à 0.
3. **SDR** : construit `D.log` à partir de `callsW`, puis recalcule les agrégats 30 j et `last`.
4. **Sales** : construit `S.meetings` — R1/R2/R3 rétrospectifs selon l'étape de `hist.open`, un meeting futur, un R1 si `sdr.rdv` ou `outbound.meeting`, des QBR si `status === 'client'`, un R3 si `hist.loss.d < 300`.

### 4.4 `rebuild()` — **l. 1057–1063** et `rescore()` — **l. 1047–1056**

```js
function rebuild(){
  const seen = new Set();
  accounts = names.map(buildAccount).filter(a => !seen.has(a.id) && seen.add(a.id));
  accounts.forEach(enrich);
  accounts.forEach(a => { const i = scoreICP(a, DEFAULT_CFG).total, e = scoreENG(a, DEFAULT_CFG).total;
                          a.q0 = quadOf(i, e, DEFAULT_CFG); a.icp0 = i; a.eng0 = e; });
  rescore();
}
```
`q0`/`icp0`/`eng0` sont les scores **au réglage par défaut**, gelés, utilisés partout pour les deltas et l'écran Moteur.

### 4.5 Générateurs dérivés (recalculés à chaque rendu)

| Fonction | Ligne | Signature | Forme du résultat |
|---|---|---|---|
| `paidOf(a)` | 1293 | `(a) => Array` | `[{ c: CreaDef, imp: number, clicks: number, spend: number }]` — répartit `a.lv.paid.imp30` entre les créas des campagnes du quadrant (`CAMPQ[a.q]`, plus `'R'` si un signal `pricing` ≤ 30 j), poids `.3+r()` normalisés, campagne `R` ramenée à 40 %. `clicks = round(imp * c.ctr * (.6 + r()*.8))`, `spend = imp * cpm / 1000`. |
| `assetStats()` | 1299 | `() => Array` | `[{ x: AssetDef, spent, imp, clicks, cons, leads, acc, A, cpl }]` — `spent = li*MTD*(.85+r*.3)`, `imp = spent/42*1000`, `cons` = nb de signaux ≤ 30 j dont `det` matche `AssetDef.m`, `leads` = sous-ensemble de types `dl|lgf|webinar|form`, `acc`/`A` = comptes distincts, `cpl = spent/leads` ou `null`. |
| `creaStats()` | 1457 | `() => Record<creaId, …>` | `{ [creaId]: { imp, cl, sp, ctr, acc } }` — agrégat de `paidOf` sur tout le portefeuille. |
| `rdvEvents()` | 1188 | `() => Array` | `[{ d: number, src: 'sdr'\|'out'\|'in'\|'paid', a: Account }]` — 4 sources : appel `out === 'rdv'`, 1re réponse outbound si `meeting`, dernier signal `form` de détail `"Demande de démo"`, dernier `lgf` de détail `"LGF — Demande de démo"`. |
| `leverRow(k, a)` | 1307 | `(k, a) => Row` | `{ state: [classe, libellé], metric: string, detail: string(HTML), next: string, sortv: number, …extras }` — une ligne du tableau de suivi, par levier. |
| `plan(a)` | 1637 | `(a) => Plan` | `{ porte: Contact, path: [{c: Contact[], why: string}], hook: string, strong: Signal\|undefined }`. `porte` = contact `actif` non-décideur le plus chaud (repli : le plus chaud tout court). |
| `layout(a)` | 1603 | `(a) => {nodes, links, byId}` | `nodes: [{id, kind:'acc'\|'ent'\|'c'\|'loss'\|'open', x, y, fixed?, c?, e?}]`, `links: [{s, t, k:'ent'\|'org'\|'hors'\|'loss'\|'lossrel'\|'open', L}]`. Simulation à ressorts, 420 itérations, puis normalisation dans une boîte 900×560 avec marge 70. |
| `taskItems(k, id)` | 1921 | `(agentKey, taskId) => Item[]` | `[{ t: string, a: Account\|null, d: number, id: string }]` — `id = k + '.' + taskId + '.' + index + '.' + (a?a.id:'')`. |
| `agentRun(k)` | 1979 | `(k) => {items, out, capped?}` | `items: [{…Item, task: TaskDef, status: 'auto'\|'validé'\|'rejeté'\|'attente'}]`, `out` = nb d'actions écartées par le périmètre, `capped` = nb reportées par le plafond `maxDay*7`. |
| `agentCfg(k)` | 1909 | `(k) => Cfg` | `{ scope:{A,B,C,D}, mine, noOpp, freq, hour, days, maxDay, notif, tasks:{[taskId]:{mode, p:{}}} }` — **auto-complétant** (crée les valeurs manquantes à la lecture). |
| `ALL_TASKS()` | 2204 | `() => Task[]` | aplatit `PHASES` → `{ph, id, t, d, who, role, j:[from,to], out, tool}`. |

### 4.6 Exemples JSON réels (sortie vérifiée du code, portefeuille par défaut)

#### Un compte — `Terrarys Énergie` (premier nom de `sampleNames()`)
```json
{
  "id": "terrarys-e-nergie",
  "name": "Terrarys Énergie",
  "domain": "terrarysenergie.fr",
  "sector": "Énergie",
  "size": 2300,
  "status": "perdu",
  "seed": 405081822,
  "fyStart": 6,
  "n30": 0,
  "contacts": [ /* 14 Contact */ ],
  "signals": [ /* 21 Signal, triés par d croissant */ ],
  "monthly": [
    {"pub":0,"site":1,"mail":0,"ext":0}, {"pub":0,"site":0,"mail":0,"ext":0},
    {"pub":0,"site":0,"mail":0,"ext":0}, {"pub":0,"site":1,"mail":0,"ext":0},
    {"pub":0,"site":0,"mail":0,"ext":0}, {"pub":0,"site":0,"mail":0,"ext":0},
    {"pub":0,"site":0,"mail":0,"ext":0}, {"pub":0,"site":0,"mail":0,"ext":0},
    {"pub":0,"site":0,"mail":0,"ext":0}, {"pub":0,"site":1,"mail":1,"ext":0},
    {"pub":0,"site":0,"mail":0,"ext":2}, {"pub":0,"site":0,"mail":0,"ext":0}
  ],
  "hist": { "loss": { "amt": 83480, "d": 76, "reason": "budget gelé en fin d'exercice", "label": "Opportunité" } },
  "entities": [ { "id": "e0", "name": "Groupe Terrarys Énergie", "kind": "groupe" } ],
  "lv": {
    "paid":   { "on": false, "w": [0,0,0,0,0,0,0,0,0,0,0,0], "imp30": 0, "cpm": 44.961502521298826 },
    "social": [ {"post":2,"who":"c7","kind":"commentaire","d":6} ],
    "outbound": { "on": false, "seq": 1, "contacts": 0, "sent": 0, "opened": 0, "replied": 0, "meeting": 0, "bounced": 0, "start": 23, "log": [] },
    "sdr": { "owner": "Inès Barrault", "callsW": [0,0,0,0,0,0,0,0,0,0,1,0], "calls30": 0, "connects": 0, "convs": 0, "rdv": 0, "last": 73, "log": [ /* 1 Call */ ] },
    "sales": { "ae": "Julien Castaing", "meetings": [ /* 1 Meeting */ ] }
  }
}
```

#### Un contact / membre de comité
```json
{ "id": "c1", "fn": "Léa", "ln": "Benali", "name": "Léa Benali",
  "role": "dec", "prov": "actif", "title": "Responsable achats",
  "sig": [ /* références vers des objets de signals */ ],
  "heat": 0.0007932152308166359 }
```

#### Un signal (contact) et un signal (compte)
```json
{ "t": "form", "d": 71, "who": "c13", "det": "Demande de contact", "st": "bofu" }
```
```json
{ "t": "hiring", "d": 31, "who": null, "n": 27, "det": "27 offres ouvertes — commerciaux" }
```
```json
{ "t": "news", "d": 43, "who": null, "det": "Nomination d'un nouveau DG" }
```

#### Une opportunité ouverte (`Dynaium Finance`)
```json
{ "open": { "amt": 88203, "stage": "Démo faite" } }
```
avec côté `lv.sales` :
```json
{ "ae": "Julien Castaing", "close": 85, "created": 97, "next": "Call de cadrage avec le DAF" }
```

#### Une perte
```json
{ "loss": { "amt": 83480, "d": 76, "reason": "budget gelé en fin d'exercice", "label": "Opportunité" } }
```

#### Une campagne paid (définition, `CAMP_DEF`, l. 811)
```json
{ "A": { "n": "ABM 1:1 — nominatif Attaquer", "b": 6000 },
  "B": { "n": "ABM 1:few — Réveiller par secteur", "b": 8000 },
  "N": { "n": "Notoriété — baromètre 2026", "b": 5000 },
  "R": { "n": "Retargeting BOFU — visiteurs tarifs", "b": 3000 } }
```
Mapping quadrant → campagne : `CAMPQ = { A:'A', B:'B', C:'N', D:'N' }` (l. 812).

#### Une créa — définition (`CREAS[0]`, l. 814) et diffusion (sortie de `paidOf`)
```json
{ "id": "cr1", "camp": "A", "t": "{compte}, 3 idées pour votre pipeline",
  "f": "Image unique", "ctr": 0.011, "bg": "#0E2841" }
```
```json
{ "c": { "id": "cr1", "camp": "A", "t": "{compte}, 3 idées pour votre pipeline", "f": "Image unique", "ctr": 0.011, "bg": "#0E2841" },
  "imp": 5497, "clicks": 64, "spend": 329.72716103986045 }
```
Les 8 créas : `cr1..cr8`, formats `Image unique`, `Document`, `Carrousel`, `Vidéo`, `Lead Gen Form`. `t` contient les jetons `{compte}` et `{secteur}` substitués par `fillCrea(t, a)` (l. 1292). `CREA_IMG` (l. 1396) associe 7 créas à une image `img/*.jpg`.

#### Un contenu — définition (`ASSETS`, l. 823) et statistiques (`assetStats()`)
```json
{ "id": "lb2", "l": "Baromètre B2B 2026", "ty": "Étude", "st": "tofu", "li": 3000,
  "m": ["Baromètre B2B 2026", "LGF — Baromètre B2B 2026"] }
```
```json
{ "x": { "id": "lb2", "l": "Baromètre B2B 2026", "ty": "Étude", "st": "tofu", "li": 3000, "m": ["Baromètre B2B 2026","LGF — Baromètre B2B 2026"] },
  "spent": 1826.7214748309925, "imp": 43493.36844835697, "clicks": 301,
  "cons": 22, "leads": 22, "acc": 19, "A": 5, "cpl": 83.03279431049965 }
```
`li` = budget LinkedIn mensuel en € · `m` = **liste des `det` de signaux qui comptent pour ce contenu** (`assetOf(s)` l. 832 fait la jointure par égalité de chaîne).

#### Un appel SDR
```json
{ "d": 10, "who": "c8", "out": "conv", "h": 17, "m": 19, "dur": 272 }
```

#### Un message outbound
```json
{ "d": 33, "who": "c12", "type": 1, "opened": false, "clicked": false, "replied": false }
```

#### Un meeting (passé et futur)
```json
{ "d": 58, "type": "R2", "who": ["c4"], "out": "tenu", "ae": "Julien Castaing" }
```
```json
{ "d": -6, "type": "R3", "who": ["c6","c3"], "out": "avenir", "ae": "Julien Castaing" }
```

#### Un événement social
```json
{ "post": 2, "who": "c7", "kind": "commentaire", "d": 6 }
```

#### Une tâche d'agent (définition, `AGENT_TASKS.paid[1]`, l. 1866)
```json
{ "id": "cut", "l": "Couper les créas faibles",
  "d": "Met en pause une créa dont le CTR reste sous le seuil après assez d'impressions.",
  "trig": "CTR sous le seuil", "mode": "valid",
  "p": [ { "k": "ctr", "l": "CTR minimum", "v": 0.35, "u": "%", "s": 0.05 },
         { "k": "imp", "l": "Impressions min. avant décision", "v": 2000, "u": "" } ] }
```
`mode` ∈ `auto` | `valid` | `off`. Un paramètre est numérique (`v`, `u` unité, `s` pas facultatif) ou un select (`o: string[]`).

#### Une entrée de journal d'agent (sortie de `agentRun`)
```json
{ "t": "Ajouté à l'audience « ABM 1:1 — nominatif Attaquer »",
  "a": { /* référence Account */ },
  "d": 3,
  "id": "paid.aud.4.lumacom-sante",
  "task": { "id": "aud", "l": "Synchroniser les audiences", "d": "…", "trig": "…", "mode": "auto", "p": [ … ] },
  "status": "auto" }
```
Les 4 statuts sont mappés par `ST_CHIP` (l. 1995) : `auto → ['ok','exécuté']`, `validé → ['ok','validé']`, `rejeté → ['mute','rejeté']`, `attente → ['warn','à valider']`.

---

## 5. POINTS D'INJECTION

### 5.1 Les 4 endroits où substituer un jeu de données réel

| Point | Ligne | Ce qu'il faut fournir | Effet |
|---|---|---|---|
| **A. `names` + `buildAccount`** | 1045 / 917 / 1057–1063 | Remplacer `accounts = names.map(buildAccount)…` par `accounts = DATA.accounts` respectant le contrat §4.2. | **Point d'injection unique et suffisant** : tous les écrans dérivent de `accounts`. `enrich()` (l. 1058) doit être **supprimé de l'appel** si `lv.*.log` / `lv.sales.meetings` sont fournis, sinon il les écrase. |
| **B. `paidOf(a)`** | 1293 | `[{c, imp, clicks, spend}]` par compte, `c` étant une entrée de `CREAS`. | Alimente Paid (vue compte et entreprise), `creaStats()`, les cartes de créas, et les KPI de la bibliothèque Content. Peut rester dérivé de `lv.paid.imp30` si on préfère. |
| **C. `assetStats()`** | 1299 | `[{x, spent, imp, clicks, cons, leads, acc, A, cpl}]`. | Alimente la bibliothèque Content et l'agent `content.boost`. Ne dépend que de `ASSETS` + des signaux (jointure par `det`). |
| **D. `taskItems(k, id)`** | 1921 | `[{t, a, d}]` par couple (agent, tâche). | Remplacer par des propositions d'agent réelles. `agentRun()` se charge du filtrage, du statut et du plafond. |

Référentiels à remplacer en même temps (tous purement déclaratifs, aucun code à toucher) :
`SECTORS` (727) · `SIG` (740) · `SIG_ORDER` (754) · `CONTENT_T` (755) · `WHY` (757) · `STATUS` (765) · `LOSS_REASONS` (768) · `QUADS` (772) · `LEVERS` (778) · `SDRS` (786) · `AES` (787) · `POSTS` (788) · `SEQS` (796) · `OPP_STAGES` (798) · `EMAIL_TYPES` (801) · `CALL_OUT` (809) · `MEET` (810) · `CAMP_DEF` (811) · `CAMPQ` (812) · `CREAS` (813) · `ASSETS` (823) · `AGENTS` (834) · `AGENT_TASKS` (1858) · `LIB` (1397) · `CHAPTERS` (1416).

### 5.2 Ce qui est CALCULÉ — à ne **jamais** fournir en dur

Écrasé à chaque `rescore()` (l. 1047–1056) :

| Champ | Formule | Ligne |
|---|---|---|
| `a.I` | `scoreICP(a, cfg)` → `{total, lines[], fy}` | 1003 |
| `a.E` | `scoreENG(a, cfg)` → `{total, parts, pts, lines, mal, raw, mix, heats, hot, committee}` | 1015 |
| `a.icp` | `a.I.total` | 1049 |
| `a.eng` | `a.E.total` | 1049 |
| `a.q` | `quadOf(a.icp, a.eng, cfg)` | 1042 |
| `a.prio` | `round((icp + eng) / 2)` | 1049 |
| `a.hot` | nb de contacts `heat ≥ cfg.eng.hotMin` et `prov !== 'hors'` | 1050 |
| `a.committee` | nb de contacts `prov !== 'hors'` | 1050 |
| `contact.heat` | `Σ sigVal(s, cfg.eng)` sur `contact.sig` | 1051 |
| `a.surge` | `Σ sigW(s≤14j) − Σ sigW(14<s≤28j)` (accélération, **poids non amortis**) | 1052 |
| `a.plan` | `Set(QUADS[a.q].levers)` + `'sales'` si `status ∈ {encours, client}` | 1053 |
| `a.q0` / `a.icp0` / `a.eng0` | mêmes scores avec `DEFAULT_CFG` (gelés) | 1060 |

Agrégats recalculés à chaque rendu (jamais stockés) : tous les KPI du cockpit, `rdvEvents()`, `creaStats()`, `assetStats()`, `leverRow()`, `plan()`, `layout()`, `agentRun()`, les séries hebdomadaires (`weekLabels()` + bucket `floor(d/7)`).

### 5.3 Dépendances champ → écran

| Champ d'`Account` | Lu par |
|---|---|
| `name`, `domain`, `sector`, `size` | partout (tableaux, recherche `sorted()` l. 1078, en-têtes, `fillCrea`) |
| `id` | clé de tout ; `ui.pins`, `ui.acc`, `ui.test`, `lvState().acc`, ids d'items d'agent |
| `status` | `scoreICP` (`I.hist`), pastille `.stp`, `leverRow('sales')`, `a.plan`, `narrative`, `plan().hook`, KPI « % jamais chassés » de la proposition |
| `size` | `sizeBand()` → `scoreICP` |
| `sector` | `scoreICP` (secteurs cibles), `fillCrea`, `plan().hook` |
| `fyStart` | `fyPhase()` → `scoreICP` ; colonne « Exercice fiscal » du cockpit ; chip « Budget en préparation » ; en-tête fiche compte ; écran Moteur (répartition du portefeuille) |
| `signals[]` | `scoreENG` (tout le pilier Intention + Timing), écran Signaux, frise de la fiche compte, `monthly`, `leverRow('content'\|'paid'\|'sdr')`, `rdvEvents()`, `assetStats()`, `paidOf()` (via `pricing`), `plan().strong`, agents `content.dl/gap`, `paid.rt`, `crm.moves/attach` |
| `signals[].st` | multiplicateur funnel, `isStrong()`, `deepest()`, filtres BOFU/MOFU/TOFU, `mixHTML` |
| `signals[].det` | `assetOf()` (jointure exacte avec `ASSETS[].m`), `rdvEvents()` (égalité exacte avec `"Demande de démo"` / `"LGF — Demande de démo"`), affichage |
| `signals[].who` | rattachement contact → `heat` → `hot` → pilier Comité ; ligne « Signaux du compte » quand `null` |
| `contacts[]` | `scoreENG` (pilier Comité), carte du comité, `plan()`, tous les tableaux de levier en vue compte, agents `crm.enrich/dedup/arch`, `outbound.enroll`, `sales.dec` |
| `contacts[].prov` | exclusion `hors` partout ; `cible` = à enrichir ; `actif` = compte dans la couverture et les malus |
| `contacts[].role` | couleurs, `plan()` (porte / décision / budget), pilier Comité, agent `social.dm` |
| `contacts[].title` | `BUDGET()` dans `plan()`, affichage, agent `crm.enrich` |
| `hist.open` | `leverRow('sales')`, KPI pipe du cockpit, `enrich()` (génère les meetings), `agentRun` filtre `noOpp`, agents `sales.stale/dec/risk`, écran Sales, proposition §02 |
| `hist.loss` | `scoreICP` (malus si `d < 180`), nœud `loss` de la carte, `narrative`, `plan().hook`, KPI de gain sur 12 mois |
| `hist.signed` / `contracts` | KPI « Signé » en vue compte Sales, `narrative`, `plan().hook` |
| `entities` | `scoreICP` (`multi` si length > 1), carte du comité, `leverRow('sales')` (« ouvrir <filiale> ») |
| `lv.paid.imp30` / `.w` / `.cpm` | `paidOf()`, KPI Paid, `touched.paid` du cockpit, courbe hebdo Paid |
| `lv.social[]` | écran Social, `touched.social`, agents `social.*` |
| `lv.outbound` | écran Outbound, `rdvEvents()` (`src:'out'`), `touched.outbound`, agents `outbound.*` |
| `lv.sdr.log` / `.owner` / `.last` | écran SDR, `rdvEvents()` (`src:'sdr'`), `touched.sdr`, filtre SDR, agents `sdr.*` et `outbound.hand` |
| `lv.sales.meetings` / `.ae` | écran Sales, KPI « Meetings tenus » du cockpit, `touched.sales`, agents `sales.brief/recap/dec` |
| `seed` | `paidOf()`, `layout()`, choix du SDR et de l'AE. **À conserver ou remplacer par un identifiant stable** si on garde ces dérivations. |

---

## 6. MOTEUR DE SCORING

### 6.1 Configuration par défaut — `DEFAULT_CFG` **l. 879–897**

```js
{
  icp: {
    size: { s: 10, m: 25, l: 40, xl: 35 },
    sectors: ['Industrie','Logiciel','Banque & assurance','Santé','Énergie'],
    sectorIn: 35, sectorOut: 5,
    hist: { ancien: 15, client: 10 },
    multi: 10,
    fy: { prep: 15, start: 8, prepFrom: 1, prepTo: 4 },
    lossMalus: 15
  },
  eng: {
    w: { intent: 55, comite: 30, timing: 15 },
    half: 30, sat: 35, hotMin: 4,
    stage: { bofu: 2, mofu: 1, tofu: 0.5 },
    sig: { form: 12, lgf: 10, job: 9, dl: 8, webinar: 7, pricing: 6,
           hiring: 5, news: 4, ad: 3, click: 3, page: 2, open: 1 },
    comite: { dec: 40, hot2: 30, champ: 20, cover: 10 },
    timing: { job: 55, event: 45 },
    noContact: 15
  },
  matrix: { icp: 78, eng: 70 }
}
```

Bandes de taille — `sizeBand(n)` l. 995 : `< 500 → 's'` · `500–1 999 → 'm'` · `2 000–9 999 → 'l'` · `≥ 10 000 → 'xl'`.

### 6.2 Score ICP — `scoreICP(a, C)` **l. 1003–1014** — sortie 0–100 entière

Somme des lignes, puis `round(clamp(Σ, 0, 100))` :

1. **Taille** : `+ C.icp.size[sizeBand(a.size)]` — toujours présent.
2. **Secteur** : `+ C.icp.sectorIn` (35) si `a.sector ∈ C.icp.sectors`, sinon `+ C.icp.sectorOut` (5) — toujours présent.
3. **Historique** : `+ C.icp.hist[a.status]` — seulement pour `ancien` (15) et `client` (10). `jamais`, `perdu`, `encours` n'apportent rien.
4. **Multi-entités** : `+ C.icp.multi` (10) si `a.entities.length > 1`.
5. **Exercice fiscal** : `+ C.icp.fy.prep` (15) si phase `prep`, `+ C.icp.fy.start` (8) si phase `start`, `+0` sinon — **toujours présent dans `lines`** (avec `v: 0` si hors période).
6. **Malus perte** : `− C.icp.lossMalus` (15) si `a.hist.loss && a.hist.loss.d < 180` (seuil **codé en dur**, ligne 1011, indépendant de la config).

**Phase d'exercice — `fyPhase(a, I)` l. 998–1001** avec `monthsTo(m) = (m - TODAY.getMonth() + 12) % 12` (l. 997, `TODAY.getMonth() === 8`) :
- `to ∈ [I.fy.prepFrom, I.fy.prepTo]` (défaut 1 à 4 mois avant le début d'exercice) → `{k:'prep', l:'budget en préparation (exercice dans N mois)'}`
- sinon, `since = (12 - to) % 12 ≤ 2` → `{k:'start', l:'exercice démarré il y a N mois'}` (ou « qui démarre ce mois-ci » si `since === 0`)
- sinon → `{k:'none'}`

### 6.3 Score d'engagement — `scoreENG(a, C)` **l. 1015–1041** — sortie 0–100 entière

#### Valeur d'un signal
```js
decay(d, E)  = 0.5 ** (d / E.half)                    // demi-vie, défaut 30 jours   (l. 991)
sigW(s, E)   = (E.sig[s.t] || 0) * (s.st ? E.stage[s.st] : 1)   // poids × multiplicateur funnel (l. 992)
sigVal(s, E) = sigW(s, E) * decay(s.d, E)             // valeur amortie               (l. 993)
```
**Multiplicateurs TOFU/MOFU/BOFU** (`E.stage`) : `bofu ×2`, `mofu ×1`, `tofu ×0,5`. Un signal **sans `st`** (`job`, `hiring`, `news`) prend un multiplicateur de **1**.

#### Pilier 1 — Intention (saturant)
```js
raw    = Σ sigVal(s, E)   sur TOUS les signaux
intent = 100 * (1 - Math.exp(-raw / E.sat))            // E.sat = 35 par défaut
```
`E.sat` est la valeur brute qui remplit 63 % de l'échelle. `lines.intent` liste les 4 types les plus contributifs (contribution ≥ 0,05), en **valeur brute** (`raw: true`).
`mix` cumule `raw` par étape : `{bofu, mofu, tofu, ext}` (`ext` = signaux sans `st`).

#### Pilier 2 — Comité (plafonné à 100)
```js
heats[ct.id] = Σ sigVal(s, E) sur ct.sig
hot          = contacts avec heats ≥ E.hotMin (4) ET prov !== 'hors'
act          = contacts prov === 'actif'
committee    = contacts prov !== 'hors'
cover        = committee.length ? act.length / committee.length : 0

comite = clamp( (décideur actif      ? E.comite.dec   : 0)   // 40
              + (hot.length >= 2     ? E.comite.hot2  : 0)   // 30
              + (champion actif      ? E.comite.champ : 0)   // 20
              + cover * E.comite.cover                       // jusqu'à 10
              , 0, 100)
```

#### Pilier 3 — Timing (plafonné à 100)
```js
job = un signal t:'job'   avec d <= 90      → + E.timing.job   (55)
ev  = un signal t:'hiring' ou 'news' avec d <= 60 → + E.timing.event (45)
timing = clamp(job + ev, 0, 100)
```
Les seuils 90 j et 60 j sont **codés en dur** (l. 1032), pas réglables.

#### Combinaison et malus
```js
W     = E.w.intent + E.w.comite + E.w.timing              // 100 par défaut
pts.k = parts.k * E.w[k] / W                              // pondération normalisée
total = Σ pts
if (aucun contact prov==='actif') total -= E.noContact    // malus 15
return round(clamp(total, 0, 100))
```
Le **seul malus** de l'engagement est `noContact`. Le seul malus de l'ICP est `lossMalus`.

### 6.4 Quadrants — `quadOf(icp, eng, C)` **l. 1042**

```js
icp >= C.matrix.icp ? (eng >= C.matrix.eng ? 'A' : 'B')
                    : (eng >= C.matrix.eng ? 'C' : 'D')
```
Seuils par défaut : **ICP ≥ 78** et **engagement ≥ 70**.

| Quadrant | Libellé | Sous-titre | Leviers activés (`QUADS[q].levers`, l. 772–777) |
|---|---|---|---|
| A | Attaquer | ICP fort · engagé | `sales, sdr, paid, content, social` |
| B | Réveiller | ICP fort · froid | `paid, social, content` |
| C | Qualifier | hors cœur ICP · engagé | `sdr, outbound, content` |
| D | Veille | ICP faible · froid | `content` |

`a.plan` ajoute `'sales'` si `status ∈ {encours, client}` (l. 1053).

Répartition obtenue avec le portefeuille d'exemple et les réglages par défaut (vérifié) : **A 17 · B 25 · C 22 · D 36** sur 100 comptes, 3 362 signaux au total.

### 6.5 Préréglages — `PRESETS` **l. 898–903**

```js
'Équilibré (défaut)' : {}
'Intention d\'abord' : { eng: { w: { intent:75, comite:15, timing:10 }, half: 21 } }
'Comité d\'abord'    : { eng: { w: { intent:35, comite:55, timing:10 } } }
'BOFU d\'abord'      : { eng: { stage: { bofu:3, mofu:1, tofu:0.25 } } }
```
Appliqués par `cfg = deepMerge(DEFAULT_CFG, PRESETS[k])` (l. 2456) — donc **remplacement complet**, pas cumulatif.

### 6.6 Où vivent les réglages

- En mémoire : `let cfg = deepMerge(DEFAULT_CFG, store.get('abm-tdc-cfg2') || {})` (l. 906–907).
- Persisté : `commit()` (l. 2461) écrit `abm-tdc-cfg2`, **ou le supprime** si `isDefault()` (comparaison `JSON.stringify` stricte, l. 908).
- Lecture/écriture par chemin pointé : `getP(path)` / `setP(path, v)` (l. 2397–2398), `path` étant p. ex. `eng.sig.form`, `icp.fy.prepTo`, `matrix.icp`. L'attribut DOM correspondant est `data-path`, l'id `in-<path avec tirets>` (`idOf`, l. 2399).
- Réglages des agents : ailleurs, dans `ui.agents.cfg[k]` → clé `abm-tdc-agents`.

### 6.7 Le « barème » affiché

Le bloc `.formula` (l. 2406–2409) reproduit textuellement :
```
ICP        = taille + secteur + historique + multi-entités + exercice fiscal − perte récente  (plafond 100)
engagement = Σ ( pilier × poids ) / Σ poids − malus  ·  intention = 100 × (1 − e^(−brut / saturation))
brut       = Σ poids du signal × multiplicateur funnel × 0,5^(âge / demi-vie)
quadrant   = ICP ≥ seuil ? (engagement ≥ seuil ? A : B) : (engagement ≥ seuil ? C : D)
```

---

## 7. PIÈGES REPÉRÉS DANS LE CODE

### 7.1 Les trois plus dangereux

**P1 — `enrich()` écrase les journaux fournis.** `rebuild()` (l. 1058) appelle `enrich` sur chaque compte. `enrich` **reconstruit intégralement** `lv.outbound.log`, `lv.sdr.log` et `lv.sales.meetings`, puis **recalcule** `outbound.{contacts,sent,opened,replied,meeting,bounced}` et `sdr.{calls30,connects,convs,rdv,last}`. Elle peut aussi **forcer `lv.paid.on = true` et réécrire `lv.paid.w`** si le compte a des signaux `ad`/`lgf` récents et `imp30 === 0` (l. 846–847). Avec des données réelles, il faut retirer `accounts.forEach(enrich)` de `rebuild()` — sinon les vrais appels, e-mails et meetings disparaissent silencieusement.

**P2 — Les jointures se font par égalité de chaîne, pas par identifiant.** Trois endroits :
- `assetOf(s) = ASSETS.find(x => x.m.includes(s.det))` (l. 832) : un contenu est reconnu par le **texte exact** de `signal.det` (guillemets français « » compris). Un accent ou une espace insécable en moins et toute la bibliothèque Content passe à zéro téléchargement.
- `rdvEvents()` (l. 1191–1192) : `s.det === 'Demande de démo'` et `s.det === 'LGF — Demande de démo'` — chaînes littérales. Le KPI « RDV générés » du cockpit et la carte « RDV par source » en dépendent entièrement.
- `plan()` (l. 1647) : `strong.det.replace(/^.*« |».*$/g, '')` et `strong.det.split(' prend')[0]` — l'accroche est extraite par découpage du texte du détail.

**P3 — Le cockpit est dimensionné à la largeur réelle et se re-rend au `resize`.** Ligne 1200 :
```js
const cw = V().clientWidth || 1100,
      full = Math.max(320, cw - 80),
      half = window.innerWidth > 1300 ? Math.max(320, Math.round((cw - 112) / 2)) : full;
```
Ces largeurs sont passées en `viewBox` aux `colChart`. Un écouteur `resize` débouncé à 200 ms (l. 2480) **re-rend uniquement le cockpit** en restaurant `window.scrollY`. Conséquences : (a) un rendu hors document (iframe cachée, capture, `display:none`) donne `clientWidth === 0` → repli sur 1100 px et graphiques mal proportionnés ; (b) tout état non persisté du cockpit est reconstruit à chaque redimensionnement ; (c) les autres écrans **ne** se re-rendent pas au resize, leurs SVG restent figés à la largeur du premier rendu.

### 7.2 Autres pièges

**Indexation temporelle inversée.** Partout, `d` = jours **écoulés** (positif = passé). Les séries hebdomadaires font `const w = Math.floor(d / 7); if (w < 12) rows[11 - w][clé]++` : **l'index 11 est la semaine courante, l'index 0 la plus ancienne**. Même inversion pour `lv.paid.w` et `lv.sdr.callsW` (`imp30 = sum(w.slice(0, 4))` = les 4 dernières semaines = indices 0 à 3 — **incohérent avec l'inversion des graphiques**, où l'agrégat hebdo lit `a.lv.paid.w[11 - i]`, l. 1498). Les meetings sont la seule structure où `d < 0` (futur).

**`monthIdx()` est ancré en dur sur 2025-10.** `(x.getFullYear() - 2025) * 12 + x.getMonth() - 9` (l. 719). Changer `TODAY` sans changer cette constante décale silencieusement la matrice `monthly`, et donc la frise `frise()` et l'axe `MONTHS`.

**`TODAY` est figé au 18/09/2026.** La date affichée dans `.phead` (l. 682) et « Semaine 38 » sont **écrites en dur dans le HTML statique**, pas dérivées de `TODAY`. `WEEK_NOW = 38` et `MTD = 18/30` (« rythme attendu au 18 ») sont eux aussi des constantes. Tout changement de date demande de toucher 4 endroits.

**Les identifiants de contact sont locaux au compte.** `c0`, `c1`, … Les clés composées utilisées pour dédoublonner des contacts à l'échelle du portefeuille sont des concaténations : `a.id + e.who` (l. 1511), `s.a.id + s.who` (l. 1816). Un id de contact réel contenant le caractère utilisé par un id de compte casserait le comptage.

**`slug()` mange les accents mais pas proprement.** `slug('Terrarys Énergie')` → `terrarys-e-nergie` (le `́` combinant issu de `NFD` devient un tiret). Les ids de comptes réels doivent être fournis explicitement, pas dérivés.

**`sorted()[0]` suppose un portefeuille non vide.** `go('compte', …)` (l. 1097) et `renderLever` (l. 1375) déréférencent `sorted()[0].id` sans garde : un filtre qui ne laisse rien **ou** un portefeuille vide lève une exception.

**`ctOf(a, id)` masque les erreurs.** L. 1287 : renvoie un contact fantôme `{name:'—', role:'ope', title:'', prov:'hors'}` quand l'id est inconnu. Une référence cassée n'apparaît donc **pas** comme une erreur mais comme une ligne « — » dans les tableaux.

**`a.plan` est un `Set`, pas un tableau.** Créé l. 1053, lu via `a.plan.has(k)` partout et `[...a.plan]` l. 1789. Il n'est **pas** sérialisable en JSON : un jeu de données réel doit fournir `status`/`q` et laisser `rescore()` le construire.

**Les objets `Contact.sig` sont des références partagées.** L. 966 : `contacts.find(c => c.id === s.who).sig.push(s)` pousse **l'objet signal lui-même**, pas une copie. `heat` et `raw` compteraient double si on dupliquait les signaux au lieu de les référencer.

**Deux champs d'état morts.** `ui.agents.mode` et `ui.agents.valid` (l. 1069) sont initialisés et persistés dans `abm-tdc-agents` mais **jamais lus** : le vrai mode d'une tâche vit dans `ui.agents.cfg[k].tasks[id].mode`, construit par `agentCfg()` (l. 1909).

**Sept fonctions / constantes mortes** (déclarées, jamais appelées) : `frise` (1153), `stageWeeks` (1161), `stageLegend` (1160), `narrative` (1662), `planNote` (1392), `CAMPS` (797, doublon dégradé de `CAMP_DEF`), `propState` (2205).

**Le split des décisions d'agent est fragile.** L. 2048 : `b.dataset.dec.split(/:(?=ok$|ko$)/)`. L'id d'item est `k + '.' + taskId + '.' + index + '.' + accountId` ; l'expression ne fonctionne que parce que le suffixe est strictement `:ok` ou `:ko` en fin de chaîne. Un id de compte finissant par `:ok` casserait la validation.

**`agentCfg()` mute à la lecture.** Appelée depuis `agentModeLabel()`, `tp()`, `taskItems()`, `agentRun()`, le rendu… Elle **crée** les entrées manquantes dans `ui.agents.cfg[k]`. Une lecture « innocente » modifie donc l'état, qui sera persisté au premier `save()`.

**`history.replaceState` uniquement.** L. 1103 : aucune entrée d'historique n'est créée. Le bouton Précédent du navigateur sort de l'application.

**Le mode document est une classe sur `<body>`.** `docmode` (l. 1096) masque sidebar, bandeau et `.phead` via CSS (l. 614–616). Un rendu qui oublierait de retirer la classe laisserait l'application sans navigation.

**Toutes les interpolations passent par `esc()`… sauf certaines.** `esc` (l. 711) n'échappe que `& < > "`. Les valeurs injectées dans des attributs `style=` ou `title=` non entourés d'`esc` (par ex. `title="${esc(r.title||'')}"` va bien, mais `style="width:${…}%"` prend une valeur numérique nue) supposent des nombres. Une valeur non numérique venant de données réelles casserait silencieusement le rendu SVG/CSS.

**Les rendus qui préservent le scroll le font à la main.** Le motif `const y = window.scrollY; render(); window.scrollTo(0, y);` est répété une dizaine de fois (1246–1249, 1369, 1853–1855, 2009, 2391). Les champs de recherche restaurent en plus `selectionStart`. Tout nouveau contrôle doit reproduire ce motif, sinon la page saute en haut.

**`openModal` capture `document.onkeydown`.** L. 1450 : assignation directe (pas `addEventListener`), qui écrase tout gestionnaire clavier global existant et n'est jamais retirée.

**Les images sont référencées en chemin relatif** `img/<nom>.jpg` (`IMG`, l. 1395). Un déplacement du fichier HTML casse les couvertures, les créas et les landing pages sans erreur visible (fonds dégradés seuls).

---

## Annexe — table de correspondance rapide « je veux modifier X »

| Objectif | Aller à |
|---|---|
| Changer les couleurs | `:root` l. 12–29 |
| Changer les polices | l. 10 + `--f-*` l. 25–27 |
| Ajouter une route | `TITLE` l. 1071, dispatch `render()` l. 1107, bouton `.nav` l. 667–684 |
| Ajouter un levier | `LEVERS` l. 778 (nav auto), `FILTERS` l. 1325, `leverRow` l. 1307, `leverCompany` l. 1479, `leverAccount` l. 1556, `QUADS[].levers` l. 772 |
| Ajouter un type de signal | `SIG` l. 740, `SIG_ORDER` l. 754, `WHY` l. 757, `DEFAULT_CFG.eng.sig` l. 887, éventuellement `CONTENT_T` l. 755 et `CONTACT_SIGS` l. 756 |
| Ajouter un agent | `AGENTS` l. 834, `AGENT_TASKS` l. 1858, branche dans `taskItems` l. 1921, défaut `ui.agents.on` l. 1069 |
| Brancher des données réelles | remplacer `rebuild()` l. 1057 (et **retirer `enrich`**) |
| Changer les seuils de quadrant | `DEFAULT_CFG.matrix` l. 895 |
| Changer la date de référence | `TODAY`/`WEEK_NOW` l. 705, `monthIdx` l. 719, `MTD` l. 833, HTML statique l. 682 |

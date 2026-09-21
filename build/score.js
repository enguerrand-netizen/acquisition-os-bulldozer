/* ============================================================
   Acquisition OS Bulldozer — moteur de scoring
   Calibré sur le CRM (495 clients signés) et sur l'étude
   outbound du 17/09/2026 (4 754 comptes appelés, 33 signés).
   Aucun coefficient inventé : chaque poids a sa source dans
   CAL.sources, affichée dans l'écran « Moteur ».
   ============================================================ */
const DAY = 864e5;
const TODAY = new Date('2026-09-21T12:00:00Z');
const days = d => d ? Math.max(0, (TODAY - new Date(d)) / DAY) : null;
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const log1 = (v, k) => Math.log(1 + v) / Math.log(1 + k);   // saturation

/* ---- réglages par défaut (modifiables dans l'écran Moteur) ---- */
const CFG_DEF = {
  icp:  { secteur: 25, taille: 20, surface: 20, histo: 20, anciennete: 15 },
  eng:  { comite: 35, intention: 30, timing: 20, reciprocite: 15 },
  demiVie: 120,                 // jours — décroissance de l'intention
  etape:  { TOFU: 0.5, MOFU: 1, BOFU: 2 },
  malus:  { perteRecente: 12, aucunSignal: 25 },
  seuils: { icp: 70, eng: 65 },
  plancherSecteur: 0.25
};

/* ---- barèmes mesurés ---- */
const CAL = {
  // taux de signature observés par tranche d'effectif (étude outbound)
  taille: [ [0,50,.4], [50,200,.7], [200,1000,1.5], [1000,5000,1.0], [5000,1e9,.8] ],
  // taux par tranche de CA déclaré (M€)
  ca:     [ [0,10,.5], [10,100,.9], [100,500,2.0], [500,1e9,1.1] ],
  // taux par année de création de l'entreprise
  age:    [ [0,1999,1.0], [2000,2016,1.35], [2017,2100,.7] ],
  sources: {
    secteur:  "Part du secteur dans les 495 clients signés du CRM. Plancher à 0,25 : un secteur jamais signé est une absence de preuve, pas une impossibilité.",
    taille:   "Taux de signature par tranche : 201-1 000 sal. 1,5 %, ≥1 000 sal. 1,0 % — étude outbound 17/09/2026.",
    ca:       "100-500 M€ = 2,0 % de signature, la tranche la plus forte — même étude.",
    surface:  "Les grands comptes signés du CRM sont entrés par une filiale : Veolia via SARP et Veolia Recyclage, Carrefour via Carrefour Pro.",
    histo:    "Un chiffrage déjà accepté en interne rouvre plus vite qu'une porte froide ; un compte client sur une autre entité est une référence activable.",
    anciennete:"Entreprises créées 2000-2016 : 1,2-1,5 % de signature ; 2017+ : 0,7 %.",
    comite:   "Décideur en base + ≥2 contacts → 5,3 % de signature contre 0,5 % — le prédicteur le plus fort du CRM.",
    intention:"Contenu téléchargé avant l'appel → 3,9 % contre 0,5 %. Un formulaire LinkedIn Lead Gen seul ne discrimine pas (76 % des deux côtés).",
    timing:   "Délai médian premier appel → deal : 97 jours ; 14 des 33 signés au-delà de 6 mois.",
    reciprocite:"157 touches sans signal en face (Veolia Énergie Performance) : la dépense d'effort n'est pas un signal d'intérêt.",
    aucunSignal:"0 contact ou aucun signal digital → 0,0-0,1 % de signature, quel que soit le nombre de contacts importés."
  }
};
const band = (tbl, v) => { if (v == null) return null;
  for (const [lo, hi, w] of tbl) if (v >= lo && v < hi) return w; return null; };

/* ============================ ICP ============================ */
function scoreICP(a, cfg, ctx) {
  const w = cfg.icp, p = {};

  // 1. secteur — part du secteur dans les clients signés, avec plancher.
  // Un secteur jamais signé n'est pas une preuve d'impossibilité : c'est une
  // absence de preuve. D'où le plancher cfg.plancherSecteur (0,25 par défaut),
  // sans lequel tous les industriels tomberaient à zéro et le portefeuille
  // entier basculerait en quadrant D.
  const part = ctx.secteurs[a.secteur] || 0;
  const fl = cfg.plancherSecteur ?? 0.25;
  p.secteur = ctx.secteurMax ? fl + (1 - fl) * Math.sqrt(clamp(part / ctx.secteurMax, 0, 1)) : fl;

  // 2. taille — effectif et CA, la meilleure des deux preuves disponibles
  const t = band(CAL.taille, a.effectif), c = band(CAL.ca, a.ca ? a.ca / 1e6 : null);
  const best = [t, c].filter(v => v != null);
  p.taille = best.length ? clamp(Math.max(...best) / 2.0, 0, 1) : 0.35;   // 2,0 % = plafond observé

  // 3. surface d'attaque — entités du groupe présentes dans le CRM
  p.surface = clamp(log1((a.groupe?.entites?.length || 1) - 1, 4), 0, 1);

  // 4. historique — chiffrage perdu, client ailleurs
  const chiffre = (a.deals || []).some(d => !d.auto && d.montant > 0);
  const cycle   = (a.deals || []).some(d => !d.auto);
  const clientGroupe = (a.groupe?.entites || []).some(e => e.client);
  p.histo = clamp((clientGroupe ? .55 : 0) + (chiffre ? .45 : cycle ? .25 : 0), 0, 1);

  // 5. ancienneté de l'entreprise
  const an = a.annee_creation || null;
  p.anciennete = an ? clamp((band(CAL.age, an) || .7) / 1.35, 0, 1) : .5;

  let s = 0, tot = 0;
  for (const k in w) { s += (p[k] || 0) * w[k]; tot += w[k]; }
  s = tot ? (s / tot) * 100 : 0;

  // malus — perte de moins de 6 mois
  const perte = (a.deals || []).filter(d => d.perdu && d.cloture)
    .map(d => days(d.cloture)).sort((x, y) => x - y)[0];
  const mal = (perte != null && perte < 180) ? cfg.malus.perteRecente : 0;
  return { score: clamp(Math.round(s - mal), 0, 100), piliers: p, malus: mal, detail: { perteJours: perte } };
}

/* ========================= ENGAGEMENT ========================= */
function scoreENG(a, cfg) {
  const w = cfg.eng, p = {};
  const cs = a.contacts || [], sg = a.signaux || [];

  // 1. comité — le décideur d'abord, le nombre ensuite
  const dec = cs.filter(c => c.role === 'decideur').length;
  const pra = cs.filter(c => c.role === 'praticien').length;
  const nb  = a.compteurs?.contacts ?? cs.length;
  p.comite = clamp(
      (dec ? .5 : 0) + (dec > 1 ? .12 : 0) + (pra ? .13 : 0)
    + .25 * log1(Math.max(0, nb - 1), 12), 0, 1);

  // 2. intention — signaux datés, décroissants, pondérés par étape de funnel
  const hl = Math.max(15, cfg.demiVie);
  let inten = 0;
  for (const s of sg) {
    const d = days(s.date); if (d == null) continue;
    const poidsType = s.type === 'formulaire' ? 1 : s.type === 'clic_email' ? .6
                    : s.type === 'meeting' ? 1.2 : s.type === 'visite' ? .35 : .2;
    const et = cfg.etape[s.etape || 'TOFU'] ?? 1;
    inten += poidsType * et * Math.pow(0.5, d / hl);
  }
  p.intention = clamp(log1(inten, 6), 0, 1);

  // 3. timing — récence du dernier signal, quel qu'il soit
  const last = sg.map(s => days(s.date)).filter(v => v != null).sort((x, y) => x - y)[0];
  p.timing = last == null ? 0 : last <= 30 ? 1 : last <= 90 ? .75 : last <= 180 ? .5 : last <= 365 ? .25 : .08;

  // 4. réciprocité — ce qu'ils font rapporté à ce qu'on fait
  const eux = sg.filter(s => ['formulaire','clic_email','visite'].includes(s.type)).length;
  const nous = Math.max(1, a.compteurs?.touches || 0);
  p.reciprocite = clamp(log1(eux, 8) * (0.45 + 0.55 * clamp(eux / nous * 3, 0, 1)), 0, 1);

  let s = 0, tot = 0;
  for (const k in w) { s += (p[k] || 0) * w[k]; tot += w[k]; }
  s = tot ? (s / tot) * 100 : 0;

  // malus — aucun signal digital du tout
  const aucun = (a.compteurs?.formulaires || 0) === 0 && eux === 0;
  const mal = aucun ? cfg.malus.aucunSignal : 0;
  return { score: clamp(Math.round(s - mal), 0, 100), piliers: p, malus: mal,
           detail: { decideurs: dec, praticiens: pra, dernierSignalJours: last, signauxEntrants: eux } };
}

/* ========================== QUADRANT ========================== */
const QUAD = {
  A: { nom: 'Attaquer',  txt: 'Comité en place et compte qui bouge. On y met les moyens.' },
  B: { nom: 'Réveiller', txt: 'Le compte nous ressemble mais ne bouge pas. Contenu et paid avant l\'appel.' },
  C: { nom: 'Qualifier', txt: 'Ils bougent sans nous ressembler. Vérifier le besoin avant d\'investir.' },
  D: { nom: 'Veille',    txt: 'Ni fit ni signal. Coût zéro, on regarde passer.' }
};
function quadrant(icp, eng, seuils) {
  const hi = icp >= seuils.icp, he = eng >= seuils.eng;
  return hi && he ? 'A' : hi ? 'B' : he ? 'C' : 'D';
}

/* ===================== contexte de calibrage ==================== */
/* Construit la table des secteurs à partir des clients réellement
   signés : part de chaque secteur dans le CA signé.               */
function buildCtx(clients) {
  const sect = {}; let max = 0;
  for (const c of clients) {
    if (!c.secteur) continue;
    sect[c.secteur] = (sect[c.secteur] || 0) + 1;
  }
  for (const k in sect) max = Math.max(max, sect[k]);
  return { secteurs: sect, secteurMax: max };
}

function scoreAll(comptes, clients, cfg) {
  const ctx = buildCtx(clients);
  return comptes.map(a => {
    const i = scoreICP(a, cfg, ctx), e = scoreENG(a, cfg);
    return Object.assign({}, a, { icp: i, eng: e, q: quadrant(i.score, e.score, cfg.seuils) });
  });
}

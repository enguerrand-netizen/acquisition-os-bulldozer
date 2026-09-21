
/* ============================================================================
   LEVIERS — réécriture sur données réelles.
   Ces déclarations écrasent celles de la maquette (même nom, déclarées après).
   Règle : aucun budget, aucune campagne, aucune créative, aucun post n'est
   affiché s'il ne vient pas d'une source. Un levier sans source affiche ce
   qu'il faut brancher.
   ========================================================================== */
const CO = DATA.company;
const eur0 = n => fmtN(Math.round(n)) + ' €';
const pctS2 = (x, d = 2) => (100 * x).toFixed(d).replace('.', ',');
const nb = (n, s, p) => n + ' ' + (n > 1 ? (p || s + 's') : s);

/* Panneau « rien à mesurer » — dit le constat, puis ce qui manque. */
const notBranche = (titre, constat, manquant, comment) => `
  <div class="card nb"><header><div><h2>${titre}</h2><p>Aucune source exploitable au 21 septembre 2026</p></div></header>
    <div class="body" style="display:flex;flex-direction:column;gap:14px">
      <div class="nb-b"><b>Ce qu'on observe</b><p>${constat}</p></div>
      <div class="nb-b warn"><b>Ce qui manque</b><p>${manquant}</p></div>
      ${comment ? `<div class="nb-b"><b>Pour le brancher</b><p>${comment}</p></div>` : ''}
      <p class="nb-f">Cet écran restera vide tant que la source n'existe pas. Il n'affichera pas de chiffre plausible à la place.</p>
    </div></div>`;

const resBloc = (titre, arr) => !arr || !arr.length ? '' : `
  <div class="card"><header><div><h2>${titre}</h2><p>À faire voyager avec les chiffres ci-dessus</p></div></header>
    <div class="body"><ul class="res">${arr.map(r => `<li>${esc(r)}</li>`).join('')}</ul></div></div>`;

/* ---- pas de ventilation par créative et par compte : la régie ne la donne pas ---- */
function paidOf(){ return []; }

/* ---------------------------------------------------------------- leverRow */
function leverRow(k, a){
  const S = a.lv;
  if (k === 'content') {
    const c = a.signals.filter(s => s.st && CONTENT_T.includes(s.t)), c30 = c.filter(s => s.d <= 30);
    const hasB = c.some(s => s.st === 'bofu'), last = c[0];
    return { state: c30.length ? (hasB ? ['ok', 'BOFU atteint'] : ['warn', 'consomme, pas de BOFU'])
                   : c.length ? ['warn', 'rien depuis 30 j'] : ['crit', 'aucun contenu'],
             metric: nb(c.length, 'contenu') + ' · ' + c30.length + ' sur 30 j',
             detail: last ? fnPill(last.st) + ' ' + esc(last.det.slice(0, 60)) + ' · il y a ' + ago(last.d) : '—',
             next: hasB ? 'Proposer un échange sur le sujet consommé' : 'Pousser un contenu MOFU au comité' };
  }
  if (k === 'paid') {
    const e = a.crm.expoPub, g = a.crm.engPub;
    return { state: e ? (g ? ['ok', 'exposé · engagé'] : ['warn', 'exposé · sans réaction']) : ['crit', 'jamais exposé'],
             metric: e ? fmtN(e) + ' impressions · 90 j' : 'aucune impression',
             detail: e ? nb(g, 'engagement') + ' sur 90 jours (source : fiche CRM)' : 'ce compte n\'a vu aucune de nos publicités LinkedIn',
             next: e ? 'Retargeter les contacts exposés' : 'Ajouter le compte à une audience nominative' };
  }
  if (k === 'social') {
    return { state: ['mute', 'non branché'], metric: '—',
             detail: 'aucun post de la page Bulldozer n\'est stocké : accès à la page refusé',
             next: 'Ouvrir l\'accès administrateur à la page LinkedIn' };
  }
  if (k === 'outbound') {
    const O = S.outbound, l30 = O.log.filter(m => m.d <= 30);
    return { state: !O.sent ? ['crit', 'jamais contacté par e-mail']
                   : O.replied ? ['ok', nb(O.replied, 'réponse')]
                   : l30.length ? ['warn', 'en cours'] : ['mute', 'en sommeil'],
             metric: O.sent ? nb(O.sent, 'e-mail envoyé', 'e-mails envoyés') + ' · ' + l30.length + ' sur 30 j' : '—',
             detail: O.log[0] ? 'dernier : ' + esc((O.log[0].sujet || '(sans objet)').slice(0, 58)) + ' · il y a ' + ago(O.log[0].d) : 'aucun e-mail sortant tracé',
             next: O.mailsEntrants ? 'Passer la main au SDR' : 'Relancer le décideur identifié' };
  }
  if (k === 'sdr') {
    const D = S.sdr, conn = D.log.filter(x => x.out === 'conv').length;
    return { state: !D.log.length ? ['crit', 'jamais appelé']
                   : conn ? ['ok', nb(conn, 'conversation')]
                   : D.calls30 ? ['warn', 'appelé, pas de décroché'] : ['mute', 'pas appelé depuis ' + ago(D.last)],
             metric: D.log.length ? nb(D.log.length, 'appel') + ' · ' + conn + ' décroché' + (conn > 1 ? 's' : '') : '—',
             detail: D.log.length ? 'dernier il y a ' + ago(D.last) + ' · ' + esc(D.owner) : 'aucun appel tracé sur 24 mois',
             next: conn ? 'Caler le rendez-vous' : D.log.length ? 'Changer d\'interlocuteur' : 'Premier appel au décideur' };
  }
  const O = a.hist.open, sl = S.sales;
  const held = sl.meetings.filter(m => m.d >= 0 && m.out === 'tenu'), up = sl.meetings.filter(m => m.d < 0);
  return { state: O ? ['ok', 'opportunité ouverte'] : a.hist.loss ? ['crit', 'perdue il y a ' + ago(a.hist.loss.d)]
                 : held.length ? ['warn', 'rencontré, pas d\'opportunité'] : ['mute', 'jamais rencontré'],
           metric: held.length ? nb(held.length, 'rendez-vous tenu', 'rendez-vous tenus') : 'aucun rendez-vous',
           detail: O ? O.stage + (O.amt ? ' · ' + eur0(O.amt) : ' · montant non renseigné')
                 : a.hist.loss ? esc(a.hist.loss.label) + (a.hist.loss.amt ? ' · ' + eur0(a.hist.loss.amt) : '') : '—',
           next: up.length ? 'Rendez-vous à venir' : O ? 'Faire avancer l\'étape' : 'Provoquer un premier rendez-vous' };
}

/* ------------------------------------------------------------ leverCompany */
function leverCompany(k){
  const inPlan = accounts.filter(a => a.plan.has(k));
  let K = '', B = '';

  if (k === 'paid') {
    const L = CO.paid.linkedin, M = CO.paid.meta, X = CO.paid.exposition_comptes;
    const mois = {}; (L.par_mois || []).forEach(m => { mois[m.mois] = { label: m.mois.slice(5) + '/' + m.mois.slice(2, 4), li: m.depense_eur, me: 0 }; });
    (M.par_mois || []).forEach(m => { (mois[m.mois] = mois[m.mois] || { label: m.mois.slice(5) + '/' + m.mois.slice(2, 4), li: 0, me: 0 }).me = m.depense_eur; });
    const serie = Object.keys(mois).sort().slice(-12).map(x => mois[x]);
    const camps = (L.par_campagne || []).filter(c => c.depense_eur || c.impressions)
      .sort((x, y) => (y.depense_eur || 0) - (x.depense_eur || 0));
    const expoAcc = accounts.filter(a => a.crm.expoPub > 0);
    K = kpi('Dépense LinkedIn 2026', eur0(L.total.depense_eur), fmtK(L.total.impressions) + ' impressions · CTR ' + pctS2(L.total.ctr) + ' %')
      + kpi('Dépense Meta', eur0(M.total.depense_eur), fmtK(M.total.impressions) + ' impressions · CTR ' + pctS2(M.total.ctr) + ' %')
      + kpi('Comptes du plan exposés', `${expoAcc.length}<small>/ ${accounts.length}</small>`, X.engages_cibles + ' comptes cibles ont réagi', expoAcc.length < accounts.length / 2)
      + kpi('Pression hors portefeuille', X.part_hors_portefeuille + '<small> %</small>', X.exposes_toute_base + ' entreprises exposées dans la base, ' + X.exposes_portefeuille + ' ici', true);
    B = `<div class="card"><header><div><h2>Dépense par mois</h2><p>LinkedIn et Meta · compte publicitaire Bulldozer</p></div></header>
        <div class="body">${legendOf([['var(--c1)', 'LinkedIn'], ['var(--c2)', 'Meta']])}
        ${colChart(serie, ['li', 'me'], ['var(--c1)', 'var(--c2)'], ['LinkedIn', 'Meta'], { h: 240, w: Math.max(320, (V().clientWidth || 1100) - 80), fmt: fmtK, unit: ' €' })}</div></div>
      <div class="card"><header><div><h2>Campagnes LinkedIn</h2><p>${camps.length} campagnes avec des métriques sur ${L.campagnes_referencees || camps.length} référencées · 1er janvier au 20 septembre 2026</p></div></header>
        <div class="body tbox"><table style="min-width:760px"><thead><tr><th>Campagne</th><th>Statut</th><th>Objectif</th><th class="r">Dépense</th><th class="r">Impr.</th><th class="r">Clics</th><th class="r">CTR</th><th class="r">CPC</th></tr></thead><tbody>
        ${camps.map(c => `<tr><td><b>${esc(c.nom)}</b></td><td><span class="state ${c.statut === 'ACTIVE' ? 'ok' : 'mute'}">${c.statut === 'ACTIVE' ? 'active' : 'en pause'}</span></td>
          <td style="font-size:12px;color:var(--muted)">${esc((c.objectif || '—').replace(/_/g, ' ').toLowerCase())}</td>
          <td class="r">${c.depense_eur ? eur0(c.depense_eur) : '—'}</td><td class="r">${fmtN(c.impressions || 0)}</td><td class="r">${fmtN(c.clics || 0)}</td>
          <td class="r">${c.impressions ? pctS2((c.clics || 0) / c.impressions) + ' %' : '—'}</td><td class="r">${c.cpc_eur ? c.cpc_eur.toFixed(2).replace('.', ',') + ' €' : '—'}</td></tr>`).join('')}
        </tbody></table></div></div>
      <div class="card"><header><div><h2>Exposition des comptes du portefeuille</h2><p>Impressions vues par chaque compte sur 90 jours · source : fiche entreprise du CRM</p></div></header>
        <div class="body">${expoAcc.length ? hbars(expoAcc.sort((x, y) => y.crm.expoPub - x.crm.expoPub).map(a => ({
          label: a.name, value: a.crm.expoPub, max: Math.max(...expoAcc.map(x => x.crm.expoPub)),
          text: fmtN(a.crm.expoPub) + ' <small>' + a.crm.engPub + ' réactions</small>',
          color: a.crm.engPub ? 'var(--c2)' : 'var(--c1)' })))
          : '<p class="nb-f">Aucun des 30 comptes n\'a été exposé à une publicité LinkedIn sur les 90 derniers jours.</p>'}</div></div>`
      + resBloc('Réserves du levier Paid', CO.paid.reserves);
  }

  else if (k === 'content') {
    const L = DATA.lib, all = accounts.flatMap(a => a.signals.filter(x => x.st && CONTENT_T.includes(x.t)).map(x => ({ ...x, a })));
    const casse = L.contenus.filter(c => c.mort);
    const top = L.contenus.slice().sort((x, y) => y.n - x.n)[0];
    const totC = sum(L.contenus, c => c.n) + sum(L.hors_page, c => c.n);
    const totL = sum(L.lead_gen, c => c.n);
    const dt = d => d ? d.slice(8, 10) + '/' + d.slice(5, 7) + '/' + d.slice(2, 4) : '—';
    K = kpi('Contenus en ligne', L.contenus.length + L.hors_page.length, L.contenus.length + ' pages capturées le 21 septembre')
      + kpi('Conversions sur les contenus', fmtN(totC), 'contacts entrés par un contenu, comptés une fois')
      + kpi('Le plus performant', esc(top.t.split('—')[0].trim()), fmtN(top.n) + ' conversions depuis ' + dt(top.d1))
      + kpi('Landings cassées', casse.length, casse.length ? 'l\'URL que pointaient les campagnes renvoie un 404' : 'toutes les URL répondent', casse.length > 0);
    const carte = c => `<figure class="lbc${c.mort ? ' ko' : ''}">
        ${c.img ? `<a href="${esc(c.u)}" target="_blank" rel="noopener"><img src="${c.img}" alt="${esc(c.t)}" loading="lazy"></a>`
                : '<div class="lbc-no">page non capturée</div>'}
        <figcaption>
          <div class="lbc-h"><b>${esc(c.t)}</b><span class="state ${c.st === 'bofu' ? 'ok' : 'mute'}">${c.ty}</span></div>
          <div class="lbc-m">${fnPill(c.st)} <b>${fmtN(c.n)}</b> conversions · ${dt(c.d1)} → ${dt(c.d2)}</div>
          ${c.u ? `<a class="lbc-u" href="${esc(c.u)}" target="_blank" rel="noopener">${esc(c.u.replace(/^https?:\/\/(www\.)?/, '').slice(0, 58))}</a>` : ''}
          ${c.mort ? `<p class="lbc-ko">⚠ ${esc(c.note || '')}<br><span>${esc(c.mort.replace(/^https?:\/\/(www\.)?/, ''))}</span></p>` : ''}
          ${c.note && !c.mort ? `<p class="lbc-n">${esc(c.note)}</p>` : ''}
        </figcaption></figure>`;
    const AD = DATA.ads, M = AD.meta;
    const eurA = n => fmtN(Math.round(n)) + ' €';
    const adc = x => `<figure class="adc">
        <div class="adc-i"><img src="${x.img}" alt="" loading="lazy">${x.pf === 'Meta' ? '<span class="adc-pf">Meta</span>' : '<span class="adc-pf li">LinkedIn</span>'}</div>
        <figcaption>
          <b>${esc(x.nom)}</b>
          <div class="adc-c">${esc(x.campagne || '—')}${x.format ? ' · ' + esc(x.format.toLowerCase()) : ''}</div>
          <div class="adc-m"><span><b>${eurA(x.dep)}</b></span><span>${fmtK(x.imp)} impr.</span><span>${pctS2(x.ctr)} % CTR</span>${x.cpc ? `<span>${x.cpc.toFixed(2).replace('.', ',')} € CPC</span>` : ''}</div>
          ${x.corps ? `<p class="adc-t">${esc(x.corps.slice(0, 190))}${x.corps.length > 190 ? '…' : ''}</p>`
                    : `<p class="adc-t vide">Texte de l'annonce non importé dans l'OS${x.pf === 'LinkedIn' ? " — c\u2019est le cas de toutes les créatives LinkedIn" : ''}.</p>`}
          <div class="adc-f">${x.leadForm ? '<span class="state ok">formulaire Lead Gen</span>' : ''}${x.url ? `<a href="${esc(x.url)}" target="_blank" rel="noopener">${esc(x.url.replace(/^https?:\/\/(www\.)?/, '').slice(0, 42))}</a>` : ''}</div>
        </figcaption></figure>`;
    B = `<div class="card"><header><div><h2>Les annonces</h2><p>${M.acq} annonces d'acquisition diffusées en 2026 pour ${eurA(M.dep_acq)} · ${fmtK(M.imp_acq)} impressions · ${fmtN(M.clics_acq)} clics · les ${M.montrees} plus dépensières sont montrées, ${M.avec_visuel} ont un visuel récupérable</p></div></header>
        <div class="body"><div class="adgrid">${AD.annonces.map(adc).join('')}</div>
        <p class="nb-f" style="margin-top:14px">${M.tdt} autres annonces (${eurA(M.dep_tdt)}) sont des tests de traction montés pour des prospects, pas de l'acquisition Bulldozer : elles sont exclues de ce décompte.</p></div></div>
      ${resBloc('Ce que la régie ne rend pas', M.manques)}
      <div class="card"><header><div><h2>La bibliothèque</h2><p>Les contenus poussés sur LinkedIn et leurs landing pages · vignettes capturées le 21 septembre 2026 sur les pages en ligne</p></div></header>
        <div class="body"><div class="lbgrid">${L.contenus.slice().sort((x, y) => y.n - x.n).map(carte).join('')}</div></div></div>
      <div class="card"><header><div><h2>Contenus sans page à nous</h2><p>Formulaires hébergés ailleurs : rien à capturer</p></div></header>
        <div class="body tbox"><table><thead><tr><th>Contenu</th><th>Type</th><th>Étape</th><th class="r">Conversions</th><th class="r">Période</th></tr></thead><tbody>
        ${L.hors_page.slice().sort((x, y) => y.n - x.n).map(c => `<tr><td><b>${esc(c.t)}</b>${c.note ? `<div style="font-size:12px;color:var(--muted)">${esc(c.note)}</div>` : ''}</td>
          <td>${esc(c.ty)}</td><td>${fnPill(c.st)}</td><td class="r">${fmtN(c.n)}</td><td class="r" style="font-size:12px">${dt(c.d1)} → ${dt(c.d2)}</td></tr>`).join('')}
        </tbody></table></div></div>
      <div class="card"><header><div><h2>Formulaires Lead Gen LinkedIn</h2><p>L'autre moitié de la bibliothèque : le formulaire est dans la publicité, il n'y a pas de page à voir · ${fmtN(totL)} conversions au total</p></div></header>
        <div class="body tbox"><table><thead><tr><th>Formulaire</th><th class="r">Conversions</th><th class="r">Période</th><th>Poids dans le total</th></tr></thead><tbody>
        ${L.lead_gen.map(c => `<tr><td><b>${esc(c.t)}</b></td><td class="r">${fmtN(c.n)}</td><td class="r" style="font-size:12px">${dt(c.d1)} → ${dt(c.d2)}</td>
          <td><div class="t" style="height:8px;background:var(--mute-bg);border-radius:2px"><i style="display:block;height:100%;width:${(c.n / totL * 100).toFixed(1)}%;background:var(--c1);outline:1px solid rgba(0,0,0,.35);outline-offset:-1px;border-radius:2px"></i></div></td></tr>`).join('')}
        </tbody></table></div></div>
      <div class="card"><header><div><h2>Ce que consomment les 30 comptes</h2><p>Sur les ${fmtN(all.length)} signaux de contenu du portefeuille · 12 mois glissants</p></div></header>
        <div class="body">${hbars(Object.entries(all.reduce((o, x) => { const l = SIG[x.t].l; o[l] = (o[l] || 0) + 1; return o; }, {})).sort((x, y) => y[1] - x[1])
          .map(([l, n]) => ({ label: l, value: n, max: all.length, text: fmtN(n) })))}</div></div>`
      + resBloc('Réserves du levier Content', [L.methode].concat(CO.content.reserves || []));
  }

  else if (k === 'social') {
    K = kpi('Posts de la page', '—', 'aucun post de la page Bulldozer stocké')
      + kpi('Profils suivis', '2', 'deux profils de personnes, pas la page')
      + kpi('Comptes du plan', inPlan.length, 'attendraient ce levier')
      + kpi('Interactions attribuables', '0', 'aucune interaction rattachable à un compte');
    B = notBranche('Social — non branché',
      esc(CO.social.constat),
      esc(CO.social.manquant),
      'Une fois la page ouverte, cet écran montrera les posts, leurs réactions, et surtout quels contacts de vos 30 comptes ont réagi — c\'est cette jointure qui manque aujourd\'hui.');
  }

  else if (k === 'outbound') {
    const log = accounts.flatMap(a => a.lv.outbound.log.map(m => ({ ...m, a })));
    const l30 = log.filter(m => m.d <= 30);
    const wk = weekLabels().map(l => ({ label: l, v: 0 }));
    log.forEach(m => { const w = Math.floor(m.d / 7); if (w < 12) wk[11 - w].v++; });
    const rep = sum(accounts, a => a.lv.outbound.mailsEntrants);
    const owners = {}; log.forEach(m => { if (m.owner) owners[m.owner] = (owners[m.owner] || 0) + 1; });
    const touche = accounts.filter(a => a.lv.outbound.sent > 0);
    K = kpi('E-mails sortants', fmtN(log.length), l30.length + ' sur 30 jours · 24 mois relevés')
      + kpi('E-mails entrants', fmtN(rep), 'reçus de ces comptes — le CRM ne dit pas lesquels répondent à un envoi')
      + kpi('Comptes touchés', `${touche.length}<small>/ ${accounts.length}</small>`, accounts.length - touche.length + ' n\'ont jamais reçu d\'e-mail', touche.length < accounts.length * 0.7)
      + kpi('Séquences Lemlist', fmtN(CO.outbound.campagnes_total), 'aucune en cours, aucun volume lisible', true);
    B = `<div class="card"><header><div><h2>E-mails sortants par semaine</h2><p>Objets EMAIL du CRM · 12 semaines</p></div></header>
        <div class="body">${colChart(wk, ['v'], ['var(--navy)'], ['E-mails'], { h: 220, w: Math.max(320, (V().clientWidth || 1100) - 80), fmt: fmtN, unit: ' e-mails' })}</div></div>
      <div class="card"><header><div><h2>Qui écrit</h2><p>Propriétaire de l'e-mail sortant · 24 mois</p></div></header>
        <div class="body">${hbars(Object.entries(owners).sort((x, y) => y[1] - x[1]).map(([o, n]) => ({ label: o, value: n, max: Math.max(...Object.values(owners)), text: fmtN(n) })))}</div></div>`
      + notBranche('Séquences Lemlist — non branché', esc(CO.outbound.constat), esc(CO.outbound.manquant),
          'Les e-mails ci-dessus viennent du CRM, pas de Lemlist : on voit ce qui est parti, pas les ouvertures ni les taux par étape de séquence.');
  }

  else if (k === 'sdr') {
    const log = accounts.flatMap(a => a.lv.sdr.log.map(x => ({ ...x, a })));
    const conn = log.filter(x => x.out === 'conv'), nr = log.filter(x => x.out === 'nr'), vm = log.filter(x => x.out === 'vm');
    const wk = weekLabels().map(l => ({ label: l, v: 0 })); log.forEach(x => { const w = Math.floor(x.d / 7); if (w < 12) wk[11 - w].v++; });
    const owners = {}; log.forEach(x => { if (x.owner) owners[x.owner] = (owners[x.owner] || 0) + 1; });
    const jamais = accounts.filter(a => !a.lv.sdr.log.length);
    K = kpi('Appels passés', fmtN(log.length), log.filter(x => x.d <= 30).length + ' sur 30 jours · 24 mois relevés')
      + kpi('Taux de décroché', pct(conn.length, log.length) + '<small> %</small>', conn.length + ' conversations sur ' + log.length + ' appels')
      + kpi('Comptes jamais appelés', `${jamais.length}<small>/ ${accounts.length}</small>`, jamais.length ? jamais.slice(0, 3).map(a => a.name).join(', ') + (jamais.length > 3 ? '…' : '') : '—', jamais.length > 5)
      + kpi('Sans réponse', fmtN(nr.length), vm.length + ' messageries · ' + pct(nr.length, log.length) + ' % des appels');
    B = `<div class="card"><header><div><h2>Appels par semaine</h2><p>Objets CALL du CRM · 12 semaines</p></div></header>
        <div class="body">${colChart(wk, ['v'], ['var(--navy)'], ['Appels'], { h: 220, w: Math.max(320, (V().clientWidth || 1100) - 80), fmt: fmtN, unit: ' appels' })}</div></div>
      <div class="g2"><div class="card"><header><div><h2>Résultat des appels</h2><p>24 mois · résultat saisi dans le CRM</p></div></header>
        <div class="body">${hbars([['conv', 'Conversation'], ['nr', 'Sans réponse'], ['vm', 'Messagerie'], ['bar', 'Barrage / mauvais numéro'], ['call', 'Résultat non saisi']].map(([o, l], i) => {
          const n = log.filter(x => x.out === o).length;
          return { label: l, value: n, max: log.length || 1, text: n + ' <small>' + pct(n, log.length) + ' %</small>', color: o === 'conv' ? 'var(--ok)' : o === 'call' ? 'var(--line-2)' : 'var(--navy-3)' }; }))}</div></div>
      <div class="card"><header><div><h2>Qui appelle</h2><p>Propriétaire de l'appel · 24 mois</p></div></header>
        <div class="body">${hbars(Object.entries(owners).sort((x, y) => y[1] - x[1]).map(([o, n]) => ({ label: o, value: n, max: Math.max(...Object.values(owners)), text: fmtN(n) })))}</div></div></div>`
      + resBloc('Réserve du levier SDR', ['Le CRM ne stocke pas l\'heure de l\'appel, seulement la date : aucune analyse par créneau horaire n\'est possible.',
          'La durée d\'appel n\'est pas renseignée non plus.',
          'Les messages LinkedIn, SMS et WhatsApp sont bloqués par le connecteur : le volume de prospection réel est supérieur à ce qui est affiché ici.']);
  }

  else {
    const M = accounts.flatMap(a => a.lv.sales.meetings.map(m => ({ ...m, a })));
    const cal = M.filter(m => m.d >= 0 && m.type !== 'AUTRE'), tenus = cal.filter(m => m.out === 'tenu');
    const autres = M.filter(m => m.type === 'AUTRE'), avenir = M.filter(m => m.d < 0);
    const opps = accounts.filter(a => a.hist.open), perdus = accounts.filter(a => a.hist.loss);
    const chiffres = perdus.filter(a => a.hist.loss.amt);
    const wk = weekLabels().map(l => ({ label: l, v: 0 })); M.forEach(m => { const w = Math.floor(m.d / 7); if (m.d >= 0 && w < 12) wk[11 - w].v++; });
    K = kpi('Rendez-vous au calendrier', fmtN(cal.length), tenus.length + ' avec un résultat saisi · ' + (cal.length - tenus.length) + ' sans résultat au CRM')
      + kpi('Opportunités ouvertes', opps.length, opps.filter(a => !a.hist.open.amt).length + ' sans montant renseigné', opps.filter(a => !a.hist.open.amt).length > 0)
      + kpi('Chiffrages perdus', chiffres.length, eur0(sum(chiffres, a => a.hist.loss.amt)) + ' cumulés')
      + kpi('Comptes jamais rencontrés', accounts.filter(a => !a.lv.sales.meetings.filter(m => m.type !== 'AUTRE').length).length, autres.length + ' réunions écartées : comités de mission, restitutions, événements');
    B = `<div class="card"><header><div><h2>Rendez-vous par semaine</h2><p>Objets MEETING du CRM · 12 semaines</p></div></header>
        <div class="body">${colChart(wk, ['v'], ['var(--navy)'], ['Rendez-vous'], { h: 220, w: Math.max(320, (V().clientWidth || 1100) - 80), fmt: fmtN, unit: ' RDV' })}</div></div>
      <div class="card"><header><div><h2>Toutes les transactions du portefeuille</h2><p>Hors transactions créées automatiquement par les formulaires Lead Gen</p></div></header>
        <div class="body tbox"><table style="min-width:720px"><thead><tr><th>Compte</th><th>Transaction</th><th>Étape</th><th class="r">Montant</th><th class="r">Créée</th><th class="r">Clôturée</th><th>Propriétaire</th></tr></thead><tbody>
        ${accounts.flatMap(a => a.deals.filter(d => !d.auto).map(d => ({ d, a }))).sort((x, y) => (y.d.montant || 0) - (x.d.montant || 0))
          .map(({ d, a }) => `<tr class="click" data-lvacc="${a.id}"><td><b>${esc(a.name)}</b></td><td>${esc(d.nom || '')}</td>
          <td><span class="state ${/WON/i.test(d.etape) ? 'ok' : /DEAD|Standby|No Show/i.test(d.etape) ? 'crit' : 'warn'}">${esc(d.etape || '')}</span></td>
          <td class="r">${d.montant ? eur0(d.montant) : '<span class="state mute">non renseigné</span>'}</td>
          <td class="r" style="font-size:12px">${esc((d.cree || '').slice(0, 10))}</td><td class="r" style="font-size:12px">${esc((d.cloture || '').slice(0, 10)) || '—'}</td>
          <td style="font-size:12px">${esc(d.owner || '—')}</td></tr>`).join('')}
        </tbody></table></div></div>`
      + resBloc('Réserves du levier Sales', CO.pipeline.reserves);
  }
  return `<div class="kpis">${K}</div>${B}${suiviHTML(k)}`;
}

/* Avertissement vérifié en tête de fiche, quand la fiche CRM est trompeuse. */
const alerteHTML = a => !a.alerte ? '' :
  `<div class="card"><div class="body"><div class="nb-b warn"><b>${a.alerte[0] === 'mission' ? 'Attention — mission en cours' : 'Attention — fiche peu fiable'}</b><p>${esc(a.alerte[1])}</p></div></div></div>`;

/* --------------------------------------------------------- leverAccount */
function leverAccount(k, a){
  const head = alerteHTML(a) + accHead(k, a);
  let K = '', B = '';
  const vide = (t, p) => `<div class="card"><header><div><h2>${t}</h2></div></header><div class="body"><p class="nb-f">${p}</p></div></div>`;

  if (k === 'content') {
    const c = a.signals.filter(s => s.st && CONTENT_T.includes(s.t));
    K = kpi('Contenus consommés', c.length, c.filter(s => s.d <= 30).length + ' sur 30 jours')
      + kpi('Étape la plus profonde', c.some(s => s.st === 'bofu') ? 'BOFU' : c.some(s => s.st === 'mofu') ? 'MOFU' : c.length ? 'TOFU' : '—', 'atteinte sur 12 mois')
      + kpi('Contacts concernés', new Set(c.map(s => s.who).filter(Boolean)).size, 'sur ' + a.contacts.filter(x => x.prov !== 'hors').length + ' au comité')
      + kpi('Dernier signal', c[0] ? 'il y a ' + ago(c[0].d) : '—', c[0] ? esc(c[0].det.slice(0, 44)) : 'aucun');
    B = c.length ? `<div class="card"><header><div><h2>Journal des contenus</h2><p>Du plus récent au plus ancien · 12 mois</p></div></header>
      <div class="body tbox"><table style="min-width:640px"><thead><tr><th>Il y a</th><th>Contact</th><th>Type</th><th>Étape</th><th>Libellé du formulaire</th></tr></thead><tbody>
      ${c.map(s => { const ct = s.who ? ctOf(a, s.who) : null; return `<tr><td style="white-space:nowrap">${ago(s.d)}</td><td>${ct ? ctLine(ct) : '<span class="state mute">compte</span>'}</td>
        <td>${esc(SIG[s.t].l)}</td><td>${fnPill(s.st)}</td><td style="font-size:12.5px">${esc(s.det)}</td></tr>`; }).join('')}
      </tbody></table></div></div>` : vide('Journal des contenus', 'Ce compte n\'a rempli aucun formulaire sur les 12 derniers mois.');
  }

  else if (k === 'paid') {
    K = kpi('Impressions · 90 j', a.crm.expoPub ? fmtN(a.crm.expoPub) : '0', 'vues par les contacts de ce compte')
      + kpi('Réactions · 90 j', a.crm.engPub || 0, a.crm.expoPub ? 'sur ' + fmtN(a.crm.expoPub) + ' impressions' : 'aucune exposition')
      + kpi('Signaux publicitaires', a.signals.filter(s => s.t === 'lgf' || s.t === 'ad').length, 'formulaires Lead Gen remplis · 12 mois')
      + kpi('Quadrant', a.q + ' · ' + QUADS[a.q].l, QUADS[a.q].s);
    B = notBranche('Détail par campagne — indisponible pour un compte',
      a.crm.expoPub ? 'La fiche CRM indique ' + fmtN(a.crm.expoPub) + ' impressions et ' + (a.crm.engPub || 0) + ' réactions sur 90 jours pour ce compte.'
                    : 'La fiche CRM n\'indique aucune impression sur les 90 derniers jours pour ce compte.',
      'La régie ne rend l\'exposition qu\'au niveau du compte et sur 90 jours glissants : ni la ventilation par campagne, ni par créative, ni par semaine ne sont disponibles par entreprise.',
      'La vue entreprise du levier Paid donne le détail réel par campagne, tous comptes confondus.');
  }

  else if (k === 'social') {
    K = kpi('Interactions', '—', 'non mesurable par compte')
      + kpi('Abonnés LinkedIn', a.contacts.filter(c => c.abonneLI).length, 'contacts de ce compte abonnés à la page')
      + kpi('Comité', a.contacts.filter(c => c.prov !== 'hors').length, 'contacts actifs')
      + kpi('Décideurs', a.contacts.filter(c => c.role === 'dec' && c.prov !== 'hors').length, 'à toucher en organique');
    B = notBranche('Social — non branché', esc(CO.social.constat), esc(CO.social.manquant),
      'L\'abonnement LinkedIn est la seule trace exploitable, et il n\'est pas daté : on sait qui suit la page, pas depuis quand ni ce qu\'il a vu.');
  }

  else if (k === 'outbound') {
    const O = a.lv.outbound;
    K = kpi('E-mails envoyés', O.sent, O.log.filter(m => m.d <= 30).length + ' sur 30 jours')
      + kpi('E-mails entrants', O.mailsEntrants, 'reçus de ce compte, pas forcément des réponses')
      + kpi('Dernier envoi', O.log[0] ? 'il y a ' + ago(O.log[0].d) : '—', O.log[0] ? esc(O.log[0].owner || '') : 'jamais contacté par e-mail')
      + kpi('Comité joignable', a.contacts.filter(c => c.prov !== 'hors').length, a.crm.sansEmail ? a.crm.sansEmail + ' contacts sans adresse' : 'tous avec une adresse');
    B = O.log.length ? `<div class="card"><header><div><h2>E-mails sortants</h2><p>Objets EMAIL du CRM · du plus récent au plus ancien</p></div></header>
      <div class="body tbox"><table style="min-width:640px"><thead><tr><th>Il y a</th><th>Objet</th><th>Envoyé par</th></tr></thead><tbody>
      ${O.log.slice(0, 40).map(m => `<tr><td style="white-space:nowrap">${ago(m.d)}</td><td style="font-size:12.5px">${esc((m.sujet || '(sans objet)').slice(0, 90))}</td><td style="font-size:12.5px">${esc(m.owner || '—')}</td></tr>`).join('')}
      </tbody></table></div></div>` : vide('E-mails sortants', 'Aucun e-mail sortant tracé sur ce compte en 24 mois.');
  }

  else if (k === 'sdr') {
    const D = a.lv.sdr, conn = D.log.filter(x => x.out === 'conv');
    K = kpi('Appels passés', D.log.length, D.log.filter(x => x.d <= 30).length + ' sur 30 jours')
      + kpi('Décrochés', conn.length, D.log.length ? pct(conn.length, D.log.length) + ' % des appels' : '—')
      + kpi('Dernier appel', D.last == null ? 'jamais' : 'il y a ' + ago(D.last), esc(D.owner))
      + kpi('Décideurs au comité', a.contacts.filter(c => c.role === 'dec' && c.prov !== 'hors').length, 'cibles prioritaires');
    B = D.log.length ? `<div class="card"><header><div><h2>Journal d'appels</h2><p>Objets CALL du CRM · du plus récent au plus ancien</p></div></header>
      <div class="body tbox"><table style="min-width:560px"><thead><tr><th>Il y a</th><th>Résultat</th><th>Par</th></tr></thead><tbody>
      ${D.log.slice(0, 40).map(x => `<tr><td style="white-space:nowrap">${ago(x.d)}</td>
        <td><span class="state ${x.out === 'conv' ? 'ok' : x.out === 'call' ? 'mute' : 'warn'}">${CALL_OUT[x.out] ? CALL_OUT[x.out][0] : 'non saisi'}</span></td>
        <td style="font-size:12.5px">${esc(x.owner || '—')}</td></tr>`).join('')}
      </tbody></table></div>
      <div class="body"><p class="nb-f">Le CRM ne stocke ni l'heure ni la durée de l'appel : impossible de dire à quel créneau ce compte décroche.</p></div></div>`
      : vide('Journal d\'appels', 'Ce compte n\'a jamais été appelé en 24 mois.');
  }

  else {
    const S = a.lv.sales, tenus = S.meetings.filter(m => m.d >= 0 && m.out === 'tenu' && m.type !== 'AUTRE');
    K = kpi('Rendez-vous', S.meetings.filter(m => m.type !== 'AUTRE').length, tenus.length + ' avec un résultat saisi · ' + S.meetings.filter(m => m.type === 'AUTRE').length + ' réunions hors vente')
      + kpi('Transactions', a.deals.filter(d => !d.auto).length, a.crm.dealsAuto ? a.crm.dealsAuto + ' créées automatiquement, exclues' : 'aucune création automatique')
      + kpi('Statut', STATUS[a.status].l, a.hist.loss ? 'perdue il y a ' + ago(a.hist.loss.d) : a.hist.open ? a.hist.open.stage : '—')
      + kpi('Chiffrage connu', a.hist.loss && a.hist.loss.amt ? eur0(a.hist.loss.amt) : a.hist.open && a.hist.open.amt ? eur0(a.hist.open.amt) : '—', 'montant accepté en interne');
    B = (a.deals.filter(d => !d.auto).length ? `<div class="card"><header><div><h2>Transactions</h2></div></header><div class="body tbox">
      <table style="min-width:620px"><thead><tr><th>Transaction</th><th>Étape</th><th class="r">Montant</th><th class="r">Créée</th><th class="r">Clôturée</th></tr></thead><tbody>
      ${a.deals.filter(d => !d.auto).map(d => `<tr><td><b>${esc(d.nom || '')}</b></td><td><span class="state ${/DEAD|Standby|No Show/i.test(d.etape) ? 'crit' : /WON/i.test(d.etape) ? 'ok' : 'warn'}">${esc(d.etape || '')}</span></td>
        <td class="r">${d.montant ? eur0(d.montant) : '<span class="state mute">non renseigné</span>'}</td><td class="r" style="font-size:12px">${esc((d.cree || '').slice(0, 10))}</td>
        <td class="r" style="font-size:12px">${esc((d.cloture || '').slice(0, 10)) || '—'}</td></tr>`).join('')}</tbody></table></div></div>` : vide('Transactions', 'Aucune transaction sur ce compte.'))
      + (S.meetings.length ? `<div class="card"><header><div><h2>Rendez-vous</h2><p>Objets MEETING du CRM</p></div></header><div class="body tbox">
      <table style="min-width:560px"><thead><tr><th>Il y a</th><th>Objet</th><th>Avec</th></tr></thead><tbody>
      ${S.meetings.map(m => `<tr><td style="white-space:nowrap">${m.d < 0 ? 'dans ' + ago(-m.d) : ago(m.d)}</td><td style="font-size:12.5px">${esc((m.sujet || '(sans objet)').slice(0, 80))}</td><td style="font-size:12.5px">${esc(m.ae)}</td></tr>`).join('')}
      </tbody></table></div></div>` : vide('Rendez-vous', 'Aucun rendez-vous tracé sur ce compte.'));
  }
  return head + `<div class="kpis">${K}</div>` + B;
}

/* ------------------------------------------------------------------ AGENTS
   La maquette affichait une flotte d'agents en marche : actions exécutées,
   file de validation, journal. Aucun agent n'a jamais tourné ici. L'écran
   devient donc un CATALOGUE : ce que chaque agent ferait, ce qu'il lui faut
   pour tourner, et si cette source existe aujourd'hui. Zéro compteur inventé. */
const AGENT_SRC = {
  content:  { etat: 'ok',      src: 'Formulaires et signaux du CRM', manque: null },
  paid:     { etat: 'partiel', src: 'Régie LinkedIn via l\'OS, exposition par compte dans le CRM',
              manque: 'La régie ne rend pas la ventilation par créative et par compte : couper une créa sur un critère par compte n\'est pas mesurable aujourd\'hui.' },
  social:   { etat: 'non',     src: null,
              manque: 'Aucun post de la page Bulldozer n\'est stocké : l\'accès administrateur à la page est refusé.' },
  outbound: { etat: 'partiel', src: 'E-mails sortants et entrants du CRM',
              manque: 'Lemlist ne rend aucun volume : ouvertures, clics et taux par étape de séquence sont invisibles.' },
  sdr:      { etat: 'ok',      src: 'Appels du CRM avec leur résultat', manque: 'Ni heure ni durée d\'appel : pas de recommandation de créneau.' },
  sales:    { etat: 'ok',      src: 'Rendez-vous et transactions du CRM',
              manque: 'Le montant manque sur la plupart des transactions ouvertes du portail.' },
  crm:      { etat: 'ok',      src: 'Contacts, entreprises et associations du CRM',
              manque: 'Les messages LinkedIn, SMS et WhatsApp sont bloqués par le connecteur.' }
};
const AG_LBL = { ok: ['ok', 'câblable aujourd\'hui'], partiel: ['warn', 'câblable en partie'], non: ['crit', 'source manquante'] };

function renderAgents(){
  const ks = Object.keys(AGENTS);
  const nT = ks.reduce((n, k) => n + (AGENT_TASKS[k] || []).length, 0);
  const cab = ks.filter(k => AGENT_SRC[k].etat === 'ok').length;
  const nonC = ks.filter(k => AGENT_SRC[k].etat === 'non').length;
  const sel = ui.agentSel && AGENTS[ui.agentSel] ? ui.agentSel : 'content';
  const S = AGENT_SRC[sel], T = AGENT_TASKS[sel] || [];

  V().innerHTML = `
    <div class="kpis">
      ${kpi('Agents décrits', ks.length, nT + ' tâches unitaires au catalogue')}
      ${kpi('Câblables aujourd\'hui', `${cab}<small>/ ${ks.length}</small>`, 'leur source existe déjà dans le CRM ou l\'OS')}
      ${kpi('En attente d\'une source', nonC + ks.filter(k => AGENT_SRC[k].etat === 'partiel').length, nonC + ' complètement bloqués', true)}
      ${kpi('Actions exécutées', '0', 'aucun agent n\'a encore été mis en marche')}
    </div>
    <div class="card"><header><div><h2>Ce que chaque agent ferait</h2><p>Catalogue, pas état de marche : rien n'est branché en écriture et aucune action n'a été exécutée.</p></div></header>
      <div class="body tbox"><table style="min-width:720px"><thead><tr><th>Agent</th><th>Tâches</th><th>État</th><th>Source</th><th>Ce qui bloque</th></tr></thead><tbody>
      ${ks.map(k => { const A = AGENTS[k], s = AGENT_SRC[k], [cls, lbl] = AG_LBL[s.etat];
        return `<tr class="click" data-ag="${k}"${k === sel ? ' style="background:var(--card-2)"' : ''}>
          <td><b>${esc(A.l)}</b><div style="font-size:12px;color:var(--muted);max-width:340px">${esc(A.does)}</div></td>
          <td class="r">${(AGENT_TASKS[k] || []).length}</td>
          <td><span class="state ${cls}">${lbl}</span></td>
          <td style="font-size:12.5px">${s.src ? esc(s.src) : '<span class="state mute">aucune</span>'}</td>
          <td style="font-size:12.5px;max-width:320px;color:var(--muted)">${s.manque ? esc(s.manque) : '—'}</td></tr>`; }).join('')}
      </tbody></table></div></div>
    <div class="card"><header><div><h2>${esc(AGENTS[sel].l)} · les tâches en détail</h2><p>${esc(AGENTS[sel].does)}</p></div></header>
      <div class="body" style="display:flex;flex-direction:column;gap:12px">
        ${T.map(t => `<div class="nb-b"><b>${esc(t.l)}</b>
          <p>${esc(t.d)}</p>
          <p style="font-size:12.5px;color:var(--muted);margin-top:6px"><b style="display:inline;text-transform:none;letter-spacing:0;font-size:12.5px">Déclencheur :</b> ${esc(t.trig)}
          ${(t.p || []).length ? ' · <b style="display:inline;text-transform:none;letter-spacing:0;font-size:12.5px">Réglages :</b> ' + t.p.map(p => esc(p.l) + ' = ' + esc(String(p.v)) + (p.u ? ' ' + esc(p.u) : '')).join(' · ') : ''}</p></div>`).join('')}
        <p class="nb-f">Ces réglages décrivent le comportement souhaité. Tant qu'aucun agent n'est mis en marche, ils ne produisent rien : l'outil est en lecture seule sur le CRM.</p>
      </div></div>`;
  V().querySelectorAll('[data-ag]').forEach(r => r.onclick = () => { ui.agentSel = r.dataset.ag; const y = window.scrollY; renderAgents(); window.scrollTo(0, y); });
}

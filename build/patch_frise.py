# -*- coding: utf-8 -*-
"""Passe 11 — frise mensuelle et pistes par contact, comme sur Signal d'intention.
Chaque ligne de compte porte sa frise ; on la déplie pour voir une piste par
contact et un point par touchpoint, sur un axe de temps continu."""
import pathlib, sys
P = pathlib.Path("app.src.html"); s = P.read_text(encoding="utf-8"); n = 0
def sub(old, new, label, count=1):
    global s, n
    if old not in s: print("  ÉCHEC  ", label); sys.exit(1)
    s = s.replace(old, new, count); n += 1; print("  ok     ", label)

JS = r"""
/* ============================ FRISES =====================================
   Reprise de la grammaire de « Signal d'intention » : une frise mensuelle par
   compte, et au dépliement une piste par contact avec un point par touchpoint.
   Le canal donne la couleur, le poids du signal donne le diamètre.
   ======================================================================== */
const CANAL_SIG = { lgf: 'pub', ad: 'pub', form: 'site', dl: 'site', webinar: 'site', pricing: 'site',
                    wbr_in: 'site', wbr_go: 'site', page: 'site', click: 'mail', open: 'mail', reply: 'mail' };
const CANAL_COL = { pub: 'var(--c1)', site: 'var(--c2)', mail: 'var(--c3)', ext: 'var(--c4)' };
const FENETRE = 340;   /* jours couverts par les signaux */

/* Frise mensuelle compacte : 12 barres empilées par canal. */
function frise(a, w, h){
  w = w || 132; h = h || 26;
  const m = Array.from({ length: 12 }, () => ({ pub: 0, site: 0, mail: 0, ext: 0 }));
  a.signals.forEach(x => { const i = 11 - Math.floor(x.d / 28.3); if (i >= 0 && i < 12) m[i][CANAL_SIG[x.t] || 'site']++; });
  const max = Math.max(1, ...m.map(c => c.pub + c.site + c.mail + c.ext));
  const bw = w / 12;
  let out = '';
  m.forEach((c, i) => {
    let y = h;
    ['pub', 'site', 'mail', 'ext'].forEach(k => {
      if (!c[k]) return;
      const bh = (c[k] / max) * (h - 2); y -= bh;
      out += `<rect x="${(i * bw + .6).toFixed(1)}" y="${y.toFixed(1)}" width="${(bw - 1.2).toFixed(1)}" height="${bh.toFixed(1)}" fill="${CANAL_COL[k]}" stroke="rgba(0,0,0,.35)" stroke-width=".4"/>`;
    });
  });
  const tot = a.signals.length;
  return `<svg class="frz" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" role="img" aria-label="${tot} signaux sur 12 mois"><title>${tot} signal${tot > 1 ? 'ux' : ''} sur 12 mois · le mois le plus chargé : ${max}</title>${out}</svg>`;
}

/* Pistes par contact : un point par touchpoint, placé à sa date. */
function pistes(a){
  const sig = a.signals.filter(x => x.d <= FENETRE);
  if (!sig.length) return `<div class="pst-vide">Aucun signal entrant daté sur douze mois. Les ${a.crm.contactsAssocies} contacts de ce compte sont au CRM, mais rien ne vient d'eux.</div>`;
  const par = {};
  sig.forEach(x => { const k = x.who || '_'; (par[k] = par[k] || []).push(x); });
  const ordre = Object.keys(par).sort((x, y) => par[y].length - par[x].length);
  const pos = d => ((FENETRE - d) / FENETRE * 100);
  /* repères de mois */
  const now = TODAY, mois = [];
  for (let i = 11; i >= 0; i--) {
    const dt = new Date(now.getFullYear(), now.getMonth() - i, 1);
    const jours = Math.round((now - dt) / DAY);
    if (jours <= FENETRE) mois.push({ l: dt.toLocaleDateString('fr-FR', { month: 'short' }), an: dt.getFullYear(), x: pos(jours) });
  }
  const dt0 = m => (m.l.indexOf('janv') === 0 ? ' ' + String(m.an).slice(2) : '');
  const axe = mois.map(m => `<span class="pst-m" style="left:${m.x.toFixed(2)}%">${m.l.replace('.','')}${dt0(m)}</span>`).join('')
            + mois.map(m => `<i class="pst-g" style="left:${m.x.toFixed(2)}%"></i>`).join('');
  const lane = k => {
    const c = k === '_' ? null : ctOf(a, k), L = par[k];
    const pts = L.slice().sort((x, y) => y.d - x.d).map(x => {
      const w = sigW(x, cfg.eng), r = Math.max(3, Math.min(9, 3 + w * .45));
      return `<i class="pst-p" style="left:${pos(x.d).toFixed(2)}%;width:${r}px;height:${r}px;background:${CANAL_COL[CANAL_SIG[x.t] || 'site']}"
        title="${esc(SIG[x.t].l)} · ${fmtDate(x.d)}${x.st ? ' · ' + x.st.toUpperCase() : ''} — ${esc(x.det.slice(0, 90))}"></i>`;
    }).join('');
    return `<div class="pst-l">
      <div class="pst-n">${c ? `<b>${esc(c.name)}</b><span>${esc(c.title || (c.role === 'dec' ? 'décideur' : c.role === 'champ' ? 'praticien' : 'fonction inconnue'))}</span>`
                            : '<b>Signaux du compte</b><span>sans contact rattaché</span>'}</div>
      <div class="pst-t">${axe}${pts}</div></div>`;
  };
  const sansContact = par['_'] ? par['_'].length : 0;
  return `<div class="pst">${ordre.map(lane).join('')}
    <p class="pst-f">${sig.length} touchpoint${sig.length > 1 ? 's' : ''} sur ${ordre.filter(k => k !== '_').length} contact${ordre.length > 2 ? 's' : ''}
    ${sansContact ? ` · ${sansContact} sans contact rattaché au CRM` : ''} · diamètre = poids du signal dans le score · survolez un point pour le détail.</p></div>`;
}
"""
sub("/* ---------------------------------------------------------------- leverRow */", JS + "\n/* ---------------------------------------------------------------- leverRow */", "fonctions frise et pistes")

# colonne Frise dans l'en-tête
sub("<th>Compte</th><th>Quadrant</th>", "<th>Compte</th><th>Frise 12 mois</th><th>Quadrant</th>", "en-tête de colonne")
# cellule + chevron de dépliement
sub("""<td>${pinBtn(a)}</td><td class="rank">${i + 1}</td>""",
    """<td>${pinBtn(a)}</td><td class="rank"><button class="xpd" data-xp="${a.id}" aria-expanded="${ui.xp === a.id}" title="Déplier les pistes par contact">${i + 1}<i></i></button></td>""",
    "chevron de dépliement")
sub("""</div></div></td>
        <td>${qPill(a.q, true)}</td>""",
    """</div></div></td>
        <td class="frzc">${frise(a)}</td>
        <td>${qPill(a.q, true)}</td>""", "cellule frise")

# état de dépliement
sub("cp: 30, cpTab: 'dash', agentSel: 'paid', agentTab: 'tasks',",
    "cp: 30, cpTab: 'dash', agentSel: 'paid', agentTab: 'tasks', xp: null,", "état xp")

# ligne dépliée juste après la ligne de compte
sub("""</tr>`).join('') : `<tr><td colspan=""", """</tr>${ui.xp === a.id ? `<tr class="xprow"><td colspan="10">${pistes(a)}</td></tr>` : ''}`).join('') : `<tr><td colspan=""", "ligne dépliée")

# clic sur le chevron : déplier sans ouvrir la fiche
sub("""  el.querySelectorAll('[data-f]').forEach""",
    """  el.querySelectorAll('[data-xp]').forEach(b => b.onclick = e => {
    e.stopPropagation();
    ui.xp = ui.xp === b.dataset.xp ? null : b.dataset.xp;
    const y = window.scrollY; renderCockpit(); window.scrollTo(0, y);
  });
  el.querySelectorAll('[data-f]').forEach""", "clic du chevron")

# la ligne dépliée ne doit pas ouvrir la fiche
sub("""<th title="Mes comptes en cours">★</th><th>#</th>""", """<th title="Mes comptes en cours">★</th><th title="Cliquez le numéro pour déplier les pistes">#</th>""", "info-bulle du numéro")

# styles
s = s.replace("</style>", """
.xpd{background:none;border:0;padding:0;font:inherit;color:inherit;display:inline-flex;align-items:center;gap:5px;cursor:pointer}
.xpd i{width:0;height:0;border-left:4px solid transparent;border-right:4px solid transparent;border-top:5px solid var(--faint);transition:transform .12s}
.xpd[aria-expanded="true"] i{transform:rotate(180deg);border-top-color:var(--text)}
.frzc{width:150px}
svg.frz{display:block}
tr.xprow > td{background:var(--card-2);padding:0}
/* la cellule dépliée fait la largeur du tableau (qui défile) : on ancre le
   panneau à gauche pour qu'il reste lisible sans défiler horizontalement */
.pst{padding:14px 16px 12px;position:sticky;left:0;width:min(100%,calc(100vw - var(--side) - 78px));box-sizing:border-box}
.pst-l{display:flex;align-items:center;gap:14px;min-height:34px;border-top:1px solid var(--line)}
.pst-l:first-child{border-top:0}
.pst-n{width:210px;flex:none;min-width:0;padding:5px 0}
.pst-n b{display:block;font:600 12.5px/1.25 var(--f-display);color:var(--text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.pst-n span{display:block;font-size:11px;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.pst-t{position:relative;flex:1;height:30px;min-width:0}
.pst-g{position:absolute;top:0;bottom:0;width:1px;background:var(--line);transform:translateX(-.5px)}
.pst-p{position:absolute;top:50%;transform:translate(-50%,-50%);border-radius:50%;border:1px solid rgba(0,0,0,.35);cursor:help}
.pst-m{position:absolute;top:-13px;font:400 9.5px var(--f-mono);color:var(--faint);transform:translateX(-50%);letter-spacing:.04em;white-space:nowrap}
.pst-l:not(:first-child) .pst-m{display:none}
.pst-l:first-child .pst-t{margin-top:12px}
.pst-f{margin:10px 0 0;font-size:12px;color:var(--muted)}
.pst-vide{padding:16px;font-size:13px;color:var(--muted)}
@media(max-width:900px){.pst-n{width:130px}}
</style>""", 1)
n += 1; print("  ok      styles des pistes")

P.write_text(s, encoding="utf-8"); print(f"\n{n} injections")

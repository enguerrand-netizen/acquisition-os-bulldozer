# -*- coding: utf-8 -*-
"""Passe 4 — corrections d'honnêteté : ne rien afficher qu'on ne mesure pas."""
import pathlib, sys
P = pathlib.Path("app.src.html"); s = P.read_text(encoding="utf-8"); n = 0
def sub(old, new, label):
    global s, n
    if old not in s: print("  ÉCHEC  ", label); sys.exit(1)
    s = s.replace(old, new, 1); n += 1; print("  ok     ", label)

# ---------- 1. exercice fiscal : aucune source, on le dit ----------
sub("const FY_LABEL = m => MONTH_FULL[m] + ' → ' + MONTH_FULL[(m + 11) % 12];",
    "const FY_LABEL = m => m == null ? 'non renseigné' : MONTH_FULL[m] + ' → ' + MONTH_FULL[(m + 11) % 12];", "FY_LABEL")
sub("const fyPhase = (a, I) => { const to = monthsTo(a.fyStart), since = (12 - to) % 12;",
    "/* Le mois de début d'exercice n'existe nulle part dans le CRM. Tant qu'il n'est pas\n   saisi, le pilier ne rapporte rien et l'écran affiche « non renseigné ». */\nconst fyPhase = (a, I) => { if (a.fyStart == null) return { k: 'na', l: 'non renseigné dans le CRM' };\n  const to = monthsTo(a.fyStart), since = (12 - to) % 12;", "fyPhase null")
sub("""<td style="font-size:12.5px;white-space:nowrap">${MONTH_FULL[a.fyStart]}<br><span class="state ${a.I.fy.k === 'prep' ? 'ok' : a.I.fy.k === 'start' ? 'warn' : 'mute'}">${a.I.fy.k === 'prep' ? 'budget en prépa.' : a.I.fy.k === 'start' ? 'exercice démarré' : 'hors période'}</span></td>""",
    """<td style="font-size:12.5px;white-space:nowrap">${a.crm.dernierContact == null ? '<span class="state mute">jamais</span>' : 'il y a ' + ago(a.crm.dernierContact)}<br><span class="state ${a.crm.dernierContact != null && a.crm.dernierContact <= 30 ? 'ok' : a.crm.dernierContact != null && a.crm.dernierContact <= 120 ? 'warn' : 'mute'}">${a.crm.touches} touche${a.crm.touches > 1 ? 's' : ''} au total</span></td>""",
    "colonne exercice -> dernier contact")
sub(">Exercice fiscal<", ">Dernier contact<", "en-tête de colonne")
sub("['fy','Budget en préparation',fyPrep],", "", "filtre budget retiré")
sub("""${kpi('Comptes à attaquer', `${qN('A')}<small>/ ${accounts.length}</small>`, fyPrep + ' comptes avec un budget en préparation', true)}""",
    """${kpi('Comptes à attaquer', `${qN('A')}<small>/ ${accounts.length}</small>`, accounts.filter(a => a.crm.dernierContact != null && a.crm.dernierContact <= 30).length + ' comptes touchés sur 30 j', true)}""",
    "KPI comptes à attaquer")

# ---------- 2. RDV : rendez-vous réels, source attribuée au dernier contact ----------
sub("const RDV_SRC = { sdr: 'SDR', out: 'Outbound', in: 'Inbound site', paid: 'Paid (LGF)' };",
    "const RDV_SRC = { sdr: 'SDR (appel)', out: 'Outbound (e-mail)', in: 'Inbound (formulaire)', paid: 'Paid (Lead Gen)', nc: 'Non attribué' };",
    "RDV_SRC")
sub("""['sdr','out','in','paid'], ['var(--c1)','var(--c2)','var(--c3)','var(--c4)']""",
    """['sdr','out','in','paid','nc'], ['var(--c1)','var(--c2)','var(--c3)','var(--c4)','var(--line-2)']""", "clés du graphique RDV")
sub("""function rdvEvents(){
  const ev = [];
  accounts.forEach(a => {
    a.lv.sdr.log.forEach(x => { if (x.out === 'rdv') ev.push({ d: x.d, src: 'sdr', a }); });
    if (a.lv.outbound.meeting) { const m = a.lv.outbound.log.find(m => m.replied); if (m) ev.push({ d: m.d, src: 'out', a }); }
    const f = a.signals.filter(s => s.t === 'form' && s.det === 'Demande de démo'); if (f.length) ev.push({ d: f[f.length - 1].d, src: 'in', a });
    const l = a.signals.filter(s => s.t === 'lgf' && s.det === 'LGF — Demande de démo'); if (l.length) ev.push({ d: l[l.length - 1].d, src: 'paid', a });
  });
  return ev;
}""",
"""/* Un RDV est un meeting réellement tenu, relevé dans le CRM.
   Sa source est le dernier geste dans les 14 jours qui l'ont précédé : un appel
   (SDR), un e-mail sortant (outbound), un formulaire Lead Gen (paid) ou un autre
   formulaire (inbound). Sans rien dans la fenêtre, le RDV reste « non attribué »
   plutôt que d'être rattaché arbitrairement. Les comités de mission, restitutions,
   kick-offs et événements sont exclus : ce ne sont pas des rendez-vous commerciaux. */
const RDV_WINDOW = 14;
function rdvEvents(){
  const ev = [];
  accounts.forEach(a => {
    a.lv.sales.meetings.forEach(m => {
      if (m.d < 0 || m.out === 'noshow' || m.type === 'AUTRE') return;
      const av = x => x.d >= m.d && x.d <= m.d + RDV_WINDOW;
      const cand = [];
      a.lv.sdr.log.forEach(x => { if (av(x)) cand.push({ d: x.d, src: 'sdr' }); });
      a.lv.outbound.log.forEach(x => { if (av(x)) cand.push({ d: x.d, src: 'out' }); });
      a.signals.forEach(x => { if (av(x) && (x.t === 'lgf' || x.t === 'form' || x.t === 'pricing' || x.t === 'dl' || x.t === 'reply'))
        cand.push({ d: x.d, src: x.t === 'lgf' ? 'paid' : 'in' }); });
      cand.sort((x, y) => x.d - y.d);
      ev.push({ d: m.d, src: cand.length ? cand[0].src : 'nc', a, m });
    });
  });
  return ev;
}""", "rdvEvents sur meetings réels")

# ---------- 3. pipe : dire que le montant manque au lieu d'afficher 0 € ----------
sub("""const opps = accounts.filter(a => a.hist.open), pipe = sum(opps, a => a.hist.open.amt);""",
    """const opps = accounts.filter(a => a.hist.open), pipe = sum(opps, a => a.hist.open.amt);
  /* 280 des 321 transactions ouvertes du portail n'ont aucun montant : un pipe
     à 0 € ne veut pas dire « pas d'affaires », il veut dire « pas chiffrées ». */
  const oppsSansMontant = opps.filter(a => !a.hist.open.amt).length;""", "pipe sans montant")

P.write_text(s, encoding="utf-8"); print(f"\n{n} corrections")

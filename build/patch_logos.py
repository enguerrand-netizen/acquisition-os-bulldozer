# -*- coding: utf-8 -*-
"""Passe 10 — logos des comptes cibles.
Récupérés à la source (voir logos_embed.json pour le niveau et l'URL d'origine).
Société Générale ne publie aucune icône exploitable : pastille typographique,
signalée comme telle. Aucun logo n'est recréé ni généré."""
import json, pathlib, sys, re
P = pathlib.Path("app.src.html"); s = P.read_text(encoding="utf-8"); n = 0
D = pathlib.Path("/private/tmp/claude-501/-Users-enguerrandchalvondemersay/a75e6ca6-5ff8-478d-bd1a-9a963b0419f5/scratchpad/acq/data")
def sub(old, new, label, count=1):
    global s, n
    if old not in s: print("  ÉCHEC  ", label); sys.exit(1)
    s = s.replace(old, new, count); n += 1; print("  ok     ", label)

LOG = json.load(open(D / "logos_embed.json"))
sub("const DATA = ", "const LOGOS = " + json.dumps(LOG, ensure_ascii=False, separators=(",", ":")) + ";\nconst DATA = ", "LOGOS injectés")

# helper : pastille logo, repli typographique si la marque n'en publie pas
sub("const ctOf = (a, id) =>",
    """/* Pastille logo. Un logo sous 64 px est affiché à sa taille native plutôt
   qu'agrandi : une icône de 16 px étirée à 34 px est illisible. */
const logoOf = (a, px) => {
  const L = LOGOS.logos[a.crmId], s = px || 34;
  if (!L) return `<span class="lgo lgo-txt" style="width:${s}px;height:${s}px;font-size:${Math.round(s * .38)}px" title="${esc(a.name)} — aucun logo publié par la marque">${esc((a.name || '?').replace(/[^A-Za-zÀ-ÿ]/g, ' ').trim().split(/\\s+/).slice(0, 2).map(w => w[0]).join('').toUpperCase())}</span>`;
  const w = Math.min(s - 6, L.px < 64 ? L.px : s - 6);
  return `<span class="lgo" style="width:${s}px;height:${s}px" title="${esc(a.name)} · logo ${L.niveau} (${L.px} px)"><img src="${L.d}" alt="" style="max-width:${w}px;max-height:${w}px"></span>`;
};
const ctOf = (a, id) =>""", "helper logoOf")

# tableau « tous les comptes » du cockpit
sub("""<td class="acc"><b>${esc(a.name)}</b><span>${a.sector} · ${fmtN(a.size)} pers.</span></td>""",
    """<td class="acc"><div class="accl">${logoOf(a)}<div><b>${esc(a.name)}</b><span>${a.sector} · ${fmtN(a.size)} pers.</span></div></div></td>""",
    "logo dans le tableau des comptes")

# tableau « suivi compte par compte » des leviers
sub("""<td class="acc"><b>${esc(a.name)}</b><span>${a.sector} · ${STATUS[a.status].l}""",
    """<td class="acc"><div class="accl">${logoOf(a, 30)}<div><b>${esc(a.name)}</b><span>${a.sector} · ${STATUS[a.status].l}""",
    "logo dans le suivi par compte")
sub("""${a.plan.has(k) ? '' : ' · hors plan'}</span></td>""",
    """${a.plan.has(k) ? '' : ' · hors plan'}</span></div></div></td>""", "fermeture du suivi")

# en-tête de la vue compte d'un levier
sub("""<div style="flex:1;min-width:220px"><div class="eyebrow">${LEVERS[k].l} · vue compte</div>""",
    """${logoOf(a, 52)}<div style="flex:1;min-width:220px"><div class="eyebrow">${LEVERS[k].l} · vue compte</div>""",
    "logo dans l'en-tête de levier")

# en-tête de la fiche compte
sub("""      <div class="eyebrow">${idx >= 0 ? idx + 1 + '\u1d49 sur ' + order.length + ' · ' : ''}${esc(a.domain)}</div>
      <h2 style="margin-top:6px">${esc(a.name)}</h2>""",
    """      <div class="accsheet">${logoOf(a, 58)}<div>
      <div class="eyebrow">${idx >= 0 ? idx + 1 + '\u1d49 sur ' + order.length + ' · ' : ''}${esc(a.domain)}</div>
      <h2 style="margin-top:6px">${esc(a.name)}</h2></div></div>""", "logo dans la fiche compte")

# styles
s = s.replace("</style>", """
.lgo{display:inline-flex;align-items:center;justify-content:center;flex:none;background:var(--surface);border:1px solid var(--line);border-radius:var(--r-s);overflow:hidden}
.lgo img{display:block;object-fit:contain}
.lgo-txt{font-family:var(--f-display);font-weight:700;color:var(--muted);background:var(--card-2);letter-spacing:.02em}
.accl{display:flex;align-items:center;gap:10px}
.accl > div{min-width:0}
.accsheet{display:flex;align-items:center;gap:14px}
.accsheet > div{min-width:0}
</style>""", 1)
n += 1; print("  ok      styles des pastilles")

P.write_text(s, encoding="utf-8"); print(f"\n{n} injections de logos")

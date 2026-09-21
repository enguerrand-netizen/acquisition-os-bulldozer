# -*- coding: utf-8 -*-
"""Passe 7 — corrections issues de l'audit de code.
Chaque substitution échoue bruyamment : un patch muet est passé inaperçu une fois."""
import pathlib, sys, re
P = pathlib.Path("app.src.html"); s = P.read_text(encoding="utf-8"); n = 0
def sub(old, new, label):
    global s, n
    if old not in s: print("  ÉCHEC  ", label); sys.exit(1)
    s = s.replace(old, new, 1); n += 1; print("  ok     ", label)

# 1. scoreICP — le chiffrage déjà accepté et les entités du groupe (patch perdu au rejeu)
sub("""  if (I.hist[a.status]) lines.push({ l: 'Historique : ' + STATUS[a.status].l.toLowerCase(), v: I.hist[a.status] });
  if (a.entities.length > 1) lines.push({ l: 'Plusieurs entités (groupe + filiale)', v: I.multi });""",
"""  /* Un chiffrage déjà accepté en interne pèse plus que le statut seul : on retient
     le meilleur des deux et on dit lequel. */
  const chiffre = !!(a.hist.loss && a.hist.loss.amt) || !!(a.hist.open && a.hist.open.amt);
  const vSt = I.hist[a.status] || 0, vCh = chiffre ? (I.hist.chiffre || 0) : 0;
  if (vSt || vCh) lines.push(vCh > vSt
    ? { l: 'Chiffrage déjà accepté en interne (' + fmtE((a.hist.loss || a.hist.open).amt) + ')', v: vCh }
    : { l: 'Historique : ' + STATUS[a.status].l.toLowerCase(), v: vSt });
  /* Surface d'attaque : chaque entité du groupe présente au CRM est une porte.
     Plafonnée à trois fois le poids pour qu'un grand groupe n'écrase pas le score. */
  if (a.entities.length > 1) lines.push({
    l: a.entities.length + ' entités du groupe au CRM' + (a.entities.filter(e => e.client).length ? ' — dont ' + a.entities.filter(e => e.client).length + ' cliente(s)' : ''),
    v: Math.min(I.multi * 3, I.multi * (a.entities.length - 1)) });""", "scoreICP · chiffrage et entités")

# 2. pilier Timing — la maquette le calculait sur des signaux externes (prise de poste,
#    recrutement, actualité) qu'aucune source ne fournit : il valait 0 pour les 30 comptes
#    et plafonnait l'engagement à 80/100 sans le dire. Il devient la récence du dernier signal.
sub("""  const job = a.signals.some(s => s.t === 'job' && s.d <= 90), ev = a.signals.some(s => (s.t === 'hiring' || s.t === 'news') && s.d <= 60);
  const timing = clamp((job ? E.timing.job : 0) + (ev ? E.timing.event : 0), 0, 100);
  if (job) lines.timing.push({ l: 'Prise de poste < 90 j', v: E.timing.job });
  if (ev) lines.timing.push({ l: 'Recrutement / actualité < 60 j', v: E.timing.event });""",
"""  /* Récence du dernier signal entrant. Les déclencheurs externes de la maquette
     (prise de poste, recrutement, actualité) n'ont aucune source ici : les garder
     aurait laissé ce pilier à zéro pour les 30 comptes, soit 20 points inatteignables. */
  const last = a.signals.length ? Math.min.apply(null, a.signals.map(s => s.d)) : null;
  const timing = last == null ? 0 : last <= 14 ? 100 : last <= 30 ? 85 : last <= 90 ? 60 : last <= 180 ? 35 : last <= 365 ? 15 : 5;
  lines.timing.push(last == null
    ? { l: 'Aucun signal entrant', v: 0 }
    : { l: 'Dernier signal il y a ' + ago(last), v: timing });""", "pilier Timing sur la récence")

# 3. plus aucune personne inventée : les propriétaires viennent des activités du CRM
sub("const SDRS = ['Léa Marchetti','Hugo Delaunay','Inès Barrault','Karim Othmani'];",
    "const SDRS = [];   /* rempli depuis les propriétaires réels des appels */", "SDRS vidé")
sub("const AES = ['Julien Castaing','Claire Vautrin','Mathieu Roblin'];",
    "const AES = [];    /* rempli depuis les propriétaires réels des rendez-vous */", "AES vidé")

# 4. un appel sans résultat n'est pas un rappel demandé
sub("call: ['Rappel demandé','ok']", "call: ['Résultat non saisi','mute']", "CALL_OUT.call")

# 5. l'accroche par défaut affirmait une exposition publicitaire pour n'importe quel signal
sub("""  else hook = `Exposé à nos campagnes depuis ${ago(a.signals[a.signals.length - 1].d)} : envoyer le cas client ${a.sector} le plus proche.`;""",
"""  else if (a.crm && a.crm.expoPub) hook = `Exposé à nos publicités LinkedIn (${fmtN(a.crm.expoPub)} impressions sur 90 j) : envoyer le cas client ${a.sector} le plus proche.`;
  else if (a.signals.length) hook = `Dernier signe de vie il y a ${ago(a.signals[0].d)} (${SIG[a.signals[0].t].l.toLowerCase()}) : reprendre là-dessus, pas sur une offre générique.`;
  else hook = `Aucun signal entrant : rien à quoi raccrocher une accroche, il faut créer l'exposition avant d'appeler.`;""",
    "accroche par défaut")

P.write_text(s, encoding="utf-8"); print(f"\n{n} corrections d'audit")

# ---- suite : propriétaires réels, tiroir d'import, filtres ----
s = P.read_text(encoding="utf-8"); n2 = 0
def sub2(old, new, label):
    global s, n2
    if old not in s: print("  ÉCHEC  ", label); sys.exit(1)
    s = s.replace(old, new, 1); n2 += 1; print("  ok     ", label)

# les listes de propriétaires viennent des activités réellement tracées
sub2("  const owners = k === 'sdr' ? SDRS : k === 'sales' ? AES : null;",
     """  /* Propriétaires réels, lus sur les appels et les rendez-vous du CRM. */
  const owners = k === 'sdr' ? [...new Set(accounts.flatMap(a => a.lv.sdr.log.map(x => x.owner)).filter(Boolean))].sort()
               : k === 'sales' ? [...new Set(accounts.flatMap(a => a.lv.sales.meetings.map(m => m.ae)).filter(x => x && x !== '—'))].sort()
               : k === 'outbound' ? [...new Set(accounts.flatMap(a => a.lv.outbound.log.map(x => x.owner)).filter(Boolean))].sort()
               : null;""", "filtres propriétaires réels")

# le tiroir d'import ne chargeait rien : le portefeuille vient du CRM
sub2("document.getElementById('openImport').onclick = () => { ui.drawer = true; go('cockpit'); };",
     """document.getElementById('openImport').onclick = () => toast("Le portefeuille est lu dans HubSpot, pas collé ici : pour ajouter un compte, passez-le en cible dans le CRM et relancez l'extraction.");""",
     "tiroir d'import désactivé")

P.write_text(s, encoding="utf-8"); print(f"{n2} corrections supplémentaires")

# ---- suite 2 : le Moteur affichait encore les exemples de contenus de la maquette ----
s = P.read_text(encoding="utf-8"); n3 = 0
def sub3(old, new, label, count=1):
    global s, n3
    if old not in s: print("  ÉCHEC  ", label); sys.exit(1)
    s = s.replace(old, new, count); n3 += 1; print("  ok     ", label)

# les listes d'exemples de SIG sont du contenu inventé : on les vide, les vrais
# libellés viennent des formulaires réellement remplis et sont déjà affichés
# dans l'écran Content.
s2 = re.sub(r", d: \[\[[^\]]*\](?:, *\[[^\]]*\])*\] \}", " }", s)
s2 = re.sub(r", d: \['[^\]]*'\] \}", " }", s2)
if s2 != s: s = s2; n3 += 1; print("  ok      exemples de contenus de la maquette retirés")

# le pilier Timing ne mesure plus des déclencheurs externes
sub3("'eng.w.timing', 'Timing', 'déclencheurs externes'", "'eng.w.timing', 'Timing', 'récence du dernier signal'", "libellé du pilier Timing")
# le bloc « exercice fiscal » du barème n'a aucune source
sub3("Un compte dont l'exercice démarre bientôt prépare son budget : c'est le moment d'y entrer.",
     "Le mois de début d'exercice n'existe nulle part dans le CRM : ce pilier est réglé à zéro et ne rapporte rien. Les réglages restent visibles pour le jour où l'information sera saisie.",
     "note du bloc exercice")

# la tâche de retargeting citait une page /tarifs qui n'existe pas sur le site
sub3("d: 'Ajoute au retargeting les comptes qui ont visité la page tarifs.', trig: 'Visite de /tarifs'",
     "d: 'Ajoute au retargeting les comptes dont un contact a rempli un formulaire de prise de contact.', trig: 'Signal BOFU — demande de rendez-vous'",
     "tâche de retargeting")
P.write_text(s, encoding="utf-8"); print("%d corrections Moteur" % n3)

# ---- suite 3 : vider les référentiels de la maquette restés en code mort ----
s = P.read_text(encoding="utf-8"); n4 = 0
# Ces tableaux (campagnes, créatives, contenus, posts, séquences, chapitres de la
# proposition commerciale) ne sont plus appelés — les surcharges les ont remplacés.
# Mais ils contiennent des libellés inventés. On les vide en gardant le nom lié,
# pour qu'aucun appel résiduel ne lève d'exception.
VIDE = {"ASSETS": "[]", "LIB": "[]", "CREAS": "[]", "POSTS": "[]", "SEQS": "[]",
        "CAMPS": "[]", "CHAPTERS": "[]", "EMAIL_TYPES": "[]",
        "CAMP_DEF": "{}", "CAMPQ": "{}", "CREA_IMG_OFF": "{}"}
for nom, vide in VIDE.items():
    m = re.search(r"\nconst " + nom + r" = .*?;\n(?=const |function |/\*|\n)", s, re.S)
    if not m:
        m = re.search(r"\nconst " + nom + r" = [\s\S]*?\n\];\n", s) or re.search(r"\nconst " + nom + r" = [\s\S]*?\n\};\n", s)
    if m:
        s = s[:m.start()] + "\nconst " + nom + " = " + vide + ";   /* référentiel de la maquette, vidé : contenu inventé */\n" + s[m.end():]
        n4 += 1; print("  ok      %s vidé" % nom)
    else:
        print("  (absent) %s" % nom)
P.write_text(s, encoding="utf-8"); print("%d référentiels vidés" % n4)

# ---- suite 4 : neutraliser les fonctions mortes qui portent encore du contenu inventé ----
s = P.read_text(encoding="utf-8"); n5 = 0
# lpHTML / roiHTML / tplHTML / mixHTML fabriquaient de fausses landing pages et un
# calculateur de ROI ; taskItems fabriquait des propositions d'agents. Plus rien ne
# les appelle depuis la réécriture des leviers et de l'écran Agents. On remplace
# leur corps : les identifiants restent liés, le contenu inventé disparaît.
MORTES = {"lpHTML": "''", "roiHTML": "''", "tplHTML": "''", "taskItems": "[]"}
for nom, ret in MORTES.items():
    m = re.search(r"\nfunction " + nom + r"\(([^)]*)\)\{", s)
    if not m: print("  (absent) %s" % nom); continue
    i = m.end() - 1; depth = 0
    for j in range(i, len(s)):
        if s[j] == "{": depth += 1
        elif s[j] == "}":
            depth -= 1
            if depth == 0: break
    s = s[:m.start()] + "\nfunction %s(%s){ return %s; }   /* corps retiré : contenu de maquette */\n" % (nom, m.group(1), ret) + s[j + 1:]
    n5 += 1; print("  ok      %s neutralisée" % nom)
# la modale « bibliothèque » n'a plus de bibliothèque à ouvrir
s = s.replace("function bindLibrary(el){", "function bindLibrary(el){ return;   /* bibliothèque de la maquette retirée */\n", 1)
n5 += 1; print("  ok      bindLibrary neutralisée")
# dernier reste : la modale d'aperçu d'un contenu de la maquette
m = re.search(r"\n\s*if \(t === 'tool'\) return openModal\([^\n]*\n", s)
if m:
    s = s[:m.start()] + "\n" + s[m.end():]
    n5 += 1; print("  ok      modale d'aperçu retirée")
P.write_text(s, encoding="utf-8"); print("%d fonctions neutralisées" % n5)

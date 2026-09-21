# -*- coding: utf-8 -*-
"""CRM réel -> contrat Account de l'application « Acquisition OS ».
Source : dossiers30.json (contacts joints par identifiant d'entreprise, donc
exhaustifs), comptes.json, groupes30.json, secteurs.json.
Règle unique : rien n'est inventé. Un champ sans source vaut None ou une liste
vide, et l'écran affiche ce qu'il manque."""
import json, pathlib, datetime, re
from collections import defaultdict, Counter

D = pathlib.Path("/private/tmp/claude-501/-Users-enguerrandchalvondemersay/a75e6ca6-5ff8-478d-bd1a-9a963b0419f5/scratchpad/acq/data")
TODAY = datetime.date(2026, 9, 21)
jload = lambda n: json.load(open(D/n)) if (D/n).exists() else None
def jours(v):
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", str(v or ""))
    return (TODAY - datetime.date(*map(int, m.groups()))).days if m else None

SEC = jload("secteurs.json"); CURE = SEC["cure"]
GRP = jload("groupes30.json"); CPT = {str(c["hs_object_id"]): c for c in jload("comptes.json")}
DOS = (jload("dossiers30.json") or {}).get("comptes", {})
assert len(DOS) == 30, f"dossiers30 incomplet : {len(DOS)} comptes"

# --- signal entrant -> type applicatif + étape de funnel ---
# Les webinars ne sont tracés nulle part dans HubSpot au 21/09/2026 : ni formulaire,
# ni objet « événement marketing » (0 enregistrement), ni propriété contact. Les deux
# types sont néanmoins câblés ici pour s'allumer le jour où la source arrive.
SOUS = {"webinar_inscrit": ("wbr_in", "mofu"), "webinar_participant": ("wbr_go", "mofu"),
        "typeform": ("pricing", "bofu"), "livre_blanc": ("form", "mofu"),
        "barometre": ("form", "mofu"), "ressource": ("dl", "mofu"),
        "autre_contenu": ("form", "mofu"), "webinar": ("webinar", "mofu"),
        "lead_gen_linkedin": ("lgf", "tofu")}
ROLE = {"decideur": "dec", "praticien": "champ", "achat": "champ",
        "technique": "ope", "autre": "ope", "inconnu": "ope"}
CALL_OUT = {"Connected": "conv", "No answer": "nr", "Left voicemail": "vm",
            "Busy": "bar", "Wrong number": "bar"}
MORTS = {"closedlost", "555624160", "555471297", "3924524269", "1577902267", "1291729115"}
GAGNES = {"closedwon", "401531322", "2472791261", "555543744"}
STAGE_OPEN = {"appointmentscheduled": "Découverte", "qualifiedtobuy": "Découverte",
              "3779831023": "Démo faite", "3606921430": "Démo faite",
              "decisionmakerboughtin": "Proposition envoyée", "4151951583": "Négociation",
              "1610207445": "Négociation", "5557824735": "Négociation"}
CANAL = {"ad": "pub", "lgf": "pub", "form": "site", "page": "site", "pricing": "site",
         "dl": "site", "webinar": "site", "click": "mail", "open": "mail", "reply": "mail"}

# Le nom du CRM est parfois bas de casse, tronqué ou faux. On affiche un nom
# propre et on garde le nom d'origine, visible sur la fiche compte.
NOMS = {
 "229193587951": "L'Oréal", "315914050757": "Contentsquare",
 "18938276038": "Saint-Gobain Distribution Bâtiment France",
 "17818953714": "Keolis", "19976068547": "Veolia Énergie Performance",
 "59663610043": "KPMG France", "87436872902": "Pierre Fabre",
 "316281684204": "ESSCA", "36322852030": "Société Générale",
 "148704214225": "Alpine (Renault)", "175301965003": "Capgemini Invent",
 "14624157398": "Martell Mumm Perrier-Jouët (Pernod Ricard)",
 "317411495156": "MGEN (groupe VYV)", "315014441197": "Docaposte (La Poste)",
}
NOTE_NOM = {"316281684204": "fiche nommée « Rothschild & Co » au CRM — il s'agit en réalité de l'ESSCA"}
# Avertissements vérifiés, affichés en tête de fiche.
ALERTE = {
 "19976068547": ("mission", "Mission en cours, pas un prospect : comités stratégiques mensuels réservés jusqu'en mars 2027 et kick-off de mission au calendrier, malgré un cycle de vie « lead » au CRM."),
 "316281684204": ("fiche", "Fiche peu fiable : elle porte le nom « Rothschild & Co » mais tous les contacts sont en @essca.eu / @essca.fr, et ce sont des adresses d'anciens élèves rattachées à 18 employeurs différents. Ce n'est pas un compte au sens commercial."),
}
accounts, prov, manquant = [], {"comptes": {}}, Counter()

for i, d in DOS.items():
    c = CPT[i]; secteur, orig_sec, justif = CURE[i]; g = GRP.get(i, {})
    ent = d.get("entreprise", {}); ver = d.get("verification", {})

    # ---------- comité ----------
    contacts, cmap = [], {}
    for k, ct in enumerate(d.get("contacts", [])):
        cid = "c%d" % k; ctid = str(ct.get("id"))
        titre = (ct.get("intitule_poste") or "").strip()
        actif = bool(titre or ct.get("date_dernier_formulaire") or ct.get("date_dernier_clic_email")
                     or ct.get("date_dernier_contact") or ct.get("nb_visites"))
        fn = (ct.get("prenom") or "").strip(); ln = (ct.get("nom") or "").strip()
        contacts.append(dict(id=cid, fn=fn, ln=ln, name=(fn + " " + ln).strip() or "(sans nom)",
                             role=ROLE.get(ct.get("role"), "ope"), prov="actif" if actif else "hors",
                             title=titre, sigIdx=[], heat=0, crmId=ctid,
                             seniorite=ct.get("seniorite"), source=ct.get("source_acquisition"),
                             abonneLI=bool(ct.get("abonne_linkedin")),
                             cree=ct.get("date_creation"), owner=ct.get("proprietaire")))
        cmap[ctid] = cid
    if not contacts: manquant["comptes sans contact"] += 1

    # ---------- signaux entrants (ce qu'ILS font) ----------
    signals = []
    for s in d.get("signaux", []):
        j = jours(s.get("date"))
        if j is None or j < 0 or j > 339: continue
        ty, sous = s.get("type"), s.get("sous_type")
        if ty == "formulaire":      t, st = SOUS.get(sous, ("form", "tofu"))
        elif ty == "visite":        t, st = "page", "tofu"
        elif ty == "clic_email":    t, st = "click", "mofu"
        elif ty in ("reponse_email", "email_entrant"): t, st = "reply", "mofu"
        elif ty == "abonnement_linkedin": continue   # date non fiable : piège vérifié
        else: continue                               # appel / e-mail sortant / meeting = nos actions
        who = cmap.get(str((s.get("contact") or {}).get("id") or ""))
        signals.append(dict(t=t, d=j, who=who, det=(s.get("libelle") or "—")[:140], st=st))
    signals.sort(key=lambda s: s["d"])
    for k, s in enumerate(signals):
        if s["who"]:
            ct = next((x for x in contacts if x["id"] == s["who"]), None)
            if ct: ct["sigIdx"].append(k)

    # ---------- transactions ----------
    br = d.get("deals", [])
    # Le marqueur « auto » (transaction créée par un formulaire Lead Gen) ne suffit
    # pas à dire qu'elle n'a pas été travaillée : les quatre transactions auto de ce
    # portefeuille portent toutes un propriétaire nommé et un motif de sortie saisi
    # à la main. On ne les écarte que si personne ne les a prises en main.
    for x in br:
        prop = x.get("proprietaire")
        x["autoBrut"] = bool(x.get("auto"))
        x["auto"] = bool(x.get("auto")) and not (isinstance(prop, dict) and prop.get("nom"))
    deals = [x for x in br if not x.get("auto")]
    ouverts = [x for x in deals if str(x.get("etape_id")) not in MORTS | GAGNES]
    perdus  = [x for x in deals if str(x.get("etape_id")) in MORTS]
    gagnes  = [x for x in deals if str(x.get("etape_id")) in GAGNES]
    hist = {}
    if gagnes:
        hist["signed"] = round(sum(float(x.get("montant") or 0) for x in gagnes) / 1000)
        hist["contracts"] = len(gagnes)
    if perdus:
        p = sorted(perdus, key=lambda x: (-(float(x.get("montant") or 0)), jours(x.get("date_cloture")) or 9999))[0]
        hist["loss"] = {"amt": round(float(p.get("montant") or 0)),
                        "d": jours(p.get("date_cloture")) or jours(p.get("date_creation")) or 999,
                        # `reason` porte l'étape de sortie, pas le motif de perte :
                        # le motif saisi à la main n'est pas exposé par le connecteur.
                        "reason": "sortie en « " + (p.get("etape_libelle") or "?") + " »",
                        "label": p.get("nom") or "Opportunité"}
    if ouverts:
        o = sorted(ouverts, key=lambda x: -(float(x.get("montant") or 0)))[0]
        hist["open"] = {"amt": round(float(o.get("montant") or 0)),
                        "stage": STAGE_OPEN.get(str(o.get("etape_id")), o.get("etape_libelle") or "Découverte")}
    status = "encours" if ouverts else "perdu" if perdus else "jamais"

    # ---------- activités : ce que NOUS faisons ----------
    A = d.get("activites", [])
    def who_of(a):   # les activités ne portent pas d'identifiant de contact
        return None
    calls = [a for a in A if a.get("type") == "CALL"]
    mails = [a for a in A if a.get("type") == "EMAIL"]
    meets = [a for a in A if a.get("type") == "MEETING"]
    sortants = [a for a in mails if a.get("direction") in ("Outgoing", "Outbound")]
    entrants = [a for a in mails if a.get("direction") == "Incoming"]

    callsW = [0] * 12
    log_sdr = []
    for a in calls:
        j = jours(a.get("date"))
        if j is None or j < 0: continue
        if j < 84: callsW[11 - j // 7] += 1
        log_sdr.append(dict(d=j, who=None, out=CALL_OUT.get(a.get("resultat"), "call"),
                            h=None, m=None, dur=None,
                            owner=(a.get("proprietaire") or {}).get("nom"),
                            sujet=a.get("sujet")))
    log_sdr.sort(key=lambda x: x["d"])
    conn = [x for x in log_sdr if x["out"] == "conv"]
    owners_sdr = Counter(x["owner"] for x in log_sdr if x["owner"])

    log_out = []
    for a in sortants:
        j = jours(a.get("date"))
        if j is None or j < 0: continue
        log_out.append(dict(d=j, who=None, type=0, opened=False, clicked=False, replied=False,
                            owner=(a.get("proprietaire") or {}).get("nom"), sujet=a.get("sujet")))
    log_out.sort(key=lambda x: x["d"])
    owners_out = Counter(x["owner"] for x in log_out if x["owner"])

    mtg = []
    for a in meets:
        j = jours(a.get("date"))
        if j is None: continue
        suj = a.get("sujet") or ""
        # 23 des 70 « R1 » de la maquette étaient des comités de mission, des
        # restitutions ou des événements : on ne les compte pas comme des rendez-vous
        # commerciaux. Et 66 meetings sur 80 n'ont aucun résultat saisi au CRM.
        hors = re.search(r"mission|comit|restitution|kick.?off|award|jury|soir[ée]e|webinar|point\s+hebdo", suj, re.I)
        ty = ("AUTRE" if hors else "R2" if re.search(r"\bR2\b", suj, re.I)
              else "R3" if re.search(r"\bR3\b", suj, re.I) else "R1")
        out = ("avenir" if j < 0 else "noshow" if a.get("resultat") == "Canceled"
               else "tenu" if a.get("resultat") == "Completed" else "nc")
        mtg.append(dict(d=j, type=ty, who=[], out=out,
                        ae=(a.get("proprietaire") or {}).get("nom") or "—", sujet=suj))
    mtg.sort(key=lambda x: x["d"])
    owners_ae = Counter(m["ae"] for m in mtg if m["ae"] != "—")

    monthly = [dict(pub=0, site=0, mail=0, ext=0) for _ in range(12)]
    for s in signals:
        x = TODAY - datetime.timedelta(days=s["d"])
        m = (x.year - 2025) * 12 + (x.month - 1) - 9
        if 0 <= m < 12: monthly[m][CANAL.get(s["t"], "site")] += 1

    expo = int(c.get("fibbler_linkedin_ad_impressions_90_days") or 0)
    # « groupe » désigne le compte lui-même, les autres sont des entités sœurs ou
    # parentes : le CRM ne porte aucune hiérarchie, on n'en invente pas.
    ents = [dict(id="e0", crmId=i, name=NOMS.get(i) or (c.get("name") or "").replace("&amp;", "&"), kind="groupe")]
    for k, e in enumerate(g.get("entites", [])):
        ents.append(dict(id="e%d" % (k + 1), crmId=e.get("id"), name=e["nom"], kind="filiale",
                         client=bool(e.get("client")), ca=e.get("ca_signe")))

    accounts.append(dict(
        id="a" + i, crmId=i,
        name=NOMS.get(i) or (c.get("name") or "").replace("&amp;", "&"),
        nomCRM=(c.get("name") or "").replace("&amp;", "&"), noteNom=NOTE_NOM.get(i),
        alerte=ALERTE.get(i),
        domain=c.get("domain") or "", sector=secteur, secteurOrigine=orig_sec, secteurJustif=justif,
        size=int(c.get("numberofemployees") or 0), status=status, seed=int(i) % 2**31,
        fyStart=None,   # le mois de début d'exercice n'existe pas dans le CRM

        n30=len([s for s in signals if s["d"] <= 30]),
        contacts=contacts, signals=signals, monthly=monthly, hist=hist, entities=ents,
        crm=dict(contactsAssocies=ver.get("contacts_compteur_fiche", len(contacts)),
                 contactsVus=len(contacts), ecart=ver.get("ecart_contacts", 0),
                 joignables=ver.get("contacts_joignables_par_domaine"),
                 sansEmail=ver.get("contacts_sans_domaine_email"),
                 formulaires=int(c.get("num_conversion_events") or 0),
                 visites=int(c.get("hs_analytics_num_visits") or 0),
                 touches=int(c.get("num_contacted_notes") or 0),
                 dernierContact=jours(c.get("notes_last_contacted")),
                 dealsAuto=len([x for x in br if x.get("auto")]),
                 expoPub=expo, engPub=int(c.get("fibbler_linkedin_ad_engagements_90_days") or 0)),
        deals=[dict(nom=x.get("nom"), etape=x.get("etape_libelle"), etapeId=str(x.get("etape_id")),
                    montant=float(x.get("montant") or 0), cree=x.get("date_creation"),
                    cloture=x.get("date_cloture"), owner=(x.get("proprietaire") or {}).get("nom")
                    if isinstance(x.get("proprietaire"), dict) else x.get("proprietaire"),
                    auto=bool(x.get("auto"))) for x in br],
        lv=dict(
          paid=dict(on=expo > 0, w=[0] * 12, imp30=0, cpm=None, expo90=expo,
                    eng90=int(c.get("fibbler_linkedin_ad_engagements_90_days") or 0)),
          social=[],
          # `entrants` compte les e-mails reçus de ce compte, pas les réponses à une
          # séquence : le CRM ne relie pas un entrant à un sortant. Un « taux de
          # réponse » calculé dessus dépasserait 100 % (Veolia : 94 reçus, 91 envoyés).
          outbound=dict(on=bool(log_out), seq=0, contacts=len({x["sujet"] for x in log_out}),
                        sent=len(log_out), mailsEntrants=len(entrants), meeting=1 if mtg else 0,
                        bounced=0, start=(log_out[0]["d"] if log_out else 0), log=log_out,
                        owners=dict(owners_out)),
          sdr=dict(owner=(owners_sdr.most_common(1)[0][0] if owners_sdr else "—"),
                   callsW=callsW, calls30=len([x for x in log_sdr if x["d"] <= 30]),
                   connects=len(conn),
                   rdv=1 if any(m["type"] == "R1" for m in mtg) else 0,
                   last=(log_sdr[0]["d"] if log_sdr else None), log=log_sdr,
                   owners=dict(owners_sdr)),
          sales=dict(ae=(owners_ae.most_common(1)[0][0] if owners_ae else "—"),
                     meetings=mtg, owners=dict(owners_ae),
                     **({"created": jours(ouverts[0].get("date_creation"))} if ouverts else {})))))
    prov["comptes"][i] = dict(nom=c.get("name"), contacts=len(contacts), signaux=len(signals),
                              deals=len(deals), appels=len(calls), mails=len(mails),
                              meetings=len(meets), statut=status, secteur=secteur,
                              origine_secteur=orig_sec, ecartContacts=ver.get("ecart_contacts"))

(D/"accounts.json").write_text(json.dumps(accounts, ensure_ascii=False), encoding="utf-8")
(D/"provenance.json").write_text(json.dumps(prov, ensure_ascii=False, indent=1), encoding="utf-8")
T = lambda f: sum(f(a) for a in accounts)
print(f"{len(accounts)} comptes · {T(lambda a: len(a['contacts']))} contacts · "
      f"{T(lambda a: len(a['signals']))} signaux · {T(lambda a: len(a['deals']))} deals · "
      f"{T(lambda a: len(a['lv']['sdr']['log']))} appels · {T(lambda a: len(a['lv']['outbound']['log']))} e-mails sortants · "
      f"{T(lambda a: len(a['lv']['sales']['meetings']))} meetings")
print(f"\n{'compte':32s} {'ctc':>4} {'déc':>4} {'sig':>4} {'app':>4} {'mail':>5} {'mtg':>4}  {'statut':8s} secteur")
for a in sorted(accounts, key=lambda a: -len(a["signals"])):
    dec = len([c for c in a["contacts"] if c["role"] == "dec" and c["prov"] != "hors"])
    print(f"{a['name'][:31]:32s} {len(a['contacts']):>4} {dec:>4} {len(a['signals']):>4} "
          f"{len(a['lv']['sdr']['log']):>4} {len(a['lv']['outbound']['log']):>5} "
          f"{len(a['lv']['sales']['meetings']):>4}  {a['status']:8s} {a['sector']}")
if manquant: print("\nmanques :", dict(manquant))

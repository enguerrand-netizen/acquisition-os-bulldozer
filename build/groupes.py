# -*- coding: utf-8 -*-
"""Surface d'attaque : pour chacun des 30, les autres entités du même groupe
présentes dans le CRM. Deux sources : appariement automatique (domaine racine +
nom normalisé) et une table curée pour les rattachements qu'aucun champ ne porte
(Alpine→Renault, Docaposte→La Poste, MGEN→VYV, Martell→Pernod Ricard…).
Chaque rattachement garde sa provenance : 'auto' ou 'cure'."""
import json, re, unicodedata, pathlib
D = pathlib.Path("/private/tmp/claude-501/-Users-enguerrandchalvondemersay/a75e6ca6-5ff8-478d-bd1a-9a963b0419f5/scratchpad/acq/data")
C = json.load(open(D/"comptes.json"))

IDS30 = """317410706620 315914050757 229907236085 229193587951 9770448590 317411495156
238621997284 92346012914 342918544596 36144254182 316281698550 18938276038 162003232956
36322852030 140916864248 175301965003 87436872902 148704214225 59663610043 315014441197
14793944264 36289884362 19976068547 17818953714 141529360630 316281711842 316281684204
143877777655 174866082014 14624157398""".split()

# racines de groupe curées : id du compte -> (nom du groupe, motifs de recherche)
GROUPES = {
 "19976068547":  ("Veolia",        [r"\bveolia\b", r"\bsarp\b", r"sarpindustries"]),
 "162003232956": ("BNP Paribas",   [r"bnp\s*paribas", r"\barval\b", r"\bcardif\b"]),
 "18938276038":  ("Saint-Gobain",  [r"saint[- ]?gobain", r"\bpoint\.?p\b", r"\blapeyre\b"]),
 "36322852030":  ("Société Générale", [r"societe\s*generale", r"\bboursorama\b"]),
 "315014441197": ("La Poste",      [r"\bla\s*poste\b", r"\bdocaposte\b", r"\bgeopost\b", r"\bchronopost\b"]),
 "175301965003": ("Capgemini",     [r"\bcapgemini\b", r"\bsogeti\b", r"\baltran\b"]),
 "148704214225": ("Renault",       [r"\brenault\b", r"\balpine\b", r"\bdacia\b", r"\bmobilize\b"]),
 "14624157398":  ("Pernod Ricard", [r"pernod", r"martell", r"\bmumm\b", r"perrier[- ]?jouet", r"\bricard\b"]),
 "9770448590":   ("Sodexo",        [r"\bsodexo\b", r"\bpluxee\b"]),
 "317411495166": ("VYV", []),
 "317411495156": ("VYV",           [r"\bmgen\b", r"\bvyv\b", r"harmonie\s*mutuelle", r"\bmnt\b"]),
 "17818953714":  ("Keolis",        [r"\bkeolis\b"]),
 "229907236085": ("SUEZ",          [r"\bsuez\b"]),
 "317410706620": ("Schneider Electric", [r"schneider\s*electric"]),
 "229193587951": ("L'Oréal",       [r"l\s*'?\s*oreal", r"\bloreal\b"]),
 "238621987284": ("LVMH", []),
 "238621997284": ("LVMH",          [r"christian\s*dior", r"\blvmh\b", r"\bsephora\b", r"louis\s*vuitton"]),
 "87436872902":  ("Pierre Fabre",  [r"pierre\s*fabre", r"\bavene\b", r"naturactive", r"\bducray\b"]),
 "36289884362":  ("Michelin",      [r"\bmichelin\b"]),
 "14793944264":  ("TotalEnergies", [r"total\s*energies", r"\btotal\b(?!ly)"]),
 "316281698550": ("Stellantis",    [r"\bstellantis\b", r"\bpeugeot\b", r"\bcitroen\b", r"\bopel\b", r"\bfiat\b"]),
 "140916864248": ("Groupe SEB",    [r"groupe\s*seb", r"\bseb\b", r"\bkrups\b", r"\btefal\b", r"\bmoulinex\b"]),
 "59663610043":  ("KPMG",          [r"\bkpmg\b"]),
 "174866082014": ("Thales",        [r"\bthales\b"]),
 "143877777655": ("EssilorLuxottica", [r"essilor", r"luxottica", r"\bgrandvision\b"]),
 "316281711842": ("Galileo Global Education", [r"galileo", r"\bggeedu\b", r"\bpsb\b", r"\bcox\b"]),
 "316281684204": ("Rothschild & Co", [r"rothschild"]),
 "141529360630": ("Malakoff Humanis", [r"malakoff"]),
 "92346012914":  ("Berger-Levrault", [r"berger[- ]?levrault"]),
 "342918544596": ("Sage",          [r"^sage\b", r"\bsage\s"]),
 "36144254182":  ("Léon Grosse",   [r"leon\s*grosse"]),
 "315914050757": ("Contentsquare", [r"content\s*square", r"contentsquare"]),
}

# faux rattachements repérés à l'audit : le motif matche mais l'entreprise
# n'appartient pas au groupe. Chacun est justifié.
EXCLUS = {
 "Peugeot Frères Industrie": "holding de la famille Peugeot, pas Stellantis",
 "Cours Thalès": "école de soutien scolaire, homonyme de Thales",
 "Pluxee": "scindée de Sodexo en février 2024, société cotée indépendante",
 "Pluxee France": "scindée de Sodexo en février 2024, société cotée indépendante",
}
# fiches sans nom dans le CRM, identifiées par leur domaine
RENOMME = {"realestate.bnpparibas": "BNP Paribas Real Estate (fiche sans nom au CRM)"}
# entités rattachées à un groupe dont elles sont sorties : le lien commercial
# reste utile (même interlocuteurs), la filiation non.
EX_GROUPE = {}

def norm(s):
    s = unicodedata.normalize("NFKD", (s or "")).encode("ascii","ignore").decode().lower()
    return re.sub(r"[^a-z0-9 ]+"," ", s).strip()

out = {}
for i in IDS30:
    nom_grp, motifs = GROUPES.get(i, (None, []))
    src = next((c for c in C if str(c["hs_object_id"]) == i), None)
    ents = []
    for c in C:
        cid = str(c["hs_object_id"])
        n, d = norm(c.get("name")), norm(c.get("domain"))
        if cid == i:
            continue
        # un domaine de réseau social ou un lien court ne prouve aucun lien de groupe
        if re.search(r"linkedin|bit ly|instagram|facebook|twitter", d or ""):
            continue
        if (c.get("name") or "") in EXCLUS:
            continue
        if any(re.search(m, n) or (d and re.search(m, d)) for m in motifs):
            ents.append(dict(id=cid, nom=c.get("name") or RENOMME.get((c.get("domain") or "").strip(), "(fiche sans nom)"),
                             client=c.get("population") == "client",
                             ca_signe=float(c.get("total_revenue") or 0),
                             effectif=c.get("numberofemployees"),
                             stage=c.get("lifecyclestage"), provenance="auto",
                             domaine=c.get("domain"),
                             note=EX_GROUPE.get(c.get("name") or "")))
    # dédoublonnage par ensemble de mots : « La Poste Groupe » et « Le Groupe La
    # Poste » sont une seule porte, « Arval BNP Paribas Group » ×3 aussi. On
    # retire aussi les fiches qui redoublent le compte cible lui-même.
    STOP = {"le","la","les","du","de","des","group","groupe","sa","sas"}
    key = lambda n: frozenset(norm(n).split()) - STOP
    moi = key(src.get("name") or "") if src else frozenset()
    vus, uniq = {moi}, []
    for e in sorted(ents, key=lambda e: (-e["ca_signe"], e["nom"])):
        k = key(e["nom"])
        if k in vus or not k: continue
        vus.add(k); uniq.append(e)
    ents = uniq
    out[i] = dict(groupe=nom_grp, entites=ents,
                  entites_total=len(ents) + 1,
                  clients_dans_le_groupe=[e for e in ents if e["client"]])

pathlib.Path(D/"groupes30.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"{'compte':34s} {'groupe':18s} entités  dont clients (CA signé)")
for i in IDS30:
    src = next((c for c in C if str(c["hs_object_id"]) == i), None)
    g = out[i]; cl = g["clients_dans_le_groupe"]
    ca = sum(e["ca_signe"] for e in cl)
    print(f"{(src.get('name') or '')[:33]:34s} {str(g['groupe'])[:17]:18s} {g['entites_total']:>3}      "
          f"{len(cl)}{'  ('+format(int(ca),',').replace(',',' ')+' €)' if ca else ''}")

# -*- coding: utf-8 -*-
"""Passe 3 — injection des données réelles. Point A de la carte technique :
remplacer `accounts = names.map(buildAccount)` suffit, tout le reste dérive.
`enrich()` est retirée de l'appel : elle reconstruit et écrase les journaux
d'appels, d'e-mails et de meetings réels (piège P1)."""
import json, pathlib, sys
D = pathlib.Path("/private/tmp/claude-501/-Users-enguerrandchalvondemersay/a75e6ca6-5ff8-478d-bd1a-9a963b0419f5/scratchpad/acq/data")
P = pathlib.Path("app.src.html"); s = P.read_text(encoding="utf-8")
ACC = json.load(open(D/"accounts.json")); CO = json.load(open(D/"company.json"))
LIB = json.load(open(D/"contenus.json"))
ADS = json.load(open(D/"annonces.json"))
n = 0
def sub(old, new, label):
    global s, n
    if old not in s: print("  ÉCHEC  ", label); sys.exit(1)
    s = s.replace(old, new, 1); n += 1; print("  ok     ", label)

# --- 1. nouveau type de signal : réponse / e-mail entrant ---
sub("  news:    { l: 'Actualité', c: 'ext'",
    "  reply:   { l: 'Réponse e-mail', c: 'mail' },\n"
    "  wbr_in:  { l: 'Webinar — inscrit', c: 'site' },\n"
    "  wbr_go:  { l: 'Webinar — participant', c: 'site' },\n"
    "  news:    { l: 'Actualité', c: 'ext'", "SIG webinar + reply")
sub("const SIG_ORDER = ['form','lgf','job','dl','webinar','pricing','hiring','news','ad','click','page','open'];",
    "const SIG_ORDER = ['pricing','wbr_go','reply','form','dl','wbr_in','webinar','click','lgf','page','open','ad','job','hiring','news'];", "SIG_ORDER")
sub("const CONTENT_T = ['dl','webinar','page','pricing','form','lgf','ad','click','open'];",
    "const CONTENT_T = ['dl','webinar','wbr_in','wbr_go','page','pricing','form','lgf','ad','click','open','reply'];", "CONTENT_T")
sub("sig: { pricing: 16, form: 12, dl: 10, webinar: 9, click: 5, lgf: 4,",
    "sig: { pricing: 16, wbr_go: 14, reply: 14, form: 12, dl: 10, webinar: 9, wbr_in: 8, click: 5, lgf: 4,", "poids reply + webinar")
sub("  lgf: 'A laissé ses coordonnées depuis une pub : appel sous 48 h.', form:",
    "  reply: 'A répondu à un e-mail : la conversation est ouverte, ne pas la laisser retomber.',\n  lgf: 'Formulaire Lead Gen : ne prouve rien à lui seul. Sur les 4 754 comptes appelés de l\\'étude outbound, 76 % en ont un, signés comme non signés.', form:", "WHY.reply")

# --- 2. familles sectorielles réelles ---
sub("const SECTORS = ['Industrie','Banque & assurance','Retail','Santé','Énergie','Logiciel','Transport & logistique','Agroalimentaire','BTP','Services B2B'];",
    "const SECTORS = ['Logiciel','Conseil','Banque & assurance','Distribution & commerce','Santé','Énergie & environnement','Immobilier','Enseignement','Construction','Industrie','Télécoms & médias','Transport & logistique','Autres services','Secteur public'];",
    "SECTORS réels")

# --- 3. les données ---
data = "const DATA = " + json.dumps({"accounts": ACC, "company": CO, "lib": LIB, "ads": ADS}, ensure_ascii=False, separators=(",", ":")) + ";\n"
sub("function rebuild(){",
    data + """/* Hydratation : les signaux d'un contact sont stockés par indice et repointés
   ici vers les objets de a.signals — le contrat exige des références partagées,
   sinon la chaleur d'un contact serait calculée sur des copies. */
function hydrate(raw){
  const a = Object.assign({}, raw);
  a.contacts = raw.contacts.map(c => Object.assign({}, c, { sig: (c.sigIdx || []).map(i => a.signals[i]).filter(Boolean) }));
  return a;
}
function rebuild(){""", "DATA + hydrate")
sub("""  const seen = new Set();
  accounts = names.map(buildAccount).filter(a => !seen.has(a.id) && seen.add(a.id));
  accounts.forEach(enrich);""",
    """  accounts = DATA.accounts.map(hydrate);
  /* enrich() n'est PAS appelée : elle reconstruit lv.outbound.log, lv.sdr.log et
     lv.sales.meetings à partir d'agrégats simulés et écraserait les vrais appels,
     e-mails et rendez-vous relevés dans le CRM. */""", "rebuild sur données réelles")

P.write_text(s, encoding="utf-8")
print(f"\n{n} injections · {len(ACC)} comptes · {len(s):,} caractères".replace(",", " "))

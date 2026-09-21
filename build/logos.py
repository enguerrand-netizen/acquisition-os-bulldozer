# -*- coding: utf-8 -*-
"""Logos des 30 comptes cibles — échelle logo-resolver, règles resserrées.
Deux erreurs corrigées après un premier passage :
 · l'`og:image` n'est PAS un logo (c'est la photo d'accueil : L'Oréal renvoyait
   une bannière 1920×800, SUEZ une photo 2000×1125). Retiré des candidats.
 · un favicon de 16 ou 32 px est bien le logo officiel, mais illisible à l'écran.
   En dessous de 96 px on tente la banque de logos et on garde le plus grand,
   en signalant le niveau.
Rien n'est recréé, rien n'est généré."""
import json, re, subprocess, pathlib, concurrent.futures as cf
R = pathlib.Path("/private/tmp/claude-501/-Users-enguerrandchalvondemersay/a75e6ca6-5ff8-478d-bd1a-9a963b0419f5/scratchpad/acq")
OUT = R / "logos"; OUT.mkdir(exist_ok=True)
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125 Safari/537.36"
FIX = {"316281684204": "essca.eu",          # fiche « Rothschild & Co » = ESSCA
       "14624157398": "pernod-ricard.com",
       "36322852030": "sg.fr"}              # societegenerale.com ne sert pas d'icône

def sh(a, t=22):
    try: return subprocess.run(a, capture_output=True, timeout=t)
    except Exception: return None

def dim(p):
    if p.suffix == ".svg": return 512, 512
    r = sh(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(p)], 12)
    m = re.findall(r":\s*(\d+)", r.stdout.decode() if r else "")
    return (int(m[0]), int(m[1])) if len(m) >= 2 else (0, 0)

def page(dom):
    for b in (f"https://www.{dom}", f"https://{dom}"):
        r = sh(["curl", "-sL", "--max-time", "18", "-A", UA, b])
        if r and r.returncode == 0 and len(r.stdout) > 500:
            return b, r.stdout[:220000].decode("utf-8", "ignore")
    return f"https://{dom}", ""

def cands(base, html):
    c = []
    for m in re.finditer(r'<link[^>]+>', html, re.I):
        tag = m.group(0)
        rel = (re.search(r'rel=["\']([^"\']+)["\']', tag) or [None, ""])[1].lower()
        if not any(k in rel for k in ("apple-touch-icon", "icon", "mask-icon")): continue
        h = re.search(r'href=["\']([^"\']+)["\']', tag)
        if not h: continue
        sz = re.search(r'sizes=["\'](\d+)', tag)
        pri = int(sz.group(1)) if sz else (180 if "apple" in rel else 300 if ".svg" in h.group(1).lower() else 48)
        c.append((pri, h.group(1)))
    c += [(180, "/apple-touch-icon.png"), (170, "/apple-touch-icon-precomposed.png"),
          (300, "/favicon.svg"), (48, "/favicon.ico")]
    seen, out = set(), []
    for _, u in sorted(c, key=lambda x: -x[0]):
        v = "https:" + u if u.startswith("//") else base.rstrip("/") + u if u.startswith("/") else u if u.startswith("http") else base.rstrip("/") + "/" + u
        if v in seen: continue
        seen.add(v); out.append(v)
    return out

def dl(url, dest):
    r = sh(["curl", "-sL", "--max-time", "15", "-A", UA, "-o", str(dest), "-w", "%{http_code} %{content_type}"])
    return None
def fetch(url, dest):
    r = sh(["curl", "-sL", "--max-time", "15", "-A", UA, "-o", str(dest), "-w", "%{http_code}|%{content_type}", url])
    if not r or r.returncode != 0: dest.unlink(missing_ok=True); return None
    code, _, ct = r.stdout.decode().partition("|")
    if code.strip() != "200" or not dest.exists() or dest.stat().st_size < 400:
        dest.unlink(missing_ok=True); return None
    if not any(t in ct for t in ("image", "svg", "octet")): dest.unlink(missing_ok=True); return None
    return ct.strip()

def grab(acc):
    cid, nom, dom0 = acc
    dom = FIX.get(cid) or re.sub(r"^www\.", "", (dom0 or "").replace("https://", "").replace("http://", "").strip("/").split("/")[0])
    res = dict(id=cid, nom=nom, domaine=dom, niveau=None, source=None, fichier=None, px=None, note=None)
    if not dom or "linkedin" in dom or "bit.ly" in dom:
        res["note"] = "domaine inexploitable dans le CRM"; return res
    base, html = page(dom)
    best = None
    for u in cands(base, html):
        ext = ".svg" if ".svg" in u.lower().split("?")[0] else ".png"
        tmp = OUT / (cid + "_t" + ext)
        ct = fetch(u, tmp)
        if not ct: continue
        w, h = dim(tmp)
        if w and h and max(w, h) / max(1, min(w, h)) > 2.6:   # bannière, pas un logo
            tmp.unlink(missing_ok=True); continue
        if not best or w > best[1]:
            if best: (OUT / best[3]).unlink(missing_ok=True)
            f = cid + ext; tmp.rename(OUT / f); best = (u, w, "officiel", f)
        else: tmp.unlink(missing_ok=True)
        if w >= 128: break
    if not best or best[1] < 96:
        tmp = OUT / (cid + "_g.png")
        gu = f"https://www.google.com/s2/favicons?domain={dom}&sz=256"
        if fetch(gu, tmp):
            w, _ = dim(tmp)
            if not best or w > best[1]:
                if best: (OUT / best[3]).unlink(missing_ok=True)
                f = cid + ".png"; tmp.rename(OUT / f); best = (gu, w, "banque", f)
            else: tmp.unlink(missing_ok=True)
    if best:
        p = OUT / best[3]
        res.update(niveau=best[2], source=best[0], fichier="logos/" + best[3], px=best[1], poids=p.stat().st_size)
    else:
        res["note"] = "aucun fichier récupéré (site protégé ou sans icône exploitable)"
    return res

A = json.load(open(R / "data" / "accounts.json"))
with cf.ThreadPoolExecutor(max_workers=8) as ex:
    out = list(ex.map(grab, [(a["crmId"], a["name"], a["domain"]) for a in A]))
(R / "data" / "logos.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
ok = [x for x in out if x["fichier"]]
print(f"{len(ok)}/{len(out)} · officiel {sum(1 for x in ok if x['niveau']=='officiel')} · banque {sum(1 for x in ok if x['niveau']=='banque')}")
for x in sorted(out, key=lambda x: (x["px"] or 0)):
    print(f"  {x['nom'][:34]:36s} {str(x['niveau']):9s} {str(x['px']):>5}px  {(x['note'] or x['source'] or '')[:52]}")

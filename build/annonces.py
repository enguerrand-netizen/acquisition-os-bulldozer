# -*- coding: utf-8 -*-
"""Annonces de la bibliothèque : les créas réellement diffusées en 2026.
Visuels téléchargés depuis le stockage de l'OS, redimensionnés à 260 px.
Les champs que l'OS n'a jamais importés (texte du post LinkedIn, accroche)
restent vides et l'écran le dit — on n'invente pas d'accroche."""
import json, base64, pathlib, subprocess
R = pathlib.Path("/private/tmp/claude-501/-Users-enguerrandchalvondemersay/a75e6ca6-5ff8-478d-bd1a-9a963b0419f5/scratchpad/acq")
B = json.load(open(R/"data"/"bibliotheque.json"))
A = B["annonces"]
TH = R/"data"/"thumbs"; TH.mkdir(exist_ok=True)

acq = [x for x in A if x.get("nature") == "acquisition_bulldozer"]
tdt = [x for x in A if x.get("nature") == "test_traction_prospect"]
dep = lambda xs: round(sum((x.get("metriques_2026") or {}).get("depense_eur") or 0 for x in xs))
imp = lambda xs: sum((x.get("metriques_2026") or {}).get("impressions") or 0 for x in xs)
clk = lambda xs: sum((x.get("metriques_2026") or {}).get("clics") or 0 for x in xs)

avec = [x for x in acq if (x.get("visuel") or {}).get("fichier_local") and pathlib.Path(x["visuel"]["fichier_local"]).exists()]
avec.sort(key=lambda x: -((x.get("metriques_2026") or {}).get("depense_eur") or 0))
TOP = avec[:28]
out = []
for x in TOP:
    src = pathlib.Path(x["visuel"]["fichier_local"])
    d = TH/(x["l3Id"]+".jpg")
    subprocess.run(["sips","-Z","260","-s","format","jpeg","-s","formatOptions","58",str(src),"--out",str(d)],capture_output=True)
    if not d.exists() or d.stat().st_size < 400: continue
    m = x.get("metriques_2026") or {}; t = x.get("texte") or {}; dst = x.get("destination") or {}
    out.append(dict(
        id=x["l3Id"], nom=x.get("nom_annonce") or "(sans nom)", pf=x.get("plateforme"),
        campagne=(x.get("campagne_l1") or {}).get("nom"), objectif=(x.get("campagne_l1") or {}).get("objectif"),
        format=x.get("format"), statut=x.get("statut"),
        dep=round(m.get("depense_eur") or 0), imp=m.get("impressions") or 0, clics=m.get("clics") or 0,
        ctr=m.get("ctr") or 0, cpc=m.get("cpc_eur"), conv=m.get("conversions"),
        du=(m.get("periode") or {}).get("du"), au=(m.get("periode") or {}).get("au"),
        corps=(t.get("corps_body") or None), accroche=(t.get("accroche_title") or None),
        cta=", ".join(str(c.get("libelle") or "") for c in (t.get("appel_a_action") or []) if c.get("libelle")) or None,
        url=dst.get("url"), leadForm=bool(dst.get("leadFormId")),
        img="data:image/jpeg;base64,"+base64.b64encode(d.read_bytes()).decode()))

meta = dict(
  total_annonces=len(A), acq=len(acq), tdt=len(tdt),
  dep_acq=dep(acq), dep_tdt=dep(tdt), imp_acq=imp(acq), clics_acq=clk(acq),
  avec_visuel=len(avec), montrees=len(out),
  avec_texte=sum(1 for x in acq if (x.get("texte") or {}).get("corps_body")),
  manques=["Le texte du post sponsorisé LinkedIn n'a jamais été importé dans l'OS : il est vide sur 100 % des créatives LinkedIn. Côté Meta il est complet.",
           "L'accroche (`title`) est vide sur 116 des 117 créatives interrogées, toutes plateformes confondues.",
           "Les dates de début et de fin de diffusion sont vides sur les 756 annonces.",
           "La portée est vide sur les 225 annonces LinkedIn ; réactions et commentaires le sont sur 745 des 756.",
           "Sept annonces ne rendent aucune créative, dont la meilleure LinkedIn de l'année (849 € dépensés, 12 % de CTR) : son visuel est irrécupérable."])
(R/"data"/"annonces.json").write_text(json.dumps(dict(annonces=out, meta=meta), ensure_ascii=False), encoding="utf-8")
p=(R/"data"/"annonces.json")
print(f"{len(out)} annonces montrées sur {len(avec)} avec visuel · {len(acq)} d'acquisition ({meta['dep_acq']} €) · {len(tdt)} tests de traction ({meta['dep_tdt']} €)")
print(f"fichier {round(p.stat().st_size/1024)} Ko · textes disponibles : {meta['avec_texte']}")

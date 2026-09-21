# -*- coding: utf-8 -*-
"""Version publiable : l'Artifact fournit lui-même doctype, head et un reset.
On retire donc l'enveloppe du document et on ne garde que title, styles,
contenu et script."""
import pathlib, re
L = pathlib.Path("app.src.html").read_text(encoding="utf-8").split("\n")
h0 = next(i for i, l in enumerate(L) if l.strip() == "<head>")
h1 = next(i for i, l in enumerate(L) if l.strip() == "</head>")
b0 = next(i for i, l in enumerate(L) if l.strip() == "<body>")
b1 = next(i for i, l in enumerate(L) if l.strip() == "</body>")
head = [l for l in L[h0 + 1:h1]
        if not re.match(r"\s*<meta\s+(charset|name=\"viewport\")", l)]
out = "\n".join(head + L[b0 + 1:b1])
# le squelette de l'Artifact pose un fond clair : l'application peint le sien
out = out.replace("</style>", "\nhtml,body{background:var(--bg)}\n</style>", 1)
p = pathlib.Path("/private/tmp/claude-501/-Users-enguerrandchalvondemersay/a75e6ca6-5ff8-478d-bd1a-9a963b0419f5/scratchpad/acquisition-os-bulldozer.html")
p.write_text(out, encoding="utf-8")
print(f"{p} · {len(out):,} caractères".replace(",", " "))

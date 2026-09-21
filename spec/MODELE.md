# Acquisition OS Bulldozer — modèle de décision

Portefeuille : les 30 grands comptes du 21/09/2026. Deux scores indépendants, un quadrant, des leviers.

## Score ICP /100 — « ce compte ressemble-t-il à ce qu'on signe ? »
Calibré sur les 495 clients réellement signés (26,17 M€), pas sur une définition déclarative.

| Pilier | Poids déf. | Mesure |
|---|---|---|
| Secteur | 25 | Part du secteur dans les 495 clients signés, normalisée. Un secteur jamais signé vaut 0. |
| Taille | 20 | Courbe issue du CRM : 201-1 000 sal. = 1,5 % de signature, 100-500 M€ de CA = 2,0 %, ≥1 000 sal. médiane identique au reste. Le maximum n'est donc PAS sur les plus gros. |
| Surface d'attaque | 20 | Nombre d'entités du même groupe présentes dans le CRM. Veolia = 3 fiches, BNP = 4. Une seule fiche = une seule porte. |
| Historique | 20 | Deal déjà chiffré perdu = +, client sur une autre entité = ++, jamais de deal = 0. |
| Ancienneté de la fiche | 15 | Comptes créés 2000-2016 signent à 1,2-1,5 %, les « jeunes » (2017+) à 0,7 %. |
| Malus | − | Perte de moins de 6 mois : la porte est fermée pour un trimestre. |

## Score engagement /100 — « ce compte bouge-t-il ? »
Calibré sur l'étude outbound du 17/09/2026 (4 754 comptes appelés, 33 signés).

| Pilier | Poids déf. | Mesure |
|---|---|---|
| Comité | 35 | Décideur en base + ≥ 2 contacts → 5,3 % de signature contre 0,5 %. C'est le prédicteur le plus fort : il pèse le plus. |
| Intention | 30 | Formulaires datés, décroissance exponentielle (demi-vie 120 j réglable), saturation logarithmique. Étape TOFU ×0,5 / MOFU ×1 / BOFU ×2. Un formulaire LinkedIn Lead Gen seul compte TOFU : 76 % des comptes en ont un, signés comme non signés. |
| Timing | 20 | Récence du dernier signal quel qu'il soit. |
| Réciprocité | 15 | Rapport entre ce qu'ils font (signaux) et ce qu'on fait (touches). Beaucoup de touches sans signal = on pousse dans le vide. |
| Malus | − | Aucun signal digital : l'étude donne 0 à 0,1 % de signature quel que soit le nombre de contacts importés. |

## Quadrants
Seuils par défaut ICP 70 · engagement 65, réglables et sauvegardés.
- **A — Attaquer** : ICP fort, engagement fort. Comité + intention. On y met les moyens.
- **B — Réveiller** : ICP fort, engagement faible. Le compte nous va, il ne bouge pas. Levier contenu et paid.
- **C — Qualifier** : ICP faible, engagement fort. Ils bougent mais ne nous ressemblent pas. Vérifier avant d'investir.
- **D — Veille** : ni l'un ni l'autre. Coût zéro.

## Règles d'affichage non négociables
- Aucun chiffre inventé. Un levier sans source affiche ce qu'il manque pour le brancher, jamais une valeur plausible.
- Tout compteur CRM est cumulé depuis toujours : il dit l'épaisseur du lien, pas l'actualité. Seules les dates fenêtrent.
- Les fonctions viennent de la jointure par domaine e-mail : « aucun décideur identifié » veut dire « aucun vu », pas « aucun en base ». L'écart est affiché compte par compte.
- Les ouvertures e-mail sont gonflées par Apple MPP : clics pondérés ×4, ouvertures plafonnées.

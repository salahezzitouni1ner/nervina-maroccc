# Nervina Maroc, boutique

Boutique statique : `index.html` (la page) et `store.json` (produits, prix, textes).

## Mettre en ligne avec GitHub Pages
1. Créez un dépôt sur github.com, puis envoyez ces fichiers à la racine.
2. Dans le dépôt : Settings, Pages, Source « Deploy from a branch », branche `main`, dossier `/ (root)`.
3. Après une minute, la boutique est disponible sur `https://VOTRE-COMPTE.github.io/NOM-DU-DEPOT/`.
4. Pour utiliser nervina.ma : Settings, Pages, Custom domain, puis créez l'enregistrement DNS indiqué par GitHub.

## Modifier la boutique
Modifiez `store.json` (prix, noms, textes). Placez les photos dans un dossier `images/`, puis écrivez leur chemin (ex. `images/table-amazonica.jpg`) dans la liste `imgs` du produit, dans `store.json`.

## Page d'accueil
- Bandeau d'annonces qui défile, slider plein écran (4 diapositives), réassurance, univers, carrousels produits,
  bannière « pièce signature », bannière sur mesure, étapes de commande, grille Instagram.
- Photos de l'accueil dans `images/home/`. Contenu des diapositives : `source/home_pro.py` (HOME).
- `vendor/` : GSAP 3.15 + ScrollTrigger (licence standard GreenSock, gratuite) et Lenis 1.3 (MIT).
- Si le visiteur a activé « réduire les animations », rien ne défile tout seul.

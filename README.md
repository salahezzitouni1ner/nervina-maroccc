# Nervina Maroc, boutique

Boutique statique : `index.html` (la page) et `store.json` (produits, prix, textes).

## Mettre en ligne avec GitHub Pages
1. Créez un dépôt sur github.com, puis envoyez ces fichiers à la racine.
2. Dans le dépôt : Settings, Pages, Source « Deploy from a branch », branche `main`, dossier `/ (root)`.
3. Après une minute, la boutique est disponible sur `https://VOTRE-COMPTE.github.io/NOM-DU-DEPOT/`.
4. Pour utiliser nervina.ma : Settings, Pages, Custom domain, puis créez l'enregistrement DNS indiqué par GitHub.

## Modifier la boutique
Modifiez `store.json` (prix, noms, textes). Placez les photos dans un dossier `images/`, puis écrivez leur chemin (ex. `images/table-amazonica.jpg`) dans la liste `imgs` du produit, dans `store.json`.

## Animations
- `vendor/` : GSAP 3.15 (ScrollTrigger, SplitText, DrawSVG — licence standard GreenSock, gratuite) et Lenis 1.3 (MIT), hébergés avec le site.
- Bannière de l'accueil : effets inspirés de React Bits (BlurText, ShinyText, CircularText, Noise), réécrits en GSAP.
- Si le visiteur a activé « réduire les animations », la bannière reste fixe et le défilement doux est désactivé.

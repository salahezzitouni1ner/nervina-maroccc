# Nervina Maroc, boutique

Boutique statique : `index.html` (la page) et `store.json` (produits, prix, textes).

## Mettre en ligne avec GitHub Pages
1. Créez un dépôt sur github.com, puis envoyez ces fichiers à la racine.
2. Dans le dépôt : Settings, Pages, Source « Deploy from a branch », branche `main`, dossier `/ (root)`.
3. Après une minute, la boutique est disponible sur `https://VOTRE-COMPTE.github.io/NOM-DU-DEPOT/`.
4. Pour utiliser nervina.ma : Settings, Pages, Custom domain, puis créez l'enregistrement DNS indiqué par GitHub.

## Modifier la boutique
Modifiez `store.json` (prix, noms, textes). Placez les photos dans un dossier `images/`, puis écrivez leur chemin (ex. `images/table-amazonica.jpg`) dans la liste `imgs` du produit, dans `store.json`.

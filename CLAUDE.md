# Le Mag Maliboo

Site statique du magazine de l'agence Maliboo, publié par GitHub Pages sur https://www.referencement-maliboo.com (branche `main`, dossier `docs/`).

## Organisation

- `mag/articles/*.json` : un fichier par article. C'est la seule chose à ajouter pour publier.
- `mag/mag_b.py` : le générateur (avec `mag/build.py`, `mag/piste_b.py`, `mag/style.css`, `mag/mag.js`).
- `docs/` : le site construit. Ne jamais le modifier à la main, il est entièrement réécrit à chaque construction.

Construire le site : `cd mag && python3 mag_b.py prod` (réécrit `docs/`). Aperçu local : `python3 mag_b.py` (écrit `mag/apercu-b/`, ignoré par git).

## Publier un article (lundi et jeudi)

1. Lire les titres et rubriques des articles existants dans `mag/articles/` pour ne pas répéter un sujet.
2. Choisir un sujet utile à un artisan, un commerçant, une profession libérale ou une PME : référencement Google, fiche Google et Google Maps, avis clients, visibilité dans les IA (GEO), Google Ads. Alterner les rubriques. Un article par mois au moins porte sur les avis clients.
3. Vérifier par une recherche web tout fait daté ou susceptible d'avoir changé (règles de Google, fonctionnalités, lois). Ne rien affirmer qui n'ait été vérifié.
4. Créer `mag/articles/AAAA-MM-JJ-slug.json` en copiant la structure d'un article existant : `slug`, `date` (date du jour, AAAA-MM-JJ), `rubrique` (`ia`, `avis`, `google`, `pub` ou `coulisses`), `titre`, `titre_seo`, `description`, `chapeau`, `corps` (blocs `p`, `h2`, `liste`), `conseil` (`titre`, `texte`, `etapes` : 3 ou 4 étapes concrètes), `mot` (`terme`, `definition`), `enbref` (3 points), `annonce` (`titre`, `texte`, `lien` vers une page de https://www.maliboo-referencement.fr/, `bouton`).
5. Construire, vérifier que la nouvelle page existe dans `docs/` et que la une l'affiche, puis valider et pousser sur `main` avec un message de commit court en français.
6. Donner à Laurent le lien de l'article : `https://www.referencement-maliboo.com/<slug>/`.

## Règles de rédaction

- Français, vouvoiement, phrases courtes, ton concret. 450 à 700 mots. Guillemets français « », espaces avant : ; ? ! (le générateur pose les espaces insécables).
- Chaque article contient un conseil applicable tout de suite.
- Aucun nom de client de Maliboo sans l'accord de Laurent. Aucune promesse chiffrée de résultat. Jamais de garantie sur les réponses des IA.
- Toujours un lien vers maliboo-referencement.fr dans le bloc `annonce`.
- Ne jamais écrire que les articles sont rédigés ou assistés par une IA. Signature : « la rédaction Maliboo ».
- Pas de nom de famille pour Laurent sur le site.
- Les exemples (villes, métiers, noms d'entreprise) sont inventés et vraisemblables ; les villes sont de préférence en France.

# Maintenir le site de Charlotte Giraud

Le site public est disponible à https://giraudcharlotte.github.io. Le français est servi à la racine et l’anglais sous `/en/`.

## Modifier les textes

Les pages françaises se trouvent dans `_pages/fr/` et leurs équivalents anglais dans `_pages/en/`. Conserver le même `page_id` et le même `permalink` pour les deux versions. Le bouton de langue conserve la rubrique consultée. Les titres, descriptions et textes peuvent être modifiés indépendamment dans chaque langue.

Les libellés de navigation et boutons sont dans `_data/fr/strings.yml` et `_data/en/strings.yml`. Les conférences sont dans `_data/conferences.yml` : modifier les dates et villes dans les deux langues, le titre de la communication, le lien officiel et éventuellement le nom du programme PDF. Déplacer une conférence de `upcoming` à `past` une fois passée. Conserver la mention de panel en cours d’évaluation pour Montevideo tant que son statut n’a pas changé.

Les titres de publications restent dans leur langue originale. Le mémoire de master compte 173 pages. L’article prévu pour 2027 reste indiqué « à paraître » jusqu’à sa publication.

## Mettre à jour les documents

Le CV éditable est `cv/CV_Charlotte_Giraud.tex`. Compiler avec `latexmk -pdf CV_Charlotte_Giraud.tex`, vérifier chaque page, puis remplacer `assets/pdf/CV_Charlotte_Giraud.pdf` et `assets/tex/CV_Charlotte_Giraud.tex`. Si la pagination change, mettre à jour le nombre de pages dans les deux fichiers `strings.yml`.

Les programmes de Milan et Lorient sont dans `assets/pdf/`. La photo originale est dans `assets/img/photo.jpg` ; son affichage circulaire est défini en CSS. Tous les documents sont partagés entre les deux langues.

## Vérifier et publier

La branche `main` contient les sources. Le workflow GitHub Actions vérifie la mise en forme, les overrides, la compilation Jekyll et les liens internes avant de publier avec GitHub Pages. La publication utilise l’artefact `_site` ; aucun build automatique de Jekyll par GitHub Pages n’est nécessaire.

Pour travailler localement, utiliser Ruby 3.3.5 et Node 20 ou plus récent :

```sh
bundle install
npm ci
npm run lint:prettier
bundle exec al-folio upgrade audit
bundle exec al-folio upgrade overrides audit --fail-on-stale
bundle exec jekyll build
python3 bin/check-site.py _site
bundle exec jekyll serve
```

Le port local habituel est 4000. Laisser `baseurl` vide pour ce site à la racine du domaine.

## Mettre à jour al-folio

Le site repose sur le starter al-folio v1 et le runtime `al_folio_core`, avec Jekyll Polyglot pour les langues. Les dépendances sont verrouillées dans `Gemfile.lock`.

Les quatre overrides enregistrés dans `.al-folio-overrides.yml` concernent le header, le footer, les métadonnées et le layout principal. Les autres fichiers ajoutés sont propres au site. Avant une mise à jour de gem, créer une branche, lire `AGENTS.md` et les skills dans `.agents/skills/`, puis exécuter l’audit. En cas d’override obsolète, examiner `bundle exec al-folio upgrade overrides diff CHEMIN`, réconcilier les différences et seulement ensuite exécuter `bundle exec al-folio upgrade overrides accept CHEMIN`.

Vérifier au minimum la page d’accueil, les conférences, le CV, le bouton de langue et le menu mobile dans les deux langues. La règle de style du dépôt upstream interdit les overrides dans son propre starter ; elle ne s’applique pas aux overrides autorisés de ce site personnel.

Aucun mot de passe ni jeton d’accès ne doit être ajouté au dépôt. Le site n’utilise ni formulaire de contact, ni commentaires, ni analytics.

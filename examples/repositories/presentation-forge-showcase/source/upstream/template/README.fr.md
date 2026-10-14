# Presentation Forge

Créez des présentations en HTML propre et lisible.

Vous écrivez une slide par fichier HTML ; une petite étape de build regroupe les
slides avec le moteur, le thème et vos images dans un seul `index.html` autonome
que vous pouvez double-cliquer, envoyer par mail ou héberger n'importe où. Aucun
framework, aucune dépendance.

*[English version](README.md)*

## Structure

```
presentation-forge/
├── engine/              # la logique de présentation - ne pas toucher
│   ├── deck-stage.js    #   le moteur : un custom element <deck-stage>
│   ├── base.css         #   sa mécanique : mise à l'échelle, contrôles, mode présentateur
│   ├── motion.css       #   la boîte à outils d'animation (entrées, boucles, transitions)
│   ├── components/      #   graphiques, chiffres, frises… (inclus seulement si utilisés)
│   └── icons.json       #   icônes pour <i data-icon="…"> (Lucide, ISC)
├── themes/              # les apparences - un dossier par thème, interchangeables
│   ├── obsidian/        #   sombre, éditorial (le thème par défaut)
│   │   ├── tokens.css   #     les réglages : couleurs, échelle typo, espacements, polices
│   │   ├── fonts.css    #     déclarations @font-face
│   │   ├── slides.css   #     style des blocs (.title, .bullets, variantes…)
│   │   ├── fonts/       #     fichiers de police   ┐ le look - voyage
│   │   ├── images/      #     fonds, textures      │ avec le thème
│   │   └── logos/       #     logos                ┘
│   └── ink-blue/        #   alternative claire et sobre
├── slides/              # votre contenu - un fichier par slide, ordonné par nom
│   ├── 01-title.html    #   (une nouvelle présentation démarre vide : à vous de les écrire)
│   └── …
├── assets/              # images de contenu de CETTE présentation (séparées des thèmes)
├── deck.config.json     # titre, langue, thème, transition, niveau d'animation
├── deck.css             # facultatif : styles propres à cette présentation
├── build.py             # regroupe tout dans un seul index.html autonome
├── index.html           # le résultat du build - ouvrez & partagez CE fichier
└── README.fr.md
```

Trois couches claires : **logique** (`engine/`), **apparence** (`themes/`),
**contenu** (`slides/`). Un thème est un dossier autonome (styles + ses polices,
fonds et logos) ; changer le `theme` dans `deck.config.json` restyle toute la
présentation sans toucher une seule slide, car chaque thème respecte le même jeu
de variables et de classes.

## Utilisation

```sh
# 1. Éditez les slides dans slides/ (un <section class="slide"> par fichier).
# 2. Construisez la présentation (sous Windows, utilisez "python" au lieu de
#    "python3" si c'est ce qui est dans votre PATH) :
python3 build.py            # -> index.html (autonome)
# 3. Ouvrez ou partagez index.html - un seul fichier avec tout dedans,
#    images comprises : il marche en double-clic et hors-ligne.
```

Pendant l'édition, reconstruire à chaque sauvegarde et rafraîchir le navigateur :

```sh
python3 build.py --watch
python3 build.py --open     # construit, puis ouvre dans le navigateur
```

Le texte corrigé directement dans le navigateur (le bouton Modifier, dans Chrome
ou Edge, sur le fichier local) est enregistré dans `index.html` ; le build
suivant le recopie d'abord dans `slides/`, donc reconstruire ne le perd jamais.
`python3 build.py --pull` fait seulement cette copie.

Parcourez les slides avec les flèches ou Espace.

## Écrire une slide

Chaque fichier de `slides/` est un `<section class="slide">` :

```html
<section class="slide">
  <h2 class="title">Votre point ici.</h2>
  <ul class="bullets">
    <li>Une idée par ligne.</li>
  </ul>
  <aside class="notes">Notes - visibles seulement en mode présentateur.</aside>
</section>
```

Variantes de slide : `slide--title`, `slide--section`, `slide--conclude`.
Blocs de contenu fournis par le thème : `eyebrow`, `display`, `title`, `lead`,
`muted`, `accent`, `bullets`, `two-col`, `card`, `blockquote`, `pre > code`.
Composants fournis par le moteur : `stats`, `bars`, `ring`, `steps`, `timeline`,
`compare`, `grid`, icônes (`<i data-icon="rocket"></i>`) et décor `fx`.
Animation : `data-anim`, `data-stagger`, `data-count`, `data-loop`,
`data-transition`, dosés par `"motion"` dans `deck.config.json` (de `none` à
`extra`).

Les slides s'affichent dans l'**ordre des noms de fichiers** (`01-`, `02-`…) ;
pour en ajouter une, déposez un nouveau fichier dans `slides/`. Voir
[docs/writing-slides.md](docs/writing-slides.md) pour le guide complet.

## Présenter

- **Révélation progressive** - ajoutez `class="fragment"` à un élément pour le
  révéler étape par étape au clic (la vue présentateur affiche `step 2/3`).
- **Plein écran** - le bouton ⤢ ou `f`.
- **Mode présentateur** - le bouton écran ou `p` : ouvre une fenêtre audience
  (slide en plein écran) et une vue présentateur ici, avec l'aperçu de la slide
  suivante, les notes, l'heure réelle et les chronos, le dessin et le laser.
- **Vue d'ensemble** - `o` affiche toutes les slides en grille ; `b` / `w`
  passe l'écran en noir / blanc.
- **Raccourcis clavier** - touche `?` pour la liste complète.

## Licence

Le moteur et les outils de build sont sous licence [MIT](LICENSE) © Thomas Gourmelen. Les slides que vous écrivez vous appartiennent.

# Components: charts, figures, icons

Ready-made graphic blocks shipped in the engine (`engine/components/`). They take
the colours and fonts of whatever theme is active, and `build.py` bundles only the
ones a deck uses - an unused chart adds nothing to `index.html`. Use these
instead of drawing SVG or writing CSS by hand. Their motion (bars growing, rows
appearing) is built in and follows the deck's level.

Sizes are for the 1920x1080 canvas. Keep each one to the item counts noted: past
that, split the slide.

## Key figures - `stats`

```html
<div class="stats" data-stagger="rise">
  <div class="stat">
    <p class="stat__value" data-count>+18%</p>
    <p class="stat__label">revenue, year on year</p>
  </div>
  <div class="stat">…</div>
</div>
```

2 to 4 figures. One alone as the hero of a slide: `<div class="stat stat--hero">`.
`data-count` makes the number count up.

## Bar chart - `bars`

```html
<ul class="bars">
  <li style="--value: 100"><span class="bars__label">France</span><span class="bars__value">412 k€</span></li>
  <li style="--value: 64" class="is-highlight"><span class="bars__label">Spain</span><span class="bars__value">264 k€</span></li>
</ul>
```

`--value` is 0-100: scale the data so the largest bar is 100. `.is-highlight`
stresses one bar. `class="bars bars--vertical"` for columns (up to ~8). 3 to 7 bars.

## Gauge - `ring`

```html
<div class="ring" style="--value: 64">
  <p class="ring__value">64%</p>
  <p class="ring__label">of teams adopted it</p>
</div>
```

One percentage. Several side by side: put them in a `.stats` row.

## Process or flow - `steps`

```html
<ol class="steps steps--numbered">
  <li><i data-icon="search"></i><h3>Collect</h3><p>One short line.</p></li>
  <li><h3>Decide</h3><p>One short line.</p></li>
  <li class="is-highlight"><h3>Ship</h3><p>One short line.</p></li>
</ol>
```

Boxes joined by arrows, 2 to 5 steps. `--numbered` adds 1, 2, 3 badges; an icon
as the first child becomes the step's icon; `.is-highlight` marks one step.

## Timeline - `timeline`

```html
<ol class="timeline">
  <li><p class="timeline__date">2019</p><h3>Founded</h3><p>Two people, one idea.</p></li>
  <li class="is-now"><p class="timeline__date">Today</p><h3>12 countries</h3><p>…</p></li>
</ol>
```

3 to 6 dated milestones; `.is-now` marks where we are.

## Comparison table - `compare`

```html
<table class="compare compare--last">
  <thead><tr><th></th><th>Today</th><th>With us</th></tr></thead>
  <tbody>
    <tr><td>Works offline</td><td class="no"></td><td class="yes"></td></tr>
    <tr><td>Setup time</td><td class="partial">2 days</td><td class="yes">5 min</td></tr>
  </tbody>
</table>
```

Empty `.yes` / `.no` / `.partial` cells draw ✓ ✗ ~; with text inside, the text is
coloured instead. `--last` highlights the last column. Up to ~8 rows.

## Columns - `grid`

```html
<div class="grid grid--3" data-stagger="rise">
  <div class="card"><i data-icon="zap" class="icon-tile"></i><h3>Fast</h3><p>…</p></div>
  …
</div>
```

`.grid--2` / `--3` / `--4`, or `.grid` alone to fit as many as there is room for.
Feature lists, team members, logos, options.

## Icons - `<i data-icon>`

```html
<i data-icon="rocket"></i>                          inline, sized like the text
<i data-icon="shield-check" class="icon-tile"></i>  in a tinted square
```

Size with `font-size`, colour with `color`; `data-anim="draw"` traces it in. An
unknown name makes `build.py` warn. Available (Lucide, line style):

arrow-down-right · arrow-right · arrow-up-right · award · bell · book-open ·
brain · briefcase · building-2 · calendar · chart-column · chart-line · chart-pie ·
check · circle-check · circle-help · circle-x · clock · cloud · code · coins · cpu ·
database · dollar-sign · download · euro · eye · file-text · flag · flask-conical ·
gauge · git-branch · globe · graduation-cap · handshake · heart · hourglass ·
image · info · layers · leaf · lightbulb · link · lock · mail · map-pin ·
megaphone · message-circle · minus · monitor · package · percent · phone ·
piggy-bank · play · plus · puzzle · recycle · refresh-cw · rocket · scale ·
search · server · settings · shield-check · shopping-cart · smartphone ·
sparkles · star · target · terminal · thumbs-up · trending-down · trending-up ·
triangle-alert · trophy · truck · user · users · wifi · workflow · wrench · x ·
zap

## Decoration - `fx`

```html
<div class="fx fx--glow fx--tr" aria-hidden="true"></div>
<div class="fx fx--glass fx--br" data-loop="float" aria-hidden="true"></div>
```

Shapes behind the content, never clickable: `fx--glow` (soft light), `fx--grid`
(dot grid), `fx--glass` (floating pane), `fx--ring` (outline circle), `fx--aurora`
(colour band). Place with `fx--tl` / `--tr` / `--bl` / `--br` / `--center` (or a
`style="top:…; left:…"`), size with `fx--sm` / `fx--lg`. Always `aria-hidden="true"`.
Mostly for title, section and closing slides, and for `lively` / `extra` decks.

## Code

```html
<pre data-filename="app.py"><code><span class="line">first line</span><span class="line">second line</span></code></pre>
```

One `.line` span per line (escape `< > &`). `data-stagger="type"` on the `<code>`
types the lines in one after the other.

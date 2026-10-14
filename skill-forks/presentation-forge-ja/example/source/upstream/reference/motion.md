# Motion: the animation toolkit

Everything here ships in the engine (`engine/motion.css`), works with every
theme, and costs a few KB. Pick from this menu - never write your own
`@keyframes` for a deck. The user chose a **level** at the start; it is
`"motion"` in `deck.config.json`, and it decides how much you use.

## 1. The five levels

The level only turns the dials (duration, distance, loops). Slides keep the same
markup at every level, so changing it later is one word in the config.

| Level | Feel | Use |
| :-- | :-- | :-- |
| `none` | perfectly still | No `data-anim`, no loops. Fragments still reveal (instantly). Transition `none` or `fade`. |
| `subtle` | calm, corporate | `data-anim="fade"` or `rise` on a few key elements; `data-stagger` on one list per slide at most. Transitions become a plain fade. |
| `balanced` (default) | polished | An entrance on most content slides (title or main block); `data-stagger` on lists, grids, stats; `data-count` on key figures; `fragment` where the order of points matters. |
| `lively` | energetic | Everything in balanced, plus varied effects (`from-left`, `zoom`, `pop`), ambient loops on decoration (`data-loop`), `fx` shapes, a `slide` or `zoom` transition on section dividers. |
| `extra` | "full show" | Everything in lively, pushed: `pop` and `flip` entrances, `draw` on icons and SVG, `fx--glass` / `fx--aurora` decor with loops, `flip` or `zoom` transitions on key slides, `highlight` fragments. Still one idea per slide: motion serves the point, never hides it. |

Whatever the level: entrances only play when moving **forward** (going back shows a
slide finished), the OS "reduce motion" setting is always respected, and the
thumbnails, print view and presenter preview always show the finished slide.

## 2. Entrances: `data-anim`

An element animates in when its slide appears:

```html
<h2 class="title" data-anim="rise">Caching cut p99 by 40%.</h2>
<div class="card" data-anim="from-right" style="--delay: .3s">…</div>
```

| Effect | Motion |
| :-- | :-- |
| `fade` | fades in |
| `rise` / `drop` | slides up from below / down from above |
| `from-left` / `from-right` | slides in from that side |
| `zoom` | grows in |
| `pop` | grows in with a springy overshoot |
| `blur` | comes into focus |
| `wipe` | revealed left to right |
| `type` | revealed left to right in character steps (one line, or code lines) |
| `flip` | swings in, 3D |
| `draw` | an SVG or icon traces its own strokes |

`style="--delay: .4s"` waits before starting (cascades to the children).

## 3. One after the other: `data-stagger`

On a parent: each child enters in turn, with that effect.

```html
<ul class="bullets" data-stagger="rise">…</ul>
<div class="grid grid--3" data-stagger="pop">…</div>
<pre><code data-stagger="type"><span class="line">…</span><span class="line">…</span></code></pre>
```

## 4. On click: fragments with an effect

`class="fragment"` reveals on the next click (→ / Space / clicker). Add
`data-anim` to choose how; inside a `data-stagger` parent a fragment uses the
parent's effect.

```html
<li class="fragment" data-anim="from-left">…</li>
<p>Keep it on screen and <span class="fragment" data-anim="highlight">mark these words</span> on the click.</p>
```

`highlight` is special: the text stays visible and gets a marker sweep on the click.

## 5. Figures that count: `data-count`

```html
<p class="stat__value" data-count>+18%</p>
```

The first number counts up from 0 when the slide appears (balanced and up), then
the exact original text is restored. Put it on an element that holds only the
figure's text (no child tags).

## 6. Ambient loops: `data-loop` (lively and extra)

`float` · `drift` · `pulse` · `glow` · `spin`. Paused below `lively`. Use them on
decoration (an `fx` shape, an icon tile), not on text. A loop owns the element's
animation: don't put `data-loop` and `data-anim` on the same element - wrap one.

```html
<div class="fx fx--glass fx--tr" data-loop="float" aria-hidden="true"></div>
```

## 7. Slide transitions

Deck default in `deck.config.json` (`"transition"`), or per slide:

```html
<section class="slide slide--section" data-transition="zoom">
```

`none` · `fade` (default) · `slide` (follows the direction) · `zoom` · `rise` ·
`blur` · `flip` (3D, follows the direction). A `subtle` deck keeps all of them a
plain fade.

## 8. Built-in motion of the components

`bars` grow, `ring` fills, `timeline` draws its line then shows each milestone,
`steps` and `compare` rows come in one after the other. Nothing to add.

## Don'ts

- Don't animate everything on a slide: one entrance (or one stagger) per slide is
  usually right; the eye should go where the point is.
- Don't put `data-anim` on the `<section>` itself (use `data-transition`).
- Don't fight the level: at `subtle`, don't stack effects; at `extra`, still keep
  text readable and the takeaway obvious.
- Don't write custom `@keyframes` or inline `animation:` styles - if something is
  missing from this menu, say so to the user.

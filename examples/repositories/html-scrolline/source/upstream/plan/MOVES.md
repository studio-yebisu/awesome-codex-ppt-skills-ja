# W3 move 라이브러리 — 통합 명세 (MOVES)

- 정본 명세(구현 지시 수준) = `plan/moves.catalog.jsonl`(한 줄 = move 하나). 이 문서는 그 요약·결정·규칙. 별칭 표 = `plan/moves.aliases.json`.
- 입력: `plan/concepts/{canvas,data,kinetic,launch,rail,zoom}.moves.jsonl` 96줄(중복 id 6줄 포함 90개) + `concepts/*/concept.json` allow·signature + R7 인벤토리.
- 결과: **move 80개** = signature 18 + 비 signature 62(그중 2개 이상 컨셉이 쓰는 공용 11). family 9개, W3 잡 17개 + 공용 helper 잡 W3-S0 1개.

## 1. 병합 결정 (같은 동작 = 하나, 컨셉 질감 = param 프리셋)

- 기준: 같은 role·같은 대상 part·같은 운동 구조(무엇이 어디서 어디로)면 하나로. 질감 차이(크기·시차·밑줄 vs 색)는 param으로 남기고 컨셉별 값은 `presets`(계약 v2 대기 PRESETS: concept `moves.params`)에 둔다.
- signature move는 병합 대상에서 제외(18개 전부 원래 id 유지).
- 같은 id로 여러 컨셉이 쓴 정의(count-roll×3·video-scrub×3·mask-word-in×2·line-mask-rise×2)는 내용이 같아 하나로, 덧붙인 요청(rail의 captionIn 등)은 param으로 흡수.

| 정본 id | 흡수한 id | 합친 이유 | 컨셉 프리셋 |
|---|---|---|---|
| `blur-drop` | focus-drop | blur 퇴장. 어절 단위 하강(kinetic) vs 블록 단위 렌즈 이탈(zoom) | zoom: unit="block", blur=8, drop=0, scaleTo=0.97, emLast=0.1 |
| `count-roll` | count-up | number enter, from→value Intl 카운트 + 단위·label 후행. 단위 x 이동만 다름 | canvas: unitSlide=8; data: unitSlide=8 |
| `divider-split` | compare-ledger | 가운데 괘선 → 항목 갈라짐 → 결론. data는 값 카운트 | data: count=true, spread=0 |
| `focus-pull` | focus-pull-in | 어절 blur→선명 랙 포커스 등장. canvas는 scale, zoom은 y·자간 | canvas: scaleFrom=1.06, rise=0, tracking=0, duration=1.0 |
| `line-draw` | line-draw-race | 선 그래프 왼→오 draw. 여러 선·머리 이름표는 param | data: headLabels=true, markPop=false |
| `line-mask-rise` | headline-set | 줄 클립 rise 헤드라인. data는 위 괘선 + 밑줄 강조 | data: rule=true, emStyle="underline", stagger=0.14, tracking=0, duration=1.0 |
| `mask-word-in` | glyph-window | 글자 마스크 속 영상 등장. 숫자 글리프가 기준선에서 솟는 질감은 riseFrom | data: riseFrom=100, brightFrom=0.7, brightTo=1.15, scaleFrom=1, trackFrom=1, captionIn=true; rail: captionIn=true; kinetic: riseFrom=100 |
| `recede` | chart-recede, region-recede | 식으며 물러나는 퇴장(블러 없음). 차트는 위로 빠짐, 지도는 옅게 남음 | canvas: to=0.22, scaleTo=0.985; data: drift=0.06, duration=0.7 |
| `type-on` | speech-type | prompt 입력 계단. 글자 단위(kinetic) vs 어절 묶음·화자 먼저(launch) | launch: chunk="word", speakerFirst=true, rule=true |
| `window-open` | window-expand | 영상 창이 clip inset으로 열림 + media 1.12→1. 시작 모양 line vs box | launch: shape="box", scrim=true |

- 축소 1건: `glyph-rise` accepts `[text, video]` → `[text]`. video의 글자 솟음은 `mask-word-in`(kinetic 프리셋 riseFrom=100)이 맡는다(글자별 마스크 분리는 textMask 한 장 구조와 충돌).
- 남긴 유사쌍(병합 안 함): `frame-scrub`(step)·`video-scrub`(enter)는 role이 달라 별개(같은 `_shared/media.js` 사용). `map-label-settle`(글자 자간, 지도 인쇄 문법) vs `tracking-close`(어절 transform). `rail-settle`(rail 컨셉 오프닝, yaw) vs `establish-crane`(canvas signature, pitch). `text-mask-dive`(획 속 줌) vs `word-door`(kinetic signature, 문짝). `strike-swap`(숫자) vs `scramble-swap`(어절). `point-focus` vs `port-aim`(링·지시선, zoom→zoom-dive 이음).

### concept.json 갱신 필요 (컨셉 소유자 또는 메인, 이 설계자는 수정 안 함)

- `data`: `chart-recede` → `recede`, `compare-ledger` → `divider-split`, `count-up` → `count-roll`, `glyph-window` → `mask-word-in`, `headline-set` → `line-mask-rise`, `line-draw-race` → `line-draw`
- `launch`: `speech-type` → `type-on`, `window-expand` → `window-open`
- `zoom`: `focus-drop` → `blur-drop`
- `canvas`: `count-up` → `count-roll`, `focus-pull-in` → `focus-pull`, `region-recede` → `recede`
- `kinetic`: byType.video.enter: glyph-rise → mask-word-in (glyph-rise accepts = text로 축소)
- 일괄 치환은 `plan/moves.aliases.json`으로 기계 처리(allow·signature·defaults·byType 모두). 덱 yaml도 같은 표로.

## 2. family 분류와 폴더

- family = `engine/constants.js FAMILIES`의 9개 그대로(계약 변경 없음). 폴더 `moves/<family>/<id>.js` + `<id>.test.js`, family 목록 `moves/<family>/index.js`.
- 분류 기준: **무엇을 움직이는가**. 글자 part(type), 차트·숫자(data), 영상·마스크·프레임(media), 한 모양이 다음 beat의 모양이 됨(morph, link 전용), 카메라·world 배율(camera, 3D 허용 유일), 레일 시간축(rail), 흐림·밝기 초점(reveal), 선·항목이 갈라지고 모임(assemble), 초점 조준·주석·물러남(emphasis).

| family | 수 | move |
|---|---|---|
| reveal | 4 | `blur-drop` `focus-pull` `lights-out` `lit-from-dark` |
| type | 16 | `caret-blink` `glyph-rise` `half-split` `line-focus` `line-mask-rise` `map-label-settle` `phrase-fold` `push-build` `result-stream` `scramble-out` `scramble-swap` `slot-pick` `sweep-out` `tracking-close` `type-on` `word-slam` |
| morph | 6 | `caret-collapse` `field-burst` `frame-to-figure` `glyph-to-bar` `headline-to-caption` `iris-to-dot` |
| camera | 6 | `arc-flight` `atlas-pullback` `establish-crane` `rail-settle` `zoom-dive` `zoom-surface` |
| rail | 10 | `counter-handoff` `era-shift` `fold-to-rail` `rail-advance` `rail-compress` `rail-draw` `rail-drop` `rail-lift` `rail-split-open` `rail-surface` |
| data | 19 | `aggregate-split` `annotation-pin` `baseline-grow` `count-roll` `diverge-grow` `dot-multiply` `dot-seed` `dots-pour` `forecast-extend` `ink-in` `line-draw` `line-to-waffle` `mark-morph` `number-slam` `point-focus` `rank-reorder` `strike-swap` `threshold-line` `waffle-recount` |
| media | 11 | `frame-scrub` `into-word` `mask-word-in` `scrub-callouts` `slow-push` `sticky-scrub-link` `text-mask-dive` `video-scrub` `window-open` `window-takeover` `word-door` |
| assemble | 3 | `divider-split` `pin-drop` `transcript-condense` |
| emphasis | 5 | `depth-ladder` `ladder-callout` `port-aim` `recede` `rule-mark` |

## 3. 전체 표

- 쓰는 덱 = 그 move를 allow한 컨셉(덱 = 컨셉당 1편). sig = 그 컨셉의 signature. 난이도 1 쉬움·2 보통·3 어려움(수식·다단 handoff·canvas).

| id | family | role | 쓰는 덱 | sig | 난이도 | 잡 | sources |
|---|---|---|---|---|---|---|---|
| `blur-drop` ← focus-drop | reveal | exit | kinetic, zoom | - | 1 | W3-RV | blur-dissolve, word-rise-fade, rack-focus |
| `focus-pull` ← focus-pull-in | reveal | enter | canvas, zoom | - | 1 | W3-RV | blur-resolve, rack-focus, blur-reveal, atmospheric-depth |
| `lights-out` | reveal | exit | launch | - | 1 | W3-RV | dip-to-color, spotlight |
| `lit-from-dark` | reveal | enter | launch | launch | 2 | W3-RV | lamp-cone-reveal, light-sweep, blur-resolve |
| `caret-blink` | type | ambient | kinetic | - | 1 | W3-TY2 | context-caret, typewriter |
| `glyph-rise` | type | enter | kinetic | - | 2 | W3-TY1 | mask-reveal, tracking-reveal, char-stagger |
| `half-split` | type | exit | kinetic | - | 1 | W3-TY3 | text-half-split, split-slide |
| `line-focus` | type | enter | kinetic | - | 2 | W3-TY2 | lyric-line-focus, word-relay |
| `line-mask-rise` ← headline-set | type | enter | data, launch, rail | - | 1 | W3-TY1 | mask-reveal, word-rise-fade, tracking-reveal, underline-draw |
| `map-label-settle` | type | enter | canvas | - | 2 | W3-TY1 | tracking-reveal, word-rise-fade, highlight-sweep |
| `phrase-fold` | type | link | kinetic | kinetic | 3 | W3-TY3 | letter-anagram-shift, origami-fold, phrase-push-build, text-half-split |
| `push-build` | type | enter | kinetic | - | 2 | W3-TY1 | phrase-push-build, word-relay |
| `result-stream` | type | step | kinetic | - | 2 | W3-TY2 | word-pop-caption, karaoke-caption, typewriter |
| `scramble-out` | type | exit | kinetic | - | 2 | W3-TY3 | text-scramble, text-particle-dissolve |
| `scramble-swap` | type | step | kinetic | - | 2 | W3-TY3 | text-scramble, strikethrough-replace, word-slot-cycle |
| `slot-pick` | type | enter | kinetic | kinetic | 3 | W3-TY2 | next-token, word-slot-cycle, phrase-push-build, word-rise-fade |
| `sweep-out` | type | exit | kinetic | - | 1 | W3-TY3 | word-relay, motion-blur, overlapping-action |
| `tracking-close` | type | enter | kinetic | - | 1 | W3-TY1 | tracking-reveal, word-rise-fade |
| `type-on` ← speech-type | type | enter | kinetic, launch | - | 2 | W3-TY2 | typewriter, context-caret, karaoke-caption |
| `word-slam` | type | enter | kinetic | - | 2 | W3-TY1 | kinetic-beats, kinetic-type-sweep, anticipation |
| `caret-collapse` | morph | link | kinetic | - | 2 | W3-MO | origami-fold, split-slide, morph-match-cut, context-caret |
| `field-burst` | morph | link | kinetic | - | 2 | W3-MO | clip-reveal, split-panel-handoff, text-particle-dissolve |
| `frame-to-figure` | morph | link | rail | - | 2 | W3-MO | scale-swap, match-cut, clip-reveal |
| `glyph-to-bar` | morph | link | data | - | 3 | W3-MO | text-cutout-zoom, shape-morph, bar-grow |
| `headline-to-caption` | morph | link | canvas | - | 2 | W3-MO | match-cut, inline-image-expand |
| `iris-to-dot` | morph | link | data | - | 3 | W3-MO | morph-match-cut, scale-swap, shape-morph, text-cutout-zoom |
| `arc-flight` | camera | camera | canvas | canvas | 3 | W3-CA1 | camera-flight, parallax, deep-parallax, atmospheric-depth |
| `atlas-pullback` | camera | camera | canvas | canvas | 2 | W3-CA1 | zoom-to-detail, perspective-tilt, atmospheric-depth |
| `establish-crane` | camera | camera | canvas | canvas | 2 | W3-CA1 | crane-tilt, perspective-tilt, atmospheric-depth |
| `rail-settle` | camera | camera | rail | - | 2 | W3-CA1 | perspective-tilt, crane-tilt, parallax, atmospheric-depth |
| `zoom-dive` | camera | link | zoom | zoom | 3 | W3-CA2 | infinite-zoom, zoom-to-detail, zoom-through, giant-mask-reveal, push-in |
| `zoom-surface` | camera | link | zoom | zoom | 3 | W3-CA2 | infinite-zoom, scale-swap, zoom-to-detail, focus-contraction |
| `counter-handoff` | rail | link | rail | rail | 3 | W3-RL2 | rolling-digits, count-up, match-cut, scale-swap, glyph-roll |
| `era-shift` | rail | link | rail | rail | 3 | W3-RL1 | wipe, luma-wipe, pan, tracking-reveal, rolling-digits, match-on-action |
| `fold-to-rail` | rail | link | rail | - | 2 | W3-RL2 | split-panel-handoff, line-draw, scale-swap, push-transition |
| `rail-advance` | rail | step | rail | rail | 3 | W3-RL1 | pan, infinite-pan, parallax, rolling-digits, glyph-roll, motion-blur, timeline-scrub, focus-handoff |
| `rail-compress` | rail | link | rail | - | 3 | W3-RL1 | axis-rescale, scale-swap, zoom-to-detail, time-compression |
| `rail-draw` | rail | enter | rail | - | 2 | W3-RL1 | line-draw, stagger, tracking-reveal |
| `rail-drop` | rail | link | rail | - | 2 | W3-RL2 | scale-swap, match-cut, match-on-action |
| `rail-lift` | rail | link | rail | - | 2 | W3-RL2 | match-cut, morph-match-cut, scale-swap, clip-reveal |
| `rail-split-open` | rail | link | rail | - | 2 | W3-RL2 | split-slide, symmetric-panel-open, counter-moving-matte, clip-reveal |
| `rail-surface` | rail | enter | rail | - | 1 | W3-RL1 | fade-slide, stagger, overlapping-action |
| `aggregate-split` | data | enter | data | - | 3 | W3-DA4 | aggregate-split-merge, stacked-grouped-transition |
| `annotation-pin` | data | step | data | data | 2 | W3-DA2 | annotation-callout, annotation-tracking, underline-draw |
| `baseline-grow` | data | enter | data | - | 1 | W3-DA1 | bar-grow, count-up |
| `count-roll` ← count-up | data | enter | canvas, data, kinetic, rail, zoom | - | 1 | W3-DA1 | count-up, rolling-digits |
| `diverge-grow` | data | enter | data | - | 2 | W3-DA1 | bar-grow, change-arrows |
| `dot-multiply` | data | step | data | data | 3 | W3-DA3 | unit-grid, particle-assemble, aggregate-split-merge, dot-regroup |
| `dot-seed` | data | enter | data | - | 2 | W3-DA3 | scale-pop, annotation-callout |
| `dots-pour` | data | link | data | - | 3 | W3-DA3 | dot-regroup, unit-aggregate-transition, beeswarm-settling |
| `forecast-extend` | data | step | data | - | 2 | W3-DA2 | confidence-band-reveal, point-to-point-build |
| `ink-in` | data | enter | data | - | 2 | W3-DA2 | outline-then-fill, line-draw |
| `line-draw` ← line-draw-race | data | enter | canvas, data | - | 2 | W3-DA2 | line-draw, line-chart-race, annotation-tracking |
| `line-to-waffle` | data | link | data | - | 3 | W3-DA3 | unit-grid, scale-swap, fractional-icon-fill |
| `mark-morph` | data | step | data | data | 3 | W3-DA4 | chart-path-morph, axis-rescale, staged-chart-transition, line-draw |
| `number-slam` | data | enter | launch | launch | 2 | W3-DA1 | scale-pop, light-sweep, blur-resolve |
| `point-focus` | data | step | canvas | - | 2 | W3-DA2 | focus-handoff, threshold-pulse |
| `rank-reorder` | data | link | data | - | 3 | W3-DA4 | rank-transition, object-constant-update, bump-rank-reveal |
| `strike-swap` | data | step | zoom | - | 2 | W3-DA1 | strikethrough-replace, rolling-digits, count-up |
| `threshold-line` | data | step | data | - | 2 | W3-DA2 | threshold-pulse, chart-filter-fade, line-draw |
| `waffle-recount` | data | step | data | - | 2 | W3-DA3 | unit-grid, color-encoding-transition |
| `frame-scrub` | media | step | canvas | - | 1 | W3-ME1 | frame-scrub, scroll-frame-scrub, scroll-scrub-cinema |
| `into-word` | media | link | kinetic | - | 2 | W3-ME2 | inline-image-expand, text-window-fill, clip-reveal |
| `mask-word-in` ← glyph-window | media | enter | data, launch, rail | - | 2 | W3-ME2 | text-window-fill, tracking-reveal |
| `scrub-callouts` | media | step | launch | - | 2 | W3-ME1 | frame-scrub, annotation-tracking, annotation-callout, exploded-assembly |
| `slow-push` | media | ambient | launch | - | 1 | W3-ME1 | push-in, ken-burns |
| `sticky-scrub-link` | media | link | launch | launch | 2 | W3-ME1 | scroll-frame-scrub, frame-scrub, anchored-substitution |
| `text-mask-dive` | media | step | launch | - | 2 | W3-ME2 | text-cutout-zoom, giant-mask-reveal, text-window-fill |
| `video-scrub` | media | enter | data, kinetic, rail, zoom | - | 1 | W3-ME1 | scroll-frame-scrub, frame-scrub, scroll-scrub |
| `window-open` ← window-expand | media | enter | canvas, launch | - | 2 | W3-ME2 | iris-mask, clip-reveal, mask-reveal, screen-emergence, inline-image-expand, window-expand |
| `window-takeover` | media | step | canvas | - | 2 | W3-ME2 | inline-image-expand, scroll-grid-expand |
| `word-door` | media | step | kinetic | kinetic | 3 | W3-ME2 | text-window-fill, text-cutout-zoom, split-slide, inline-image-expand |
| `divider-split` ← compare-ledger | assemble | enter | canvas, data | - | 2 | W3-AS | split-slide, push-transition, line-draw, split-compare, count-up |
| `pin-drop` | assemble | enter | canvas | - | 2 | W3-AS | map-event-accumulation, fade-slide |
| `transcript-condense` | assemble | step | launch | - | 2 | W3-AS | aggregate-split-merge, token-split, highlight-sweep |
| `depth-ladder` | emphasis | ambient | zoom | zoom | 2 | W3-EM | active-indicator-glide, progressive-disclosure, route-highlight |
| `ladder-callout` | emphasis | enter | zoom | - | 2 | W3-EM | annotation-callout, line-draw, sequence-message-draw |
| `port-aim` | emphasis | step | zoom | - | 2 | W3-EM | focus-contraction, spotlight, annotation-callout, zoom-to-detail |
| `recede` ← chart-recede, region-recede | emphasis | exit | canvas, data | - | 1 | W3-EM | chart-filter-fade, fade-slide, fade, atmospheric-depth |
| `rule-mark` | emphasis | step | zoom | - | 2 | W3-EM | line-draw, underline-draw, annotation-callout |

## 4. 라이브러리 공통 규칙 (모든 move)

- 플러그인 금지: SplitText·Flip·MorphSVG·DrawSVG·CustomEase 안 씀(harness `plugins = {}`, 결정론). 선은 `pathLength=1` dash, 운반은 `transferVars`, 글자는 beat part.
- move 사이 상태 공유 금지: 앞 move의 overlay·변수를 읽지 않는다. dot-multiply → dots-pour, line-to-waffle → waffle-recount처럼 이어지는 격자는 `_shared/grid.js` 순수 배치를 각자 다시 계산.
- 측정은 anchor·handoff rect만(getBoundingClientRect 직접 금지). 색 목표는 `_shared/color.js`(var( 금지 규칙과 충돌 없이 해석된 값).
- 컨셉별 질감은 move 안에서 컨셉 id로 분기하지 않는다(params·tokens만). `ctx.tokens` 값이 있으면 param 기본값보다 우선하는 키: `blurMax`(blur 상한), `stagger`(params에 stagger가 없을 때), `dimOthers`, `depthNear·depthFar`.
- 「짜침」 회피 수치·결정론 체크·계약 v2 임시 규칙은 지시서 공통 블록(`plan/briefs/W3-*.md` 「공통 규칙」 이하)이 정본.

## 5. 공용 helper `moves/_shared/` (W3-S0, 다른 잡보다 먼저)

모든 helper는 `moves/_shared/<name>.js` 한 파일 = 한 주제, 옆에 `<name>.test.js`(check-tests 면제 폴더지만 테스트는 필수). import는 `../../engine/index.js`만. gsap은 import하지 않고 인자로 받은 `tl`·`ctx.gsap`만 쓴다. 전부 순수하거나, `tl`에 tween을 추가만 한다(바깥 상태 없음).

| 파일 | export | 뜻 |
|---|---|---|
| `timeline.js` | `seg(d, a, b) → { at, duration }` | 비율 구간 a..b(0..1)를 길이 d의 local 시각으로. `tl.to(x, { …, duration }, at)`에 그대로 씀 |
| | `slots(n, { start, span, each, compress = 1, minRatio = 0.4 }) → Array<{ at, duration }>` | n개 항목 stagger 시각. compress < 1이면 간격이 k번째마다 compress배(최소 minRatio배)로 줄어듦(time compression). 순수 |
| | `px(ctx, n) → number` | `n × ctx.viewport.px` |
| | `clamp(v, lo, hi)`, `lerp(a, b, t)` | |
| `link.js` | `finishLink(tl, ctx, { at, cross = 0.12, from = [ctx.handoff.from.node], to = [ctx.handoff.to.node] })` | `ctx.initial(to, { autoAlpha: 0 })` 선언 + `at − cross`..`at` 구간 from 1→0·to 0→1(cross는 0.15로 clamp) + `at`에 `tl.set(to, {autoAlpha:1})`·`tl.set(from, {autoAlpha:0})`. C7 소유권 규칙의 유일한 구현 |
| | `ghost(ctx, node, rect) → HTMLElement` | node를 `cloneNode(true)`해 `ctx.overlay`에 `position:absolute; left:rect.x; top:rect.y; width:rect.w; height:rect.h; margin:0`으로 놓은 대역. `data-part` 제거, `dataset.slRect = JSON.stringify(rect)`(contract-check가 최종 rect 계산에 씀). 원본은 건드리지 않음(숨김은 호출자가 `ctx.initial`/`tl.set`) |
| | `carriedRect(node, gsap) → Rect` | `dataset.slRect` 기준 + gsap x·y·scaleX·scaleY(origin 0 0)로 현재 rect 계산. 테스트·자기검사용 |
| `stroke.js` | `svgLayer(ctx) → SVGSVGElement` | `ctx.overlay` 안 전체 무대 SVG(`viewBox 0 0 w h`, `position:absolute; inset:0; overflow:visible; pointer-events:none`) |
| | `path(svg, d, attrs?) → SVGPathElement` | `pathLength="1"`, `fill="none"`, `stroke-dasharray="1 1"`, `stroke-dashoffset="1"`(안 그려진 상태) |
| | `line(svg, x1, y1, x2, y2, attrs?)`, `polyline(svg, pts, attrs?)` | 같은 규칙의 path |
| | `drawOn(tl, path, { at, duration, from = 0, to = 1, ease })` | `fromTo(path, { strokeDashoffset: 1 − from }, { strokeDashoffset: 1 − to, immediateRender: false, … })`. DrawSVG·getTotalLength 대체 |
| | `pointOnPolyline(pts, t) → Point` | 꼭짓점 배열 길이 비례 선형 보간(순수). 선 머리 이름표·마커 위치용 |
| `count.js` | `formatNumber(v, { lang = 'ko', decimals = 0, prefix = '', suffix = '' }) → string` | `Intl.NumberFormat(lang, { minimumFractionDigits: decimals, maximumFractionDigits: decimals })` |
| | `countTo(tl, node, { from, to, at, duration, ease, lang, decimals, prefix, suffix })` | build 때 `node.textContent = formatNumber(from)`, proxy `{v}` fromTo(immediateRender:false), onUpdate에서 textContent = formatNumber(v). onUpdate는 v만 읽음(누적 상태 없음) |
| `reel.js` | `buildReel(host, text) → Reel` | 숫자 자리마다 0–9 세로 스택(`span.sl-reel__col[data-place] > span×10`), 숫자 아닌 글자는 고정 span. host 내용을 대체. `Reel = { cols: Element[], text }` |
| | `reelFrom(counterEl) → Reel` | 렌더러가 이미 만든 chronology counter(v2: `[data-place]` 열, `data-digit`)를 같은 Reel 형태로 감쌈(DOM 변경 없음) |
| | `rollReel(tl, reel, fromText, toText, { at, duration, ease, stagger = 0, steps = false })` | 바뀌는 자리만 `yPercent = −digit×10` fromTo. 자리 수가 다르면 왼쪽에 폭 0→1로 열리는 새 자리. steps면 `ease: 'steps(n)'` |
| `mask.js` (계약 v2 대기 TEXTMASK) | `applyTextMask(ctx, node, text, { rect, align, font })` | `ctx.textMask?.(text, { rect, align })`(v2, 컨셉 display 글꼴) 또는 engine `textMask(text, { font: font ?? '900 160px sans-serif', width: rect.w, height: rect.h, align })`로 data URL을 만들어 `ctx.initial(node, { maskImage, webkitMaskImage, maskSize: '100% 100%', maskRepeat: 'no-repeat', maskPosition: '50% 50%' })` |
| | `clearMask(tl, node, at)` | `tl.set(node, { maskImage: 'none', webkitMaskImage: 'none' }, at)` |
| `media.js` (계약 v2 대기 FRAMESEQ) | `frameSeqOf(beat) → FrameSeq \| null` | `beat?.media?.seq ?? null`(v2 초안 `BeatInstance.media`). v2 확정 뒤 이 한 곳만 고침 |
| | `scrubTo(tl, seq, { from, to, at, duration, ease = 'none' })` | proxy `{p}` fromTo, onUpdate에서만 `seq.setProgress(p)`. seq null이면 proxy만 만들고 호출 생략 |
| `color.js` | `colorOf(ctx, name) → string` | `ctx.colors?.[name]` → `getComputedStyle(ctx.stage.root).getPropertyValue('--sl-' + name).trim()` → 고정 대체값(fg #ffffff, bg #000000, accent #ffb000, accent-2 #4cc9f0, fg-muted #8a8a8a, rule #444444, scrim rgba(0,0,0,0.55)). `var(` 반환 금지 |
| `words.js` | `wordsIn(beat, partName) → Element[]` | partName 요소 안의 `[data-part="word"]` 목록, 없으면 `beat.part('word')` |
| | `ghostWords(ctx, node, rect) → Element[]` | `ghost` 뒤 그 안 텍스트를 engine `words`로 어절 span 분할한 대역(prompt result처럼 어절 part가 없을 때) |
| `scramble.js` | `scrambleTable(rng, length, frames, glyphs) → string[][]` | build 때 ctx.rng로 미리 뽑은 기호 표(frames×length) |
| | `scrambleAt(from, to, p, table) → string` | 순수: p=0 → from, p=1 → to, 고정 글자 수 = floor(p×to.length), 나머지 자리 = table[floor(p×(frames−1))][i]. 폭은 max(from, to) 길이 |
| `grid.js` | `gridLayout({ n, cols, cell, gap, origin, order = 'row', from }) → Array<{ x, y, i }>` | 순수 격자 좌표. order 'near'면 from 점에서 가까운 칸부터 |
| | `canvasLayer(ctx) → { canvas, g }` | overlay 안 canvas(viewport × dpr). `g = canvas.getContext?.('2d') ?? null`(happy-dom은 null) |
| | `drawDots(layer, dots, { r, color })` | g가 null이면 아무것도 안 함(예외 금지) |
| `contract-check.js` | `checkMove(move, scenario, createHarness) → string[]` | C17 move 테스트 1~7을 실행해 실패 문장 목록을 돌려줌(vitest import 금지 — 테스트가 `expect(checkMove(…)).toEqual([])`). 아래 상세 |

`checkMove` 상세:
- `scenario = { beats, rects?, viewport?, concept?, run: { role, beat, from?, params? }, prepare?(h), nodes?(h, ctx) → Element[] }`. `prepare`는 runMove 전에 harness beat를 손질(노드 추가·`beat.media` 주입)하는 훅.
- 1 `createRegistry([move])`가 throw하지 않음. 2 `move.timing(params, data)` 2회 deepEqual, role이 ambient가 아니면 duration > 0, `'fill'`은 ambient만. 3 `tl.duration() ≤ timing.duration + 0.001`. 4 대상 노드 = `nodes()` 또는 모든 beat part 노드 + overlay 자손. seek(0.37d)→스냅샷 A, seek(0.81d), seek(0.37d)→스냅샷 B, A와 B 같음(props `x y scaleX scaleY opacity` + inline style + textContent). 5 seek(0) 스냅샷 → seek(d) → seek(0) 스냅샷 같음. 6 새 harness(reduce: true)로 다시 돌려 seek(0, 0.5d, d)마다 모든 노드 inline style에 `blur(`가 0이 아닌 값으로 없음, family가 camera가 아니면 `rotateX|rotateY|translateZ|perspective|matrix3d` 없음. 7 role이 link면 seek(d)에서 `ctx.handoff.to.node` 보임(opacity 1, visibility ≠ hidden)·`ctx.handoff.from.node` 숨김, 그리고 운반 노드(`scenario.carry?.(h, ctx)` 기본 from.node)의 최종 rect(`carriedRect` 또는 getBoundingClientRect)가 `handoff.to.rect`와 ±1px. `scenario.carry === null`이면 rect 검사 생략(운반 없이 여는 link: rail-split-open·era-shift 등).


## 6. 계약 v2 대기

| 표시 | 내용 | move |
|---|---|---|
| ANCHOR_INDEX | anchor(part, index)·음수 index·MoveDef.handoff(params, {from,to}) 선택 함수·skipNodes(#7·#8, C5 v2 상자 1~3) | `aggregate-split` `annotation-pin` `caret-blink` `counter-handoff` `dots-pour` `era-shift` `forecast-extend` `glyph-to-bar` `into-word` `ladder-callout` `line-focus` `line-to-waffle` `mark-morph` `phrase-fold` `pin-drop` `point-focus` `port-aim` `push-build` `rail-advance` `rail-compress` `rail-drop` `rail-lift` `rank-reorder` `result-stream` `scramble-swap` `slot-pick` `strike-swap` `threshold-line` `zoom-dive` `zoom-surface` |
| FRAMESEQ | ctx.beat.media.seq / ctx.from.media.seq (#16·#20, C5 v2 상자 4) | `frame-scrub` `iris-to-dot` `lit-from-dark` `rail-drop` `rail-split-open` `scrub-callouts` `sticky-scrub-link` `video-scrub` |
| OVERLAY_LIFE | overlay 수명 = span 시작 ~ beat 끝(#19, C5 v2 상자 6) | `annotation-pin` `caret-blink` `depth-ladder` `dot-multiply` `forecast-extend` `line-to-waffle` `mark-morph` `port-aim` `rule-mark` `scrub-callouts` `threshold-line` `waffle-recount` `zoom-surface` |
| TEXTMASK | ctx.textMask(text, {rect, align}) + move가 ctx.initial로 적용(#17, C5 v2 상자 5) | `glyph-to-bar` `into-word` `mask-word-in` `text-mask-dive` `word-door` |
| CHART_PARTS | chart part title·dek·note(data-index)·baseline, orient h, 음수(#9~#11, C4 v2) | `aggregate-split` `annotation-pin` `baseline-grow` `diverge-grow` `dot-multiply` `dot-seed` `dots-pour` `forecast-extend` `glyph-to-bar` `ink-in` `iris-to-dot` `line-draw` `line-to-waffle` `mark-morph` `rank-reorder` `recede` `threshold-line` `waffle-recount` `zoom-dive` `zoom-surface` |
| CHART_STATES | ctx.step {name,index} + [data-state] 상태 층, 값·모양 바꾸는 step은 reduce self(#12, C5 v2 상자 10) | `annotation-pin` `dot-multiply` `forecast-extend` `mark-morph` `threshold-line` `waffle-recount` |
| CHRONO_PARTS | chronology dot·stem·label·caption·counter(reel data-place·data-digit)·ground(ghost)·now·ticks·data-weight(#2~#6, C4 v2) | `counter-handoff` `era-shift` `fold-to-rail` `pin-drop` `rail-advance` `rail-compress` `rail-draw` `rail-drop` `rail-lift` `rail-settle` `rail-split-open` `rail-surface` |
| PROMPT_WORDS | prompt result 어절 part word(#24, C4 v2) | `phrase-fold` `result-stream` `transcript-condense` |
| PRESETS | concept moves.params 컨셉별 param 프리셋(설계자 요청 1, v2 커밋 6dbd55c에 없음 — 미결) | `blur-drop` `count-roll` `divider-split` `focus-pull` `line-draw` `line-mask-rise` `mask-word-in` `recede` `type-on` `window-open` |
| PERSIST | beat persist: true(#1, C3 v2) | `recede` |
| HARNESS | harness prev·next·camera·step·skipNodes·media·rects "#index"(C17 v2) | `arc-flight` `atlas-pullback` `establish-crane` `rail-settle` |

- v2 커밋 뒤: `_shared/media.js frameSeqOf`·`_shared/mask.js`·harness 시나리오만 고치는 수리 잡(Hat: refactor) 1개로 맞춘다. move 본문은 임시 규칙대로 이미 v2 호출 형태(`anchor(part, index)`, `state` param)로 쓰므로 고칠 곳이 적다.

## 7. registry 결합 (C16)

- `moves/<family>/index.js`: `import <camelId> from './<id>.js';` 줄을 id 알파벳 순으로, `export default [<camelId>, …];`(같은 순서). 이 폴더 밖 import 금지. **메인 소유** — 잡은 건드리지 않고, 메인이 병합 때 한 줄씩 추가(한 family를 여러 잡이 나눠 쓰므로 index 충돌을 없애려는 것).
- `moves/index.js`(메인): 9 family index를 모두 import해 `createRegistry([...assemble, ...camera, ...data, ...emphasis, ...media, ...morph, ...rail, ...reveal, ...type])`. 스캐폴드 완료(빈 배열, 내장 engine:* 4개만 등록됨).
- 병합 뒤 family index 최종 내용은 `plan/WORK-SPLIT-W3.md` §5에 그대로 있음.

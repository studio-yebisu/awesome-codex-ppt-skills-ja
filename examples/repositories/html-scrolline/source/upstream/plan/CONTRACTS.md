# Scrolline v2 — 인터페이스 계약 정본 (CONTRACTS)

- **계약 판 v2 (2026-10-08)**: W2 병합 뒤 개정 요청 27건 반영(결정 원장 `plan/CONTRACT-REQUESTS.md`, 엔진 반영 잡 `plan/WORK-SPLIT-v2.md`). 바뀐 절마다 「v2 변경」 줄로 표시. 「v2 변경」이 붙은 기능은 해당 E2 잡 병합 전까지 엔진에 없을 수 있음(잡 id 병기).

- 이 문서가 워커 지시서의 인용 원본. 코드가 이 문서와 다르면 코드가 틀린 것.
- 계약 변경은 메인만 한다(이 파일 + `engine/types.js` + `engine/constants.js` 동시 수정, 커밋 1개, `Hat: refactor`).
- 표기: `u` = timeline 단위(GSAP 초와 같은 수, 의미는 「스크롤 거리 단위」). `px` = CSS px. 좌표는 전부 **stage-local**(stage 루트 왼쪽 위 = 0,0).
- 타입 정본은 `engine/types.js`(JSDoc typedef). 이 문서의 TS 표기는 읽기용.

---

## C0. 폴더·파일 위치

| 경로 | 소유 | 내용 |
|---|---|---|
| `engine/index.js` | 메인(동결) | 공개 API 재수출. 다른 층은 이 파일만 import |
| `engine/types.js` | 메인(동결) | JSDoc typedef 정본 |
| `engine/constants.js` | 메인(동결) | 이벤트 이름·CSS 변수 이름·키·정규식 상수 |
| `engine/stage.js` | W2-E1 | `createStage`, `computeViewport` |
| `engine/util/{dom,rng,schema}.js` | W2-E1 | DOM 도우미·seeded RNG·schema 검사 |
| `engine/engine.css` | W2-E1 | 무대 기본 CSS(`--sl-*` 소비) |
| `engine/a11y.js` | W2-E1 | reduced-motion·aria-live·transcript·inert |
| `engine/timeline.js` | W2-E2 | `plan`(순수), `build`, 내장 fallback move |
| `engine/registry.js` | W2-E2 | `createRegistry` |
| `engine/deck-schema.js` | W2-E2 | `validateDeck`, 내용 감사 |
| `engine/scroll.js` | W2-E3 | `createScrollDriver`(Lenis + ScrollTrigger) |
| `engine/presenter.js` | W2-E3 | `createPresenter` 발표 키 |
| `engine/handoff.js` | W2-E4 | `measure`, `anchorOf`, `rectIn`, `toInset`, `transferVars` |
| `engine/testing.js` | W2-E4 | move·beat 테스트 harness(테스트 전용 진입점) |
| `engine/beats/*.js` | W2-E5 | beat 렌더러 10종 + `index.js` |
| `engine/media.js` | W2-E6 | `frameSequence`, `videoClip`, `textMask`, `preloadImages` |
| `tools/media/extract-frames.mjs` | W2-E6 | ffmpeg 프레임 추출 |
| `engine/export.js` | W2-E7 | `exportPath`(순수), `buildExportTimeline` |
| `tools/export.mjs`, `tools/capture.mjs` | W2-E7 | HyperFrames 렌더·스냅샷 래퍼 |
| `engine/boot.js` | W2-E8 | `boot` 통합 진입 |
| `decks/_smoke/**`, `tools/cli.mjs` | W2-E8 | 통합 확인 덱·CLI |
| `moves/<family>/<id>.js` + `<id>.test.js` | W3 family별 1잡 | move 1개 = 파일 1개 + 테스트 1개 |
| `moves/<family>/index.js` | 그 family 잡 | family의 move 배열 export |
| `moves/index.js` | 메인 | family index 묶음 + registry |
| `concepts/<id>/{concept.json,tokens.css,index.js}` | W2 컨셉 잡(opus) → W3 | 컨셉 팩 |
| `concepts/<id>/layout.css` (+ `layout.test.js`) | 그 컨셉(덱 통합 담당) | **v2.2** 컨셉 고유 배치 CSS(C11, #49). 선택 |
| `decks/<id>/{deck.yaml,index.html,main.js,assets/,sequences/}` | W4 덱 잡 | 덱 |
| `tools/check*.mjs` | 메인 | 게이트 |
| `state/board.json`, `state/runs.jsonl` | 메인만 씀 | 상태 정본 |

- 테스트 파일은 대상 옆에 `<name>.test.js`. 다른 위치 금지.
- 새 engine 파일 추가는 계약 변경(메인 승인).
- **v2 변경**: 같은 모듈의 회귀 테스트를 `Hat: refactor` 커밋에서 더할 때는 기존 테스트를 고치지 않고 옆에 `<name>.<주제>.test.js`를 새로 만든다(예: `engine/deck-schema.fixes.test.js`). `engine/constants.js`에는 C19 밖 engine 내부 상수도 둘 수 있고, `engine/index.js`는 C19 이름만 골라 내보낸다.

---

## C1. 의존 규칙 (`tools/check-deps.mjs`가 강제)

- 층 순위: `engine`(0) < `moves`(1) < `concepts`(2) < `decks`(3) < `site`(4). `tools/`와 루트 설정 파일은 층 밖(아무거나 import 가능, 아무도 tools를 import 못 함).
- **R1 하향만**: 파일은 자기 층 이하만 import.
- **R2 공개 진입점만**: 다른 층에서 들어올 때 대상은 다음 중 하나여야 함.
  - `engine/index.js`, `engine/engine.css`, `engine/testing.js`(`*.test.js`에서만)
  - `moves/index.js`
  - `concepts/<id>/index.js`, `concepts/<id>/tokens.css`, `concepts/<id>/layout.css`(v2.2)
- **R3 순환 금지**: 파일 단위 import 그래프 전체에 cycle 0.
- **R4 형제 격리**: `concepts/a` ↛ `concepts/b`, `decks/a` ↛ `decks/b`, `moves/famA` ↛ `moves/famB`(`moves/_shared/`만 예외로 모든 family가 import 가능).
- **R5 외부 패키지**:
  - `gsap`, `gsap/*`: `engine/**`만. moves·concepts·decks는 `ctx.gsap`·`ctx.plugins`로 받는다.
  - `lenis`: `engine/scroll.js`만.
  - `three`: 금지(W2 범위 밖. 히어로 WebGL은 추후 `engine/media-gl.js` 계약 추가 후).
  - `vitest`: `*.test.js`만. `happy-dom`: `engine/testing.js`만.
  - `yaml`: `tools/**`만(덱은 vite plugin이 넘겨준 객체를 받음).
- 검사 대상 확장자 `.js .mjs`. import 형태 `import … from`, `import '…'`, `export … from`, `import('…')` 모두.

---

## C2. 단위·좌표·뷰포트

- `Viewport = { w, h, portrait, px, dpr }`
  - `portrait = w / h <= 1`
  - `px = portrait ? w / 760 : Math.min(w, h * 16 / 9) / 1920` (디자인 기준 1920 가로 / 760 세로)
  - `dpr = Math.min(devicePixelRatio || 1, 2)`
- CSS: engine이 stage 루트에 `--px`(숫자, 단위 없음), `--vw-px`, `--vh-px`(px 단위 문자열), `--sl-portrait`(0|1) 설정. 글자 크기는 `calc(var(--px) * N * 1px)`.
- `Rect = { x, y, w, h }`(stage-local px, transform 이전 layout box 기준). `Point = { x, y }`.
- **timeline 단위 u**: 스크롤 1u = `viewport.h × timing.unit` px. 기본 `unit = 0.55`.
- **track 높이** = `h + duration × h × unit` px.
- **world 좌표**(canvas·zoom 컨셉): `x`, `y` 단위 = 화면 1장(x=1 → 화면 너비만큼 오른쪽), `z` = px 깊이, `s` = 배율. world 원점 = 첫 화면 왼쪽 위.

---

## C3. deck.yaml 스키마

```yaml
id: rail-history            # ^_?[a-z0-9][a-z0-9-]*$, 폴더 이름과 같음(v2: `_`로 시작 = 내부 덱)
title: "…"
lang: ko                    # ko | en
concept: rail               # concepts/<id>
sample: false               # true면 가상 회사 표본: 화면에 「표본」 표기 의무, source 면제
sources:                    # 출처 원장(수치·인용·사진은 source id 필수, sample:true 덱 제외)
  - { id: s1, title: "…", url: "https://…", accessed: "2026-10-08" }
timing:                     # 선택. concept.timing 덮어쓰기
  unit: 0.55
  hold: 0.6
  overlap: 0.2
export:                     # 선택. exportPath 옵션 덮어쓰기
  secondsPerUnit: 0.5
beats:
  - id: b-open              # 덱 안에서 유일, ^[a-z0-9][a-z0-9-]*$
    type: text              # C4 beat 종류
    # … type별 필드(C4)
    place: { slot: center } # 또는 { world: { x: 0, y: 0, z: 0, s: 1 } }
    enter: { move: word-rise, params: { stagger: 0.12 }, at: 0 }
    steps:                  # 선택. 머문 뒤 이어지는 동작(차트 변신 등), 각 step 끝에 정지점
      - { name: q4, move: bar-to-line, params: {} }
    exit:  { move: blur-out }
    link:  { move: match-cut, params: { fromPart: frame, toPart: media } }  # 다음 beat로 이음. 있으면 exit 무시
    camera: { move: fly-to, params: {} }   # 선택. beat 시작에 카메라 이동
    ambient: [ { move: ken-burns } ]       # 선택. beat 수명 내내
    stop: true              # 기본 true. false면 주 정지점 없음
    hold: 0.8               # 선택. 정지점 뒤 머무는 u
    at: 0                   # 선택. 앞 beat 기준 시작 오프셋(C6)
    exportHold: 2.0         # 선택. MP4 내보내기에서 이 정지점 머무는 초
    repeat: intended        # 선택. 같은 move 덱 안 2회 이상 허용 사유
    persist: false          # 선택(v2). true면 beat 끝에 숨기지 않음. place.world beat만
    tone: 2                 # 선택(v2). 0..5 정수 → 루트 data-tone. tokens.css가 C11 변수만 재정의
    source: s1              # 수치·인용·실사 beat. v2: 문자열 또는 문자열 배열 [s3, s4]
```

**v2 변경 (C3)**
- deck `id`는 `DECK_ID_PATTERN = ^_?[a-z0-9][a-z0-9-]*$`. `_`로 시작하는 덱(`decks/_smoke`)은 내부 덱: 갤러리·다양성 게이트·export 일괄 대상에서 빠진다. beat id·move id는 그대로 `ID_PATTERN`(`_` 불가).
- 공통 beat 필드 3개 추가: `persist`(C6 build ⑥), `tone`(C11), `source` 배열 허용. 이 셋과 C3 표의 공통 키는 beat type `fields`에 넣지 않고 validateDeck이 따로 검사한다(`source`만 예외: 출처를 화면에 그리는 type은 `fields.source`를 `type: 'any'`로 둔다).
- `sources[]` 항목에 선택 `short`(화면 L3용 짧은 이름, 예 `arXiv`·`Reuters`) 추가. 렌더러 출처 표기는 `short ?? title`.
- 마지막 beat에는 컨셉 기본 exit을 붙이지 않는다(직접 적은 `exit`만). C6 「마지막 beat가 그대로 남는 경우」가 기본이 됨(rail.md 8.2, E2-1·E2-6).
- `at` 양수는 앞 beat 퇴장 시작 뒤 틈(빈 화면), 음수는 겹침. 결과 `s`는 `prev.start` 아래로 내려가지 않는다(C6 그대로).
- `link`가 있는 beat의 `exit`(직접 적었든 컨셉 기본값이든)는 plan과 validateDeck 모두 무시한다.
- `MoveRef = { move: string, params?: object, at?: number, override?: string }`
  - `override`: 컨셉 허용 목록 밖 move를 쓸 때 사유 문자열(없으면 검증 실패).
- 기본값 해석 순서: beat 필드 → `concept.defaults.byType[type].{enter,exit,link}` → `concept.defaults.{enter,exit}` → 내장 `engine:fade-in` / `engine:fade-out`.
- `link`가 있는 beat는 마지막 beat일 수 없음.

### 내용 감사 (`validateDeck`가 강제, luna 사건 대응)
- 모든 문자열 필드에 대해 `PLACEHOLDER_PATTERNS`(engine/constants.js) 매치 시 오류: `TODO`, `TBD`, `lorem`, `ipsum`, `xxx`, `「x」`, `???`, `{{`, `}}`, `<placeholder>`, `자리표`, `예시 문구`, 빈 문자열, 공백만.
  - v2 명시: 검사 범위 = 덱 객체 전체(move `params` 안 문자열·`states[]`·`notes[]` 포함).
- `number`, `chart`, `quote`, `photo`(실사)에는 `source` 필수(`sample: true` 덱 제외). **v2**: `compare`도 `items[].value`가 하나라도 있으면 필수(`SOURCED_TYPES`). `source`는 `sources[].id` 하나 또는 그 배열(빈 배열·중복·없는 id 오류).
- 같은 move id가 덱 안에서 같은 role로 2회 이상 → `repeat: intended` 없으면 오류. **v2**: `engine:none`(`NO_MOVE`)은 반복 검사 면제. 반복 키는 (role, move id) 쌍으로 비교(콜론 든 id를 자르지 않음, #15 수리).
- 컨셉 `moves.allow` 밖 move → `override` 없으면 오류.
- **v2 추가 검사**(E2-6): `persist: true`는 `place.world` beat만(screen beat면 오류) · `tone`은 `TONE_RANGE` 0..5 정수 · chart `states[].name`이 `base`(`BASE_STATE`)면 오류 · chart `states[].name`은 그 beat `steps[].name` 중 하나와 같아야 함 · chart `notes[].index`·`highlight.index`는 `0..categories.length-1` · link `accepts`는 **다음 beat** type으로 검사(#21 수리) · `engine:none`은 role 검사 면제(#22 수리).

---

## C4. beat 종류와 데이터 스키마

- beat 렌더러 = DOM과 part만 만든다. **움직임은 0**(move 몫). 렌더 직후 상태 = 「정지점에서 보이는 완성 상태」.
- 모든 beat 루트: `<section class="sl-beat sl-beat--<type>" data-beat="<id>">`. 렌더러는 class까지 만들고 `data-beat`는 build(테스트에선 harness)가 채운다. 각 part 요소에 `data-part="<name>"`. 루트 자신은 `parts`에 넣지 않는다.
- `parts`는 항상 `Record<string, Element[]>`(하나여도 배열).
- 텍스트는 실제 DOM 글자(canvas 금지). 한국어는 어절 단위(`words`), 타이핑은 글자 단위(`chars`).
- 숫자는 `Intl.NumberFormat(lang)` 포맷. 단위·접두는 별도 span.

**v2 변경 (C4 공통)**
- part 요소 class = `sl-<type>__<part>`(sequence는 `sl-seq-<use>__<part>`). **build(와 harness)가 render 직후 모든 part 요소에 이 class를 더한다**(렌더러가 이미 넣었으면 그대로, E2-1). 렌더러의 다른 class(`sl-chart` 등)는 자유. engine.css·move는 이 이름만 믿는다(E2-2 CSS가 이 규칙으로 씀).
- `source` 표기: part `source` 1개, 글자 = 출처마다 `rc.sources[id].short ?? .title`(없으면 id)을 ` · `로 이음. `<a href>`는 넣지 않는다(발표 화면).
- `BeatView.media?: { seq?: FrameSeq, clip?: Clip }` — video 렌더러가 만든 핸들. build가 `BeatInstance.media`(없으면 `{}`)로 옮긴다(#16·#20).
- **상태 층**(`data-state`): 정지점 뒤 step이 바꿀 글자(chart `states[]`의 title·dek·note)는 렌더러가 미리 그린다. 기본 상태 요소 = `data-state="base"`, 상태 k 요소 = `data-state="<states[k].name>"`. base 아닌 층은 렌더 직후 `style.visibility = 'hidden'; style.opacity = '0'`. 상태가 어떤 글자 필드를 생략하면 앞 상태 값을 물려받아 그 층에 복제해 그린다(move는 층 하나만 켜고 끄면 됨). 같은 part 이름을 쓰므로 `part('title')`은 모든 층을 돌려준다(`[data-state]`로 거름).
- 렌더러가 받는 `rc`(v2): `{ viewport, lang, asset, media: { frameSequence, videoClip }, el, words, chars, sources, mode }`. `sources` = `deck.sources`를 id로 묶은 객체, `mode` = `'live'|'export'`.

| type | 필수 필드 | 선택 필드 | parts | primary |
|---|---|---|---|---|
| `text` | `text: string` | `emphasis: string[]`(부분 문자열), `size: xl\|l\|m`, `lines: string[]`(명시 줄) | `block`, `line`, `word`, `em` | `block` |
| `photo` | `src: asset`, `alt: string` | `focus: {x,y}`(0..1), `caption`, `credit`, `source` | `frame`, `media`, `caption` | `frame` |
| `video` | `src: asset`(mp4), `poster: asset`, `alt`, `mode: scrub\|play\|loop` | `frames: asset`(frames.json, scrub 필수), `caption`, `mask: {type: text\|shape, text?, shape?}`, `source`, **v2** `credit` | `frame`, `media`, `caption`, **v2** `credit` | `frame` |
| `number` | `value: number`, `label: string` | `format: {prefix, suffix, decimals, unit}`, `from: number`(count-up 시작), `source` | `value`, `digits`, `unit`, `label`, `source` | `value` |
| `chart` | `kind: bar\|line\|area\|dot`, `categories: string[]`, `series: [{name, values: number[]}]` | `unit`, `highlight: {series?, index?}`, `states: [{name, kind?, series?, `**v2** `title?, dek?, notes?, unit?}]`(steps용), `source`, **v2** `title`(L1 결론), `dek`(L2 보충), `notes: [{index, series?, text}]`, `orient: v\|h` | `plot`, `axis`, `mark`, `label`, `legend`, `source`, **v2** `title`, `dek`, `note`, `baseline` | `plot` |
| `chronology` | `events: [{date, title}]`(2개 이상) | `events[].note`, `events[].media`, `scale: even\|time`, `axis: x\|y`, **v2** `events[].weight: major\|minor`, `events[].source`, `label`, `caption`, `counter: none\|year\|month`, `ground: boolean`, `now: number`(0..1), `ticks: none\|year` | `track`, `event`, `date`, `title`, `note`, `media`, **v2** `dot`, `stem`, `source`(event 안), `label`, `caption`, `counter`, `reel`, `ground`, `ghost`, `now`, `tick` | `track` |
| `compare` | `items: [{label}]`(2~4개) | `items[].value`, `items[].text`, `items[].media`, `verdict`, **v2** `source` | `item`, `label`, `value`, `text`, `divider`, `verdict`, **v2** `source` | `item` |
| `quote` | `text`, `by` | `role`, `source` | `block`, `mark`, `word`, `by` | `block` |
| `prompt` | `text` | `label`, `result: {type: photo\|text, src?, text?, alt?}` | `field`, `char`, `caret`, `label`, `result`, **v2** `word`(result 글 어절) | `field` |
| `code` | `code`, `lang` | `highlight: [[from,to]]`(1-base 줄 범위), `caption` | `block`, `line`, `token`, `caret` | `block` |
| `sequence` | `use: string`(덱 전용 sequence 이름) | `data: any` | sequence가 정의 | sequence가 정의 |

- `chart` 렌더: SVG `viewBox="0 0 1600 900"`, mark마다 `data-series`, `data-index`. 축 눈금은 정적.
  - **v2 변경 (chart, #9·#10·#11·#12, E2-3)**: 이름 통일 — L1 = `title`, L2 = `dek`, 표식 주석 = `notes[]`(part `note`). zoom 덱의 `note:`(단수 문자열)는 `dek:`로 바꾼다(별칭 없음).
  - `title`·`dek`는 SVG 밖 HTML(`h2.sl-chart__title`, `p.sl-chart__dek`), plot 위. `notes[k]` → `p.sl-chart__note`에 `data-index`·`data-series`(생략 시 `0`), 위치 = 해당 mark 옆(viewBox 좌표를 % 위치로 환산한 inline `left/top`).
  - `orient: h` = 가로 막대(범주가 y축 위→아래, 값이 x축). `bar`에서만 의미, 다른 kind는 무시.
  - 음수: 값 영역 = `[min(0, 최소값), max(0, 최대값)]`(둘 다 0이면 `[0, 1]`). **v2.2 (#50)**: 선택 필드 `domain: { min?, max? }`는 영역을 넓히기만 한다 = `[min(domain.min, 최소값, 0), max(domain.max, 최대값, 0)]`(전후 비교 차트가 같은 눈금). 렌더러는 실제 영역을 `svg.sl-chart`의 `data-min`·`data-max`에 적는다 — 값→좌표를 직접 환산하는 move는 series에서 다시 계산하지 말고 이 값을 읽는다. 막대는 0 기준선에서 위·아래(h면 좌·우)로. 0 기준선 = part `baseline`(`line.sl-chart__baseline`, 값 영역에 음수가 있을 때만). mark에 `data-sign="neg"|"pos"`.
  - `states[]`: 글자 필드(`title`·`dek`·`notes`·`unit`)는 상태 층(C4 공통)으로 미리 렌더. `kind`·`series` 변화(모양·값)는 step move 몫(렌더러는 base 상태 mark만 그림). 상태 층 순서 = `states[]` 순서.
- `chronology` 렌더: track 위 event를 `scale`대로 배치. `axis: x`면 가로 레일(rail 컨셉).
  - **v2 변경 (chronology, #2·#3·#5·#6, E2-4)**: event마다 `dot`(점)·`stem`(점과 제목을 잇는 줄기) part를 늘 그림. `weight` → event `data-weight`(기본 `major`).
  - `label` → `h2.sl-chronology__label`(장 이름). `caption` → `p.sl-chronology__caption`(L3 한 줄, track 끝 아래). `events[].source` → event 안 `small.sl-chronology__source`(C4 공통 표기, 출처 감사는 id 존재만 — chronology는 `SOURCED_TYPES` 밖).
  - `counter: year|month` → `div.sl-chronology__counter` 안에 자리마다 `reel`(0–9 세로 스택 10칸, `data-place`=자리 순번, `data-digit`=정적 숫자). 정적 상태 = `events[0].date`의 숫자(`year` = YYYY 4자리, `month` = YYYY.MM 6자리, 구분 점은 part 아님). 정적 offset은 inline `transform: translateY(-<digit×10>%)`. move는 첫 tween 전에 `ctx.initial(reel, { y: 0, yPercent: -digit × 10 })`으로 GSAP 상태를 맞춘다. `none`(기본) = 없음.
  - `ground: true` → `div.sl-chronology__ground`(`data-depth="0"`, track 뒤 배경층) 안에 event마다 연도 큰 글자 `ghost`. `now: 0..1` → `div.sl-chronology__now`(beat 루트 너비 기준 x 비율의 세로선). `ticks: year` → track 위 연도 경계마다 `tick`(scale time 기준, even이면 event마다).
- `asset` = 덱 폴더 기준 상대 경로(`assets/…`). 렌더러는 `ctx.asset(path)`로 URL 변환.
- `sequence`(덱 전용): `decks/<id>/sequences/<use>.js` default export = `BeatTypeDef & { timing(data), build(tl, ctx) }`(C5·C7과 같은 시그니처). 엔진은 이 beat의 enter를 sequence 자신의 `build`로 대신한다.
  - **v2 명시 (E2-1)**: plan은 sequence beat의 enter span을 `{ role: 'enter', move: 'seq:<use>', params: {} }`로 기록하고 길이·내부 정지점은 `sequence.timing(data)`에서 얻는다(`beat.enter`를 적으면 validateDeck 오류). build는 그 span에서 `sequence.build(tl, ctx)`를 부른다. exit·link·steps·camera·ambient는 일반 beat와 같음.
- **v2 변경 (그 밖 type)**: `video.credit`(스톡 라이선스 표기, part `credit`) · `compare.source`(part `source`) · `prompt.result.type: text`면 result 안 글을 어절 `word` part로 · `photo`·`number`·`quote`·`chart`·`compare`의 `source`는 문자열 또는 배열(C4 공통 표기 규칙).
- **video 렌더(v2, #16·#17, E2-5)**: `mode: scrub` → `rc.media.frameSequence(host, asset(frames))`, canvas가 part `media`, `BeatView.media.seq` = 그 FrameSeq. `mode: play|loop` → `rc.media.videoClip(host, { src, poster, loop, mode }, { exportMode: rc.mode === 'export' })`, `clip.el`이 part `media`, `BeatView.media.clip` = 그 Clip. `mask.type: text`는 렌더러가 **적용하지 않는다**: media에 `class sl-mask`·`data-mask-text`만 표시(렌더 완성 상태 = 마스크 없는 영상). 마스크를 거는 것은 move(C5 `ctx.textMask`). `mask.type: shape`는 정적 clip이라 렌더러가 `clipPath` 적용(지금과 같음).

### BeatTypeDef (engine/beats/<type>.js default export)
```ts
{
  type: string,
  fields: FieldSchema,                 // C9 schema 형식
  primary: string,                     // 기본 anchor part
  render(data: object, rc: RenderContext): BeatView
}
RenderContext = { viewport: Viewport, lang: 'ko'|'en', asset(p: string): string, media: MediaApi, el, words, chars,
                  sources: Record<string, Source>, mode: 'live'|'export' }          // v2: sources·mode
MediaApi = { frameSequence, videoClip }                                             // v2: C13 함수 그대로
BeatView = { root: HTMLElement, parts: Record<string, Element[]>, media?: { seq?: FrameSeq, clip?: Clip } }   // v2: media
```

---

## C5. move 계약

> **v2 변경 요약 — move 라이브러리 설계자용(MOVES.md·moves/ 작업자는 이 상자만 읽어도 됨)**
> 1. **anchor index**: `beat.anchor(part?, index = 0)`. 음수 index = 뒤에서(-1 = 마지막). `Handoff.index`는 양수로 정규화된 값. 「N번째 막대·사건」을 handoff 대상으로 쓸 수 있다(#7·#8).
> 2. **link가 넘길 part 고르기**: MoveDef 선택 함수 `handoff(params, { from, to }) → { from?: { part?, index? }, to?: { part?, index? } }`(순수, link만). 생략하면 양쪽 primary·index 0. 엔진이 이것으로 `ctx.handoff`를 만든다.
> 3. **skip 규칙**: `ctx.skipNodes: Element[]` 추가 — 이 요소들은 건드리지 않는다(enter·step 모두: `ctx.initial`·들여오기 tween 금지). **v2.2**: step이 그 요소를 「지나간 것」으로 접는 tween(step 구간 안, build 시점 inline style 불변)은 허용(#48). `ctx.skipParts`는 통째로 넘어간 part 이름만(to.index를 지정한 link면 `[]`, 그 요소 하나만 skipNodes). move는 둘 다 지켜야 함.
> 4. **영상 핸들**: `ctx.beat.media = { seq?: FrameSeq, clip?: Clip }`. 스크럽 move는 `scrubTo(tl, seq, …)`(`moves/_shared/media.js`)로 부른다. **v2.2**: tween `onUpdate` 부수 효과 금지 — `seek()`·`pause(t)`·export는 콜백을 억제해 점프 때 안 불린다(launch 통합). 값을 받아 DOM·canvas·프레임에 쓰는 일은 `driveValue(tl, apply, { from, to, at, duration, ease })`(`moves/_shared/drive.js`, tween이 accessor 속성을 직접 써서 setter가 매 렌더 실행)로(C13). link에서 A의 영상은 `ctx.from.media`(#16·#20).
> 5. **글자 마스크**: 렌더러는 `data-mask-text`만 표시, 마스크 적용은 move. `ctx.textMask(text, { rect?, align? }) → data URL`(글꼴 = 컨셉 display 글꼴·굵기, rect 기본 = `ctx.beat.anchor('media').rect`). 적용은 `ctx.initial(media, { maskImage: url, webkitMaskImage: url, maskRepeat: 'no-repeat', … })` 후 `maskSize`·`maskPosition` tween(#17).
> 6. **overlay 수명**: `ctx.overlay`는 span 시작에 보이고 **그 move를 가진 beat가 끝날 때**(`beat.span.end`, persist beat면 끝까지) 숨는다. step·ambient가 만든 링·주석은 beat 끝까지 남는다(#19). 먼저 지우고 싶으면 move가 자기 tween으로 지운다. link span은 받는 beat(B) 소유라 B 끝까지.
> 7. **채워지는 ctx**: `prev`·`next`(앞뒤 BeatInstance), `camera`(camera role: place.world에서 계산, C8), `step: { name, index }`(step role). 
> 8. **engine:none**은 모든 role에 쓸 수 있다(role·반복 검사 면제, #22). link가 B를 다 그리는 설계면 B enter = `engine:none`.
> 9. **link accepts = 받는 beat(B) type**(validateDeck 수리, #21). 보내는 쪽 제한은 build에서 `ctx.from.type` 검사로.
> 10. **상태 층**: chart `states[]`의 글자는 `[data-state="<name>"]` 층으로 미리 그려져 있다(C4). step move는 `ctx.step.name` 층을 켜고 다른 층을 끈다. **값·모양을 바꾸는 step move는 `reduce: 'self'` 필수**(reduce에서도 최종 값이 보여야 하므로 fade 대체 금지).
> 11. **tone·persist**: beat 루트 `data-tone`(색 변수는 CSS가 바꿈, move는 색 tween 시 `ctx.tokens`나 계산값 사용), `persist` beat는 끝에 숨지 않으므로 그 beat의 exit move는 「물러남」(흐림·축소)으로 설계.
> 12. **슬롯 배치는 CSS `translate` 속성**(C8). beat 루트·part의 `transform`은 move 전용이고 측정은 transform을 무시한다.

```ts
// moves/<family>/<id>.js
export default {
  id: 'match-cut',                       // ^[a-z0-9][a-z0-9-]*$, 전역 유일, 파일 이름 = id
  family: 'morph',                       // 폴더 이름과 같음
  role: 'link',                          // enter | exit | link | step | camera | ambient
  accepts: ['photo', 'video'],           // beat type 목록 또는 ['*']. link는 to beat 기준
  sources: ['morph-match-cut'],          // awesome-ai-motion slug(1개 이상, 원리 차용 포함)
  reduce: 'self',                        // 'self' = ctx.reduce 직접 처리 | 'fade' = 엔진이 같은 길이 fade로 대체
  params: { duration: { type: 'number', default: 1.2, min: 0.2, max: 4, doc: '…' }, /* … */ },
  timing(params, data) { return { duration: params.duration, stops: [] }; },   // 순수 함수
  build(tl, ctx, params) { /* tl = 이 move 전용 local timeline, 0부터 */ },
};
```

- **timing은 순수**: 입력은 `params`(기본값 채운 뒤)와 beat data뿐. viewport·reduce·DOM 측정 금지. 같은 입력 → 같은 출력.
  - 반환 `Timing = { duration: number | 'fill', stops?: Array<{ name: string, at: number }> }`. `'fill'`은 `role: ambient`만.
  - `stops[].at`은 move 시작 기준 상대 u. 이름 `^[a-z0-9][a-z0-9-]*$`.
  - link의 `data` = `{ from: A.data, to: B.data }`.
- **build 규칙**
  - `tl`은 local timeline. 위치 인자는 0 기준. 엔진이 `master.add(tl, span.start)`.
  - 끝나면 엔진이 `tl.duration() <= timing.duration + 0.001` 검사(테스트·dev에서 throw).
  - 시작 전 상태는 `ctx.initial(targets, vars)`로만 선언(엔진이 측정 후 일괄 `gsap.set`). `tl.from()` 금지. `fromTo`는 `immediateRender: false` 필수.
  - tween 값에 `var(` 문자열 금지. 수치는 `ctx.tokens`에서.
  - beat 루트(`ctx.beat.root`) 의 `autoAlpha`·`visibility`·`display` 건드리지 않음(엔진 소유). part만 움직임.
  - `ctx.skipParts`에 든 part, `ctx.skipNodes`에 든 요소는 건드리지 않음(link가 이미 넘겨준 것). v2: skipNodes 추가.
  - 무작위는 `ctx.rng()`만. `Math.random`·`Date.now`·`performance.now` 금지.
  - DOM 추가가 필요하면 `ctx.overlay`(이 move 전용 컨테이너) 안에만. 엔진이 수명 관리.
  - 3D 규칙(C10) 준수.
- **role별 시간 배치**: C6 참고. 

### MoveContext
```ts
{
  gsap, plugins: { SplitText, Flip, MorphSVGPlugin, DrawSVGPlugin, CustomEase },
  role: Role,
  beat: BeatInstance,                 // 대상 beat(link면 to)
  from?: BeatInstance,                // link·exit에서 나가는 beat(link면 A, exit면 beat 자신과 같음)
  prev?: BeatInstance, next?: BeatInstance,
  handoff?: { from: Handoff, to: Handoff },   // link만. v2: MoveDef.handoff()가 고른 part·index
  camera?: CameraTarget,              // camera role만: beat.place.world → 목표(v2 식은 C8)
  stage: Stage, viewport: Viewport, reduce: boolean,
  start: number, duration: number,    // 절대 시작 u, 이 move 길이(fill 해석 후)
  skipParts: string[],                // 통째로 넘어간 part 이름
  skipNodes: Element[],               // v2: 건드리지 않을 요소(link가 넘긴 요소)
  step?: { name: string, index: number },   // v2: step role만(name = step.name ?? String(index+1))
  overlay: HTMLElement,               // v2: 수명 = span.start ~ beat.span.end(persist면 끝까지)
  tokens: ConceptTokens,
  ease(alias: 'in'|'out'|'inout'|'scrub'|string): string,   // 컨셉 alias → gsap ease 문자열, 모르는 이름은 그대로
  initial(targets: Element|Element[], vars: object): void,
  rng(): number,                      // [0,1), seed = hashSeed(`${deck.id}:${beat.id}:${role}:${move.id}`)
  textMask(text: string, opts?: { rect?: Rect, align?: 'center'|'left' }): string,   // v2: C13 textMask + 컨셉 display 글꼴
  overlaysOf(beat: BeatInstance): HTMLElement[],   // v2.2: 그 beat의 앞 span move overlay들(이 move의 overlay 제외). exit·link가 나가는 beat의 주석·canvas를 같이 접을 때. engine:fade-out·engine:crossfade(A쪽)·recede가 쓴다
}
// v2: MoveDef 선택 필드
handoff?(params, data: { from: object, to: object }): { from?: { part?: string, index?: number }, to?: { part?: string, index?: number } }   // link만, 순수
```

### BeatInstance
```ts
{
  id, type, data, place,
  root: HTMLElement,
  parts: Record<string, Element[]>,
  part(name: string): Element[],      // 없으면 []
  anchor(part?: string, index?: number): Handoff,   // 측정 스냅샷 기준. part 생략 = primary, index 기본 0·음수 = 뒤에서(v2)
  span: { start, stop, end },         // TimelineMap 값
  media: { seq?: FrameSeq, clip?: Clip },           // v2: BeatView.media(없으면 {})
}
```

---

## C6. 연속 timeline 모델 (`plan` 알고리즘 정본)

- `plan(deck, { registry, concept, beatTypes, sequences }) → TimelineMap`. **DOM 없이 node에서 돈다**(export·검사·테스트가 같은 결과를 씀).
- timing 해석: `T = { unit, hold, overlap, tail } = { …ENGINE_TIMING_DEFAULTS, …concept.timing, …deck.timing }`. 기본 `unit 0.55, hold 0.6, overlap 0.2, tail 0.8`.
- 알고리즘(정확히 이대로):

```
prev = null
for each beat b (i = 0..n-1):
  linkIn = prev?.link                        // 앞 beat의 link가 b로 들어옴
  if i == 0:          s = 0
  else if linkIn:     s = prev.holdEnd + (b.at ?? 0)
  else:               s = prev.exitStart + (b.at ?? T.overlap)
  s = max(s, prev?.start ?? 0)
  t = s
  if linkIn:  L = timing(linkIn); span(link, s, s + L.duration); t = s + L.duration
  if enter:   E = timing(enter); es = max(s, t + (b.enter.at ?? 0)); span(enter, es, es + E.duration)
              internal stops: es + E.stops[k].at → "stop:<b.id>/<name>"
              stopT = es + E.duration
  else        stopT = t
  if camera:  C = timing(camera); span(camera, s, s + C.duration); stopT = max(stopT, s + C.duration)
  if b.stop !== false: label "stop:<b.id>" at stopT
  cur = stopT + (b.hold ?? T.hold)
  for each step k:  D = timing(step); span(step, cur, cur + D.duration)
                    label "stop:<b.id>/<step.name ?? k+1>" at cur + D.duration
                    cur = cur + D.duration + (step.hold ?? T.hold)
  holdEnd = cur
  if b.link:  exitStart = holdEnd; end = (다음 beat 처리 때 link span 끝으로 채움)
  elif exit:  X = timing(exit); span(exit, holdEnd, holdEnd + X.duration); exitStart = holdEnd; end = holdEnd + X.duration
  else:       exitStart = holdEnd; end = holdEnd     // 마지막 beat가 그대로 남는 경우
  ambient:    span(ambient, s, end)  ('fill'이면 end - s)
  prev = { start: s, holdEnd, exitStart, link: b.link }
duration = max(all span ends, all stop labels) + T.tail
```

- **v2 변경 (plan, E2-1)**: sequence beat의 enter = `seq:<use>` span(C4). 내부 정지점은 지금처럼 **enter(와 sequence)만** 기록한다(step·camera의 `stops`는 무시 — 필요한 move는 enter로 설계). map 형식·불변식은 그대로(`version: 1` 유지: v2 필드는 map에 들어가지 않음).

- `TimelineMap`:
```ts
{
  version: 1, deck: string, concept: string,
  duration: number, unit: number,
  stops: Array<{ name: string /* 'b-open' | 'b-open/q4' */, label: string /* 'stop:b-open' */, t: number, beat: string }>,  // t 오름차순
  beats: Array<{ id, type, start, stop, end, spans: Array<{ role, move, start, end, params }> }>,
}
```
- **map 불변식**(테스트 대상): ① stops t 오름차순·이름 유일 ② 모든 span `start <= end` ③ `beats[i].start` 비감소 ④ 같은 deck 입력 → JSON 동일 ⑤ **viewport·reduce·portrait와 무관**(그래서 resize 뒤 같은 t가 같은 내용).
- `build(map, { stage, deck, registry, concept, beatTypes, sequences, reduce, gsap, measureFn? }) → BuiltDeck`
  - 순서: ① 모든 beat `render` + `place` 적용 ② `document.fonts.ready` 뒤 `measure`(모든 beat의 모든 part rect 스냅샷, transform 없는 상태) ③ 모든 move의 `ctx.initial` 수집·적용 ④ master `gsap.timeline({ paused: true, defaults: { ease: 'none' } })`에 span별 local tl을 `add` ⑤ 라벨 추가 ⑥ beat 루트 가시성: `gsap.set(root, {autoAlpha:0})`, `tl.set(root, {autoAlpha:1}, start)`, 마지막 beat 아니고 `persist`가 아니면 `tl.set(root, {autoAlpha:0}, end)` ⑦ master 길이를 `map.duration`으로 맞춤.
  - **v2 변경 (build, E2-1)**
    - ① render에 C4 v2 `rc` 전부(`media`·`sources`·`mode` 포함)를 넘기고, `beat.tone`이 있으면 루트 `data-tone`, `BeatView.media` → `BeatInstance.media`.
    - ⑥ `persist: true` beat는 끝 숨김 `set` 생략(#1). plan·정지점 불변.
    - overlay: span마다 `stage.overlayFor(`${beat}:${role}:${k}:${move}`)`(k = 같은 beat·role 안 순번, 키 충돌 방지). 가시성 = `gsap.set(ov, {autoAlpha:0})`, `tl.set(ov, {autoAlpha:1}, span.start)`, 마지막 beat도 persist도 아니면 `tl.set(ov, {autoAlpha:0}, beat.span.end)`(루트 ⑥과 같은 조건). (#19)
    - ctx: `prev`·`next` = 앞뒤 BeatInstance, `camera` = C8 v2 식, `step` = `{ name, index }`, `skipNodes`, `textMask`, `handoff` = `MoveDef.handoff?.(params, {from: A.data, to: B.data})`로 고른 `A.anchor(from.part, from.index)`·`B.anchor(to.part, to.index)`.
    - skip 전달: link가 `to.index`를 지정했으면 B의 enter·step에 `skipNodes = [handoff.to.node]`, `skipParts = []`. 지정 안 했으면 `skipParts = [to.part]`, `skipNodes = B.part(to.part)`.
    - reduce 대체(`'fade'`)일 때도 skip·overlay 규칙은 같음.
  - reduce && move.reduce === 'fade' → 같은 duration의 내장 move로 대체: enter→`engine:fade-in`, exit→`engine:fade-out`, link→`engine:crossfade`, step→`engine:fade-in`(대상 part 없으면 no-op), ambient→no-op. camera move는 `reduce: 'self'` 필수.
  - `BuiltDeck = { tl, map, beats: BeatInstance[], byId: Map<string, BeatInstance>, destroy() }`.
- 내장 move(`engine:*`): `engine:fade-in`(beat의 모든 최상위 part opacity 0→1), `engine:fade-out`(1→0), `engine:crossfade`(A 전체 1→0, B 1←0, 앞 40% 겹침), `engine:none`(duration 0). registry가 항상 포함.
- **v2 변경 (내장 move, E2-1)**
  - `engine:none`: 등록 role은 `ambient`지만 **모든 role**에 쓸 수 있다(validateDeck·build가 role 검사를 하지 않음). duration 0, build 없음. 반복 검사 면제.
  - `engine:fade-in`: 대상 = beat의 part 요소 중 skipNodes 밖, **base 아닌 상태 층(`[data-state]:not([data-state="base"])`) 밖**. step role로 쓰이면(reduce 대체 포함) 상태 층 교대: `[data-state="<ctx.step.name>"]` 0→1, 그 밖 `[data-state]` 1→0. 대상이 없으면 no-op.
  - `engine:fade-out`·`engine:crossfade`(A 쪽): 상태 층 포함 모든 part를 `tl.to(…, { autoAlpha: 0 })`(현재 값에서 0, 숨은 층은 변화 없음). crossfade B 쪽은 fade-in과 같은 대상 규칙.

### 정지점
- 라벨 이름 = `STOP_PREFIX + name`, `STOP_PREFIX = 'stop:'`. 다른 라벨은 자유지만 `stop:`으로 시작하면 정지점으로 취급.
- 첫 beat의 enter가 `engine:none`이면 첫 정지점 t=0.

---

## C7. handoff 계약

> **v2.3 변경 (10-08 사용자 반려 「들어간 뒤 그냥 빠진다」)**
> 1. **이륙 규칙**: link move는 carry(복제본)를 띄우는 순간 `takeoff(tl, ctx)`(moves/_shared/link.js)로 원본 node와 앞 beat 루트를 숨긴다. 비행 중 보이는 것은 carry와 그 아래 드러나는 다음 beat뿐.
> 2. **마스크 규칙**: mask-size·mask-position을 바꾸는 move는 `driveValue`로 둘을 매 render 함께 쓴다(앞 move가 남긴 값에 덮이지 않고 seek에도 같은 화면). 확대 초점(focus)은 글자 획 위여야 한다(획 밖이면 종이로 들어가 화면이 빈다).
> 3. **깊이 규칙(C10)**: 화면 전체 바탕 part(chronology `ground` 등)는 엔진 CSS에서 `translate: 0 0 -8px`로 내용 뒤에 둔다. 카메라 기울기 중 3D 정렬에서 바탕이 내용을 덮는 것을 막는다.
> 4. **전환 검사**: 정지점 smoke만으로는 전환 중 결함을 못 잡는다. `node tools/transitions.mjs <deck>`로 모든 link·step 구간을 촘촘히 찍은 시트를 확인한다.

```ts
Handoff = {
  beat: string, part: string,
  index: number,           // v2: 그 part 안 요소 순번(음수 입력은 양수로 정규화)
  kind: 'rect' | 'point',
  rect: Rect,              // 측정 스냅샷(stage-local, transform 이전)
  point: Point,            // rect 중심(kind:'point'면 이것만 의미)
  node: Element,           // 그 part의 index번째 요소(v1: 첫 요소)
  style: { color: string, radius: number, fontSize: number },   // getComputedStyle 스냅샷(px 수치)
}
```
- 측정: `measure(stageRoot, beats, measureFn = defaultMeasure) → MeasureSnapshot`(`Map<Element, Rect>`). `defaultMeasure(node, root)` = getBoundingClientRect 차이. 측정은 build ②에서 한 번, 모든 transform 적용 전.
- `anchorOf(beat, part?, snapshot) → Handoff`. `BeatInstance.anchor(part)`는 이것을 부른다.
- **v2 변경 (#7·#8, E2-2)**: `anchorOf(beat, part, snapshot, primary?, index = 0)`. `index < 0`이면 `parts[part].length + index`. 범위 밖이면 throw(`Beat "<id>" has no <part>[<index>]`). `BeatInstance.anchor(part, index)`가 이것을 부른다.
- link가 넘기는 대상 = `MoveDef.handoff?.(params, { from, to })`(C5 v2 2번). 생략 = 양쪽 primary·index 0(v1과 같음).
- **소유권 규칙(link)**:
  - link 시작 시 A의 `handoff.from.node`를 움직여 `handoff.to.rect`로 보낸다(또는 overlay에 대역을 만들어 보냄).
  - link 끝 시각에: B의 대상 part(`handoff.to.part`)는 보임(`ctx.initial`로 숨겨 두었다가 끝에 `tl.set(…, {autoAlpha:1}, end)`), A의 대역·원본은 숨김.
  - 두 개가 동시에 보이는 구간은 crossfade 0.15u 이하.
  - 엔진은 B의 enter move에 `skipParts = [handoff.to.part]`를 넘긴다. **v2**: to.index를 지정한 link면 `skipParts = []`, `skipNodes = [handoff.to.node]`(C6 v2 skip 전달).
- 도우미(engine/handoff.js):
  - `rectIn(node, root) → Rect`
  - `toInset(rect, viewport) → string` (`inset(top right bottom left)` clip-path 값)
  - `transferVars(fromRect, toRect) → { x, y, scaleX, scaleY, transformOrigin: '0 0' }` (from 요소를 to 자리로 보내는 GSAP vars)

---

## C8. Stage·카메라

```ts
createStage(host: HTMLElement, { viewport: Viewport, concept: ConceptPack, mode: 'live'|'export' }) → Stage
Stage = {
  root: HTMLElement,        // .sl-stage  (fixed, 100vw×100vh; export면 1920×1080)
  viewportEl: HTMLElement,  // .sl-viewport (perspective: var(--sl-perspective))
  camera: HTMLElement,      // .sl-camera   (transform-style: preserve-3d) ← camera role만 움직임
  world: HTMLElement,       // .sl-world    (place.world beat가 들어감)
  screen: HTMLElement,      // .sl-screen   (place.slot beat가 들어감, 카메라 영향 없음)
  overlay: HTMLElement,     // .sl-overlay  (move overlay 컨테이너들의 부모, 최상단)
  viewport: Viewport,
  placeBeat(root: HTMLElement, place: Place): void,
  cameraVars(target: CameraTarget): object,   // .sl-camera에 줄 GSAP vars
  overlayFor(key: string): HTMLElement,       // move별 전용 컨테이너(없으면 생성)
  clear(): void,
}
Place = { slot: Slot } | { world: { x: number, y: number, z?: number, s?: number } }
Slot = 'center' | 'left' | 'right' | 'top' | 'bottom' | 'full' | 'lower-third'
CameraTarget = { x: number, y: number, s: number, rx?: number, ry?: number }  // world 단위, rx·ry 도(°)
```
- slot은 CSS class `sl-slot-<slot>`. 위치는 concept tokens(C11)로 조정.
- `cameraVars({x,y,s,rx,ry})` = 목표 world 점이 화면 중앙에 오도록 `.sl-camera`의 `x, y, scale, rotationX, rotationY, transformOrigin`. |rx|,|ry| ≤ 12 강제(clamp + dev 경고).

**v2 변경 (C8, #18·#25, E2-2)**
- slot 배치 = `SLOT_DEFAULTS[slot]`(engine/constants.js) 위에 `concept.slots[slot]`을 키 단위로 덮어쓴 `{ x, y, ax, ay, w? }`. `x·y` = 화면 비율 위치, `ax·ay` = 블록 안 기준점(0 = 왼쪽·위 끝, 0.5 = 가운데, 1 = 오른쪽·아래 끝), `w` = 최대 너비(화면 비율). 지금까지 stage는 `concept.slots`를 무시했다(수리).
  - 적용: 루트 inline `left: x×100%; top: y×100%; translate: -ax×100% -ay×100%; max-width: w×100%`. **CSS `translate` 속성**을 쓰고 `transform`은 쓰지 않는다(transform = move 전용, `defaultMeasure`가 inline transform을 지우므로 slot 위치가 측정에서 빠지는 문제 방지). engine.css의 slot class는 `transform`을 쓰지 않는다.
  - 기본값: `left`·`lower-third`는 `ax: 0`(블록 **왼쪽 끝**이 x에 고정 → 길이가 다른 어절이 와도 같은 자리 컷이 흔들리지 않음, #25), `right`는 `ax: 1`, `full`은 `inset: 0`(위치 키 무시).
- world 배치도 `transform` 대신 개별 속성: `left: x×w px; top: y×h px; translate: 0 0 <z>px; scale: <s>`(transform-origin 0 0). camera의 transform만 move가 움직인다.
- `ctx.camera`(camera role) = beat의 `place.world`가 화면을 꽉 채우는 목표: `{ x: wx + 0.5×s, y: wy + 0.5×s, s: 1/s, rx: 0, ry: 0 }`(wx·wy·s = place.world, s 기본 1). 즉 「타일 중심이 화면 중앙」(canvas.md 8.3 관례와 같음). move params가 덮어쓸 수 있음. screen beat의 camera move면 `ctx.camera` = 직전 camera 목표(없으면 `{x:0.5,y:0.5,s:1}`).

---

## C9. schema 형식 (move params·beat fields 공통)

```ts
FieldSchema = Record<string, Field>
Field = {
  type: 'number'|'integer'|'string'|'boolean'|'enum'|'ease'|'part'|'asset'|'array'|'object'|'any',
  default?: any, required?: boolean,
  min?: number, max?: number,       // number·integer
  values?: string[],                // enum
  of?: Field,                       // array
  fields?: FieldSchema,             // object
  doc: string,                      // 필수. 한 줄 설명
}
resolveParams(schema, given) → resolved   // 기본값 채움, 알 수 없는 키·범위 위반·필수 누락 = SchemaError
validateSchema(schema, value, path) → Array<{ path: string, message: string }>
```
- move params는 전부 `default`가 있어야 함(`required` 금지). beat fields는 `required` 사용 가능.

---

## C10. 3D 규칙

- 설명용 3D 오브젝트 금지(도는 물체·와이어프레임·회전 카드).
- `rotationX`·`rotationY`·`rotateX`·`rotateY`·`z`·`translateZ`·`transformPerspective`·`perspective` tween은 **`family: camera` move만**, 대상은 `ctx.stage.camera` 또는 `[data-depth]` 층만.
- 카메라 tilt |rx|,|ry| ≤ 12°. 깊이 패럴랙스는 `data-depth`(0=먼, 1=가까운) 층의 이동량 차이로.
- WebGL: W2 범위 밖. 덱당 최대 1곳(히어로)만 추후 계약으로 허용.
- `tools/check-moves.mjs`(W3)가 정적 검사: 위 속성 문자열이 camera family 밖에 있으면 실패, `.from(` 실패, `var(` tween 실패, `Math.random|Date.now|performance.now` 실패.

---

## C11. 컨셉 팩

`concepts/<id>/concept.json`:
```json
{
  "id": "rail",
  "name": "가로 레일 연표",
  "axis": "x",
  "camera": { "mode": "rail", "perspective": 1600 },
  "timing": { "unit": 0.55, "hold": 0.6, "overlap": 0.2 },
  "eases": { "in": "power2.in", "out": "power3.out", "inout": "power2.inOut", "scrub": "none" },
  "beats": { "allow": ["text", "chronology", "photo", "number", "quote", "video"] },
  "moves": {
    "allow": ["rail-pan", "word-rise", "match-cut"],
    "signature": ["rail-pan"]
  },
  "defaults": {
    "enter": "word-rise", "exit": "blur-out",
    "byType": { "chronology": { "enter": "rail-pan" } }
  },
  "slots": { "center": { "x": 0.5, "y": 0.5 } },
  "tokens": { "blurMax": 6, "depthNear": 1.0, "depthFar": 0.55, "stagger": 0.08 }
}
```
- `signature`: 이 컨셉을 다른 컨셉과 구별하는 move(덱에서 1회 이상 써야 함, W5 다양성 게이트).
- `tokens` = `ctx.tokens`(수치만, JS에서 읽음). 색·글꼴은 tokens.css.
- **v2.1 변경 (#46 PRESETS)**: `concept.moves.params`(선택) = `{ "<moveId>": { "<param>": value } }` 컨셉별 param 프리셋. params 해석 순서 = beat `MoveRef.params` → `concept.moves.params[moveId]` → move schema 기본값. 합친 결과를 `resolveParams`로 검사(프리셋의 모르는 키도 SchemaError). 구현 위치 = `engine/timeline.js`(plan·build 둘 다 같은 값을 써야 timing 순수성 유지).
- **v2.1 변경 (#47 COLORS)**: `ctx.colors` = `{ bg, fg, 'fg-muted', accent, 'accent-2', rule, scrim }` 계산된 색 문자열. build 직전 1회 `getComputedStyle(beat 루트)`에서 `--sl-<name>`을 읽어 beat마다 만든다(tone이 beat마다 다르므로). 값이 비면 키 생략. move는 색 tween 때 `ctx.colors`만 쓴다(`var(` 금지 유지). 구현 위치 = `engine/timeline.js` build(ctx 조립), 테스트 harness는 `colors` 주입 옵션.
- `concepts/<id>/index.js`: `import concept from './concept.json' with { type: 'json' }; export default concept;`
- `tokens.css`: `.sl-concept-<id>` 범위에 아래 CSS 변수만 정의(이름 고정, 추가는 계약 변경):

| 변수 | 뜻 |
|---|---|
| `--sl-bg` `--sl-fg` `--sl-fg-muted` `--sl-accent` `--sl-accent-2` `--sl-rule` `--sl-scrim` | 색 |
| `--sl-font-display` `--sl-font-text` `--sl-font-mono` | 글꼴 family |
| `--sl-weight-display` `--sl-weight-text` | 굵기 |
| `--sl-size-xl` `--sl-size-l` `--sl-size-m` `--sl-size-s` `--sl-size-caption` | 글자 크기(`calc(var(--px) * N * 1px)`) |
| `--sl-leading-display` `--sl-leading-text` `--sl-tracking-display` | 행간·자간 |
| `--sl-perspective` | `.sl-viewport` perspective(px) |
| `--sl-gutter` `--sl-radius` | 여백·모서리 |

| `--sl-caption-left` `--sl-caption-bottom` `--sl-caption-width` | **v2** 영상·사진 캡션 칼럼 위치(길이 값, 예 `8%`·`10%`·`36%`). engine.css의 `.sl-video__caption`·`.sl-photo__caption`이 소비(#18) |

- engine이 정의하는 변수(컨셉이 덮어쓰지 않음): `--px`, `--vw-px`, `--vh-px`, `--sl-portrait`.
- **v2 변경 (C11)**
  - `slots`: `{ <slot>: { x?, y?, ax?, ay?, w? } }`(C8 v2). 기존 `{x, y}`만 쓴 컨셉은 그대로 유효하지만 `left`·`lower-third`의 기준점이 왼쪽 끝으로 바뀐다(이미 그렇게 의도한 값들: kinetic·data·rail·canvas·launch).
  - `tone`: tokens.css는 `.sl-concept-<id> [data-tone="N"] { … }`(N = 0..5)에서 위 표의 변수만 재정의할 수 있다(새 변수 금지). 정의 안 한 tone은 기본 색.
  - beat type별 기본 레이아웃 CSS는 engine.css가 맡는다(C4 v2 class 규칙, E2-2). tokens.css는 계속 변수만.
- **v2.2 변경 (#49 layout.css)**: 컨셉 고유 배치는 `concepts/<id>/layout.css`(선택, 컨셉당 1개)에 둔다. engine.css는 모든 컨셉 공통 중립 기본값만(컨셉 범위·`[data-tone]`·`[data-now]` 배치 금지, `engine/engine-css.neutral.test.js`).
  - 범위: 모든 선택자가 `.sl-concept-<id>`로 시작(`@media`·`@supports`·`@container` 안도 같음). `@keyframes` 이름은 `<id>-`로 시작. 그 밖 at-rule(`@import`·`@layer`·`@font-face` 등) 금지.
  - 색: 값에 16진·색 함수(`rgb(` `hsl(` `oklch(` …)·색 이름 금지 → `var(--sl-*)`(tokens.css·tone이 정의)만. `transparent`·`currentColor`는 허용.
  - 변수: `--sl-*` 정의 금지(tokens.css·엔진·렌더러 몫). 컨셉 고유 변수는 `--<id>-*`.
  - `!important` 금지(move가 쓰는 inline 값을 이기면 안 됨). 렌더러가 내놓는 배치 변수(`--sl-position-x`·`--sl-span`·`--sl-now`·`--sl-lane`·`--sl-ratio` 등)는 읽기만.
  - 덱 `main.js`는 그 컨셉에 layout.css가 있으면 `tokens.css` 다음 줄에 import, 다른 컨셉 layout.css는 import 금지. `tools/cli.mjs new`가 자동으로 넣는다.
  - 강제: `tools/check-concepts.mjs`(`node tools/check.mjs`의 concepts 항목). 같은 type을 두 컨셉이 다르게 배치하려면 각자 layout.css로, 공통으로 필요한 구조(예: 숫자 릴 1em 창)만 engine.css.

---

## C12. 스크롤 드라이버·발표 키·이벤트

```ts
createScrollDriver({ track: HTMLElement, tl, map: TimelineMap, viewport: Viewport, reduce: boolean }) → ScrollDriver
ScrollDriver = {
  attach(): void, detach(): void,
  timeToY(t: number): number, yToTime(y: number): number,
  time(): number,                                  // 현재 timeline 시각
  seek(t: number, opts?: { immediate?: boolean, duration?: number }): void,
  stops(): Array<{ name, label, t, y, beat }>,
  lenis, st,                                       // 내부 객체(테스트·디버그용)
}
```
- `attach`: track 높이 = C2 식. ScrollTrigger `{ trigger: track, start: 'top top', end: 'bottom bottom', scrub: true, animation: tl }`. Lenis `reduce ? { smoothWheel: false, lerp: 1 } : { lerp: 0.1, wheelMultiplier: 0.9, smoothWheel: true }`. `lenis.on('scroll', ScrollTrigger.update)`, `gsap.ticker.add(t => lenis.raf(t * 1000))`, `gsap.ticker.lagSmoothing(0)`.
- `timeToY(t) = st.start + (t / map.duration) * (st.end - st.start)`.

```ts
createPresenter(driver: ScrollDriver, { reduce, target = window }) → Presenter
Presenter = { next(), prev(), first(), last(), goto(name: string), blackout(on?: boolean), destroy() }
```
- 키(`PRESENTER_KEYS`):
  - 다음: `ArrowRight` `ArrowDown` `PageDown` `Space`(Shift 없이)
  - 이전: `ArrowLeft` `ArrowUp` `PageUp` `Shift+Space`
  - 처음·끝: `Home` `End`
  - 블랙아웃 토글: `b` `.`
  - 전체화면 토글: `f`
- 메타·Ctrl·Alt 조합은 무시. 링크·버튼·input에 포커스가 있으면 Space·Enter 양보.
- 다음 정지점 = 현재(진행 중 목표 우선) 시각보다 `0.01u` 이상 뒤의 첫 stop. 이동 시간(초) = `min(2.6, 0.9 + |Δy| / h × 0.35)`, easing = cubic inOut. reduce면 즉시 이동.
- URL 파라미터: `?t=<u>`(시작 시각), `?stop=<name>`, `?motion=reduce`(강제 reduce), `?debug=1`(HUD: t·stop·beat). **v2.2 구현**: live 모드에서 boot가 ready 직전에 `?stop`(name 또는 label, `?t`보다 우선) → `?t`(0..duration으로 자름) 순으로 `driver.seek(t, { immediate: true })`. `?debug=1` HUD = `div.sl-debug`(host 안, fixed, 매 프레임 `t 0.00 · stop <name> · beat <id>`), destroy 때 제거.

- **v2 명시 (E2-7)**: `scrolline:active` 발생 주체 = **boot**(지금은 아무도 안 냄 — 수리). master tl `onUpdate`와 boot가 부르는 seek 뒤에 현재 t로 beat별 `[span.start, span.end)` 안팎을 이전 값과 비교해 enter/leave를 낸다(같은 t 재계산은 이벤트 없음). `persist` beat도 span 끝에 leave(화면에는 남되 inert). video clip activate/deactivate도 같은 지점에서(C13 v2). export 모드에서는 내지 않음. 정지점·키 규칙 변화 없음.

### window 이벤트 (`EVENTS`, 전부 `CustomEvent`, detail 고정)
| 이름 | detail | 발생 |
|---|---|---|
| `scrolline:ready` | `{ map, mode }` | 첫 build 완료 |
| `scrolline:rebuild` | `{ reason: 'resize'\|'fonts'\|'hot', time }` | 재빌드 완료 |
| `scrolline:stop` | `{ name, index, beat }` | 발표 키 도착 또는 스크롤 150ms 정지 시 현재 t가 stop ±0.02u |
| `scrolline:active` | `{ beat, phase: 'enter'\|'leave' }` | beat span 진입·이탈(a11y inert 토글용) |
| `scrolline:blackout` | `{ on }` | 블랙아웃 토글 |
| `scrolline:export-ready` | `{ duration }` | export 모드 wrapper 등록 직후 |

### window.__deck (디버그·캡처 API)
```ts
{ version: 2, mode, map, tl, time(): number, seek(t): void, goto(name): void, stops(): Stop[] }
```

### resize 재계산 규칙
- debounce 200ms. 폭이 같고 높이 변화 < 15%면 무시(모바일 주소창).
- 그 외: 현재 t 기억 → `stage.clear()` → viewport 재계산 → `build` 재실행(map은 그대로 재사용) → `driver.seek(t, { immediate: true })` → `scrolline:rebuild`.
- 폰트 로드 완료 후 1회 재측정 build(`reason: 'fonts'`).

---

## C13. media 계약

```ts
frameSequence(host: HTMLElement, manifest: FramesManifest | string /*url*/, opts?: { fit?: 'cover'|'contain', tier?: number }) → FrameSeq
FrameSeq = { canvas: HTMLCanvasElement, count: number, setProgress(p: number): void, setFrame(i: number): void, ready(): Promise<void>, preloadAll(): Promise<void>, destroy(): void }
```
- `FramesManifest`(`frames.json`): `{ version: 1, fps, count, width, height, pattern: 'f_%04d.webp', tiers: { "1920": "1920/", "960": "960/" }, poster: 'poster.webp' }`. 프레임 경로 = manifest 폴더 + tiers[tier] + pattern(1-base).
- tier 선택: `viewport.w × dpr ≥ 1400` → 가장 큰 tier, 아니면 960.
- 로딩 순서: poster → 8장 간격(coarse) → 현재 위치 ±12장 → 나머지. 그리기 = 목표 프레임이 없으면 **가장 가까운 앞쪽 로드된 프레임**(되감기 안정).
- **v2.2 (ctx.textMask)**: 글자 폭 ≤ rect.w × 0.92 이고 잉크 높이 ≤ rect.h × 0.8(둘 중 작은 쪽). 브라우저에서는 canvas에 문서 글꼴(웹폰트 포함)로 그려 `data:image/png` URL, canvas가 없으면 위 SVG `textMask`. 흰 글자 + 투명 배경이라 mask alpha 의미는 같다.
- `setProgress`는 timeline tween이 쓰는 setter에서만 부름(`driveValue`·`scrubTo`, 스크럽 결정론). **v2.2**: manifest 로드 전 `setProgress`·`setFrame`은 기억했다가 도착 뒤 그 프레임을 그린다.

```ts
videoClip(host, { src, poster, loop, mode: 'play'|'loop' }, { exportMode: boolean }) → Clip
Clip = { el: HTMLVideoElement, activate(): void, deactivate(): void, bindExport({ start, duration }): void, destroy(): void }
```
- live: `<video muted playsinline preload="metadata">`, `scrolline:active` enter에서 `activate()`(play), leave에서 `deactivate()`(pause, currentTime 유지).
- export: `bindExport`가 `data-start`(초, 루트 기준), `data-duration` 설정. JS로 play·seek 하지 않음(HyperFrames 소유). `crossorigin` 속성 금지.

```ts
textMask(text: string, { font: string /* CSS font 축약 */, width: number, height: number, align?: 'center'|'left' }) → string   // data:image/svg+xml URL, mask-image 값으로 사용
preloadImages(urls: string[]) → Promise<void>      // img.decode() 전부 대기
```
- 영상 마스크: 대상 `.sl-mask` 요소에 `mask-image: url(...)` 또는 `clip-path`. 마스크 move는 `--sl-mask-*`가 아니라 GSAP으로 `clipPath`·`maskPosition`·`maskSize`를 tween.
- **v2 변경 (C13, #16·#17)**
  - 글자 마스크 적용 주체 = **move**. 렌더러는 `data-mask-text`만 남긴다. move는 `ctx.textMask(text, opts)`(C5)로 URL을 받아 `ctx.initial`로 `maskImage`·`webkitMaskImage`를 건다. `ctx.textMask` = `textMask(text, { font: '<--sl-weight-display> <크기>px <--sl-font-display>', width: rect.w, height: rect.h, align })`, 크기 = 글자 폭이 rect.w의 0.92가 되도록(엔진 계산, getComputedStyle 허용 — build는 순수 아님).
  - `textMask` SVG = 배경 투명 + 흰 글자(mask는 alpha로 읽음. v1의 검정 배경 rect는 전체를 보이게 만드는 버그였음 — v2 커밋에서 수리). `videoClip`은 host 이벤트 리스너를 달지 않는다(v2 커밋에서 제거).
  - video beat 핸들: `BeatInstance.media.seq`(scrub)·`.clip`(play·loop). live에서 clip `activate`/`deactivate`는 boot가 `scrolline:active` enter/leave에 맞춰 부른다(move는 부르지 않음). export에서는 boot가 `clip.bindExport({ start: toExportSeconds(path, span.start), duration: toExportSeconds(path, span.end) − start })`, seq는 `preloadAll()` 대기(C14 그대로).

`tools/media/extract-frames.mjs`:
```
node tools/media/extract-frames.mjs <input.mp4> <outDir> [--fps 24] [--tiers 1920,960] [--quality 78] [--from 0] [--to <sec>]
→ <outDir>/frames.json, <outDir>/poster.webp, <outDir>/<tier>/f_0001.webp …
```
- ffmpeg 필수(`ffmpeg -version` 실패 시 exit 2). 산출 count·크기를 frames.json에 기록.

---

## C14. export 계약 (덱 → MP4, HyperFrames)

```ts
EXPORT_DEFAULTS = { width: 1920, height: 1080, fps: 30, secondsPerUnit: 0.5, stopHold: 1.6, travelMin: 0.6, travelMax: 5, lead: 0.4, tail: 1.2, ease: 'power1.inOut' }
exportPath(map: TimelineMap, opts?, holds?: Record<stopName, seconds>) → ExportPath   // 순수
ExportPath = {
  duration: number,         // 초
  segments: Array<{ kind: 'lead'|'travel'|'hold'|'tail', from: number /*u*/, to: number /*u*/, start: number /*s*/, end: number /*s*/ }>,
  stopAt: Record<string, number>,   // stop 이름 → 영상 초(정지 구간 중앙)
}
buildExportTimeline(master, path, gsap) → wrapper   // paused gsap timeline, 길이 = path.duration
toExportSeconds(path, t /*u*/) → number             // 영상 안 in-scene video data-start 계산용
```
- 경로: lead(t=0 정지) → 각 stop 사이 travel(초 = clamp(Δu × secondsPerUnit, travelMin, travelMax), ease) → stop마다 hold(`beat.exportHold ?? stopHold`) → 마지막 stop 뒤 map 끝까지 travel → tail.
- wrapper = `gsap.timeline({ paused: true })`에 `master.tweenFromTo(from, to, { duration, ease })`를 segment 시작 초에 `add`. hold는 위치 인자로 비워 둠(빈 tween 금지).
- export 모드 boot: viewport 고정 1920×1080, reduce=false, scroll driver·presenter 없음, frameSequence `preloadAll()`·폰트·이미지 decode 대기 후 `window.__timelines['scrolline'] = wrapper`(등록은 build 완료 **뒤**), 이어서 `scrolline:export-ready`.
- 루트 HTML: `<div id="scrolline-root" data-composition-id="scrolline" data-width="1920" data-height="1080" data-duration="<path.duration>">`. `data-duration`은 `tools/export.mjs`가 node에서 `plan`+`exportPath`로 계산해 정적으로 박는다.
- `tools/export.mjs <deckId> [--fps 30] [--out out/export/<deckId>.mp4]`: ① node에서 plan·exportPath ② `vite build` export 진입(`SCROLLINE_MODE=export SCROLLINE_DECK=<id>`) → `out/export/<id>/` ③ `npx hyperframes lint` ④ `npx hyperframes render`. Playwright 금지.
- `tools/capture.mjs <deckId> [--stops] [--at s1,s2]`: export 빌드에 대해 `npx hyperframes snapshot`으로 정지점 중앙(`stopAt`)·정지점 사이 중간 프레임 PNG → `out/capture/<id>/`. 실패 시 exit ≠ 0, `manifest.json`(파일·t·stop) 기록.

---

## C15. boot

```ts
boot({
  host: HTMLElement, deck: object /* deck.yaml 파싱 결과 */, concept: ConceptPack, moves: Registry,
  sequences?: Record<string, BeatTypeDef & SequenceDef>, assetBase: string, mode?: 'live'|'export',
}) → Promise<DeckHandle>
DeckHandle = { map, built: BuiltDeck, driver?: ScrollDriver, presenter?: Presenter, rebuild(reason): Promise<void>, destroy(): void }
```
- 순서: `validateDeck` 실패 시 화면에 오류 목록을 그리고 throw → `plan` → viewport → `createStage` → `build` → (live) driver·presenter·a11y·resize / (export) `buildExportTimeline` 등록.
- **v2 변경 (C15, E2-7)**: boot가 build에 넘기는 것 = `asset`(`assetBase` + 덱 상대 경로, 이중 슬래시 없음), `media: { frameSequence, videoClip }`, `el`·`words`·`chars`(util/dom), `sources`(deck.sources를 id로), `mode`, `plugins`(SplitText·Flip·MorphSVGPlugin·DrawSVGPlugin·CustomEase 등록 후). 지금 boot는 이것들을 넘기지 않아 video scrub이 `<video>`로 떨어지고 asset 경로가 덱 기준으로 안 풀린다(수리 대상). clip·seq 연결은 C13 v2. export에서 모든 seq `preloadAll()`·이미지 `preloadImages` 뒤 wrapper 등록.
- 덱 진입 파일 형태(`decks/<id>/main.js`):
```js
import { boot } from '../../engine/index.js';
import '../../engine/engine.css';
import moves from '../../moves/index.js';
import concept from '../../concepts/<concept>/index.js';
import '../../concepts/<concept>/tokens.css';
import '../../concepts/<concept>/layout.css';   // v2.2: 그 컨셉에 있을 때만(C11)
import deck from './deck.yaml';
// sequence 덱: import ground from './sequences/ground.js'; … → boot({ …, sequences: { ground } })
boot({
  host: document.getElementById('app'),
  deck,
  concept,
  moves,
  assetBase: new URL('./', document.baseURI).href,
  mode: import.meta.env.SCROLLINE_MODE,   // v2.2 필수: tools/export.mjs가 SCROLLINE_MODE=export로 빌드(없으면 MP4 export 불가)
});
```
- **v2.2**: `node tools/check.mjs`(concepts 항목)가 `mode` 줄 누락을 막는다. `npm run deck -- plan <id>`는 `_` 내부 덱도 받고, `main.js`의 `./sequences/*.js` import를 그대로 읽어 `validateDeck` 뒤 plan을 낸다(오류면 목록 출력·exit 1).

---

## C16. registry

```ts
createRegistry(defs: MoveDef[]) → Registry
Registry = { get(id): MoveDef /* 없으면 throw */, has(id): boolean, ids(): string[], byFamily(f): MoveDef[], byRole(r): MoveDef[] }
```
- 생성 시 검사: id 유일·형식, family·role 유효, `params` 모든 키 `default`·`doc` 보유, `timing`·`build` 함수, `sources` 1개 이상. 위반 = throw.
- **v2 변경 (E2-6)**: `handoff`가 있으면 함수여야 하고 `role: 'link'`여야 함. id는 `seq:`로 시작할 수 없음(sequence span 예약).
- `engine:*` 내장 move 자동 포함.
- `moves/index.js`(메인 소유): `import { createRegistry } from '../engine/index.js'; import reveal from './reveal/index.js'; … export default createRegistry([...reveal, ...]);`

---

## C17. 테스트·CI 명령

| 명령 | 내용 | 통과 기준 |
|---|---|---|
| `npm test` | `vitest run` (환경 happy-dom, pool `vmThreads` — 워커당 환경 1회·파일마다 VM 격리, 대상 `{engine,moves,concepts,decks,tools}/**/*.test.{js,mjs}`). 실제 레포 전체 검사는 단위 테스트에 두지 않고 `npm run check` 몫. 하위 node 프로세스·임시 트리는 /mnt/d 밖(os.tmpdir) | 전부 녹색 |
| `npm run check` | `node tools/check.mjs` = check-deps + check-tests(모듈마다 테스트) + check-state(board·runs 스키마) + check-moves(C5·C10) + check-concepts(C11 layout.css, v2.2) | exit 0 |
| `npm run ci` | `npm test && npm run check` | main 병합 조건 |
| `npm install` | `.npmrc`의 `legacy-peer-deps=true` 전제(npm 10.9 arborist가 vitest 5·vite 8 peer 묶음에서 죽음) | 워커는 설치 금지, 메인만 |
| `node tools/check.mjs --hat <base>..<head>` | 두 모자 검사 | feature: 테스트 파일 추가·수정 1개 이상 / refactor: 기존 `*.test.js` 수정 0(이름 변경만 허용) |

- 커밋 trailer: 병합 커밋마다 `Hat: feature|refactor|none` 한 줄(check-hat 대상). **v2.2**: `none` = 문서·계획·자산 커밋, 코드(`*.js`·`*.mjs`·`*.css`) 변경 0이어야 함.
- **check-tests 규칙**: `engine/**/*.js`·`moves/**/*.js`(테스트·`index.js`·`types.js`·`constants.js`·`testing.js`·`moves/_shared/` 제외)마다 옆에 `.test.js` 필수. 단 파일 첫 30줄 안에 `@stub` 표기가 있으면 면제(스캐폴드 상태). 워커는 구현 시 `@stub`을 지우고 테스트를 넣는다.
- **engine 모듈 테스트 최소 항목**
  - timeline: map 불변식 ①~⑤, 고정 fixture 덱의 stop t 값 정확 일치, fallback move 대체 시 map 동일
  - stage: viewport 식(1920×1080, 390×844, 1280×1024), slot class, cameraVars clamp
  - handoff: `transferVars` 수치, `toInset` 문자열, 측정 스냅샷이 transform 무시
  - scroll: `timeToY`/`yToTime` 왕복, track 높이 식(Lenis·ScrollTrigger는 vi.mock 허용)
  - presenter: 키 → next/prev 선택 규칙, 포커스 양보, reduce 즉시 이동
  - media: tier 선택, 로딩 순서, 가장 가까운 앞 프레임 규칙(이미지는 가짜 객체)
  - export: path 합계 = duration, segment 연속, stopAt 위치, wrapper seek 결정론
  - **v2 추가**: timeline — persist 끝 숨김 생략·overlay 수명·sequence span·skipNodes 전달·engine:fade-in 상태 층 교대 / handoff — anchor index(양수·음수·범위 밖) / stage — slot 기준점(ax·ay)·concept.slots 덮어쓰기·transform 미사용 / beats — C4 v2 새 part 전부 존재·상태 층 hidden·음수 막대 방향 / boot — rc 전달·clip activate/deactivate·export bindExport
- **move 테스트 최소 항목**(`engine/testing.js`의 harness 사용)
  1. `createRegistry([move])` 통과(형식)
  2. timing 순수: 같은 입력 2회 → deepEqual, 기본 params로 duration > 0(ambient 제외)
  3. build 길이: local tl duration ≤ timing.duration + 0.001
  4. seek 결정론: `seek(a)` 스냅샷 → `seek(b)` → `seek(a)` 스냅샷 동일
  5. 되감기: `seek(end)` → `seek(0)` 후 대상 inline style = `initial` 상태
  6. reduce: `reduce: true`에서 `filter`에 blur 없음, 3D 속성 없음(camera 제외)
  7. link만: 끝 시각에 to part 보임·from 숨김, 운반 노드 최종 rect ≈ `handoff.to.rect`(±1px, harness 가짜 측정)
  8. **v2**: skipNodes에 든 요소의 inline style이 build 전후 같음(enter·step), `handoff()`가 있으면 순수(같은 입력 2회 deepEqual)
  - **v2.2**: `moves/_shared/contract-check.js` `checkMove`가 1·2·8번을 실제로 돈다. timing·handoff는 schema 기본값을 채운 params로 부른다. 8번 기본 대상 = 그 beat primary 첫 요소(시나리오 `skip(h)`로 바꿈), 정지 0 시점의 x·y·scale·rotation·opacity·visibility가 build 전과 같아야 함. 대상 거르기는 `moves/_shared/skip.js` `partFree(ctx, part)`.

### engine/testing.js (harness)
```ts
createHarness({ beats: Array<{ id, type, data, place? }>, viewport?: Partial<Viewport>, reduce?: boolean, rects?: Record<string /* `${beatId}.${part}` */, Rect>, concept?: Partial<ConceptPack> }) → Harness
Harness = {
  stage: Stage, beats: Map<string, BeatInstance>,
  runMove(move: MoveDef, { role, beat, from?, params? }) → { tl, ctx, timing },   // local tl를 master 0에 add
  seek(t: number): void,
  snapshot(nodes: Element[], props?: string[]): object,   // gsap.getProperty 값 + inline style
  destroy(): void,
}
```
- harness는 happy-dom 위에서 돌고, 측정은 `rects` 값으로 대체(happy-dom은 layout 없음). 기본 rect는 `{x:0,y:0,w:100,h:100}`.
- **v2 변경 (E2-1)**: `rects` 키에 `${beatId}.${part}#${index}`(index번째 요소) 허용, `#` 없으면 index 0. `runMove`는 C5 v2 ctx(`skipNodes`·`step`·`textMask`·`prev`·`next`·`camera`)를 채우고 `{ …, step?, skipNodes? }` 옵션을 받는다. `beats` 항목에 `media?`(가짜 seq·clip) 허용.

---

## C18. 상태 기록 (state/)

- `state/board.json` — 현재 상태 스냅샷. 스키마 `state/schema/board.schema.json`. 메인만 수정.
- `state/runs.jsonl` — append-only 이벤트 로그, 한 줄 = 한 레코드. 스키마 `state/schema/runs.schema.json`. 메인만 append.
- **run 줄**(`kind` 생략 또는 `"run"`): 잡 시작 때 1줄(`status: running`), 끝날 때 같은 `run_id`로 1줄 더(`success|error|cancelled`). **같은 run_id의 마지막 줄이 현재 상태.**
  - 필수: `run_id`(hex32), `parent_run_id`(null = 루트), `root_run_id`, `run_type`(`wave|research|design|build|judge|render|repair`), `name`, `status`(`queued|running|success|error|cancelled`), `started_at`
  - 선택: `trace`, `model`(`codex gpt-5.6-terra medium` · `claude-opus` 등), `hat`(`feature|refactor|none`), `target`(`{kind: deck|move|engine|concept|site|research, id}`), `inputs`(`{brief, brief_sha256, files: {path: sha256}}`), `outputs`(`{files: {path: sha256}, commit}`), `error`, `ended_at`, `tokens`(`{input, output, total}` 또는 null), `tags`
  - 웨이브 = `run_type: wave` 루트 run(trace). 잡 run의 `parent_run_id` = 웨이브 run_id.
- **feedback 줄**(`kind: "feedback"`): 판정 1건. 필수 `feedback_id`, `run_id`(대상 run), `key`(`wow|tech|content|diversity|a11y`), `score`(0~1), `by_run_id`(판정 run), `time`. 선택 `value`(PASS|FAIL 등), `comment`.
- 시각 형식 `YYYY-MM-DDTHH:MM:SS`(시간대 생략 = KST).
- `npm run check`가 두 파일 스키마 검사(파일 없으면 통과).

---

## C19. engine/index.js 공개 이름 (전부, 이 밖은 없음)

- 함수: `createStage` `computeViewport` `el` `words` `chars` `createRng` `hashSeed` `resolveParams` `validateSchema` `prefersReducedMotion` `createA11y` `plan` `build` `resolveTiming` `createRegistry` `validateDeck` `createScrollDriver` `createPresenter` `measure` `defaultMeasure` `anchorOf` `rectIn` `toInset` `transferVars` `frameSequence` `videoClip` `textMask` `preloadImages` `pickTier` `loadOrder` `exportPath` `buildExportTimeline` `toExportSeconds` `boot`
- 상수·클래스: `VERSION` `STOP_PREFIX` `ID_PATTERN` `ROLES` `BEAT_TYPES` `SLOTS` `FAMILIES` `ENGINE_MOVES` `REDUCE_FALLBACK` `ENGINE_TIMING_DEFAULTS` `VIEWPORT` `MAX_TILT` `CAMERA_ONLY_PROPS` `EVENTS` `PRESENTER_KEYS` `PRESENTER_TRAVEL` `RESIZE` `CSS_VARS` `PLACEHOLDER_PATTERNS` `EXPORT_DEFAULTS` `FRAMES` `ENGINE_MOVE_DEFS` `SchemaError` `beatTypes`
- `engine/contract.test.js`가 이 목록과 정확히 일치하는지 검사(메인 소유).
- **v2 변경**: 공개 이름은 바꾸지 않는다. v2 상수(`CONTRACT_VERSION` `DECK_ID_PATTERN` `NO_MOVE` `SLOT_DEFAULTS` `TONE_RANGE` `BASE_STATE` `SOURCED_TYPES`)는 engine 내부 전용(`engine/constants.js`에서 직접 import, `index.js`는 내보내지 않음). moves·concepts·decks가 필요하면 문자열 값을 그대로 쓴다(`'engine:none'`, `'base'`).

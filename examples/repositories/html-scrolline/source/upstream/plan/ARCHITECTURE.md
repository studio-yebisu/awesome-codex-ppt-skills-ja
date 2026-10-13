# Scrolline v2 — 아키텍처 (10-08)

- 정본 순서: PLAN.md(목표) → 이 문서(설계 이유) → CONTRACTS.md(인터페이스 정본, 워커 인용용) → WORK-SPLIT.md(W2 잡)
- 수치·시그니처는 CONTRACTS.md에만 정본으로 둔다. 여기는 구조와 결정 이유

## 1. 핵심 결정 요약

- **D1 timing은 layout과 무관한 순수 계산**: `plan(deck)`이 DOM 없이 node에서 TimelineMap(정지점·beat span)을 만든다. move의 `timing(params, data)`도 순수. 덕분에 ① resize·세로 화면·reduced-motion에서 같은 t = 같은 내용 ② export가 node에서 영상 길이를 미리 박음 ③ 정지점·길이를 브라우저 없이 테스트
- **D2 beat = DOM, move = 움직임**: beat 렌더러는 완성 상태 DOM과 `data-part`만 만든다. 움직임은 전부 move. 옛 판의 「장면 템플릿 = 레이아웃+안무 한 덩어리」를 쪼개서, 같은 beat에 컨셉마다 다른 move 문법을 입힌다
- **D3 스크롤 영상 = 이미지 시퀀스 canvas**, 장면 안 재생 영상 = `<video>`, 덱 → MP4 = HyperFrames 렌더(스크롤 대신 「발표 경로」 wrapper timeline). 이유는 §6
- **D4 장면 경계 없음 계승**: 무대 1개·master timeline 1개·`stop:*` 라벨 정지점·handoff(앞 요소가 다음 요소가 됨). SG J조 scroll-v2의 `mount/build/handoffRect` 계약을 일반화
- **D5 3D는 카메라만**: `.sl-camera` 1개와 `data-depth` 층만 3D 속성을 가진다. move 정적 검사로 강제

## 2. 모듈 구조

```
engine/      무대·시간·스크롤·발표·이음·미디어·접근성·내보내기 (내용 모름)
  index.js       공개 API(다른 층은 이것만 import)
  types.js       JSDoc typedef 정본          constants.js  이벤트·CSS 변수·키·정규식
  stage.js       무대·카메라·slot·world      timeline.js   plan(순수)·build·내장 move
  registry.js    move registry 검증          deck-schema.js deck 검증·내용 감사
  scroll.js      Lenis+ScrollTrigger 드라이버 presenter.js  발표 키·블랙아웃
  handoff.js     측정 스냅샷·anchor·좌표 변환 media.js      프레임 시퀀스·video·text mask
  a11y.js        reduced-motion·aria-live·inert export.js   발표 경로·wrapper timeline
  boot.js        통합 진입                    testing.js    move·beat 테스트 harness
  beats/         beat 렌더러 10종(text·photo·video·number·chart·chronology·compare·quote·prompt·code)
  util/          dom(el·words·chars)·rng(seeded)·schema(params 검사)
  engine.css     무대 기본 CSS
moves/       family별 폴더, move 1개 = 파일 1개 + 테스트 1개, family index.js, 루트 index.js = registry
  _shared/       family 공용 도우미(예: 글자 쪼개기 규칙)
concepts/    컨셉 팩: concept.json(축·timing·ease·허용 move·signature·tokens) + tokens.css(색·글꼴) + index.js
decks/       덱: deck.yaml + index.html + main.js + assets/ + sequences/(덱 전용 beat)
  _smoke/        엔진 통합 확인용 최소 덱
tools/       cli·check(deps·tests·state·hat·moves)·capture·export·media/extract-frames·vite/deck-plugin
site/        갤러리(W6)
state/       board.json·runs.jsonl(LangSmith식 상태 정본)·schema/
```

- 의존 방향: `decks → concepts → moves → engine`(+ `site`가 맨 위). 순환 금지. `tools/check-deps.mjs`가 R1~R5로 차단(CONTRACTS C1)
- moves·concepts·decks는 `gsap`을 직접 import하지 않고 `ctx.gsap`·`ctx.plugins`로 받는다 → 플러그인 등록·버전이 engine 한 곳
- 덱 전용 연출은 `beat type: sequence` + `decks/<id>/sequences/<name>.js`로만. 엔진·move 수정 없이 덱 고유 장면을 넣는 탈출구(J조 Parts·Tour 같은 것)

## 3. 연속 타임라인 모델

- **무대 1개**: `.sl-stage`(fixed) 안에 `.sl-viewport`(perspective) → `.sl-camera`(preserve-3d) → `.sl-world`, 그리고 카메라 영향 없는 `.sl-screen`, 최상단 `.sl-overlay`
- **timeline 1개**: master `gsap.timeline({paused:true})`. beat의 move마다 local timeline을 만들어 span 시작에 `add`. 장면 핀·장면별 ScrollTrigger 없음
- **단위**: 1u = 화면 높이 × `unit`(기본 0.55)만큼 스크롤. track 높이 = h + duration × h × unit. 컨셉별 `unit` 조정(키네틱은 짧게, 캔버스는 길게)
- **beat 시간 배치**(정본 C6): 앞 beat의 exit 시작 + `overlap`에 다음 beat가 들어온다 → 빈 화면 없이 겹침이 기본. link가 있으면 exit 대신 link가 두 beat를 하나의 동작으로 잇는다
  - 한 beat 안: `link(들어옴) → enter → [stop] → hold → steps(각각 stop·hold) → exit 또는 link(나감)`, 그 위에 `camera`(시작에 병렬), `ambient`(수명 내내)
- **정지점**: `stop:<beatId>`(enter 끝)와 `stop:<beatId>/<sub>`(move 내부 정지점·step 끝). 발표 키는 이 라벨만 따라간다. 휠과 키가 같은 Lenis 좌표를 공유
- **발표 키**: → ↓ Space PageDown 다음 / ← ↑ Shift+Space PageUp 이전 / Home End / `b`·`.` 블랙아웃 / `f` 전체화면. 이동 시간 = min(2.6, 0.9 + 거리/h × 0.35)초
- **reduced-motion**: Lenis 부드러움 끔, 발표 키 즉시 이동, `reduce:'fade'` move는 **같은 길이**의 내장 fade로 대체(정지점 불변), `reduce:'self'` move(카메라 필수)는 blur·깊이 차이·3D tilt를 스스로 끔. `?motion=reduce`로 강제
- **세로 화면**: `w/h ≤ 1`. `--px = w/760`(가로는 min(w, h·16/9)/1920). 배치(slot 좌표·world 배율)만 바뀌고 시간표는 그대로
- **리사이즈**: 200ms debounce, 폭 같고 높이 변화 < 15%면 무시. 그 외엔 현재 t 기억 → 무대 비움 → 재측정 build(map 재사용) → 같은 t로 즉시 이동. 폰트 로드 뒤 1회 재측정

## 4. beat 종류

| type | 쓰임 | 핵심 데이터 |
|---|---|---|
| text | 한 문장 무대 | text, emphasis, size |
| photo | 사진 | src, alt, focus, caption, source |
| video | 영상(스크럽·재생·루프) | src, poster, mode, frames, mask |
| number | 큰 숫자 | value, format, label, source |
| chart | 차트(막대·선·면·점) | kind, categories, series, states |
| chronology | 연표·레일 | events[date,title,note,media], scale, axis |
| compare | 비교(2~4) | items[label,value,text,media], verdict |
| quote | 인용 | text, by, role, source |
| prompt | 프롬프트 타이핑 → 결과 | text, label, result |
| code | 코드 | code, lang, highlight |
| sequence | 덱 전용 장면 | use, data |

- 필드·part 정본은 CONTRACTS C4. 모든 beat는 정지점 상태의 완성 DOM으로 렌더 → reduce·접근성·export 스냅샷이 같은 DOM을 본다

## 5. move 계약 요지

- `{ id, family, role, accepts, sources, reduce, params, timing(params,data), build(tl, ctx, params) }`
- role 6종: `enter`(나타남) · `exit`(사라짐) · `link`(A→B 이음, handoff 사용) · `step`(머문 뒤 변신) · `camera`(카메라 이동) · `ambient`(머무는 동안 은근한 움직임)
- handoff: build 전에 모든 part rect를 transform 없이 한 번 측정(스냅샷). link는 `ctx.handoff.from`(A의 part: rect·node·style)을 `ctx.handoff.to`(B의 part rect) 자리로 보내고, 끝에 B part 보임·A 숨김. B의 enter는 `skipParts`로 그 part를 건드리지 않음 → 「한 물체가 변해서 다음이 된다」를 계약으로 보장
- 결정론: local tl, `ctx.initial`로 시작 상태 선언, `from()` 금지, `fromTo(immediateRender:false)`, seeded rng, 시계 함수 금지
- 원천: `sources`에 awesome-ai-motion slug(637 정의·61 클립). W1 인벤토리(R7) → W3 family별 구현
- 초기 family(W3에서 확정): `reveal`(마스크·클립 리빌) · `type`(키네틱 타이포) · `morph`(매치컷·모프·fly-to) · `camera`(줌인·플라이스루·무한 줌·깊이 패럴랙스) · `rail`(가로 레일 팬) · `data`(차트→차트·count-up) · `media`(영상 스크럽·ken-burns·영상 마스크) · `assemble`(흩어졌다 모이기·접기·쌓기) · `emphasis`

## 6. 영상 연결 설계

### 6.1 스크롤 영상 스크럽 → 이미지 시퀀스 canvas 채택
| 후보 | 판정 | 이유 |
|---|---|---|
| 이미지 시퀀스 + canvas | **채택** | 프레임 = 파일이라 seek가 즉시·정확, 되감기 대칭, 모든 브라우저 동일, HyperFrames 렌더에서도 그대로 결정론. J조 Tour·옛 frame-scrub에서 검증됨 |
| `video.currentTime` | 보조 금지 | keyframe 간격에 묶여 seek 지연·역방향 끊김, 브라우저별 편차. all-intra 인코딩(`-g 1`)이면 나아지나 파일 크기 폭증 |
| WebCodecs | 보류 | demux(mp4box 등) 추가 의존·디코더 큐 관리 복잡, 프레임 정확 seek를 직접 구현해야 함. 이득은 대역폭뿐 → 성능 문제 실측 시 재검토 |
- 비용 관리: `extract-frames`가 fps·tier(1920/960)·webp 품질을 조절, 로딩은 poster → 8장 간격 → 현재 ±12장 → 나머지, 없는 프레임은 가장 가까운 앞 프레임
- 진행률은 timeline tween의 `onUpdate`에서만 `setProgress` → 스크롤·발표 키·export가 같은 경로

### 6.2 장면 안 재생 영상
- live: `<video muted playsinline>`를 beat 활성(`scrolline:active`) 동안만 재생, 이탈 시 일시정지. 스크롤과 무관하게 흐르는 「살아 있는 화면」용(루프 배경·짧은 시연)
- export: 같은 요소에 `data-start`·`data-duration`(발표 경로 기준 초)을 박아 HyperFrames가 재생·디코드를 소유

### 6.3 영상 마스크
- 글자 모양 마스크: `textMask()`가 SVG data URL을 만들고 `.sl-mask`의 `mask-image`로. 마스크 move가 `maskSize`·`maskPosition`을 tween(글자 안에 영상 → 글자가 열리며 전체 화면)
- 도형 마스크: `clip-path`(inset·circle·polygon) tween. J조 hero의 inset 접기 계승

### 6.4 덱 → MP4 (HyperFrames)
- 판단: **맞출 수 있다.** HyperFrames 계약 = 「단일 paused GSAP timeline, 시간만으로 같은 픽셀」. 우리 master tl이 이미 paused·결정론이고, 스크롤만 입력. 스크롤을 「발표 경로」로 바꾸면 됨
- 발표 경로 `exportPath(map)`: lead → stop 사이 travel(Δu × 0.5초, 0.6~5초 clamp, power1.inOut) → stop마다 hold 1.6초(beat별 `exportHold`) → tail. 순수 함수라 node가 길이를 계산해 루트 `data-duration`에 정적으로 박음(HyperFrames는 루트 길이를 스크립트 실행 전에 읽음)
- wrapper timeline = `master.tweenFromTo(a, b)`를 segment 시작 초에 add. `window.__timelines['scrolline']`에 build 완료 **후** 등록
- 렌더: `tools/export.mjs`가 vite export 빌드 → `npx hyperframes lint` → `npx hyperframes render`. 정지점 캡처도 `hyperframes snapshot`(Playwright 금지 규칙 준수, 판정용 캡처 경로가 이것 하나로 통일)
- 오디오·이어 붙이기는 ffmpeg 후처리

## 7. 3D 규칙

- 3D = 카메라 언어만: 원근 tilt(≤12°), 깊이 패럴랙스(`data-depth` 층별 이동량 차), 플라이스루(world 좌표 사이 카메라 비행), 무한 줌(배율 연쇄)
- 금지: 설명용 3D 오브젝트(도는 물체·와이어프레임·회전 카드), camera family 밖의 rotationX/Y·z·perspective
- WebGL: W2 범위 밖. 덱당 히어로 1곳만, 추후 `engine/media-gl.js` 계약 추가 시
- 강제: `tools/check-moves.mjs`(W3) 정적 검사 + move 테스트 6번(reduce에서 3D 없음)

## 8. 파울러 5원칙 적용

| 원칙 | 이 레포에서 |
|---|---|
| 진화적 설계·작은 단계 | W2 끝 = `_smoke` 덱이 휠·키로 돌아감. W4는 rail 1편 끝까지 → 나머지. 잡 1개 = 모듈 1개 |
| 자가 테스트 코드 | `npm test`(vitest + happy-dom). engine 모듈·move마다 옆에 `.test.js` 필수(`check-tests`). 테스트 항목 최소 목록은 CONTRACTS C17. 시킹 결정론·handoff 좌표·정지점 t 정확 일치 |
| 지속 통합 | `npm run ci` = `npm test && npm run check`. 워커 산출은 메인이 ci 녹색 확인 후에만 병합. GitHub Actions `.github/workflows/ci.yml` 동일 명령 |
| 두 모자 | 잡 지시서 머리에 `Hat: feature` 또는 `Hat: refactor`. 커밋 trailer `Hat:` 동일. `node tools/check.mjs --hat <range>`: feature = 테스트 추가·수정 1개 이상, refactor = 기존 테스트 수정 0 |
| 모듈 경계·응집 | 단방향 층 + 공개 진입점 + 형제 격리 + 외부 패키지 위치 제한 + 순환 0(`check-deps`) |

- 스텁 표기: 스캐폴드 파일 머리 `@stub` → `check-tests` 면제. 구현 잡은 `@stub` 삭제 + 테스트 추가가 완료 조건

## 9. 상태 관리 (LangSmith식)

- 대응: project = 덱 1편, trace = 웨이브 1개(root run), run = 잡 1개, feedback = 판정 점수, dataset = `research/ledger`
- `state/board.json`(현재 상태 스냅샷, 메인만 수정):
```json
{
  "version": 1, "updated": "ISO",
  "waves": { "W2": { "root_run_id": "…", "status": "running" } },
  "engine": { "E2": { "files": ["engine/timeline.js"], "status": "running", "runs": ["…"] } },
  "concepts": { "rail": { "stage": "storyboard", "status": "review", "runs": [] } },
  "moves": { "match-cut": { "family": "morph", "stage": "impl", "status": "pass", "sources": ["morph-match-cut"], "used_by": ["rail-history"], "runs": [] } },
  "decks": { "rail-history": { "concept": "rail", "stage": "assemble", "status": "running", "moves": [], "score": { "wow": 0.7 }, "runs": [] } }
}
```
  - stage 값: engine `spec|impl|tested|merged` · concept `direction|storyboard|tokens|done` · move `inventory|spec|impl|tested|merged` · deck `brief|storyboard|assemble|judge|repair|done`
  - status 값: `todo|running|review|pass|fail|blocked`
- `state/runs.jsonl`(append-only 이벤트 로그, 메인이 이미 쓰는 형식 계승): run 줄 = 시작 1줄(`running`) + 끝 1줄(같은 run_id, 마지막 줄이 현재 상태). 필드 run_id·parent_run_id·root_run_id·run_type(`wave` = trace 루트)·name·model·status·started_at·ended_at + 선택 hat·target·inputs/outputs 파일 해시·commit·tokens / `kind: feedback` 줄 = 판정 1건(run_id·key·score 0~1·value·comment·by_run_id)
- board의 `runs` 배열이 run_id로 runs.jsonl과 이어짐. 산문 문서에는 상태를 적지 않음
- 스키마: `state/schema/board.schema.json`, `state/schema/runs.schema.json`. `npm run check`가 검사

## 10. 게이트 위치

| 게이트 | 도구 | 단계 |
|---|---|---|
| 테스트·결정론·정지점 | `npm test` | 모든 잡 |
| 의존·테스트 존재·상태 스키마·두 모자 | `npm run check` | 모든 잡 |
| deck 스키마·내용 감사(자리표·출처 없는 수치) | `validateDeck`(boot·cli) | W4 |
| move 정적 검사(3D·from·var·시계) | `tools/check-moves.mjs` | W3 |
| 다양성(덱 간 move 지문·signature 사용·덱 안 반복) | `tools/check-diversity.mjs` | W5 |
| 시각(겹침·빈 화면·글리프 잘림·대비) + 와우 판정 | `tools/capture.mjs`(hyperframes snapshot) → opus 판정 | W5 |
| 휠·발표 키 실제 입력 | Aside 브라우저 수동 판정 | W5 |

## 11. 남은 위험

- HyperFrames가 우리 단일 루트(클립·sub-composition 없이 master만) 구조를 lint 통과시키는지 미실측 → W2-E7 첫 작업이 spike
- happy-dom은 layout이 없어 handoff 실좌표는 harness 가짜 측정으로만 테스트됨 → 실좌표는 W5 캡처 판정에서 확인
- 이미지 시퀀스 용량(1920 tier 수백 장) → 덱별 프레임 예산(W4 지시서에 상한)
- 휠·키 e2e 자동화 없음(Playwright 금지) → Aside 수동 판정으로 대체

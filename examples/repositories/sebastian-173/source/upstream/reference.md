# deck-factory reference — 다크 에디토리얼 덱 상세

SKILL.md의 8규칙·절차를 실제로 구현하는 토큰·컴포넌트·렌더 디테일. 시작점은
`assets/styles.css`(그대로 복사해 쓰는 재사용 CSS). 실물 예시는 `work/premium/slides/slide-01.html`(커버)·`slide-05.html`(스탯).

---

## 1. 색 토큰 (`:root`)

| 역할 | 토큰 | 값 |
|---|---|---|
| 캔버스 | `--bg-0` | `#08090A` (near-black, **순흑 금지**) |
| surface 래더 | `--bg-1/2/3` | `#0F1012` · `#16181B` · `#1F2226` |
| ink / body / mute / faint | `--ink/--body/--mute/--faint` | `#F5F6F7` · `#A6ABB2` · `#6A6F77` · `#3C4046` |
| hairline | `--line` / `--line-strong` | `rgba(255,255,255,.07)` / `.15` |
| accent | `--accent` / `--accent-2` | `#6E7BF2` / `#8B95FF` |
| accent tint / glow / cyan | `--accent-soft`/`--glow`/`--cyan` | `rgba(110,123,242,.12)` / `#4C63E6` / `#43C7F4` |
| delta | `--pos` / `--neg` | `#3FB984` / `#E5695B` |
| theme effects | `--grain-opacity`/`--grain-blend`/`--glow-opacity` | `.035` / `overlay` / `.55` |
| component internals | `--mark-shadow`/`--code-highlight`/`--mock-*` | 프로파일별 shadow·inset·mock surface |

- 다크에서 **유일한 테두리 = 알파화이트 hairline**. 카드 배경은 채우기가 아니라 surface 래더에서 한 단 올린 것.
- accent는 슬라이드당 1곳. delta 색은 슬라이드당 ≤2종.
- DECK-STANDARD 원안은 시그널 레드 `#E5484D`를 accent로 썼다. 구현 덱은 인디고 `#6E7BF2` 계열로 갔다 — **덱마다 accent 하나를 골라 고정**하면 된다(레드든 인디고든 한 색).

## 2. 타이포

- 스택: sans/display `"Pretendard", -apple-system, "Segoe UI"`, mono `"Geist Mono","JetBrains Mono","D2Coding"`. 한글은 Pretendard.
- 스케일(px): 11·12·13·15·16·18·20·23·29·40·56·80·116·172. 한 슬라이드에서 크기 종류 ≤3.
- display 음수 트래킹 `-.03em`, 스탯 숫자 `-.045em`. mono 라벨은 양수 트래킹 `.1em` + uppercase.
- 숫자엔 `font-feature-settings: "tnum" 1`(tabular) — 자릿수 흔들림 방지.
- CJK 필수 세트(body에): `word-break: keep-all; overflow-wrap: normal; line-break: strict;`

## 3. 마스터 크롬 (4모서리) — 전 슬라이드 공통

`.slide` 안에 `.frame` 형제로 절대배치. `--mx:140px`(좌우) / `--my:96px`(상하) safe margin.

- `.deck-brand`(좌상): accent 그라디언트 `.mark` 아이콘 + `.wm` 워드마크.
- `.deck-meta`(우상): mono 15px mute, 파트/날짜.
- `.deck-author`(좌하): mono 15px mute.
- `.deck-page`(우하): `<b>05</b> / 12` — 현재 페이지만 ink.

콘텐츠는 세로 중앙이 아니라 **광학적 위 1/3~중앙** 앵커. `.frame > .spacer:first-of-type { flex:.62 }`로 위쪽을 눌러 앉힌다.

## 4. 에디토리얼 골격 (콘텐츠 슬라이드 카피 스키마)

```
.eyebrow      11~17px 대문자 mono, accent, 앞에 짧은 rule. .eyebrow.ko는 한글용(트래킹↓, 소문자)
.action-title 56~116px, weight 600, -.03em, 마침표로 끝나는 단정문. .dim=회색강조, em=accent강조
.subhead      (선택) 29px body, max 46ch
[지배 오브젝트 1개]  stat / flow / bento / timeline / code / mock …
.tail         (선택) margin-top:auto + hairline 위 반전·단서 1줄. .tail b = ink 강조
```

- **박스 안에 박스 금지**. 멀티존은 카드가 아니라 세로 1px hairline(`.col + .col { border-left }`)으로 나눈다.
- 액션타이틀은 명사 나열 금지 — "품질 게이트" (X) → "미달은, 통과하지 못한다." (O).

## 5. 컴포넌트 카탈로그 (언제 쓰나 → 클래스)

| 지배 오브젝트 | 언제 | 핵심 클래스 |
|---|---|---|
| **빅넘버 스탯** | KPI·수치 3개로 요점 | `.stat-row > .stat`: `.k`(라벨 16px mute uppercase) / `.v`(172px + `<small>`단위 / `.mult`배수 accent) / `.c`(캡션 21px) / `.delta.up|.down` |
| **파이프라인 flow** | 단계·프로세스 | `.flow > .node`: `.n`(번호) `.t`(제목) `.d`(설명), 활성 노드 `.node.on`(accent-soft 그라디언트). 노드 사이 border-left |
| **bento** | 팔레트·기능 타일 그리드 | `.bento`(4열 grid) `> .tile`: `.swatch` `.name` `.desc` `.glow-s`. 유일하게 radius 박스 허용 존 |
| **타임라인** | 시간축 로드맵 | `.timeline > .tstep`: 상단 그라디언트 rail + `.dot`(glow) `.tm` `.lb` `.sb` |
| **코드블록** | CLI·명령 시연 | `.code`: mono, `.cmd`/`.flag`(accent)/`.str`(cyan)/`.cmt`(mute)/`.caret`(accent) 토큰 컬러 |
| **번호 스텝** | 순서 있는 절차 | `.steps > .step`: `.no`(각진 번호칩) + `.tx h3/p` |
| **before/after** | 개선 대비 | `.mockrow`(2열) > `.mock.before`(neg cap) / `.mock.after`(pos cap), `.mock-num` 거대숫자 |
| **반원 게이지** | 단일 점수·비율 | `.gauge`: `.center > .g-v`(130px) `.g-l`(라벨). SVG arc는 별도 |

`.gap-s/-m/-l`(22/40/64px)·`.spacer`(flex)로 수직 리듬을 준다.

## 6. 이미지 · 깊이

- **커버/챕터**: `.bg > img.bg-img`(object-fit:cover) + `.scrim`(텍스트측 `linear-gradient(90deg,#08090A 20%,rgba(8,9,10,.55) 50%,transparent 82%)`) + `.bg-grain`(SVG 노이즈, opacity .035). 텍스트를 이미지 위에.
- **데이터 슬라이드**: 히어로를 우측 세로 슬롯에 격리(예: `right:-30px; top:50%; height:124%`) + `.glow`(cyan, opacity .12) 저조도 글로우. `.hairgrid`(radial mask 그리드)로 은은한 격자.
- 빈 박스 대신 **AI 다이어그램** 생성: "Deck DNA" 톤 프롬프트(`#0B1220/#5E6AD2/#38BDF8/#E6E9F0`, 21:9)로 codex-imagegen. 
- **생성 이미지 위에 코드로 글자 합성 절대 금지** — 오타·잘림·폰트 불일치의 원인. 글자가 필요하면 프롬프트를 고쳐 재생성하거나, HTML 텍스트 레이어로 이미지 위에 얹는다.

## 7. 13-슬롯 레이아웃 어휘

cover · chapter · statement · bullets · two-col · cards-3 · data-split · image-full · image-split · flow · chart-bar · kpi-3 · closing. 각 슬롯은 고정 필드 + max_chars/max_lines를 가진다고 보고, **이 enum 밖 레이아웃을 발명하지 않는다**(형태는 계약, 내용만 채운다). 오버플로 0이 목표 — Pretendard 실폰트 기준 박스폭 90%를 넘으면 카피를 줄인다.

## 8. 라이트/문서 프로파일 전환

기본은 다크. 문서형·보고서형·출력형 브리프는 같은 골격과 컴포넌트에 light token만 얹는다.

사용법:

```html
<body data-theme="light">
  <section class="slide">…</section>
</body>
```

혼합 테스트나 특정 슬라이드만 전환할 때:

```html
<section class="slide" data-theme="light">…</section>
```

선택 우선순위:

1. 명시 `theme: light` / `profile: light` → light 강제.
2. 명시 `theme: dark` / `profile: dark` → dark 강제.
3. 자동 감지 — 문서·보고서·제안서·출력·프린트·핸드아웃·화이트페이퍼·이사회·공공·학술, 또는 report/proposal/document/print/handout/whitepaper/board memo/academic/government 신호면 light.
4. 그 외는 dark.

Light token:

| 역할 | 토큰 | 값 |
|---|---|---|
| 캔버스 | `--bg-0` | `#F7F4EC` paper |
| surface 래더 | `--bg-1/2/3` | `#EFE9DC` · `#E6DECF` · `#DCD2C0` |
| ink / body / mute / faint | `--ink/--body/--mute/--faint` | `#1A1A1A` · `#4C4A45` · `#747066` · `#C7BDAA` |
| hairline | `--line` / `--line-strong` | `rgba(26,26,26,.10)` / `.18` |
| accent | `--accent` / `--accent-2` | `#5662CC` / `#4852B8` |
| accent tint / glow / cyan | `--accent-soft`/`--glow`/`--cyan` | `rgba(86,98,204,.10)` / `#8790D8` / `#147D9D` |
| delta | `--pos` / `--neg` | `#237A54` / `#B94A3C` |
| theme effects | `--grain-opacity`/`--grain-blend`/`--glow-opacity` | `.018` / `multiply` / `.18` |

Light QA:

- surface는 밝은 한지/문서처럼 보여야지 흰 웹앱 대시보드처럼 보이면 안 된다.
- hairline은 알파블랙이고, 채운 회색 카드로 구조를 만들지 않는다.
- display 음수 트래킹은 유지하되 과하게 조이지 않는다.
- glow와 grain은 dark보다 낮게. blob 장식은 금지.
- 본문 대비는 `--body` on `--bg-0` 기준 4.5:1 이상이어야 한다.

## 9. WSL / 헤드리스 크로미움 렌더

- 각 slide-NN.html을 1920×1080 뷰포트로 캡처: `chromium --headless --window-size=1920,1080 --screenshot=out.png --default-background-color=00000000 file://…/slide-01.html`. Playwright(`page.set_viewport_size({width:1920,height:1080})` → `page.screenshot`)가 더 안정적.
- **폰트가 안 뜨면**(WSL에 Pretendard/Geist 미설치) 렌더가 폴백 폰트로 나가 트래킹·줄바꿈이 다 틀어진다. 해결: (a) 시스템에 폰트 설치 후 `fonts.css`에서 `local()` 참조, 또는 (b) `fonts.css`에 woff2를 **base64 data URI로 임베드**(`@font-face { src: url(data:font/woff2;base64,…) }`) — 파일 경로/CORS/캐시 문제를 원천 제거. 프리미엄 덱은 임베드 방식을 권장.
- PNG 후 PDF: 슬라이드 PNG들을 순서대로 합치거나, print CSS(`@page{size:1920px 1080px;margin:0}` + `-webkit-print-color-adjust:exact`)로 크로미움 `--print-to-pdf`.
- **공유용 PDF는 기본 경량화**: Chrome PDF 원본은 폰트 subset·색상 프로필 때문에 커질 수 있다. PDF를 만든 뒤 스킬 helper를 실행해 `*-lite.pdf`를 기본 전달물로 삼는다.

```bash
skills/deck-factory/scripts/compact-pdf.sh out/deck.pdf
```

  - 기본 preset은 `ebook`이며 보통 발표 공유용에 충분하다.
  - 더 작게 필요하면 세 번째 인자로 `screen`, 인쇄 품질을 더 남기려면 `printer`.
  - Ghostscript가 없으면 원본 PDF를 유지하되, 최종 보고에 경량화 미실행을 명시한다.
- 렌더 후 반드시 합격 체크리스트(SKILL.md)로 눈검수 — near-black 여부, 거대숫자 높이, 한글 깨짐, accent 개수.

## 10. 지향 파이프라인 (로드맵 — 자동 아님)

이 스킬이 지금 보장하는 건 "Claude가 이 시스템으로 슬라이드를 짓는다"까지다. 그 위에 얹으려는
방법론: **storyline**(출처 수집·claims) → **copy**(액션타이틀 카피) → **plan/compose**(결정론 조립)
→ **grader**(hard-fail 7종 + 6카테고리 가중합 90점) → **export**(실렌더). "브리프 한 줄로 전부 자동"은
아직 아니다 — 각 단계는 사람이 계약 파일을 보고 고칠 수 있어야 한다. 원본 계약 SSOT는
`deck-factory/design/DECK-STANDARD.md`.

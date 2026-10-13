---
name: scrolline-deck
description: 발표 브리프를 스크롤로 진행하는 발표 덱(Scrolline v2)으로 만든다. 무대 1개·연속 timeline 1개·handoff move·컨셉 6종(rail·data·launch·zoom·canvas·kinetic)별 움직임 문법. deck.yaml 작성 → node plan 확인 → 브라우저 smoke → HyperFrames MP4 내보내기까지. 트리거 — "스크롤 덱 만들어", "스크롤 발표", "스크롤텔링 덱", "스크롤로 넘어가는 발표자료", "연표 덱", "데이터 스토리 덱", "제품 발표 스크롤", "줌 드릴다운 발표", "덱을 MP4로", "scrolline", "scrolline deck", "scroll deck", "scrollytelling deck", "scroll-driven presentation", "export deck to mp4". 후속 — "이 beat만 move 바꿔", "정지점 추가", "홀드 길게", "컨셉 바꿔서", "smoke 다시", "MP4 다시 뽑아" 도 이 스킬. ※ 이산 슬라이드·발표자 노트 중심이면 slideshow, 덱과 무관한 영상 제작이면 hyperframes 소관.
---

# scrolline-deck — 스크롤 발표 덱 (v2)

- 산출물: `decks/<id>/` 덱 1개(브라우저 발표용) + `out/export/<id>.mp4`(선택)
- 작업 위치: 이 SKILL.md가 있는 레포 루트. 다른 폴더에서 호출되면 레포 루트로 이동 후 진행(`cd ~/.claude/skills/scrolline-deck` 등). 모든 명령은 레포 루트 기준
- 정본: `plan/CONTRACTS.md`(인터페이스), 사용 문서 `docs/*.md`. 이 파일과 문서가 다르면 CONTRACTS가 우선

## 원칙

1. **내용은 beat, 움직임은 move**: `deck.yaml`에는 내용과 move 이름·params만. 덱을 위해 engine·moves 코드를 고치지 않는다. 덱 고유 장면이 꼭 필요하면 `decks/<id>/sequences/<use>.js`(`type: sequence`)
2. **컨셉 문법 준수**: 컨셉 `moves.allow` 밖 move는 쓰지 않는다(불가피하면 `override: "<사유>"`). 컨셉 `moves.signature` move는 덱에서 1회 이상 사용
3. **컷 대신 handoff**: 이어지는 두 beat가 같은 대상(숫자·막대·사건·글자)을 다루면 `link` move로 잇는다. link가 B를 다 그리면 B의 `enter`는 `engine:none`
4. **수치 날조 금지**: 실데이터 덱(`sample: false`)은 number·chart·quote·photo·값 있는 compare마다 `source` 필수, `sources[]`에 url·확인일. 가상 회사면 `sample: true`(화면에 「표본」 표기)
5. **한 정지점 = 한 주장**: 정지점마다 초점 1개, 글자 위계 3단(결론·보충·출처) 이내. 메타 캡션(「25초」「녹화」 등) 금지
6. **3D는 카메라만**: 설명용 3D 오브젝트 금지. 깊이·기울기는 camera family move와 `data-depth` 층으로만

## 절차

### 1. 브리프 정리
- 확인 항목: 주제, 청중, 발표 길이, 결론 1문장, 보유 자료(수치·출처·영상·사진), 실데이터/표본 여부, 언어(ko|en)
- 정지점 수 기준: 발표 1분당 정지점 1~2개
- 출처 없는 수치는 사용자에게 출처를 받거나 표본으로 전환. 임의 수치 생성 금지

### 2. 컨셉 선택

| 이야기 구조 | 컨셉 | signature move |
|---|---|---|
| 시간 순서로 사건이 이어짐(연혁·로드맵) | `rail` | `rail-advance` `era-shift` `counter-handoff` |
| 수치·차트가 변하며 주장을 쌓음(실적·시장 분석) | `data` | `dot-multiply` `mark-morph` `annotation-pin` |
| 제품 하나를 공개(신제품·신기능) | `launch` | `lit-from-dark` `sticky-scrub-link` `number-slam` |
| 전체에서 원인 하나로 파고듦(진단·TAM-SAM-SOM) | `zoom` | `zoom-dive` `zoom-surface` `depth-ladder` |
| 여러 영역을 지도 위에서 순회(피치덱·전략 지도) | `canvas` | `arc-flight` `establish-crane` `atlas-pullback` |
| 문장이 무대(강의·키노트·선언) | `kinetic` | `word-door` `slot-pick` `phrase-fold` |

- 허용 beat type·move·기본값: `concepts/<id>/concept.json`. 참고 덱: 컨셉마다 `decks/` 예제 1편
- 사용자에게 컨셉과 beat 목록(id·type·한 줄 내용·정지점)을 표로 보여 주고 합의 후 작성

### 3. 덱 생성·작성

```bash
npm run deck -- new <deckId> --concept <concept>
npm run deck -- moves --family <family> --role <role>   # 쓸 수 있는 move 목록
```

- `decks/<deckId>/main.js`의 `boot({...})`에 `mode: import.meta.env.SCROLLINE_MODE`가 있는지 확인(없으면 추가. MP4 내보내기 필수 조건)
- `deck.yaml` 필드: `docs/writing-a-deck.md`. beat type별 필수 필드·part: CONTRACTS C4
- move params: 해당 `moves/<family>/<id>.js`의 `params`(doc·min·max). 범위 밖 값은 검증 실패
- 같은 move를 같은 role로 2회 이상 쓰면 `repeat: intended`(의도된 리듬일 때만)
- 영상: 스크럽 = `npm run frames -- <in.mp4> decks/<id>/assets/frames/<name>` 후 `mode: scrub` + `frames`. 재생 = `mode: play|loop`. 스톡은 라이선스와 출처를 `decks/<id>/assets/CREDITS.md`에 기록(`docs/media.md`)

### 4. 정지점 확인(node)

```bash
npm run deck -- plan <deckId>
```

- 확인: 정지점 순서·간격, 빈 구간 없음, step 정지점(`<beat>/<step>`) 위치
- 정지점 간격이 너무 짧으면 `hold`·move `duration`, 너무 길면 `timing.unit`·`overlap` 조정

### 5. 브라우저 smoke

```bash
npm run dev -- --port 5190                              # 별도 터미널
node tools/smoke.mjs <deckId> --driver chrome --shots
```

- 결과: `out/smoke/<deckId>/report.json`, `stop-XX.png`, `sheet.png`
- 통과 기준: errors 0, empty 0, overlaps 0, clipped 0, tiny 0
- `sheet.png`를 직접 열어 정지점마다 원칙 5(초점 1개·위계·메타 캡션) 판정

### 6. MP4 내보내기(요청 시)

```bash
npm run export -- <deckId> --dry-run    # 길이·발표 경로 확인
npm run export -- <deckId>              # out/export/<deckId>.mp4
npm run capture -- <deckId> --stops     # 정지점 PNG, out/capture/<deckId>/
```

- 정지점별 머무는 시간: beat `exportHold`(초), 기본 1.6초
- 배경 음악·이어 붙이기는 ffmpeg 후처리(도구 범위 밖)

## 게이트(전부 통과해야 완료 보고)

| 게이트 | 확인 방법 | 기준 |
|---|---|---|
| 스키마·내용 감사 | 브라우저 로드(boot의 validateDeck) 또는 `npm test`(덱 `deck.test.js`가 있을 때) | 오류 0. 자리표(`TODO`·`TBD`·`lorem`·`???`·`{{`·`자리표` 등)·빈 문자열·출처 누락·허용 밖 move 차단 |
| 정지점 | `npm run deck -- plan <deckId>` | 계획한 정지점이 순서대로 존재 |
| 브라우저 | `node tools/smoke.mjs <deckId> --driver chrome --shots` | errors·empty·overlaps·clipped·tiny 전부 0 |
| 컨셉 문법 | `deck.yaml` 대조 | signature move 1회 이상, 같은 move 반복은 `repeat: intended`만 |
| 저장소 | `npm run ci` | 녹색(엔진·move·덱 테스트 + 의존·테스트 존재·state·move 정적 규칙) |
| 화면 판정 | smoke `sheet.png` 육안 | 정지점마다 초점 1개, 위계 3단 이내, 메타 캡션·장식 3D 없음 |
| 내보내기(요청 시) | `npm run export -- <deckId>` | exit 0, `out/export/<deckId>.mp4` 생성 |

## 금지

- 덱 하나를 위해 `engine/`·`moves/`·`concepts/` 수정(필요하면 별도 작업으로 분리, `docs/moves.md`·`docs/concepts.md` 절차)
- `tl.from`·`Math.random`·`Date.now`·tween 값 안 `var(`(move 작성 시)
- 출처 없는 실수치, 표본 덱의 실존 회사·인물 이름
- Playwright로 캡처(캡처는 `capture`·`smoke` 경로만)

## 참고 문서

- `docs/getting-started.md`: 설치부터 MP4까지
- `docs/writing-a-deck.md`: `deck.yaml` 필드·beat type·내용 감사
- `docs/concepts.md`: 컨셉 팩 6종·새 컨셉 추가
- `docs/moves.md`: move 계약·작성·테스트
- `docs/media.md`: 프레임 시퀀스·영상·마스크
- `docs/export.md`: 내보내기·캡처·smoke
- `docs/architecture.md`: 층 구조·timeline 모델·개발 원칙·state 기록

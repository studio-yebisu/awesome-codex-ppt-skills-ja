/**
 * JSDoc typedef 정본(메인 동결). plan/CONTRACTS.md v2(2026-10-08)와 1:1. 런타임 코드 없음.
 * 사용: `/** @type {import('../engine/types.js').MoveDef} *\/`
 */

// ── C2 단위·좌표 ──
/** @typedef {{ w: number, h: number, portrait: boolean, px: number, dpr: number }} Viewport */
/** @typedef {{ x: number, y: number, w: number, h: number }} Rect  stage-local px, transform 이전 */
/** @typedef {{ x: number, y: number }} Point */

// ── C3 deck ──
/** @typedef {{ move: string, params?: Record<string, any>, at?: number, override?: string }} MoveRef */
/** @typedef {MoveRef & { name?: string, hold?: number }} StepRef */
/** @typedef {{ slot: Slot } | { world: { x: number, y: number, z?: number, s?: number } }} Place */
/** @typedef {'center'|'left'|'right'|'top'|'bottom'|'full'|'lower-third'} Slot */
/** @typedef {string | string[]} SourceRef  v2: deck.sources[].id 하나 또는 1개 이상 배열 */
/**
 * @typedef {{
 *   id: string, type: string, place?: Place,
 *   enter?: MoveRef, exit?: MoveRef, link?: MoveRef, camera?: MoveRef, ambient?: MoveRef[], steps?: StepRef[],
 *   stop?: boolean, hold?: number, at?: number, exportHold?: number, repeat?: string,
 *   persist?: boolean, tone?: number, source?: SourceRef,
 *   [field: string]: any
 * }} BeatSpec  v2: persist(place.world 전용, 끝 숨김 생략)·tone(0..5 → 루트 data-tone)
 */
/**
 * @typedef {{
 *   id: string, title: string, lang: 'ko'|'en', concept: string, sample?: boolean,
 *   sources?: Array<{ id: string, title: string, url: string, accessed: string, short?: string }>,
 *   timing?: Partial<Timing>, export?: Partial<ExportOptions>, beats: BeatSpec[]
 * }} DeckSpec
 */
/** @typedef {{ unit: number, hold: number, overlap: number, tail: number }} Timing */

// ── C9 schema ──
/**
 * @typedef {{
 *   type: 'number'|'integer'|'string'|'boolean'|'enum'|'ease'|'part'|'asset'|'array'|'object'|'any',
 *   default?: any, required?: boolean, min?: number, max?: number, values?: string[],
 *   of?: Field, fields?: Record<string, Field>, doc: string
 * }} Field
 */
/** @typedef {Record<string, Field>} FieldSchema */
/** @typedef {{ path: string, message: string }} SchemaIssue */

// ── C4 beat ──
/** @typedef {{ seq?: FrameSeq, clip?: Clip }} BeatMedia  v2: video beat가 move·boot에 넘기는 핸들 */
/** @typedef {{ root: HTMLElement, parts: Record<string, Element[]>, media?: BeatMedia }} BeatView */
/**
 * @typedef {{ frameSequence: Function, videoClip: Function }} MediaApi
 */
/**
 * @typedef {{
 *   viewport: Viewport, lang: 'ko'|'en', asset: (p: string) => string, media: MediaApi,
 *   el: Function, words: Function, chars: Function,
 *   sources: Record<string, { id: string, title: string, url: string, accessed: string, short?: string }>,
 *   mode: 'live'|'export'
 * }} RenderContext  v2: sources(출처 표기)·mode 추가
 */
/**
 * @typedef {{
 *   type: string, fields: FieldSchema, primary: string,
 *   render: (data: object, rc: RenderContext) => BeatView
 * }} BeatTypeDef
 */
/**
 * @typedef {BeatTypeDef & {
 *   timing: (data: object) => MoveTiming,
 *   build: (tl: object, ctx: MoveContext) => void
 * }} SequenceDef  덱 전용 sequence(C4)
 */
/**
 * @typedef {{
 *   id: string, type: string, data: object, place: Place,
 *   root: HTMLElement, parts: Record<string, Element[]>,
 *   part: (name: string) => Element[],
 *   anchor: (part?: string, index?: number) => Handoff,
 *   span: { start: number, stop: number, end: number },
 *   media: BeatMedia
 * }} BeatInstance  v2: anchor index(음수 = 뒤에서), media 핸들
 */

// ── C5 move ──
/** @typedef {'enter'|'exit'|'link'|'step'|'camera'|'ambient'} Role */
/** @typedef {{ duration: number | 'fill', stops?: Array<{ name: string, at: number }> }} MoveTiming */
/** @typedef {{ part?: string, index?: number }} HandoffEnd */
/** @typedef {{ from?: HandoffEnd, to?: HandoffEnd }} HandoffSpec  v2: link move가 고르는 넘김 part·index(생략 = primary·0) */
/**
 * @typedef {{
 *   id: string, family: string, role: Role, accepts: string[], sources: string[],
 *   reduce: 'self'|'fade', params: FieldSchema,
 *   timing: (params: Record<string, any>, data: object) => MoveTiming,
 *   build: (tl: object, ctx: MoveContext, params: Record<string, any>) => void,
 *   handoff?: (params: Record<string, any>, data: { from: object, to: object }) => HandoffSpec
 * }} MoveDef  v2: handoff(link 전용, 순수, 선택)
 */
/**
 * @typedef {{
 *   gsap: object, plugins: Record<string, any>, role: Role,
 *   beat: BeatInstance, from?: BeatInstance, prev?: BeatInstance, next?: BeatInstance,
 *   handoff?: { from: Handoff, to: Handoff }, camera?: CameraTarget,
 *   stage: Stage, viewport: Viewport, reduce: boolean,
 *   start: number, duration: number, skipParts: string[], skipNodes: Element[], overlay: HTMLElement,
 *   step?: { name: string, index: number },
 *   tokens: Record<string, number>,
 *   ease: (alias: string) => string,
 *   initial: (targets: Element|Element[], vars: object) => void,
 *   rng: () => number,
 *   textMask: (text: string, opts?: { rect?: Rect, align?: 'center'|'left' }) => string,
 *   overlaysOf: (beat: BeatInstance) => HTMLElement[]
 * }} MoveContext  v2: skipNodes·step·textMask 추가, prev·next·camera 채움. v2.2: overlaysOf
 */
/**
 * @typedef {{
 *   get: (id: string) => MoveDef, has: (id: string) => boolean, ids: () => string[],
 *   byFamily: (f: string) => MoveDef[], byRole: (r: Role) => MoveDef[]
 * }} Registry
 */

// ── C6 timeline ──
/** @typedef {{ name: string, label: string, t: number, beat: string }} StopEntry */
/** @typedef {{ role: Role, move: string, start: number, end: number, params: Record<string, any> }} Span */
/**
 * @typedef {{
 *   version: 1, deck: string, concept: string, duration: number, unit: number,
 *   stops: StopEntry[],
 *   beats: Array<{ id: string, type: string, start: number, stop: number, end: number, spans: Span[] }>
 * }} TimelineMap
 */
/**
 * @typedef {{ tl: object, map: TimelineMap, beats: BeatInstance[], byId: Map<string, BeatInstance>, destroy: () => void }} BuiltDeck
 */

// ── C7 handoff ──
/**
 * @typedef {{
 *   beat: string, part: string, index: number, kind: 'rect'|'point', rect: Rect, point: Point, node: Element,
 *   style: { color: string, radius: number, fontSize: number }
 * }} Handoff  v2: index(양수로 정규화된 요소 순번)
 */
/** @typedef {Map<Element, Rect>} MeasureSnapshot */

// ── C8 stage ──
/** @typedef {{ x: number, y: number, s: number, rx?: number, ry?: number }} CameraTarget */
/**
 * @typedef {{
 *   root: HTMLElement, viewportEl: HTMLElement, camera: HTMLElement, world: HTMLElement,
 *   screen: HTMLElement, overlay: HTMLElement, viewport: Viewport,
 *   placeBeat: (root: HTMLElement, place: Place) => void,
 *   cameraVars: (target: CameraTarget) => object,
 *   overlayFor: (key: string) => HTMLElement,
 *   clear: () => void
 * }} Stage
 */

// ── C11 concept ──
/** @typedef {{ x?: number, y?: number, ax?: number, ay?: number, w?: number }} SlotSpec  v2: SLOT_DEFAULTS 위에 키 단위 덮어쓰기, w = 최대 너비(화면 비율) */
/**
 * @typedef {{
 *   id: string, name: string, axis: 'x'|'y'|'z'|'free',
 *   camera: { mode: string, perspective: number },
 *   timing: Partial<Timing>, eases: Record<string, string>,
 *   beats: { allow: string[] },
 *   moves: { allow: string[], signature: string[] },
 *   defaults: { enter?: string, exit?: string, link?: string, byType?: Record<string, { enter?: string, exit?: string, link?: string }> },
 *   slots?: Record<string, SlotSpec>,
 *   tokens: Record<string, number>
 * }} ConceptPack
 */

// ── C12 scroll·presenter ──
/**
 * @typedef {{
 *   attach: () => void, detach: () => void,
 *   timeToY: (t: number) => number, yToTime: (y: number) => number,
 *   time: () => number,
 *   seek: (t: number, opts?: { immediate?: boolean, duration?: number }) => void,
 *   stops: () => Array<StopEntry & { y: number }>,
 *   lenis: object, st: object
 * }} ScrollDriver
 */
/**
 * @typedef {{ next: () => void, prev: () => void, first: () => void, last: () => void,
 *   goto: (name: string) => void, blackout: (on?: boolean) => void, destroy: () => void }} Presenter
 */

// ── C13 media ──
/**
 * @typedef {{ version: 1, fps: number, count: number, width: number, height: number,
 *   pattern: string, tiers: Record<string, string>, poster: string }} FramesManifest
 */
/**
 * @typedef {{ canvas: HTMLCanvasElement, count: number, setProgress: (p: number) => void, setFrame: (i: number) => void,
 *   ready: () => Promise<void>, preloadAll: () => Promise<void>, destroy: () => void }} FrameSeq
 */
/**
 * @typedef {{ el: HTMLVideoElement, activate: () => void, deactivate: () => void,
 *   bindExport: (w: { start: number, duration: number }) => void, destroy: () => void }} Clip
 */

// ── C14 export ──
/**
 * @typedef {{ width: number, height: number, fps: number, secondsPerUnit: number, stopHold: number,
 *   travelMin: number, travelMax: number, lead: number, tail: number, ease: string, compositionId: string }} ExportOptions
 */
/**
 * @typedef {{ duration: number,
 *   segments: Array<{ kind: 'lead'|'travel'|'hold'|'tail', from: number, to: number, start: number, end: number }>,
 *   stopAt: Record<string, number> }} ExportPath
 */

// ── C15 boot ──
/**
 * @typedef {{ map: TimelineMap, built: BuiltDeck, driver?: ScrollDriver, presenter?: Presenter,
 *   rebuild: (reason: string) => Promise<void>, destroy: () => void }} DeckHandle
 */

export {};

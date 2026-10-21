import type { Step } from '../../../presentation-kit'
import { BookWorld, type WorldPayload } from '../Scene'
export const step: Step<WorldPayload> = {
  id:'book-step-2',era:"置く",title:"読み終えた一冊を、本棚へ。",caption:"持ち主から、共通の本棚へ。一冊の位置が変わり、関係が見えてきます。",groupKey:'book-world',payload:{"book": [290, 132, 106, 145], "owner": 1, "shelf": 1, "reader": 0, "arrow": "place", "note": false},Scene:BookWorld
}

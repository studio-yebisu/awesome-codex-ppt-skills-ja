import type { Step } from '../../../presentation-kit'
import { BookWorld, type WorldPayload } from '../Scene'
export const step: Step<WorldPayload> = {
  id:'book-step-7',era:"戻す",title:"もう一度、本棚へ。",caption:"同じ一冊を共通の本棚へ戻す。交換の輪をもう一度。",groupKey:'book-world',payload:{"book": [433, 153, 66, 95], "owner": 0.12, "shelf": 1, "reader": 0.22, "arrow": "return", "note": false},Scene:BookWorld
}

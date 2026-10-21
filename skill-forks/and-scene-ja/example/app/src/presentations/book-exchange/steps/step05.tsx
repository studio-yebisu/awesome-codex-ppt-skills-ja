import type { Step } from '../../../presentation-kit'
import { BookWorld, type WorldPayload } from '../Scene'
export const step: Step<WorldPayload> = {
  id:'book-step-5',era:"見つける",title:"読みたい本を、持ち帰る。",caption:"本棚の一冊が、次の読み手の側へ移ります。",groupKey:'book-world',payload:{"book": [545, 142, 80, 116], "owner": 0.12, "shelf": 0.45, "reader": 1, "arrow": "take", "note": false},Scene:BookWorld
}

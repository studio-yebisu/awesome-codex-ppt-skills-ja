import type { Step } from '../../../presentation-kit'
import { BookWorld, type WorldPayload } from '../Scene'
export const step: Step<WorldPayload> = {
  id:'book-step-4',era:"見つける",title:"次の読み手が、一冊を見つける。",caption:"本棚を眺める次の読み手と、同じ一冊をつなぎます。",groupKey:'book-world',payload:{"book": [433, 153, 66, 95], "owner": 0.12, "shelf": 1, "reader": 1, "arrow": "find", "note": false},Scene:BookWorld
}

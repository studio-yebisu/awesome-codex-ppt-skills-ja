import type { Step } from '../../../presentation-kit'
import { BookWorld, type WorldPayload } from '../Scene'
export const step: Step<WorldPayload> = {
  id:'book-step-1',era:"置く",title:"一冊の本が、次の人へ。",caption:"架空の交換本棚の提案。同じ一冊が、置く・見つける・戻すをつなぎます。",groupKey:'book-world',payload:{"book": [340, 55, 200, 270], "owner": 0, "shelf": 0, "reader": 0, "arrow": "", "note": false},Scene:BookWorld
}

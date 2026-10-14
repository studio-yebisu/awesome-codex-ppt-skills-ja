import type { Step } from '../../../presentation-kit'
import { BookWorld, type WorldPayload } from '../Scene'
export const step: Step<WorldPayload> = {
  id:'book-step-8',era:"戻す",title:"一冊を、次の人へ。",caption:"本棚を介して、一冊を次の人へ。料金・住所・営業実績は未設定です。",groupKey:'book-world',payload:{"book": [354, 80, 174, 236], "owner": 0.18, "shelf": 0.12, "reader": 0.18, "arrow": "cycle", "note": false},Scene:BookWorld
}

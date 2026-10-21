import type { Step } from '../../../presentation-kit'
import { BookWorld, type WorldPayload } from '../Scene'
export const step: Step<WorldPayload> = {
  id:'book-step-6',era:"戻す",title:"読み終えたら、次へつなぐ。",caption:"読み終わった一冊を、次の人へつなぐことを考えます。",groupKey:'book-world',payload:{"book": [545, 142, 80, 116], "owner": 0.12, "shelf": 0.12, "reader": 1, "arrow": "", "note": false},Scene:BookWorld
}

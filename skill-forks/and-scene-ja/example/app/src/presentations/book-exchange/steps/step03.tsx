import type { Step } from '../../../presentation-kit'
import { BookWorld, type WorldPayload } from '../Scene'
export const step: Step<WorldPayload> = {
  id:'book-step-3',era:"置く",title:"本の名前と、ひとことを添える。",caption:"本の名前と短いひとことを添える、という参加の案。",groupKey:'book-world',payload:{"book": [433, 153, 66, 95], "owner": 0.18, "shelf": 1, "reader": 0, "arrow": "", "note": true},Scene:BookWorld
}

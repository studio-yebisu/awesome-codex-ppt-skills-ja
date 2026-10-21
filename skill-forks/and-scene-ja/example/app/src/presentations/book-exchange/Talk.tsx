import { Presentation, type Step } from '../../presentation-kit'
import type { WorldPayload } from './Scene'
import {step as step1} from './steps/step01'
import {step as step2} from './steps/step02'
import {step as step3} from './steps/step03'
import {step as step4} from './steps/step04'
import {step as step5} from './steps/step05'
import {step as step6} from './steps/step06'
import {step as step7} from './steps/step07'
import {step as step8} from './steps/step08'
import './style.css'
const STEPS:Step<WorldPayload>[]=[step1,step2,step3,step4,step5,step6,step7,step8]
export default function Talk(){return <main className="book-talk"><Presentation steps={STEPS} title="一冊の本が、次の人へ。" initialMode="browse" brand={<span className="proposal">交換本棚の提案 <small>架空の企画</small></span>} homeHref="./index.html" homeLabel="提案の最初へ" marker={i=>`${String(i+1).padStart(2,'0')} / 08`} /></main>}

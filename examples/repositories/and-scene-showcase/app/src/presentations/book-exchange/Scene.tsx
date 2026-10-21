import { motion } from 'motion/react'
import { SceneLayer, MotionNode, Label, Arrow, type SceneProps } from '../../presentation-kit'
import { ENTITIES } from './entities'
export type WorldPayload={book:number[];owner:number;shelf:number;reader:number;arrow:string;note:boolean}
const labelOpacity=(n:number)=>n===0?0:Math.max(n,.75)
function Person({role,opacity}:{role:string;opacity:number}){return <><motion.svg animate={{opacity}} viewBox="0 0 100 110" aria-hidden="true"><circle cx="50" cy="28" r="19"/><path d="M15 104V91c0-22 16-35 35-35s35 13 35 35v13"/></motion.svg><motion.span animate={{opacity:labelOpacity(opacity)}}>{role}</motion.span></>}
function Book(){return <svg viewBox="0 0 150 205" aria-label="同じ一冊の本"><path className="book-front" d="M13 7H143V196H13c-9 0-12-7-12-15V24C1 13 5 7 13 7Z"/><path className="book-spine" d="M13 7V196M14 185H140"/><path className="book-lines" d="M44 55H111M44 63H90"/><text x="77" y="113" textAnchor="middle">BOOK</text><path className="book-mark" d="M100 7V35l10-6 10 6V7"/></svg>}
export function BookWorld({step}:SceneProps<WorldPayload>){const p=step.payload!;const [x,y,w,h]=p.book;return <SceneLayer className="world">
<div className="place owner-place"><MotionNode layoutId={ENTITIES.owner}><motion.div className="person"><Person role="持ち主" opacity={p.owner}/></motion.div></MotionNode></div>
<div className="place shelf-place"><MotionNode layoutId={ENTITIES.shelf}><motion.div className="shelf"><motion.svg animate={{opacity:p.shelf}} viewBox="0 0 230 250" aria-hidden="true"><path d="M20 20H210V230H20ZM20 100H210M20 180H210M44 230V245M186 230V245"/></motion.svg><motion.span animate={{opacity:labelOpacity(p.shelf)}}>共通の本棚</motion.span></motion.div></MotionNode></div>
<div className="place reader-place"><MotionNode layoutId={ENTITIES.reader}><motion.div className="person reader"><Person role="次の読み手" opacity={p.reader}/></motion.div></MotionNode></div>
<div className="place book-place" style={{left:x,top:y}} data-allow-overlap><MotionNode layoutId={ENTITIES.book} className="book" style={{width:w,height:h}}><Book/></MotionNode></div>
<div className="place arrow-place"><Arrow layoutId={ENTITIES.arrow}><motion.div animate={{opacity:p.arrow?1:0}} className={'connector '+p.arrow}>{p.arrow==='cycle'?<svg viewBox="0 0 526 340" aria-label="本棚から次の読み手へ。読んだら本棚へ戻す"><defs><marker id="cycle-tip" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10"/></marker></defs><path d="M10 35H515" markerEnd="url(#cycle-tip)"/><path d="M515 270V325H275V310" markerEnd="url(#cycle-tip)"/><text x="263" y="15" textAnchor="middle">本棚から、次の読み手へ</text><text x="395" y="302" textAnchor="middle">読んだら、本棚へ</text></svg>:p.arrow==='return'?'←':'→'}</motion.div></Arrow></div>
<div className="place note-place"><Label layoutId={ENTITIES.note}><motion.div animate={{opacity:p.note?1:0}} className="note">本の名前<br/><span>ひとこと</span></motion.div></Label></div>
</SceneLayer>}

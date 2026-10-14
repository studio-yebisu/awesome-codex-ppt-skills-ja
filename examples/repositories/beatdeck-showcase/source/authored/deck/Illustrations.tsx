/** Original explanatory SVGs, not product photography, process measurements or recipes. */
export function Dough() {
 return <svg viewBox="0 0 240 160" aria-label="生地の説明用図形" role="img"><path d="M30 123 C26 74 64 30 114 31 C170 17 213 69 211 121 Z" fill="var(--surface)" stroke="var(--ink)" strokeWidth="2"/><path d="M60 98 Q81 54 101 53 M129 50 Q160 57 178 88" fill="none" stroke="var(--hair-strong)" strokeWidth="2"/></svg>;
}
export function Bread({warm=false}:{warm?:boolean}) {
 return <svg viewBox="0 0 240 160" aria-label="パンの説明用図形" role="img"><path d="M26 120 C25 67 63 33 119 29 C177 24 215 63 215 119 L211 135 L31 135 Z" fill={warm?'var(--accent)':'var(--surface)'} stroke="var(--ink)" strokeWidth="2"/><path d="M80 50 L65 94 M120 41 L107 92 M160 46 L149 95" fill="none" stroke={warm?'var(--surface)':'var(--hair-strong)'} strokeWidth="3"/></svg>;
}
export function Shelf() {
 return <svg viewBox="0 0 300 170" aria-label="棚とパンの説明用図形。個数はデータではない" role="img"><path d="M21 42 V148 M279 42 V148 M21 113 H279 M21 148 H279" fill="none" stroke="var(--ink)" strokeWidth="2"/>{[30,114,198].map(x=><path key={x} d={`M${x} 100 C${x} 61 ${x+64} 58 ${x+68} 100 Z`} fill="var(--accent)" stroke="var(--ink)" strokeWidth="1.5"/>)}</svg>;
}

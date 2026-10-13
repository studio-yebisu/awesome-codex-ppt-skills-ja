// Original vector renderer by Studio Yebisu. CC0-1.0.
export const xml = value => String(value ?? '').replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[char]));
const number = value => Number.isFinite(Number(value)) ? Number(value) : 0;
const paint = (value, fallback) => /^#[0-9a-f]{3,8}$/i.test(value || '') || ['none','transparent'].includes(value) ? value : fallback;

export function validateDeck(deck) {
  if (!deck || !/^[a-z0-9-]+$/.test(deck.id || '') || !Array.isArray(deck.slides) || !deck.slides.length) throw new Error('idとslidesが必要です');
  for (const [i,slide] of deck.slides.entries()) {
    if (!slide.title || !Array.isArray(slide.nodes)) throw new Error(`${i+1}枚目: titleとnodesが必要です`);
    for (const node of slide.nodes) {
      if (!['text','rect','circle','line','path'].includes(node.type)) throw new Error(`未対応の要素: ${node.type}`);
      for (const key of ['x','y','w','h','r','x2','y2','size','delay']) {
        if (node[key] !== undefined && !Number.isFinite(node[key])) throw new Error(`${i+1}枚目: ${key}は有限の数値で指定してください`);
      }
      if (node.type === 'text' && (!node.text || node.size < 14)) throw new Error(`${i+1}枚目: 文字の内容と14px以上のサイズが必要です`);
      if (node.type === 'path' && !/^[MmLlHhVvCcSsQqTtAaZz0-9.,\s+-]+$/.test(node.d || '')) throw new Error('pathの形式が不正です');
      const x=node.x??0,y=node.y??0;
      if(x<0||x>1280||y<0||y>720)throw new Error(`${i+1}枚目: 座標がスライドの範囲を超えています`);
      if(node.type==='rect'&&(x+(node.w??0)>1280||y+(node.h??0)>720))throw new Error(`${i+1}枚目: 四角形がスライドの範囲を超えています`);
    }
  }
  return deck;
}

export function renderSlide(deck, index=0, {animate=false, label=true}={}) {
  const slide=deck.slides[index];
  if(!slide)throw new Error('指定したスライドがありません');
  const bg=paint(slide.background || deck.background,'#f7f7f2');
  const ink=paint(deck.ink,'#171b27');
  const font=xml(slide.font || deck.font || 'Noto Sans JP');
  const nodes=slide.nodes.map((node,i)=>{
    const fill=paint(node.fill,ink),stroke=paint(node.stroke,'none');
    const attrs=`fill="${fill}" stroke="${stroke}" stroke-width="${number(node.strokeWidth||0)}"`;
    const motion=animate?` class="reveal" style="animation-delay:${number(node.delay??i*65)}ms"`:'';
    let element='';
    if(node.type==='text'){
      const lines=String(node.text).split('\n');
      element=`<text x="${number(node.x)}" y="${number(node.y)}" font-size="${number(node.size||32)}" font-weight="${number(node.weight||400)}" font-family="${xml(node.font||font)}, sans-serif" letter-spacing="${number(node.spacing||0)}" text-anchor="${['middle','end'].includes(node.anchor)?node.anchor:'start'}" ${attrs}>${lines.map((line,j)=>`<tspan x="${number(node.x)}" dy="${j?number(node.leading||node.size*1.45):0}">${xml(line)}</tspan>`).join('')}</text>`;
    }else if(node.type==='rect')element=`<rect x="${number(node.x)}" y="${number(node.y)}" width="${number(node.w)}" height="${number(node.h)}" rx="${number(node.rx||0)}" ${attrs}/>`;
    else if(node.type==='circle')element=`<circle cx="${number(node.x)}" cy="${number(node.y)}" r="${number(node.r)}" ${attrs}/>`;
    else if(node.type==='line')element=`<line x1="${number(node.x)}" y1="${number(node.y)}" x2="${number(node.x2)}" y2="${number(node.y2)}" ${attrs}/>`;
    else element=`<path d="${xml(node.d)}" ${attrs}/>`;
    return `<g${motion}>${element}</g>`;
  }).join('');
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720"${label?` role="img" aria-label="${xml(slide.title)}"`:''}><title>${xml(slide.title)}</title>${animate?'<style>.reveal{animation:appear .6s cubic-bezier(.16,1,.3,1) both;transform-box:fill-box;transform-origin:center}@keyframes appear{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:translateY(0)}}@media(prefers-reduced-motion:reduce){.reveal{animation:none}}</style>':''}<rect width="1280" height="720" fill="${bg}"/>${nodes}</svg>`;
}

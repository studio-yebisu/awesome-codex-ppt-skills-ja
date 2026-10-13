import { useState, useEffect, useCallback } from 'react';
import { AnimatePresence } from 'framer-motion';
import { slides } from './slides';

export default function App() {
  const [current, setCurrent] = useState(0);
  const total = slides.length;

  const goNext = useCallback(() => setCurrent((c) => Math.min(c + 1, total - 1)), [total]);
  const goPrev = useCallback(() => setCurrent((c) => Math.max(c - 1, 0)), []);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if(e.key==='Escape'&&parent!==window){parent.postMessage({type:'yebisu-close'},location.origin);return;}
      if((e.target as Element).closest('input,textarea,select,[data-interactive]:not(.native-nav)'))return;
      if((e.key===' '||e.key==='Enter')&&(e.target as Element).closest('button,a'))return;
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'Enter') {
        e.preventDefault();
        goNext();
      } else if (e.key === 'ArrowLeft') {
        e.preventDefault();
        goPrev();
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [goNext, goPrev]);


  useEffect(() => {
    const receive = (e: MessageEvent) => {if(e.origin!==location.origin||e.source!==parent||e.data?.type!=='yebisu-slide'||!Number.isInteger(e.data.index))return;setCurrent(Math.max(0,Math.min(total-1,e.data.index)));};
    window.addEventListener('message',receive);return()=>window.removeEventListener('message',receive);
  },[total]);
  useEffect(()=>{if(parent!==window)parent.postMessage({type:'yebisu-page',index:current,total},location.origin)},[current,total]);

  const CurrentSlide = slides[current];

  return (
    <div data-deck-page={current} onClick={(e)=>{if((e.target as Element).closest('button,input,textarea,select,a,[data-interactive]'))return;(e.clientX>innerWidth/2?goNext:goPrev)();}} style={{ width: '100vw', height: '100vh', position: 'relative', overflow: 'hidden', background: '#1a1a1a' }}>
      <AnimatePresence mode="wait">
        <CurrentSlide key={current} />
      </AnimatePresence>

      <nav className="native-nav" data-interactive aria-label="資料のページ移動">
        <button style={{padding:'10px 24px'}} onClick={goPrev} disabled={current===0}>前へ</button>
        <button style={{padding:'10px 24px'}} onClick={goNext} disabled={current===total-1}>次へ</button>
        <p>架空の企画案</p>
      </nav>
      {/* Progress bar */}
      <div
        style={{
          position: 'fixed',
          bottom: 0,
          left: 0,
          width: '100%',
          height: 3,
          background: 'rgba(255,255,255,0.05)',
          zIndex: 50,
        }}
      >
        <div
          style={{
            height: '100%',
            width: `${((current + 1) / total) * 100}%`,
            background: '#FF5722',
            transition: 'width 0.3s ease',
          }}
        />
      </div>

      {/* Slide counter */}
      <div
        style={{
          position: 'fixed',
          bottom: 12,
          right: 20,
          fontFamily: "'FAQ Japanese', sans-serif",
          fontSize: 'clamp(13px,1.2vw,18px)',
          color: '#a0a0a0',
          zIndex: 50,
        }}
      >
        {current + 1} / {total}
      </div>
    </div>
  );
}

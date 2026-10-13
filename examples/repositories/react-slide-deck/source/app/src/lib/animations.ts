import type { Variants } from 'framer-motion';

export const slideVariants: Variants = {
  enter: { opacity: 0, y: 30 },
  center: { opacity: 1, y: 0, transition: { duration: 0.5, ease: 'easeOut' } },
  exit: { opacity: 0, y: -20, transition: { duration: 0.3, ease: 'easeIn' } },
};

export const fadeUp: Variants = {
  hidden: { opacity: 0, y: 24 },
  visible: (i: number = 0) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.12, duration: 0.5, ease: 'easeOut' },
  }),
};

export const fadeIn: Variants = {
  hidden: { opacity: 0 },
  visible: (i: number = 0) => ({
    opacity: 1,
    transition: { delay: i * 0.1, duration: 0.4 },
  }),
};

export const scaleIn: Variants = {
  hidden: { opacity: 0, scale: 0.9 },
  visible: (i: number = 0) => ({
    opacity: 1,
    scale: 1,
    transition: { delay: i * 0.12, duration: 0.5, ease: 'easeOut' },
  }),
};

export const staggerContainer: Variants = {
  hidden: {},
  visible: {
    transition: { staggerChildren: 0.1, delayChildren: 0.2 },
  },
};

if(window.matchMedia('(prefers-reduced-motion: reduce)').matches){for(const variants of [slideVariants,fadeUp,fadeIn,scaleIn,staggerContainer])for(const key of Object.keys(variants)){const v=variants[key];variants[key]=typeof v==='function'?()=>({opacity:1,y:0,scale:1,transition:{duration:0}}):{opacity:1,y:0,scale:1,transition:{duration:0}};}}

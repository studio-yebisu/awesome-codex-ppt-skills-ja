export const presentations=[{slug:'book-exchange',title:'一冊の本が、次の人へ。',load:()=>import('./book-exchange/Talk')}]
export const presentationSlugs=new Set(presentations.map(p=>p.slug))

export function caseCountLabel(study){
  if(study.page_unit==='段階')return (study.scene_count?study.scene_count+'場面 / ':'')+study.page_count+'段階';
  return study.page_count+'枚';
}

export function collectionCountLabel(studies){
  const pages=studies.filter(c=>c.page_unit!=='段階').reduce((n,c)=>n+c.page_count,0);
  const steps=studies.filter(c=>c.page_unit==='段階').reduce((n,c)=>n+c.page_count,0);
  return studies.length+'冊 / '+[pages||!steps?pages+'枚':'',steps?steps+'段階':''].filter(Boolean).join(' + ');
}

export function playbackCounter(study,index){
  return (index+1)+' / '+study.page_count+(study.page_unit==='段階'?' 段階':'');
}

export function playbackOrdinal(study,index){
  return (index+1)+(study.page_unit==='段階'?'段階目':'ページ目');
}

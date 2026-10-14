export function caseDownloadName(study,path){
 let title=String(study.title||study.id||'資料').normalize('NFC')
  .replace(/[<>:"/\\|?*\u0000-\u001f]/g,'・').replace(/\s+/g,' ').trim().slice(0,100).replace(/[。．. ]+$/g,'');
 if(!title)title='資料';
 if(/^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])$/i.test(title))title='資料 '+title;
 const extension=new URL(path,'https://atelier.example/').pathname.match(/\.[a-z0-9]+$/i)?.[0]||'';
 return title+extension;
}

// Frontend Slides' editing contract: E, local persistence, Ctrl+S HTML export.
if(parent!==window)document.documentElement.classList.add('catalog-embedded');
const count=document.getElementById('page-count');count.textContent='1 / '+presentation.slides.length;
document.getElementById('prev').onclick=()=>presentation.showSlide(presentation.currentSlide-1);
document.getElementById('next').onclick=()=>presentation.showSlide(presentation.currentSlide+1);
const editable=[...document.querySelectorAll('[data-edit]')],key='CASE_STORAGE_KEY';
const original=editable.map(el=>el.innerHTML);
try{const saved=JSON.parse(localStorage.getItem(key)||'null');if(Array.isArray(saved)&&saved.length===editable.length)editable.forEach((el,i)=>el.innerHTML=saved[i])}catch{}
let editing=false;
const toggle=document.getElementById('editToggle');
function edit(){editing=!editing;editable.forEach(el=>el.contentEditable=String(editing));toggle.classList.toggle('active',editing)}
toggle.onclick=edit;const hotzone=document.querySelector('.edit-hotzone');hotzone.onclick=edit;
hotzone.onmouseenter=()=>toggle.classList.add('show');toggle.onmouseleave=()=>{if(!editing)toggle.classList.remove('show')};
editable.forEach(el=>el.addEventListener('input',()=>{try{localStorage.setItem(key,JSON.stringify(editable.map(el=>el.innerHTML)))}catch{}}));
const saveLink=document.createElement('a');saveLink.id='saveHtml';saveLink.textContent='HTMLを保存';saveLink.download='CASE_ID.html';document.querySelector('.deck-controls').append(saveLink);
const resetButton=document.createElement('button');resetButton.id='resetHtml';resetButton.textContent='初期状態へ戻す';document.querySelector('.deck-controls').append(resetButton);
let saveUrl;
function updateDownload(){
  const clone=document.documentElement.cloneNode(true);
  clone.querySelectorAll('[contenteditable]').forEach(el=>el.removeAttribute('contenteditable'));
  clone.querySelectorAll('#saveHtml,#resetHtml').forEach(el=>el.remove());
  clone.querySelector('#editToggle')?.classList.remove('active');
  if(saveUrl)URL.revokeObjectURL(saveUrl);
  saveUrl=URL.createObjectURL(new Blob(['<!doctype html>'+clone.outerHTML],{type:'text/html'}));saveLink.href=saveUrl;
}
resetButton.onclick=()=>{editable.forEach((el,i)=>el.innerHTML=original[i]);localStorage.removeItem(key);updateDownload()};
editable.forEach(el=>el.addEventListener('input',updateDownload));updateDownload();
document.addEventListener('keydown',e=>{
  const save=(e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='s';
  if(e.target.isContentEditable&&!save)return;
  if(e.key.toLowerCase()==='e')edit();
  if(save){e.preventDefault();updateDownload();saveLink.click()}
});

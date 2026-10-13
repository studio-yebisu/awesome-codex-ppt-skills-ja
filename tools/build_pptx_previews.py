"""Standalone viewer for PNGs exported from completed PowerPoint files."""
from pathlib import Path
import html,json
ROOT=Path(__file__).resolve().parents[1]
for c in json.loads((ROOT/"data/case-studies.json").read_text(encoding="utf-8")):
    if c["format"]!="pptx":continue
    folder=ROOT/"examples/cases"/c["id"]
    pages=[dict(image="render/slide-"+str(i+1).zfill(2)+".png",title=t) for i,t in enumerate(c["titles"])]
    doc='<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+html.escape(c["title"])+'</title><style>body{margin:0;background:#182119;color:#fff;font-family:sans-serif}img{width:100vw;height:calc(100dvh - 50px);object-fit:contain}nav{height:40px;display:flex;gap:14px;align-items:center;justify-content:center}button,a{color:white;background:#283929;border:1px solid #666;padding:8px;text-decoration:none}</style><img id="page" alt=""><nav><button id="prev">←</button><span id="counter"></span><button id="next">→</button><a href="deck.pptx" download>PPTX ↓</a><a href="render/deck.pdf" download>PDF ↓</a></nav><script>const pages='+json.dumps(pages,ensure_ascii=False)+';let n=0;function show(i){n=Math.max(0,Math.min(i,pages.length-1));document.getElementById("page").src=pages[n].image;document.getElementById("page").alt=pages[n].title;document.getElementById("counter").textContent=(n+1)+" / "+pages.length;}document.getElementById("prev").onclick=()=>show(n-1);document.getElementById("next").onclick=()=>show(n+1);document.addEventListener("keydown",e=>{if(e.key==="ArrowRight")show(n+1);if(e.key==="ArrowLeft")show(n-1)});show(0);</script></html>'
    (folder/"index.html").write_text(doc,encoding="utf-8",newline="\n")
print("Standalone viewers of real PowerPoint renders built")

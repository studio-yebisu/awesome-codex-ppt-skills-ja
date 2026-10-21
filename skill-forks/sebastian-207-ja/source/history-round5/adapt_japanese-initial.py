from pathlib import Path
import json
b=Path('/workspace/shared/slide-207-prep/adapted/codex-ppt-skill')
f=b/'design-system/native/theme.mjs';s=f.read_text().replace('zh-CN','ja-JP').replace('doc.company = "codex-ppt-skill"','doc.company = "Studio Yebisu"');f.write_text(s)
f=b/'design-system/native/layouts.mjs';s=f.read_text();
for a,z in {'核心观点':'企画の視点','观点':'企画の宣言','主题主视觉':'表紙の挿絵','场景视觉':'街の風景','能力图解':'体験の設計','流程图解':'体験の流れ','数据关系':'関係図','案例画面':'編集の風景','内容图解':'体験の断片','方案 A':'これまで','方案 B':'編集室','WHY IT MATTERS':'企画の意図','BEFORE':'いつもの読書','AFTER':'編集室の読書'}.items():s=s.replace(a,z)
# closing echo: preserve original typography, omit default placeholder panel
s=s.replace('  const rect = { x: 7.32, y: 0.68, w: 4.95, h: 5.98 };','  if (variant === "minimal") return;\n  const rect = { x: 7.32, y: 0.68, w: 4.95, h: 5.98 };')
# meaning-bound Japanese label and remove decorative default motifs on statement/quote
s=s.replace('  visualMotif(slide, ShapeType, { x: 10.1, y: 1.58, w: 2.25, h: 3.48 }, style, "grid");','')
s=s.replace('  visualMotif(slide, ShapeType, { x: 9.35, y: 3.0, w: 2.7, h: 2.15 }, style, "stack");','')
s=s.replace('  visualMotif(slide, ShapeType, { x: rect.x + rect.w - 1.45, y: rect.y + rect.h - 1.16, w: 1.04, h: 0.78 }, style, "stack");','')
f.write_text(s)
f=b/'scripts/build_native_pptx.mjs';s=f.read_text().replace('`讲解本页：${s.title || ""}`','`本頁の説明：${s.title || ""}`');f.write_text(s)
r=Path('/workspace/shared/slide-207-prep/ppt_runs/2026-10-14_machi-yohaku')
f=r/'spec_lock.json';d=json.loads(f.read_text());d['fonts']={'heading':'Noto Serif CJK JP','body':'Noto Sans CJK JP','number':'DejaVu Sans'};d['execution_status']='authorized_for_this_sample';f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
f=r/'slides_plan.json';d=json.loads(f.read_text());d['slides'][3]['title']='棚の読書、編集台の対話';d['slides'][4]['title']='街で拾った断片が、一冊になる';d['slides'][5]['title']='週末編集室の体験';d['slides'][6]['title']='4週間の試行計画';f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
f=r/'asset_plan.json';d=json.loads(f.read_text());a=d['assets'][0];a['backend']='codex_builtin_imagegen';a['generation_backend']='codex_builtin_imagegen';a['generation_required']=True;a['status']='generated';a['prompt_path']=str(r/'cover_prompt.txt');a['semantic_binding']['bound_to_slide']=True;a['semantic_binding']['intended_composition']='縦5:6。中央に本と街の紙工作を配置し、原典表紙右側枠に挿入。文字はネイティブで左側に保持。';f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')

import json
from pathlib import Path
p=Path(__file__).parent
req=json.loads((p/'page_request.json').read_text(encoding='utf-8-sig'))
navy='#0D2C56'; teal='#12949B'; pale='#E7F4FA'
m={'slide':req['slide'],'content_box':req['content_box'],'source':{'path':'source.png','width_px':1672,'height_px':941},'page_strategy':'Native Japanese text, layout cards and arrows with builtin image-edit separated icons','text_inventory':[],'visual_inventory':[],'background_strategy':{'mode':'native-or-script','source_consistency_contract':'Preserve white background, pale blue panels, teal pills and three-column source geometry.','removed_foreground':'No source background bitmap reused; text and three icons rebuilt independently.','comparison_note':'Solid background and panel source geometry retained; minor source texture is replaced by uniform fills.'},'quality_checks':{'font_size_calibrated':False,'visual_inventory_matched':False,'background_strategy_checked':False,'shape_corner_geometry_checked':False},'text_boxes':[],'shapes':[],'images':[],'asset_provenance':[]}
def shape(id,box,fill,r):
 m['shapes'].append({'id':id,'type':'roundRect','box_px':box,'fill':fill,'stroke':'none','source_corner_radius_px':r,'corner_category':'pill' if r>=box[3]/2 else 'large-radius','z_index':10})
def text(id,s,box,size,align='left',color=navy):
 m['text_inventory'].append({'id':id,'text':s,'decision':'native-text'})
 m['text_boxes'].append({'id':id,'text':s,'box_px':box,'font':'Yu Gothic','preview_font':'C:/Windows/Fonts/YuGothB.ttc','font_size':size,'font_size_source':'measured','bold':True,'color':color,'align':align,'valign':'middle','wrap':'none','line_height':1.0,'z_index':40})
text('title','Gitの保存・記録・共有',[77,54,1260,158],76)
text('subtitle','はじめてのGit・3分入門',[87,212,825,88],36)
shape('callout',[56,762,1560,127],pale,32)
text('conclusion','保存しただけでは、履歴にも共有先にも届かない',[159,779,1362,96],36,'center')
for i,(x,word,desc) in enumerate([(93,'保存','ファイルに反映'),(627,'記録','手元の履歴に残す'),(1161,'共有','リモートへ送る')]):
 shape(f'card-{i}',[x,326,421,396],pale,30)
 shape(f'pill-{i}',[x+66,562,287,79],teal,39.5)
 text(f'label-{i}',word,[x+66,562,287,79],32,'center','#FFFFFF')
 text(f'desc-{i}',desc,[x+24,650,373,58],23,'center')
for i,x in enumerate([534,1068]):
 pts=[[x,469],[x+38,469],[x+38,445],[x+77,493],[x+38,541],[x+38,517],[x,517]]
 m['shapes'].append({'id':f'arrow-{i}','type':'polygon','box_px':[x,445,77,96],'polygon_px':pts,'fill':teal,'stroke':'none','z_index':20})
for name,box in [('document',[204,342,201,218]),('history',[721,349,252,207]),('upload',[1228,346,283,211])]:
 path=f'assets/icons/{name}.png'
 m['images'].append({'id':name,'path':path,'box_px':box,'z_index':30})
 m['visual_inventory'].append({'id':name,'role':'foreground','object_type':'icon','path':path,'source_type':'asset-sheet-separated'})
 m['asset_provenance'].append({'path':path,'source':'assets/icon-sheet.png','source_type':'asset-sheet-separated','provenance_note':'Builtin image_gen edited source.png into the three-icon chroma sheet; original editppt image import and process-sheet removed green and split inspected complete-object regions. See imagegen-jobs.json and command logs.'})
m['visual_inventory'].append({'role':'structure','description':'Three large-radius cards, three pill fills, one large-radius conclusion panel and two ordinary right-pointing arrows are native structural shapes.'})
(p/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')

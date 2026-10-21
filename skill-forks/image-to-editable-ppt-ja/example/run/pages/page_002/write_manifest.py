import json
from pathlib import Path
p=Path(__file__).parent
req=json.loads((p/'page_request.json').read_text(encoding='utf-8-sig'))
navy='#0D2C56';teal='#12949B';pale='#E7F4FA'
m={'slide':req['slide'],'content_box':req['content_box'],'source':{'path':'source.png','width_px':1672,'height_px':941},'page_strategy':'Native Japanese Git three-place diagram with source-faithful builtin image-edit separated icons','text_inventory':[],'visual_inventory':[],'background_strategy':{'mode':'native-or-script','source_consistency_contract':'Preserve white backdrop, pale near-white local container and cyan border, pale cyan cards, teal pills, all positions and radii.','removed_foreground':'No background bitmap reused; all text and icons rebuilt independently.','comparison_note':'Native structural fills preserve source layout; subtle source texture omitted.'},'quality_checks':{'font_size_calibrated':False,'visual_inventory_matched':False,'background_strategy_checked':False,'shape_corner_geometry_checked':False},'text_boxes':[],'shapes':[],'images':[],'asset_provenance':[]}
def shape(id,box,fill,r,stroke='none',width=0):
 m['shapes'].append({'id':id,'type':'roundRect','box_px':box,'fill':fill,'stroke':stroke,'stroke_width':width,'source_corner_radius_px':r,'corner_category':'pill' if r>=box[3]/2 else 'large-radius','z_index':10})
def text(id,s,box,size,align='left',color=navy):
 m['text_inventory'].append({'id':id,'text':s,'decision':'native-text'})
 m['text_boxes'].append({'id':id,'text':s,'box_px':box,'font':'Yu Gothic','preview_font':'C:/Windows/Fonts/YuGothB.ttc','font_size':size,'font_size_source':'measured','bold':True,'color':color,'align':align,'valign':'middle','wrap':'none','line_height':1.0,'z_index':40})
text('title','変更は3つの場所を進む',[77,53,1395,161],74.5)
shape('local-container',[54,232,1566,505],'#F5FBFD',30,'#B1DEF5',4.5)
text('local-heading','自分のパソコン（ローカル）',[208,248,650,66],27)
for i,(box,pill,word,desc) in enumerate([([85,329,405,381],[120,554,341,76],'作業ツリー','編集中のファイル'),([647,329,378,381],[685,554,302,76],'ステージ','次に記録する内容'),([1195,329,393,381],[1226,554,333,76],'ローカル履歴','コミットの記録')]):
 shape(f'card-{i}',box,pale,29);shape(f'pill-{i}',pill,teal,38)
 text(f'label-{i}',word,pill,27,'center','#FFFFFF')
 text(f'desc-{i}',desc,[box[0]+16,637,box[2]-32,59],23,'center')
for i,x in enumerate([526,1068]):
 pts=[[x,466],[x+41,466],[x+41,443],[x+89,488],[x+41,533],[x+41,510],[x,510]]
 m['shapes'].append({'id':f'arrow-{i}','type':'polygon','box_px':[x,443,89,90],'polygon_px':pts,'fill':teal,'stroke':'none','z_index':20})
text('add','git add',[499,547,140,53],25,'center')
text('commit','git commit',[1029,547,164,53],25,'center')
for i,(box,s) in enumerate([([55,763,773,124],'git add は記録する内容を選ぶ'),([846,763,773,124],'git commitで手元の履歴に残す')]):
 shape(f'callout-{i}',box,pale,28)
 text(f'conclusion-{i}',s,[box[0]+32,784,box[2]-64,79],29,'center')
for name,box in [('laptop',[100,242,95,75]),('document',[194,339,197,214]),('staging',[738,342,198,208]),('database',[1303,345,173,205])]:
 path=f'assets/icons/{name}.png'
 m['images'].append({'id':name,'path':path,'box_px':box,'z_index':30})
 m['visual_inventory'].append({'id':name,'role':'foreground','object_type':'icon','path':path,'source_type':'asset-sheet-separated'})
 m['asset_provenance'].append({'path':path,'source':'assets/icon-sheet.png','source_type':'asset-sheet-separated','provenance_note':'Builtin image_gen edited source.png into four-object sheet; original editppt import and process-sheet keyed green and split inspected regions. Full prompt, hashes, returned path in builtin-imagegen-receipt.json.'})
m['visual_inventory'].append({'role':'structure','description':'Large local container, three cards, three teal pill fills, two conclusion panels and two ordinary arrows are native structural shapes.'})
(p/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')

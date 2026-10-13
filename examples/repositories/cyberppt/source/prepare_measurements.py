"""Manual blueprint element measurements; not measured rendered object bounds."""
from pathlib import Path
import json,subprocess,sys,hashlib
P=Path(__file__).resolve().parents[1]
O=json.loads((P/'input/outline.json').read_text(encoding='utf-8'))
def dump(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def page(n):
    E=[]
    def add(id,kind,b,**kw): E.append(dict(element_id=id,kind=kind,priority='P0' if id in ['title','takeaway','footer'] else 'P1',source_component=id,blueprint_bbox_px=dict(zip(['x','y','w','h'],b)),**kw))
    def t(id,txt,b,sz=20,**kw):add(id,'text',b,text=txt,font_size_pt=sz,role='C0' if n==1 and id=='title' else 'T2' if id=='title' else 'T14' if id=='footer' else 'T7',**kw)
    def l(id,b,**kw):add(id,'line',b,**kw)
    def r(id,b,**kw):add(id,'rect',b,**kw)
    a=O['slides'][n-1]
    if n==1:
      l('cover-accent',[71,120,102,0.5],color='9A5A2E',width=1.6)
      t('title','商店街のイベント案内を、\n一つにまとめる',[68,157,1230,185],44,bold=True)
      t('subtitle',a['subtitle'],[68,410,650,50],19)
      l('subtitle-rule',[68,388,472,.5])
      t('page-number','01',[1425,35,190,160],94,font='Times New Roman',color='9A5A2E')
      l('number-rule',[1435,207,170,.5])
      for i,(x,label,icon) in enumerate([(720,'見つける','search'),(1053,'選ぶ','calendar-event'),(1385,'迷わず行く','map-pin')]):
        add('circle-'+str(i),'ellipse',[x,375,170,170],stroke='9A5A2E',width=1.2)
        add('icon-'+str(i),'icon',[x+39,414,92,92],icon=icon)
        t('label-'+str(i),label,[x-42,563,255,60],25,bold=True,align='center')
      l('arrow-1',[913,461,110,.5],color='9A5A2E',width=1.3,arrow=True);l('arrow-2',[1245,461,111,.5],color='9A5A2E',width=1.3,arrow=True)
      l('bottom-rule',[68,727,1538,.5]);t('takeaway',a['so_what'][0],[310,765,1090,74],28,font='Yu Mincho',color='9A5A2E',align='center')
      t('footer','架空の企画例。実在の開催情報ではありません。',[1218,875,390,28],10,color='76716A')
    elif n==2:
      t('page-number','02',[40,48,52,49],20,bold=True,color='9A5A2E');l('number-rule',[102,34,.5,75],color='9A5A2E')
      t('title',a['title'],[141,27,1460,80],36,bold=True);t('subtitle',a['subtitle'],[142,115,1480,45],20,bold=True)
      l('header-rule',[40,182,1592,.5],color='9A5A2E');t('section','案内の入口をそろえる',[39,213,900,49],21,bold=True,color='9A5A2E')
      for id,txt,b,col in [('current','現状の仮説',[144,300,285,45],'161616'),('proposal','提案',[790,300,100,45],'9A5A2E'),('keep','残すもの',[1330,300,220,45],'9A5A2E')]: t(id,txt,b,21,bold=True,color=col)
      for i,(label,y) in enumerate([('SNS',361),('Web',478),('掲示板',595)]):
        r('source-box-'+str(i),[73,y,331,92],stroke='9A5A2E',width=1.2);t('source-label-'+str(i),label,[100,y+20,277,50],21,bold=True,align='center')
      r('list-box',[600,392,472,254],stroke='9A5A2E',width=1.2);t('list-label','共通のイベント一覧',[642,484,399,76],25,bold=True,align='center')
      r('details-box',[1217,392,415,254],stroke='9A5A2E',width=1.2);t('details-label','各店の詳しい案内への\nリンク',[1232,472,385,100],19,bold=True,align='center')
      l('route-1',[404,407,195,73],color='9A5A2E',arrow=True);l('route-2',[404,521,195,.5],color='9A5A2E',arrow=True);l('route-3',[404,560,195,78],color='9A5A2E',arrow=True,flipV=True);l('route-4',[1072,521,144,.5],color='9A5A2E',arrow=True)
      t('caveat','現地調査は未実施',[39,729,500,36],14);l('bottom-rule',[40,804,1592,.5],color='9A5A2E');t('takeaway',a['so_what'][0],[40,832,1290,62],27,bold=True,color='9A5A2E');t('footer','架空の企画例。課題は検証前の仮説です。',[1348,875,289,31],8)
    else:
      configs={3:([35,193,1603,521],[35,359,679,1006,1319,1638],[193,297,434,575,714],[139,23,1460,79],[140,110,1480,54]),4:([49,247,1574,499],[49,490,1030,1623],[247,329,467,605,746],[49,81,1575,84],[49,174,1550,51]),5:([51,238,1569,418],[51,505,1073,1620],[238,325,448,552,656],[194,50,1425,94],[197,157,1420,53])}
      box,xs,ys,tb,sb=configs[n]
      if n==3:t('page-number','03',[31,34,61,51],23,bold=True,color='9A5A2E');l('number-rule',[106,26,.5,69],color='9A5A2E')
      if n==4:t('page-number','04',[49,19,61,50],23,bold=True,color='9A5A2E');l('number-rule',[120,46,1505,.5],color='9A5A2E')
      if n==5:add('number-disc','ellipse',[51,44,107,107],fill='9A5A2E',stroke='none');t('page-number','05',[64,62,82,66],33,bold=True,color='FFFFFF',align='center')
      t('title',a['title'],tb,34 if n==3 else 35 if n==4 else 38,bold=True);t('subtitle',a['subtitle'],sb,20)
      r('table-header',[xs[0],ys[0],xs[-1]-xs[0],ys[1]-ys[0]],fill='9A5A2E',stroke='none')
      for i,x in enumerate(xs):l('table-v-'+str(i),[x,ys[0],.5,ys[-1]-ys[0]])
      for i,y in enumerate(ys):l('table-h-'+str(i),[xs[0],y,xs[-1]-xs[0],.5])
      table=a['tables'][0]
      for c,label in enumerate(table['headers']):t('header-'+str(c),label,[xs[c]+10,ys[0]+17,xs[c+1]-xs[c]-20,ys[1]-ys[0]-30],22,bold=True,color='FFFFFF',align='center')
      for row,vals in enumerate(table['rows']):
        for c,label in enumerate(vals):
          if n==3 and c==1:label=label.replace('）','）\n')
          if n==3 and row==0 and c==3:label='入場無料／\n購入は別'
          if n==3 and row==0 and c==4:label='小雨実施・\n荒天中止'
          if n==5 and row==0 and c==1:label='来訪者に目的の案内を探して\nもらう'
          if n==5 and row==2 and c==2:label='文字の読みやすさ・\n問い合わせ'
          pad=140 if n==4 and c==0 else 27 if n==3 else 40
          t(f'cell-{row}-{c}',label,[xs[c]+pad,ys[row+1]+20,xs[c+1]-xs[c]-pad-20,ys[row+2]-ys[row+1]-40],19 if n==3 else 20,bold=n==4 and c==0 or n==5 and c==0)
        if n==4:
          cy=[393,535,677][row];add('step-disc-'+str(row),'ellipse',[89,cy-30,60,60],fill='9A5A2E',stroke='none');t('step-number-'+str(row),str(row+1),[91,cy-25,56,50],24,bold=True,color='FFFFFF',align='center')
          if row<2:l('step-arrow-'+str(row),[119,cy+37,.5,69],color='9A5A2E',arrow=True,width=1.2)
      if n==3:
        t('note-1',a['annotations'][0],[47,733,1450,40],15);t('note-2',a['annotations'][1],[47,781,1470,40],15);l('bottom-rule',[35,849,1604,.5]);t('takeaway',a['so_what'][0],[35,863,1190,54],24,bold=True,color='9A5A2E');t('footer','架空の企画例。開催情報はすべて例示。',[1278,886,365,32],10)
      if n==4:
        t('note-1',a['annotations'][0],[50,773,1540,40],15);l('bottom-rule',[49,835,1575,.5],color='9A5A2E');t('takeaway',a['so_what'][0],[400,849,873,58],24,bold=True,color='9A5A2E',align='center');t('footer','架空の企画例。担当体制は提案であり未合意。',[1288,894,339,27],8)
      if n==5:
        t('note-1',a['annotations'][0],[50,683,1550,49],19);t('note-2',a['annotations'][1],[50,736,1550,49],19);l('bottom-rule',[51,811,1570,.5],width=1.4);t('takeaway',a['so_what'][0],[51,829,1250,75],29,bold=True,color='9A5A2E');t('footer','架空の企画例。試行は提案であり未実施。',[1300,875,330,29],9)
    # Thin strokes need a non-empty comparison crop; preserve draw geometry separately.
    for e in E:
      if e['kind']=='line':
        e['draw_bbox_px']=dict(e['blueprint_bbox_px'])
        b=e['blueprint_bbox_px']
        if b['h']<4:b['y']-=2;b['h']=5
        if b['w']<4:b['x']-=2;b['w']=5
    dump(P/f'design/slide-{n:02d}-elements.json',{'slide':n,'title':a['title'],'notes':'架空の制作例。'+a['subtitle']+'。'+a['so_what'][0],'measurement_method':'Manual pixel bounds on the ImageGen blueprint, recorded before native generation. These are layout bounds; rendered ink bounds are measured separately.','elements':E})
    components=[{'id':e['element_id'],'type':e['kind'],'priority':e['priority'],'required_subcomponents':[e['element_id']],'content_lock_refs':['title' if e['element_id']=='title' else 'annotations'],'must_preserve_type':True} for e in E]
    dump(P/f'design/slide-{n:02d}-components.json',{'components':components})
    receipts=[]
    for tool,args in [('build_component_signature.py',['--blueprint',str(P/f'design/slide-{n:02d}-blueprint.png'),'--content-lock',str(P/f'design/slide-{n:02d}-content-lock.json'),'--components',str(P/f'design/slide-{n:02d}-components.json'),'--slide',str(n),'--out',str(P/f'design/slide-{n:02d}-signature.json')]),('measure_blueprint.py',['--blueprint',str(P/f'design/slide-{n:02d}-blueprint.png'),'--annotations',str(P/f'design/slide-{n:02d}-elements.json'),'--out',str(P/f'design/slide-{n:02d}-registry.json')])]:
      argv=[sys.executable,str(P/'source/upstream/scripts'/tool)]+args
      r=subprocess.run(argv,capture_output=True,text=True);log=P/f'review/{n:02d}-{tool}.log';log.write_text(r.stdout+'\n'+r.stderr,encoding='utf-8')
      receipts.append({'argv':argv,'exit_code':r.returncode,'log':str(log.relative_to(P)).replace('\\','/'),'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest()});r.check_returncode()
    dump(P/f'review/slide-{n:02d}-measurement-receipts.json',receipts)
for n in ([int(sys.argv[1])] if len(sys.argv)>1 else range(1,6)):page(n)

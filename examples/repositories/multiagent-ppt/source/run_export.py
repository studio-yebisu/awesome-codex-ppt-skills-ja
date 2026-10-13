from pathlib import Path
import json,sys
source=Path(__file__).parent/'upstream/backend/save_ppt'
sys.path.insert(0,str(source))
import ppt_generator as original
# Data-only mapping correction: indices of cloned placeholders in the shipped template.
original.SlideConfig.SHAPE_IDS['TITLE_PAGE_DATE']=3
original.SlideConfig.SHAPE_IDS['SUBCHAPTER_TITLE']=2
original.SlideConfig.SHAPE_IDS['SUBCHAPTER_ITEMS'][3]=[3,5,4]
# This route has no image URLs. Fail instead of silently downloading anything.
def no_network(*args,**kwargs):
    raise RuntimeError('Network disabled for this local export demonstration')
original.requests.sessions.Session.request=no_network
result=original.start_generate_presentation(json.loads((Path(__file__).parents[1]/'input/data.json').read_text(encoding='utf8')))
assert result, 'Original exporter failed'
print('OUTPUT='+result)

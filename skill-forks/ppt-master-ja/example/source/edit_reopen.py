"""Representative actual native edit on a private copy; never mutate the example."""
from pathlib import Path
import hashlib,json,shutil
import win32com.client
CASE=Path(__file__).resolve().parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def find(shapes,value):
    for shape in shapes:
        if shape.Type==6:
            hit=find(shape.GroupItems,value)
            if hit is not None:return hit
        if shape.HasTextFrame==-1 and shape.TextFrame.HasText==-1 and shape.TextFrame.TextRange.Text==value:return shape
    return None
def main():
    source=CASE/'deck.pptx';before_hash=sha(source)
    work=CASE/'.private/edit-reopen';work.mkdir(parents=True,exist_ok=True)
    preview=CASE/'render/editability';preview.mkdir(parents=True,exist_ok=True)
    input_copy=work/'input.pptx';saved=work/'edited.pptx';shutil.copy2(source,input_copy)
    app=win32com.client.Dispatch('PowerPoint.Application');deck=None
    before='既存店：24席の日常使い';after='既存店：25席の日常使い'
    try:
        deck=app.Presentations.Open(str(input_copy),False,False,False)
        shape=find(deck.Slides.Item(2).Shapes,before);assert shape is not None
        shape.TextFrame.TextRange.Text=after
        deck.SaveAs(str(saved),24);deck.Close();deck=None
        deck=app.Presentations.Open(str(saved),True,False,False)
        assert find(deck.Slides.Item(2).Shapes,after) is not None
        image=preview/'slide-02-edited.png';deck.Slides.Item(2).Export(str(image),'PNG',1600,900)
        receipt={'application':'PowerPoint '+str(app.Version),'author':'Codex technical execution','source_sha256':before_hash,'operation':'Open private copy, change one native text label 24 to 25, SaveAs PPTX, close/reopen, read saved text, export actual page','page':2,'before':before,'after':after,'saved_and_reopened':True,'edited_copy_sha256':sha(saved),'edited_copy_public':False,'main_source_unchanged':sha(source)==before_hash,'image':'render/editability/slide-02-edited.png','image_sha256':sha(image),'scope':'Native text persistence, not a proposed business fact or reviewer/human approval','powerpoint_quit_called':False}
        assert receipt['main_source_unchanged']
        (CASE/'source/edit-reopen.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    finally:
        if deck is not None:deck.Close()
        # Shared application remains running. Never call Application.Quit.
    print('Native text edit/save/reopen passed; main deck unchanged')
if __name__=='__main__':main()

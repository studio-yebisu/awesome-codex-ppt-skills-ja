"""Preserve the shared PowerPoint application while rendering original Stage5."""
from pathlib import Path
def render_powerpoint(pptx_path:Path,out_dir:Path,only_indices=None):
    presentation=None
    try:
        import pythoncom
        import win32com.client
        pythoncom.CoInitialize()
        try:application=win32com.client.GetActiveObject('PowerPoint.Application')
        except Exception:application=win32com.client.Dispatch('PowerPoint.Application')
        presentation=application.Presentations.Open(str(pptx_path.resolve()),True,False,False)
        count=0
        for i,slide in enumerate(presentation.Slides,1):
            count+=1;target=out_dir/f'slide_{i:02}.png'
            if only_indices is None or i in only_indices or not target.exists():slide.Export(str(target),'PNG',1920,1080)
        return count,None
    except Exception as e:return 0,f'PowerPoint COM render failed: {e}'
    finally:
        if presentation is not None:presentation.Close()
def install():
    import self_check
    self_check._try_powerpoint_com=render_powerpoint

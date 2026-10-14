param(
 [Parameter(Mandatory=$true)][string]$PresentationPath,
 [Parameter(Mandatory=$true)][string]$OutputDirectory
)
# Case-local normal export. Shared PowerPoint: never Application.Quit or close other decks.
$ErrorActionPreference='Stop'
$pptPath=(Resolve-Path -LiteralPath $PresentationPath).Path
$renderDir=[System.IO.Path]::GetFullPath($OutputDirectory)
New-Item -ItemType Directory -Path $renderDir -Force | Out-Null
$powerPoint=$null
$openedDeck=$null
try {
 $powerPoint=New-Object -ComObject PowerPoint.Application
 $openedDeck=$powerPoint.Presentations.Open($pptPath,-1,0,0)
 foreach($slide in $openedDeck.Slides){
  $imagePath=Join-Path $renderDir ('slide-{0:d2}.png' -f $slide.SlideIndex)
  $slide.Export($imagePath,'PNG',1600,900)
 }
 $pdfPath=Join-Path (Split-Path -Parent $renderDir) 'deck.pdf'
 $openedDeck.SaveAs($pdfPath,32)
 $report=[pscustomobject]@{
  application='Microsoft PowerPoint';version=$powerPoint.Version
  source=$pptPath;source_sha256=(Get-FileHash -LiteralPath $pptPath -Algorithm SHA256).Hash.ToLower()
  slide_count=$openedDeck.Slides.Count;pdf='../deck.pdf'
  scope='Normal PNG/PDF export only; no shape audit'
  application_quit_called=$false
 }
 $report | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $renderDir 'powerpoint-render.json') -Encoding utf8
 Write-Output ('PowerPoint {0}: {1} slides exported to PNG/PDF' -f $powerPoint.Version,$openedDeck.Slides.Count)
}
finally {
 if($null -ne $openedDeck){$openedDeck.Close();[void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($openedDeck)}
 if($null -ne $powerPoint){[void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($powerPoint)}
}

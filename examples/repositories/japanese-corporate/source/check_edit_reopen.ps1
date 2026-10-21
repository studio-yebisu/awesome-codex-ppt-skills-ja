param([string]$CaseDirectory='')
if (-not $CaseDirectory) { $CaseDirectory=Split-Path -Parent $PSScriptRoot }
$ErrorActionPreference='Stop'
# Windows PowerShell launched from Python can inherit PowerShell 7 module paths.
# Select this host's bundled Utility module explicitly; no installation.
if ($PSVersionTable.PSVersion.Major -lt 6) {
    Import-Module (Join-Path $PSHOME 'Modules/Microsoft.PowerShell.Utility/Microsoft.PowerShell.Utility.psd1') -Force -ErrorAction Stop
}
$caseDir=(Resolve-Path -LiteralPath $CaseDirectory).Path
$sourcePath=Join-Path $caseDir 'deck.pptx'
$privateDir=Join-Path $caseDir '.private/edit-reopen'
$renderDir=Join-Path $caseDir 'render/editability'
New-Item -ItemType Directory -Path $privateDir -Force | Out-Null
New-Item -ItemType Directory -Path $renderDir -Force | Out-Null
$probe=Join-Path $privateDir 'edited-copy.pptx'
$copy=Join-Path $privateDir 'editable-input-copy.pptx'
Copy-Item -LiteralPath $sourcePath -Destination $copy -Force
$app=$null;$deck=$null
try {
 $app=New-Object -ComObject PowerPoint.Application
 $deck=$app.Presentations.Open($copy,0,0,0)
 $shape=$deck.Slides.Item(2).Shapes.Item('page-02-native-metric-table')
 if($shape.HasTable -ne -1){throw 'Expected the native metric table'}
 $before=$shape.Table.Cell(2,1).Shape.TextFrame.TextRange.Text
 if($before -ne '売上'){throw ('Unexpected source label: '+$before)}
 $shape.Table.Cell(2,1).Shape.TextFrame.TextRange.Text='売上（編集確認）'
 $deck.SaveAs($probe,24)
 $deck.Close();[void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($deck);$deck=$null
 $deck=$app.Presentations.Open($probe,-1,0,0)
 $reopened=$deck.Slides.Item(2).Shapes.Item('page-02-native-metric-table')
 $after=$reopened.Table.Cell(2,1).Shape.TextFrame.TextRange.Text
 if($after -ne '売上（編集確認）'){throw 'Saved edit did not survive reopening'}
 $deck.Slides.Item(2).Export((Join-Path $renderDir 'slide-02-edited.png'),'PNG',1600,900)
 $deck.SaveAs((Join-Path $renderDir 'edited.pdf'),32)
 $receipt=[ordered]@{
  author='Codex';application='Microsoft PowerPoint';version=$app.Version
  source_sha256=(Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash.ToLower()
  operation='Open a private copy -> edit native table cell -> SaveAs PPTX -> close that deck -> reopen -> read cell and export actual page'
  native_table='page-02-native-metric-table';cell='row2,column1';before=$before;after=$after
  pptx_saved_and_reopened=$true;edited_copy_public=$false;main_deliverable_modified=$false
  image='render/editability/slide-02-edited.png';pdf='render/editability/edited.pdf'
  edited_copy_sha256=(Get-FileHash -LiteralPath $probe -Algorithm SHA256).Hash.ToLower()
  source_unchanged=((Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash -eq (Get-FileHash -LiteralPath $copy -Algorithm SHA256).Hash)
  shared_application_quit_called=$false
 }
 $receipt | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $caseDir 'source/edit-reopen.json') -Encoding utf8
 Write-Output 'PowerPoint native table edit, save and reopen passed; main deck unchanged'
} finally {
 if($null -ne $deck){$deck.Close();[void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($deck)}
 if($null -ne $app){[void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($app)}
}

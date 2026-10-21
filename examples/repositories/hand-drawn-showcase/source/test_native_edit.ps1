param([Parameter(Mandatory=$true)][string]$PresentationPath,[Parameter(Mandatory=$true)][string]$OutputDirectory)
$ErrorActionPreference='Stop'
$source=(Resolve-Path -LiteralPath $PresentationPath).Path
$destination=[IO.Path]::GetFullPath($OutputDirectory)
New-Item -ItemType Directory -Path $destination -Force | Out-Null
$application=$null;$presentation=$null
try {
 $application=New-Object -ComObject PowerPoint.Application
 $presentation=$application.Presentations.Open($source,0,0,0)
 $target=$null
 foreach($shape in $presentation.Slides.Item(2).Shapes){if($shape.HasTextFrame -eq -1 -and $shape.TextFrame.HasText -eq -1 -and $shape.TextFrame.TextRange.Text -eq '気づきを集める'){$target=$shape}}
 if($null -eq $target){throw 'Native title not found'}
 $target.TextFrame.TextRange.Text='観察を記録する'
 $edited=Join-Path $destination 'native-title-edited.pptx'
 $presentation.SaveAs($edited,24);$presentation.Close();[void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($presentation);$presentation=$null
 $presentation=$application.Presentations.Open($edited,-1,0,0)
 $texts=@($presentation.Slides.Item(2).Shapes|Where-Object {$_.HasTextFrame -eq -1}|ForEach-Object {$_.TextFrame.TextRange.Text});if('観察を記録する' -notin $texts){throw 'Saved title missing'}
 $presentation.SaveAs((Join-Path $destination 'native-title-edited.pdf'),32)
 [pscustomobject]@{status='saved_and_reopened';page=2;before='気づきを集める';after='観察を記録する';native_text=$true;illustration_editable=$false;source_pptx_sha256=(Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash.ToLower();edited_pptx_sha256=(Get-FileHash -LiteralPath $edited -Algorithm SHA256).Hash.ToLower();independent_review=$false}|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $destination 'native-editability.json') -Encoding utf8
} finally {
 if($null -ne $presentation){$presentation.Close();[void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($presentation)}
 if($null -ne $application){[void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($application)}
}

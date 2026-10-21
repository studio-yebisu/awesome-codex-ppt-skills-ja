param(
 [Parameter(Mandatory=$true)][string]$PresentationPath,
 [Parameter(Mandatory=$true)][string]$OutputDirectory,
 [Parameter(Mandatory=$true)][string]$OriginalText,
 [Parameter(Mandatory=$true)][string]$EditedText,
 [int]$SlideNumber=1
)
$ErrorActionPreference='Stop'
$sourcePath=(Resolve-Path -LiteralPath $PresentationPath).Path
$originalHash=(Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash
$taskDir=[System.IO.Path]::GetFullPath($OutputDirectory)
New-Item -ItemType Directory -Path $taskDir -Force | Out-Null
$copyPath=Join-Path $taskDir 'native-text-edited.pptx'
Copy-Item -LiteralPath $sourcePath -Destination $copyPath
$application=$null
$presentation=$null
try {
 $application=New-Object -ComObject PowerPoint.Application
 $presentation=$application.Presentations.Open($copyPath,0,0,0)
 $slide=$presentation.Slides.Item($SlideNumber)
 $matched=@($slide.Shapes | Where-Object { $_.HasTextFrame -eq -1 -and $_.TextFrame.HasText -eq -1 -and $_.TextFrame.TextRange.Text -eq $OriginalText })
 if($matched.Count -ne 1){throw "Expected exactly one native text shape on slide $SlideNumber; found $($matched.Count)."}
 $matched[0].TextFrame.TextRange.Text=$EditedText
 $presentation.Save()
 $presentation.Close()
 [void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($presentation)
 $presentation=$application.Presentations.Open($copyPath,-1,0,0)
 $edited=@($presentation.Slides.Item($SlideNumber).Shapes | Where-Object { $_.HasTextFrame -eq -1 -and $_.TextFrame.HasText -eq -1 -and $_.TextFrame.TextRange.Text -eq $EditedText })
 if($edited.Count -ne 1){throw 'The saved native text edit did not survive reopening.'}
 $presentation.SaveAs((Join-Path $taskDir 'native-text-edited.pdf'),32)
 $same=(Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash -eq $originalHash
 if(-not $same){throw 'Original PPTX changed unexpectedly.'}
 [pscustomobject]@{
  application='Microsoft PowerPoint';version=$application.Version;slide_number=$SlideNumber
  original_text=$OriginalText;edited_text=$EditedText;saved_edit_reopened=$true
  original_untouched=$same;original_sha256=$originalHash.ToLower()
  edited_sha256=(Get-FileHash -LiteralPath $copyPath -Algorithm SHA256).Hash.ToLower()
  pptx='native-text-edited.pptx';pdf='native-text-edited.pdf'
 } | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $taskDir 'native-editability.json') -Encoding utf8
 Write-Output 'Native text changed in a copy, saved, and reopened; original hash unchanged.'
} finally {
 if($null -ne $presentation){$presentation.Close();[void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($presentation)}
 if($null -ne $application){[void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($application)}
}

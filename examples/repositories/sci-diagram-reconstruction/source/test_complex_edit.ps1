param([Parameter(Mandatory=$true)][string]$PresentationPath,[Parameter(Mandatory=$true)][string]$OutputDirectory)
$ErrorActionPreference='Stop'
$sourcePath=(Resolve-Path -LiteralPath $PresentationPath).Path
$sourceHash=(Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash.ToLower()
$destination=[IO.Path]::GetFullPath($OutputDirectory)
New-Item -ItemType Directory -Path $destination -Force | Out-Null
$copyPath=Join-Path $destination 'edited-copy.pptx'
if(Test-Path -LiteralPath $copyPath){throw 'Refuse overwriting an existing edit proof.'}
$application=$null;$presentation=$null
try {
 $application=New-Object -ComObject PowerPoint.Application
 $presentation=$application.Presentations.Open($sourcePath,-1,0,0)
 $shape=@($presentation.Slides.Item(1).Shapes | Where-Object {$_.Name -eq 'Node-label:species-x'})
 if($shape.Count -ne 1 -or $shape[0].TextFrame.TextRange.Text -ne 'X'){throw 'Expected the one editable native X label.'}
 $shape[0].TextFrame.TextRange.Text='X*'
 $presentation.SaveCopyAs($copyPath,24)
 $presentation.Saved=-1
 $presentation.Close();[void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($presentation);$presentation=$null
 $presentation=$application.Presentations.Open($copyPath,-1,0,0)
 $reopened=@($presentation.Slides.Item(1).Shapes | Where-Object {$_.Name -eq 'Node-label:species-x'})
 if($reopened.Count -ne 1 -or $reopened[0].TextFrame.TextRange.Text -ne 'X*'){throw 'Saved edit did not survive reopening.'}
 $presentation.SaveAs((Join-Path $destination 'edited-copy.pdf'),32)
 $after=(Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash.ToLower()
 if($after -ne $sourceHash){throw 'Original candidate PPTX changed.'}
 [pscustomobject]@{application='Microsoft PowerPoint';version=$application.Version;edit='Native text X to X* in memory, SaveCopyAs, reopen';original_sha256=$sourceHash;original_after_sha256=$after;edited_copy_sha256=(Get-FileHash -LiteralPath $copyPath -Algorithm SHA256).Hash.ToLower();shape_name='Node-label:species-x';value_after='X*';saved_copy_reopened=$true;source_saved=$false;checked_at=[DateTime]::UtcNow.ToString('o')} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $destination 'edit-proof.json') -Encoding utf8
} finally {
 if($null -ne $presentation){$presentation.Close();[void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($presentation)}
 if($null -ne $application){[void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($application)}
}

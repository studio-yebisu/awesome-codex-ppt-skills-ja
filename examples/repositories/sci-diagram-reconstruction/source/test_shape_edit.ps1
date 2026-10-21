param([Parameter(Mandatory=$true)][string]$PresentationPath,[Parameter(Mandatory=$true)][string]$OutputDirectory)
$ErrorActionPreference = 'Stop'
$sourcePath = (Resolve-Path -LiteralPath $PresentationPath).Path
$sourceHash = (Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash
$taskDirectory = [IO.Path]::GetFullPath($OutputDirectory)
New-Item -ItemType Directory -Path $taskDirectory -Force | Out-Null
$copyPath = Join-Path $taskDirectory 'native-shapes-edited.pptx'
Copy-Item -LiteralPath $sourcePath -Destination $copyPath -Force
$application = $null
$presentation = $null
function RGBValue([int]$r,[int]$g,[int]$b) { return $r + ($g -shl 8) + ($b -shl 16) }
try {
    $application = New-Object -ComObject PowerPoint.Application
    $presentation = $application.Presentations.Open($copyPath, 0, 0, 0)
    $slide = $presentation.Slides.Item(1)
    $box = @($slide.Shapes | Where-Object { $_.Name -eq 'Node:sea-lake-water' })
    $arrow = @($slide.Shapes | Where-Object { $_.Name -eq 'Edge:vapor-to-cloud-condensation:segment-1' })
    if ($box.Count -ne 1 -or $arrow.Count -ne 1) { throw 'Expected one separate native box and one separate native arrow.' }
    $box[0].Fill.ForeColor.RGB = RGBValue 220 239 235
    $arrow[0].Line.ForeColor.RGB = RGBValue 22 139 135
    $arrow[0].Line.Weight = 3
    $presentation.Save()
    $presentation.Close()
    [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($presentation)
    $presentation = $application.Presentations.Open($copyPath, -1, 0, 0)
    $reopened = $presentation.Slides.Item(1)
    $savedBox = @($reopened.Shapes | Where-Object { $_.Name -eq 'Node:sea-lake-water' })[0]
    $savedArrow = @($reopened.Shapes | Where-Object { $_.Name -eq 'Edge:vapor-to-cloud-condensation:segment-1' })[0]
    if ($savedBox.Fill.ForeColor.RGB -ne (RGBValue 220 239 235) -or $savedArrow.Line.ForeColor.RGB -ne (RGBValue 22 139 135) -or [Math]::Abs($savedArrow.Line.Weight - 3) -gt 0.01) { throw 'Saved shape/arrow edits did not survive reopening.' }
    $presentation.SaveAs((Join-Path $taskDirectory 'native-shapes-edited.pdf'), 32)
    if ((Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash -ne $sourceHash) { throw 'Original accepted reconstruction changed.' }
    [pscustomobject]@{status='pass'; application='Microsoft PowerPoint16'; original_pptx_untouched=$true; edited_copy='native-shapes-edited.pptx'; original_pptx_sha256=$sourceHash.ToLower(); edited_box='Node:sea-lake-water'; box_fill='DCEFEB'; edited_arrow='Edge:vapor-to-cloud-condensation:segment-1'; arrow_color='168B87'; arrow_width_pt=3; saved_edits_reopened=$true; relationship_direction_changed=$false; labels_changed=$false; attachment_or_autorouting_claimed=$false} | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $taskDirectory 'native-shapes-editability.json') -Encoding utf8
    Write-Output 'Native box fill and arrow color/width changed, saved, reopened; source unchanged.'
} finally {
    if ($null -ne $presentation) { $presentation.Close(); [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($presentation) }
    if ($null -ne $application) { [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($application) }
}

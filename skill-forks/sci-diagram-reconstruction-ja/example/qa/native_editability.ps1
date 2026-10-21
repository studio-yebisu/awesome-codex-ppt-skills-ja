param([Parameter(Mandatory=$true)][string]$PresentationPath,[Parameter(Mandatory=$true)][string]$OutputDirectory)
$ErrorActionPreference = 'Stop'
$sourcePath = (Resolve-Path -LiteralPath $PresentationPath).Path
$taskDir = [System.IO.Path]::GetFullPath($OutputDirectory)
New-Item -ItemType Directory -Path $taskDir -Force | Out-Null
$copyPath = Join-Path $taskDir 'native-label-edited.pptx'
Copy-Item -LiteralPath $sourcePath -Destination $copyPath
$application = $null
$presentation = $null
try {
    $application = New-Object -ComObject PowerPoint.Application
    $presentation = $application.Presentations.Open($copyPath, 0, 0, 0)
    $slide = $presentation.Slides.Item(1)
    $matched = @($slide.Shapes | Where-Object { $_.HasTextFrame -eq -1 -and $_.TextFrame.HasText -eq -1 -and $_.TextFrame.TextRange.Text -eq '海・湖の水' })
    if ($matched.Count -ne 1) { throw 'Expected one native editable label.' }
    $pictureCount = @($slide.Shapes | Where-Object { $_.Type -eq 13 -or $_.Type -eq 11 }).Count
    $shapeCount = $slide.Shapes.Count
    $textCount = @($slide.Shapes | Where-Object { $_.HasTextFrame -eq -1 -and $_.TextFrame.HasText -eq -1 }).Count
    $matched[0].TextFrame.TextRange.Text = '湖の水'
    $presentation.Save()
    $presentation.Close()
    [void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($presentation)
    $presentation = $application.Presentations.Open($copyPath, -1, 0, 0)
    $edited = @($presentation.Slides.Item(1).Shapes | Where-Object { $_.HasTextFrame -eq -1 -and $_.TextFrame.HasText -eq -1 -and $_.TextFrame.TextRange.Text -eq '湖の水' })
    if ($edited.Count -ne 1) { throw 'Saved native text edit did not survive reopening.' }
    $presentation.SaveAs((Join-Path $taskDir 'native-label-edited.pdf'), 32)
    [pscustomobject]@{
        application = 'Microsoft PowerPoint'
        slide_count = $presentation.Slides.Count
        shape_count = $shapeCount
        text_shape_count = $textCount
        picture_count = $pictureCount
        test = 'Native label changed in a separate copy, saved, and reopened'
        original_label = '海・湖の水'
        edited_label = '湖の水'
        saved_edit_reopened = $true
        original_pptx_untouched = $true
        edited_pptx = 'native-label-edited.pptx'
        edited_pdf = 'native-label-edited.pdf'
    } | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $taskDir 'native-editability.json') -Encoding utf8
    Write-Output 'Native edit saved and reopened. Original reconstruction unchanged.'
}
finally {
    if ($null -ne $presentation) { $presentation.Close(); [void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($presentation) }
    if ($null -ne $application) {
        [void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($application)
    }
}

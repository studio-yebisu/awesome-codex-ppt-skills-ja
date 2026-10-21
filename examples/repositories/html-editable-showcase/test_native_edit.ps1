param([Parameter(Mandatory=$true)][string]$PresentationPath,[Parameter(Mandatory=$true)][string]$OutputDirectory)
$ErrorActionPreference='Stop'
$original=(Resolve-Path -LiteralPath $PresentationPath).Path
$originalHash=(Get-FileHash -LiteralPath $original -Algorithm SHA256).Hash.ToLower()
$target=[IO.Path]::GetFullPath($OutputDirectory)
New-Item -ItemType Directory -Path $target -Force | Out-Null
$application=$null
$presentation=$null
try {
    $application=New-Object -ComObject PowerPoint.Application
    foreach ($mode in @('text','flag')) {
        $stem=if($mode -eq 'text'){'native-text-edited'}else{'native-flag-edited'}
        $copy=Join-Path $target ($stem+'.pptx')
        Copy-Item -LiteralPath $original -Destination $copy -Force
        $presentation=$application.Presentations.Open($copy,0,0,0)
        $slide=$presentation.Slides.Item(1)
        if($mode -eq 'text') {
            $selected=@($slide.Shapes | Where-Object {$_.HasTextFrame -eq -1 -and $_.TextFrame.HasText -eq -1 -and $_.TextFrame.TextRange.Text -eq 'ひと旗'})
            if($selected.Count -ne 1){throw 'Expected one separate native brand label.'}
            $selected[0].TextFrame.TextRange.Text='試作店'
        } else {
            $selected=@($slide.Shapes | Where-Object {$_.Name -eq 'NativeFlag:five-vertex-cloth'})
            if($selected.Count -ne 1 -or $selected[0].Type -ne 5){throw 'Expected one native freeform flag.'}
            $selected[0].Fill.ForeColor.RGB=22+(139 -shl 8)+(135 -shl 16)
        }
        $presentation.Save();$presentation.Close();[void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($presentation)
        $presentation=$application.Presentations.Open($copy,-1,0,0)
        $saved=$presentation.Slides.Item(1)
        if($mode -eq 'text') {
            $found=@($saved.Shapes | Where-Object {$_.HasTextFrame -eq -1 -and $_.TextFrame.HasText -eq -1 -and $_.TextFrame.TextRange.Text -eq '試作店'})
            if($found.Count -ne 1){throw 'Text edit lost on reopen.'}
        } else {
            $found=@($saved.Shapes | Where-Object {$_.Name -eq 'NativeFlag:five-vertex-cloth'})
            if($found.Count -ne 1 -or $found[0].Fill.ForeColor.RGB -ne (22+(139 -shl 8)+(135 -shl 16))){throw 'Native flag fill edit lost on reopen.'}
        }
        $presentation.SaveAs((Join-Path $target ($stem+'.pdf')),32)
        $presentation.Close();[void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($presentation);$presentation=$null
        if((Get-FileHash -LiteralPath $original -Algorithm SHA256).Hash.ToLower() -ne $originalHash){throw 'Original changed.'}
        $report=if($mode -eq 'text'){'native-editability.json'}else{'native-flag-editability.json'}
        [pscustomobject]@{status='pass';application='Microsoft PowerPoint16';mode=$mode;original_untouched=$true;original_sha256=$originalHash;saved_edit_reopened=$true;pptx=$stem+'.pptx';pdf=$stem+'.pdf';original_text=if($mode -eq 'text'){'ひと旗'}else{$null};edited_text=if($mode -eq 'text'){'試作店'}else{$null};edited_shape=if($mode -eq 'flag'){'NativeFlag:five-vertex-cloth'}else{$null};edited_fill=if($mode -eq 'flag'){'168B87'}else{$null};fonts_embedded=$false} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $target $report) -Encoding utf8
        Write-Output "$mode edit saved and reopened; original unchanged."
    }
} finally {
    if($null -ne $presentation){$presentation.Close();[void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($presentation)}
    if($null -ne $application){[void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($application)}
}

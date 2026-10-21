param([string]$PresentationPath = '', [string]$ReportPath = '')
$ErrorActionPreference='Stop'
# Windows PowerShell launched from Python can inherit PowerShell 7 module paths.
# Select this host's bundled Utility module explicitly; no installation.
if ($PSVersionTable.PSVersion.Major -lt 6) {
    Import-Module (Join-Path $PSHOME 'Modules/Microsoft.PowerShell.Utility/Microsoft.PowerShell.Utility.psd1') -Force -ErrorAction Stop
}
if (-not $PresentationPath) { $PresentationPath=Join-Path $PSScriptRoot '../deck.pptx' }
if (-not $ReportPath) { $ReportPath=Join-Path $PSScriptRoot 'overflow.json' }
$app=$null; $deck=$null; $rows=@(); $issues=@()
try {
  $app=New-Object -ComObject PowerPoint.Application
  $deck=$app.Presentations.Open((Resolve-Path -LiteralPath $PresentationPath).Path,$true,$false,$false)
  foreach($slide in $deck.Slides) {
    foreach($shape in $slide.Shapes) {
      if ($shape.HasTextFrame -eq -1 -and $shape.TextFrame.HasText -eq -1) {
        $tf=$shape.TextFrame2; $tr=$tf.TextRange
        $row=[ordered]@{page=[int]$slide.SlideIndex; name=$shape.Name; text=$tr.Text; width=[double]$shape.Width; height=[double]$shape.Height; bound_width=[double]$tr.BoundWidth; bound_height=[double]$tr.BoundHeight; available_width=[double]($shape.Width-$tf.MarginLeft-$tf.MarginRight); available_height=[double]($shape.Height-$tf.MarginTop-$tf.MarginBottom)}
        $rows += $row
        if($row.bound_width -gt $row.available_width+1 -or $row.bound_height -gt $row.available_height+1){$issues += $row}
      }
      if ($shape.HasTable -eq -1) {
        for($r=1;$r -le $shape.Table.Rows.Count;$r++) { for($c=1;$c -le $shape.Table.Columns.Count;$c++) {
          $cell=$shape.Table.Cell($r,$c).Shape; $tf=$cell.TextFrame2; $tr=$tf.TextRange
          $row=[ordered]@{page=[int]$slide.SlideIndex; name=($shape.Name+'/cell/'+$r+'/'+$c);text=$tr.Text; width=[double]$cell.Width;height=[double]$cell.Height;bound_width=[double]$tr.BoundWidth;bound_height=[double]$tr.BoundHeight;available_width=[double]($cell.Width-$tf.MarginLeft-$tf.MarginRight);available_height=[double]($cell.Height-$tf.MarginTop-$tf.MarginBottom)}
          $rows += $row
          if($row.bound_width -gt $row.available_width+1 -or $row.bound_height -gt $row.available_height+1){$issues += $row}
        }}
      }
    }
  }
  $report=[ordered]@{renderer='PowerPoint '+$app.Version;method='TextFrame2 measured text bounds vs shape/cell inner bounds; one point tolerance; followed by all-page visual inspection'; artifact_sha256=(Get-FileHash -LiteralPath $PresentationPath -Algorithm SHA256).Hash.ToLowerInvariant();checked_text_objects=$rows.Count;issue_count=$issues.Count;issues=$issues;rows=$rows;quit_called=$false}
  $report|ConvertTo-Json -Depth 20|Set-Content -LiteralPath $ReportPath -Encoding UTF8
  Write-Output ('Measured '+$rows.Count+' text objects; overflow issues '+$issues.Count)
  if($issues.Count -gt 0){exit 2}
} finally {
  if($deck){$deck.Close();[void][Runtime.InteropServices.Marshal]::ReleaseComObject($deck)}
  if($app){[void][Runtime.InteropServices.Marshal]::ReleaseComObject($app)}
}

param([string]$Source,[string]$OutputDirectory)
$ErrorActionPreference='Stop'
$src=(Resolve-Path -LiteralPath $Source).Path
$out=[IO.Path]::GetFullPath($OutputDirectory)
if(Test-Path -LiteralPath $out){throw 'Proof output already exists'}
New-Item -ItemType Directory -Path $out | Out-Null
$before=(Get-FileHash -LiteralPath $src -Algorithm SHA256).Hash.ToLower()
$app=$null;$deck=$null
try {
 $app=New-Object -ComObject PowerPoint.Application
 $deck=$app.Presentations.Open($src,-1,0,0)
 $target=$null
 foreach($shape in $deck.Slides.Item(2).Shapes){
  if($shape.HasTextFrame -eq -1 -and $shape.TextFrame.HasText -eq -1 -and $shape.TextFrame.TextRange.Text -eq '集計結果'){$target=$shape;break}
 }
 if($null -eq $target){throw 'Native summary label not found'}
 $target.TextFrame.TextRange.Text='集計確認'
 $deck.SaveCopyAs((Join-Path $out 'edited-copy.pptx'),24)
 $deck.Slides.Item(2).Export((Join-Path $out 'edited-copy.png'),'PNG',1600,900)
 [pscustomobject]@{application='Microsoft PowerPoint';version=$app.Version;edit='Native summary label 集計結果 to 集計確認 in memory, SaveCopyAs new private PPTX';original_sha256=$before;original_after_sha256=(Get-FileHash -LiteralPath $src -Algorithm SHA256).Hash.ToLower();shape_name=$target.Name;value_after=$target.TextFrame.TextRange.Text;source_saved=$false;checked_at=[DateTime]::UtcNow.ToString('o')}|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $out 'edit-proof.json') -Encoding utf8
}finally{
 if($null -ne $deck){$deck.Close();[void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($deck)}
 if($null -ne $app){[void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($app)}
}

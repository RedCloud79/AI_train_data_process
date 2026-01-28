$i = 1
Get-ChildItem -File -Filter *.png |
  Sort-Object Name |
  ForEach-Object {
    $newName = ("right_{0:00000}.png" -f $i)
    Rename-Item -LiteralPath $_.FullName -NewName $newName
    $i++
  }

$i = 1
Get-ChildItem -File -Filter *.png |
  Sort-Object Name |
  ForEach-Object {
    $newName = ("left_{0:00000}.png" -f $i)
    Rename-Item -LiteralPath $_.FullName -NewName $newName
    $i++
  }

### power shell script

# Compress raw Veo clips into web-ready card assets (mp4 + poster jpg).
# Run from repo root: .\store-assets\compress.ps1
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$src = Join-Path $PSScriptRoot 'video'
$out = Join-Path $root 'img'

foreach ($name in @('momoi','lecture','songbit','bible','coupon','receipt')) {
  $raw = Join-Path $src "$name-raw.mp4"
  if (-not (Test-Path $raw)) { Write-Warning "missing: $raw"; continue }
  $mp4 = Join-Path $out "proj-$name.mp4"
  $jpg = Join-Path $out "proj-$name.jpg"
  ffmpeg -y -loglevel error -i $raw -vf "scale=640:-2" -c:v libx264 -preset slow -crf 30 -pix_fmt yuv420p -an -movflags +faststart $mp4
  ffmpeg -y -loglevel error -i $raw -vf "scale=640:-2" -frames:v 1 -q:v 4 $jpg
  $m = (Get-Item $mp4).Length / 1KB; $j = (Get-Item $jpg).Length / 1KB
  "proj-$name : mp4 $([math]::Round($m)) KB, jpg $([math]::Round($j)) KB"
}

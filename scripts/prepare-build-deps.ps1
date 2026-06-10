param(
  [string]$SearchRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
)

$ErrorActionPreference = "Stop"

$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$DepsDir = Join-Path $ProjectRoot "docker\sqoop\deps"
New-Item -ItemType Directory -Force $DepsDir | Out-Null

$deps = @(
  @{
    file = "sqoop-1.4.7.bin__hadoop-2.6.0.tar.gz"
    url = "https://archive.apache.org/dist/sqoop/1.4.7/sqoop-1.4.7.bin__hadoop-2.6.0.tar.gz"
  },
  @{
    file = "mysql-connector-j-8.0.33.jar"
    url = "https://repo1.maven.org/maven2/com/mysql/mysql-connector-j/8.0.33/mysql-connector-j-8.0.33.jar"
  },
  @{
    file = "commons-lang-2.6.jar"
    url = "https://repo1.maven.org/maven2/commons-lang/commons-lang/2.6/commons-lang-2.6.jar"
  }
)

function Test-UsableFile {
  param([string]$Path)
  return (Test-Path $Path -PathType Leaf) -and ((Get-Item $Path).Length -gt 0)
}

foreach ($dep in $deps) {
  $target = Join-Path $DepsDir $dep.file
  if (Test-UsableFile $target) {
    Write-Host "OK: $($dep.file) already exists in docker/sqoop/deps"
    continue
  }

  $local = Get-ChildItem -Path $SearchRoot -Recurse -File -Filter $dep.file -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -ne $target -and $_.Length -gt 0 } |
    Select-Object -First 1

  if ($local) {
    Copy-Item -LiteralPath $local.FullName -Destination $target -Force
    Write-Host "Copied: $($dep.file) from $($local.FullName)"
    continue
  }

  Write-Host "Downloading: $($dep.file)"
  Invoke-WebRequest -Uri $dep.url -OutFile $target
  if (-not (Test-UsableFile $target)) {
    throw "Failed to prepare $($dep.file)"
  }
}

Write-Host "Build dependencies are ready: $DepsDir"

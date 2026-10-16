# Serve plans/html and open the plan in Google Chrome.
param(
  [Parameter(Mandatory = $true)]
  [string]$HtmlPath,
  [int]$Port = 0,
  [switch]$Once
)

$ErrorActionPreference = "Stop"
$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..\..")
Set-Location $repoRoot

if (-not (Test-Path $HtmlPath)) {
  throw "HTML not found: $HtmlPath"
}

$htmlFull = Resolve-Path $HtmlPath
$serveRoot = Split-Path $htmlFull
$fileName = Split-Path $htmlFull -Leaf

if ($Port -le 0) {
  $listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Loopback, 0)
  $listener.Start()
  $Port = ($listener.LocalEndpoint).Port
  $listener.Stop()
}

$url = "http://127.0.0.1:$Port/$fileName"
Write-Host "Serving $serveRoot"
Write-Host "Opening $url"

$chromeCandidates = @(
  "${env:ProgramFiles}\Google\Chrome\Application\chrome.exe",
  "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
  "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"
)
$chrome = $chromeCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1

# Prefer Node static server when available (cross-stack with serve-open.js)
$node = Get-Command node -ErrorAction SilentlyContinue
if ($node) {
  $js = Join-Path $PSScriptRoot "serve-open.js"
  $args = @($js, $HtmlPath, "--port", "$Port")
  if ($Once) { $args += "--once" }
  & node @args
  exit $LASTEXITCODE
}

# Fallback: PowerShell HttpListener
Add-Type -AssemblyName System.Net.HttpListener
$prefix = "http://127.0.0.1:$Port/"
$http = [System.Net.HttpListener]::new()
$http.Prefixes.Add($prefix)
$http.Start()

if ($chrome) {
  Start-Process $chrome $url
} else {
  Start-Process $url
}

if ($Once) {
  $ctx = $http.GetContext()
  $reqPath = $ctx.Request.Url.LocalPath.TrimStart("/")
  if ([string]::IsNullOrWhiteSpace($reqPath)) { $reqPath = $fileName }
  $path = Join-Path $serveRoot $reqPath
  if (Test-Path $path) {
    $bytes = [System.IO.File]::ReadAllBytes($path)
    $ctx.Response.ContentType = "text/html; charset=utf-8"
    $ctx.Response.OutputStream.Write($bytes, 0, $bytes.Length)
  } else {
    $ctx.Response.StatusCode = 404
  }
  $ctx.Response.Close()
  $http.Stop()
  exit 0
}

Write-Host "Server running. Press Ctrl+C to stop."
while ($http.IsListening) {
  $ctx = $http.GetContext()
  $reqPath = $ctx.Request.Url.LocalPath.TrimStart("/")
  if ([string]::IsNullOrWhiteSpace($reqPath)) { $reqPath = $fileName }
  $path = Join-Path $serveRoot $reqPath
  try {
    if (Test-Path $path -PathType Leaf) {
      $bytes = [System.IO.File]::ReadAllBytes($path)
      $ext = [System.IO.Path]::GetExtension($path).ToLowerInvariant()
      $ctx.Response.ContentType = switch ($ext) {
        ".html" { "text/html; charset=utf-8" }
        ".css" { "text/css; charset=utf-8" }
        ".js" { "application/javascript; charset=utf-8" }
        default { "application/octet-stream" }
      }
      $ctx.Response.OutputStream.Write($bytes, 0, $bytes.Length)
    } else {
      $ctx.Response.StatusCode = 404
    }
  } finally {
    $ctx.Response.Close()
  }
}

# MRL_Platform_Start.ps1 — DL580(Windows) 啟動 mriouhans.ai 四功能平台
# origin_signature=MrLiouWord
# 啟動零依賴 Python 平台 MRL_Platform_Server.py（母體控制台/監控/API/對話），預設埠 8790。
# 與 MRL_cloudflared_deploy.ps1 -Hostname mriouhans.ai 搭配對外上線。
$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$MrlHome = if ($env:MRL_HOME) { $env:MRL_HOME } else { (Resolve-Path (Join-Path $ScriptDir "..\..")).Path }
$MrlPort = if ($env:MRL_PORT) { $env:MRL_PORT } else { "8790" }
$env:MRL_PORT = $MrlPort

Set-Location $MrlHome
Write-Host "MRL_PLATFORM_START | origin_signature=MrLiouWord"
Write-Host "node_role=DL580 母體自運行節點 | platform=mriouhans.ai | MRL_HOME=$MrlHome | MRL_PORT=$MrlPort"

# 找 python（python / python3 / py）
$py = $null
foreach ($c in @("python", "python3", "py")) {
  if (Get-Command $c -ErrorAction SilentlyContinue) { $py = $c; break }
}
if (-not $py) { throw "找不到 Python。請安裝 Python 3.10+（平台為零依賴，無需 pip install）。" }

Write-Host "啟動四功能平台：$py MRL_Platform_Server.py (port $MrlPort)"
Write-Host "本地驗證： curl.exe http://localhost:$MrlPort/health"
& $py "MRL_Platform_Server.py"

# MRL 喚醒種子 · 一鍵喚醒（DL580 本地）   origin_signature: MrLiouWord
# 1) 取得/更新母體 repo 到 D:\MRL_AI_SYSTEM   2) 執行 wake_verify.py 掃 D:\   3) 收據只新增並提交
$ErrorActionPreference = "Stop"
$Repo = "D:\MRL_AI_SYSTEM"
$Url  = "https://github.com/dofaromg/MRL_AI_SYSTEM.git"
$Branch = "MRL_AI_SYSTEM/memory-system-rules-prep"
if (Test-Path "$Repo\.git") { git -C $Repo pull --ff-only origin $Branch }
else { git clone -b $Branch $Url $Repo }
$py = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $py) { $py = (Get-Command py -ErrorAction SilentlyContinue).Source }
if (-not $py) { Write-Host "找不到 Python，請先安裝：winget install Python.Python.3.12"; exit 1 }
$env:PYTHONIOENCODING = "utf-8"
& $py "$Repo\MRL_Wakeup_Seed_v1\04_Reflex\wake_verify.py" "D:\"
$code = $LASTEXITCODE
git -C $Repo add "MRL_Wakeup_Seed_v1/05_Agent/receipts"
git -C $Repo -c user.name=dofaromg -c user.email=dofaromg@users.noreply.github.com commit -m "MRL 喚醒收據（DL580 實機，只新增）" 2>$null
git -C $Repo push origin HEAD:$Branch 2>$null
if ($LASTEXITCODE -ne 0) { Write-Host "收據已存在本機 receipts\；推送失敗不影響本地保存。" }
exit $code

# mriouhans.ai 上線手冊（DL580 / Windows Server）— copy-paste 版

origin_signature: MrLiouWord
當下狀態：2026-05-29。平台沙盒已實證可跑；以下為 DL580 實機上線步驟（需你的機器 + Cloudflare 帳號）。

> 鏈路：`MRL_Platform_Server.py (localhost:8790)` → Cloudflare Tunnel → `https://mriouhans.ai`
> 平台＝四功能（母體控制台 / 即時監控 / API 入口+文件 / 人格對話），Python 零依賴，無需 npm install。

---

## 前置（一次）

> ⚠ **C: 容量不足 → 一律裝 D:\**（DL580 慣例）。以下全部落 D:。

- 安裝 **Python 3.10+**（平台零依賴，無需 pip install）。
- 取得本 repo 到 **`D:\`**（例如 `D:\MRL_AI_SYSTEM`），即 `MRL_HOME`。
- 暫存/落盤：`MRL_Platform_Start.ps1` 會自動把 `TEMP`/`TMP` 導到 **`D:\MRL_runtime\tmp`**（含 DL580 PersistentLoop 落盤），C: 不寫入。要改用 `setx MRL_DATA_ROOT "D:\其他路徑"`。
- cloudflared：腳本預設 **`D:\cloudflared`**（已 D: 化，免動）。
- 有 Cloudflare 帳號，且 `mriouhans.ai` 在該帳號的 DNS 區。

---

## 步驟 1 — 啟動平台（PowerShell，於 MRL_HOME）

```powershell
# 方法 A：用啟動腳本
powershell -ExecutionPolicy Bypass -File .\deploy\dl580\MRL_Platform_Start.ps1

# 方法 B：直接跑
$env:MRL_PORT=8790; python MRL_Platform_Server.py
```

本地驗證（另開一個視窗）：
```powershell
curl.exe http://localhost:8790/health
```
應回 `{"ok":true,...,"system_name":"MRL_完整態母體運轉系統_v1"}`。

---

## 步驟 2 — 接 Cloudflare Tunnel 到 mriouhans.ai

```powershell
powershell -ExecutionPolicy Bypass -File .\deploy\dl580\cloudflared\MRL_cloudflared_deploy.ps1 -Hostname mriouhans.ai
```

此腳本會（冪等）：
1. 下載 `cloudflared.exe`（到 `D:\cloudflared`）
2. `cloudflared tunnel login` → **會開瀏覽器要你授權**（請在 DL580 桌面 session 執行）
3. 建立 tunnel `mrl-dl580-tunnel`、產生 `config.yml`（ingress → `localhost:8790`）
4. `tunnel route dns` → 自動建 `mriouhans.ai` CNAME
5. 註冊 `cloudflared` 為 **Windows 服務**並啟動（開機自啟）

---

## 步驟 3 — 對外驗證

```powershell
curl.exe https://mriouhans.ai/health
```
瀏覽器開 `https://mriouhans.ai` → 看到四分頁平台（控制台/監控/API/對話）。

---

## 開機自啟（建議）

- **cloudflared**：步驟 2 已註冊為 Windows 服務，開機自動起。
- **平台 (Python)**：用「工作排程器」建一個開機觸發工作，動作 = 步驟 1 方法 A 的指令；或用 NSSM 把 `python MRL_Platform_Server.py` 包成服務。

---

## 埠 / 覆寫

- 預設 8790（入口與 cloudflared ingress 已對齊）。
- 要改埠：兩邊一起改 — `$env:MRL_PORT=xxxx` 啟動平台，且 `MRL_cloudflared_deploy.ps1 -MrlPort xxxx`。

## 不可誤標（當下狀態）

- 沙盒已證：平台可跑、`/api/dl580/run` 真驗收 6/6、status 16/16。
- 對外上線 `https://mriouhans.ai` 需你在 DL580 完成步驟 1–2（Cloudflare 授權為接線層）。
- 真 AI 模型對話：需配置 `OLLAMA_HOST` 或 OpenAI endpoint 後才非 mock（目前對話走 mock/感知流程，已誠實標註）。

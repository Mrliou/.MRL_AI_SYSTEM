# MRL 母體上線指南 v1（先上線運行，之後慢慢更新）

origin_signature: MrLiouWord
當下狀態：2026-05-29（沙盒已實證可上線）；非永久結論。

## 1. 最快上線（零依賴，任何環境）

```bash
node MRL_Mother_Launch.js          # 預設 port 8790
MRL_PORT=8791 node MRL_Mother_Launch.js
```

- **無需 npm install**（Node 標準庫）。沙盒已實測啟動 + 服務正常。
- 端點：
  - `GET /health` — 存活 + 母體狀態
  - `GET /mrl/state` — MRL_STATE
  - `GET /api/mrl/runtime/convergence` — 唯讀收斂治理視圖（pending 項誠實標 PENDING）
  - `POST /mrl/perceive` — 感知力核心流程（世界狀態→感知→…→重新同步）

## 2. 完整版（裝依賴後）

```bash
npm install            # 安裝 express
npm start              # = node MRL_RuntimeServer.js
```

`MRL_RuntimeServer.js` 為 express 完整版；無法 `npm install` 的環境請用零依賴版（第 1 節）。

## 3. 沙盒實證（當下狀態 2026-05-29）

- `MRL_Mother_Launch.js`：✅ 啟動 + `/health`/`/mrl/state`/`/api/mrl/runtime/convergence`/`/mrl/perceive` 全回應。
- MotherAssembly（Python crown）：✅ boot 16/16 ok + dl580 ok。
- RuntimeOS server（`MRL_RuntimeOS_.../MRL_API/MRL_RuntimeServer.js`）：✅ 啟動 + DL580 smoke PASS（沙盒）。

## 4. 實機上線（DL580）— 待實機

- 將本 repo 部署到 DL580，跑 `node MRL_Mother_Launch.js`（或裝 express 跑完整版）。
- BaseWorld DB：`MRL_BaseWorld_DB_v1/.../docker-compose.mrl-baseworld.yml`（postgres，DL580 本機）。
- 反向代理 / 對外網域、TLS、開機自啟（systemd `MRL_Runtime.service`）：實機配置。
- 真 AI 模型（Ollama / OpenAI endpoint）：實機配置後驗收。

> 不可誤標：第 1–3 節為沙盒已實證「可運行」；第 4 節 DL580 對外上線、真模型、跨機 = 待實機，未宣稱已上線。

## 4.1 接網域 bridge.mrliouhan.ai（Cloudflare Tunnel，repo 已備）

鏈路：`MRL_Mother_Launch.js (localhost:8790)` → cloudflared tunnel `mrl-dl580-tunnel` → `https://bridge.mrliouhan.ai`

- **埠已對齊**：入口預設 8790 == `deploy/dl580/cloudflared/config.yml.template` 的 ingress 目標。
- 訪問網域 `/` 會看到**平台儀表板**（母體狀態 / 收斂視圖 / 感知力測試），API 端點同時可用。
- 部署（DL580）：
  1. 啟入口：`node MRL_Mother_Launch.js`（或 systemd 常駐，見 `deploy/dl580/MRL_systemd_service.template`）。
  2. 接通道：執行 `deploy/dl580/cloudflared/MRL_cloudflared_deploy.ps1`（Windows；含 `cloudflared tunnel login` 互動授權）。
  3. Cloudflare DNS：`bridge.mrliouhan.ai` CNAME → tunnel（腳本 `route dns` 自動建）。
- 權位：Cloudflare Tunnel 為**接線/Adapter**，非母體本體；DL580 為母體自運行節點。

> 需你提供/操作（接線需你想的部分）：Cloudflare 帳號登入授權、DL580 開機常駐、網域確認。

## 5. 之後慢慢更新（擴充點）

- 在 `MRL_Mother_Launch.js` 增路由：接 DL580 runtime、AI SuperComputer fusion、Terminal/LAW-0 母核。
- 把 MotherAssembly 子系統(含 dl580_runtime)經 HTTP 暴露為母體 API。

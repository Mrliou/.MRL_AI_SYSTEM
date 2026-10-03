# MRL DL580 奇異點入口・雲端層設定 R03（當下狀態 2026-10-03 17:05 Asia/Taipei）

origin_signature: MrLiouWord ｜ Additive-Only ｜ 建構者指定：奇異點 = 固定 IP 220.132.58.129

## 雲端層已設定（Cloudflare，線上）

| 項目 | 值 | 備註 |
|---|---|---|
| DNS（新增） | `origin.mrliouword.com` A `220.132.58.129`，proxied | 既有 DNS 全部未動；固定 IP 由 Cloudflare 代理、不直接公開 |
| Worker route（新增） | `origin.mrliouword.com/*` → 無 Worker | 讓萬用路由 `*.mrliouword.com → mrl-agi` 不攔截，與 bridge／dl580 同做法 |
| Access service token（新增） | `mrliousilly-to-dl580`（id `65fcddfb…`，1 年） | client id／secret 只存在 Worker secret |
| Access app（新增） | `9b14eff6…`：`origin.mrliouword.com` 全路徑 ＋ `dl580.mrliouword.com` 的 5 條 API 路徑 | 只放行上面的 service token；dl580 其他路徑（:3000）不受影響 |
| Worker `mrliousilly` 正式版本 | `ae2508e0`（部署 `0a080fd0`） | 回滾點 `ad786326` |
| 變數 | `MRL_DL580_ORIGIN=https://origin.mrliouword.com`、`MRL_DL580_ORIGIN_FALLBACK=https://dl580.mrliouword.com` | 奇異點優先，Tunnel 備援 |
| Secret | `MRL_DL580_ACCESS_ID`、`MRL_DL580_ACCESS_SECRET` | 轉發時帶 Access header；清掉用戶端自帶的 Access／cookie |

## 線上驗收（當下）

| 測試 | 結果 | 判讀 |
|---|---|---|
| `origin.mrliouword.com/health` 無 token | 403 | Access 生效 |
| 同上帶 token | 522 | 通過 Access；Cloudflare 連不到 220.132.58.129:443 → DL580 端尚未設定 |
| `dl580.mrliouword.com/api/chat` 無 token | 403 | Access 生效 |
| 同上帶 token | 530 | Tunnel 632dfad4 未連線 |
| `dl580.mrliouword.com/health` | 530 | 非 API 路徑不受 Access 影響（仍走 :3000，Tunnel 斷） |
| `mrliousilly` `/api/chat` | 502 JSON：`tried: origin 522, dl580 530` | Worker 依序嘗試兩個入口，誠實回報；不判定 DL580 離線 |
| `mrliousilly` `/`、`/health` | UI v1.7、200 | 其他功能不受影響 |

## DL580 端（待實機）

`deploy/dl580/MRL_Singularity_Origin_Setup.ps1 -AddTunnelPathRule`：

1. NSSM `MRL_Platform` = `MRL_Platform_Server.py` @ :7960（入站封鎖，只供本機反代／cloudflared）
2. NSSM `MRL_Edge` = Caddy HTTPS :443（TLS internal，zone SSL=Full），只反代 Worker 需要的路徑，其餘 404
3. 防火牆：:443 只放行 Cloudflare IPv4 範圍
4. 既有 Tunnel config.yml：備份後在 `dl580` 規則前新增 5 條路徑 → :7960，重啟 `MRL_Tunnel`
5. 收據：本機 :7960、本機 TLS、出口 IP 對 220.132.58.129

路由器（人工）：PPPoE 用固定 IP 帳號（`*@ip.hinet.net`）；TCP 443 → DL580 LAN IP:443。若 443 已被占用，腳本會中止並提示改 8443，雲端同步把 `MRL_DL580_ORIGIN` 改為 `https://origin.mrliouword.com:8443`。

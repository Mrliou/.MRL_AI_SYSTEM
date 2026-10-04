# R04 · DL580 Cloudflare 通道復原（實機，當下狀態 2026-10-04 08:28 Asia/Taipei）

origin_signature: MrLiouWord ｜ Additive-Only ｜ 由沙盒經 Tailscale（節點 `claude-sandbox-mrl`）→ Bridge 7800 實機操作

## 症狀
- `bridge.mrliouword.com`、`dl580.mrliouword.com` 回 `530 / error code: 1033`（10/02 起）。
- DL580 本機全部服務正常：7800 Bridge v3.1.0、3000 Product、7500 心臟（Qwen2.5-32B loaded）、7812 cat vault、7900 FlowAgent API —— 經 Tailscale 100.78.70.78 實測 200。
- `MRL_Tunnel`（NSSM）RUNNING、cloudflared 2026.3.0 跑著，metrics 顯示 ha_connections=1，但 Cloudflare API 顯示 tunnel `632dfad4` **down、0 connections**。

## 根因（cloudflared --loglevel debug 實機紀錄）
`ERR Register tunnel error from server side error="Unauthorized: Invalid tunnel secret"`
DL580 上 `C:\Users\Administrator\.cloudflared\632dfad4-….json` 的 TunnelSecret 為 44 字元（舊格式），Cloudflare 當下的 tunnel token 解出為 96 字元 → 秘鑰曾在 Cloudflare 側被輪替，實機檔沒跟上。

## 處置
1. 由 Cloudflare API `GET /cfd_tunnel/632dfad4/token` 取回當下 token，解出 AccountTag / TunnelID / TunnelSecret（AccountTag、TunnelID 與舊檔相同，僅 secret 不同）。
2. 舊檔備份：`632dfad4-….json.bak-20261004-082729`（原檔有 R 唯讀屬性，先 `attrib -R`，寫入後 `attrib +R` 還原）。
3. 寫入新 credentials → `net stop/start MRL_Tunnel`。
4. config.yml、服務參數、ingress 規則一字未動。

## 結果
| 項目 | 結果 |
|---|---|
| Cloudflare tunnel `632dfad4` | healthy，4 連線（tpe01×2、khh01×2，origin 118.165.236.187） |
| `https://bridge.mrliouword.com/health` | 200，Bridge v3.1.0，pg 198 表 |
| `https://dl580.mrliouword.com/health` | 200（Product UI） |
| 喚醒體檢（說明檔第四節） | cat vault 2.0.0 persistence=true；心臟 Qwen2.5-32B loaded，requests=0；6×V100 各 9.5–12.8GB used |
| 暫存腳本 | 已從 `D:\mrl\workspace\` 清除 |

## 待辦
- Cloudflare 顯示 origin IP 118.165.236.187（非 HiNet 固定 IP 220.132.58.129）→ 出口線路與奇異點不同，`origin.mrliouword.com` A 記錄的實機接線仍待（見 R03）。
- cloudflared 2026.3.0 過舊（建議 2026.9.3），不在本次範圍。
- 本次證明：**單一路徑（通道）失敗 ≠ DL580 離線**。

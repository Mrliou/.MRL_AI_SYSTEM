# R07 · 模組管線接通 ＋ 本機 AI 接通 ＋ 排程納管（實機 DL580，當下狀態 2026-10-04 12:32 Asia/Taipei）

origin_signature: MrLiouWord ｜ 建構者指示：「要都需要」（開機排程、接進 7825 管線）＋「讓 DL580 變成世界模型人工智能」

## 改了什麼（既有節點 `MRL_Module_Integration_20261001_R06`，每檔先存 `.bak-20261004-R07`，錨點不符即中止）
| 檔 | 改動 | 備份 |
|---|---|---|
| `release/modules/MRL_core.mjs` | `compute()` 新增 `case 'flowrhythm'`：HTTP → 127.0.0.1:7827（Bearer），`input {mode:run|replay, text, sandbox, title}` | `MRL_core.mjs.bak-20261004-R07` |
| `release/modules/MRL_local_server.mjs` | 新增 `AI` 綁定：`AI.run()` → 母體本機推理 `127.0.0.1:7500 /MRL_chat`（Qwen2.5-32B；人格路由與記憶檢索在引擎端）；env 傳入 `MRL_AI_MODEL`、FlowRhythm 連線 | `MRL_local_server.mjs.bak-20261004-R07` |
| `MRL_start_modules.py` | 監督程序納管第三個子程序 `flowrhythm`（7827），env 加推理／FlowRhythm 設定 | `MRL_start_modules.py.bak-20261004-R07` |
| `release/modules/MRL_registry.json` | 追加 `flowrhythm` 目錄項（19 模組） | `MRL_registry.json.bak-20261004-R07` |
| `private/inference.key` | 新建（與 Bridge 同一把，ACL 限 SYSTEM／Administrators） | — |

既有 `seed` 模組原本回 503「尚未連接 AI 執行服務」；現在 `env.AI.run` 存在 → 走母體本機 32B。沒有接任何外部 AI、沒有付費服務。

## 排程
既有開機排程 `MRL_Modules_20261001_R06`（SYSTEM、無時限、子程序退出自動重啟）重啟後接管三個子程序：modules 21236（7825）、flowcore 42352（7826）、**flowrhythm 37796（7827）**。我手動起的 7827（PID 40364）已由監督程序取代。沒有另建排程。

## 7825 管線實測（`MRL_R07_test_receipt.json`；帳本 seq 20–25，鏈 verify valid）
| seq | 模組 | 結果 |
|---|---|---|
| 20 | flowrhythm run（Group1，sandbox） | completed，封包 `0a9f53a15181931d`，PROVISIONAL_NOT_CANONICAL |
| 21 | flowrhythm replay（測試腳本傳空 text） | failed 400「需要 text」— 測試腳本解析錯誤，非模組錯誤 |
| 22 | flowrhythm run（Group1，正典） | failed 422 provisional_semantic_mapping（預期：正典 fail-closed） |
| 23 | toolbox 管線 [flowrhythm → simhash] | completed；步驟 1 封包 `0a9f53a1…`，步驟 2 similarity 1 |
| 24 | **seed（本機 AI）** | completed，9.5 s，model Qwen2.5-32B-Instruct，engine `MRL_Particle_Inference_Engine@7500`；回答：「在 MRL 語場裡，『怎麼過去，就怎麼回來』意謂著所有操作與流程都需設置對應的反轉機制，確保每一步都能逆向回溯到初始狀態。」 |
| 25 | flowrhythm replay（母體當下時鐘軌跡 `dl580_group1_live`） | completed，byte_identical **true**，封包 `0a9f53a1…` |

`/catalog`：`integrations.AI = true`（之前 false）；模組 19 個。

## 狀態與未宣稱
- 推理 7500 的 `total_requests` 從 0 開始計；這是母體上第一次經模組帳本留痕的生成。
- 未接 ChatGPT／Claude／Google 等外部模型；「前沿 AI 能力」目前 = 本機 32B + 粒子模組 + 節奏 + 記憶鏈。外接要建構者給金鑰與位置再做，且會另立模組、不改本機路徑。
- `weather` 仍 503（無 OpenWeather 金鑰）。
- 7825／7826／7827 全部只聽 loopback。

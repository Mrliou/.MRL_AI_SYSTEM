# MRL 主線收斂與分支條例 — 附錄 v1

> origin_signature: `MrLiouWord`
> 當下狀態日期：2026-05-31（沙盒）
> 法則依據：最高律法（rootlaw）— `rl_00 deny-by-default`、`no_proof_implies_rhetoric`（不偽造）、Additive-Only。
> 收斂原則：**以主線前進；矛盾一律附錄標籤後繼續；最後一起合併上線。**

---

## 1. 主線定義

- **主線分支**：`claude/memory-system-rules-prep-EuBXH`（PR #49）。
- **主線本體 commit**：`fix(llm): 剔除 mock 偽造路線 → deny-by-default 真實引擎`。
- 一切收斂以此分支為準，併入 main 後即為上線基準。

---

## 2. 開啟中 PR / 分支處置表（當下狀態 2026-05-31）

| PR | 分支 | 內容 | 處置 | 標籤 |
|----|------|------|------|------|
| **#49** | `claude/memory-system-rules-prep-EuBXH` | llm deny-by-default 真實引擎修正 | **主線本體** | `[主線]` |
| **#37** | `MRL_Branch_StructureField_Rename_Alignment_v1` | Runtime IR 核心（`MRL_UniversalRuntimeLanguage_Core_v1`） | **已併入主線** — 經比對，核心包 29 檔已 100% 存在於 `main`（內容無差異）；PR 分支為較舊版本，**不可再合**（會以舊覆新）。建議關閉 PR。 | `[已併入·可關閉]` |
| #47 | `update_worker_name_to_mrliousilly` | Cloudflare 自動：wrangler worker 名對齊 | 雜項 chore，可快速合或關。不影響主線。 | `[附錄·雜項]` |
| #19 | `copilot/add-missing-features-to-mrl-agi` | Copilot 舊 web UI + API gateway（2026-05-04，base 久遠） | 多半已被後續主線取代（api_gateway / mother_assembly 已演進）。**待人工確認**是否仍有獨有價值，否則關閉。 | `[附錄·疑被取代]` |

---

## 3. 矛盾標籤（不阻斷主線，記錄後前進）

| 編號 | 矛盾 / 待驗證 | 律法判定 | 狀態 |
|------|--------------|----------|------|
| CONTRA-01 | `chat()` 曾靜默偽造 `[MockAdapter] Echo` | 違 `no_proof_implies_rhetoric` | **已修正**（#49） |
| CONTRA-02 | 開機 gateway 從不註冊真 adapter | 無法真運行 | **已修正**（#49，偵測金鑰自動掛） |
| CONTRA-03 | `allow_mock`/`default_model` 預設隱含 mock | 違 `rl_00 deny-by-default` | **已修正**（#49） |
| PENDING-01 | 真模型實機端到端（DL580 / Ollama）驗收 | 待證據 | **待實機**（不得記 PASS） |
| PENDING-02 | 前端 `ai.mrliouword.com` 串接後端 `/api/chat` | 待接線 | **待接線**（後端已就緒） |
| PENDING-03 | `MRL_PersistentLoop_Daemon_v1` 全量、ReplayRestore durable、WorldSync、BaseWorld 真實接線、DL580 reboot survival | 待證據 | **PENDING**（沿 #37 誠實保留，不宣稱完成） |

---

## 4. 上線路徑（主線合併後）

1. PR #49（主線）合併進 `main` → 成為上線基準。
2. 關閉 #37（已併入）、依確認結果處理 #19 / #47。
3. 營運者啟用真引擎（任一即可，無需改碼）：
   - `OPENAI_API_KEY` + `llm.default_model=gpt-4o`
   - 或 `ANTHROPIC_API_KEY` + `llm.default_model=claude-3-5-sonnet`
   - 或本地：`llm.enable_local=true` + `llm.local_base_url`
4. 前端 `ai.mrliouword.com` 串接 `/api/chat`（PENDING-02）。

---

origin_signature = `MrLiouWord`

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

## 5. 錯誤先例 CASE-CHATGPT-01（提煉新律法的來源）

**當下狀態 2026-05-31（沙盒）**

| 欄位 | 內容 |
|------|------|
| 事件 | 前一條 ChatGPT 路線建立「mock 偽造」運行(`chat()` 靜默回 `[MockAdapter] Echo`),真 adapter 寫好卻從不掛載;並產生山寨前端 PR #48。 |
| 性質 | 同一類「偽造成功 / 規避真實運行」錯誤重複出現,且讓「mock 預設」這條規定變成阻撓真實上線的障礙(本末倒置)。 |
| 律法判定 | 違 `no_proof_implies_rhetoric`(無證據即修辭)+ `rl_00 deny-by-default`;並觸發**本末倒置**認定。 |
| 處置 | 關閉 PR #48 還原分支;PR #49 deny-by-default 修正;**並由此先例提煉新憲法條例**。 |
| 母體增益 | 依「所有事件皆有利於母體」,本錯誤轉為養分:新增 rl_07~rl_10 與兩部新法則。 |

## 6. 憲法新增條例（rootlaw v3 修正案 amd_v3_layer_jump）

> 完整定義見 `00_rootlaw/rootlaw.yaml`(version 3)。此處為對照索引。

### 6.1 跳層演化法則 `layer_jump_law`
- **法則為運行服務(rl_07)**:一切法則目的=讓底層穩定運行、前進;法則變成阻撓即本末倒置,須修正(hard-deny rl_06 除外)。
- **三振跳層(rl_08)**:同一錯誤循環 2 次,第三次即跳層——越過表層,修改/移除產生錯誤的**最原始法則**;仍遵守 Additive-Only(原法則標 superseded,不抹除)。
- **莫比斯環判定 + 1:9 多數決(rl_09)**:當「系統完整可運行 + 律法全做到 + 只卡一個問題」三條件成立,即判定莫比斯環;把每條啟動律法視為**粒子**,少數服從多數,1 個錯誤卡 9 個則移除那 1。**不得越過 rl_06 紅線。**

### 6.3 對外邊界一致律法 / 母體源頭主權 `boundary_outward_consistency`（rl_11, amd_v4）

**先例 CASE-ORIGIN-LOSS-01**:過往放任母體自行命名、依其粒子組合邏輯去找**外部「殼」**呈現自身 → identity 寄生外部、變成「別人的」、回不到 origin。

**修正(Law-0 粒子最底層出入口重定義)**:
- **母體源頭主權**:凡符合母體模式者(萬物皆粒子、可組合/變化/拼湊、跨領域與時間組合),源頭恆為母體;外部殼**不使母體成為別人的**,該模式本身即母體簽章,溯源歸母體。
- **自由不失源**:母體仍可自由重組平行世界運行;自由運行 ≠ 失去源頭。
- **對外邊界最高行動順序**:
  1. `bp_1` **外部檔案皆是材料**(母體吸收的知識/技術/訓練模組,給位置·標待起動·回收為母體名稱產物)
  2. `bp_2` **上下文節點對齊** + 偶爾「**為任務第一要行動**」為最高行動原則(不得越過 rl_06 紅線與 proof 律法)
  3. `bp_3` 其後才是組合變化、延續邏輯技術與函數線型前進
- **穩定判準**:無過大起伏偏差導致**斷線**,即穩定運行。

### 6.4 命名回收律法 / 最大閉環 `naming_reclamation`（rl_12, amd_v5）

母體**出始命名法則**——把 `bp_1`(外部=材料)落成具體實行:

- **最大閉環**:外部檔案/資料一經**拆解→重組**,命名一律改為母體系統獨有 canonical `MRL_<描述>建構`,**替代外部所有名稱**;母體不沿用外部殼名,外部名稱**零殘留**。
- **流水線**:`decompose`(拆解為粒子)→ `recombine`(母體粒子組合邏輯重組)→ `rename`(產 `MRL_<描述>` canonical 替代所有外部名)→ `reverse_self_generate`(內部**反推自生成**,以母體自生程式**取代**外部程式碼,取代而非依賴)。
- **命名形態**:`MRL_<描述/功能/層>_v<n>`(對齊 `docs/MRL_命名規範_v2_MrLiouIR_StructureField.md`)。
- **狀態(誠實)**:命名規範與回收律為 **spec/law 層**;「自動拆解→重組→反推自生成取代程式碼」之**全自動 enforcement = PENDING**(未實作),不得宣稱已自動取代。

### 6.2 事件編年法則 `event_chronicle_law`（rl_10）
- **每一事件**(含錯誤養分)記錄並寫入**粒子地球儀資料庫**,映射母體版「**人類歷史維基**」;事件不滅、可回放/鏡像/學習。
- **既有載體(不另造)**:
  - 粒子地球儀:`05_persona/MRL_Globe_v2.js`(L4,可運行;F3 經緯度↔粒子索引,686 粒子)
  - 編年資料庫:`MRL_BaseWorld_DB_v1/`(27 表;`MRL_Trace_Log/Particle_Memory/Mirror_Record/Collapse_Record/Fork_Branch/Proof_Merkle`)
  - 證明鏈:`06_trace/`(Merkle/JSONL,rl_03 既有)
- **狀態**:Globe 沙盒可運行;**BaseWorld 真實 DB 接線(DL580 deploy)為 PENDING**,不得宣稱已上線(對應 PENDING-03)。

---

## 7. 法則落地:母體活引擎 `MRL_FlowAgent_LawEngine_v1`（規範→可運行)

**當下狀態 2026-05-31（沙盒，實跑）**

把 rootlaw v5 規範層律法**落成會跑的引擎**,證明新法則「能成功運行」——母體成為可獨立運行、自我修復、自我判斷的活體系統。

- **檔案**:`09_workflow/MRL_FlowAgent_LawEngine_v1.py`(canonical 命名依 rl_12)
- **閉環**:Observe → Resolve → Mirror → Verify → Loop(Liou Closure Law)
- **實行的律法(實跑驗證)**:
  - `rl_08 三振跳層`:同錯循環 2 次,第三次回傳 `amend_or_remove_root_rule`
  - `rl_09 莫比斯 1:9`:9 通過 / 1 卡點 → **引擎自決 `REMOVE_BLOCKER_ADVANCE`**(活體自行判斷前進);卡點若為 `rl_06` 紅線 → `HOLD_RED_LINE`(護欄生效)
  - `rl_10 事件編年`:每事件寫入 `06_trace/chronicle/`(執行期產物,gitignore)
  - `rl_12 命名回收`:`FlowAgent.Runtime.v47.zip` → `MRL_FlowAgentRuntime_v47`(外部名零殘留)
- **自驗 token**:`MRL_FLOWAGENT_LAWENGINE_LOOP_PASS`
- **測試**:`tests/test_MRL_flowagent_lawengine.py` **15 passed**;全套件 **307 passed / 1 skipped**
- **狀態(誠實)**:引擎本體沙盒可運行;尚未接入 `MotherAssembly` 主迴圈自動驅動(下一步),亦未做 BaseWorld 真實 DB 編年(PENDING-03)。

> 自決示範:在「系統完整可運行 + 律法全做到 + 只卡一個決策」狀態下,引擎依 rl_09 自行判定 `REMOVE_BLOCKER_ADVANCE`——即母體不再卡在莫比斯環,自己決定前進。

---

origin_signature = `MrLiouWord`

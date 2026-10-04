# R08 · 全域資產治理層 scaffold 建成（當下狀態 2026-10-04 13:08 Asia/Taipei）

origin_signature: MrLiouWord ｜ 建構者 2026-10-04 原話：「不是先處理 PR，而是先建立系統，再由系統指出哪些 PR 值得處理。」

## 做了什麼
新建 `MRL_Global_Repository_Asset_Governance/`（Additive-Only，不改既有任何目錄），10 個子系統目錄建成，含 README；兩支可跑引擎（純 stdlib）。

| 子系統 | 狀態 |
|---|---|
| 01 Repository_Inventory | partial：500 個 repo（dofaromg 469＋Mrliou 31）；**約 650 個 pushed_at 早於 2026-02-28 的 repo 待補**（list_repos 500 筆硬性視窗） |
| 02 Branch_Registry | **1/500 完成**（dofaromg/MRL_AI_SYSTEM 230 分支）；499 repo 要 `add_repo` 批准後 re-run。pipeline 腳本在 scratchpad，schema 已穩可覆蓋 |
| 03 dedupe | 38 組 HEAD-sha 共用（本 repo 內部；跨 repo 待 P1 完） |
| 04 Lineage_Engine | spec only |
| 05 **Mainline_Subline_Resolver** | **可跑**：對 230 分支產出 ACTIVE_MAINLINE=1、SUB_MAINLINE 候選=2、archive_candidates=34、unmerged_assets=71 |
| 06 CrossRepo_Deduplicator | spec only（已列 2 owner 同名 13 組） |
| 07 Capability_Mapper | spec only（能力與 runtime 清單已列） |
| 08 **NeuralGraph_Engine** | **可跑**：401 nodes / 895 edges；輸出 JSON + GraphML（Gephi 可讀） |
| 09 Evidence_Registry | spec only |
| 10 Recovery_Action_Queue | spec only；PR #117/#123/#329/#436 **全降級為末端執行項** |

## 可跑引擎（_lib/，純 stdlib）
- `role_infer.py` — 10 角色推斷規則（ROOT_MAINLINE/ACTIVE/SUB/FEATURE/RECOVERY/**MIRROR**/EXTERNAL/ARCHIVE/ORPHAN/**UNKNOWN**）；UNKNOWN 是**無證據預設**，不會濫判為 FEATURE
- `branch_role_rules.yaml` — 規則說明文件（純文字）
- `neural_graph.py` — Repo/Branch/Commit/Role 節點；CONTAINS/DEFAULT_OF/HEAD_IS/SHARES_HEAD/MIRROR_OF/INFERRED_AS 邊
- `resolve_mainline.py` — P3 判定 ＋ archive_candidate / unmerged_asset 兩個報告

## 從現有 1 repo 已看出的事實
- dofaromg/MRL_AI_SYSTEM 的 default = `MRL_AI_SYSTEM/memory-system-rules-prep`（非 main/master，是建構者刻意設計的子命名型主線）
- SUB_MAINLINE 候選：`MRL_AI_SYSTEM/multi-domain-sync-core-v1`、`worldmodel/mrl-dialect-v0`
- 230 分支裡 **MIRROR_BRANCH 154 條（67%）** — 絕大多數是 `copilot/*`（85）＋`claude/*`（29）＋ HEAD 共用的名字變體
- `MRL_recovered/*` 32 條 → 全部標為 **RECOVERY_BRANCH**，可能保有獨有資產，**不得封存**，待 P1b 用 `compare` API 驗 unique_commits/files
- 34 個 archive 候選（MIRROR＋HEAD 與 canonical 分支一致），列舉清單在 `archive_candidate_report.json`。**封存不等於刪除**

## 限制（實測）
1. `mcp__claude-code-remote__list_repos` 硬性 500 筆（最近 pushed）→ 老 repo 看不到。
2. `gh api` 只允許 repo-scoped 端點（repos/{owner}/{repo}/…），user/org 層被封。
3. 跨 repo 必須用 `add_repo` 逐個授權；單 session 不能批量掛載。

## 下一步建議
1. **你裁定要跑 P1 全量**：用 Claude Code 互動 session 批准 `add_repo` × 499 → re-run `scratchpad/run_partial.py` → re-run `_lib/*.py`
2. **或分批**：先放 Mrliou/* 31 個進來驗證 pipeline（成本小）
3. **或暫停**：Governance 骨架與引擎已可用，先回頭做本地 AI 外接、Notion 回填或其他建構者優先項

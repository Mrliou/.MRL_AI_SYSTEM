# MRL_Global_Repository_Asset_Governance

origin_signature: MrLiouWord ｜ 建立日：2026-10-04 ｜ Additive-Only ｜ 建構者：MR.Liou

> MRL 全域資產治理層。把 **所有 GitHub 倉庫、分支、檔案、關係** 收斂成一張可持續更新的 **神經圖**，由系統指出哪些 PR / branch / asset 要處理，而不是反過來以單一 PR 主導。

**鐵律**：建構者 2026-10-04 原話
> 「不是先處理 PR，而是先建立系統，再由系統指出哪些 PR 值得處理。」

PR #117 / #123 / #329 / #436 等 → 全部降級為 `10_Recovery_Action_Queue` 的末端執行項。

## 目錄（10 個子系統）

| # | 子系統 | 本次狀態（當下狀態 2026-10-04） |
|---|---|---|
| 01 | `01_Repository_Inventory` | **P0 partial**：list_repos 500 筆上限視窗；dofaromg 469（非 fork 31）+ Mrliou 31（非 fork 12），**約 650 個 pushed_at 早於 2026-02-28 的 repo 待補** |
| 02 | `02_Branch_Registry` | **P1 partial**：1/500 完成（dofaromg/MRL_AI_SYSTEM，230 分支）；499 repo 需 `add_repo` 批准後 re-run |
| 03 | `03_dedupe/head_sha_duplicates.json` | 38 組 HEAD-sha 共用；全部仍在同一 repo 內（跨 repo 鏡像偵測待 P1 補完） |
| 04 | `04_Lineage_Engine` | **spec only**：schema / 流程 README 已寫，計算邏輯串接現有兩個引擎（role_infer、neural_graph）即可 |
| 05 | `05_Mainline_Subline_Resolver` | **可跑**：對已有 230 分支產出 `mainline_registry.json` / `branch_role_map.json` / `archive_candidate_report.json` / `unmerged_asset_report.json` |
| 06 | `06_CrossRepo_Deduplicator` | **spec only**：待 P1 全跑完後跨 repo HEAD-sha 比對 |
| 07 | `07_Capability_Mapper` | **spec only**：Asset → Module → Capability → Runtime → Product 映射待 P2 做完後接 |
| 08 | `08_NeuralGraph_Engine` | **可跑**：對目前 230 分支產出 `MRL_Branch_NeuralGraph.json`（401 nodes, 895 edges）＋ GraphML（Gephi 可讀） |
| 09 | `09_Evidence_Registry` | **spec only**：對應 MRL_Docs/Evidence/* 的入口與 SHA256 索引 |
| 10 | `10_Recovery_Action_Queue` | **spec only**：PR / recovery / archive 的執行項佇列；此佇列由 05 / 06 / 07 的結果 feed |

## 可跑引擎（_lib/，純 stdlib，無外部依賴）

- `_lib/role_infer.py` — 分支角色推斷規則引擎（10 角色；prefix + is_default + 內容線索）
- `_lib/branch_role_rules.yaml` — 推斷規則說明（純文件；邏輯內嵌 role_infer.py）
- `_lib/neural_graph.py` — 神經圖建構器（Repo / Branch / Commit / Role 節點；CONTAINS / DEFAULT_OF / HEAD_IS / SHARES_HEAD / MIRROR_OF / INFERRED_AS 邊）
- `_lib/resolve_mainline.py` — P3 主線／分線判定（寫 05/* 四份輸出）

## 一鍵（對目前 1 repo）
```sh
python3 _lib/neural_graph.py   --registry 02_Branch_Registry/branch_registry.json \
                               --dupes    03_dedupe/head_sha_duplicates.json \
                               --out-json      08_NeuralGraph_Engine/MRL_Branch_NeuralGraph.json \
                               --out-graphml   08_NeuralGraph_Engine/MRL_Branch_NeuralGraph.graphml
python3 _lib/resolve_mainline.py --registry 02_Branch_Registry/branch_registry.json \
                                 --dupes    03_dedupe/head_sha_duplicates.json \
                                 --out-dir  05_Mainline_Subline_Resolver
```

## 關鍵限制
1. `mcp__claude-code-remote__list_repos` 硬性 500 筆（最近 pushed）→ 老 repo 看不到。
2. `gh api` 只允許 **repo-scoped** 端點（repos/{owner}/{repo}/…）；user/org 層被封。
3. 跨 repo 要用 `mcp__claude-code-remote__add_repo` 一個一個授權；單 session 不能自動大量掛載。

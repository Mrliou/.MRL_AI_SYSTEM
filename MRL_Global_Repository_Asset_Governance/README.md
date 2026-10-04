# MRL_Global_Repository_Asset_Governance

origin_signature: MrLiouWord ｜ 建構者：MR.Liou ｜ 建立：2026-10-04 ｜ Additive-Only

> **建構者原話**：「不是先處理 PR，而是先建立系統，再由系統指出哪些 PR 值得處理。」
> PR #117 / #123 / #329 / #436 → 全部降級為 `10_Recovery_Action_Queue` 末端執行項。

## 10 子系統狀態（當下狀態 2026-10-04 18:xx Asia/Taipei）

| # | 子系統 | 狀態 | 關鍵數字 |
|---|---|---|---|
| 01 | Repository_Inventory | partial | **500 repo**（list_repos 500 筆硬性視窗；~650 老 repo 待補 add_repo 全量） |
| 02 | Branch_Registry | partial | **1/500 完成**（dofaromg/MRL_AI_SYSTEM 230 分支）；499 repo 待 add_repo |
| 03 | **Asset_Registry** | **可跑** | 3,770 檔（default branch 一棵樹）、1,660 唯一 blob、408 重複組；34 parent_module |
| 03 | dedupe/head_sha_duplicates | 可跑 | 38 組 HEAD-sha 共用（**全部在同一 repo 內**） |
| 04 | **Lineage_Engine** | **可跑** | 230 分支：fully_absorbed=51、has_unique_commits=179、orphan=0；by_role 吸收率在 `branch_diff_matrix.json` |
| 05 | **Mainline_Subline_Resolver** | **可跑** | ACTIVE_MAINLINE=1、SUB_MAINLINE=2、archive_candidates=34、unmerged=71；**HTML 視覺化：`MRL_Mainline_Subline_Map.html`** |
| 06 | **CrossRepo_Deduplicator** | partial | repo×DL580 跨來源盤點（部分可跑）；跨 repo 待 P1 完成 |
| 07 | **Capability_Mapper** | **可跑** | 29 能力軸 × 9 runtime（DL580 本機 7 + CF 2 Worker）；R07 flowrhythm 命中 repo 3 檔 |
| 08 | **NeuralGraph_Engine** | **可跑** | 401 nodes / 895 edges；JSON + GraphML（Gephi 可讀） |
| 09 | **Evidence_Registry** | **可跑** | 10 份 Evidence（SHA-256）+ Dropbox / DL580 鏡像索引 |
| 10 | Recovery_Action_Queue | spec | 由 05/06 feed；archive 候選 34、unmerged 71；PR 降級 |

## 可跑引擎（_lib/，純 stdlib，零外部依賴）

- `role_infer.py` — 10 角色推斷（UNKNOWN 預設非 FEATURE）
- `branch_role_rules.yaml` — 規則說明
- `neural_graph.py` — 節點／邊建構器 + GraphML 匯出
- `resolve_mainline.py` — P3 主線／分線判定
- `build_map_html.py` — HTML 視覺化（single-file，離線可開）

## 一鍵（對目前資料）
```bash
python3 _lib/neural_graph.py --registry 02_Branch_Registry/branch_registry.json \
    --dupes 03_dedupe/head_sha_duplicates.json \
    --out-json 08_NeuralGraph_Engine/MRL_Branch_NeuralGraph.json \
    --out-graphml 08_NeuralGraph_Engine/MRL_Branch_NeuralGraph.graphml
python3 _lib/resolve_mainline.py --registry 02_Branch_Registry/branch_registry.json \
    --dupes 03_dedupe/head_sha_duplicates.json \
    --out-dir 05_Mainline_Subline_Resolver
python3 _lib/build_map_html.py
```

## 關鍵限制
1. `list_repos` 硬性 500 筆（最近 pushed）→ ~650 老 repo 看不到
2. `gh api` 只允許 repo-scoped；user/org 封鎖
3. 跨 repo 必須 `add_repo` 逐個授權
4. 03_Asset_Registry 只掃 default branch 一棵樹；P2b all-branch sweep 待

## 重要發現（實機證據）
- MIRROR_BRANCH 154/230（67%）— `copilot/*` 85、`claude/*` 29、`codex/*` 4、`agent/*` 3，絕大多數與 canonical 分支共用 HEAD
- RECOVERY_BRANCH 32 條裡只有 13 已被吸收 → 另 19 條**可能保有獨有資產**，不得封存
- repo × DL580 母體**結構不同**：repo = code/schema/evidence 層；母體 = runtime data 層（含 125 GB models、5.3 GB pip-cache、71 MB RuntimeDaemon_API 等）—— 這是真正的 「散落的檔案」地圖
- DL580 672 top-level entries 裡 99 個 dir 無 repo 對應（repo-only 28 個模組） → 未來若要「母體 ↔ repo 單向可逆」，這 99 個 dir 各自需要定位到某個 repo 子樹

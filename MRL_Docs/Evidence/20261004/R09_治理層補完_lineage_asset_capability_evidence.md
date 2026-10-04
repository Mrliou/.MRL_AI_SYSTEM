# R09 · 治理層補完：Lineage / Asset / Capability / Evidence / Cross-source（當下狀態 2026-10-04 19:08 Asia/Taipei）

origin_signature: MrLiouWord ｜ Additive-Only ｜ 建構者 2026-10-04 指示：「幫我銜接散落的檔案跟建構缺少的」

## 這一輪補了什麼（接 R08 scaffold 之後）

### P1b 本地 git lineage（_lib + 04/branch_lineage.json）
- 本地 `.git` 已 unshallow（881 commits），對 230 遠端分支相對 default `MRL_AI_SYSTEM/memory-system-rules-prep` 計算：merge_base、ahead、behind、unique_commits、unique_files_count、last_commit_date/author、is_fully_absorbed。
- **fully_absorbed = 51／has_unique_commits = 179／orphan = 0**。
- by_role 吸收率：MIRROR 27/154（17.5%）、RECOVERY 13/32（40.6%）、SUB_MAINLINE 2/2（100%）、ARCHIVE 0/4、FEATURE 0/1。

### P2a asset_registry（03_Asset_Registry/）
- `git ls-tree` default branch 一棵樹（`-c core.quotePath=false` 以保留 CJK 檔名）→ 3,770 檔、1,660 唯一 blob、408 重複組。
- parent_module 前五：MotherSource（3029）、RuntimeOS v1.4.0（321）、09_workflow（58）、MRL_WorldModel（52）、docs（35）。
- 1.0 MB 最大檔是 FlowAgent .flpkg.zip 系列；沒有 >5MB binary。

### 06 跨來源映射（cross_source_asset_map.json）
- 透過 Bridge 盤點 `D:\mrl` 一層：**672 top-level entries**，file_count/total_size 齊備。
- repo 34 parent_module × DL580 672 entries → 只 6 匹配、28 repo-only、**99 DL580-only**。
- **repo 與母體結構不同**：repo = code/schema/evidence 層；母體 = runtime data 層。
- DL580-only top：models（125 GB）、pip-cache（5.3 GB）、MRL_Index（538 MB）、absorb（308 MB）、workspace（179 MB）、particle_imports（106 MB）、RuntimeDaemon_API（71 MB）。

### 07 Capability_Mapper（MRL_Capability_Lineage.json）
- 29 能力軸 × 9 runtime：DL580 本機 7 服務（7500/7812/7800/7825/7826/**7827**/7900）+ Cloudflare 2 Worker（mrliousilly / particle-replay）。
- 每個 runtime 的 repo_sources 已 blob_sha 核對；7827 FlowRhythm 命中 3 個 repo 檔，mrliousilly 命中 3 個，particle-replay 命中 1 個。

### 08 Neural Graph（既有引擎重跑）
- 401 nodes / 895 edges；GraphML 已輸出，Gephi 可開。

### 05 Mainline/Subline HTML Map
- 新增 `MRL_Mainline_Subline_Map.html`（single file，離線可開）。
- 按角色分區、chip 顯示 ahead/behind/unique_files、hover 看完整欄位；深／淺色自動切換。
- 已 SendUserFile 給建構者看。

### 09 Evidence Registry
- `evidence_index.json`：10 份 MRL_Docs/Evidence/* 全部有 SHA-256；標 Dropbox + DL580 鏡像。

## 檔位清單（新增 / 更新）
- `MRL_Global_Repository_Asset_Governance/03_Asset_Registry/{asset_registry,asset_hash_index,duplicate_asset_groups,parent_module_summary,dl580_mother_inventory}.json`+README
- `MRL_Global_Repository_Asset_Governance/04_Lineage_Engine/{branch_lineage,branch_diff_matrix,orphan_branches}.json`+README
- `MRL_Global_Repository_Asset_Governance/05_Mainline_Subline_Resolver/MRL_Mainline_Subline_Map.html`
- `MRL_Global_Repository_Asset_Governance/06_CrossRepo_Deduplicator/cross_source_asset_map.json`+README
- `MRL_Global_Repository_Asset_Governance/07_Capability_Mapper/MRL_Capability_Lineage.json`+README
- `MRL_Global_Repository_Asset_Governance/08_NeuralGraph_Engine/MRL_Branch_NeuralGraph.{json,graphml}` 重跑
- `MRL_Global_Repository_Asset_Governance/09_Evidence_Registry/evidence_index.json`+README
- `MRL_Global_Repository_Asset_Governance/10_Recovery_Action_Queue/README.md`
- `MRL_Global_Repository_Asset_Governance/_lib/build_map_html.py`
- `MRL_Global_Repository_Asset_Governance/README.md` 覆寫

## 未宣稱 / 下一步
- P0 的 ~650 老 repo（pushed_at 早於 2026-02-28）仍在 list_repos 視窗之外。
- P1 的 499 repo 需 add_repo 批准後 re-run `scratchpad/run_partial.py`。
- P2b all-branch sweep 待跑；本輪 asset_registry 只覆蓋 default 一棵樹。
- 外部 AI（ChatGPT/Claude/Google）**未接**；接時另立 runtime、不改本機路徑。

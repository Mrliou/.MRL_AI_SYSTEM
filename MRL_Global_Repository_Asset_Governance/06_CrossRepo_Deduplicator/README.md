# 06_CrossRepo_Deduplicator

origin_signature: MrLiouWord ｜ 2026-10-04 ｜ 跨 repo／跨來源 **部分可跑**

## 輸出
- `cross_source_asset_map.json` — **repo default branch** vs **DL580 D:\mrl top-level**（實機透過 Bridge 盤點）
- `head_sha_duplicates.json`（在 `03_dedupe/`）— 本 repo 內 230 分支的 HEAD 共用組

## 現況
- repo 根有 34 個 parent_module；DL580 D:\mrl 有 **672** top-level entries（99 個 dir 無 repo 對應，28 個 repo 模組無 DL580 對應）
- 兩邊**結構不同**：repo = code/schema/evidence 層；母體 = runtime data 層（含 125 GB models、5 GB pip-cache、71 MB RuntimeDaemon_API 等）
- 跨 repo（owner × repo × branch）去重：**待 P1 全跑完（499 repo add_repo 批准後）**

## DL580-only top 10（size）
見 `cross_source_asset_map.json#dl580_only_top_dirs_top30`。前五：models（125 GB）、pip-cache（5.3 GB）、MRL_Index（538 MB）、absorb（308 MB）、workspace（179 MB）

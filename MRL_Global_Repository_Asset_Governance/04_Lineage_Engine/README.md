# 04_Lineage_Engine

origin_signature: MrLiouWord ｜ 2026-10-04 ｜ 入口 spec，核心計算借 _lib/

## 任務
- 分支從哪裡分出（merge-base）
- 哪些檔案首次出現（first_seen）
- 哪些檔案跨分支漂移（content hash 相同、路徑不同）
- 哪些能力只存在於舊分支
- 哪些分支已被完整吸收（HEAD 可從 ancestor 可達）
- 哪些分支仍保有母體缺失資產（unique_assets > 0 且未 merge-back）

## 輸入／輸出
- 入：`02_Branch_Registry/branch_registry.json`、`03_dedupe/head_sha_duplicates.json`、（P2 完成後）`03_Asset_Registry/`
- 出：
  - `branch_lineage.json` — 每個 branch 的 fork_point / parent / child（P1b 用 `GET /repos/.../compare/{base}...{head}` 計算）
  - `branch_diff_matrix.json` — ahead/behind 矩陣（成本高；只跑 non-fork repo）
  - `orphan_branches.json` — 無法找到共同祖先的分支

## 現況
P1 只拿到 1/500 repo，compare API 尚未啟動。先把現有分類（_lib/role_infer）當 lineage 的「標籤層」用。

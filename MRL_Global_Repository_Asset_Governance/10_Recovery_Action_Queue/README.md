# 10_Recovery_Action_Queue

origin_signature: MrLiouWord ｜ 2026-10-04

PR / archive / recovery 的執行佇列。**此佇列由 05 / 06 / 07 的結果 feed，而不是由人工先寫**。

## 來源
- `05_Mainline_Subline_Resolver/archive_candidate_report.json`（低風險：MIRROR + 共用 HEAD → archive 候選，**不等於刪**）
- `05_Mainline_Subline_Resolver/unmerged_asset_report.json`（**不得封存**，可能保有獨有資產）
- `06_CrossRepo_Deduplicator/*`（待 P1 全跑完）

## 現況
PR #117 / #123 / #329 / #436 等舊佇列統統降級為「待系統建立後逐一驗證」，先不處理。

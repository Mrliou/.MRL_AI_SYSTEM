# 04_Lineage_Engine

origin_signature: MrLiouWord ｜ 2026-10-04 ｜ P1b 本地 git lineage 結果（230 分支 vs 預設分支）

## 任務（P1b 已實跑）

對 `02_Branch_Registry/branch_registry.json` 的 230 個分支 B，以本地 git（unshallow 後所有 remote refs 齊全）相對預設分支 D = `MRL_AI_SYSTEM/memory-system-rules-prep` 計算：

- 分支的 merge_base（分出點）
- ahead/behind 計數
- unique_commits（B 相對 D 的獨有 commits）
- unique_files_count（merge_base..B 的 diff 檔案數）
- 最後 commit 的 sha/date/author
- is_fully_absorbed：`ahead == 0 AND merge_base == head_sha`（B 的 HEAD 已在 D 可達 → 完全被主線吸收）

## 方法（實作在 `scratchpad/p1b_lineage.py`）

純本地 git，不打 GitHub API。每個分支以 `refs/remotes/origin/<branch_name>` 為 ref：

| 欄位 | git 指令 |
|---|---|
| merge_base | `git merge-base D B` |
| ahead | `git rev-list --count D..B` |
| behind | `git rev-list --count B..D` |
| unique_files_count | `git diff --name-only $(merge-base)..B \| wc -l` |
| last_commit | `git log -1 --format=%H\|%cI\|%an B` |

批次處理：ThreadPoolExecutor 平行度 20，每 50 條回報 stderr。失敗單筆記在 `error` 欄繼續（實跑 0 筆錯誤）。

## 輸出

- `branch_lineage.json` — 扁平陣列，按 `last_commit_date` desc 排序。欄位：`branch_id, full_name, branch_name, merge_base, ahead, behind, unique_commits, unique_files_count, last_commit_date, last_commit_sha, last_commit_author, is_fully_absorbed, parent_branch_candidate, error`。
- `branch_diff_matrix.json` — 聚合統計 + 用 `05_Mainline_Subline_Resolver/branch_role_map.json` 做角色交叉：`by_role_absorbed`。
- `orphan_branches.json` — 定義為 `ahead > 0 AND merge_base IS NULL`（與 D 無共同祖先）。

## 結果（當下狀態 2026-10-04，實跑本地 git）

- total：230
- fully_absorbed：**51**（ahead=0 且 merge_base=head_sha；HEAD 已在 D 可達）
- has_unique_commits（ahead>0）：**179**
- has_unique_files（unique_files_count>0）：**179**
- orphans（無共同祖先）：**0**
- 錯誤：0

51 + 179 = 230 — fully_absorbed 和 has_unique_commits 完全互斥，覆蓋全部 230。

### 角色交叉（by_role_absorbed，`absorbed/total`）

| role | absorbed/total | 比率 |
|---|---|---|
| ACTIVE_MAINLINE | 1/1 | 100% — 即 D 自己（merge_base=D 的 head） |
| SUB_MAINLINE | 2/2 | 100% — `worldmodel/mrl-dialect-v0`、`MRL_AI_SYSTEM/multi-domain-sync-core-v1`，皆已 fast-forward 吸收 |
| MIRROR_BRANCH | 27/154 | 17.5% — 大量 copilot/* 鏡像分支仍帶 1~2 個獨有 commit（看起來是 bot 增量 patch） |
| RECOVERY_BRANCH | 13/32 | 40.6% — `MRL_recovered/*` 多數已被重整回主線；仍有 19 個帶獨有變更 |
| ARCHIVE_BRANCH | 0/4 | 0% — `backup/MrliouAI-*-20260724` 等備份點本就「凍結在歷史某點」，不會被 D 覆蓋 |
| FEATURE_BRANCH | 1/1 | 「fix/mrliou-product-telemetry-canonicalization」仍活著（540 檔獨有） |
| UNKNOWN_BRANCH | 8/36 | PR 類分支（mrl/pr149-*、mrl/pr151-*、dl580-tunnel-recover-20261004 等）大多還在 flight |

## 真正孤立分支

**0 筆**。230 個分支全部與預設分支共有 merge_base — 這個 repo 內部沒有「獨立起源」分支（無 `git commit --orphan` 類操作）。

→ P1b 的 orphan 定義在本 repo 無命中。若之後要抓「邏輯孤立」（例如 ahead 很高且很久沒動），需要用別的門檻（例如 `ahead > 1000 AND age > N days`），不是這次的任務範圍。

## Limitation（當下狀態標註）

1. **只跟預設分支一個比**：lineage 計算 base 固定是 D。SUB_MAINLINE 之間的交叉關係沒算（例如 `multi-domain-sync-core-v1` 和 `memory-system-rules-prep` 的分叉點，就是它自己的 head），所以某個分支真正的「爸爸」若不是 D，這邊的 `parent_branch_candidate` 只是標了 D，不是真實父分支推論。
2. **head_sha 以本地 ref 為準**：registry 的 `head_sha` 來自 P1 當時的 GitHub API 拍照，本地 `refs/remotes/origin/<B>` 是 fetch 當下的版本。實跑時 `last_commit_sha` 直接讀本地 ref 的 head，若 GitHub 遠端在 fetch 之後又有 push，這邊的 last_commit 會比 registry.head_sha 新。
3. **is_fully_absorbed 定義**：採 `ahead==0 AND merge_base==head_sha`，等同於「HEAD 可從 D 可達」。這偵測 fast-forward 吸收或 squash-merge-into-D。若 D 是 B 的 merge-commit 父節點，但 B 又有新 commit，則 `ahead>0`、不算 absorbed（這是對的）。
4. **unique_files_count 的語意**：採 `merge_base..B` 的 diff，表示「B 分出去之後動了幾個檔」。它跟「B vs D 現在差幾個檔」不同（後者等於 `D..B` 的 diff name-only，會把 D 側的新檔也視為差異）。對於要知道「B 到底帶了多少不在 D 的工作」這題，前者才對。
5. **只讀 origin remote**：`allb/*`、`full/*` 兩個額外 remote 的分支沒進 registry，也不在此計算範圍。

## 下一步建議

- **P1c（可選）**：對 `MIRROR_BRANCH` 中仍 live 的 127 筆，計算 `ahead=1~2` 的那些是不是只有 bot squash commit — 用 commit message 判定是否可直接關閉。
- **P1d**：對 `RECOVERY_BRANCH` 的 19 筆未吸收分支，去比對它們的 `unique_files` 是否已經在 D 的某處 — 真的沒了（需要回收），還是只是檔名換過（可丟）。這個要先有 P2 asset_registry 才做得到。
- **P2 asset_registry**：見同層目錄 `../03_Asset_Registry/`。

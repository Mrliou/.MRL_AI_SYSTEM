# 02_Branch_Registry — P1 Branch 全量盤點

**當下狀態（2026-10-04，沙盒 agent-proxy 執行）**：

- 這是 **partial** 收斂結果，不是完整 500 repo 的 branch 全圖；詳見下方「限制與下一步」。
- 500 個 repo 中，**1 個完整抓到**（`dofaromg/MRL_AI_SYSTEM`，230 branches），
  **499 個 pending_access**（403，`add_repo` 未授權）。
- 檔案格式與 schema 已完整，資料欄位齊整；補完僅需在相同 pipeline 上授權後 re-run。

## 檔案

| 檔案 | 內容 |
|---|---|
| `branches_raw.jsonl` | 每行一個 repo 的原始回應 `{full_name, owner, repo, repo_meta, default_commit_date, branches:[...], branch_count, errors:[...], status?}`。pending_access 的 repo 也占一行，`errors` 載明原因，`inventory_hints` 保留 P0 既有欄位 (visibility/fork/pushed_at/can_push)。 |
| `branch_registry.json` | 扁平 branch 列表，依 `full_name` → `branch_name` 排序。欄位：`branch_id` (sha1 前 16 字 of `{owner}/{repo}@{branch_name}`)、`full_name`、`owner`、`repo`、`branch_name`、`head_sha`、`protected`、`is_default`、`repo_default_branch`、`repo_size_kb`、`repo_language`、`repo_archived`、`repo_fork`、`repo_pushed_at`。 |
| `branch_counts.json` | 總計與分組：`total_branches`、`by_owner`、`by_fork`、`by_archived`、`repos_with_only_default_branch[*]`、`max_branches_top10`，另有 `repos_fetched`、`repos_pending_access`、`repos_with_errors` 以供後續狀態追蹤。 |

head_sha 跨 repo／跨 branch 重複分析在同一棵樹的 `03_dedupe/head_sha_duplicates.json`。

## 方法

對每個 repo：
1. `GET /repos/{owner}/{repo}` 取 `default_branch, size, language, archived, fork, created_at, updated_at, pushed_at, open_issues_count` 等。
2. `GET /repos/{owner}/{repo}/branches?per_page=100&page=N` **手動分頁**（agent-proxy 拒絕 `--paginate` 跟隨之 `repositories/{id}/...` numeric-ID URL，所以不使用 `--paginate`）—— 每頁 100，直到回傳 < 100 筆或空陣列。
3. 對 default_branch 的 HEAD SHA，`GET /repos/{owner}/{repo}/commits/{sha}` 取 `commit.committer.date` 作 `default_commit_date`。
4. **僅 default branch 取 commit date**。非 default 的 commit date、ahead/behind、unique commits / files，為 P1b 另做（成本為 N × M，須以 `GET /repos/{owner}/{repo}/compare/{base}...{head}` 執行）。

並行度：ThreadPoolExecutor，batch=20；每 50 筆 echo 進度到 stderr。單 repo 任何階段錯誤收進該 repo 的 `errors[]`，整體流程不中斷。

## 當下數字（partial）

- `total_branches`：230
- `by_owner`：`{"dofaromg": 230}`（僅 1 repo 可取；469 dofaromg + 31 Mrliou 未進）
- `repos_fetched`：1 / 500
- `repos_pending_access`：499 / 500
- `max_branches_top10`：`[["dofaromg/MRL_AI_SYSTEM", 230]]`
- head_sha dedupe groups：38（跨 branch coord，皆在同一 repo 內 — 皆為 recovered/copilot/claude 等 prefix 下的鏡像分支）

### `dofaromg/MRL_AI_SYSTEM` branch naming prefix top10

| prefix | count |
|---|---|
| `copilot/*` | 85 |
| `(no-slash)` | 64 |
| `MRL_recovered/*` | 32 |
| `claude/*` | 29 |
| `codex/*` | 4 |
| `agent/*` | 3 |
| `mrl/*` | 3 |
| `MRL_AI_SYSTEM/*` | 2 |
| `backup/*` | 2 |
| `evidence/*` | 2 |

`default_branch`：`MRL_AI_SYSTEM/memory-system-rules-prep` — HEAD 2026-10-04T02:24:01Z。
`protected` 分支：0。

## 限制（當下狀態 2026-10-04）

1. **access gating**：此 session 的 agent-proxy 僅附掛 cwd 對應之 `dofaromg/MRL_AI_SYSTEM`；其他 499 repo 走 `api.github.com` 一律 HTTP 403，回應明示須呼叫 `add_repo` 工具。該工具在 auto-mode 分類器下被阻斷（permission 分類為 `[Permission Grant]`），本輪未取得授權，故 pending。
2. **非 default branch commit date**：未收，成本考量。
3. **非 default branch 的 ahead/behind、unique commits / files**：須 `GET /compare/{base}...{head}` × 每 branch，標記為 P1b。
4. **cross-repo head_sha dedupe**：當前 38 groups 都在單一 repo 內（分支改名／recovery／copilot/claude 多樣存檔）。真正的「跨 repo 鏡像」偵測須等 pending 499 補完。
5. **大於 20 branches 的 repo 的 top 10 最近 branches**：本輪未抓（本任務指示欄 7），且在沒有非 default branch commit date 的前提下，「最近」只能用 branch head sha 的 committer date 定義，與 default-only 政策衝突 → 搬到 P1b 統一處理。

## 下一步（P1b 待辦）

1. 授權 `add_repo` 以逐 repo 掛載，re-run `scratchpad/fetch_branches.py`；partial jsonl 可直接覆蓋（schema 已穩）。
2. 完成後，re-run `scratchpad/build_registry.py` 重算 registry / counts / dedupe。
3. 擴充功能：
   - 非 default branch commit date（可用 `GET /commits/{sha}` 僅對 top-N 分支）
   - `GET /compare/{default}...{branch}` → ahead/behind、unique commits、changed files
   - 跨 repo HEAD-sha dedupe → fork／mirror／split 檢測
4. 把 branch_registry.json 寫入 PG / D1，加 `last_active`、`is_ahead_of_default`、`is_dead` 等衍生欄位。

## 誠實狀態標記（CLAUDE.md 規約）

- `repos_fetched = 1` — 實跑過（沙盒 gh api，透過 agent-proxy）— 當下狀態 2026-10-04。
- `repos_pending_access = 499` — pending，未實跑，待 `add_repo` 授權後 re-run。
- 不得將此輪結果對外宣稱為「全 500 repo branch 盤點完成」。

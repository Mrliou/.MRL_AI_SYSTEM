# 01_Repository_Inventory — P0 Repository 全量發現

> 當下狀態：2026-10-04（沙盒，透過 `list_repos` MCP 工具）。非永久結論；視窗會隨推送時間移動。

## 這是什麼

MR.liou GitHub 平行世界空間（owner `dofaromg` + `Mrliou`）的 repository 清單第一版，作為後續 P0b／P1 治理（分支、大小、語言、母體定位）的底表。

## 方法

- 工具：僅用 `mcp__claude-code-remote__list_repos`（`query` 子字串過濾，`limit=200`）。
- 枚舉：對 `dofaromg/` 與 `Mrliou/` 兩個前綴，各接 `a-z`、`0-9`、`-`、`.`、`_` 共 39 個字元逐一查詢，另加兩次裸前綴查詢；合計 80 次枚舉 + 3 次探針。
- 以 `full_name` 去重，依 `full_name` 排序。

## 當下計數（2026-10-04）

| 項目 | 數量 |
|---|---|
| 總數（去重） | 500 |
| dofaromg | 469（fork 438 / 非 fork 31） |
| Mrliou | 31（fork 19 / 非 fork 12） |
| 可見性 | public 469 / private 28 / internal 3 |
| 名稱含 mrl 的 fork | 100 |
| 兩 owner 同名 | 13 |
| pushed_at 視窗 | 2026-02-28 → 2026-10-04 |

非 fork 清單（MRL 原生候選）見 `repository_status_map.json`。

## 限制（必讀）

1. **視窗上限 500**：去重總數恰為 500，且每一個查詢（含空結果與無意義字串）都回 `has_more=true`，最舊 `pushed_at` 一律止於 2026-02-28。推定此工具只回最近推送的 500 筆可存取 repo，再做子字串過濾；`has_more` 無法藉由再切分消除。建構者自述兩帳號約 1,150 repo，故約 650 筆早於 2026-02-28 推送的 repo **本工具看不到**。看不到 ≠ 不存在（遵守「局部視角不得升格全局權威」）。
2. 只列本帳號可存取的 repo。
3. 工具不提供 branch、size、language、default_branch、archived、description 等欄位，一律標 **待補**，由 P0b 以 per-repo API（`gh api repos/{owner}/{repo}`）補齊；P0b 同時應以 `gh api users/dofaromg/repos` / `orgs/Mrliou/repos` 分頁補足 500 視窗外的 repo。
4. `can_push` 全為 true（本帳號對兩 owner 皆有推送權）。

## 檔案

- `repositories.json` — 完整清單（含 `origin_signature: MrLiouWord`、`generated_at`、`count`）。
- `repository_inventory.csv` — 同內容表格版。
- `repository_status_map.json` — 依 owner／可見性／fork 的計數、各 owner 非 fork 清單、MRL 命名 fork、兩 owner 同名清單、限制說明。

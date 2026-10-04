# 03_Asset_Registry

origin_signature: MrLiouWord ｜ 2026-10-04 ｜ P2a 母體預設分支一次性 asset snapshot（3,770 檔）

## 任務（P2a 已實跑）

對預設分支 D = `MRL_AI_SYSTEM/memory-system-rules-prep` 的檔案樹（一棵樹，不含歷史）建 asset registry：

- 每個檔一條記錄：`asset_id`、`canonical_path`、`blob_sha`、`size`、`content_type`、`language`、`parent_module`、`branches_present`、`capability_hint`、`runtime_hint`
- 建 blob_sha → paths 的索引（讓 content-identical 檔自然 groupby）
- 標出 repo 內 content-duplicate 的檔案組（同 blob 出現在 ≥2 條路徑）
- 按 parent_module 聚合（file count / total size / top content types / top hints）

## 方法（實作在 `scratchpad/p2_asset_registry.py`）

一次 `git ls-tree`（不走 GitHub API）：

```
git -c core.quotePath=false ls-tree -r --long refs/remotes/origin/MRL_AI_SYSTEM/memory-system-rules-prep
```

**`core.quotePath=false` 很重要**：預設 git 會把 CJK 檔名 C-escape（例如 `"MRL_\346\257\215..."`），這個 repo 有 1,579/3,770 個路徑含中文；關掉 quote 才能拿到真的檔名、第一層目錄才聚得準。

每條 ls-tree 記錄解析成：

| 欄位 | 來源 |
|---|---|
| asset_id | `sha256(canonical_path).hex[:16]` |
| canonical_path | ls-tree TAB 右邊的 repo-relative path |
| blob_sha | ls-tree 第三欄 |
| size | ls-tree 第四欄（bytes） |
| content_type / language | 依副檔名查表（.py→python、.mjs→javascript、.md→markdown、.json→json、.yaml→yaml、.fltnz/.pcode→mrl_particle…，其他→text 或 binary） |
| parent_module | path 的第一層目錄；根目錄的檔標 `<ROOT>` |
| branches_present | `["MRL_AI_SYSTEM/memory-system-rules-prep"]`（P2a 只掃預設；P2b 做全分支 sweep） |
| capability_hint | 由 parent_module 推：MRL_WorldModel→rhythm/world_model、MRL_Mother→memory/mother、MRL_Platform_Server/src→code、docs/MRL_Docs→documentation、deploy/MRL_Deploy→deployment、MRL_Global_Repository_Asset_Governance→governance；沒命中→null |
| runtime_hint | 由檔名/路徑模式推（先較具體再 fallback）：含 `inference`/`persona`→DL580_7500；含 `flowrhythm`/`flow_rhythm`→DL580_7827；含 `bridge`→DL580_Bridge_7800；含 `Module_Integration`→DL580_7825；含 `worker`/`cloudflare`/`.mjs`→Cloudflare_Worker；含 `_dl580_`/`DL580`/`workspace`→DL580_runtime；沒命中→null |

每 500 條回報 stderr。

## 輸出

- `asset_registry.json` — 3,770 條扁平陣列，依 canonical_path 排序。
- `asset_hash_index.json` — `{ blob_sha → [canonical_path, …] }` 完整索引（1,660 keys）。
- `duplicate_asset_groups.json` — blob_sha 出現 ≥2 次的分組（408 組，涵蓋 2,518 檔）。
- `parent_module_summary.json` — 按 parent_module 聚合：file_count、total_size、capability_hints 分佈、runtime_hints 分佈、content_types 分佈。

## 結果（當下狀態 2026-10-04）

- **總檔數**：3,770
- **唯一 blob 數**：1,660
- **重複檔案（> 1 份）**：2,518（1,660 - (1,660-408) = 2,518；也就是 408 個 blob 分佈到 2,518 條路徑）
- **重複組數**：408（blob_sha 出現 ≥ 2 次）
- **錯誤**：0（ls-tree 解析 0 筆失敗）
- **> 5MB 的大檔**：**0**（最大檔 ~1.0 MB，是 `FlowAgent.*.v1` 壓縮包）

### Top 5 parent_module（by file count）

| parent_module | files | 備註 |
|---|---|---|
| MRL_MotherSource_ZhiZhang_FlowAgent_Lineage_v1 | 3,029 | 母源 FlowAgent 的 Lineage 封裝；內含 FlowAgent.Runtime.v1 到 v47 多版本平行存放 |
| MRL_RuntimeOS_EnterpriseRuntimePlatform_CoreExecutable_v1_4_0 | 321 | RuntimeOS Enterprise 核心可執行層 |
| 09_workflow | 58 | GitHub Actions / workflow 相關 |
| MRL_WorldModel | 52 | 世界模型層；capability_hint=rhythm/world_model |
| docs | 35 | 文件；capability_hint=documentation |

Top 10：加上 `MRL_Docs=29`、`MRL_Deploy=27`、`.github=22`、`<ROOT>=20`、`MRL_Symbolic=18`。

### Content type 分佈（前 10）

python=1473、text=536、json=526、archive=474、markdown=267、mrl_particle=171、shell=84、javascript=64、svg=41、pdf=35。

### Runtime hint 命中

總共 436/3,770 檔命中（11.6%）：
- DL580_7500：363（inference / persona）
- DL580_7827：28（flowrhythm）
- DL580_Bridge_7800：22（bridge）
- DL580_runtime：17（含 DL580/workspace 關鍵字）
- Cloudflare_Worker：6（.mjs / worker / cloudflare）

### 重複組 top 3（為什麼會重）

1. `FlowAgent.Runtime.v1..v47/flow_cli.py` — 同一支 CLI 檔，在 47 個版本資料夾各一份（blob 93e82f82…）
2. `FlowAgent.Runtime.v1..v47/run.sh` — 同上，47 份（b864ed98…）
3. `FlowAgent.Runtime.v1..v47/boot.py` — 同上，47 份（ea66284f…）

→ Lineage_v1 目錄採「版本資料夾平行放」的保存法；content 層面有大量冗餘，但從「保留歷史快照」的角度看不是 bug。

## Limitation（當下狀態標註）

1. **只覆蓋預設分支一棵樹，不含歷史**：asset_registry 等於 D 的 HEAD 當下的檔案清單。D 的歷史裡被刪過的檔、別的分支獨有的檔，這個表都沒有。要抓那些要走 P2b。
2. **branches_present 只標 D**：所有 3,770 條都標 `["MRL_AI_SYSTEM/memory-system-rules-prep"]`。要知道一個檔還存在於哪些分支，必須對每個 (blob_sha, path) 跟 230 個分支的 tree 交叉查詢（230 × 3,770 ≈ 87 萬次 blob 查詢，但 git 內部可用 `git cat-file --batch-check` 批次處理）。這是 P2b 的工作。
3. **capability_hint 只用一層目錄**：目前只用 `parent_module` 映射，所以 3,650/3,770（96.8%）都是 `<none>`。要更細，可以用檔名正則或檔案內容做二次推論，但那是 P2c 等級。
4. **runtime_hint 命中率 11.6%**：是把 user plan 給的規則照抄的結果；不是精準分類，而是粗略 label。
5. **blob_sha 是 git 的 SHA-1，不是檔內容的 SHA-256**：git blob SHA 已含標頭（`blob <size>\0`），不等於單純對檔案 bytes 算 hash。做跨 repo 的 content-identical 比對時要注意。
6. **大檔門檻 5MB 無命中**：這 repo 的大檔都是 FlowAgent 的壓縮包（~1MB 等級）；真正的大 binary（模型權重、資料集）不在本 repo。

## P2b 計畫（all-branch sweep）

- 對 230 個 `refs/remotes/origin/<B>` 各跑一次 `git ls-tree -r <B>`，建 `{(blob_sha, path) → [B, ...]}` 的反向索引
- 更新 `asset_registry.json` 的 `branches_present` 欄為真實分支清單
- 新增 `only_in_branches.json`：D 沒有、只有某些 B 有的檔案（這就是 P1b 說「要先有 P2 asset_registry」才做得到的那題：RECOVERY_BRANCH 中仍 live 的 19 筆，unique_files 是不是母體 D 真的沒有？）
- 新增 `only_in_default.json`：D 有、某些 B 已經沒有的檔案（判斷「吸收後是否也移除了」）

成本：230 × 3-4k 檔 ≈ 70-100 萬條，Python stdlib + ThreadPoolExecutor 平行 20 應該可以在幾分鐘內跑完，是可行的。

## 下一步建議

1. **先做 P2b**，有了 `branches_present` 才能回答「P1b 未吸收的 unique_files 是不是真的只在 B」。
2. **跟 03_dedupe/head_sha_duplicates.json 交叉**：38 個 head_sha 等價組（分支層）＋ 408 個 blob 等價組（檔案層）合在一起看，就能分出「同 head 的鏡像分支」vs「不同 head 但大量檔案相同的 forked 分支」。
3. **跟 05_Mainline_Subline_Resolver/branch_role_map.json 交叉**：MIRROR_BRANCH 有多少檔是真的「跟 D 完全一樣」vs 「大部分相同、幾個 bot patch」，為 ARCHIVE 決策做底。

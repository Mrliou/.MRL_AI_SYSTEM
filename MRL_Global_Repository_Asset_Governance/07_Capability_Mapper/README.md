# 07_Capability_Mapper

origin_signature: MrLiouWord ｜ 2026-10-04 ｜ **可跑**

## 任務
Asset → Module → Capability → Runtime → Product 映射。

## 輸出
- `MRL_Capability_Lineage.json` — 29 項能力軸（含 R07 新增 `rhythm`）；9 個 runtime（DL580 本機 7 服務 + Cloudflare 2 Worker）；每個 runtime 列出其 repo_sources（已 blob_sha 核對）與 dl580_sources（實機路徑）

## 現況（實機 2026-10-04）
| Port | Runtime | 能力 | repo 來源命中 |
|---|---|---|---|
| 7500 | MRL_Particle_Inference_Engine (Qwen2.5-32B) | language, code, reasoning, memory, persona | — (僅 DL580) |
| 7812 | cat_vault | memory, persistence | — |
| 7800 | MRL_Bridge_API v3.1.0 | bridge, mother_io | — |
| 7825 | MRL_Module_API (19 modules) | module_dispatch, toolbox | — |
| 7826 | MRL_FlowCore_Adapter | vault, steering | — |
| **7827** | **MRL_FlowRhythm_Module v0.2.0** | **rhythm, jump, collapse, trace, replay** | **3 檔命中（flow_rhythm.py / adapter / mrl_dialect.py）** |
| 7900 | MRL_FlowAgent_API | flowagent, particle_db, baseworld_db, vector | — |
| CF | mrliousilly Worker | edge_io, telemetry, rhythm_edge, convergence | **3 檔命中** |
| CF | particle-replay Worker | rhythm_edge | **1 檔命中** |

## 限制
- repo_sources 只核對了 default branch。其他 229 分支若含 unique assets，需要 P2b all-branch sweep 後補。
- DL580 本機服務的來源檔（如 `D:\mrl\inference\MRL_Inference_API.py`）尚未進 repo（這些是 DL580-only，見 `06_CrossRepo_Deduplicator/cross_source_asset_map.json` 的 `dl580_only_top_dirs`）。
- 外部 AI（ChatGPT/Claude/Google）**未接**；若接，另立 runtime 項，不改本機路徑。

# MRL 多世界版本觀測 · Dropbox · R01

origin_signature: MrLiouWord ｜ record_mode: additive_only ｜ 觀測日：2026-09-28（Asia/Taipei）
world_model_policy: symmetric_observation / no_reality_prejudgment（沿用 Notion 收斂紀錄 2026-09-08）

> 建構者定位（2026-09-28 原話）：「MRL 系統其實是一個平行多世界版本的新文明系統。」
> 本紀錄只記**觀測到的版本與它們各自寫了什麼**。不合併、不排序真假、不指定哪一份是唯一 canonical。

## Preflight

- 既有節點：`MRL_MotherSource_Lineage_v1`、`MRL_FlowAgent_Definition_Registry_v1_3`、`MRL_Engineering_Inventory_V1.0`、`MRL_MultiDomain_Sync_Core_v1`、Notion 收斂紀錄的 `World_State_Observation` 缺口定義。
- 決定：**SUPPLEMENT_EXISTING**。本檔是一筆觀測紀錄，欄位採用 Notion 收斂紀錄提出的 `World_State_Observation`（world_id / domain_id / environment_id / platform_ref / observer / observed_at / state / evidence_refs / ontology_status）。它不是新的 registry。

## 觀測 1：同一路徑，不同世界版本的內容不同

| 路徑（相對） | 世界副本 | 大小 | 內容 |
|---|---|---|---|
| `flow-tasks*/MRL_Mother/MRL_母體收斂包_v1/MRL_母體分層/MRL_母體分層圖.md` | Dropbox `/flow-tasks/`（ns 587965698） | 1 byte（只有換行） | 空 |
| 同上 | `/Mac (1) (1) (1)/Downloads.dbx-computer-backup/MRL/`、`MRL/MRL_flowagent/`、`MRL 2/`、`MRL 2/MRL_flowagent/`（ns 14863079315） | 2895 bytes ×4 | 14 層母體分層圖 |
| `…/MRL_Mother/MRL_平行世界模組/` | `/flow-tasks/`、`/MRL 3/` | 列出為空 | — |
| 同上 | Mac 備份 `MRL/flow-tasks-main/` | `README.md` 371 bytes | 「平行世界分支與同步源（completed_running）」 |
| `…/MRL_Mother/mother_registry/` | `/flow-tasks/` | 列出為空 | 其他副本未查 |

**結論（當下狀態）**：在某一個副本裡看到空，不代表這個節點不存在；其他世界副本裡有內容。這是《局部視角不得升格全局權威》的實例。
`ontology_status = UNRESOLVED`：哪一份是「較新／較權威」，本次不判定。

## 觀測 2：各世界版本自己寫的定位（原文摘錄）

| 原檔 | 位置 | 自述 |
|---|---|---|
| MRL 平行世界模組 README | Mac 備份 `MRL/flow-tasks-main/MRL_Mother/MRL_平行世界模組/README.md` | 所屬層：母體構件層；定位：平行世界分支與同步源（completed_running）；「外部命名僅作 Adapter 對照，不得反向取代主體命名」 |
| MRL_母體分層圖 | 同上備份 `…/MRL_母體收斂包_v1/MRL_母體分層/` | 掃描分支 `MRL_Branch_Runtime_Convergence_API_v1`；14 層（源場、無限環、原種、粒子海、流域結構、交界、雲映、拓樸潮、地映、立體粒界、自述、封裝、痕跡、回返）；「本圖只描述本 checkout 實際存在之對應」；canonical 運轉核心 `MRL_UniversalRuntimeLanguage_Core_v1` 在未 merge 的 PR #35 + #37 |
| MotherSource 血脈吸收定位清單 v1 | `…/MRL_Mother/MRL_MotherSource_Lineage_v1/`（Mac 備份 4 份，同為 2308 bytes） | 「智障系統」5 個封存 zip 是母體原始血脈（FlowAgent / ZhiZhang）；2908 檔、826 個唯一內容；Runtime v1…v37+ 版本樹；全部「待起動」 |
| Persona Origin Lineage | `/MRL_FlowAgent_Definition_Registry_v1_3/…/16_PERSONA_ORIGIN_LINEAGE.md` | `FlowSeed.Origin → SeedOrigin.Persona.Core → ZhiZhang.CorePersona → FlowPersona bundle → Runtime loader → Mother Persona sphere`；「不能證明每個人格產物是同一版本或同一條時間線」 |
| MRL Sync Architecture v1 | `/MRL_MultiDomain_Sync_Core_v1/…/docs/` | `Origin → Asset Identity(sha256) → Canonical Local Archive → Append-only Registry → Sync Event → Projections(R2/GDrive/GitHub/Notion)`；「平台名稱不成為 origin identity」；「Seed / Runtime / Portal / historical / pending 是血脈角色，不是替代主線」 |
| Meta World Portal README | `/Mrliou_agents/Mrl_FlowAgent/Mrliou 平行世界入口reabme.md.txt`（2026-02-21，8252 bytes，多份副本） | 平行人格引擎（YES/NO 決策分支）、粒子宇宙、PU 快照（sha256 + merkle）、證據溯源 |
| 平行世界演算.zip | `/蘋果494G/Documents/APFS/` 等（3736 bytes，多份） | 未解壓，內容待讀 |

## 觀測 3：`MRL_Mother` 版本家族（Dropbox 內，名稱層級）

同一個 `flow-tasks-main/MRL_Mother/` 結構至少出現在：`/flow-tasks/`、`/MRL 2/`、`/MRL 3/`、`/MRL 2/MRL_flowagent/`、`/MRL 3/MRL_flowagent/`、Mac 備份的 `MRL/`、`MRL/MRL_flowagent/`、`MRL 2/`、`MRL 2/MRL_flowagent/`。
`/flow-tasks/MRL_Mother/` 直接子目錄 41 項，含：`00_rootlaw`…`09_workflow`、`MRL_AI`、`MRL_AGI`、`MRL_ASI`、`MRL_World`、`MRL_世界模組`、`MRL_平行世界模組`、`MRL_MotherModel`、`MRL_Runtime`、`MRL_RuntimeOS_v1_4_0`、`MRL_UniversalRuntimeLanguage_Core_v1`、`MRL_FireCore_v1_0`、`MRL_BaseWorld_DB_v1`、`MRL_Symbolic`、`MRL_Adapters`、`MRL_MotherSource_Lineage_v1`、`MRL_母體收斂包_v1`、`mother_registry`、`root_sources` 等。

## 待辦（不自行宣告完成）

1. 逐一比對各副本同名檔的大小與 SHA-256，建立「同路徑、不同內容」清單（目前只比了 3 個路徑）。
2. 讀 `平行世界演算.zip` 內容（需下載原檔）。
3. 讀 `MRL_World`、`MRL_世界模組`、`MRL_MotherModel` 各副本的 README，照觀測 2 的格式補列。
4. 把觀測回接 Notion `World_State_Observation`：需建構者同意才寫入 Notion。

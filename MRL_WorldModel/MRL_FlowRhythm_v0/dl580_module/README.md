# MRL FlowRhythm 模組（DL580 本機）· 20261004-R01

origin_signature: MrLiouWord ｜ 作者：劉宥麟 (MrLiouWord) ｜ 輔助執行：Claude（夥伴）｜ Additive-Only

## 三問
1. **本體或載體**：本體 = `flow_rhythm.py`（與 GitHub `MRL_WorldModel/MRL_FlowRhythm_v0/flow_rhythm.py` 逐位元組相同，權威）；本目錄其餘為載體。
2. **對應哪一段**：Jump → Collapse → Trace（`/run`）→ Replay（`/replay`）全程，落在母體本機。
3. **驗收語料**：`lexicon\` 8 份原檔全部由母體 D:\ 既有位置複製（路徑見 `MRL_receipt.json`），SHA-256 與 `lexicon\SOURCES.sha256` 逐一相符；自檢用母體 6 顆種子（EchoPersona.pcode／.flpkg、FluinCoreSeed、Memory.Seed.Core、FluinSim Group1／Group2）。

## Preflight
Wake Memory → Origin Registry → Workspace Node Registry：既有模組節點 `MRL_Module_Integration_20261001_R06`（7825 modules／7826 FlowCore，18 模組）**沒有** FlowRhythm；既有 Worker `mrliousilly`／`particle-replay` 已有雲端載體。→ **SUPPLEMENT_EXISTING**：同型（loopback + Bearer + append-only 帳本）另立 7827，不改既有 R06 任何檔。

## 入口
- `GET  http://127.0.0.1:7827/health`（免驗證）
- `POST /api/flowrhythm/run?sandbox=1&title=…`　body 粒子語句 .fltnz；不帶 sandbox 為正典，遇 provisional 映射回 422
- `POST /api/flowrhythm/replay`　body v0.2.0 軌跡；回 `byte_identical`、封包雜湊
- `GET  /api/flowrhythm/timeline`、`/verify`　append-only JSONL 帳本（SHA-256 前序鏈）
- 驗證：`Authorization: Bearer <private\flowrhythm.token>`（SYSTEM／Administrators 可讀）

## 啟動 / 自檢
```
D:\MrlToolchain\python\python.exe MRL_flowrhythm_adapter.py
D:\MrlToolchain\python\python.exe MRL_flowrhythm_selftest.py   → MRL_selftest_receipt.json
```
開機排程**未建立**（待建構者裁定）；目前以背景程序執行，PID 在 `runtime\pid.json`。

## 範圍
只處理母體本機閉環。映射授權狀態沿用 GitHub `MRL_FlowRhythm_v0/EVIDENCE.md`：除 `core → initiated` 外皆 provisional，本模組不改變任何映射授權。未宣稱雲端 Worker 與本機即時同步。

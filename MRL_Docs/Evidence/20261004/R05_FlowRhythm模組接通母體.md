# R05 · FlowRhythm 模組接通母體（實機 DL580，當下狀態 2026-10-04 12:20 Asia/Taipei）

origin_signature: MrLiouWord ｜ Additive-Only ｜ 建構者指示：「接通模組建構模組」

## 三問
- **本體或載體**：本體 `flow_rhythm.py`（repo `MRL_WorldModel/MRL_FlowRhythm_v0/`，sha256 `bc4a5df1…`）逐位元組放到母體；載體 = 母體本機 adapter（127.0.0.1:7827）。
- **對應段**：Jump → Collapse → Trace（run）→ Replay（replay），在母體本機完成。
- **驗收語料**：母體 D:\ 既有的 8 份 2025-07 原檔（7 份在 `D:\mrl\…\flowagent_final\expanded_core\engineer_pack\`，FluinSim 在 `D:\deep-learning-containers-main\flowagent_final拷貝\…\engineer_pack\`），SHA-256 與 `lexicon/SOURCES.sha256` 全部相符；6 顆母體種子。

## Preflight
母體既有模組節點 `D:\mrl\workspace\MRL_Module_Integration_20261001_R06`（7825 modules：particle/webgpu/attention/simhash/pvm/kernel/reversible/toolbox/timeline/environment/weather/capabilities/topology/unified/terminal/fluin/flowcore/seed；7826 FlowCore）—— 無 FlowRhythm。Codex 10/04 08:45 的 `MRL_Mother_Continuation_20261004_R01` 已驗 particle 模組 + 7500 推理 + 世界記憶鏈（PASS）。→ **SUPPLEMENT_EXISTING**：同型另立 `MRL_FlowRhythm_Module_20261004_R01`（loopback、Bearer、append-only SHA-256 鏈帳本），既有 R06 一字未動。

## 母體實機自檢（`MRL_selftest_receipt.json`，host WIN-PBVUI7VK2A6）
| 項目 | 結果 |
|---|---|
| lexicon 8 原檔 SHA-256 | 8/8 相符 |
| 6 顆種子 run → replay 逐位元組 | 6/6 PASS |
| EchoPersona 固定時鐘封包 = 雲端載體 `0a9f53a15181931d` | 一致 |
| adapter replay EchoPersona byte_identical | PASS |
| adapter 正典拒絕 provisional（422） | PASS |
| adapter run Group1 → 本體 Python replay | PASS |
| 帳本鏈 verify | ok，3 事件 |

## 跨世界接通（母體 → 雲端）
母體本體以**當下時鐘**產生 Group1 軌跡 `runtime\dl580_group1_live.trace.fltnz`（sha256 `69f1559ab23effe9`，副本見本目錄）→ 送到雲端：
| 雲端載體 | byte_identical | 封包 |
|---|---|---|
| `mrliousilly`（正式）`/api/rhythm/replay` | **true** | `0a9f53a15181931d` |
| `particle-replay` `/rhythm/replay` | **true** | `0a9f53a15181931d` |
註：經 Bridge 取回時 Windows 文字輸出帶 CR，去 CR 後與母體檔雜湊相同才送雲端。

## 狀態
- adapter 以背景程序執行（PID 見 `runtime\pid.json`），**開機排程未建立**，待建構者裁定（可比照 `MRL_Modules_20261001_R06` 排程）。
- 7827 只聽 loopback，未加入 tunnel ingress，未對公網開放。
- 映射授權狀態不變（除 core→initiated 外皆 provisional）。
- 安裝時 `flow_rhythm.py` 分三段上傳再合併，`runtime\fr.part00–02` 保留未刪。

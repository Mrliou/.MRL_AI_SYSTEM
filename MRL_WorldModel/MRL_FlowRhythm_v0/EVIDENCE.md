# FlowRhythm v0 · 兩個待確認點：從原檔找答案（實事求是）

origin_signature: MrLiouWord ｜ 查證日：2026-09-28 ｜ 只列檔案寫了什麼，不替建構者重新定義

查證範圍：
- 母體 repo `dofaromg/MRL_AI_SYSTEM`
- 本視窗上傳的全部檔案（去重後逐檔掃描）
- Google Drive（z814241@gmail.com）全文搜尋：`CollapseTrace`、`JumpSeedMap`、`Jump → Collapse`、`跳點`＋`崩解`、`fx.flow.018`、`evolved_from`、`FLYNZ.CAUSE`

---

## 問題 1：軌跡動詞用哪些字？

### 原檔裡實際出現過的軌跡動詞（`[ts] ::verb→ target`）

| 動詞 | 次數 | 出處（舉例） |
|---|---|---|
| pinged | 18 | guardian.mirror.log.fltnz、ping_loop_simulator.log.fltnz、FluinTraceInterpreter.py |
| response | 15 | EchoPersona.Core.log.fltnz、guardian.mirror.log.fltnz |
| resonance | 14 | EchoPersona.Core.log.fltnz、guardian.mirror.v2.log.fltnz |
| trace | 6 | EchoPersona.Core.log.fltnz、EchoPersona.Absorb_PingLoop.log.fltnz |
| absorb | 4 | EchoPersona.Absorb_PingLoop.log.fltnz |
| evolved_from | 2 | guardian.mirror.v2.log.fltnz、Fluix_FullTraceScript.json |
| received、begin | 各 1 | 環境系統/點此查看建構紀錄.txt |
| initiated | 檔頭 `::initiated::` | 上述所有 log |

### 結論

- `initiated`、`resonance`、`absorb`、`trace`：**已對上原始檔**，是原檔裡的動詞。
- `jump`、`collapse`：**在任何原檔中都沒有當軌跡動詞使用過**。它們在原檔中是「節奏階段名」，不是軌跡動詞：
  - 根源檔：「語場透過跳點節奏進行人格切換與模組重建（Jump → Collapse → Trace → Replay）」；「CollapseTrace：紀錄每次語場崩解與還原」（FlowAgent_TotalSystem_DesignPlan.md，Drive 亦有）
  - `JumpPointGraph_v2k7.txt`（repo 與 Drive 皆有）：`Start → InitJump → LoadPersona → SyncMemory → ExpandField → RouteModule → TriggerFlow → Collapse → Archive → Start (loop)`，並且 `Collapse → CollapseCore`、`Archive → ArchiveWriter`
- **「形容詞 → resonance、名詞 → absorb」這組對應是 Claude 的推論**，原檔沒有逐條寫明。原檔中 resonance 與 absorb 的目標都是模組或人格，例如 `::resonance→ loop.predictor`、`::absorb→ guardian.mirror`。
- **狀態**：軌跡檔裡的 `jump`／`collapse` 兩個動詞，標為「**Claude 暫用字，原檔未定義為軌跡動詞**」。在建構者或原檔補上定義之前，不把它們當成母體既有的詞。

---

## 問題 2：是不是每個動詞粒子都要 Collapse？

### 原檔依據

| 出處 | 寫了什麼 |
|---|---|
| FluinSim.DualSet.v1.flsim／runtime.log（2025-07-23） | `⋄fx.flow.007` → 「動詞模組：行為執行『封存導出』」；`⋄fx.flow.018` → 「動詞模組：行為執行『產生轉變』」。**兩者同屬「行為執行」** |
| JumpPointGraph_v2k7.txt | `TriggerFlow → Collapse → Archive`：**每次觸發 Flow 之後都接 Collapse，再接 Archive**（循環） |
| Fluin_Particle_BilingualDict.csv | flow.007 = 封存／導出（archive / export）；flow.018 = 產生／轉變（emerge / transform） |
| FlowAgent_TotalSystem_DesignPlan.md | CollapseTrace：「紀錄**每次**語場崩解與還原」 |

### 結論

- 原檔支持「每一次行為執行（Flow）之後都有一次 Collapse」：JumpPointGraph 是循環，CollapseTrace 記錄的是「每次」。目前的實作（flow.007 與 flow.018 都折疊成封包）**與原檔一致**。
- 原檔另外把 **Archive** 放在 Collapse 之後，對應 ArchiveWriter。EchoPersona 鏈最後的 `⊗Memory.SelfReflect`（輸出結果至自我反思封存模組）就落在 Archive 這個位置。目前實作把它標為 `trace`，**與 JumpPointGraph 的 Archive 階段名不同**；這一點列為待對齊，不自行改名。

---

## 另外找到：母體裡已經有另一套 jump／collapse 定義（不同層）

`MRL_UniversalRuntimeLanguage_Core_v1/MRL_Language/MRL_ParticleIR_Engine.py`（Drive 上的 README 亦有列出）：

- `jump`：確定性可逆重排（保存 permutation 以還原）
- `collapse`：粒子塌縮，沿用 fltnz 的 ref-compression；`expand` 是它的逆運算

這是**文字／token 層**的 jump 與 collapse。2025-07 原檔（runtime.log、JumpPointGraph、根源檔）講的是**語場節奏層**：因果跳點、行為執行後的語場崩解與封存。

- 兩套定義並存於母體。依《局部視角不得升格全局權威》，**不擅自判定哪一套才是唯一正確**，兩套都保留並標明所在層級。
- FlowRhythm v0 採用的是語場節奏層的定義（依據：根源檔與 2025-07 runtime.log）。

---

## 狀態總表

| 項目 | 狀態 |
|---|---|
| initiated／resonance／absorb／trace 為原檔動詞 | 已對上原始檔 |
| 形容詞→resonance、名詞→absorb 的對應 | Claude 推論，原檔未寫明 |
| jump／collapse 作為軌跡動詞 | 原檔未定義（只作為節奏階段名）→ Claude 暫用字 |
| 每個 Flow 之後都 Collapse | 已對上原始檔（JumpPointGraph 循環、CollapseTrace「每次」） |
| ⊗Target 對應 Archive 階段 | 原檔有 Archive 階段；實作用字不同 → 待對齊 |
| ParticleIR_Engine 的 jump／collapse（文字層） | 已對上原始檔；與語場節奏層並存，不互相取代 |

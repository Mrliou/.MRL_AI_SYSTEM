# FlowRhythm v0 · 邊緣載體（edge）

origin_signature: MrLiouWord ｜ 怎麼過去，就怎麼回來 ｜ Additive-Only

1. **本體或載體**：載體。承載本體 `../flow_rhythm.py`（權威），自己不定義語意。
2. **對應哪一段**：Jump → Collapse → Trace → Replay 全程；補上 `src/mrl_worker.js` convergence 裡 `replay_restore_runtime: PENDING` 的邊緣那一段（只補邊緣，不改該狀態）。
3. **驗收語料**：母體 6 顆種子（EchoPersona.pcode／.flpkg、FluinCoreSeed／Memory.Seed.Core .flseed、FluinSim Group1／Group2），與 `tests/test_rhythm.py` E 段相同。

| 檔案 | 作用 |
|---|---|
| `build_lexicon_json.py` | 呼叫 `load_lexicon()` 讀 2025-07 原檔 → `lexicon.v0.2.0.json`；8 個原檔 SHA-256 須與 `../lexicon/SOURCES.sha256` 相符，否則中止 |
| `flow_rhythm.mjs` | JS 版節奏引擎（WebCrypto SHA-256），語義 Gate 與 Python 相同 |
| `conformance.mjs` | JS ⇄ Python 逐位元組驗收（`node conformance.mjs`） |
| `dump_reference.py`、`python_replay_check.py` | 驗收用：Python 出參考值／Python 反向 Replay JS 軌跡 |

Worker 端點（`src/mrl_worker.js`，POST 純文字）：
- `/api/rhythm/run` —— 輸入粒子語句 .fltnz；預設正典 → 遇 provisional 映射回 422
- `/api/rhythm/replay` —— 輸入 v0.2.0 軌跡；回傳 `byte_identical`、封包雜湊
- 加 `?sandbox=1` 才允許 provisional；輸出保留 `PROVISIONAL_NOT_CANONICAL`

## 驗收（當下狀態 2026-10-02，沙盒）

| 項目 | 結果 |
|---|---|
| H. JS run ＝ Python run（軌跡／封包／敘述），6/6 種子 | PASS |
| I. JS Replay 讀 Python 軌跡，逐位元組重現 | PASS |
| J. Python Replay 讀 JS 軌跡（反向） | PASS |
| K. 正典 fail-closed；竄改 status／刪授權行／竄改映射 → 拒絕 | PASS |
| L. v0.1.0 歷史軌跡判為歷史、不當 v0.2.0 Replay；`traces/` 前後雜湊不變 | PASS |
| wrangler dev 本機實跑兩端點（Group1：封包 `0a9f53a15181931d`，邊緣↔Python 雙向一致） | PASS（沙盒本機） |
| Cloudflare 線上部署 | 待部署（先前 API token 驗證失敗，待建構者換新 token） |
| DL580 實機 | 待實機 |

映射狀態沿用 `../EVIDENCE.md`：除 `core → initiated` 外皆 provisional，本載體不改變任何映射授權。

# 07_Capability_Mapper

origin_signature: MrLiouWord ｜ 2026-10-04

## 任務：Asset → Module → Capability → Runtime → Product 映射

能力清單（引自 MRL_Module_Integration_20261001_R06 ＋ R07 新增）：
language, code, reasoning, multimodal, longcontext, tools, math, creative, retrieval, memory, **rhythm**（FlowRhythm，R07 新增）

## Runtime 清單（實機 DL580 當下狀態 2026-10-04）
- 7500 推理 Qwen2.5-32B（人格路由＋記憶檢索）
- 7812 cat vault
- 7800 Bridge v3.1.0（198 PG tables）
- 7825 Module API（19 modules，含 R07 新增 flowrhythm）
- 7826 FlowCore
- 7827 FlowRhythm（loopback，供 7825 toolbox 管線呼叫；本體 flow_rhythm.py v0.2.0）
- 7900 FlowAgent API
- bridge/dl580.mrliouword.com Cloudflare Tunnel（R04 復原）
- Workers: mrliousilly（prod）、particle-replay（SUPPLEMENT_EXISTING）

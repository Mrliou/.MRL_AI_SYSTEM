# 06_CrossRepo_Deduplicator

origin_signature: MrLiouWord ｜ 2026-10-04 ｜ **待 P1 全跑完後觸發**

## 任務
- 跨 repo 以 HEAD sha / commit sha / tree sha 判定鏡像
- fork 群內的子集 - fork 與其 upstream 的差異
- 兩個 owner（dofaromg / Mrliou）同名 repo 的對照
  - 目前已知 13 組同名：bookish-waddle, cfe, claude-cookbooks, claude-honcho, Dropbox, flow-tasks, mrl_ai_os--, MRL_AI_SYSTEM, Mrlcristalina-v4, mrliouword-system, nemori, scylladb, unicornstudio-react

## 現況
P1 只有 1 repo 的 branch 資料；只能偵測到該 repo 內部 HEAD-sha 共用（38 組）。跨 repo 偵測必須等 P1 補完 499 repo 後執行。

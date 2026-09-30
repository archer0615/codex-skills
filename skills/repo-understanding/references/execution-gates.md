# Tool and Skill Execution Gates

工具或 Skill 可用不等於應執行。每次操作前都要在 `toolchain-utilization.md` 記錄：

```text
Tool / Skill | Claim or Gap | Preconditions | Expected Evidence / Artifact | Minimum Scope | Execute / Skip / Blocked | Reason
```

僅在有明確 claim/gap/target、工具可用且不需未授權操作、結果可驗證、以及沒有更低成本 primary evidence 時執行。每次操作後補：

```text
Command / Query | Result Reference | Evidence Delta | Verification | Next Action
```

Evidence Delta 只能是 CONFIRMED、REFUTED、GAP REDUCED、SCOPE NARROWED 或 NO MATERIAL GAIN。最後一種禁止在 revision、輸入、target 或診斷未變時重跑相同工具／scope；改用不同證據或記錄 UNKNOWN/BLOCKED。兩輪未減少 material gap 必須停止。

專屬 gate：analyze 僅在 index 缺失/stale/重大結構變更，且預設不用 embeddings/PDG/watch/group sync；GitNexus 查詢一個決策問題一次；impact/detect_changes 僅用於可識別 diff；PDG 僅在控制／資料依賴需求明確且層已建立；onboarding 在 FULL 建立一次、Incremental 僅更新受影響區段；Archify 需先有 Diagram Inventory 與 evidence，且不預設匯出靜態格式；其他 Skill 先讀其 SKILL.md，僅處理專屬問題。

DONE 前稽核：每個適用工具／Skill 都須有 EXECUTED、SKIP、NOT APPLICABLE 或 BLOCKED；每筆 EXECUTED 都必須有 precondition、expected result、result reference、evidence delta 和 verification，否則為 UNVERIFIED。抽樣回放 ledger、檢查無理由重複呼叫為 0、以故意無結果 query 驗證不重跑、並確認高成本選項沒有明確收益時被 SKIP。

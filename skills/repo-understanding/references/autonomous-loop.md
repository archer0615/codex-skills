# Autonomous Loop

依序執行：`SCOPE → CAPABILITY/GATE SELECTION → (INDEX when useful) → DISCOVER → EVIDENCE → IMPACT (when applicable) → DOCUMENT → VISUALIZE (when applicable) → SEMANTIC VALIDATE → COVERAGE → UTILIZATION → FINAL VERIFY`。Multi-repository mode 先固定 inventory，再逐 repository 完成 scope-relevant evidence 和 coverage，最後才建立由雙方證據支持的跨-repository contracts、flows 與 diagrams。跳過 gate 時記錄 `SKIP`／`NOT APPLICABLE` 和理由；不可把工具存在當成執行要求。

每次操作先依 `execution-gates.md` 記錄 precondition、預期收益與最小 scope，結束後記錄 result reference、evidence delta 與 verification。依 `resume-and-checkpoint.md` 在 phase/gate 完成、BLOCKED 前與 final verification 後更新 run-state。每完成一項可驗證工作，重新評估是否仍有：可安全補證的 CRITICAL/HIGH 缺口、未解釋的 material index/architecture/flow gap、STALE 或 NEEDS VERIFICATION 產物、或未執行的適用 gate。若有，僅處理最高 materiality 的最小範圍，再進入下一輪。

在下列情況停止：

- 所有適用且必要的 acceptance gate 通過、`STALE = 0`，且沒有未解釋的 CRITICAL/HIGH gap：DONE；未使用的 optional gate 不影響完成。
- 剩餘項目全是具體證據支持的 NOT APPLICABLE/BLOCKED：完成並列出限制。
- 需要授權、憑證、不可逆操作或無法安全界定影響：BLOCKED。
- 連續兩輪未減少任何 material gap：停止並回報已做的檢查、證據與需要的決策；不可宣告 DONE。

GitNexus 結論一律以原始碼、設定、測試與 runtime 證據交叉驗證。FULL 覆蓋實際存在的入口、模組、對外介面、資料邊界、整合、背景工作、錯誤、測試與部署；Incremental 僅處理 diff/impact 證明受影響或 stale 的產物。

# Knowledge Base and Coverage

優先使用 repository 的既有文件慣例；若沒有，建立 `docs/repo-understanding/`，包含 dashboard、profile、architecture、flows、modules、evidence model、gitnexus coverage、architecture coverage、diagram coverage、gaps、toolchain utilization 與 `diagrams/`。圖表數量與 scope 規則依 `diagram-coverage.md`，GitNexus 掃描限制與查詢證據依 `gitnexus-coverage.md`。

每個重要 claim／圖表元素記錄：Status、Primary evidence（path + symbol/config/test/runtime）、GitNexus supporting evidence、Evidence type、Last verified revision、Artifact state（CURRENT/STALE/NEEDS VERIFICATION）。沒有來源的內容不得寫成 CONFIRMED。

在 coverage matrix 維護：

```text
Area / Flow | Exists | Primary Evidence | GitNexus Coverage | Documentation | Diagram | Semantic Validation | Last Verified | Staleness | Status
```

驗證至少包括：

1. 原生檔案清單與 index reconciliation；每個預期來源分類為 indexed、excluded、unsupported、generated、ignored 或 unexplained。
2. 每個實際存在的入口、模組、對外介面與資料／外部邊界都有 primary evidence 與文件定位。
3. 重要 trigger 可追至 handler、orchestration 與 side effect；中斷點需有原因。
4. 以 diff、detect_changes、impact 判定受影響文件與圖表，更新 STALE 並驗證 NEEDS VERIFICATION。
5. 圖表語意驗證：workflow 包含 entry/exit、分支、失敗、retry/fallback；sequence 包含 participant、順序、回傳、條件、loop、error。Archify renderer 通過不取代語意驗證。

PASS 表示沒有未解釋的 material gap，不代表所有檔案都可被 GitNexus 解析。

Multi-repository system 的 repository-level artifacts 留在各 Git root；system root 使用 `docs/repository-understanding-system/` 放置 inventory、architecture、integration contracts、cross-repository flows、evidence model、coverage、gaps、ledger 與 system run state。系統 claim 必須包含 repository IDs、revisions 與雙方 primary evidence。

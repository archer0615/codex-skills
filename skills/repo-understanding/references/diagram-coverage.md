# Diagram Coverage

以「獨立 scope」而不是「每種 Archify 類型一張」決定圖表數量。先從已確認 Evidence Model 建立 Diagram Inventory：

```text
Diagram ID | Type | Scope / boundary | Primary evidence | GitNexus evidence | Related document | Status
```

scope 是可獨立理解與維護的責任邊界，例如付款整合、結帳請求鏈、訂單狀態機。只要同類型候選 scope 的責任邊界、主要證據、entry/external participant、資料邊界或狀態機不同，就必須產出不同 artifact；不可把多個獨立 scope 塞入一張巨型圖。

對每個 scope 分別判定適用類型：component/service/integration boundary 用 `architecture`；有決策、失敗或 retry 的程序用 `workflow`；request/RPC/event chain 用 `sequence`；資料來源至消費者的路徑用 `dataflow`；獨立狀態轉移規則用 `lifecycle`。同一 scope 可以有多種類型；僅在內容完全重複且沒有額外維護價值時才省略，並記錄原因。

每個確認項目需有獨立 spec、已 deliver 的 HTML、receipt、primary/supporting evidence、semantic validation、Last Verified 與 `CURRENT`／`STALE`／`NEEDS VERIFICATION`。圖片匯出僅在使用者要求時產生。將結果記錄在 `diagram-coverage.md`：

```text
Diagram ID | Type | Scope / Boundary | Primary Evidence | GitNexus Evidence | Artifact | Semantic Validation | Last Verified | Staleness | Status
```

Diagram coverage 通過前，所有重要 scope 都必須有適用性判定；每個應產出的 scope/type 組合要有 artifact，或有具體 `NOT APPLICABLE`／`BLOCKED` 原因。Incremental 使用 `detect_changes`／`impact` 判定受影響圖表並重新驗證。

# 可丟棄驗證 Fixture

此目錄用來驗證 Repository Understanding 的控制流程，不是要被模板本身分析的正式應用程式。請將它複製到暫存位置後再操作，避免其 Git 狀態或產物污染本模板。

## Fixture 設計

- `src/app.js` 有兩個 HTTP 入口：`POST /orders` 與 `POST /refunds`。
- 每個入口各自通往 service 與 repository，因此兩個 sequence scope 必須分開盤點與產圖，不能只用一張泛稱的 API sequence。
- 測試只依賴 Node 內建模組，不需要安裝 `express`；靜態掃描可讀取 `app.js`，而 runtime app 啟動則應因未安裝依賴被如實記為未驗證。

## 建立隔離 target

1. 將本目錄複製到一個暫存資料夾，例如 `<temp>/resume-fixture`。
2. 在該資料夾執行 `git init`、`git add .`、`git commit -m "fixture baseline"`。
3. 先將本 Plugin 的 `skills/repo-understanding/` 安裝到測試用 Codex Skills 目錄，再在 fixture 根目錄啟動 `$repo-understanding`；不要複製 portable workflow 或覆寫 fixture 的既有規則。
4. 執行 `node --test`，確認 service/repository 的靜態可驗證基線可運作。

## 驗證案例

| 案例 | 操作 | 預期可驗證結果 |
| --- | --- | --- |
| 首次執行 | 輸入 README 的「第一次執行」指令 | 建立 Source Identity、Capability Profile、execution ledger 與知識庫產物；`/orders`、`/refunds` 都有 primary evidence。 |
| 相同 checkpoint 續跑 | 不改檔案，輸入「後續續跑」指令 | 已完成且 CURRENT 的 gate 被跳過，只處理 `Next Minimal Action` 或 pending gap。 |
| staged 變更 | 修改並 `git add src/order-service.js` 後續跑 | Working Tree Identity 改變；只將 order flow 相關文件、圖表與測試標成需驗證，再以 impact 縮小範圍。 |
| unstaged 變更 | 修改 `src/refund-repository.js` 但不 stage 後續跑 | Working Tree Identity 改變；refund flow 成為受影響範圍。 |
| relevant untracked | 新增 `src/notification-worker.js` 後續跑 | untracked inventory 改變；新增 worker 的來源與圖表需求被盤點。 |
| GitNexus 或 Archify 缺失 | 在工具不可用的環境執行 | 對應列為 `BLOCKED / USER AUTHORIZATION REQUIRED`，不假裝建立 index 或圖表；啟用工具後續跑時只補該列。 |
| 多圖 scope | Archify 可用且 evidence 已確認時產圖 | `diagram-coverage.md` 至少有 order sequence 與 refund sequence 的獨立 scope/artifact，或記錄具體 BLOCKED／NOT APPLICABLE 原因。 |

## 判定方式

每個案例都檢查 `run-state.md` 的 revision 與三個 Working Tree Identity 欄位、`toolchain-utilization.md` 的 evidence delta，以及 coverage 文件的 `CURRENT`／`STALE`／`BLOCKED` 狀態。不要只以「GitNexus index 成功」或「有一張圖」判定通過。

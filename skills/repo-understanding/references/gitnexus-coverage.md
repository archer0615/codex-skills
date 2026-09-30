# GitNexus Coverage

GitNexus index 存在不等於 repository 已被充分理解。Bootstrap 必須從副檔名、manifest、build/workspace 設定建立 Capability Profile：

```text
Language / Framework / Package | Detection Evidence | GitNexus Support | Required Queries | Fallback Evidence | Status
```

偵測後才補證：.NET 檢查 route/DI/host/EF/test；JVM 檢查 entry/Controller/config/persistence/event，可信本地 Actuator snapshot 才考慮 `--spring-actuator`；前端檢查 package 邊界、route、API client、entry/build/test；Python 檢查 route、worker、configuration、migration/test；monorepo 必須逐一清點 app/service/worker/library。

Multi-repository system 逐 repository 建立 index 與 reconciliation；不得從一個 repository 的 index 推論另一個 repository 的 coverage 或 impact。跨 repository edge 必須以雙方 source/config/contract evidence 交叉驗證，並在系統 coverage 記錄兩端 revision。

以原生 inventory 對照 index，將每個預期來源分類為 indexed、excluded、unsupported、generated、ignored 或 unexplained。material unexplained 不可 PASS。對動態 route/DI/reflection/ORM/plugin、generated client、feature flag、環境或外部服務，使用設定、測試、可信 runtime snapshot 或文件補證；沒有證據即 UNKNOWN，不能以 graph 缺少邊線推論不存在。

依適用性記錄最小查詢：context/clusters（模組）、processes/query/trace（流程）、route_map/tool_map/api_impact（介面）、detect_changes/impact（Incremental）、pdg_query/explain（只有 --pdg 且需要資料／控制依賴時）、check（結構健康）。每筆 query 要保留目標、結果與 primary evidence；無結果需區分不存在與索引限制。

驗證此規則時：先完成 inventory reconciliation；對已知入口用 process/trace/context 與 source 逐段交叉驗證；每個 framework 抽樣驗證一項 profile 補證；在安全分支或 disposable fixture 做小型變更，確認 detect_changes/impact 將對應知識產物標為 NEEDS VERIFICATION；再用已知動態／不支援行為進行負向測試，確認它被標為 UNKNOWN/unsupported 而非錯誤 CONFIRMED。

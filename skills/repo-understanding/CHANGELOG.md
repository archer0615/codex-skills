# Changelog

## 2.1.0

- 將 GitNexus、Node、npm 與 Archify 改為依接受範圍和 gate 條件判斷，不再由工具缺失一律阻擋整份分析。
- 明確區分 source-based knowledge work、graph supporting evidence、Node runner、專案依賴安裝與 diagram gate。

## 2.0.0

- 從基本掃描升級為 evidence-backed、可續跑的 onboarding workflow。
- 新增 FULL/INCREMENTAL/RESUME/FINAL-VERIFY、scope/evidence/artifact freeze 與 persistent inventories。
- 強化跨 repository route/service/batch/CAAS、動態設定與未知證據標示。
- 新增 Archify 多 scope 拆圖、索引與驗證規則，以及 Windows fallback 原則。
- 保留不修改 application/production/remote Git、不安裝未知工具的安全邊界。

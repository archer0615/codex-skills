# Codebase Onboarding 整合契約

本文件將 `codebase-onboarding` 的核心能力整合進 `repo-understanding`，不是第二個可獨立安裝的 Skill。唯一真實來源仍是上層的 `SKILL.md`。

## 角色分工

- GitNexus：提供 repository graph、call chain、process、route、trace、impact 與 change evidence。
- Codebase Onboarding：將已驗證的證據整理成可供人類與 Agent 使用的專案地圖。
- Archify：只將已確認的元件、流程、資料邊界與狀態轉成圖表。
- Repository Understanding：管理 scope、run-state、coverage、evidence ledger、freshness 與安全 gate。

Codebase Onboarding 不可自行建立另一個事實來源，也不可用推測取代 primary evidence 或 GitNexus evidence。

## 分析輸入

依序檢查並交叉比對：

1. `AGENTS.md`、既有開發規則、README、security 與 contribution 文件。
2. manifests、lockfiles、workspace 設定與 runtime version。
3. application startup、routes、commands、workers、jobs 與公開介面。
4. 排除 dependency、cache、build、generated 與 VCS 目錄後的淺層目錄結構。
5. container、environment、task runner、bundler、deployment 與 service 設定。
6. tests、lint、type-check、build、fixtures 與 CI workflow。
7. Git 歷史；若歷史不足，明確標示不可由歷史確認。

可使用 GitNexus 結果縮小候選範圍，但每個重要結論仍需回到原始碼、設定、測試或 runtime 證據。

## 必須產出的專案地圖

至少涵蓋：

- Purpose：repository 做什麼、誰或什麼會使用它。
- Stack and boundaries：語言、framework、runtime、package／service 邊界。
- Architecture and request flow：至少一條代表性流程，包含入口、驗證、協調／domain、資料或外部依賴、回應／副作用。
- Key entry points：實際檔案路徑與角色。
- Conventions：區分 documented rule、observed convention、local exception、unknown。
- Verification：快速檢查、完整檢查、前置服務、憑證、容器與授權需求。
- First-change map：功能、API、schema、測試與 generated file 應從哪裡開始。
- Unknowns and risks：無法由證據確認的內容與影響。

每個重要段落都要記錄 primary evidence；可以同時附 GitNexus supporting evidence，但不能只引用圖譜結果。

## 產物與去重規則

若 target 使用預設知識庫，將 onboarding 內容放在 `docs/repo-understanding/` 的既有 `index`、`profile`、`architecture`、`flows`、`modules` 與 `gaps` 產物中。不要另外建立未受 run-state 與 coverage 管理的 `wiki/`。

若 target 已有明確的 onboarding 文件，先更新既有文件；除非使用者要求，不能建立重複的 `AGENTS.md`、`CLAUDE.md` 或 onboarding wiki。

## 品質與安全門檻

- 沒有證據的結論標記為 `NEEDS VERIFICATION` 或 `[NEEDS INVESTIGATION]`。
- 不把 manifest 中存在的 dependency 當成實際使用中的架構元件，除非程式碼或 runtime 證明。
- 不讀取整個 repository 到 context；使用針對責任的抽樣與 GitNexus 導航。
- 不臆造 build、test、migration、deployment 或安裝命令。
- 不執行 heavyweight build、container、migration、付費 API、production 操作，除非使用者明確授權且 gate 需要。
- onboarding 產物完成後，回寫 coverage、evidence、revision 與 staleness；不能只以文件產生成功宣告 DONE。


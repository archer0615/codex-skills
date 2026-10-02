# Dependency Contract

`repo-understanding` 的依賴以 repository 的 `toolchain.json` 為 authoritative manifest。AI 不得只依賴記憶或作業系統慣例判斷套件是否存在。

## 依賴表

| Capability | Required for | Detection | Missing action | Install policy |
|---|---|---|---|---|
| Python 3.9+ | 所有初始化與驗證腳本 | `python --version` | 停止腳本流程並回報環境阻塞 | `user-authorized` |
| Git | repository identity 與 diff | `git --version`、`git status` | 降級為 source-only，標記 `UNVERIFIED` | `user-authorized` |
| GitNexus >= 1.6.12 | 完整 graph/process/route/trace/impact | `gitnexus --version` 與 runner 檢查 | 跳過受影響 gate，回報 `BLOCKED` 或 `PARTIAL` | `user-authorized` |
| Node >= 18 | Node runner 與 runtime verification | `node --version` | 跳過 Node-specific gate，保留 source evidence | `user-authorized` |
| npm >= 9 | 已宣告 project dependency install | `npm --version` | 不執行 npm install，標記 `BLOCKED` | `user-authorized` |
| codebase-onboarding | project map 與 first-change guide | 檢查 bundled reference | 若本 Skill 完整，直接使用內建能力 | `bundled` |
| archify | architecture/workflow/sequence/lifecycle diagrams | 依 `test-archify.py` 與 Skill 路徑檢查 | 跳過 diagram gate，標記 `BLOCKED` | `user-authorized` |

## 修復規則

預設只執行 audit 與 version check。缺少能力時先報告，不自動下載或修改使用者環境。只有使用者明確授權後，才可依平台與官方／專案指定方式安裝；安裝完成必須重新執行 detection 與受影響測試。

若 target repository 有自己的 lockfile 或 bootstrap，優先遵循 target 的 package manager 與 lockfile；不要以全域安裝取代 project-managed dependency。若沒有可靠的 repair command，回報 `manual`，不要自行發明安裝命令。

完整分析只有在所有適用 required capability 通過檢查時才可標記 `DONE`；否則使用 `PARTIAL` 或 `BLOCKED`。

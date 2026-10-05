# Dependency Contract

`repo-understanding` 的依賴以 repository 的 `toolchain.json` 為 authoritative manifest。清單中的工具是特定 gate 的依賴，不是每次執行的整體前置條件。AI 不得只依賴記憶或作業系統慣例判斷套件是否存在，也不可因工具存在就預設執行。

## 依賴表

| Capability | Required for | Detection | Missing action | Install policy |
|---|---|---|---|---|
| Python 3.9+ | 執行本 Plugin 的 Python 初始化／驗證 scripts | `python --version` | 只阻擋相關 script；可用原生檔案檢查時保留其證據 | `user-authorized` |
| Git | 需要 revision、diff、工作樹 identity 或 Git history 的檢查 | `git --version`、`git status` | 省略 Git 衍生證據，標為 `UNVERIFIED`／`NOT APPLICABLE`；source-based 分析可繼續 | `do-not-install` |
| GitNexus >= 1.6.12 | 使用者要求或 material gap 需要 graph/process/route/trace/impact supporting evidence 時 | `gitnexus --version` 與既有 runner/index 檢查 | 若非驗收必要，記錄 `SKIP`／`OPTIONAL MISSING` 並以 primary source 繼續；若是明確必要 gate，僅該 gate 為 `BLOCKED`／`PARTIAL` | `user-authorized` |
| Node >= 18 | 使用需要 Node 的 runner，例如執行 Archify | `node --version` | 只阻擋依賴 Node 的 gate | `user-authorized` |
| npm >= 9 | 使用者明確要求且 target 有對應 lockfile 的 dependency install | `npm --version` | 不安裝；僅在依賴安裝是驗收必要條件時阻擋該 gate | `user-authorized` |
| codebase-onboarding | repository map 與 first-change guide | 檢查 bundled reference | 已隨本 Skill 內建 | `bundled` |
| archify | 使用者要求或驗收明確需要 diagrams 時產生／驗證 diagrams | 依 `test-archify.py` 與 Skill 路徑檢查 | 無圖表需求則 `NOT APPLICABLE`；有明確圖表 gate 時只將該 gate 標為 `BLOCKED`／`PARTIAL` | `user-authorized` |

## 修復規則

預設只執行 audit 與 version check。缺少能力時先報告，不自動下載或修改使用者環境。只有使用者明確授權後，才可依平台與官方／專案指定方式安裝；安裝完成必須重新執行 detection 與受影響測試。

若 target repository 有自己的 lockfile 或 bootstrap，優先遵循 target 的 package manager 與 lockfile；不要以全域安裝取代 project-managed dependency。若沒有可靠的 repair command，回報 `manual`，不要自行發明安裝命令。

依使用者要求的 scope 和 acceptance criteria 判斷完成度。所有適用且必要的 acceptance gate 完成即可標記 `DONE`；對非必要工具標記 `SKIP`／`NOT APPLICABLE`，其缺少不會自動使整體成為 `PARTIAL`。只有明確要求或必要 gate 未完成時才回報 `PARTIAL`／`BLOCKED`，並指出受影響範圍。

# AI 使用與依賴處理指南

本文件是提供給使用者與 AI 的操作契約。每個 Skill 的唯一行為來源仍是該 Skill 目錄下的 `SKILL.md`；本文件只說明共通的安裝、依賴檢查與缺失處理方式。

## 使用 Skill

在 Codex 中以 `$skill-name` 明確啟用，例如：

```text
使用 $repo-understanding 分析目前 repository，先做環境稽核，不要修改環境。
```

AI 必須先讀取該 Skill 的 `SKILL.md`，再依其中列出的 references、scripts 與驗收條件執行。

## 每個 Skill 的依賴契約

新增或修改 Skill 時，應在該 Skill 的 `SKILL.md` 或其 references 中列出：

| 欄位 | 說明 |
|---|---|
| Name | 套件、命令、Skill 或整合能力名稱 |
| Kind | `python-runtime`、`command`、`python-package`、`node-package`、`codex-skill` 或 `integrated-capability` |
| Required | `required` 或 `optional` |
| Version | 最低版本或相容範圍；無法確認時標示 `unknown` |
| Purpose | 缺少時會影響哪個功能 |
| Detection | AI 或 script 如何檢查它 |
| Install policy | `bundled`、`user-authorized`、`project-managed` 或 `do-not-install` |
| Repair command | 只有在取得授權後才可執行的修復命令；沒有就填 `manual` |

依賴不可只寫「請安裝相關套件」，必須說明檢查方式、影響範圍與授權邊界。

## 缺少依賴時的決策流程

1. 先執行只讀檢查，確認命令、版本、檔案或 Skill 是否真的不存在。
2. 將結果分成：
   - `READY`：必要依賴存在且版本符合。
   - `OPTIONAL MISSING`：可繼續執行，但功能或證據覆蓋率下降。
   - `BLOCKED / USER AUTHORIZATION REQUIRED`：必要依賴缺少、需要下載、安裝、權限、憑證或外部服務。
   - `UNVERIFIED`：環境無法可靠判斷，不能假設已存在。
3. 只對 `READY` 的 gate 執行工作；對其他 gate 保留缺失證據與影響。
4. 不得因缺少工具而臆造結果，也不得把工具錯誤當成專案架構結論。
5. 若修復需要安裝或修改環境，先回報：缺少什麼、為何需要、將執行什麼、會改變哪裡；等待使用者明確授權。
6. 授權後才執行 Skill 定義的 repair command，完成後重新檢查，不得直接宣稱成功。

## 本 Plugin 目前的依賴

`toolchain.json` 的 `requiredCapabilities` 是 task-scoped gate 能力清單；依賴名稱列在此處，不代表所有工作都需要安裝或執行它們。

- Python 3.9+：只在執行本 Plugin 的初始化／驗證腳本時需要。
- Git：在需要 revision、diff 或工作樹身分時需要；沒有 Git 時改標相關證據未驗證，source inspection 可繼續。
- GitNexus 1.6.12+：只有 graph supporting evidence 或 GitNexus impact gate 符合使用條件時需要；source-based onboarding 不會因此自動阻塞。
- Node 18+：執行需要 Node 的選用 runner 時需要，例如 Archify。
- npm 9+：只在使用者要求、target manifest/lockfile 支援且已授權安裝專案依賴時需要。
- `codebase-onboarding`：隨 `repo-understanding` 內建，不需額外下載。
- `archify`：僅在圖表屬於使用者要求或驗收範圍時需要；其他情形標示 `NOT APPLICABLE`／`SKIP`。

工具缺少時只影響需要它的 gate。只有該 gate 是接受條件且未完成，才將結果標為 `PARTIAL`／`BLOCKED`；不可因可選工具缺少而把整次 source-based 分析判為失敗。

本清單以 `toolchain.json` 為準；若兩者不一致，AI 必須回報 manifest drift，不得自行猜測。

## 安裝與修復的安全邊界

- 預覽、audit、version check 是只讀操作，可先執行。
- `--apply`、`--force`、npm install、下載外部工具、修改 PATH 或使用憑證，都必須有明確授權。
- 不執行 commit、push、merge、deploy 或 production 修改。
- 任何修復都必須遵循 `Identify → Fix → Re-verify`，並報告實際命令與結果。

## AI 最終回報格式

以下詳細格式適用於執行環境稽核、初始化、依賴修復，或使用外部工具／能力 gate 的任務。一般 Skill 工作依其 `SKILL.md` 與全域自訂指示回報實際修改、驗證及限制；若沒有外部依賴或 gate，不必建立空白狀態表。

適用上述依賴流程時，至少回報：

- 使用的 Skill 與版本
- 依賴狀態表與檢查命令
- 已執行的 gate
- `READY`、`OPTIONAL MISSING`、`BLOCKED`、`UNVERIFIED` 項目
- 是否修改環境，以及是否取得授權
- 驗證結果與仍未解決的限制

---
name: repo-understanding
description: "Run evidence-backed repository onboarding for a repository, monorepo, or explicitly scoped multi-repository system, including GitNexus reconciliation, API/flow tracing, Archify diagrams, resumable knowledge-base artifacts, and final verification."
---

# Repo Understanding

建立或更新以證據為核心、可續跑的 repository onboarding 知識庫。完整規則在 [Evidence-backed workflow](references/evidence-backed-workflow.md)；本入口只保留路由與安全邊界。所有結論仍以原始碼、設定、測試與可用 runtime 證據為準，GitNexus 僅作 supporting evidence，Archify 只能使用已建檔的證據。

支援 `FULL`、`INCREMENTAL`、`RESUME`、`FINAL-VERIFY` 四種模式。每次執行都必須維護 run-state、execution log、scope/evidence/artifact inventory、pending gaps 與 blocked items；開始正式產圖前必須完成 Scope Freeze、Evidence Freeze、Artifact Plan 與 Feature Boundary Review。

此 Skill 不修改 application logic、production、部署資源或 remote Git，不 commit/push/deploy，不自行安裝未知工具；只可更新本 Skill、knowledge base、diagram spec/HTML、verification artifacts、測試與文件。工具失敗必須保留證據並標為 `BLOCKED` 或 `UNKNOWN`，不可當成架構結論。

## Start

1. 讀取 repository 的 `AGENTS.md` 與其他既有開發規則。
2. 先執行 [Environment preflight](#environment-preflight)；若 target 有初始化／稽核腳本，依平台選擇並記錄結果，不要直接猜測工具是否可用。
3. 依 [System scope](references/system-scope.md) 與 [Bootstrap](references/bootstrap.md) 偵測單一 repository、monorepo 或多 repository system scope；沒有 manifest 時，multi-repository candidates 必須先由使用者確認。逐 repository 檢查 Git 狀態、GitNexus、整合的 Codebase Onboarding 能力與 index 新鮮度，並依 [GitNexus coverage](references/gitnexus-coverage.md) 建立 Capability Profile。執行 onboarding 時必讀 [Codebase Onboarding integration](references/codebase-onboarding.md)。
4. 依 [Resume and checkpoint](references/resume-and-checkpoint.md) 讀取既有工作狀態並選擇 `RESUME`、`FULL`、`INCREMENTAL` 或 `FINAL-VERIFY`。首次執行、缺少可信 baseline/index 或影響範圍不安全時使用 FULL；FINAL-VERIFY 不重新分析，只驗證既有產物。
5. 依 [Execution gates](references/execution-gates.md) 判定每個工具／Skill 是否值得執行，再依 [Autonomous loop](references/autonomous-loop.md) 建 index、蒐集證據、產出文件／圖表並執行 gate。
6. 依 [Knowledge base](references/knowledge-base.md) 記錄產物、覆蓋率、證據與新鮮度；產圖前必讀 [Diagram coverage](references/diagram-coverage.md)，以 scope inventory 決定同類型圖表數量。若 target 沒有既有文件格式，可從 `assets/output-templates/` 複製需要的骨架；不可覆寫既有文件或將範本內容當成證據。

## Deterministic helpers

若 target 需要可重複的準備或驗證，優先使用 scripts，而不是把固定檢查重新寫在對話中：

- `scripts/prepare-knowledge-base.py`：預覽或建立 `docs/repo-understanding/` 的非破壞性文件骨架；預設不寫入，套用需 `--apply`。
- `scripts/validate-knowledge-base.py`：檢查必要 coverage、run-state、toolchain 文件與未完成標記。
- `scripts/organize-knowledge-base.py`：整理 dashboard 的文件與圖表連結，不搬移或覆寫知識庫內容。
- `scripts/run-repo-understanding.py`：串接 prepare、可選的 GitNexus analyze、organize 與 validate；AI 仍負責證據與語意階段。
- `scripts/test-archify.py`：尋找 `$CODEX_HOME`、`.agents` 或 `.codex` 的 Archify，執行 `doctor` 與隔離的 `demo`。

這些 helpers 只驗證可決定的檔案與工具狀態，不代替 AI 的證據判斷、流程追蹤或語意驗證。

若 target 包含 bootstrap，先以不含 `--apply` 的命令預覽；只有使用者明確要求修正 npm 設定時才使用 `--repair-npm-prefix`。安裝／更新 bundled Skill 時尊重 `CODEX_HOME`，若目的地已有不同內容，必須使用者明確指定 `--force` 才覆蓋；不可把這個例外延伸至下載未宣告的 runner 或 Skill。

## Environment preflight

AI 必須先判斷目前作業系統與 Python 3.9+ 是否可用，再執行下列跨平台腳本：

| Environment | Audit | Initialization |
| --- | --- | --- |
| Windows／macOS／Linux | `python scripts/audit.py` | `python scripts/init.py` |

Preflight 必須記錄：

- Plugin、toolchain、SKILL.md、`agents/openai.yaml` 是否存在
- Skill 引用的 references 與 assets 是否存在
- `CODEX_HOME` 或預設 Codex 目錄
- Skill 是否已安裝、是否為相同版本
- Git、Node、npm、GitNexus runner 是否可用
- 內建 Codebase Onboarding 整合與 Archify 是否已存在
- 是否有 package.json／lockfile 可供專案依賴驗證

AI 必須將結果分類：

| Status | Meaning | Action |
| --- | --- | --- |
| `READY` | 必要來源與 Skill 已就緒 | 繼續 Bootstrap |
| `NEEDS INITIALIZATION` | Skill 尚未安裝或版本不同 | 先提供 init 預覽，等待 `--apply` 授權 |
| `OPTIONAL MISSING` | 可選工具缺少 | 記錄影響，不自行下載 |
| `BLOCKED / USER AUTHORIZATION REQUIRED` | 需要安裝、權限、憑證或外部狀態 | 停止受影響 gate，明確回報 |

預設只執行 audit／預覽。只有使用者明確要求初始化、套用或安裝時，AI 才能執行 `--apply`。初始化完成後必須依序執行 Skill validator、bootstrap smoke test，以及 target 提供的可用 Bridge smoke test；任何失敗都要回到 `Identify → Fix → Re-verify`。

若 target 沒有上述腳本，AI 不得自行建立或下載替代初始化器；改以原生 inspection 回報 `UNVERIFIED` 或 `BLOCKED`。

## Tool routing

- GitNexus：依 `gitnexus-coverage.md` 完成 index reconciliation、clusters、processes、routes、context、trace、impact、detect_changes；只在適用時使用 PDG。
- `codebase-onboarding`：使用本 Skill 內建的整合契約，從已驗證證據建立專案地圖、入口、慣例與 first-change guide；不得另建第二個 Skill 或獨立 wiki 事實來源。
- Archify：僅將已確認的元件、流程、資料邊界或狀態轉為 architecture、workflow、sequence、dataflow、lifecycle 圖；同類型的獨立 scope 必須產出不同 artifact。

完整分析的 required capabilities 是 target／toolchain 宣告的 GitNexus、Node、npm、內建 Codebase Onboarding 與 Archify。能力 profile 必須逐 repository 記錄 index revision、parsed file count、symbol/flow count、index/context/routes/processes/trace/impact/detect_changes、FTS/VECTOR/PDG、Terraform/HCL parser、排除範圍、失敗原因與 source fallback。Windows native extension、code page、FTS/VECTOR 失敗時只有限次相容模式嘗試，之後保留錯誤並改用 graph/source/config/test。

完整分析的 required capabilities 是 target／toolchain 宣告的 GitNexus、Node、npm、內建 Codebase Onboarding 與 Archify。內建 Codebase Onboarding 不需要額外下載；若 GitNexus、Node、npm 或 Archify 未就緒，先確認是否已有可用替代 runner；若執行將導致下載或安裝，回報 `BLOCKED / USER AUTHORIZATION REQUIRED` 並停止受影響 gate。不要將工具缺失誤報為 repository 的架構結論，也不要臆造未驗證的套件來源或安裝命令。

最終回報模式、revision／影響範圍、產物位置、各 gate 結果、required capabilities、STALE 數量及 BLOCKED 項目。只有所有適用 required capabilities 已 READY，且達到 reference 定義的 DONE 條件時才宣告完整完成；否則回報 PARTIAL 或 BLOCKED。

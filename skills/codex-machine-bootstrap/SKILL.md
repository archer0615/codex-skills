---
name: codex-machine-bootstrap
description: "Initialize and diagnose a local Codex installation on a new or repaired computer by discovering tools, creating user-level Codex guidance, preserving existing settings, and verifying the shell environment. Use for first-time Codex setup or environment repair; do not use for project-specific build instructions or cloud-only Work environments."
metadata:
  short-description: Initialize and diagnose a local Codex machine
---

# Codex Machine Bootstrap

在新電腦第一次準備使用 Codex，或既有電腦發生「工具找不到／PATH 不一致」時，建立可重複、可驗證的本機初始化流程。

## Scope

- 只處理本機 Codex 的使用者層設定與工具診斷。
- 不把任何特定專案、絕對路徑、帳號、Token、Secret、雲端憑證或固定版本寫入共用設定。
- 專案版本需求以專案自身的 `package.json`、lockfile、`pom.xml`、`build.gradle`、wrapper 與 `AGENTS.md` 為準。
- ChatGPT Work 的雲端環境不會自動讀取本機 Codex 設定；本 Skill 針對本機 Codex、CLI 或 IDE Extension。

## Modes

1. **Preview**：讀取現況並列出將建立或更新的檔案，不修改資料。
2. **Initialize**：使用者明確要求初始化後，建立 `AGENTS.md`、`config.toml` 與環境盤點檔；既有檔案必須先備份或明確使用 force。
3. **Doctor**：唯讀檢查工具路徑、版本、PATH、專案標記與可用 wrapper。
4. **Maintain**：重新執行 Doctor，依專案文件更新專案層規則；不要因單一案例擴張全域規則。

## Required workflow

### 1. Inspect

先確認：

- 作業系統與 shell。
- `CODEX_HOME`；未設定時使用使用者預設 Codex 目錄。
- 現有全域 `AGENTS.md`、`AGENTS.override.md`、`config.toml` 與 inventory。
- `Get-Command`／`where.exe` 或 `shutil.which` 找到的工具。
- 目前專案 root、Git root、README、`AGENTS.md`、lockfile、build manifest 與 wrapper。

不得把 shell 找不到命令直接當成未安裝；先區分 `FOUND`、`PATH_ISSUE`、`MISSING`、`OPTIONAL`、`BLOCKED_BY_AUTH`。

### 2. Preview before mutation

優先執行：

```text
python scripts/bootstrap.py --preview
```

需要實際寫入時，必須由使用者明確要求，才執行：

```text
python scripts/bootstrap.py --apply
```

若目的地已有不同內容，停止並要求使用者確認；只有使用者明確授權才使用 `--force`。force 前建立 timestamp backup。

### 3. Initialize

初始化只能建立：

- 使用者層 `AGENTS.md`：通用工具發現、驗證與安全規則。
- 使用者層 `config.toml`：保留必要的 PATH 與非秘密環境變數。
- `environment-inventory.json`：工具實際解析路徑與版本快照。

不得把工具安裝、全域 npm install、系統 PATH 修改、憑證設定、雲端登入、Terraform apply 或部署混入自動初始化。這些動作必須另外說明並取得授權。

### 4. Verify

初始化後重新執行：

```text
python scripts/doctor.py --project-root <project-path>
```

再用新的 Codex 對話確認：

```text
請執行本機環境診斷，列出目前載入的全域 AGENTS、工具路徑、版本、PATH 問題與需要人工確認的項目。不要安裝任何東西。
```

只有實際重新檢查成功，才可宣稱初始化完成。

## Maintenance

- 新電腦：執行一次 `--preview`，確認後執行 `--apply`，再重新啟動 Codex。
- 日常使用：只執行 `doctor.py`；它不應修改檔案。
- 工具升級：先更新專案自己的 manifest 或版本管理設定，再重新診斷；不要直接修改全域 prompt。
- 新增跨專案規則前，確認至少有多個專案需要，且不會覆蓋專案層指引。
- 只把穩定的工作偏好放進全域 `AGENTS.md`；把專案規則留在專案自己的 `AGENTS.md`。
- 若 `AGENTS.override.md` 存在，先向使用者說明它會優先於基礎指引。

## Deliverable

回報：

- 使用的模式與命令。
- 建立或未修改的檔案。
- 工具狀態與實際路徑。
- 驗證結果。
- 未解決的 PATH、安裝、權限、認證或外部服務問題。

# Codex Skills 操作手冊

本文件保留完整安裝、更新、稽核、知識庫與 Bridge 操作步驟。快速導覽與 Skill 文件索引請看 [README](../README.md)。這是個人使用的 Codex-only、可安裝、可版本化 Skills Plugin；28 個 Skill 的唯一來源在 `skills/<skill-name>/`。

Bran 通用 Skills 與 Codex 全域自訂指示已整合至本專案。跨專案工作原則的唯一可複製版本位於 [Codex 全域自訂指示](CODEX-CUSTOM-INSTRUCTIONS.md)；Skills 的職責與選用方式見 [Skill 職責與選用目錄](SKILL-CATALOG.md) 及 [代表性路由案例](SKILL-ROUTING-SCENARIOS.md)。

新增或維護 Skill 時遵循 [Skill 作者規範](SKILL-STANDARD.md)。

使用方式：

```text
使用 $repo-understanding 建立此 repository 的知識庫。
```

其他工作可由 Codex 依全域自訂指示及 Skill 描述選用，也可以用 `$skill-name` 明確指定。

本專案不再提供 repository-local portable workflow，也不支援由 `CLAUDE.md` 或 repository-local workflow 自動啟動流程。

## 結構

```text
codex-skills/
├── plugin.json
├── skills/
│   ├── repo-understanding/
│   ├── codex-machine-bootstrap/
│   └── <其他 26 個通用 Skills>/
│       ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── references/
│   └── assets/
├── scripts/
│   ├── repo_tools.py
│   ├── bootstrap.py / init.py / audit.py
│   ├── validate-skill.py
│   ├── prepare-knowledge-base.py
│   ├── validate-knowledge-base.py
│   ├── organize-knowledge-base.py
│   ├── run-repo-understanding.py
│   ├── test-archify.py / test-bootstrap.py
│   ├── install-claude-bridge.py / test-claude-bridge.py
│   └── install-cursor-bridge.py / test-cursor-bridge.py
├── docs/CODEX-CUSTOM-INSTRUCTIONS.md
├── docs/SKILL-CATALOG.md
└── AGENTS.md
```

## 安裝與更新

給 AI 與維護者的依賴契約、缺少套件時的處理流程與回報格式，請參閱 [AI 使用與依賴契約](AI-USAGE.md)。每個 Skill 的詳細依賴則放在該 Skill 的 `SKILL.md` 或 `references/`，不可只依賴 README 的簡略說明。

若要設定跨專案工作方式，請將 [Codex 全域自訂指示](CODEX-CUSTOM-INSTRUCTIONS.md)貼入 Codex 的全域自訂指示欄位。安裝 Plugin 不會自行修改該使用者設定。

先預覽 bundled Skill 安裝計畫：

```powershell
python scripts/bootstrap.py
```

確認後套用：

```powershell
python scripts/bootstrap.py --apply
```

bootstrap 優先使用 `CODEX_HOME`，未設定時使用 `%USERPROFILE%\.codex`。也可指定自訂路徑：

```powershell
python scripts/bootstrap.py --codex-home 'D:\Codex'
python scripts/bootstrap.py --apply --codex-home 'D:\Codex'
```

目的地不存在時會建立。相同內容會顯示已是最新且不重複覆寫；內容不同時，未指定 `--force` 會拒絕覆蓋，指定後會先建立 timestamped backup，再以 staging 驗證後替換。

```powershell
python scripts/bootstrap.py --apply --force
```

單純安裝 Skill 不會修改 npm global prefix。只有明確指定 `--repair-npm-prefix` 才會檢查非 ASCII npm prefix；搭配 `--apply` 時會依平台使用安全預設路徑：Windows 為 `%LOCALAPPDATA%\npm-global`，macOS／Linux 為 `$HOME/.npm-global`。`toolchain.json` 不包含特定使用者的固定路徑：

```powershell
python scripts/bootstrap.py --repair-npm-prefix
python scripts/bootstrap.py --apply --repair-npm-prefix
```

bootstrap 不會從 `toolchain.json` 接受路徑穿越或非法 Skill 名稱，也不會自動下載未宣告的工具、Skill 或 runner。

## 依工作範圍選用的 capabilities

`toolchain.json` 記錄各工具的最低版本與用途；其 `requiredCapabilities` 是各自 gate 的依賴清單，不代表每次 repository understanding 都必須安裝全部工具。只在所選工作範圍需要該 gate 時才要求該 capability：

| Capability | 用途與適用 gate | 缺少時 |
|---|---|---|
| GitNexus `>= 1.6.12` | 明確需要 graph／process／route／trace／impact 支援證據，或增量影響分析時 | 若該項證據不是驗收必要條件，記錄 `SKIP` 或 `OPTIONAL MISSING` 並以原始碼等主要證據完成；若使用者要求此 gate，則只將該 gate 標為 `BLOCKED`／`PARTIAL` |
| Node `>= 18.0.0` | 執行依賴 Node 的工具，例如 Archify runner | 只阻擋相應工具 gate；其他文件、source/config/test 分析照常進行 |
| npm `>= 9.0.0` | 使用者明確要求且 target lockfile 支援的專案依賴安裝 | 不影響一般分析；未授權或缺少 lockfile 時不安裝並記錄該 gate 狀態 |
| `codebase-onboarding` | repository 地圖、入口、慣例與 first-change guide | 已整合在本 Skill，無需額外安裝 |
| `archify` | 使用者要求圖表，或已確認 scope／驗收需要圖表時的 HTML 圖表產生與驗證 | 只將要求的圖表 gate 標為 `BLOCKED`／`PARTIAL`；無圖表需求時標示 `NOT APPLICABLE`／`SKIP` |

`DONE` 依使用者要求的 scope 和驗收條件判斷：所有適用且必要的 gate 通過即可；未要求、未使用且不影響驗收的工具缺失，不會自動降級整份工作。若缺少工具使明確要求的 evidence／diagram gate 無法完成，標示受影響範圍與 `PARTIAL`／`BLOCKED`，不要把它擴大成整個 Skill 都無法執行。

## 跨平台初始化與環境稽核

所有平台只需要 Python 3.9+；腳本只使用 Python 標準函式庫，不需要 pip 套件：

```text
python scripts/init.py
python scripts/init.py --apply
```

指定 Codex 路徑、Force 更新或檢查 npm：

```text
python scripts/init.py --codex-home "$HOME/.codex" --apply
python scripts/init.py --apply --force
python scripts/init.py --repair-npm-prefix
python scripts/init.py --install-project-dependencies --apply
```

預設只稽核與預覽；只有 `--apply` 才會寫入。初始化會安裝 `toolchain.json` 中列出的全部 28 個 Skills。Codebase Onboarding 已整合在 `repo-understanding`，不會安裝第二個同名 Skill；也不會自動下載 GitNexus、Archify 或其他未宣告工具。

只做環境與引用稽核：

```text
python scripts/audit.py
```

稽核會檢查 Plugin／toolchain／Skill 結構、references/assets 引用、Codex 安裝目的地及外部工具可用狀態。工具缺失是 gate 範圍的資訊，不會單憑「未安裝」就代表一般 Skill 安裝或 source-based 分析失敗；需要 Archify 時再檢查 `$CODEX_HOME/skills/archify` 或使用者層級的 `~/.agents/skills/archify`，並依該 Skill 驗證 Node runner。必要來源損壞才代表稽核本身失敗。

## AI 自動初始化與檢核

在 Codex 中可直接要求：

```text
使用 $repo-understanding 初始化並檢查目前環境。
先執行 audit，不要修改環境；列出必要、可選與阻塞項目。
```

AI 會先確認 Python 3.9+，再執行 `audit.py`，並將結果分類為：

- `READY`：可直接進入 Repository Understanding
- `NEEDS INITIALIZATION`：Skill 尚未安裝或需要更新
- `OPTIONAL MISSING`：非本次 gate 必需的工具缺失
- `BLOCKED / USER AUTHORIZATION REQUIRED`：需要使用者授權或外部狀態

確認預覽後，再要求：

```text
請套用初始化，使用目前平台適用的 init 腳本；完成後執行 validator、bootstrap smoke test 與可用的 Bridge smoke test。
```

AI 不會因為稽核發現缺少工具就偷偷下載。Codebase Onboarding 已內建；其他外部工具會記錄缺口與影響，等待明確授權。

## 驗證

```text
python scripts/validate-skill.py skills/repo-understanding
python scripts/validate-skill.py skills/evidence-first-research
python scripts/test-bootstrap.py
python scripts/test-codex-machine-bootstrap.py
python scripts/test-claude-bridge.py
python scripts/test-cursor-bridge.py
```

## Knowledge base 與 Archify 輔助腳本

預覽知識庫骨架，不會修改 target repository：

```text
python scripts/prepare-knowledge-base.py --repository-path 'D:\target-repository'
```

確認後建立缺少的骨架文件，不覆蓋已存在文件：

```text
python scripts/prepare-knowledge-base.py --repository-path 'D:\target-repository' --apply
```

驗證既有知識庫：

```text
python scripts/validate-knowledge-base.py 'D:\target-repository\docs\repo-understanding'
```

驗證已安裝的 Archify：

```text
python scripts/test-archify.py
```

建立並整理知識庫 dashboard：

```text
python scripts/run-repo-understanding.py --repository-path 'D:\target-repository'
python scripts/run-repo-understanding.py --repository-path 'D:\target-repository' --apply
```

若要在明確授權後執行 GitNexus index：

```text
python scripts/run-repo-understanding.py --repository-path 'D:\target-repository' --apply --run-gitnexus
```

輸出入口固定為 `docs/repo-understanding/index.md`。它會列出文件、圖表、run-state 與下一步；圖表放在 `docs/repo-understanding/diagrams/`。腳本不會把 AI 的分析結果硬塞進文件，也不會自動覆蓋既有內容。

## 大型跨 repository system

大型跨 repository 專案可以直接使用 `$repo-understanding`。若 system root 已有 `repository-understanding-system.yaml`，AI 會依 manifest 的 repository、role、required、triggers 與 contracts 執行；每個 Git repository 保留自己的 revision、GitNexus index、run-state 與文件，system root 則建立 `docs/repository-understanding-system/` 的整合產物。

若尚未有 manifest，AI 不會自行猜測完整範圍，而會逐步詢問：

1. system root 與掃描邊界。
2. 哪些 Git repositories 納入。
3. 每個 repository 的 id、path、role、required 與 triggers。
4. producer／consumer contracts、transport、endpoint 與 evidence。
5. 是否確認 YAML 草稿。

只有使用者確認草稿後，才會建立或更新 `repository-understanding-system.yaml`。這可避免把 sibling repository、外部路徑或猜測的 integration 當成已確認架構。

所有平台使用相同的 `.py` 腳本。這些腳本不會安裝外部工具，也不會覆蓋既有文件。

Validator 使用 Python 標準函式庫，會檢查每個 Skill 的 frontmatter 版本／狀態／檢視日期、必要章節與輸入欄位、Skill name、`agents/openai.yaml`、references/assets 連結、Plugin manifest、toolchain bundledSkills 與未完成的 TODO/FIXME/PLACEHOLDER。

## Claude Code Bridge

Claude Code 不會直接載入 Codex Skill，因此提供使用者層級 bridge。Bridge 不會將完整 workflow 複製到 target repository，而是要求 Claude Code 讀取已安裝的 Codex Skill。

先預覽，再套用：

```text
python scripts/install-claude-bridge.py
python scripts/install-claude-bridge.py --apply
```

預設更新 `%USERPROFILE%\.claude\CLAUDE.md`。若已有使用者設定，未指定 `--force` 時會拒絕混入；`--force` 會先保留 backup：

```powershell
python scripts/install-claude-bridge.py --apply --force
python scripts/test-claude-bridge.py
```

找不到已安裝的 Skill 時會回報 `BLOCKED / USER AUTHORIZATION REQUIRED`，不會自行安裝。

## Cursor Bridge

Cursor 支援全域 User Rules。Bridge 會在 Windows 的 `%USERPROFILE%\.cursor\rules\repo-understanding.mdc` 建立短規則，讓 Cursor Agent／CLI 使用已安裝的 Codex Skill，而不在 target repository 建立 portable workflow。

```text
python scripts/install-cursor-bridge.py
python scripts/install-cursor-bridge.py --apply
python scripts/install-cursor-bridge.py --apply --force
python scripts/test-cursor-bridge.py
```

## 限制

- 正式支援面是 Codex Plugin／Skill。
- Claude Code 與 Cursor 只透過使用者層級 bridge 使用同一份 Skill，不是原生載入 Codex Plugin。
- Bridge 不會自動安裝 Skill；使用者必須先完成 Codex Skill 安裝。
- 不會自動安裝 GitNexus、Archify 或 target repository dependencies；Codebase Onboarding 已內建於本 Skill。
- 動態行為、外部服務與缺少工具的驗證，會依 Skill 規則標記為 `BLOCKED` 或 `UNVERIFIED`。

## 版本與安全界線

Plugin manifest 位於根目錄 `plugin.json`。除非使用者明確要求，不會 commit、push、merge、deploy、release，也不會實際修改使用者的 Codex、Claude Code 或 Cursor 設定。

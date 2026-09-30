# Codex Skills

這是個人使用的 Codex-only、可安裝、可版本化 Skills Plugin。每個 Skill 都以 `skills/<skill-name>/` 作為唯一真實來源；目前內含 `repo-understanding`，Plugin 版本為 `1.0.0`。

使用方式：

```text
使用 $repo-understanding 建立此 repository 的知識庫。
```

本專案不再提供 repository-local portable workflow，也不支援由 `CLAUDE.md` 或 repository-local workflow 自動啟動流程。

## 結構

```text
codex-skills/
├── plugin.json
├── skills/
│   └── repo-understanding/
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
└── AGENTS.md
```

## 安裝與更新

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

## Required capabilities

`toolchain.json` 目前宣告完整分析所需的 capabilities：

| Capability | 類型 | 用途 | 缺少時 |
|---|---|---|---|
| GitNexus `>= 1.6.12` | command | graph、process、route、trace、impact evidence | graph gate `BLOCKED` |
| Node `>= 18.0.0` | command | Node runner 與 runtime verification | Node gate `BLOCKED` |
| npm `>= 9.0.0` | command | 只執行已宣告的 dependency install | npm gate `BLOCKED` |
| `codebase-onboarding` | 內建整合能力 | project map、entry points、conventions、first-change guide | 隨本 Skill 提供 |
| `archify` | Codex Skill | architecture／workflow／sequence／lifecycle diagrams | diagram gate `BLOCKED` |

初始化會自動檢查這些 capabilities。`codebase-onboarding` 已整合在本 Plugin 的唯一真實來源內，不需要額外下載；若缺少 GitNexus、Node、npm 或 Archify，AI 仍可建立部分知識庫，但不可宣告完整 `DONE`。

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

預設只稽核與預覽；只有 `--apply` 才會寫入。單純初始化只會安裝本 Plugin 的 `repo-understanding` Skill；Codebase Onboarding 已隨 Skill 提供，不會再安裝第二個同名 Skill，也不會自動下載 GitNexus、Archify 或其他未宣告工具。

只做環境與引用稽核：

```text
python scripts/audit.py
```

稽核會檢查 Plugin／toolchain／Skill 結構、references/assets 引用、Codex 安裝目的地，以及 Python、Git、Node、npm、GitNexus runner、內建 Codebase Onboarding 整合與 Archify 狀態。Archify 會依序檢查 `$CODEX_HOME/skills/archify` 與使用者層級的 `~/.agents/skills/archify`，並執行 `node bin/archify.mjs doctor`。必要來源缺失會回傳非零退出碼；缺少外部工具只會列出，不會假裝已安裝。

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
python scripts/test-bootstrap.py
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

Validator 使用 Python 標準函式庫，會檢查每個 Skill 的 frontmatter、Skill name、`agents/openai.yaml`、references/assets 連結、Plugin manifest、toolchain bundledSkills 與未完成的 TODO/FIXME/PLACEHOLDER。

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

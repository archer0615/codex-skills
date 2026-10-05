# Skill Authoring Standard

`skills/<skill-name>/` 是每個 Skill 的唯一來源。所有 Skill 都必須能被明確選用、按步驟執行，並用可觀察的條件檢查結果。

## Required frontmatter

```yaml
name: lowercase-kebab-case
version: 1.0
status: active
last_reviewed: YYYY-MM-DD
description: Use when a specific task or condition applies.
```

- `name` 必須等於 Skill 目錄名稱。
- `version` 使用 `major.minor` 或 `major.minor.patch`；相容的內容修正可維持行為契約，觸發範圍或輸出契約變更須提高版本並說明相容影響。
- `status` 使用 `active`、`experimental`、`deprecated` 或 `retired`。停用中的 Skill 必須提供替代或遷移說明。
- `last_reviewed` 必須是有效 ISO 日期。
- `description` 明確說明何時使用，避免「任何請求」等泛化觸發條件。

## Required sections

每個 `SKILL.md` 必須依序提供下列章節：

1. `## Use when`：明確觸發情境與不適用邊界。
2. `## Inputs`：列出 `Required`、`Optional`、`Preconditions`、`Missing information` 與 `Output artifact`。
3. `## Procedure`：至少一個編號步驟；步驟需說明要檢查或產生什麼，以及判斷依據。若依賴命令、工具或檔案，說明如何定位、檢查、授權與處理缺失。
4. `## Decision rules`：說明主要決策、停止條件、安全界線及與相鄰 Skills 的分工。
5. `## Verification`：使用可觀察的證據或完成條件；不得要求宣稱未執行的檢查成功。
6. `## Output`：明確規定回報或產物內容。

## Codex integration and library compatibility

- 每個 Skill 目錄必須有 `agents/openai.yaml`，且含 `display_name`、`short_description`、`default_prompt`。
- `toolchain.json` 的 `bundledSkills` 必須與 `skills/*/SKILL.md` 完全一致；名稱需唯一並符合目錄契約。
- 每個 Skill 只能有一個明確的主要責任。需要 handoff 時，定義交接輸入、輸出和觸發條件；不要複製另一個 Skill 的完整程序。
- Plugin 版本遵守 SemVer `major.minor.patch`；新增相容能力提高 minor，純修正提高 patch，破壞相容性或 Skill 使用契約變更提高 major。
- 新增或修改 Skill 時，檢查 [Skill catalog](SKILL-CATALOG.md)、全域自訂指示及相關 Skills；同步更新重疊邊界和代表性路由情境。
- 外部依賴須說明用途、檢查方式、缺失影響、安裝授權和修復命令；預設不得自行下載或改動使用者環境。
- 不放入秘密、個人資料、機器專屬路徑、未確認的命令或空白 TODO/FIXME/PLACEHOLDER。

## Validation

修改後執行：

```powershell
Get-ChildItem skills -Directory | ForEach-Object { python scripts/validate-skill.py $_.FullName }
python scripts/test-bootstrap.py
python scripts/test-codex-machine-bootstrap.py
```

涉及 `repo-understanding` 時，另執行 `python scripts/test-repo-understanding.py`。若改變多個 Skills 的路由或 handoff，也要人工檢查 [Skill catalog](SKILL-CATALOG.md) 及 README 中的驗證情境。

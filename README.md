# Codex Skills

這是個人使用的 Codex-only Skills Plugin，也是 Bran 通用 Skills 與 Codex 全域自訂指示的唯一維護來源。28 個 Skills 的唯一來源位於 `skills/<skill-name>/`；Bran Python orchestrator 不會隨 Plugin 安裝。

## 快速開始

先預覽安裝／更新計畫，再確認套用：

```powershell
python scripts/bootstrap.py
python scripts/bootstrap.py --apply
```

套用會將 `toolchain.json` 中的 Skills 安裝到 `%CODEX_HOME%\skills`（若未設定 `CODEX_HOME`，使用 `%USERPROFILE%\.codex\skills`）。遇到目的地有不同內容時會停止；只有明確要備份並覆蓋時才加 `--force`。

在 Codex 中以 `$skill-name` 指定 Skill；例如：

```text
使用 $repo-understanding 建立目前 repository 的證據導向知識庫。
```

一般明確任務可讓 Codex 依全域自訂指示與 Skill 描述選擇；簡單問答不需要啟動 Skill。

## 文件導覽

- [完整安裝、稽核、知識庫與 Bridge 操作手冊](docs/OPERATIONS.md)
- [Codex 全域自訂指示](docs/CODEX-CUSTOM-INSTRUCTIONS.md)：貼入 Codex 全域指示欄位；安裝 Plugin 不會替你修改此設定。
- [AI 使用與依賴契約](docs/AI-USAGE.md)：依賴檢查、狀態分類、授權與回報規則。
- [Skill 職責與選用目錄](docs/SKILL-CATALOG.md) 與 [代表性路由案例](docs/SKILL-ROUTING-SCENARIOS.md)
- [Skill 作者規範](docs/SKILL-STANDARD.md)：新增、修改與驗證 Skill 的契約。

## 維護原則

- 每項能力只維護一份真實來源；不要在 README、全域指示和 Skill 之間複製完整流程。
- 變更 Skill 的觸發或交接時，同步檢查職責目錄與路由案例。
- 除非使用者明確要求，不 commit、push、merge、deploy 或 release。
- 正式支援 Codex Plugin／Skill。Claude Code 與 Cursor 只透過使用者層級 Bridge 讀取已安裝的 `repo-understanding`，不是原生載入整個 Plugin。

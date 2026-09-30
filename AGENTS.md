# Codex Skills（Codex）

本 repository 是 Codex-only 個人 Skills Plugin。每個 Skill 的唯一真實來源位於 `skills/<skill-name>/`；目前 `repo-understanding` 的來源是 `skills/repo-understanding/SKILL.md`，使用時請以 `$repo-understanding` 啟動，不要尋找或建立 repository-local portable workflow。

此入口不授權修改應用程式邏輯、production、remote Git 或破壞性操作。若需要 Claude Code 或 Cursor，使用 `python scripts/install-claude-bridge.py`／`python scripts/install-cursor-bridge.py` 建立使用者層級 bridge。

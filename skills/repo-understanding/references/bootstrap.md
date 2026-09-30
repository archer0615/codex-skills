# Bootstrap

先依 `system-scope.md` 判定單一 repository、monorepo 或 multi-repository system；manifest 為 authoritative，未提供時只列出直接子目錄 Git roots 候選並要求使用者確認。逐 repository 辨識 Git status/branch/current revision、staged/unstaged diff、relevant untracked inventory、baseline/diff、語言、框架、建置工具、workspace/package 邊界與既有文件規則。各自建立 `resume-and-checkpoint.md` 的 Working Tree Identity 與 `gitnexus-coverage.md` 的 Capability Profile。檢查 GitNexus runner（既有 `.gitnexus/run.cjs`、`gitnexus`、`npx`、`pnpm dlx`、`bunx`）、index 是否存在／新鮮，以及本 Skill 內建的 `codebase-onboarding.md` 整合與 Archify 是否可用；不要尋找或安裝第二個 `codebase-onboarding` Skill。

不因缺少 index 而失敗：首次分析通常需要 FULL。若可用的 GitNexus runner 能執行，使用官方 analyze 流程建立／更新 index，並使用 `--skip-agents-md --skip-skills` 保護現有入口規則。若將下載或安裝 GitNexus／Skill，先回報 `BLOCKED / USER AUTHORIZATION REQUIRED`；不得手動建立 `.gitnexus/`。

選擇 INCREMENTAL 的前提是可信 baseline/current revision、可用 diff、current index 與安全的影響邊界；其餘情況選 FULL。

缺少 GitNexus runner、必要 Skill 或 target runtime/build dependency 時不得自動安裝。記錄缺項、影響、阻擋的 gate 與可行安裝方式：GitNexus 缺失阻擋 graph coverage，Archify 缺失只阻擋相應圖表，選用 Skill 缺失為 Skip/Not Applicable，target dependency 缺失使 runtime 驗證為 UNVERIFIED。若 target 明確含有 `scripts/bootstrap.py` 與 `toolchain.json`，先以預覽模式列出其 bundled Skills 與 lockfile 對應的 npm 安裝計畫；只有使用者明確要求 `--apply` 時才可套用。腳本會依平台處理含非 ASCII 字元的 npm global prefix，但不得下載未在 toolchain 宣告的 runner 或 Skill。其他情況取得明確授權後才提出並執行具體安裝命令，然後依 run-state 只重試 BLOCKED/Next Minimal Action。

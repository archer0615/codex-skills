# Skill 職責與選用目錄

本目錄說明 Skills 之間的分工，協助 Codex 選出一個主要執行流程。完整程序仍以各 Skill 的 `SKILL.md` 為準。

## 共通路由規則

- 簡單問答直接回答；不要為了每個請求都啟動 router 或閉環流程。
- 每個工作流選一個主要執行者。只有負責不同步驟的 Skill 才加入，並明確定義交接輸入、輸出與條件。
- 一般陌生專案的短期接手摘要使用 `existing-project-takeover`；需要可續跑、以證據為本的完整 repository 知識庫時使用 `repo-understanding`。
- `implementation-validator` 蒐集技術驗證證據；`quality-gate` 根據驗收、風險和證據判斷能否交付；`closed-loop-task-solver` 只負責跨多階段且需要反覆修正的任務。
- `security-review` 負責有明確安全範圍時的技術安全分析；`quality-gate` 消費安全證據做交付判斷，不重複執行完整稽核。
- `codex-project-bootstrap` 處理單一專案指引；`codex-machine-bootstrap` 處理本機 Codex 使用者環境。
- 研究事實需要時效或可追溯來源時使用 `evidence-first-research`；需要比較選項時再接 `option-comparison`，需要決策摘要時再接 `decision-researcher`。

## Engineering 與 Codex

| Skill | 負責範圍 | 邊界／交接 |
|---|---|---|
| `repo-understanding` | 建立可續跑、證據導向的 repository／system 知識庫 | Source/config/test 為主要證據；GitNexus 是依問題選用的 supporting evidence，Archify 僅服務適用且驗收需要的圖表 gate；工具缺失只影響相應 gate |
| `existing-project-takeover` | 陌生專案的唯讀、有限範圍接手摘要；需要時提供基線，並以有限 Git 歷史作為經來源交叉核對的輔助風險線索 | 不自行執行實作／修正循環；不從提交統計推斷缺陷率、個人責任或程式碼品質；特定修改直接交實作 owner，多階段閉環交 `closed-loop-task-solver`；不建立第二套持續維護的 repository wiki |
| `requirement-refinement` | 缺少重要範圍、限制、驗收條件或影響行為的領域詞彙／規則時釐清需求 | 需求可直接執行時不介入；領域建模是有條件的子流程，不預設建立 glossary／ADR；完整 repository 地圖交 `repo-understanding` |
| `codex-project-bootstrap` | 專案層 Codex 指引和驗證慣例 | 不處理全域電腦設定 |
| `codex-machine-bootstrap` | 本機 Codex 使用者設定、工具盤點與診斷 | 不取代專案自己的設定與依賴規則 |
| `implementation-validator` | 執行針對性檢查並整理可重現證據 | 將最終證據交給 `quality-gate`（需要交付判斷時） |
| `quality-gate` | 依範圍、品質、安全和證據判斷產物是否可交付 | 不重複執行所有驗證 |
| `security-review` | 對程式碼、設定、依賴、資料流或 AI 功能執行有界且有證據的技術安全審查 | 安全觸及面明確時使用；不自行修復、安裝套件、連線生產環境或執行未授權掃描；交付判斷交 `quality-gate` |
| `react-performance-review` | 對 React／Next.js 目標路徑進行聚焦、以專案版本和效能證據為本的檢查 | 僅適用 React／Next.js 效能情境；不取代一般驗證、安全審查或交付判斷，不機械套用優化規則 |
| `web-interface-review` | 檢查網頁介面的可及性、互動、表單、響應式和使用者狀態；有 baseline 時可做同條件視覺比較 | 跨 Web 技術棧；只回報有情境證據的問題，不套用品牌偏好或任意門檻；無 baseline 不宣稱視覺回歸；React／Next.js 效能交 `react-performance-review` |
| `closed-loop-task-solver` | 跨階段工作協調、驗收比對與有界修正循環 | 只用於實質需要修正循環的工作；選一個實作 owner，不複製其程序或驗證程序；測試、計畫、核准、子代理與 worktree 依專案規則、使用者授權和任務風險選擇 |
| `personal-ai-task-router` | 使用者要求路由或多種合理工作流難以區分時選路徑 | 日常明確任務由全域指示直接路由 |

## Research 與決策

| Skill | 負責範圍 | 邊界／交接 |
|---|---|---|
| `evidence-first-research` | 需要新近、專業或可追溯來源的研究 | 提供來源證據給比較或決策流程 |
| `option-comparison` | 依共同標準比較產品、設計、供應商或方案 | 選項與證據明確後再交 `decision-researcher` |
| `decision-researcher` | 把標準、證據、風險和取捨整理成建議 | 不把偏好當成事實 |
| `scenario-planning` | 探索不確定未來、訊號與穩健選項 | 不宣稱情境是預測 |
| `ai-governance` | AI 使用案例的風險、責任和控制設計 | 高影響流程可交 `human-review-workflow` |
| `human-review-workflow` | 人工核准、拒絕、升級、稽核與回復流程 | 不取代有權限的人作出決定 |

## Knowledge 與 Prompt

| Skill | 負責範圍 | 邊界／交接 |
|---|---|---|
| `knowledge-base-organizing` | 規劃分散文件、筆記和連結的知識架構 | 不靜默消解互相矛盾的來源 |
| `sop-generator` | 將已確認的重複流程寫成可交接 SOP | 不把未確認推論變成程序 |
| `conversation-skill-miner` | 從對話或任務歷史萃取可重用模式 | SOP 草稿可交 `sop-generator`；Skill 草稿可交 `skill-curator` |
| `prompt-evaluation` | 以代表案例測試 Prompt 的穩定性與安全性 | 有證據支持修改時再交 `prompt-curator` |
| `prompt-curator` | 整理、分類、去重和版本化 Prompt | 不宣稱未驗證的效果 |
| `prompt-skill-publisher` | 將核准的 Prompt／流程／Skill 整理成已驗證發布素材 | 發布本身仍須明確授權 |
| `skill-curator` | 盤點、去重與維護整個 Skill library | 保留名稱相容性和遷移紀錄 |
| `ai-playbook-maintainer` | 依 repo 真實來源同步維護 AI playbook | 不虛構能力或自動發布 |

## 專案追蹤與上下文

| Skill | 負責範圍 | 邊界／交接 |
|---|---|---|
| `context-management` | 長任務的狀態摘要與交接包 | 明確標示已驗證、未驗證、阻塞與恢復步驟 |
| `project-tracking` | 將專案證據整理成進度、風險和行動清單 | 不捏造進度或承諾 |

## Codex Plugin 安裝範圍

`toolchain.json` 的 `bundledSkills` 是 Plugin 安裝器唯一採用的 Skill 清單，必須與 `skills/<skill-name>/SKILL.md` 一一對應。Bran 的 Python orchestrator 不屬於 Skill，本 Plugin 不會安裝或執行它。

路由案例若提到 Codex 平台提供的 Skill（有些名稱帶 namespace，例如 `plugin-management:plugin-management`），代表在目前環境可用時交由該平台能力處理；這些名稱不是本 Plugin 的 bundled Skills，不可加入本庫清單或假設已安裝。

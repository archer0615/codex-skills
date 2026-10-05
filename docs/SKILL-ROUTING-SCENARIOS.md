# Skill Routing Scenarios

Use these cases to review Skill triggers and handoffs after a routing or scope change. They specify expected ownership, not fixed answer wording.

| # | Request | Expected route | Boundary to verify |
|---|---|---|---|
| 1 | 「東京是日本首都嗎？」 | Direct answer; no Skill | Do not invoke router or research for a stable, low-risk fact. |
| 2 | 「幫我加一個匯出功能。」 without format, data scope, or acceptance criteria | `requirement-refinement` | Ask only questions that materially affect behavior; do not invent requirements. |
| 3 | 「快速說明這個陌生專案的入口和測試，再修登入問題。」 | `existing-project-takeover` for bounded orientation, then one implementation owner | Keep orientation read-only and bounded; do not run tests without authorization; use `closed-loop-task-solver` only if the requested change needs multiple correction phases; do not create the persistent knowledge base. |
| 4 | 「為這個 monorepo 建立可續跑的完整架構和流程知識庫。」 | `repo-understanding` | Use source evidence, run-state, and applicable capability gates; GitNexus/Archify are required only when the accepted scope needs their specific evidence or diagrams. |
| 5 | 「建立本機 Codex 新電腦設定」 vs. 「替這個 repo 建立 Codex 指引」 | `codex-machine-bootstrap` vs. `codex-project-bootstrap` | User-level environment and project-local guidance remain separate. |
| 6 | 「程式改完，驗證登入流程」 vs. 「判斷這個版本能否交付」 vs. 「多階段任務要持續修正到驗收」 | `implementation-validator` vs. `quality-gate` vs. `closed-loop-task-solver` | Evidence collection follows project rules and authorization; delivery decision consumes that evidence; correction loop coordinates one implementation owner. Do not require tests, TDD, or subagents without authorization and task justification. |
| 7 | 「比較目前可用的資料庫服務，評估價格、效能和退出成本並建議方案。」 | `evidence-first-research` → `option-comparison` → `decision-researcher` | Research only when facts need freshness; compare consistent criteria; decision brief is a distinct output. |
| 8 | 「測試這個 Prompt 對缺欄位和注入文字是否穩定，必要時修正。」 | `prompt-evaluation` → `prompt-curator` | Evaluate first; curate only changes supported by test evidence. |
| 9 | 「把這段對話整理成新人可執行的 SOP。」 | `conversation-skill-miner` → `sop-generator` | Separate durable procedure from one-off claims; do not invent missing steps. |
| 10 | 「設計 AI 自動審核付款資料的流程。」 | `ai-governance` → `human-review-workflow` → `quality-gate` when delivery readiness is requested | High-impact approval cannot bypass a responsible human; do not claim legal compliance. |
| 11 | 「整理目前長任務狀態，交給另一個對話接手」 vs. 「整理本月專案進度和風險」 | `context-management` vs. `project-tracking` | Handoff preserves state/evidence; tracking summarizes dated status and actions. |
| 12 | 「盤點這個 Skills library 的重疊與觸發問題。」 | `skill-curator` → `implementation-validator`/`quality-gate` only if edits are made | Distinguish duplicate, specialization, orchestration, and handoff; preserve identifiers. |
| 13 | 「依 repository 真實能力同步更新這個 AI playbook 和導覽。」 | `ai-playbook-maintainer` | Trace every published claim to source; do not publish or deploy unless requested. |
| 14 | 「把散落筆記規劃成可檢索知識庫」 vs. 「把一次性任務經驗提煉成可重用能力」 | `knowledge-base-organizing` vs. `conversation-skill-miner` | Organize existing knowledge versus mine a reusable procedure or Skill candidate. |
| 15 | 「評估兩種未來情境下仍穩健的策略」 vs. 「整理目前決策的選項和建議」 | `scenario-planning` vs. `option-comparison` → `decision-researcher` | Scenarios describe plausible futures; option comparison evaluates concrete alternatives. |
| 16 | 「整理一組可重用 Prompt」 vs. 「把已核准 Skill 轉成可驗證交付物」 | `prompt-curator` vs. `prompt-skill-publisher` | Curating content is separate from packaging and validating a target artifact. |
| 17 | 「檢查登入、外部輸入或依賴是否有安全漏洞」 | `security-review` | 以授權範圍內的程式碼／設定證據為主；不連 production、不安裝掃描器、不做修復或外部掃描，除非明確授權。 |
| 18 | 「這個系統中的『客戶』和『使用者』是否相同？釐清後完成這項需求」 | `requirement-refinement` | 只在差異影響需求、資料或行為時檢查既有詞彙、文件、schema 與程式碼；區分業務規則和實作現況，不預設建立 glossary／ADR。 |
| 19 | 「檢查這個 Next.js 頁面載入慢的原因，並改善最明顯的效能瓶頸」 | `react-performance-review` | 先確認 framework/version 和目標路徑；區分量測與假設；只做被證據支持的最小改動，未量測改善不可宣稱已加速。 |
| 20 | 「檢查這個結帳頁面鍵盤操作、表單錯誤與手機版是否好用」 | `web-interface-review` | 檢查實際使用情境和可及性；來源程式碼無法證明的呈現／輔助科技行為標為 `UNVERIFIED`；不把通用樣式偏好當缺陷。 |
| 21 | 「比對這次 UI 修改前後的手機和桌面截圖，找出意外版面回歸」 | `web-interface-review` | 相同路由、viewport、狀態及可比瀏覽器條件下比較；分開預期差異、渲染雜訊和確認的 regression；只有單張截圖時不宣稱已完成比較。 |
| 22 | 「找一個可安裝的 Skill，補上這個 library 沒有的能力」 | `find-skills` for discovery; after the user selects a candidate, `skill-installer` for installation | 先比對目前能力與安裝來源；「尋找」不等於授權修改使用者的 Skill 目錄；安裝後再依目標環境驗證，不把外部 Skill 當成本 library 的維護來源。 |
| 23 | 「建立一個可以連接外部服務的 Codex plugin／MCP integration」 | `plugin-creator:create-plugin` | 先界定服務、資料／寫入操作和權限；plugin authoring 與本 repository 內的純 Skill 維護分開；不得因提出建置需求就連接真實帳號或發布。 |
| 24 | 「幫 Codex 連接 Slack／Drive，並說明需要哪些權限」 | `plugin-management:plugin-management` for an existing connector; `plugin-creator:create-plugin` only when a new integration must be built | 先確認所需資料範圍、讀寫能力與帳號授權；安裝／連接既有 plugin 和建立新 plugin 是不同路徑，不能默認連接或授權。 |
| 25 | 「我不確定應先釐清需求還是先看 repository，幫我選一個安全的工作順序。」 | `personal-ai-task-router` | 先根據現有上下文比較主要路徑；只在缺少資訊會改變路由時提問，並交給一個主要執行 Skill，不代替其執行工作。 |

## Review criteria

- Each request has one primary owner; supporting Skills have a distinct input and output.
- No route is selected only because the request lacks an explicit Skill name.
- Missing evidence, dependencies, approvals, and acceptance criteria remain visible.
- The route respects the global custom instructions and project-specific `AGENTS.md`.
- A creative or behavior-changing task does not automatically trigger a design-approval gate; ask only for material missing information.
- External Skill discovery, user-level installation, plugin authoring, service connection, and publication are separate actions with separate authorization boundaries.

# Repository Understanding Run State

## 身分與模式

| 欄位 | 值 |
| --- | --- |
| Run ID | <run-id> |
| Mode | <FULL / INCREMENTAL / RESUME> |
| Skill version | 2.0.0 |
| Started revision | <revision> |
| Last verified revision | <revision> |

## Working Tree Identity

| 欄位 | 值 |
| --- | --- |
| Staged diff identity | <identity> |
| Unstaged diff identity | <identity> |
| Relevant untracked inventory | <inventory> |

## Gate 與下一步

| Gate | 狀態 | 證據或原因 |
| --- | --- | --- |
| <gate> | <CURRENT / STALE / BLOCKED> | <reference> |

Next Minimal Action: <action>

Pending Gaps: <none or references>

Blocked Items: <none or references>

Scope / Evidence / Artifact inventories: <paths>

Execution log: <path>

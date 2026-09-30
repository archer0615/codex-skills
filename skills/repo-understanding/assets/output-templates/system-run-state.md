# Repository Understanding System Run State

| Field | Value |
| --- | --- |
| Run ID | <run-id> |
| Manifest identity | <path + content identity, or confirmed discovery inventory> |
| Mode | <FULL / INCREMENTAL / RESUME> |
| Status | <IN PROGRESS / BLOCKED / COMPLETE / INCOMPLETE> |

## Repository inventory

| ID | Path | Role | Required | Revision | Working Tree Identity | Local run state |
| --- | --- | --- | --- | --- | --- | --- |
| <id> | <path> | <role> | <true / false> | <revision> | <identity> | <link> |

## Contracts and impact

| Contract | Participants | Evidence on both sides | Status | Affected artifacts |
| --- | --- | --- | --- | --- |
| <id> | <repo IDs> | <paths/config/tests> | <CONFIRMED / INFERRED / UNKNOWN / BLOCKED> | <links> |

Next Minimal Action: <action>

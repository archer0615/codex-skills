# Multi-repository System Scope

Monorepo 是單一 Git repository，依 workspace/package inventory 處理。多 repository system 是多個獨立 Git worktree 的協作範圍。

若 system root 存在 `repository-understanding-system.yaml`，以它列出的 repository ID、local path、role、required 與 contracts 為唯一範圍。repository entry 使用 `id`、`path`、`role`、`required`；`role` 可為 `batch-job`，並以可選 `triggers` 記錄 schedule/manual/event。只有 `external: true` 可允許 system root 外的本機 path。HTTP contract 使用 `kind: http`；若為 HTTPS，明確加上 `transport: https` 與非敏感的 `endpoint`。不得寫入 tokens、credentials 或 signed URLs。未提供 manifest 時，只掃描 system root 的直接子目錄 Git roots 作為候選，先取得使用者確認；不遞迴猜測 sibling、parent 或外部路徑。

每個 repository 都有獨立 revision、Working Tree Identity、GitNexus index、capability profile、ledger、run state 與 repository-level artifacts。系統層產物放在 system root 的 `docs/repository-understanding-system/`，每項 claim 都要標示參與 repository 與 revision，並連回雙方證據。

跨 repository integration 需兩端 source/config/contract evidence 才是 CONFIRMED；單邊為 INFERRED，缺少 counterpart 為 UNKNOWN 或 BLOCKED。變更分析先在變更 repository 內執行，再透過已宣告或確認的 contract 標記相依 repository/system artifacts NEEDS VERIFICATION；GitNexus impact 不跨 repository 執行。

## AI 互動式 system manifest 定義

當使用者要求分析大型跨 repository system，而 system root 尚未有 `repository-understanding-system.yaml` 時，AI 必須進入互動式定義流程，不可直接猜測完整範圍。一次只問一組會影響範圍的問題，並在寫檔前展示完整草稿。

### 問答順序

1. **System root**：確認 system root 路徑與是否只允許其直接子目錄。
2. **Repository inventory**：列出偵測到的直接子目錄 Git roots，逐一詢問是否納入；外部路徑必須明確指定 `external: true`。
3. **Repository metadata**：為每個納入項目確認穩定 `id`、`path`、`role`、`required`；batch job 另外確認 schedule、manual 或 event trigger。
4. **Contracts**：詢問 repository 之間是否存在 HTTP、queue、event、file 或 library contract，並確認 producer、consumer、transport、非敏感 endpoint 與 evidence。
5. **Analysis policy**：確認是否允許掃描每個 repository、是否需要 FULL、是否有不可讀取或不可執行的路徑。
6. **Review**：展示 YAML 草稿、列出未定義欄位與風險，詢問使用者是否確認寫入。

### 寫入規則

- 使用者未確認草稿前，只能輸出預覽，不得建立或覆寫 manifest。
- 不寫入 token、credential、signed URL、密碼或其他秘密。
- 不把掃描到的目錄名稱直接當成已確認 repository；必須取得使用者確認。
- 確認後才建立 system root 的 `repository-understanding-system.yaml`，並立即驗證 paths、IDs、roles、required 與 contract references。
- manifest 變更後，所有 repository-level run-state 與 system-level inventory 都標記為 `NEEDS VERIFICATION`，重新計算 scope。

### 對使用者的最小提問範例

```text
我偵測到 3 個直接子目錄 Git repository：frontend、api、worker。
是否三個都納入？請確認每個 repository 的角色，以及 worker 是否為 required。
接著我會整理 producer／consumer contracts，展示 YAML 草稿後才寫入。
```

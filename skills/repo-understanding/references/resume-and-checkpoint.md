# Resume and Checkpoint

將持久狀態寫在文件輸出位置的 `run-state.md`。每次開始、每個 phase/gate 完成後、BLOCKED 前與 FINAL VERIFY 後更新；逐操作細節留在 `toolchain-utilization.md`，避免 checkpoint 本身成為 token 成本。

至少記錄：Run ID、Started/Last Checked Revision、Working Tree Identity（staged diff、unstaged diff、relevant untracked inventory）、Mode、Run Status（IN PROGRESS/BLOCKED/COMPLETE/INCOMPLETE）、Current/Next Minimal Action、Completed Gates、Pending Gaps、Blocked Items、Artifacts Needing Verification、Index State。

重新啟動時先驗證 state 的 revision、Working Tree Identity、產物與 evidence reference：只有 revision、staged/unstaged diff 與 relevant untracked inventory 都相同，且 gate/index/artifact 仍 CURRENT，才從 Next Minimal Action 繼續；任一 identity 改變且 diff 可信時先跑 detect_changes/impact，只標記受影響產物 NEEDS VERIFICATION；diff/index/impact 邊界不可信時記錄 `INCREMENTAL → FULL`；BLOCKED 只在授權或外部狀態改變後重試；index stale 只更新 index 再判定影響。沒有 Git identity 時採保守 FULL 或 NEEDS VERIFICATION。

驗證時以 disposable fixture 或安全分支：中斷一次後確認 revision 與 Working Tree Identity 都相同時不重跑 completed gate；在 HEAD 不變時分別做 staged、unstaged、relevant untracked 變更，確認只更新受影響文件／圖表；解除一項 BLOCKED 確認只重試該項；無可信 diff/index 時確認 fallback FULL 有明確理由。

Multi-repository mode 另維護 system run state：記錄 manifest identity、每個 repository ID/path/role/revision/Working Tree Identity、已驗證 contracts 與受影響 system artifacts。它不取代任何 repository-local run state；一個 repository 改變時，僅透過已宣告或已確認 contract 標記相關系統產物與相依 repository artifacts NEEDS VERIFICATION。

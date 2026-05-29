# 内部压缩阶段

Compact（上下文压缩）只在需要时加载。

它用于保持 CURRENT 和 TASKS 足够小。

## 触发条件

- `CURRENT.md` 超过约 120 行。
- `TASKS.md` 超过约 200 行。
- 单个任务的 Short Notes（简短记录）超过 10 行。
- 同一任务 do/check 循环超过 3 次。
- 上下文接近限制。
- `.ai/tmp/` 或 `.ai/artifacts/` 变得杂乱。

## Compact 做什么

- CURRENT 保留当前目标、阶段、blockers（阻塞项）、风险、验证摘要和下一步。
- TASKS 保留 pending / in_progress 任务和必要 blockers。
- Done 任务细节移动到 archive candidate（归档候选）。
- 可复用经验标记为 Learn Candidates（经验候选）。
- 有用产物只记录相对路径摘要。
- 确认无引用后，可清理或标记无用临时文件。

## Compact 必须保留

- 当前目标。
- 当前状态。
- 当前 blockers。
- 当前风险。
- 已完成 / 未完成状态。
- 验证结果。
- Remaining Risks（剩余风险）。
- 下一步。

## Compact 必须删除或压缩

- 长 reasoning（推理过程）。
- 长日志。
- 重复解释。
- 已废弃方案。
- 失败的中间尝试。
- 长 browser trace。
- 长 network dump。
- 长 console output。
- 长 code-reviewer 输出。
- 长 build/test 输出。

## Compact 禁止

- 把 archive 内容塞回 CURRENT。
- 删除 requirements。
- 删除 DECISIONS。
- 删除仍被引用的 artifacts。
- 把 CURRENT 变成聊天记录。

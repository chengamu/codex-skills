# 归档规则

`/archive = learn + archive + final compact`

Archive（归档）是当前任务的最终收口命令。它不会删除长期需求文件。

## 执行流程

1. 读取 CURRENT / TASKS。
2. 检查 Archive Gate（归档门）。
3. 加载 `learn.md`。
4. 将经验提炼到 MEMORY / playbooks。
5. 生成 archive 归档记录。
6. 更新 HANDOFF。
7. 加载 `compact.md` 做 final compact（最终压缩）。
8. 将 CURRENT / TASKS 清理到轻量状态。

## Archive Gate：归档门

- 不能存在 `in_progress` 任务。
- blocked 任务必须明确记录。
- 未验证内容必须标记为 `Not Run`。
- 高风险未解决问题不能归档为 `Accepted`。

## 归档模板

```md
# Archive: <feature>

## Feature：功能

## Requirement Source：需求来源

## Final Status：最终状态

Allowed values：允许值
- Accepted：已接受
- Accepted with Risks：带风险接受
- Partial：部分完成
- Blocked：阻塞
- Cancelled：取消
- Deferred：延期

## Scope：范围

## Out of Scope：不做范围

## Completed：已完成

## Not Completed：未完成

## Validation Summary：验证摘要

## Remaining Risks：剩余风险

## Lessons from Learn：经验提炼

## Key Decisions：关键决策

## Files Modified：修改文件

## Artifacts：产物

## Follow-up：后续事项
```

## 最终状态规则

只有 Acceptance Criteria（验收标准）已满足、验证已完成或明确不适用、且没有高风险 blocker 时，才能使用 `Accepted`。

否则使用 `Accepted with Risks`、`Partial`、`Blocked`、`Cancelled` 或 `Deferred`。

## 归档后

- CURRENT 保持最小状态。
- TASKS 清理已完成任务细节。
- HANDOFF 写入交接摘要。
- requirements 保留。
- DECISIONS 保留。
- MEMORY 和 playbooks 只保留可复用摘要。
- 完整日志、trace、长验证输出不进入 MEMORY。

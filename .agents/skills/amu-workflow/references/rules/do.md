# 执行规则

`/do` 是主执行命令。

它吸收 Superpowers 的执行思想：

- 任务可以按 Owner（任务负责人 / 子 Agent 角色）分配给子 Agent。
- DO 阶段应连续执行。
- 每个 Agent 都有明确边界。
- Agent 不能扩大 Scope（任务边界）。
- 上下文或文件增长过大时自动触发 Compact（上下文压缩）。
- 可复用经验通过 Playbook（排错手册）和 Archive（归档）沉淀。

## 执行模式

- `/do next`：执行下一个 pending（待执行）任务，并自动 check（检查）。
- `/do phase`：执行当前阶段所有未阻塞任务，每个任务后自动 check。
- `/do all`：执行所有未阻塞任务，每个任务后自动 check，直到完成或暂停。

## 执行流程

1. 读取 `.ai/CURRENT.md` 和 `.ai/TASKS.md`。
2. 如果存在 `wave-plan.md` 或 Task 包含 `Wave` 字段，加载 `wave-scheduler.md`。
3. 需要子 Agent 时加载 `tooling.md`，读取 Agent Registry。
4. 按当前 Wave 构建可执行任务集合。
5. 同一 Wave 内可并行时分配给多个 subagent；不可并行时顺序执行，但保留 Wave / Barrier 语义。
6. 按 Owner / OwnerSource 调度，并限制在 Task Scope（任务边界）内执行。
7. 记录 Short Notes（简短记录）和 task event，不写长过程。
8. 每个任务完成后自动加载 `check.md` 做任务级检查。
9. 当前 Wave 任务完成后执行 Barrier。
10. Barrier 通过 -> 进入下一 Wave；Barrier 失败 -> 只修复失败项，不进入下一 Wave。
11. do/check 循环重复或上下文增长 -> 加载 `compact.md`。
12. 所有任务完成 -> 将 CURRENT 的 Next Step 更新为 `Ready for /archive`。

## do/check 循环

```text
执行任务
  -> 检查任务
    -> 通过：标记 done，继续下一个任务
    -> 失败：更新 blocker / Short Notes，回到 /do 修复
    -> 重复失败或出现风险：暂停
```

## Wave Scheduler 执行

`/do` 不应把任务当作 flat checklist 顺序执行。存在 `Wave` 字段时，必须按 Wave 执行：

- 先执行 Wave 0。
- Barrier 0 通过后执行 Wave 1。
- Barrier 1 通过后执行 Wave 2。
- 以此类推。

当前环境支持 true parallel subagents 时，同一 Wave 内可并行 dispatch。当前环境不支持时，使用 sequential execution with Wave/Barrier semantics：顺序执行，但不能跳过 Barrier，也不能提前进入下一 Wave。

同一 Wave 内可执行任务必须满足：

- `Status` 是 `pending`。
- `DependsOn` 为空或依赖任务均为 `done`。
- `Files` 与其他可执行任务不重叠。
- `Forbidden` 明确。
- `ConflictBoundary` 明确。
- `Acceptance` 可验证。

Static Review Agent 审计任务必须单独放在 review Wave，不与 implementation tasks 同 Wave。

## Barrier

每个 Wave 结束后必须执行 Barrier：

1. collect diffs。
2. 检查 file overlap。
3. 检查 Forbidden path violation。
4. 检查 Acceptance criteria。
5. 记录 task events。
6. 更新 task status。
7. 已授权时运行 targeted checks。
8. 只在 Barrier 通过后进入下一 Wave。

Barrier 失败时，不进入下一 Wave；只修复失败项，然后重新执行 Barrier。

## Worktree isolation

代码修改任务优先使用 Worktree 隔离：

`.worktrees/<task-id>-<slug>/`

- 每个 subagent 只在自己的 Worktree 和允许的 `Files` 范围内工作。
- orchestrator 才能合并 diff。
- subagent 不允许修改 `Forbidden` 路径。
- subagent 不允许无关重构、升级依赖或格式化全项目。

如果当前环境不适合创建 Worktree，可在同一工作区顺序执行，但必须保留 `Files`、`Forbidden`、`ConflictBoundary` 检查。

## Agent 边界

- Agent 只能处理分配给自己的 Task Scope。
- Agent 只能修改 Task Files 中列出的文件；如需触碰其他文件，必须记录原因并保持在 Scope 内。
- Agent 不能重排任务。
- Agent 不能扩大功能范围。
- Agent 不能静默改变架构决策。
- Agent 不能绕过 Pause Points（暂停点）。
- Agent 输出必须压缩摘要写入 TASKS / CURRENT，不能完整粘贴。
- 如果 Owner 不合理，回到 `/plan` 修正；不要静默更改 Owner。

## SubAgent 调度

- 读取 `.ai/TASKS.md` 中的 `Owner`、`OwnerSource`、`OwnerReason`。
- `OwnerSource = agent-registry` 时，必须调用对应子 Agent。
- `OwnerSource = main-fallback` 时，由 main 执行。
- 不允许 main 静默吞掉已分配给子 Agent 的任务。
- 如果子 Agent 不可用，记录 `SubAgent unavailable` 和原因，再 fallback 到 main。
- fallback 后仍必须遵守原 Task Scope、Files、Forbidden、Acceptance 和 Barrier。

## Playbook 加载

`/do` 阶段只在具体问题匹配时加载 Playbook（可复用排错手册）：

- Maven / jar / compile / runtime -> `.ai/playbooks/java-build.md`
- Vue / TS / frontend build -> `.ai/playbooks/frontend-build.md`
- i18n -> `.ai/playbooks/i18n.md`
- UTC / timezone / date -> `.ai/playbooks/utc.md`
- generator -> `.ai/playbooks/generator.md`
- tenant / permission -> `.ai/playbooks/tenant.md`

## build/test/lint 授权

`/do` 运行 build/test/lint 前需要用户授权。

如果用户本轮已经授权，`/do` 可以在所有未阻塞任务完成后运行已授权命令；执行前仍要简要说明命令，然后继续进入 check。

如果没有授权，必须暂停，并列出建议命令。

未实际运行且成功，不得声称 build/test/lint 通过。

## 强制暂停条件

以下情况必须暂停：

- 需要新增依赖或升级依赖。
- 数据库结构、baseline 或 migration 未确认。
- 权限模型、租户模型、角色、菜单策略不清楚。
- i18n / UTC / 时区影响扩大。
- 需要 build/test/lint 但用户未授权。
- 子 Agent 结论冲突。
- 继续执行会扩大 Scope。
- 当前任务被 blocked。
- 需求与 requirement source 冲突。

## 产物归类

- 当前 change 有独立目录时，临时文件放 `.ai/changes/<change-id>/tmp/`。
- 当前 change 有独立目录时，日志摘要放 `.ai/changes/<change-id>/logs/`。
- 当前 change 有独立目录时，验证产物放 `.ai/changes/<change-id>/artifacts/`。
- 没有 change 目录时，临时文件放 `.ai/tmp/`，验证摘要放 `.ai/artifacts/`。
- 不在 `.ai` 根目录创建散乱的 log / tmp / json / txt / dump / trace 文件。
- 不把完整日志粘贴进 CURRENT 或 TASKS。
- 归档时只保留必要产物：`proposal.md`、`design.md`、`tasks.md`、`wave-plan.md`、`handoff.md`、`review.md`、`check.md`、`task-events.jsonl`。

## 生成文件卫生

- `.ai` 根目录必须保持干净。
- 临时文件必须进入 `.ai/tmp/`。
- 验证报告、截图、日志摘要必须进入 `.ai/artifacts/`。
- 不留下无引用产物。
- compact/archive 时，摘要化有用产物，清理或标记无用临时文件。

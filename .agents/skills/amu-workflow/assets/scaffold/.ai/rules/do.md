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
2. 找到第一个 `pending` 或 `in_progress` 任务。
3. 按 Owner 调度。
4. 在 Task Scope（任务边界）内执行。
5. 记录 Short Notes（简短记录），不写长过程。
6. 自动加载 `check.md`。
7. check 通过 -> 标记任务完成并继续。
8. check 失败 -> 更新 blocker（阻塞项）/ Short Notes，然后回到 `/do` 修复。
9. do/check 循环重复或上下文增长 -> 加载 `compact.md`。
10. 所有任务完成 -> 将 CURRENT 的 Next Step 更新为 `Ready for /archive`。

## do/check 循环

```text
执行任务
  -> 检查任务
    -> 通过：标记 done，继续下一个任务
    -> 失败：更新 blocker / Short Notes，回到 /do 修复
    -> 重复失败或出现风险：暂停
```

## Agent 边界

- Agent 只能处理分配给自己的 Task Scope。
- Agent 只能修改 Task Files 中列出的文件；如需触碰其他文件，必须记录原因并保持在 Scope 内。
- Agent 不能重排任务。
- Agent 不能扩大功能范围。
- Agent 不能静默改变架构决策。
- Agent 不能绕过 Pause Points（暂停点）。
- Agent 输出必须压缩摘要写入 TASKS / CURRENT，不能完整粘贴。
- 如果 Owner 不合理，回到 `/plan` 修正；不要静默更改 Owner。

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

- 临时文件放 `.ai/tmp/`。
- 报告、截图、验证摘要放 `.ai/artifacts/`。
- 不在 `.ai` 根目录创建散乱的 log / tmp / json / txt / dump / trace 文件。
- 不把完整日志粘贴进 CURRENT 或 TASKS。

## 生成文件卫生

- `.ai` 根目录必须保持干净。
- 临时文件必须进入 `.ai/tmp/`。
- 验证报告、截图、日志摘要必须进入 `.ai/artifacts/`。
- 不留下无引用产物。
- compact/archive 时，摘要化有用产物，清理或标记无用临时文件。

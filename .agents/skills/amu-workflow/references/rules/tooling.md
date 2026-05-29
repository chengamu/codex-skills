# 工具与子 Agent 规则

只有 `/plan` 或 `/do` 需要子 Agent 或 CodeGraph 支持时，才加载本文件。

## CodeGraph

- CodeGraph 用于定位代码结构、符号、关系和影响范围。
- 编辑前，最终行为判断仍必须读取真实源文件确认。
- 不把大量调用图、文件树、符号图复制进 `.ai` 文件。
- CodeGraph 结果过期或与真实文件冲突时，以真实文件为准，并记录风险。

## 子 Agent

- `/plan` 可以咨询子 Agent 做方案分析，但不能执行代码。
- `/do` 按 Task Owner（任务负责人 / 子 Agent 角色）调度子 Agent。
- `/check` 内部阶段可用时必须使用 `code-reviewer` 角色做审查。
- 子 Agent 不能扩大 Scope（任务边界）。
- 子 Agent 不能重排 Tasks。
- 子 Agent 不能绕过 Pause Points（暂停点）。
- 子 Agent 输出必须压缩摘要写入 CURRENT / TASKS，不能完整粘贴。

## Owner 映射

- `main`：工作流协调、文档、简单修改。
- `frontend-developer`：Vue 页面、组件、样式、交互。
- `typescript-pro`：TypeScript 类型、复杂前端逻辑、API 类型。
- `java-architect`：Java 后端、Service、Mapper、事务、权限、架构。
- `code-reviewer`：审查、验证、风险检查、验收标准检查。

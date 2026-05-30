# 工具与子 Agent 规则

只有 `/plan` 或 `/do` 需要子 Agent 或 CodeGraph 支持时，才加载本文件。

## CodeGraph

- CodeGraph 用于定位代码结构、符号、关系和影响范围。
- 编辑前，最终行为判断仍必须读取真实源文件确认。
- 不把大量调用图、文件树、符号图复制进 `.ai` 文件。
- CodeGraph 结果过期或与真实文件冲突时，以真实文件为准，并记录风险。

## 子 Agent

- `/plan` 先执行 Agent Discovery，再基于 Agent Registry 分配 Owner。
- `/plan` 可以咨询子 Agent 做方案分析，但不能执行代码。
- `/do` 按 Task Owner（任务负责人 / 子 Agent 角色）和 `OwnerSource` 调度子 Agent。
- `/check` 的 Static Review Lane 优先匹配 review / code-review / security / quality Agent 做静态审查。
- `/check` 的 Runtime Validation Lane 使用 Codex Browser / Chrome Extension / 项目测试脚本 / Playwright；不得被 code-reviewer 替代。
- 子 Agent 不能扩大 Scope（任务边界）。
- 子 Agent 不能重排 Tasks。
- 子 Agent 不能绕过 Pause Points（暂停点）。
- 子 Agent 输出必须压缩摘要写入 CURRENT / TASKS，不能完整粘贴。

## Agent Discovery

- `/plan` 开始前扫描 `.codex/agents/*.toml`。
- 如果不存在，再扫描 `.agents/agents/*.toml`。
- 从 TOML 的 `name` / `description` 生成 Agent Registry。
- 不硬编码固定 Agent 名称。
- Task Owner 只能来自 Agent Registry 或 `main`。

## Agent Matching

- Java / Spring / backend / SQL / transaction / permission / tenant：匹配 `java`、`backend`、`spring`、`architect`、`sql`、`database`。
- Vue / frontend / UI / component / CSS：匹配 `frontend`、`vue`、`ui`、`component`。
- TypeScript / type / API typing：匹配 `typescript`、`ts`、`type`。
- Static review / security / quality：匹配 `review`、`code-review`、`security`、`quality`。
- Browser / e2e / runtime / UI validation：匹配 `browser`、`e2e`、`test`、`qa`、`frontend`、`ui`。
- 找不到可信匹配时，`Owner = main`，`OwnerSource = main-fallback`，并写明 `OwnerReason`。

# AI 工作流规则

## 主命令

- `/plan`：需求沉淀与方案规划。内部按需加载 `spec.md` 和 `plan.md`。
- `/do`：按 Wave Scheduler 连续执行任务，并自动进行 do/check 循环。内部按需加载 `do.md` 和 `check.md`，必要时加载 `wave-scheduler.md` / `compact.md` / `tooling.md`。
- `/archive`：经验提炼与归档。内部按需加载 `archive.md`、`learn.md` 和 `compact.md`。

日常只使用 `/plan`、`/do`、`/archive`。内部规则分层保存，按需加载，不一次性读取全部规则。

## Lazy Loading：按需加载策略

默认只读取：

- `AGENTS.md`
- `.ai/RULES.md`
- `.ai/CONTEXT.md`
- `.ai/CURRENT.md`
- `.ai/TASKS.md`
- `.ai/MEMORY.md`

默认不要读取：

- `.ai/rules/*.md` 全量
- `.ai/requirements/*.md` 全量
- `.ai/playbooks/*.md` 全量
- `.ai/archive/*.md` 全量

按命令加载：

- `/plan` 只加载 `.ai/rules/spec.md` 和 `.ai/rules/plan.md`。
- `/do` 只加载 `.ai/rules/do.md` 和 `.ai/rules/check.md`；存在 Wave 任务时加载 `.ai/rules/wave-scheduler.md`；需要子 Agent 或 CodeGraph 时再加载 `.ai/rules/tooling.md`；上下文超限时再加载 `.ai/rules/compact.md`。
- `/archive` 只加载 `.ai/rules/archive.md`、`.ai/rules/learn.md` 和 `.ai/rules/compact.md`。

## 文件职责

- `.ai/requirements/*.md`：长期需求、产品规格、业务规则、验收标准。
- `.ai/CURRENT.md`：当前阶段状态摘要，不放长期需求全文。
- `.ai/TASKS.md`：当前任务队列、Owner、Scope、Files、Validation、Short Notes。
- `.ai/HANDOFF.md`：交接摘要。
- `.ai/DECISIONS.md`：长期设计决策。
- `.ai/MEMORY.md`：高价值、短小、可复用经验。
- `.ai/playbooks/*.md`：可复用排错手册。
- `.ai/archive/*.md`：历史执行过程、验证摘要、失败原因、完整归档。
- `.ai/tmp/`：临时过程文件。
- `.ai/artifacts/`：验证产物、截图、报告、日志摘要。
- `.ai/rules/*.md`：工作流规则，按需加载。

## 核心约束

- 默认中文回答；代码、变量名、方法名保持英文。
- 先理解需求和现有实现，再修改代码。
- 保持 minimal diff，不做无关重构。
- 不升级依赖、不修改数据库结构或 migration，除非用户明确确认。
- 遵守项目 i18n、UTC、权限、租户和数据库规则。
- build/test/lint 需要授权；未执行不能声称通过。
- 不把长日志、完整 trace、完整 build/test 输出写入 CURRENT / TASKS / MEMORY。
- 不确定内容写 TODO，不猜测不存在的框架能力。
- `/plan` 生成任务内容中文为主，字段名、Agent 名、命令、路径、状态值和专业术语保留英文。
- `/do` 支持 Wave / Barrier；不支持 true parallel subagents 时，顺序执行但保留 Wave / Barrier 语义。

## AGENTS.md 建议片段

```md
## AI Workflow

本项目使用 `amu-workflow` Skill。

日常主命令：
- `/plan`：需求沉淀 + 方案拆解 + Owner 分配
- `/do`：按 Wave Scheduler 连续执行 + 自动 check + 必要 compact
- `/archive`：learn + archive + final compact

规则：
- `.ai/**/*.md` 正文默认中文。
- 不全量读取 archive/playbooks/requirements。
- 按需加载规则。
- 不把 CURRENT/TASKS 写成知识库。
```

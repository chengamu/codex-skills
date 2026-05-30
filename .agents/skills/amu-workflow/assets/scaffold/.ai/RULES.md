# AI 工作流规则

本项目使用轻量工程化 AI workflow。

## 主命令

- `/plan`：需求沉淀 + 方案拆解 + Owner 分配。
- `/do`：按 Wave Scheduler 连续执行 + 自动 check + 必要 compact。
- `/archive`：learn + archive + final compact。

## 默认读取

- `AGENTS.md`
- `.ai/RULES.md`
- `.ai/CONTEXT.md`
- `.ai/CURRENT.md`
- `.ai/TASKS.md`
- `.ai/MEMORY.md`

## 按需加载

- `/plan`：只加载 `.ai/rules/spec.md` + `.ai/rules/plan.md`。
- `/do`：只加载 `.ai/rules/do.md` + `.ai/rules/check.md`，存在 Wave 任务时加载 `.ai/rules/wave-scheduler.md`，必要时加载 `.ai/rules/tooling.md` / `.ai/rules/compact.md`。
- `/archive`：只加载 `.ai/rules/archive.md` + `.ai/rules/learn.md` + `.ai/rules/compact.md`。

## 文件职责

- `.ai/requirements/*.md`：长期需求。
- `.ai/CURRENT.md`：当前状态摘要。
- `.ai/TASKS.md`：当前任务队列。
- `.ai/HANDOFF.md`：交接摘要。
- `.ai/DECISIONS.md`：长期决策。
- `.ai/MEMORY.md`：短小可复用经验。
- `.ai/playbooks/*.md`：排错手册。
- `.ai/archive/*.md`：历史归档。

## 约束

- `.ai/**/*.md` 正文默认中文。
- 不全量读取 archive/playbooks/requirements。
- 不把 CURRENT/TASKS 写成知识库。
- 不把 MEMORY 写成长日志库。
- 未执行的验证不得声称通过。
- `/plan` 生成任务内容中文为主，字段名、Agent 名、命令、路径、状态值和专业术语保留英文。
- `/do` 支持 Wave / Barrier；不支持 true parallel subagents 时，顺序执行但保留 Wave / Barrier 语义。

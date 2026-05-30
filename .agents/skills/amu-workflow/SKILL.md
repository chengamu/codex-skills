---
name: amu-workflow
description: 轻量工程化 AI workflow。用于需要 Codex 按 /plan、/do、/archive 三个入口完成需求沉淀、计划拆解、连续执行、自动检查、上下文压缩、经验归档的项目。适合中大型前后端工程、Java/Vue/TypeScript 项目、需要可追溯任务队列和子 Agent 协作的场景。不适合一次性简单问答或无需工程化流程的小任务。
---

# AMU Workflow Skill

## 何时使用本 Skill

当用户希望 Codex 按工程化流程处理需求、重构、修复、前后端开发、长期任务时使用。

典型触发词：
- 使用工程化工作流
- 用三段式流程
- /plan
- /do
- /archive
- 需求沉淀
- 任务拆解
- Owner 分配
- do/check 循环
- 经验归档
- playbook

## 不适合使用的情况

- 用户只是问一个概念
- 用户只是要一次性改一小段文案
- 用户明确要求不要创建 .ai 目录
- 用户明确要求不要使用流程

## 快速开始

1. 用户输入 `/plan` 时，先沉淀需求并生成可调度任务计划。
2. 用户确认后输入 `/do`，按 Wave / Barrier 执行任务和检查。
3. 功能阶段完成后输入 `/archive`，归档经验、交接信息和最终上下文。

## 工作流程

`/plan` 负责需求澄清、影响分析和任务拆解；`/do` 负责按计划执行、检查和记录风险；`/archive` 负责经验提炼、归档和交接。

## 主命令

### /plan

执行：
1. 按需读取 `references/rules/spec.md`
2. 按需读取 `references/rules/plan.md`
3. 在目标项目根目录运行 `codegraph sync`
4. 需要 Wave Scheduler 时读取 `references/rules/wave-scheduler.md`
5. 在目标项目创建或更新 .ai/requirements 下的需求文档
6. 生成可调度任务计划，必要时写入当前 change 的 wave-plan.md
7. 更新目标项目的 .ai/CURRENT.md
8. 更新目标项目的 .ai/TASKS.md
9. 停下等待用户确认 `/do`

### /do

执行：
1. 按需读取 `references/rules/do.md`
2. 按需读取 `references/rules/check.md`
3. 需要 Wave Scheduler 时读取 `references/rules/wave-scheduler.md`
4. 需要子 Agent 或 codegraph 时读取 `references/rules/tooling.md`
5. 超限或膨胀时读取 `references/rules/compact.md`
6. 按 Wave / Barrier 执行 do/check 循环
7. 如果本轮 `/do` 修改了代码，Runtime / API / Browser Validation 前在目标项目根目录运行 `codegraph sync`
8. 全部完成后把 Next Step 设置为 `Ready for /archive`

CodeGraph 同步规则：
- `codegraph sync` 用于刷新代码索引，不等同于 build/test/lint。
- sync 后仍要读取真实源文件确认最终结论。
- sync 失败时必须记录失败和风险，不能伪造成功。

### /archive

执行：
1. 按需读取 `references/rules/archive.md`
2. 按需读取 `references/rules/learn.md`
3. 按需读取 `references/rules/compact.md`
4. 提炼经验到目标项目的 .ai/MEMORY.md 或 .ai/playbooks 下的文档
5. 归档到目标项目的 .ai/archive 下的文档
6. 更新目标项目的 .ai/HANDOFF.md
7. final compact

## 按需加载原则

默认只读：
- 目标项目的 AGENTS.md
- 目标项目的 .ai/RULES.md
- 目标项目的 .ai/CONTEXT.md
- 目标项目的 .ai/CURRENT.md
- 目标项目的 .ai/TASKS.md
- 目标项目的 .ai/MEMORY.md

不要默认全量读取：
- .ai/rules 下的规则文档
- .ai/requirements 下的需求文档
- .ai/playbooks 下的经验文档
- .ai/archive 下的归档文档

按命令加载：
- `/plan` 只加载 spec + plan，生成 Wave 任务时再加载 wave-scheduler
- `/do` 只加载 do + check，必要时加载 wave-scheduler / compact / tooling
- `/archive` 只加载 archive + learn + compact

## Wave Scheduler

`Wave Scheduler` 是 `/do` 的轻量调度增强，不引入平台、服务端、数据库或额外 runtime。

- `/plan` 必须生成可调度任务，任务包含 `TaskId`、`Title`、`Owner`、`AgentRole`、`Wave`、`DependsOn`、`Files`、`Forbidden`、`ParallelGroup`、`ConflictBoundary`、`Acceptance`、`RiskLevel`。
- `/do` 不把任务当作 flat checklist 顺序执行，而是按 Wave 执行：Wave 0 -> Barrier 0 -> Wave 1 -> Barrier 1。
- 同一 Wave 内任务如果依赖已完成、Files 不重叠、Forbidden / ConflictBoundary 明确、Acceptance 可验证，可以分配给多个 subagent。
- 当前环境支持 true parallel subagents 时，同一 Wave 内并行 dispatch。
- 当前环境不支持 true parallel subagents 时，使用 sequential execution with Wave/Barrier semantics：顺序执行，但严格保留 Wave 和 Barrier 语义。
- `code-reviewer` 不和 implementation tasks 放在同一 Wave；审计默认放在 Wave 3。
- build/test/lint/browser/api validation 默认属于 `/check`，除非任务明确允许在 `/do` 做 targeted checks。

## 语言规则

面向人的内容必须中文，包括 Task 标题说明、Task 描述、Acceptance 解释、RiskLevel 原因、Barrier 检查说明、handoff summary、review summary、check summary、`/plan` 任务说明和 `/do` 状态总结。

以下内容保留英文：

- 命令：`/spec`、`/plan`、`/do`、`/check`、`/archive`
- 字段名：`TaskId`、`Title`、`Owner`、`AgentRole`、`Wave`、`DependsOn`、`Files`、`Forbidden`、`ParallelGroup`、`ConflictBoundary`、`Acceptance`、`RiskLevel`、`Status`、`Priority`
- Agent 名称：`java-architect`、`frontend-developer`、`typescript-pro`、`code-reviewer`
- 状态值：`pending`、`claimed`、`running`、`done`、`blocked`、`failed`
- 执行概念：`Wave Scheduler`、`Barrier`、`Worktree`、`subagent`、`orchestrator`、`contract`、`DTO`、`VO`、`BO`、`API`、`enum`、`pagination`、`tenant`、`permission`
- 文件路径、类名、方法名、变量名、配置名

wave-plan.md 字段名使用英文，字段内容优先中文。不允许生成整篇英文版 PLAN，不允许把中文项目需求改写成英文需求。

## 安装到新项目

如果目标项目没有 .ai 目录，先使用 `assets/scaffold/.ai/` 初始化。

不得覆盖目标项目已有的 .ai/requirements 文档、.ai/archive 文档、.ai/MEMORY.md、.ai/DECISIONS.md、.ai/HANDOFF.md。

已有文件冲突时：
- 优先备份为 `.bak`
- 或只补充缺失段落
- 不得直接覆盖用户长期资产

可使用脚本：

```powershell
python .\scripts\install-skill.py D:\path\to\project
```

```powershell
.\scripts\install-skill.ps1 -TargetPath D:\path\to\project
```

```bash
./scripts/install-skill.sh /path/to/project
```

## 文档语言规则

- .ai 下的 Markdown 正文默认中文。
- 命令名、文件名、目录名、Owner 名称、技术术语可以保留英文。
- `/plan` 生成的任务内容中文为主，字段名、Agent 名、路径、状态值和专业术语保留英文。
- 不允许整篇规则文档变成英文。

## AGENTS.md 使用建议

在其他项目使用本 Skill 时，建议在项目 AGENTS.md 中加入：

```md
## AI Workflow

本项目使用 `amu-workflow` Skill。

日常主命令：
- `/plan`：需求沉淀 + 方案拆解 + Owner 分配
- `/do`：按 Wave Scheduler 连续执行 + 自动 check + 必要 compact
- `/archive`：learn + archive + final compact

规则：
- .ai 下的 Markdown 正文默认中文。
- 不全量读取 archive/playbooks/requirements。
- 按需加载规则。
- 不把 CURRENT/TASKS 写成知识库。
```

## 资源导航

- 详细规则：`references/rules/`
- Wave Scheduler：`references/rules/wave-scheduler.md`
- 初始模板：`references/templates/`
- 通用 playbooks：`references/playbooks/`
- 可复制 scaffold：`assets/scaffold/.ai/`
- 安装脚本：`scripts/install-skill.ps1`、`scripts/install-skill.sh`

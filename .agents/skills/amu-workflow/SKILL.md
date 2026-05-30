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
- 用户明确要求不要创建 `.ai`
- 用户明确要求不要使用流程

## 主命令

### /plan

执行：
1. 按需读取 `references/rules/spec.md`
2. 按需读取 `references/rules/plan.md`
3. 在目标项目根目录运行 `codegraph sync`
4. 在目标项目创建或更新 `.ai/requirements/*.md`
5. 更新 `.ai/CURRENT.md`
6. 更新 `.ai/TASKS.md`
7. 停下等待用户确认 `/do`

### /do

执行：
1. 按需读取 `references/rules/do.md`
2. 按需读取 `references/rules/check.md`
3. 需要子 Agent 或 codegraph 时读取 `references/rules/tooling.md`
4. 超限或膨胀时读取 `references/rules/compact.md`
5. 执行 do/check 循环
6. 如果本轮 `/do` 修改了代码，Runtime / API / Browser Validation 前在目标项目根目录运行 `codegraph sync`
7. 全部完成后把 Next Step 设置为 `Ready for /archive`

CodeGraph 同步规则：
- `codegraph sync` 用于刷新代码索引，不等同于 build/test/lint。
- sync 后仍要读取真实源文件确认最终结论。
- sync 失败时必须记录失败和风险，不能伪造成功。

### /archive

执行：
1. 按需读取 `references/rules/archive.md`
2. 按需读取 `references/rules/learn.md`
3. 按需读取 `references/rules/compact.md`
4. 提炼经验到 `.ai/MEMORY.md` 或 `.ai/playbooks/*.md`
5. 归档到 `.ai/archive/*.md`
6. 更新 `.ai/HANDOFF.md`
7. final compact

## 按需加载原则

默认只读：
- 目标项目的 `AGENTS.md`
- 目标项目的 `.ai/RULES.md`
- 目标项目的 `.ai/CONTEXT.md`
- 目标项目的 `.ai/CURRENT.md`
- 目标项目的 `.ai/TASKS.md`
- 目标项目的 `.ai/MEMORY.md`

不要默认全量读取：
- `.ai/rules/*.md`
- `.ai/requirements/*.md`
- `.ai/playbooks/*.md`
- `.ai/archive/*.md`

按命令加载：
- `/plan` 只加载 spec + plan
- `/do` 只加载 do + check，必要时加载 compact/tooling
- `/archive` 只加载 archive + learn + compact

## 安装到新项目

如果目标项目没有 `.ai` 目录，先使用 `assets/scaffold/.ai/` 初始化。

不得覆盖目标项目已有的 `.ai/requirements/*.md`、`.ai/archive/*.md`、`.ai/MEMORY.md`、`.ai/DECISIONS.md`、`.ai/HANDOFF.md`。

已有文件冲突时：
- 优先备份为 `.bak`
- 或只补充缺失段落
- 不得直接覆盖用户长期资产

可使用脚本：

```powershell
.\scripts\install-skill.ps1 -TargetPath D:\path\to\project
```

```bash
./scripts/install-skill.sh /path/to/project
```

## 文档语言规则

- `.ai/**/*.md` 正文默认中文。
- 命令名、文件名、目录名、Owner 名称、技术术语可以保留英文。
- 不允许整篇规则文档变成英文。

## AGENTS.md 使用建议

在其他项目使用本 Skill 时，建议在项目 `AGENTS.md` 中加入：

```md
## AI Workflow

本项目使用 `amu-workflow` Skill。

日常主命令：
- `/plan`：需求沉淀 + 方案拆解 + Owner 分配
- `/do`：连续执行 + 自动 check + 必要 compact
- `/archive`：learn + archive + final compact

规则：
- `.ai/**/*.md` 正文默认中文。
- 不全量读取 archive/playbooks/requirements。
- 按需加载规则。
- 不把 CURRENT/TASKS 写成知识库。
```

## 资源导航

- 详细规则：`references/rules/`
- 初始模板：`references/templates/`
- 通用 playbooks：`references/playbooks/`
- 可复制 scaffold：`assets/scaffold/.ai/`
- 安装脚本：`scripts/install-skill.ps1`、`scripts/install-skill.sh`

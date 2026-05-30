# Wave Scheduler 规则

Wave Scheduler 是 `/do` 的轻量调度规则。它不引入复杂平台、服务端、数据库或额外 runtime。

## 语言规则

面向人的内容必须中文，包括 Task 标题说明、Acceptance 解释、RiskLevel 原因、Barrier 检查说明、handoff summary、review summary、check summary 和 `/do` 状态总结。

以下内容保留英文：命令名、字段名、Agent 名、状态值、路径、类名、方法名、`Wave Scheduler`、`Barrier`、`Worktree`、`subagent`、`orchestrator`、`contract`、`DTO`、`VO`、`BO`、`API`、`enum`、`pagination`、`tenant`、`permission`。

`wave-plan.md` 字段名使用英文，字段内容优先中文。不允许生成整篇英文版 PLAN。

## Task 必填字段

每个 Task 必须包含：

- `TaskId`
- `Title`
- `Owner`
- `OwnerSource`
- `OwnerReason`
- `AgentRole`
- `Wave`
- `DependsOn`
- `Files`
- `Forbidden`
- `ParallelGroup`
- `ConflictBoundary`
- `Acceptance`
- `RiskLevel`
- `Status`
- `Priority`

## 默认 Wave 模型

### Wave 0: Contract / Scope / File Boundary

用于确认 `API contract`、`DTO` / `VO` / `BO` fields、`enum`、date / timezone、`pagination`、`tenant` / `permission` boundary、DB schema boundary、frontend/backend field mapping。

目标是减少前后端并行开发时的 contract 不一致。

### Wave 1: Independent Implementation

可以并行执行 backend implementation、frontend implementation、database migration、i18n message update、docs / config update。

前提是 `Files` 不重叠，`Forbidden` 明确，`ConflictBoundary` 明确。

### Wave 2: Integration Alignment

用于对齐 frontend API types、backend DTO/VO、enum mapping、date format、page response、error message、permissions。

### Wave 3: Code Review / Security Review

使用匹配到的 review / code-review / security / quality Agent 做真实风险审计。

重点检查 permission、transaction、SQL、NPE、exception handling、logging、DTO/VO/Entity boundary、tenant/data permission、soft delete、pagination、index impact、API contract mismatch、TypeScript type safety、duplicate submit、XSS、SQL injection、privilege escalation、sensitive data leakage。

### Wave 4: Check / Validation

进入 `/check` 阶段，处理 build、test、lint、browser validation、API validation、regression check。

## `/do` 执行步骤

### Step 1: Load context

只加载必要文件：

1. `.ai/CURRENT.md`
2. 当前 change 的 `proposal.md`
3. 当前 change 的 `design.md`
4. 当前 change 的 `tasks.md`
5. 当前 change 的 `wave-plan.md`
6. `.ai/rules/wave-scheduler.md`

没有 change 目录时，使用 `.ai/TASKS.md` 和 CURRENT 引用的 requirement source。不要默认读取 archived changes。

### Step 2: Build runnable task set

当前 Wave 中可执行任务必须满足：

- `Status` 是 `pending`。
- `DependsOn` 为空，或所有依赖均为 `done`。
- `Files` 不与另一个 runnable task 重叠。
- `Forbidden` 路径明确。
- `ConflictBoundary` 明确。
- `Acceptance` 可验证。

### Step 3: Dispatch subagents

如果当前环境支持 true parallel subagents：

- 将同一 Wave 的 runnable tasks 分配给不同 subagent。
- 只传递 task description、相关 spec/design、允许的 `Files`、`Forbidden`、`Acceptance` 和 `ConflictBoundary`。
- 不传递不必要的完整项目上下文。

如果当前环境不支持 true parallel subagents：

- 顺序执行 runnable tasks。
- 保留 Wave / Barrier 语义。
- 当前 Barrier 通过前，不进入下一 Wave。

### Step 4: Worktree isolation

代码修改任务优先使用：

`.worktrees/<task-id>-<slug>/`

每个 subagent 必须：

- 只在自己的 Worktree 中工作。
- 只修改允许的 `Files`。
- 避免无关格式化。
- 避免依赖升级，除非明确允许。
- 避免扩大 Scope。

orchestrator 才能合并 diff。

### Step 5: Barrier

当前 Wave 的 runnable tasks 完成后：

1. collect diffs。
2. 检查 file overlap。
3. 检查 Forbidden path violation。
4. 检查 Acceptance criteria。
5. 记录 task events。
6. 更新 task statuses。
7. 已授权时运行 targeted checks。
8. 只在 Barrier 通过后进入下一 Wave。

### Step 6: Failure handling

任务 blocked 时：

- 标记为 `blocked`。
- 在 `task-events.jsonl` 记录中文原因。
- 如果安全，可以继续同一 Wave 中无关任务。
- 不猜测缺失业务决策。
- 不通过扩大 Scope 绕过阻塞。

Barrier 失败时：

- 不进入下一 Wave。
- 只修复失败项。
- 重新执行 Barrier。

## `task-events.jsonl`

不需要复杂数据库。每个 change 可以维护一个 `task-events.jsonl`，只记录关键事件，用于恢复上下文、审计执行过程、避免重复执行。

`summary`、`reason` 等面向人的内容必须中文。

支持事件类型：

- `task_created`
- `task_claimed`
- `task_started`
- `task_done`
- `task_blocked`
- `task_failed`
- `barrier_started`
- `barrier_passed`
- `barrier_failed`
- `review_started`
- `review_done`

示例：

```jsonl
{"ts":"2026-05-30T10:00:00+08:00","event":"task_created","task":"C1","owner":"backend-agent","wave":0}
{"ts":"2026-05-30T10:02:00+08:00","event":"task_done","task":"C1","agent":"backend-agent","summary":"已定义 API contract 与前后端字段边界"}
{"ts":"2026-05-30T10:03:00+08:00","event":"task_claimed","task":"B1","agent":"backend-agent","wave":1}
{"ts":"2026-05-30T10:09:10+08:00","event":"task_blocked","task":"F1","agent":"frontend-agent","reason":"backend response 字段名不明确，无法继续对齐前端类型"}
{"ts":"2026-05-30T10:11:00+08:00","event":"barrier_passed","wave":1,"summary":"未发现 Files 重叠或 Forbidden 路径违规"}
```

## `wave-plan.md` 结构

`wave-plan.md` 字段名必须保留英文，字段内容优先中文。

```md
# Wave Plan

## Execution Mode

- Mode: wave-scheduler
- MaxParallelAgents: 3
- UseWorktree: true
- ConflictPolicy: fail-fast
- MergePolicy: orchestrator-only

## Wave 0: Contract / Scope / File Boundary

### Task C1: 定义 API contract 与前后端字段边界

Owner: <backend-agent-from-registry>
OwnerSource: agent-registry
OwnerReason: 该任务需要确认后端 BO/DTO、VO 和 API contract，匹配后端架构类 Agent。
AgentRole: contract
Status: pending
Priority: high
RiskLevel: high
Wave: 0

Files:
- backend/src/main/java/**/dto/**
- backend/src/main/java/**/vo/**
- admin-ui/src/api/**
- admin-ui/src/types/**

Forbidden:
- package.json
- pom.xml
- .ai/archive/**

DependsOn: none
ParallelGroup: contract
ConflictBoundary: contract-only

Acceptance:
- 明确 frontend request fields 与 backend BO/DTO 的对应关系
- 明确 backend response fields 与 frontend usage 的对应关系
- 明确 enum/date/page structures
- 明确 tenant/permission boundary

## Barrier 0

Checks:
- API contract 字段已明确
- 不存在未解决的 frontend/backend field mismatch
- 不存在未明确的 tenant 或 permission boundary
- 不进入 Wave 1，直到 Barrier 0 通过
```

## 文件和目录控制

- `/do` 或 `/check` 产生的临时文件优先放在 `.ai/changes/<change-id>/tmp/`。
- 日志摘要放 `.ai/changes/<change-id>/logs/`。
- 验证产物放 `.ai/changes/<change-id>/artifacts/`。
- 禁止把临时验证产物散落在 `.ai/` 根目录。
- 归档时只保留必要产物：`proposal.md`、`design.md`、`tasks.md`、`wave-plan.md`、`handoff.md`、`review.md`、`check.md`、`task-events.jsonl`。
- 无用 tmp / log / artifacts 可在 archive 或 prune 时清理。

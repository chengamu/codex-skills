# 计划规则

`/plan = spec + plan`

Plan（计划）必须以 requirement source（需求来源）为前提。如果没有需求来源，先加载 `spec.md`，创建或更新需求文件，再创建任务。

## 执行流程

1. 读取默认上下文。
2. 在项目根目录运行 `codegraph sync`，刷新代码索引。
3. sync 成功后继续；sync 失败时记录失败原因和风险，不能伪造索引已更新。
4. 需求不清或缺少需求来源时，加载 `spec.md`。
5. 创建或更新 `.ai/requirements/*.md`。
6. 读取当前 requirement source（需求来源）。
7. 分析真实代码结构和项目约束。
8. 需要可并行调度时，加载 `wave-scheduler.md`。
9. 只有明确相关时才加载 Playbook（可复用排错手册）。
10. 生成方案拆解。
11. 分配 Owner（任务负责人 / 子 Agent 角色）。
12. 生成可调度任务计划，并写入 `.ai/TASKS.md`；复杂需求可同时生成当前 change 的 `wave-plan.md`。
13. 更新 `.ai/CURRENT.md`。
14. 停止，等待用户确认进入 `/do`。

## CodeGraph 同步

`/plan` 开始分析代码结构前，必须在项目根目录运行：

```bash
codegraph sync
```

- `codegraph sync` 用于刷新代码索引，保证后续 CodeGraph 查询尽量基于最新代码。
- `codegraph sync` 不等同于 build/test/lint。
- sync 后仍要读取真实源文件确认最终结论。
- sync 失败时，必须在 CURRENT / TASKS 中记录风险；不能假装已同步成功。

## Clarification Gate：澄清门

生成详细计划前，先判断需求是否足够明确：

- 目标和 Scope（任务边界）是否明确。
- 关键业务规则是否明确。
- 数据库、权限、i18n、UTC 影响是否清楚。
- 涉及异步 / 同步、分页、导出、筛选、兼容性、性能时，预期是否清楚。

如果不明确，不创建任务。只记录当前理解、可选方案、风险，并提出最少必要问题。

## 方案与推荐

多方向需求必须包含：

- Option A：方案 A
- Option B：方案 B
- Recommendation：推荐方案
- Trade-offs：取舍
- Risks：风险

简单需求可以只记录推荐方案和理由。

## Plan Revision：计划修订

出现以下情况时，必须回到 `/plan`，并更新 `.ai/CURRENT.md` / `.ai/TASKS.md`：

- Scope（任务边界）或需求变化。
- 任务顺序变化。
- 原方案不可行。
- 出现新的技术约束。
- 出现新的数据库、i18n、UTC、权限影响。

必须记录原计划、修订原因、新计划、影响范围、Acceptance Criteria（验收标准）变化和 Risks（风险）变化。

## Owner 分配

允许的 Owner：

- `main`：跨领域协调、工作流规则、简单任务。
- `frontend-developer`：前端页面、组件、样式、交互。
- `typescript-pro`：TypeScript 类型和复杂 TS 逻辑。
- `java-architect`：Java 后端、Service、Mapper、权限、事务、架构影响。
- `code-reviewer`：最终静态审查和验收。

## Wave Scheduler 任务要求

`/plan` 生成任务时，必须让任务可被 `/do` 调度。复杂需求默认使用 Wave Scheduler。

每个 Task 必须包含：

- `TaskId`
- `Title`
- `Owner`
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

字段名、Agent 名、路径、状态值和专业术语保留英文；Task 标题、说明、Acceptance、RiskLevel 原因、Barrier Checks 必须中文为主。

默认 Wave 模型：

- Wave 0：确认 `API contract`、`DTO` / `VO` / `BO` 字段、`enum`、日期 / 时区、`pagination`、`tenant` / `permission` 边界、DB schema 边界、前后端字段映射。
- Wave 1：独立实现，可包含 backend、frontend、database migration、i18n message、docs / config；前提是 `Files` 不重叠，`ConflictBoundary` 明确。
- Wave 2：集成对齐，校准 frontend API types、backend DTO/VO、enum、date format、page response、error message、permissions。
- Wave 3：Code Review / Security Review，使用 `code-reviewer` 做真实风险审计。
- Wave 4：进入 `/check`，执行 build、test、lint、browser validation、API validation、regression check。

`code-reviewer` 不应和 implementation tasks 放在同一 Wave。

## 任务模板

```md
### T001 - <title>

Owner：任务负责人 / 子 Agent 角色
Status：状态，例如 pending / in_progress / done / blocked
DependsOn：依赖任务
Requirement Source：需求来源
Scope：任务边界
Files：预计相关文件
Validation：验证方式
Blockers：阻塞项
Short Notes：简短记录
```

Wave Scheduler 任务示例：

```md
### Task B1: 实现后端接口与服务逻辑

Owner: java-architect
AgentRole: backend
Status: pending
Priority: high
RiskLevel: high
Wave: 1

Files:
- backend/src/main/java/**/controller/**
- backend/src/main/java/**/service/**
- backend/src/main/resources/mapper/**

Forbidden:
- admin-ui/**
- package.json
- pom.xml
- .ai/archive/**

DependsOn:
- C1

ParallelGroup: backend
ConflictBoundary: backend-only

Acceptance:
- API 必须实现 Wave 0 定义的 contract
- 写操作必须在需要时具备 transaction 边界
- 必须遵守 tenant/data permission
- 不允许引入 raw SQL injection 风险
- 异常信息必须对用户安全，必要时兼容 i18n
```

## CURRENT 模板

`.ai/CURRENT.md` 只保存当前执行上下文：

```md
# Current

## Current Goal：当前目标

## Requirement Source：需求来源

## Current Phase：当前阶段

## Scope：范围

## Out of Scope：不做范围

## Key Decisions：关键决策

## Active Tasks：当前任务

## Risks / Pause Points：风险 / 暂停点

## Validation Plan：验证计划

## Next Step：下一步
```

## Plan 必须包含

- Requirement Source（需求来源）。
- Options（可选方案）。
- Recommendation（推荐方案）。
- Trade-offs（取舍）。
- Risks（风险）。
- Pause Points（暂停点）。
- Owner Assignment（负责人分配）。
- Task Breakdown（任务拆解）。

## Plan 禁止

- 修改业务代码。
- 运行 build/test/lint。
- 执行任务。
- 把需求全文放进 CURRENT。
- 默认读取所有 archive 或 playbooks。
- 猜测数据库结构、权限策略、i18n、UTC、异步、分页、导出、筛选规则。

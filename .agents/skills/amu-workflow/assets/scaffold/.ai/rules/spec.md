# 内部需求阶段

Spec（需求阶段）是 `/plan` 内部加载的前置阶段。

它负责：

- 头脑风暴。
- 发现和澄清需求。
- 探索可选方案。
- 分析风险。
- 比较取舍。
- 确认需求。
- 定义 Acceptance Criteria（验收标准）。
- 沉淀长期需求。

Spec 不生成实现任务。任务只能由 `plan.md` 生成。

## 何时进入 Spec

当 `/plan` 开始时，如果需求不明确，或没有 requirement source（需求来源），必须先进入 Spec 阶段。

Spec 必须：

- 澄清用户目标和 Scope（任务边界）。
- 存在多个方向时，提出 2 到 3 个可选方案。
- 比较优缺点和风险。
- 只提出最少必要问题。
- 需求足够明确后，创建或更新 `.ai/requirements/*.md`。

Spec 禁止：

- 修改业务代码。
- 运行 build/test/lint。
- 生成 `.ai/TASKS.md`。
- 把长期需求全文粘贴进 `.ai/CURRENT.md`。

## 需求沉淀

Requirements（长期需求）是长期资产，不能随意覆盖。

- 同一个 feature（功能）：更新同一个需求文件。
- 新 feature（功能）：创建新的需求文件。
- 建议文件名：`.ai/requirements/YYYYMMDD-feature-name.md`。

## 需求模板

```md
# Requirement: <feature>

## Goal：目标

## Background：背景

## Scope：范围

## Out of Scope：不做范围

## User Stories / Use Cases：用户故事 / 使用场景

## Business Rules：业务规则

## UX / UI Requirements：交互 / 界面要求

## API Requirements：接口要求

## Data Requirements：数据要求

## Permission / Tenant Rules：权限 / 租户规则

## i18n / UTC Rules：国际化 / 时间规则

## Options：可选方案

### Option A：方案 A
Pros：优点
Cons：缺点

### Option B：方案 B
Pros：优点
Cons：缺点

## Recommended Option：推荐方案

## Risks：风险

## Open Questions：待确认问题

## Acceptance Criteria：验收标准

## Related Decisions：相关决策
```

## OpenSpec 风格

需求不明确时：

- 不直接跳到任务拆解。
- 先提出方案和取舍。
- 列出风险。
- 最多询问 3 到 5 个关键问题。
- 将已确认需求沉淀到 `.ai/requirements/`。

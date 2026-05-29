# UTC Playbook

仅在 UTC、时区、日期和时间语义相关问题出现时按需加载。

## 规则

- 遵守 `AGENTS.md` 和 `.ai/CONTEXT.md` 中的 UTC 规则。
- 业务时间和 API 时间不要依赖系统默认时区。
- 时间存储、筛选、展示或 payload 格式变化时，必须在 CURRENT 记录 UTC 影响。

## 待补充

- 重复出现稳定问题后，再补充 UTC 排查步骤。

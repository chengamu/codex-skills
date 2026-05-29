# Playbooks：可复用排错手册

Playbook 是可复用的排错和执行指南。

Playbook 按需加载。

## 加载策略

- `/plan` 只有在明确相关时才读取 Playbook。
- `/do` 在出现具体问题时读取 Playbook。
- `/archive` 可以通过 `learn.md` 更新 Playbook。

## 规则

- 不写任务历史。
- 不写完整日志。
- 不写一次性业务细节。
- 只写稳定步骤、常见坑和约束。

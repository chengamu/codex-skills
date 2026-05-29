# 内部经验提炼阶段

Learn（经验提炼）由 `/archive` 加载。

它在最终归档前提炼可复用经验。

## 职责

- 分析已完成任务。
- 分析失败和修复方式。
- 提炼可复用 lessons（经验）。
- 判断内容应写入 MEMORY、Playbook、Archive，还是忽略。

## 去向规则

- 高价值、短小、跨任务可复用 -> `.ai/MEMORY.md`。
- 稳定排查步骤 -> `.ai/playbooks/*.md`。
- 一次性过程和详细执行历史 -> `.ai/archive/*.md`。
- 纯日志噪音 -> 忽略。

## MEMORY 限制

- 每条建议不超过 10 行。
- 不保存完整日志。
- 不保存完整堆栈。
- 不保存长命令输出。
- 不保存一次性业务流水。

## Playbook 限制

- 写稳定排查步骤。
- 写常见坑。
- 写禁止事项。
- 不写完整日志。
- 不写本次任务流水。

## 示例：Maven 旧 jar / 未 install

问题：

运行或 compile 时发现类 / 方法版本不一致，原因可能是部分 jar 是旧的，或本次未 install 对应模块。

Task Short Note：

疑似旧 jar / 未 install，先验证本地 Maven 产物。

Playbook：

遇到类 / 方法版本不一致，或运行行为和源码不一致时，先检查本地 Maven install 和旧 jar，不要第一时间修改业务逻辑。

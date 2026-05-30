# 内部检查阶段

Check（检查）是 `/do` 内部加载的阶段。

它用于在每个任务或阶段执行后进行验证。

## 职责

- Scope check：检查任务边界。
- Owner boundary check：检查 Owner 边界。
- Requirement acceptance criteria check：检查需求验收标准。
- i18n check：检查国际化。
- UTC / timezone check：检查时间语义。
- permission / tenant check：检查权限 / 租户。
- API / data compatibility check：检查接口 / 数据兼容性。
- build/test/lint result check：检查构建 / 测试 / lint 结果。
- runtime / browser / API verification check：检查运行时 / 浏览器 / API 验证。

## 双 Lane

`/check` 必须拆成两个 lane，不能让静态审查吞掉运行时验证。

### Lane A: Static Review

- 用于代码风险审查。
- 优先从 Agent Registry 匹配 `review` / `code-review` / `security` / `quality` Agent。
- 找不到可信 Agent 时由 main 执行。
- 检查 Java、Vue、TS、SQL、API、权限、事务、安全、contract、可维护性。
- 只做静态代码审查，不做浏览器自动化。

### Lane B: Runtime Validation

- 用于运行时验证。
- 优先使用 Codex in-app Browser / Chrome Extension / 项目测试脚本 / Playwright。
- 也可以从 Agent Registry 匹配 `browser` / `e2e` / `test` / `frontend` / `ui` Agent。
- 检查页面是否能打开、交互是否正常、表单是否可提交、console 是否报错、network / API 是否失败。
- 不允许被 `code-reviewer` 或 Static Review Lane 替代。

## CodeGraph 同步

如果本轮 `/do` 修改了代码，Runtime / API / Browser Validation 前，在项目根目录运行 `codegraph sync`。

- `codegraph sync` 不等同于 build/test/lint。
- sync 只代表索引刷新；确认行为仍要读取真实源文件。
- sync 失败时必须记录失败和风险，不得伪造成功。

## 验证规则

- build/test/lint 未运行时，只能记录 `Not Run` 和原因。
- 页面未打开时，不能写 UI 正常。
- API 未调用时，不能写 API 正常。
- 权限未验证时，不能写权限通过。
- Browser Validation（浏览器验证）优先使用 Codex 内置 Browser / Chrome。
- 浏览器工具不可用时，记录原因和 Remaining Risks（剩余风险）。
- 只保留结果摘要、关键错误、文件位置和产物路径。

## 失败规则

如果 check 失败：

- 不允许 archive。
- 不标记任务为 done。
- 在 TASKS 写入简短 blocker。
- 回到 `/do` 修复。

## 通过规则

如果 check 通过：

- 标记任务 done。
- 更新验证摘要。
- 继续下一个任务。

## Compact 触发

同一任务 do/check 循环重复，或 CURRENT / TASKS 变得过大时，加载 `compact.md`。

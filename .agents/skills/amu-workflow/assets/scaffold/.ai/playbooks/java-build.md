# Java 构建 Playbook

仅在 Maven / Gradle / jar / compile / runtime 问题出现时按需加载。

## 检查项

- 运行构建相关命令前，先确认命令目标、模块和用户授权。
- 如果运行行为和源码不一致，检查本地构建产物是否过期。
- 未确认产物或版本不一致前，不要先修改业务逻辑。
- Java 发布包运行目录应以项目配置或文档为准，不要猜测 jar 位置。

## 常见坑：旧 jar / 未 install

遇到类 / 方法版本不一致，或运行行为和源码不一致时，先检查本地构建产物、依赖缓存和模块安装状态。

## 常见坑：资源打包检查

- 如果 `target/classes` 或 `build/classes` 中有资源，但模块 jar 没有，先比较产物时间，再重新 package/install。
- 检查 Spring Boot fat jar 时，需要按实际结构抽查 `BOOT-INF/classes` 和 `BOOT-INF/lib` 中的模块资源。

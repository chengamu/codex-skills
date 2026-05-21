# Asset Manifest And Prompt Templates

Use these templates only when they help the current UI-to-Vue/image2 task. Keep outputs concise and specific to the project.

## UI Preflight Review

```markdown
## UI 还原前期审查

### 参考图来源
- 用户指定路径/附件：
- 是否存在多个候选参考图：
- 采用的参考图：

### 整体判断
- 页面/组件类型：
- 视觉风格：
- 核心布局：
- 首屏或主视觉重点：
- 主要风险：

### 元素拆分
| 区域 | 实现方式 | 难度 | 原因 | 是否需要确认 |
| --- | --- | --- | --- | --- |
| 顶部导航 | code | 容易 | 文本和控件应可访问 | 否 |
| 首屏主视觉 | image2 | 困难 | 依赖摄影/插画质感 | 是 |
| logo/商标 | 原素材 | 不建议生成 | 需要品牌准确性 | 是 |

### 图片资产候选
| id | UI 位置 | 类型 | 槽位尺寸 | 导出尺寸 | 透明 | 优先级 | 目标路径 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| hero-main | 首屏 | hero-image | 100vw x 60vh | 2880x1600 | 否 | 必须 image2 | src/assets/generated/hero-main.webp |

### 需要确认
- 是否要求像素级复刻，还是允许风格近似？
- 是否有 logo、人物、产品、字体等授权原素材？
- 是否需要桌面端和移动端双适配？
- 是否允许调用项目指定 image2 入口处理用户素材？
- 如果项目内有多张原型图，具体使用哪一张或哪一组？
```

## Image2 Asset Manifest

| id | UI 位置 | 类型 | code/image2 | CSS 槽位 | 导出尺寸 | 比例 | 透明 | 后处理 | 目标路径 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| product-cutout | 商品卡片 | cutout | image2 | 220x260 | 880x1040 | 11:13 | 是 | transparent-png, edge-check | src/assets/generated/product-cutout.png |

Common types: `hero-image`, `thumbnail`, `illustration`, `texture`, `cutout`, `background-plate`, `custom-icon`.

Common post-processing: `crop`, `resize`, `remove-background`, `transparent-png`, `compress-webp`, `mobile-crop`, `edge-check`.

## Image2 Prompt Template

```text
为一个 [Vue 管理端/网站/App] UI 生成 [资产类型]。

用途和位置：
- 用于：[UI 槽位]
- 目标宽高比：[比例]
- 目标导出尺寸：[宽]x[高]
- 是否透明：[是/否]

主体和构图：
- 主体：[主体描述]
- 视角/镜头：[视角]
- 前景与背景关系：[说明]
- 文案留白：[需要给代码文本保留的空间]

风格：
- 类型：[真实摄影/插画/3D/颗粒/半色调/材质纹理]
- 色彩：[主色和辅助色]
- 光照：[方向、强度、阴影]
- 质感：[材质、边缘、颗粒、清晰度]

集成约束：
- 不要出现可读文字、按钮、价格、表单、系统状态栏、logo、水印或 UI chrome
- 边缘干净，适合裁剪或透明抠图
- 与 Element Plus/yudao 风格页面融合，不要过度装饰

避免：
- 伪文字、错别字、随机品牌、变形主体、脏边、白边、硬边、低清晰度
```

For multiple same-style assets, define shared tokens first: palette, lighting, grain density, material, camera angle, line weight, realism level.

## Transparent Asset Template

```markdown
| 文件 | 透明需求 | 检查方式 | 结果 | 页面接入位置 |
| --- | --- | --- | --- | --- |
| src/assets/generated/product-cutout.png | PNG alpha | check-transparent-assets.py + 深浅背景目检 | 待检查 | 商品卡片主图 |
```

Required checks:

- PNG must have an alpha channel or a valid PNG transparency chunk.
- Actual transparent pixels should exist for cutout assets.
- Inspect on light and dark backgrounds for white fringe, hard edge, residual background, and shadow artifacts.
- Record dimensions and alpha result in the final report.

## Vue TS Component Prompt

```text
你是 Vue3 + TypeScript + Element Plus 前端工程师，遵循 yudao/ruoyi 管理端风格。

根据 UI 参考图和资产清单生成可运行 Vue SFC 组件。

要求：
1. 使用 <script setup lang="ts">
2. Props、Emits、Slots、State 全部显式类型
3. 不默认使用 any
4. 文本、按钮、表单、表格、导航用代码渲染
5. image2 生成的真实图片从 src/assets/generated/ 引用
6. 样式使用 scoped SCSS/CSS，避免无必要内联样式
7. 优先使用 Element Plus 与项目已有组件

输入：
ComponentName: {{component_name}}
PropsList: {{props}}
EmitsList: {{emits}}
SlotsList: {{slots}}
ImageAssets: {{image_assets}}

输出：
完整 .vue 文件代码：template、script setup lang="ts"、style scoped。
```

## Vue TS Page Prompt

```text
你是 Vue3 + TypeScript + Pinia + Element Plus 前端工程师，遵循 yudao/ruoyi 管理端页面规范。

生成一个可放入 src/views/ 的页面组件。

要求：
1. 页面结构贴合 app-container、查询表单、表格、分页、弹窗、权限指令、RightToolbar 等项目风格
2. API 调用沿用 src/api/** 和 @/utils/request
3. Query、Form、Table Row、API Response、Dialog State 全部显式类型
4. 图片资源引用本地 src/assets/generated/
5. 若项目缺少 TS 校验基建，最终说明不能声称类型检查已通过

页面名称：{{page_name}}
路由建议：{{route_meta}}
数据接口：{{api_endpoints}}
UI 结构：{{ui_schema}}
ImageAssets: {{image_assets}}

输出：
页面 SFC，以及需要新增/修改的 API 类型说明。
```

## Page Acceptance Checklist

- 真实 image2 资产已经落地为本地文件并接入页面。
- 透明 PNG 已运行 `scripts/check-transparent-assets.py` 或说明无法程序化验证的原因。
- 页面截图能看到生成资产在正确槽位中渲染。
- 文本没有被图片烘焙，且没有溢出、重叠或截断。
- 桌面和移动宽度下图片不拉伸、不压扁、不裁掉主体。
- Element Plus 控件、表格、弹窗和按钮交互可用。
- 未伪造 TS、lint、build、image2 或截图验证结果。

## PC / Desktop Admin Checklist

- 优先还原 PC 桌面布局，不使用手机外框，除非用户明确要求移动端。
- 侧边栏、顶部导航、面包屑、页签、查询区、表格、分页、弹窗、抽屉、操作按钮和工具栏层级清晰。
- yudao/ruoyi 管理端页面优先使用 `app-container`、`el-form` 查询区、`el-table`、`pagination`、`RightToolbar`、权限指令和 `el-dialog`。
- 在 1366、1440、1536、1920 宽度下检查布局；除宽表格外，不应出现异常横向滚动。
- 表格列、筛选项、按钮和弹窗内容保持紧凑可扫读，不做营销页式大卡片堆叠。
- 图表、主视觉或装饰图为本地资产，且不会遮挡表格、筛选区或操作按钮。

## App / iOS Prototype Checklist

- 有完整 iOS 或参考设备外框。
- 屏幕内容在设备内部，窄屏不重叠。
- 明显按钮、返回、关闭、底部导航、卡片和选项可点击或有本地模拟反馈。
- 图片、插画、缩略图是本地资产。
- 至少有一张渲染截图显示完整设备外框和屏幕内容。
- 最终说明包含预览 URL/HTML 路径、截图路径、资产路径和未完成差异。

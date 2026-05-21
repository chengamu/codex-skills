---
name: image2-ui-skill
description: Turn UI screenshots, design references, mobile App mockups, and image-heavy layouts into high-fidelity Vue3 + TypeScript + Element Plus/yudao-style frontend code with real image2 assets. Use when Codex must split a UI into code-rendered controls versus generated bitmap assets, write image2 prompts, create or verify transparent PNG/WebP cutouts, integrate assets into Vue SFC pages or components, build clickable App/iOS previews, and prove the result with rendered screenshots. Must not claim image2 was used unless real files were generated through the project-approved image2 entrypoint and rendered in the page.
---

# Image2 UI Skill

Use this skill to convert UI references into working frontend UI while preserving the original visual intent. The core job is **UI fidelity + real image2 asset workflow**. Vue3, TypeScript, Element Plus, and yudao-style rules are implementation constraints, not a replacement for visual analysis.

## Core Principles

- Inspect every provided UI reference before editing code or generating images.
- Treat UI reference images as task inputs. Use the paths provided by the user or discovered in the current project for that task; do not assume or hard-code a fixed prototype image directory in this skill.
- Split the UI into: code-rendered UI, image2 bitmap assets, icon/vector assets, and transparent cutout assets.
- Keep readable UI text in code: titles, body copy, labels, prices, buttons, navigation, form fields, table content, and dynamic values.
- Use real image2 assets for visual areas that code cannot faithfully reproduce: photography, product renders, people, complex illustration, texture, grain, halftone, map/island art, hero backgrounds, thumbnails, material effects, and transparent cutouts.
- Do not describe CSS gradients, SVG approximations, stock placeholders, or another image model as image2 output.
- Do not switch to `imagegen`, OpenAI image APIs, OpenRouter, custom Python SDKs, or `OPENAI_API_KEY` as a substitute for image2 unless the user explicitly allows an alternative.
- If the project-approved image2 entrypoint cannot be confirmed, say that clearly, complete the UI/asset breakdown, and avoid claiming image2 generation.

## Required Workflow

1. Analyze the reference UI: layout, visual weight, typography, color, shadows, spacing, image slots, responsive behavior, and interaction states.
2. Resolve the reference image source for the current task from the user's specified project path, attached image, or explicit instruction. If multiple plausible files exist, ask which one to use instead of guessing.
3. Produce an asset plan before generation. Include asset id, UI location, type, code-or-image2 decision, target slot size, export size, aspect ratio, transparency need, prompt, post-processing, and target path.
4. Generate only the assets that truly need bitmap generation. Keep structure, controls, and text in Vue code.
5. Post-process generated images as needed: crop, resize, compress, remove background, preserve alpha, and export breakpoint-specific crops.
6. Integrate local files back into the UI, normally under `src/assets/generated/` unless the project has a clearer convention.
7. Render the real page or preview and take screenshots. Verify images appear in their intended slots, are not stretched, and do not cover interactive controls.
8. Final reporting must list generated asset paths, where each asset is used, which regions are still code-rendered, and what screenshot or browser check proved the result.

If any required step is incomplete, describe the exact partial state, for example: "UI structure is implemented; real image2 assets are still pending."

## Transparent PNG / WebP Rules

- Transparent assets must preserve alpha. Do not infer transparency from the filename or from visual appearance alone.
- Use `scripts/check-transparent-assets.py` for PNG assets whenever a transparent cutout is generated or received.
- Check transparent assets on light and dark backgrounds for white edges, hard edges, leftover background, missing alpha, and unnatural shadow boundaries.
- For transparent WebP, use available project/browser/image tooling to verify alpha. If no reliable local checker exists, state that alpha could not be programmatically verified.
- Final reporting for transparent assets must include path, dimensions, alpha result, edge/fringe notes, and the page location where the asset is rendered.

## App / Mobile Prototype Rules

When the user asks for an App, mobile App, iOS preview, clickable App demo, mobile prototype, or the reference clearly shows phone UI:

- Build a clickable preview, not just a static page.
- Include an iOS-style device frame unless the reference uses a different visible device frame.
- Keep App content inside a fixed design canvas or a predictable scaling wrapper so text, buttons, illustrations, and status bars do not overlap on narrow screens.
- Make obvious buttons, back/close controls, bottom navigation, cards, tabs, options, and primary CTAs clickable or locally simulated.
- Produce at least one rendered screenshot that shows the full device frame and screen content.
- Do not claim the App prototype is complete unless the frame, click paths, local assets, and screenshot verification are done.

## PC / Desktop Web Rules

When the user asks for PC, desktop, web admin, backend management UI, dashboard, large-screen page, or the reference clearly shows a desktop browser/admin layout:

- Build the desktop experience first. Do not wrap it in a phone frame or force mobile App behavior.
- Preserve desktop information density: sidebar, top navigation, breadcrumbs, tabs, filter forms, data tables, cards, charts, dialogs, drawers, and action toolbars.
- For yudao/ruoyi-style management pages, prefer existing desktop conventions: `app-container`, `el-row` / `el-col`, inline query forms, `el-table`, `pagination`, `RightToolbar`, permission directives, and `el-dialog`.
- Keep PC layouts usable at common widths: 1366, 1440, 1536, and 1920. Important content must not overlap, collapse unexpectedly, or require horizontal scrolling unless the source UI is explicitly a wide data table.
- For data-heavy pages, optimize for scanning and repeated operation: compact spacing, aligned columns, clear search/reset actions, stable table heights, and predictable dialogs.
- If a reference includes both desktop and mobile states, implement desktop and mobile as separate responsive states and verify both. Do not let App/iOS rules override PC rules.

## Vue3 + TypeScript + Yudao Implementation Rules

Before writing Vue code, inspect the actual project:

- `package.json` for Vue, Element Plus, Pinia, TypeScript, lint, and type-check tooling.
- `src/views` for page conventions such as `app-container`, query forms, tables, dialogs, pagination, permissions, and `RightToolbar`.
- `src/api` and `@/utils/request` for API style.
- `src/router` for route and `meta` shape.
- `src/store` for Pinia store patterns.

When generating Vue code:

- Prefer single-file components with `<script setup lang="ts">`.
- Explicitly type props, emits, slots, query params, form models, table rows, API responses, and local state.
- Avoid `any`. If it is unavoidable, keep it local and explain why.
- Use Element Plus components and the project's existing global components before inventing custom controls.
- Follow yudao/ruoyi admin page shape for management screens: `app-container`, `el-form` search area, `el-table`, `pagination`, `el-dialog`, permission directives, and toolbar patterns when relevant.
- Keep API calls in `src/api/**` using the existing request wrapper. Do not create a new HTTP layer.
- Do not add dependencies, convert the project to TypeScript, change backend code, modify migrations, or change production configuration unless the user explicitly requests it.
- If the project lacks `tsconfig`, `vue-tsc`, ESLint, Prettier, or type-check scripts, do not pretend those checks passed. Say which checks were unavailable.

## Visual Quality Checks

Review the complete page, not only individual files:

- Text must not overflow buttons, cards, table cells, or mobile containers.
- Images must keep stable dimensions, correct aspect ratio, and appropriate `object-fit` / `object-position`.
- Generated images must not contain fake readable text, fake logos, watermarks, broken hands/faces, random UI chrome, or unintended labels.
- Lighting, shadow, perspective, edge quality, saturation, and grain should match the surrounding code-rendered UI.
- Interactive controls must remain clickable and must not be blocked by generated image layers.
- Check desktop and mobile widths when the target UI is responsive.
- Compare the final screenshot with the original reference and fix high-impact differences before reporting completion.

## References And Scripts

- Read `references/asset-manifest-and-prompts.md` when building the UI review, image2 asset manifest, Vue TS component/page prompt, or acceptance checklist.
- Run `scripts/check-transparent-assets.py` for PNG transparency verification:

```powershell
python C:\Users\Administrator\.codex\skills\image2_UI_skill\scripts\check-transparent-assets.py path\to\asset.png
```

The script is a verifier only. It does not generate images and does not replace the project-approved image2 entrypoint.

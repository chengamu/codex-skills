# Codex Agents And Skills

This repository stores shared Codex subagents and skills for team use.

## Contents

- `.codex/agents/python-pro.toml`
- `.codex/agents/typescript-pro.toml`
- `.codex/agents/frontend-developer.toml`
- `.codex/agents/code-reviewer.toml`
- `.codex/agents/accessibility-tester.toml`
- `.codex/agents/java-architect.toml`
- `.codex/skills/ssh-key-deploy`
- `.codex/skills/image2_UI_skill`
- `.agents/skills/amu-workflow`

The subagent TOML files are sourced from:

- <https://github.com/VoltAgent/awesome-codex-subagents>

## Install Globally

Run from this repository root:

```powershell
New-Item -ItemType Directory -Force -Path $HOME\.codex\agents, $HOME\.codex\skills | Out-Null
Copy-Item -Recurse -Force .\.codex\agents\* $HOME\.codex\agents\
Copy-Item -Recurse -Force .\.codex\skills\* $HOME\.codex\skills\
New-Item -ItemType Directory -Force -Path $HOME\.agents\skills | Out-Null
Copy-Item -Recurse -Force .\.agents\skills\amu-workflow $HOME\.agents\skills\
```

Restart Codex after installing.

## Install Into One Project

Run from this repository root and replace `<PROJECT_PATH>`:

```powershell
New-Item -ItemType Directory -Force -Path <PROJECT_PATH>\.codex\agents, <PROJECT_PATH>\.codex\skills | Out-Null
Copy-Item -Recurse -Force .\.codex\agents\* <PROJECT_PATH>\.codex\agents\
Copy-Item -Recurse -Force .\.codex\skills\* <PROJECT_PATH>\.codex\skills\
New-Item -ItemType Directory -Force -Path <PROJECT_PATH>\.agents\skills | Out-Null
Copy-Item -Recurse -Force .\.agents\skills\amu-workflow <PROJECT_PATH>\.agents\skills\
```

Project-level `.codex` files override global files with the same names.

## Usage Examples

Ask Codex to use a subagent explicitly:

```text
请使用 python-pro 子agent 修改这个 Python bug，只改相关文件。完成后让 code-reviewer 子agent 审核 diff。
```

```text
请使用 frontend-developer 子agent 实现这个前端页面，再让 typescript-pro 子agent 检查类型风险，最后让 accessibility-tester 子agent 做可访问性验证。
```

Skills are triggered by matching tasks. For example:

```text
使用 ssh-key-deploy skill 帮我配置到这台服务器的 SSH key 登录。
```

```text
使用 image2-ui-skill 根据这张 UI 参考图实现 Vue3 + TypeScript 页面。
```

## Notes

- `code-reviewer` and `accessibility-tester` are read-only agents and are suitable for verification.
- `python-pro`, `typescript-pro`, `frontend-developer`, and `java-architect` can write files. Avoid asking multiple writing agents to edit the same files at the same time.
- Do not commit private keys, API keys, tokens, passwords, or production configuration into this repository.

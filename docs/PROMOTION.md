# Promotion Kit

Use this page when presenting the project outside the repository. It keeps the
public description accurate and avoids overstating what the workflow pack does.

## GitHub About

Description:

```text
Workflow pack for turning vague ideas into bounded, verified AI coding loops with durable state.
```

Website:

```text
https://github.com/zq88577727/loop-engineering-skill/releases/tag/v0.4.2
```

## Suggested topics

```text
codex
codex-skill
ai-workflow
agent-workflow
developer-tools
state-management
software-engineering
workflow-automation
prompt-engineering
ai-coding
```

## Launch post

Short English version:

```text
I released Loop Engineering v0.4.2, a workflow pack for turning vague ideas into
bounded, verified AI coding loops.

Codex users can install it as a skill. Cursor, Claude Code, Gemini CLI, ChatGPT,
JetBrains AI, and other AI coding tools can use the Portable Prompt Pack.

Codex install:
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo zq88577727/loop-engineering-skill \
  --ref v0.4.2 \
  --path skills/loop-engineering

Portable path:
copy portable/LOOP_ENGINEERING_PROMPT.md and portable/STATE_TEMPLATE/ into your project.
```

Short Chinese version:

```text
我发布了 Loop Engineering v0.4.2。它现在不只是 Codex skill，而是一个可复用的
AI 编程 workflow pack：把模糊想法、长期任务、已有项目继续推进，收束成一个
可验收 loop，并把决策、失败、下一步写入 state 文件。

Codex 用户可以安装 skill；Cursor、Claude Code、Gemini CLI、ChatGPT、JetBrains
AI 用户可以直接复制 Portable Prompt Pack 使用。
```

## 30-second demo script

Codex path:

```text
1. Install the skill from the pinned v0.4.2 tag.
2. Restart Codex.
3. Open a new empty project.
4. Prompt: "Use Loop Engineering for this vague idea: I want a small browser
   extension for saving useful snippets, but I do not know the exact
   requirements yet. Do not implement yet."
5. Show the generated or proposed state files.
6. Continue with: "用 Loop Engineering 继续这个项目。"
7. Show that the agent passes Project Outcome Gate before deciding whether
   `state/next.md` should be executed.
```

Portable path:

```text
1. Open portable/README.md.
2. Copy portable/LOOP_ENGINEERING_PROMPT.md or portable/LOOP_ENGINEERING_PROMPT.zh.md.
3. Copy portable/STATE_TEMPLATE/ into the project as state/.
4. Prompt the AI coding tool to continue through Project Outcome Gate, review
   `state/next.md` as a candidate next step, and run one bounded loop only if it
   advances the user-visible demo and business acceptance.
```

## Positioning notes

Say:

- "A lightweight AI coding workflow pack."
- "Codex skill plus Portable Prompt Pack."
- "Best for vague ideas, stalled projects, and long-running AI coding tasks."
- "Persists decisions, failures, acceptance criteria, and the next loop."

Avoid saying:

- "A universal agent framework."
- "A guarantee that every agent will behave perfectly."
- "A replacement for tests, reviews, or product judgment."

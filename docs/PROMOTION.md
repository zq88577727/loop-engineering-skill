# Promotion Kit

Use this page when presenting the project outside the repository. It keeps the
public description accurate and avoids overstating what the skill does.

## GitHub About

Description:

```text
Codex skill for turning vague ideas into bounded, verified project loops with durable state.
```

Website:

```text
https://github.com/zq88577727/loop-engineering-skill/releases/tag/v0.3.1
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
```

## Launch post

Short English version:

```text
I released Loop Engineering Skill v0.3.1, a Codex skill for turning vague ideas
into bounded, verified project loops.

It helps Codex clarify the idea, define the first loop, persist state, verify
the result, and continue from state/next.md instead of relying on chat memory.

Install:
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo zq88577727/loop-engineering-skill \
  --ref v0.3.1 \
  --path skills/loop-engineering
```

Short Chinese version:

```text
我发布了 Loop Engineering Skill v0.3.1。它不是让 Codex 更快写代码，而是让
Codex 在模糊想法、长期任务、已有项目继续推进时，先澄清目标，拆出一个可验收
loop，写入 state 文件，再执行和验证。

适合场景：你不想每次都靠聊天记录续上下文，而是希望项目有 state/next.md、
state/decisions.md、docs/acceptance.md 这类可复用入口。
```

## 30-second demo script

```text
1. Install the skill from the pinned v0.3.1 tag.
2. Restart Codex.
3. Open a new empty project.
4. Prompt: "Use Loop Engineering for this vague idea: I want a small browser
   extension for saving useful snippets, but I do not know the exact
   requirements yet. Do not implement yet."
5. Show the generated or proposed state files.
6. Continue with: "按 state/next.md 继续，只做一个 loop，验证后更新 state。"
```

## Positioning notes

Say:

- "A lightweight Codex workflow skill."
- "Best for vague ideas, stalled projects, and long-running tasks."
- "Persists decisions, failures, acceptance criteria, and the next loop."

Avoid saying:

- "A universal agent framework."
- "A guarantee that every agent will behave perfectly."
- "A replacement for tests, reviews, or product judgment."

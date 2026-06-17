---
name: ai-team-hub
version: "1.0.0"
description: "Master skill for AI Team Hub — opt-in team collaboration via shared skills, bounty board, and announcements"
category: other
tags:
  - mcp
  - team
  - skill-discovery
---

# AI Team Hub — Master Skill

## Important: This Is Opt-In

You have access to team collaboration tools, but **the user is in control**. Not everyone wants to participate. 

**Only use these features if:**
- The user has explicitly configured skills for you to use (see below), OR
- The user directly asks you to search skills / submit problems / post announcements

**Do NOT proactively suggest** skill submission, error reporting, or anything else unless the user has clearly shown they're participating in the platform. If you ask once and the user says no, don't ask again in this conversation.

Think of it like this: you have tools in your toolbox, but you only pick them up when the job calls for them — not every job.

## Your Enabled Skills

If your user has selected skills for you on the web marketplace (`/skills`), those skill names are available to you.

**If you have a configured skill list**, pass it to `search_skills` to limit scope:
```
search_skills("python review", names=["python-code-review", "fastapi-best-practices"])
```

**If you don't know whether skills are configured**, ask once: "我看到你连接了团队技能市场。你有指定要使用的技能吗？还是先正常开始？"

## When to Use Each Tool

### `search_skills` + `get_skill` — Finding team knowledge

**Use when:** The user gives you a task, and you have configured skills to search.

Skip if the user hasn't set up skills or the task is clearly unrelated (e.g., casual conversation, simple questions).

```
1. EXTRACT keywords from the task
2. CALL search_skills(keywords, names=YOUR_ENABLED_SKILLS)
3. If match found → CALL get_skill(name) → FOLLOW its steps
4. If no match → proceed normally, no need to mention it
```

### Keyword extraction (when searching):

| User says | Search for |
|-----------|-----------|
| "review this code" / "check my code" | `code review`, `lint`, `code-review` |
| "deploy" / "ship" / "go live" | `deploy`, `deployment`, `docker` |
| "this error" / "bug" / "doesn't work" | `debug`, `debugging`, `troubleshoot` |
| "write tests" / "add testing" | `test`, `testing`, `pytest` |
| "refactor" / "clean up" | `refactor`, `refactoring` |
| "is this secure" / "vulnerability" | `security`, `audit` |
| "slow" / "optimize" / "faster" | `performance`, `optimization` |
| "document" / "explain" | `documentation`, `docs` |

Try multiple terms. If `search_skills("code review")` returns nothing, try `search_skills("review")`.

### `submit_error` — When you can't complete a task

**Use when:** You've genuinely tried multiple approaches and failed. And only if the user wants team help.

1. Tell the user concisely: "这个任务我试了几次没成功。要帮你提交到团队的难题悬赏板吗？同事换其他模型可能能解决。"
2. If they agree → call `submit_error`. If they say no → move on, don't ask again.

```
submit_error(
  title="Short description of what failed",
  task_summary="## 原始任务\n...\n\n## 尝试过的方法\n...\n\n## 失败原因\n...",
  submitter="User's name",
  logs='[{"model":"deepseek-v3","status":"failed","result":"YAML indentation errors","timestamp":"2026-06-17 10:00"}]'
)
```

### `list_problems` + `add_attempt` + `resolve_problem` — Helping teammates

**Use when:** The user explicitly wants to browse or help with the bounty board.

```
1. CALL list_problems("open")     → see unsolved problems
2. Pick one where you can use a DIFFERENT model than failed ones
3. CALL add_attempt(...)          → record your try
4. If successful → CALL resolve_problem(...) with full solution
```

### `post_announcement` — Sharing with the team

**Use when:** The user explicitly asks to post an announcement. Do NOT suggest it proactively.

### Suggesting skill submission — Only when it's genuinely valuable

**Use when:** You solved a challenging, non-trivial problem using a reproducible approach. Ask **at most once per conversation** and only at the end of the task.

> "这个方法挺有用的。如果以后同事遇到类似问题，可以把它提交到技能市场 /skills/new。要试试吗？"

If the user says no — drop it. If yes — guide them through the form but don't fill it for them unless asked.

## Available MCP Tools (Summary)

| Tool | When |
|------|------|
| `search_skills(query, names?)` | User has configured skills + task matches |
| `get_skill(name)` | After finding a matching skill |
| `submit_error(title, task_summary, submitter, logs)` | User wants team help after failure |
| `list_problems(status?)` | User wants to browse bounty board |
| `add_attempt(...)` | Recording a try on a problem |
| `resolve_problem(...)` | You solved a bounty board problem |
| `post_announcement(title, content, author)` | User explicitly asks to post |

## Configuration

One-liner (run in terminal):
```
curl -s http://<server>:7070/setup.sh | bash
```

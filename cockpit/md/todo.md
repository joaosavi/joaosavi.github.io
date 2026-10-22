# `todo`

Keeps Claude Code's native task list in front of the agent: the open tasks at session start and on each prompt from you, a reminder that a new request becomes a task first, and completed tasks moved to an archive log.

## Why

The task tools (`TaskCreate`, `TaskList`, `TaskUpdate`, `TaskGet`) write one JSON file per task in `~/.claude/tasks/<list>/`, so the list outlives a compaction, `--resume` and `--continue`. The model forgets that the list is there. After a compaction it works from the summary, and a request that lived only in the conversation is lost. A session that takes many requests, such as a manager that hands work to other agents, needs the list read back to it from disk.

## What it does

- At session start, adds a note with the open tasks of the session's list.
- On each prompt from you, attaches the open tasks and the tasks completed since the last prompt. Messages from other sessions, notifications and schedules get nothing.
- With a named list (`CLAUDE_CODE_TASK_LIST_ID`), the same prompt also carries the rule: a new request becomes a `TaskCreate` before any other work, with its owner in the subject, such as `[owner] what was asked`.
- Moves a completed task to `~/.local/state/mods/todo/<list>.jsonl` and deletes its file, so the list holds only open work. This covers a task completed by `TaskUpdate` and a task file a script rewrote.

## Order of the list

The open tasks go in one group per state, with a count, such as `waiting (2):`.

- A task's priority and state come from `metadata.priority` and `metadata.state` in its file. Without metadata, they come from a subject such as `[owner] P1 waiting: what was asked`: the `P` number after the owner, then the word before the colon.
- A task with no state goes in the group of its native status, `in_progress` or `pending`.
- In each group, tasks go from P0 up, then the ones with no priority, then by id.
- The group that holds the most urgent task comes first. On a tie, the group with a task in progress comes first.

## Turn on the task tools

Claude Code offers the task tools by default only on Opus 4.7, Sonnet 4.6, Haiku 4.5 and earlier models. On a newer model, start Claude Code with the variable set. To share one list between sessions, name the list too:

terminal:

```
CLAUDE_CODE_ENABLE_TODO_TOOLS=1 CLAUDE_CODE_TASK_LIST_ID=requests claude
```

## Options

| Option | Default | What it does |
| --- | --- | --- |
| `enabled` | `true` | Off, the mod does nothing. Takes effect in the next session, or after `/reload-plugins`. |
| `remind` | `true` | With a named list, each prompt from you carries the request rule. |
| `archive` | `true` | Moves completed tasks from the list to the archive log. Off, completed tasks stay in the list. |

## What it records

`~/.local/state/mods/todo/<day>-<session>.jsonl`: one line per note, prompt context and archive run, plus one `session-summary` line. The archive, one line per completed task, is `~/.local/state/mods/todo/<list>.jsonl`. Each line has `at`, `session` and `event`.

## Cost

The open tasks go in whole with each prompt from you, at about 15 tokens per task, 30 tasks at most. The only `tool.call` hook is on `TaskUpdate`.

## Limits

- On a Team or Enterprise plan, the built-in guard `sec-default@builtin` skips the `session.compact` hook of a mod you installed yourself, so the note right after a compaction does not appear. The next prompt from you carries the list. A `SessionStart` hook with the matcher `compact` in the session's `settings.json` can print the open tasks right away.
- Task ids restart at 1 after every file has left the list. The archive keeps the subject next to each id.
- Tested on Linux only.

## Install this mod alone

The `cockpit` bundle already installs `todo` with the other mods. To install it alone:

terminal:

```
claude plugin marketplace add joaosavi/cockpit
claude plugin install todo@cockpit
```

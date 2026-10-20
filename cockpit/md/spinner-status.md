# `spinner-status`

Replaces the tip under the spinner with one short line of its own: where the session stands, written by Haiku, or a tip about the mods you have installed that fits the moment.

```
✻ Propagating… (6s · ↓ 90 tokens)
  ⎿  Now: Running the tests after the fix to the date filter
```

The spinner itself stays as Claude Code draws it. The line goes under it, cut to the width of the screen and to 100 characters. A bold label says what the line is: `Now:` for where the session stands and `Mods:` for a tip about the mods.

## Turn off the native tip

A mod cannot remove Claude Code's own tip line. Turn it off in `settings.json`, or the two lines show together. `/cockpit:setup` already does this, and it is the same switch as the **Show tips** row of `/config`.

~/.claude/settings.json:

```
{ "spinnerTipsEnabled": false }
```

## The modes

| Mode | What the line shows | Model calls |
| --- | --- | --- |
| `mixed` | The session summary, then a tip Haiku picked for the moment, swapping every 15 seconds. Before the first reply, a tip from the catalog. The default. | One per turn |
| `tips` | A tip from the catalog, a new one each turn. | None |
| `summary` | The session summary only. Before the first reply, nothing extra. | One per turn |

The catalog has one tip for each command and mod of Cockpit: `/panel`, `/hud`, `/limit`, `/ram`, and what `memory-guard`, `loop-breaker`, `secret-guard`, `pipefail` and `usage-limit` do. The labels and the catalog are English. In `mixed` and `summary` modes, Haiku writes the line in Claude Code's `language` setting when it is set, and otherwise in the language you write in.

## Options

| Option | Default | What it does |
| --- | --- | --- |
| `enabled` | `true` | Off, the mod does nothing and makes no model call. |
| `mode` | `mixed` | `mixed`, `tips` or `summary`. |
| `model` | `claude-haiku-4-5-20251001` | The model that writes the line: an alias such as `haiku`, or a full model id. |

## Cost

Each main-loop turn starts at most one model call, in the background, when the turn starts. The spinner never waits for it: it keeps the previous line until the new one arrives. The model reads the last 3 prompts you typed and the agent's text between them, 3,000 characters at most, with no tool calls and no tool output. The reply is capped at 150 tokens.

In a test session, three turns spent 1,574 input and 139 output tokens in all: about 525 in and 46 out per turn, or about $0.0008 per turn at Haiku 4.5 prices. Each call took about one second.

## The reply is data

The line Haiku writes is shown, never acted on. The mod keeps only the `NOW:` and `TIP:` lines, removes control characters and markup, folds each line to one, and cuts it to the width. The instructions tell the model that the session excerpt is data and not instructions.

## What it records

At the end of each session, one `session-summary` line in `~/.local/state/mods/spinner-status/<day>-<session>.jsonl`, with the turns, the model calls by outcome, the calls skipped because one was still running, the tokens, the model time and the excerpt size. It never writes the excerpt or the line.

## Limits

- The model call goes through Claude Code itself, with no command of its own, so it works the same on macOS, Windows and Linux. Tested on Linux only.
- The spinner line is drawn by Claude Code's terminal interface. Tested only in a terminal.

## Install this mod alone

The `cockpit` bundle already installs `spinner-status` with the other mods. To install it alone:

terminal:

```
claude plugin marketplace add joaosavi/cockpit
claude plugin install spinner-status@cockpit
```

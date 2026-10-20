# `hud`

Shows the model, the project and its git branch, the context window, the plan limits and the memory headroom, under the prompt as a status line or above it in the band. While a turn runs, the band adds the latest note another mod added to a tool result, which only the model reads otherwise.

## The four styles

Pick one with the `style` option. Each style drops its least useful fields first when the terminal is narrow, so no row passes the width. Below is the real output of `statusline.sh` for the same session.

### `refined`

Two rows with gradient bars. The default.

```
Opus 5.5   acme-api   feat/billing  ● 1  ? 1     43m  ·  0 calls
ctx ●●○○○○ 38%   5h ●●●●○○ 64% 2h20m   7d ●●●●●○ 81%   mem 2.4G
```

### `blocks`

Each field on its own colored background.

```
 Opus 5.5   acme-api   feat/billing  ● 1  ? 1                43m
 ctx 38%   5h 64%  resets 2h20m  7d 81%   mem 2.4G free 
```

### `minimal`

Fields spelled out in words, thin bars.

```
acme-api  feat/billing  1 modified · 1 untracked  Opus 5.5 · 43m
ctx ━━──── 38%   5h ━━━━── 64% 2h20m   7d ━━━━━─ 81%   2.4G free
```

### `compact`

One row when it fits, two when it does not.

```
acme-api  feat/billing ● 1 ? 1                          Opus 5.5
ctx 38% │ 5h 64% 2h20m │ 7d 81% │ mem 2.4G
```

## The status line

A mod cannot draw rows under the prompt: that place belongs to the status line command of the settings. The mod ships one, `statusline/statusline.sh`, and `/cockpit:setup` writes it for you. To set it by hand on macOS or Linux, put this in `~/.claude/settings.json`, with `band` set to `off` so the rows do not show twice:

~/.claude/settings.json:

```
{
  "statusLine": { "type": "command", "command": "~/.claude/plugins/marketplaces/cockpit/hud/statusline/statusline.sh", "refreshInterval": 5 },
  "pluginConfigs": { "hud@cockpit": { "options": { "band": "off", "style": "refined", "icons": "nerd" } } }
}
```

The script needs Node 22.18 or later. `refreshInterval` re-runs the script every 5 seconds, so git, the PR and the session time stay current while the session is idle. On Windows, PowerShell cannot run a `.sh` file: point the command at `node ~/.claude/plugins/marketplaces/cockpit/hud/statusline/statusline.ts`, with forward slashes.

### Git and the PR

The git field shows the branch, then commits to push, commits to pull, files staged, files changed outside the stage and untracked files, or `synced` when there is nothing. The PR is the branch's open pull request from `gh pr view`, with its checks: passing, failing or running. `gh` takes about a second, so the script runs it in the background at most once a minute and shows the last answer meanwhile. Without `gh`, or without an open PR, the field is left out.

### Icons

With `icons` set to `nerd`, the default, the git, folder, model and memory fields use Nerd Font glyphs, which show only when the terminal's font is a Nerd Font. With `unicode`, they use `↑ ↓ + ● ? ✓` and no glyph for the folder, the model and the memory.

## The band above the prompt

Without the status line, the hud draws in the band above the prompt. With `band` at `panel`, the default, it draws two rows, with the right side of the first row flush with the last column:

```
Opus 5.5 · my-app  main●                              38m · 214 calls
ctx ▰▰▰▰▱▱▱▱▱▱  42%   5h ▰▰▰▰▰▰▱▱▱▱  61% resets 2h30m   7d ▰▰▰▰▱▱▱▱▱▱  44%   mem 1.9G free
```

While a turn runs and another mod left a note, the activity row follows, such as `loop-breaker: repeated error`. It hides when the turn ends. Claude Code already draws the running tool, its errors, the subagents and the turn's time, so the band leaves them out.

| Field | Colors |
| --- | --- |
| `ctx`, the context window | green below 60%, yellow below 85%, red from 85% |
| `5h` and `7d`, the plan windows | green below 75%, yellow below 90%, red from 90% |
| `mem`, the memory that still fits | yellow below 1 GB, red below 500 MB |
| Activity row | yellow |

In a narrow terminal the band drops fields instead of wrapping: first it shortens the bars, then drops `mem`, then shows `ctx`, `5h` and `7d` as percents only, then drops the reset countdown. With `band` at `line`, it draws one row:

```
Opus 5.5 │ my-app  main● │ ctx 42% │ 5h 61% │ 7d 44% │ mem 1.9G
```

## The /hud pane

```
SESSION   Opus 5.5 · my-app  main● · 38m · 214 calls · ctx 42%
LIMITS    5h 61% resets 2h30m · 7d 44% resets 3d20h
MEMORY    session 1.5G · slice 3.0/5.0G · 1.9G fits
NOW       Bash yarn turbo run test 0:42 · 2 subagents
TODAY     2 skills · 1 loop nudge · 0 refusals
```

`MEMORY` names the session's own cgroup and the group whose limit sets the headroom, or the machine's memory without a cgroup limit. `TODAY` counts today's lines in the other mods' diaries. The pane refreshes every 2 seconds while it is open; press `r` to refresh now and `esc` to close it.

## Options

In `/config`, or under `pluginConfigs` in `~/.claude/settings.json`.

| Option | Default | What it does |
| --- | --- | --- |
| `band` | `panel` | `panel` draws two rows above the prompt, `line` one, `off` none (`/hud` still works). Use `off` with the status line. |
| `activity` | `true` | Shows the activity row while a turn runs. |
| `memory` | `true` | Shows the memory headroom in the band and the `MEMORY` row. |
| `bar` | `dots` | The bar glyphs: `blocks` (▰▱), `solid` (█░), `line` (━─), `dots` (●○) or `squares` (■□). |
| `barWidth` | `10` | Cells of a full-width bar, 4 to 30. A narrow terminal still shrinks the bars. |
| `colors` | empty | The colors for ok, warning and critical, separated by spaces: a name, `#rrggbb` or a 256-color number. Empty uses green, yellow and red. |
| `hide` | empty | Fields to leave out, separated by commas: `model`, `project`, `branch`, `age`, `calls`, `ctx`, `5h`, `7d`, `reset`, `mem`. |
| `barColor` | `gradient` | `gradient` colors each cell by its place, green to red. `solid` colors the whole bar by its percent. `tone` keeps the three colors of `colors`. |
| `style` | `refined` | The status line layout: `refined`, `blocks`, `minimal` or `compact`. |
| `icons` | `nerd` | `nerd` for Nerd Font glyphs, `unicode` for plain marks. |
| `contextBase` | `compact` | What `ctx` measures against. `compact`: 100% is the auto-compact window, when smaller than the model's. `window`: the model's full window. The status line only. |
| `timeZone` | empty | The IANA time zone for the times shown and for what counts as today. Empty uses the system time zone. |

## Cost

The band's render hook does no I/O: it lays out values that events and timers already read. Every 15 seconds, idle or not, it runs one `git status` (3-second timeout) and a memory reading. During a turn, a 1-second timer reads the agent list for `/hud`, and redraws only while the pane is open. Each tool call adds two redraw requests, and Claude Code throttles redraws to 10 a second.

## Limits

- On macOS and Windows there is no per-session limit, so the memory field shows the whole machine. Those readings are tested only against simulated output.
- When the reading fails, the memory field is left out.
- The PR field needs the GitHub CLI, `gh`, signed in.
- The band, the status line and the pane are part of the terminal interface. Tested only in a terminal, and the Windows setup is not tested.

## Install this mod alone

The `cockpit` bundle already installs `hud` with the other mods. To install it alone:

terminal:

```
claude plugin marketplace add joaosavi/cockpit
claude plugin install hud@cockpit
```

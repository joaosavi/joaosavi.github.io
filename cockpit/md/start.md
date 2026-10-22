# Quickstart

Cockpit is a bundle of 12 mods for [Claude Code](https://claude.com/product/claude-code). The guards stop an agent's mistake before it costs you: a secret in tool output, a pipe that hides a failed test, a build killed by the memory limit, a commit that sweeps in another session's edits. The instruments show where the session stands, under the prompt, under the spinner, and on a page with every session on the machine.

```
claude plugin marketplace add joaosavi/cockpit
claude plugin install cockpit@cockpit
```

-  **Install the bundle** In a terminal, add the marketplace and install `cockpit`. It brings the 12 mods as dependencies.  [See every install step](https://joaosavi.github.io/cockpit/md/install.md)
-  **Restart and run the setup** Restart Claude Code and type `/cockpit:setup`. It asks four questions with previews, writes the status line, the spinner tip and when to compact, and keeps a backup of the file it changed. [See what the setup asks](https://joaosavi.github.io/cockpit/md/install.md)
-  **Work as usual** The guards stay quiet until they act. Type `/panel` for the address of the session page, and `/limit` for the plan limits. [What changes in your first session](https://joaosavi.github.io/cockpit/md/first-session.md)

## What it looks like

```
✻ Propagating… (6s · ↓ 90 tokens)
  ⎿  Now: Running the tests after the fix to the date filter

────────────────────────────────────────────────────────────────
❯ 
────────────────────────────────────────────────────────────────
Opus 5.5   acme-api   feat/billing  ● 1  ? 1     43m  ·  0 calls
ctx ●●○○○○ 38%   5h ●●●●○○ 64% 2h20m   7d ●●●●●○ 81%   mem 2.4G
```

A turn in progress: the `spinner-status` line, the prompt, and the `hud` status line in the `refined` style. Real output from the mods.

## Guards

Stop a mistake before it lands.

- `secret-guard`: Replaces every secret value in tool output with `<hidden:NAME>` before the agent reads it, and writes the real value back when the agent edits a `.env` file. [Read more](https://joaosavi.github.io/cockpit/md/secret-guard.md)
- `collision-guard`: Warns when another session on this machine edited the same file, and holds a git command once when it would take that session's uncommitted edits along. [Read more](https://joaosavi.github.io/cockpit/md/collision-guard.md)
- `pipefail`: Adds `set -o pipefail;` to a test, typecheck or lint run piped into `tail`, `head` or `grep`, so a failed run cannot exit 0. [Read more](https://joaosavi.github.io/cockpit/md/pipefail.md)
- `memory-guard` : Keeps typecheck, build, test and Playwright runs under the memory limit: as written, with one process, after a wait, or refused. Reruns a command killed with exit 137 with one process. [Read more](https://joaosavi.github.io/cockpit/md/memory-guard.md)
- `loop-breaker`: Tells the agent to stop and change approach when it repeats the same error, the same fix or the same call. [Read more](https://joaosavi.github.io/cockpit/md/loop-breaker.md)
- `usage-limit` : Limits each plan window on its own: one subagent at a time, a work-in-progress commit, a pause that keeps a reserve for you, and a resume when the window resets. [Read more](https://joaosavi.github.io/cockpit/md/usage-limit.md)

## Instruments

Show where the session stands.

- `hud` : Model, project, git branch and PR, context window, plan limits and memory, in a status line under the prompt. Four styles. [Read more](https://joaosavi.github.io/cockpit/md/hud.md)
- `spinner-status`: Replaces the tip under the spinner with one line from Haiku: where the session stands, or a tip about these mods. [Read more](https://joaosavi.github.io/cockpit/md/spinner-status.md)
- `panel` : A local web page with a card for every session on this machine: its state, what it needs from you, the tool running now and the next step. [Read more](https://joaosavi.github.io/cockpit/md/panel.md)
- `skill-loader`: Delivers the right skill when the agent touches a matching file or writes a commit, and reminds it to diagnose before fixing when you paste an error. [Read more](https://joaosavi.github.io/cockpit/md/skill-loader.md)

## Memory

- `global-memory`: Adds a machine-wide memory folder beside the per-project memory, so facts about the machine reach every session. [Read more](https://joaosavi.github.io/cockpit/md/global-memory.md)
- `todo`: Shows the open tasks of the native task list at session start and on each prompt from you, and archives completed tasks. [Read more](https://joaosavi.github.io/cockpit/md/todo.md)

## Requirements

- Claude Code 2.1.287 or later, on macOS, Windows or Linux. Mods use Claude Code's function hooks, which are in early access and may change between releases.
- Node 22.18 or later, for the status line script.
- Python 3.9 or later and `curl`, for the `panel` page. macOS and Windows 10 or later ship `curl`.
- A [Nerd Font](https://www.nerdfonts.com/) in your terminal, for the status line icons. Without one, choose the plain icons during setup.

The status line, the spinner line and the panes are part of Claude Code's terminal interface. Run `claude` in a terminal: Terminal or iTerm on macOS, Windows Terminal or PowerShell on Windows, or the terminal panel of VS Code or JetBrains. The mods are not tested in the Desktop app or in the chat panel of the IDE extensions.

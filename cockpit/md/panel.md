# `panel`

A local web page with every Claude Code session on your computer: whether it waits for you, what it needs, what it is doing now, and what it finished. Each session's summary comes from `claude -p`, refreshed every few minutes and when you ask.

![The panel page in the Inbox view: the machine in the header, the sessions by urgency on the left, and the selected session on the right](https://joaosavi.github.io/cockpit/img/panel-dark.png)

The page with made-up sessions, in the Inbox view.

## Open the page

Type `/panel` in any session for the address, `http://localhost:7777` by default, and open it in your browser. The server starts with the first session after you install the mod, and keeps running after that session ends. The page listens only on `127.0.0.1`, so only your own computer reaches it. When the sessions run on another machine, see [Run on a remote machine](https://joaosavi.github.io/cockpit/md/remote.md).

## What the page shows

- The header shows the computer in one line: the plan's 5-hour and weekly usage with the time left to each reset, memory, the CPU over the last minute, disk, and the tokens the sessions used in the last 24 hours, hour by hour. A figure turns amber at 75% and red at 90%. On the right are **Notify**, **Refresh all** and **Mods**.
- Each session shows its state (`Working`, `Waiting for you`, `Blocked`, `Done`, `Idle`), a title, the project, the git branch with its changed files and commits ahead or behind, the model, your last message, the tool running now, the summary of where the task stands, the next step and what it finished. Four figures close it: the context used against the point where it compacts, the tokens of the last 24 hours, the memory of the session's processes, and how long it has run.
- The **Mods** drawer shows the computer in full, the latest actions of the guards, what each guard did today, and how many summaries the page made today with their tokens and their price at API list prices. On Linux it also shows the memory of each cgroup with a limit and the state of their systemd services.

## The six views

The switcher under the header picks the view, and the page remembers it. The address also takes a view as its hash, such as `#board`, and `#mods` opens the drawer.

| View | What it shows | Keys |
| --- | --- | --- |
| **Inbox** | The default. The sessions by urgency on the left, and the selected one in full on the right. | `j` and `k` or the arrows move, `1` to `4` pick an option, `r` goes to the reply field |
| **Board** | Columns by state, with small cards. A card opens the session in a side drawer. | `1` to `4` in the drawer, `esc` closes it |
| **Deck** | A grid of full cards, with filters for all sessions, the ones that need you, working, done and ended. |  |
| **Focus** | One large card for the session that needs you most, and the others below it. | `n` and `p` or the arrows move |
| **Timeline** | A row per session with its tokens hour by hour over the last 24 hours, and a row for all sessions together. |  |
| **Tasks** | The open tasks of the native task list in groups (In progress, Waiting, Queued), each from P0 up, with filters by priority and group, and the last 30 tasks the [`todo`](https://joaosavi.github.io/cockpit/md/todo.md) mod archived. A row opens to show the description. It calls no model. |  |

**Working** comes from Claude Code itself, as soon as a turn starts. **Waiting for you**, **Blocked**, **Done** and **Idle** come from the summary, which `claude -p` writes from the transcript: 20 seconds after a turn ends, every 5 minutes for a session that changed, and when you press **Refresh**.

## Answer a session from the page

When a session waits for a decision, its options are buttons. Press one, or its number key, check the text, and confirm. The reply field sends any text the same way. The page leaves the text in the session's inbox, the `panel` mod in that session checks the inbox every 2 seconds and submits the text as your prompt, and Claude Code runs it once the session is idle. It works on macOS, Windows and Linux, in a terminal, the Desktop app, an IDE or Remote Control, with or without tmux.

>  **Greyed-out options** A session takes answers only when its mod checked the inbox in the last 15 seconds. Until then its options are greyed out and its reply field is hidden. A session that loaded an older `panel` mod stays that way until you run `/reload-plugins` in it. When a session does not take a message within 6 seconds, the page withdraws it and says so.

## Audit the mods

The lower half of the **Mods** drawer audits the mods from their diaries over the last day, 7 days or 30 days. Each row shows the mod's version, whether it is on, how many sessions it ran in, what it did, its failures in red, the time its hooks added per tool call, its slowest hook call, the API cost of its model calls, and its last action. A mod with nothing recorded for a week does no work on your machine.

![The Mods drawer: the computer, the guards, and one row per mod with its actions, failures and time per tool call](https://joaosavi.github.io/cockpit/img/panel-mods.png)

## Options

| Option | Default | What it does |
| --- | --- | --- |
| `enabled` | `true` | Off, the mod does nothing: no `/panel`, no server start, no answers; a server already running keeps running. Takes effect in the next session, or after `/reload-plugins`. |
| `port` | `7777` | The port the page listens on, on `127.0.0.1`. |
| `model` | `sonnet` | The model `claude -p` uses for each summary: `sonnet`, `haiku` or `opus`. |
| `refreshMinutes` | `5` | A session whose transcript changed gets a new summary this often. |
| `autostart` | `true` | Start the server when a session starts and the port does not answer. Turn it off when a service manager runs the server. |
| `answers` | `true` | Let the page send text to this session as your prompt. Off, the page shows the session's options greyed out and no reply field. |

## Start the server by hand

The page needs Python 3.9 or later, as `python3`, `python` or `py`, and `curl`. With `autostart` on, the first session starts the server, and it keeps running after that session ends. To start it yourself, run the server file from the plugin folder, which is the `installPath` of `panel@cockpit` in `~/.claude/plugins/installed_plugins.json`:

terminal:

```
python3 -I <plugin folder>/server/panel.py
```

On Windows, use `python` or `py` in place of `python3`. Set `PANEL_CLAUDE` to the path of `claude` when it is not on the `PATH`.

## How the summary is made

The server builds a digest of the transcript, at most 48,000 characters long: the message that opened the task, then the newest rows that fit, each tool call cut to one line. It sends the digest to `claude -p --safe-mode --tools "" --no-session-persistence` with a JSON schema. The call loads no hooks, plugins or tools, keeps no transcript of its own, and answers in a fixed shape, in the language you write in.

## Cost

Each summary is one `claude -p` call, and it counts toward your plan's usage limits. On the author's Linux machine in October 2026, a summary of a long session read about 48,000 tokens and took 6 to 10 seconds, and the server's memory peaked at 213 MB during the call. At API list prices with `sonnet`, a summary cost about $0.07, and with four sessions working the page spent up to $2.40 an hour. On a Pro or Max plan the calls spend plan usage, not money. `haiku` costs about 20 times less per token, with shorter and less exact summaries.

## What it records

- `~/.local/state/mods/panel/summaries/<session>.json`: the last summary of each session, with the time it was made and the transcript size it read.
- `~/.local/state/mods/panel/<day>-server.jsonl`: one line per summary with the reason, the time, the state and the tokens, one line per failure, and one line per sent answer with its length. It never writes the session's content or what you sent.

## Limits

- The sessions must run on the same machine, under the same user as the server.
- The page has no login. Anyone who can connect to the port on that machine can read it, start summaries and type into the sessions, so keep it on `127.0.0.1`. The server refuses a request that comes from a page on another site.
- An answer sent from the page waits until the session is idle. While a turn runs, it does not reach the agent, and it runs as a new turn after the current one ends.
- The state comes from the model and can lag behind the session. A busy session always shows `Working`.
- On macOS and Windows there are no memory groups, no services and no disk wait. Tested on Linux; the macOS and Windows code paths run only through simulated tests.

## Install this mod alone

The `cockpit` bundle already installs `panel` with the other mods. To install it alone:

terminal:

```
claude plugin marketplace add joaosavi/cockpit
claude plugin install panel@cockpit
```

# Your first session

After the setup and a restart, three things show on screen. The guards stay out of sight until they act.

## The status line

The `hud` draws two rows under the prompt: the model, the folder, the git branch and its changes, then the context window, the 5-hour and 7-day plan windows, and the memory headroom.

```
Opus 5.5   acme-api   feat/billing  ● 1  ? 1     43m  ·  0 calls
ctx ●●○○○○ 38%   5h ●●●●○○ 64% 2h20m   7d ●●●●●○ 81%   mem 2.4G
```

The bars turn from green to red as they fill. The `2h20m` after the 5-hour percent is the time until that window resets. The other three styles are on the [hud page](https://joaosavi.github.io/cockpit/md/hud.md).

## The line under the spinner

While a turn runs, Claude Code shows a tip under the spinner. `spinner-status` replaces it with one line from Haiku about what the agent is doing right now.

```
✻ Propagating… (6s · ↓ 90 tokens)
  ⎿  Now: Running the tests after the fix to the date filter
```

`Now:` is where the session stands. `Mods:` is a tip about the mods you have.

## The session page

`panel` starts a local web page with every session on the machine. Type `/panel` for its address.

```
❯ /panel
  ⎿  panel: http://localhost:7777
     4 sessions: 1 need you, 2 working.
```

Open the address in a browser. A session that waits for you comes first, with the options it offered as buttons. The [panel page](https://joaosavi.github.io/cockpit/md/panel.md) shows its six views.

## Commands to try

| Command | What it shows |
| --- | --- |
| `/limit` | The plan windows, when each resets, and what the mod holds back near the limit. |
| `/hud` | The full heads-up display: session, limits, memory, what runs now, and today's mod actions. |
| `/ram` | Memory headroom per group, or of the machine, and the measured peak of each heavy command. |

## When a guard acts

The agent reads a short note that starts with the mod's name, such as `pipefail:` or `Loop check`, and usually tells you about it. The latest note also shows in the band above the prompt while the turn runs.

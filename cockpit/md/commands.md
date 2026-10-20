# Commands

Every command Cockpit adds. Each one also answers in plain text, so it works where no pane is drawn, such as Remote Control.

| Command | Mod | What it shows |
| --- | --- | --- |
| `/panel` | [panel](https://joaosavi.github.io/cockpit/md/panel.md) | The address of the session page, and how many sessions need you. Starts the server when it does not answer. In a session opened over SSH, also prints the tunnel command. |
| `/hud` | [hud](https://joaosavi.github.io/cockpit/md/hud.md) | The full heads-up display: session, limits, memory, now, today. |
| `/limit` | [usage-limit](https://joaosavi.github.io/cockpit/md/usage-limit.md) | The plan windows with their stages, the state, and what is held for the resume. |
| `/ram` | [memory-guard](https://joaosavi.github.io/cockpit/md/memory-guard.md) | Memory headroom per group, or of the machine, and the measured peak of each heavy command. |
| `/cockpit:setup` | cockpit | Runs the setup again, to change the style or any other answer. |

## Keys inside a pane

Press `r` to refresh it and `esc` to close it.

## Keys on the panel page

Press `r` to summarize every session again, or `R` in Inbox, where `r` goes to the reply field. `esc` closes the send dialog, then the Mods drawer, then the Board drawer. Each view adds its own keys, listed on the [panel page](https://joaosavi.github.io/cockpit/md/panel.md).

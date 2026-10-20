# What leaves your machine

Cockpit runs inside Claude Code on your machine. Two mods send an excerpt of the session to a model, through your own account. Everything else stays local.

## What leaves

| Mod | Sends | When |
| --- | --- | --- |
| `panel` | An excerpt of each session's transcript, through `claude -p`, to `sonnet` by default | On **Refresh**, when a session goes idle after a turn, and every 5 minutes for a session that changed |
| `spinner-status` | The last few prompts and the agent's last text, at most 3,000 characters, to Haiku | Once per turn, or never in `tips` mode |
| `hud` | A `gh pr view` request for the current branch, to GitHub | At most once a minute, when `gh` is installed |

These calls use the same account and the same data terms as the rest of your Claude Code session. No other mod calls a model.

## What stays

- Every mod writes a diary under `~/.local/state/mods/<mod>/`, one line per action and one summary per session. A diary never holds a secret value or a file's content.
- `collision-guard` keeps the list of files each session edited. An ended session marks its record, and records older than `expireHours` (24 hours by default) are removed when a session starts.
- `secret-guard` holds secret values in memory only, never on disk.
- `panel` keeps the last summary of each session. The page has no login and listens only on `127.0.0.1`. Anyone who can reach that port can read it and type into your sessions, so do not expose it.

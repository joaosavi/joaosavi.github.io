# Troubleshooting

The problems people hit most, and the fix for each.

| Symptom | Fix |
| --- | --- |
| The status line does not show, or only changes when a message arrives | The `statusLine` setting is missing, or has no `refreshInterval`. Run `/cockpit:setup` again, then restart Claude Code. |
| The status line shows nothing at all | The script needs Node 22.18 or later. Run `node --version`, and update Node if it is older. |
| Icons show as boxes or question marks | The terminal font has no Nerd Font glyphs. Set `icons` to `unicode` under `hud` in `/config`, or install a Nerd Font and select it in your terminal. |
| The bars look like a single blurred shape | Some fonts draw the bar glyphs joined together. Set `bar` under `hud` to `dots` or `squares`. |
| Two lines show under the spinner | Claude Code's own tip is still on. Set `"spinnerTipsEnabled": false` in your settings, or run the setup again. |
| A mod shows `failed to load` in `claude plugin list` | The marketplace copy and the installed version are out of step. Run `claude plugin marketplace update cockpit`, then `claude plugin update cockpit@cockpit`, and restart. |
| The mod options are gone | Removing a marketplace deletes the saved options of its plugins. Run `/cockpit:setup` again to write them back. |
| `global-memory` does nothing on a Team or Enterprise plan | Those plans skip user-installed plugins on the hooks it needs. It must run as an organization plugin; its [page](https://joaosavi.github.io/cockpit/md/global-memory.md) shows the managed settings. |
| `/panel` says the page server is not running | The server starts when a session starts, unless `autostart` is off. Check that Python 3.9 or later is installed as `python3`, `python` or `py`, and that `curl` runs, then start a new session. The server writes its errors to `~/.local/state/mods/panel/server.log`. |
| The page greys out the options of a session | The session has not checked its inbox in the last 15 seconds, usually because it loaded an older `panel` mod. Run `/reload-plugins` in that session. |
| The Mods drawer shows no memory groups or services | That is expected on macOS and Windows. The page shows memory by group only for Linux cgroup v2 groups with a limit, and services only under systemd. |
| `/ram` says there is no memory reading | `memory-guard` found no `/proc/meminfo`, and the system command failed: `sysctl` and `vm_stat` on macOS, or PowerShell on Windows, missing or slower than its timeout. Until a reading works, heavy commands run as written. |
| A git command was refused with a list of files | `collision-guard` held it, because another session on this machine has uncommitted edits in the same repo, under the paths the command names. Name your own files instead, or run the same command again within 2 minutes. |

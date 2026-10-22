# Install and set up

Two commands in a terminal, a restart, and a setup with four questions. It takes about five minutes.

## Install

- **Add the marketplace and install the bundle**
terminal:

```
claude plugin marketplace add joaosavi/cockpit
claude plugin install cockpit@cockpit
```
The second command lists the mods it installs, as `+ 12 dependencies`.
- **Restart Claude Code** The new session loads the mods. A session that was already open picks them up with `/reload-plugins`.
- **Run the setup**
inside Claude Code:

```
/cockpit:setup
```
A plugin cannot write the status line, the spinner tip or when to compact by itself, because they live in your `settings.json`. The setup writes them, keeps a backup of the file it changed, and tells you what you will notice.

## What the setup asks

| Question | Options |
| --- | --- |
| Status line style | `refined` (recommended), `blocks`, `minimal` or `compact`, each with a preview drawn by the real script, with your own folder and branch. |
| Icons | The setup prints three Nerd Font icons and asks whether they show. If you see boxes, it uses plain arrows and marks that every terminal draws. |
| Time zone | Only when the system is on UTC. It sets the clock times the mods show and what counts as today. |
| When to compact | Earlier, at about 70% of a 1M model (recommended, `733000`), Claude Code's default near the end, or at about half (`500000`). Skipped when the model's window is under 200K. |

The setup also turns on auto-update for the marketplace, without asking. Run `/cockpit:setup` again to change an answer: it reads what is set and asks only about what you want to change.

## Check the install

terminal:

```
claude plugin list
```

You should see 13 entries ending in `@cockpit`, each marked `enabled`: the bundle and the 12 mods. An entry marked `failed to load` points to a version mismatch; see [Troubleshooting](https://joaosavi.github.io/cockpit/md/troubleshooting.md).

## Updates install by themselves

With auto-update on, a few minutes after the first message of a session, Claude Code updates every mod with a new version, installs any mod added to the bundle, and shows `Plugin updated: <name> · Run /reload-plugins to apply`. To turn it off, open `/plugin`, go to **Marketplaces**, and select `cockpit`.

## macOS, Windows and Linux

Every mod runs on all three systems, and they are tested on Linux only. Two things differ:

- `memory-guard` and the memory figure of the `hud` read cgroup limits and `/proc/meminfo` on Linux. On macOS they read `vm_stat` and on Windows PowerShell, and there they compare against the whole machine's memory. The macOS and Windows readings are tested only against simulated output.
- The `panel` page shows memory by cgroup, systemd services and the share of CPU time spent waiting on disk only on Linux.

On Windows, the setup points the status line at Node instead of the `.sh` script, because PowerShell cannot run a shell script.

## On a Team or Enterprise plan

Every mod works the same on every plan, except `global-memory`. Team and Enterprise plans run a built-in guard that skips plugins you install yourself on the two hooks it needs, so it installs and does nothing until your organization lists it in managed settings. The other mods run as usual. The [global-memory page](https://joaosavi.github.io/cockpit/md/global-memory.md) shows the two settings.

>  **Coming from the agent marketplace** Cockpit was called `agent` before October 2026. Rename every `@agent` key to `@cockpit` in `~/.claude/settings.json`, then run `claude plugin marketplace remove agent` before the steps above. Removing a marketplace deletes the saved options of its plugins, so rename the keys first, or run `/cockpit:setup` again afterwards.

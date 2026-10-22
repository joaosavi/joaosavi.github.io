# Versions

Cockpit 1.6.0. The bundle carries the version of the release, and each mod carries the version of the release where it last changed.

A mod that did not change in a release keeps its version, so Claude Code does not update it.

| Mod | Version |
| --- | --- |
| `cockpit` (bundle) | 1.6.0 |
| [`secret-guard`](https://joaosavi.github.io/cockpit/md/secret-guard.md) | 1.3.0 |
| [`collision-guard`](https://joaosavi.github.io/cockpit/md/collision-guard.md) | 1.3.0 |
| [`pipefail`](https://joaosavi.github.io/cockpit/md/pipefail.md) | 1.3.0 |
| [`memory-guard`](https://joaosavi.github.io/cockpit/md/memory-guard.md) | 1.3.0 |
| [`loop-breaker`](https://joaosavi.github.io/cockpit/md/loop-breaker.md) | 1.3.0 |
| [`usage-limit`](https://joaosavi.github.io/cockpit/md/usage-limit.md) | 1.3.0 |
| [`hud`](https://joaosavi.github.io/cockpit/md/hud.md) | 1.3.0 |
| [`spinner-status`](https://joaosavi.github.io/cockpit/md/spinner-status.md) | 1.0.0 |
| [`panel`](https://joaosavi.github.io/cockpit/md/panel.md) | 1.6.0 |
| [`skill-loader`](https://joaosavi.github.io/cockpit/md/skill-loader.md) | 1.3.0 |
| [`global-memory`](https://joaosavi.github.io/cockpit/md/global-memory.md) | 1.3.0 |
| [`todo`](https://joaosavi.github.io/cockpit/md/todo.md) | 1.5.0 |

## What changed

- **1.6.0**: `panel` has a Tasks view with the open tasks of the native task list, grouped and filtered by priority.
- **1.5.0**: `todo` lists the open tasks in one group per state, each sorted by priority, from the task metadata or from a subject such as `[owner] P1 waiting: what was asked`.
- **1.4.0**: new mod `todo`, which keeps the native task list in front of the agent.
- **1.3.0**: every mod has an `enabled` option, and the guards have one switch per step. `/cockpit:setup` can turn mods off.
- **1.2.0**: `usage-limit` limits each window on its own, with a separate throttle, commit and pause for the 5-hour and 7-day windows, each with its own switch and percentage.
- **1.1.0**: `secret-guard` reads the secrets folder beside the secrets file.

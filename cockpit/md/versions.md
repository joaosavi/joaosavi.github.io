# Versions

Cockpit 1.2.0. The bundle carries the version of the release, and each mod carries the version of the release where it last changed.

A mod that did not change in a release keeps its version, so Claude Code does not update it.

| Mod | Version |
| --- | --- |
| `cockpit` (bundle) | 1.2.0 |
| [`secret-guard`](https://joaosavi.github.io/cockpit/md/secret-guard.md) | 1.1.0 |
| [`collision-guard`](https://joaosavi.github.io/cockpit/md/collision-guard.md) | 1.0.0 |
| [`pipefail`](https://joaosavi.github.io/cockpit/md/pipefail.md) | 1.0.0 |
| [`memory-guard`](https://joaosavi.github.io/cockpit/md/memory-guard.md) | 1.0.0 |
| [`loop-breaker`](https://joaosavi.github.io/cockpit/md/loop-breaker.md) | 1.0.0 |
| [`usage-limit`](https://joaosavi.github.io/cockpit/md/usage-limit.md) | 1.2.0 |
| [`hud`](https://joaosavi.github.io/cockpit/md/hud.md) | 1.0.0 |
| [`spinner-status`](https://joaosavi.github.io/cockpit/md/spinner-status.md) | 1.0.0 |
| [`panel`](https://joaosavi.github.io/cockpit/md/panel.md) | 1.0.0 |
| [`skill-loader`](https://joaosavi.github.io/cockpit/md/skill-loader.md) | 1.0.0 |
| [`global-memory`](https://joaosavi.github.io/cockpit/md/global-memory.md) | 1.0.0 |

## What changed

- **1.2.0**: `usage-limit` limits each window on its own, with a separate throttle, commit and pause for the 5-hour and 7-day windows, each with its own switch and percentage.
- **1.1.0**: `secret-guard` reads the secrets folder beside the secrets file.

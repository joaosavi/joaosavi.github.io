# Configure and turn mods off

Every mod option is a row in `/config`. The setup handles the few settings a plugin cannot write itself.

## Change an option

Open `/config` and scroll to the mod. Each mod's page lists its options, their defaults and what they do. The status line picks up a change within five seconds; for the other mods, restart Claude Code or run `/reload-plugins`.

## In the settings file

The same options live under `pluginConfigs` in `~/.claude/settings.json`, keyed by `<mod>@cockpit`. This is useful to share a setup across machines:

~/.claude/settings.json:

```
{
  "pluginConfigs": {
    "hud@cockpit": { "options": { "style": "blocks", "icons": "unicode" } },
    "usage-limit@cockpit": { "options": { "timeZone": "Europe/Lisbon" } },
    "collision-guard@cockpit": { "options": { "git": "note" } }
  }
}
```

## What the setup writes

| Setting | Value | Why |
| --- | --- | --- |
| `statusLine` | the `hud` script, with `refreshInterval: 5` | A plugin cannot draw under the prompt. |
| `spinnerTipsEnabled` | `false` | So the `spinner-status` line replaces Claude Code's tip instead of sitting under it. |
| `autoCompactWindow` | `733000` on a 1M model, if you choose it | Claude Code summarizes the conversation at about 70% instead of near the end. |
| `pluginConfigs` | `band: "off"` for the hud, style, icons, time zone | Your answers to the setup questions. With the status line on, the band goes off so the rows do not show twice. |
| `enabledPlugins` | `claude-hud@claude-hud` off, when it was on | Its status line is the one the hud replaces. |
| `extraKnownMarketplaces.cockpit` | `autoUpdate: true` | The mods update by themselves. |

## Turn one mod off

Claude Code refuses to disable a plugin that an enabled plugin requires, and the `cockpit` bundle requires every mod. Disable the bundle first, then the mod:

terminal:

```
claude plugin disable cockpit@cockpit
claude plugin disable pipefail@cockpit
```

The other mods stay on. Enabling the bundle again turns the mod back on. `spinner-status` also has an **Enabled** option in `/config`, which turns it off without touching the bundle.

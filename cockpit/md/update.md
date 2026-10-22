# Update and uninstall

Updates arrive by themselves, a few minutes after the first message of a session. You can also update by hand, and remove everything in two commands.

## Automatic updates

The setup turns on auto-update for the `cockpit` marketplace. Claude Code then refreshes the marketplace once per session and updates every Cockpit mod with a new version, each one on its own. The open session keeps the versions it loaded until you run `/reload-plugins`; the next session loads the new ones.

## Update by hand

Updating the bundle does not update the mods: each mod is its own plugin. To update them all now:

terminal:

```
claude plugin marketplace update cockpit
for m in $(claude plugin list | grep -o '[a-z-]*@cockpit'); do claude plugin update "$m"; done
```

To update one mod, name it: `claude plugin update hud@cockpit`.

A mod that is new in a release does not arrive with the update: the bundle then lists it as a missing dependency. Install it by name, such as `claude plugin install todo@cockpit` for 1.4.0.

## Uninstall

terminal:

```
claude plugin uninstall cockpit@cockpit
claude plugin prune
```

Uninstalling the bundle leaves the mods installed; `claude plugin prune` removes them. The setup wrote `statusLine`, `spinnerTipsEnabled` and `autoCompactWindow` to your settings file and kept a backup next to it. Remove those keys by hand, or restore the backup.

## Remove the data

The mods leave their diaries in `~/.local/state/mods/`. Delete that folder to remove everything Cockpit wrote.

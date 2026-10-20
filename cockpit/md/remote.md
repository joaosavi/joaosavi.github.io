# Run on a remote machine

If you run Claude Code on a remote Linux machine over SSH, the mods work the same, and a few parts do more.

## Open the page through a tunnel

`panel` listens only on `127.0.0.1` of the machine where the sessions run. From your computer, open an SSH tunnel, then open `http://localhost:7777`. In a session opened over SSH, `/panel` prints this command with the machine's name.

on your computer:

```
ssh -N -L 7777:127.0.0.1:7777 <host>
```

To open the tunnel with every SSH login, add one line to the host's entry in `~/.ssh/config` on your computer:

~/.ssh/config:

```
Host <host>
  LocalForward 7777 127.0.0.1:7777
```

## Run the page as a service

Instead of letting a session start the page, run it under systemd. Set the `panel` option `autostart` to `false`, then run the server as a unit:

systemd unit:

```
[Service]
User=<user>
ExecStart=/usr/bin/python3 -I /home/<user>/.claude/plugins/marketplaces/cockpit/panel/server/panel.py
Environment=PANEL_CLAUDE=/home/<user>/.local/bin/claude
Restart=always
```

`PANEL_PORT`, `PANEL_MODEL` and `PANEL_REFRESH_MINUTES` set the server's options. Set `PANEL_GROUPS` to a comma-separated list of cgroup paths, such as `agents.slice`, to show those groups and everything under them on the page.

## Memory limits

When sessions run under a cgroup v2 memory limit, as a systemd service or a container sets, `memory-guard` keeps heavy commands under the tightest limit, the `hud` shows the room left under it, `/ram` shows each group, and the page shows each group's memory and the state of its systemd services.

## Remote Control and tmux

Every Cockpit command also answers in plain text, so it works when you drive a session over [Remote Control](https://code.claude.com/docs/en/remote-control) from claude.ai or the mobile app, where no pane is drawn. The page links a session to claude.ai when the session runs with Remote Control. For a session that runs in tmux, its **tmux** button copies the command that attaches to its pane.

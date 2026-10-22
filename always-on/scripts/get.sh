#!/bin/sh
# Baixa os scripts do Always-On para ~/always-on, ou para a pasta do primeiro argumento.
#   curl -fsSL https://joaosavi.github.io/always-on/scripts/get.sh | sh
set -eu
BASE=https://joaosavi.github.io/always-on/scripts
DEST=${1:-$HOME/always-on}
# A lista é conferida pelo build-txt.py: um arquivo novo na pasta scripts entra aqui.
FILES="install.sh config.env.example bin/agent bin/orchestrator-rc bin/orchestrator-spawn bin/recover-rc bin/memstat
bin/sessions-restart bin/sessions-idle bin/cockpit-panel templates/orchestrator.md templates/recover.md templates/projects.json"
for f in $FILES; do
    mkdir -p "$DEST/$(dirname "$f")"
    curl -fsSL "$BASE/$f" -o "$DEST/$f"
done
chmod 755 "$DEST/install.sh" "$DEST"/bin/*
[ -f "$DEST/config.env" ] || cp "$DEST/config.env.example" "$DEST/config.env"
echo "Scripts em $DEST. Ajuste $DEST/config.env e rode $DEST/install.sh"

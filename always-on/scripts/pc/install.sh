#!/usr/bin/env bash
# Monta no seu computador o harness do servidor numa configuração separada, ~/.claude-vps, para o
# `agent start --host` abrir agentes nele. Roda no computador, chamado pelo `agent host install <host>`
# do servidor depois do rsync que traz o harness para ~/.claude-vps/harness. A ~/.claude pessoal do
# computador não é tocada. Pode rodar de novo. macOS usa o Homebrew; Linux (o Ubuntu do WSL 2) usa o apt.
set -euo pipefail

CFG="$HOME/.claude-vps"
H="$CFG/harness"
export CLAUDE_CONFIG_DIR="$CFG"
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"

case "$(uname -s)" in
  Darwin)
    command -v brew >/dev/null || {
      echo "falta o Homebrew. No terminal do Mac: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"" >&2
      exit 1
    }
    for p in tmux jq node rsync; do command -v "$p" >/dev/null || brew install -q "$p"; done
    ;;
  Linux)
    miss=()
    for p in tmux jq rsync python3 git curl; do command -v "$p" >/dev/null || miss+=("$p"); done
    command -v node >/dev/null || miss+=(nodejs)
    [ ${#miss[@]} -eq 0 ] || sudo apt-get install -y -q "${miss[@]}"
    ;;
  *) echo "sistema $(uname -s) sem suporte; no Windows, rode dentro do WSL 2" >&2; exit 1 ;;
esac

command -v claude >/dev/null || curl -fsSL https://claude.ai/install.sh | bash

mkdir -p "$CFG/skills" "$CFG/agents"
cat "$H/CLAUDE.md" "$H/pc/CLAUDE.md" > "$CFG/CLAUDE.md"
for d in "$H"/skills/*/; do [ -d "$d" ] && ln -sfn "${d%/}" "$CFG/skills/$(basename "$d")"; done

# O settings.json do servidor, com cada marketplace de pasta apontado para a cópia que veio no rsync.
# O Claude Code regrava o arquivo, então as chaves do servidor entram por cima das que já estão lá.
tpl=$(jq --arg h "$H/marketplaces" '
  .extraKnownMarketplaces |= (. // {} | with_entries(
    if .value.source.source == "directory" then .value.source.path = ($h + "/" + .key) else . end))' "$H/settings.json")
if [ -f "$CFG/settings.json" ]; then
  jq -s '.[0] * .[1]' "$CFG/settings.json" <(echo "$tpl") > "$CFG/settings.json.new"
else
  echo "$tpl" > "$CFG/settings.json.new"
fi
mv "$CFG/settings.json.new" "$CFG/settings.json"

[ -f "$CFG/.claude.json" ] || echo '{}' > "$CFG/.claude.json"
jq '.hasCompletedOnboarding = true' "$CFG/.claude.json" > "$CFG/.claude.json.new" && mv "$CFG/.claude.json.new" "$CFG/.claude.json"

for m in $(jq -r '.extraKnownMarketplaces // {} | to_entries[] | if .value.source.source == "directory"
    then .value.source.path else .value.source.repo // empty end' "$CFG/settings.json"); do
  claude plugin marketplace add "$m" >/dev/null 2>&1 || true
done
claude plugin marketplace update >/dev/null 2>&1 || true
for p in $(jq -r '.enabledPlugins // {} | to_entries[] | select(.value) | .key' "$CFG/settings.json"); do
  claude plugin install "$p" >/dev/null 2>&1 || claude plugin update "$p" >/dev/null 2>&1 || echo "plugin $p não instalou" >&2
done

cp "$H/VERSION" "$CFG/VERSION"
if claude auth status 2>/dev/null | jq -e '.loggedIn' >/dev/null; then
  echo "harness $(cat "$CFG/VERSION") instalado; login ok"
else
  echo "harness $(cat "$CFG/VERSION") instalado; falta o login: no servidor, rode agent host login <host>"
fi

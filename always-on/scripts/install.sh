#!/usr/bin/env bash
# Monta o essencial do Claude Code Always-On numa VPS Ubuntu: swap, o slice dos agentes, o recover,
# o orquestrador, o comando agent e os timers que mantêm a máquina sozinha. O guia:
# https://joaosavi.github.io/always-on/
#
#   ./install.sh          instala. Pode rodar de novo: o que já está certo fica como está
#   ./install.sh --check  só confere, sem escrever nada, e sai com 1 quando falta alguma coisa
#
# Rode como o usuário que roda as sessões, com sudo sem senha. Os valores vêm do config.env ao lado
# deste script. Leia antes de rodar: less ~/always-on/install.sh
#
# O que ele escreve, e nada além disto. <orq> é o ORCHESTRATOR e <slice> o SLICE do config.env.
#
#   Com sudo, em /etc/systemd/system:
#     <slice>.slice              teto de memória dos agentes somados
#     recover.slice              256 MB reservados e teto de 512 MB para o recover
#     <orq>.service              o orquestrador, num tmux, ligado no boot
#     recover-rc.service         o recover, num tmux, ligado no boot
#     sessions-restart.service e .timer   todo dia às 7h40
#     sessions-idle.service e .timer      de hora em hora
#   Com sudo, fora do systemd:
#     /swapfile e uma linha no /etc/fstab, só se a máquina não tem swap e SWAP_GB > 0 (nunca num container)
#     /etc/needrestart/conf.d/always-on.conf, só se o needrestart existe
#     /var/lib/systemd/linger/<usuário>, pelo loginctl enable-linger
#     apt install de tmux, python3, git, curl e util-linux, só dos que faltam. O apt grava o que
#     cada pacote pede, como o grupo _ssh em /etc/group, o /etc/shells e o estado do dpkg
#     systemctl daemon-reload, enable e start das units acima
#   Como o seu usuário:
#     ~/.local/bin: agent, orchestrator-rc, orchestrator-context, recover-rc, memstat,
#                   sessions-restart, sessions-idle
#     ~/.local/bin/claude e ~/.local/share/claude, pelo instalador oficial, só se o claude falta
#     ~/.claude/backups, a cópia que o próprio Claude Code faz do ~/.claude.json
#     ~/.config/always-on/env               o nome do orquestrador e o slice, que os comandos leem
#     ~/.config/always-on/pc/               o que o agent start --host leva ao seu computador
#     ~/<orq>/CLAUDE.md, projects.json e .claude/settings.json   criados uma vez, depois são seus
#     ~/recover/CLAUDE.md                                         criado uma vez
#     ~/.claude.json e ~/.claude/settings.json   só as chaves das telas de primeira vez e da
#                                                confiança nas pastas ~/<orq> e ~/recover
#
# Rede: o apt, e o curl do instalador oficial do Claude Code (https://claude.ai/install.sh) quando o
# claude falta. Nenhuma porta é aberta, e nada escuta na rede.
# Não faz: firewall, SSH, usuário, Docker, Cockpit, ai-memory, Telegram, WhatsApp, cofre, a entrada
# de reserva do orquestrador. Esses são passos opcionais do guia.
set -euo pipefail

HERE=$(cd "$(dirname "$0")" && pwd)
USER=${USER:-$(id -un)}
[ -f "$HERE/config.env" ] && . "$HERE/config.env"
ORCHESTRATOR=${ORCHESTRATOR:-$USER}
SLICE=${SLICE:-agents}
SWAP_GB=${SWAP_GB:-8}
SYSTEM_MB=${SYSTEM_MB:-1024}
CHECK=0
case "${1:-}" in
    --check) CHECK=1 ;;
    "") ;;
    *) sed -n '6,7p' "$0" | sed 's/^# *//' >&2; exit 2 ;;
esac

BIN="$HOME/.local/bin"
UNITS=/etc/systemd/system
LOGIN_SHELL=$(getent passwd "$USER" | cut -d: -f7)
MISSING=0
CHANGED=0

ok()      { printf '  ok      %s\n' "$*"; }
missing() { printf '  falta   %s\n' "$*"; MISSING=$((MISSING + 1)); }
done_()   { printf '  feito   %s\n' "$*"; CHANGED=1; }
step()    { printf '\n%s\n' "$*"; }
die()     { printf 'install.sh: %s\n' "$*" >&2; exit 1; }

# put DESTINO DONO MODO < conteúdo
# Grava o arquivo quando ele não existe ou está diferente. DONO é root ou user.
put() {
    local dest=$1 owner=$2 mode=$3 tmp
    tmp=$(mktemp)
    cat >"$tmp"
    if [ -f "$dest" ] && cmp -s "$tmp" "$dest"; then
        ok "$dest"
    elif [ "$CHECK" = 1 ]; then
        if [ -f "$dest" ]; then missing "$dest está diferente"; else missing "$dest não existe"; fi
    elif [ "$owner" = root ]; then
        sudo install -m "$mode" -o root -g root "$tmp" "$dest" && done_ "$dest"
    else
        install -D -m "$mode" "$tmp" "$dest" && done_ "$dest"
    fi
    rm -f "$tmp"
}

# put_once DESTINO < conteúdo
# Grava só quando o arquivo não existe: depois dele, quem edita é você.
put_once() {
    local dest=$1
    if [ -f "$dest" ]; then
        cat >/dev/null
        ok "$dest"
    elif [ "$CHECK" = 1 ]; then
        cat >/dev/null
        missing "$dest não existe"
    else
        mkdir -p "$(dirname "$dest")"
        cat >"$dest" && done_ "$dest"
    fi
}

step "Pré-requisitos"
[ "$(id -u)" != 0 ] || die "rode como o usuário das sessões, não como root"
echo "$ORCHESTRATOR" | grep -Eq '^[a-z][a-z0-9-]*$' || die "ORCHESTRATOR=$ORCHESTRATOR: use letras minúsculas, números e hífen"
[ "$ORCHESTRATOR" != recover ] || die "o nome recover já é do agente de recover"
sudo -n true 2>/dev/null || die "o usuário $USER precisa de sudo sem senha (veja Como fazer a config inicial da VPS)"
[ -d /run/systemd/system ] || die "esta máquina não roda o systemd"
ok "usuário $USER com sudo sem senha"
apt_missing=""
for pkg in tmux python3 git curl util-linux; do
    dpkg -s "$pkg" >/dev/null 2>&1 || apt_missing="$apt_missing $pkg"
done
if [ -z "$apt_missing" ]; then
    ok "tmux, python3, git e curl"
elif [ "$CHECK" = 1 ]; then
    missing "pacotes:$apt_missing"
else
    sudo apt-get update -qq && sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq $apt_missing >/dev/null
    done_ "pacotes:$apt_missing"
fi
export PATH="$BIN:$PATH"
if command -v claude >/dev/null; then
    ok "claude $(claude --version 2>/dev/null | cut -d' ' -f1)"
elif [ "$CHECK" = 1 ]; then
    missing "o Claude Code não está instalado"
else
    curl -fsSL https://claude.ai/install.sh | bash >/dev/null
    done_ "Claude Code instalado em $BIN/claude"
fi

step "Swap"
if systemd-detect-virt --container -q 2>/dev/null; then
    ok "container: o swap vem do host ($(awk '/SwapTotal/ {print int($2/1024)}' /proc/meminfo) MB)"
elif [ "$(awk 'NR > 1' /proc/swaps | wc -l)" -gt 0 ]; then
    ok "swap ligado, $(awk '/SwapTotal/ {print int($2/1024)}' /proc/meminfo) MB"
elif [ "$SWAP_GB" = 0 ]; then
    ok "sem swap, como pede SWAP_GB=0"
elif [ "$CHECK" = 1 ]; then
    missing "a máquina não tem swap"
else
    sudo fallocate -l "${SWAP_GB}G" /swapfile
    sudo chmod 600 /swapfile
    sudo mkswap -q /swapfile
    sudo swapon /swapfile
    grep -q '^/swapfile ' /etc/fstab || echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab >/dev/null
    done_ "swap de ${SWAP_GB} GB em /swapfile"
fi

step "Slices de memória"
total_mb=$(awk '/MemTotal/ {print int($2/1024)}' /proc/meminfo)
swap_mb=$(awk '/SwapTotal/ {print int($2/1024)}' /proc/meminfo)
max_mb=$((total_mb - 512 - SYSTEM_MB))
high_mb=$((max_mb - 512))
[ "$high_mb" -gt 512 ] || die "a máquina tem $total_mb MB, pouco para o slice dos agentes"
echo "  memória $total_mb MB: agentes até $max_mb MB, lentos acima de $high_mb MB"
put "$UNITS/$SLICE.slice" root 644 <<EOF
[Unit]
Description=Sessões do Claude Code, com teto de memória somado

[Slice]
MemoryHigh=${high_mb}M
MemoryMax=${max_mb}M
MemorySwapMax=$((swap_mb / 2))M
EOF
put "$UNITS/recover.slice" root 644 <<'EOF'
[Unit]
Description=Memória reservada do agente de recover

[Slice]
MemoryMin=256M
MemoryMax=512M
CPUWeight=1000
EOF

step "Comandos em $BIN"
for f in agent orchestrator-rc orchestrator-context recover-rc memstat sessions-restart sessions-idle; do
    put "$BIN/$f" user 755 <"$HERE/bin/$f"
done

# O que o agent start --host leva ao seu computador: o instalador de lá e o que o CLAUDE.md ganha nele.
put "$HOME/.config/always-on/pc/install.sh" user 755 <"$HERE/pc/install.sh"
put "$HOME/.config/always-on/pc/CLAUDE.md" user 644 <"$HERE/pc/CLAUDE.md"

step "Pastas do orquestrador e do recover"
put "$HOME/.config/always-on/env" user 644 <<EOF
AGENT_ORCHESTRATOR=$ORCHESTRATOR
AGENT_SLICE=$SLICE.slice
EOF
sed -e "s/<orquestrador>/$ORCHESTRATOR/g" -e "s/<slice>/$SLICE/g" "$HERE/templates/orchestrator.md" |
    put_once "$HOME/$ORCHESTRATOR/CLAUDE.md"
put_once "$HOME/$ORCHESTRATOR/projects.json" <"$HERE/templates/projects.json"
# Ao abrir, retomar e compactar, o hook põe na conversa as tarefas abertas e os agentes vivos.
put_once "$HOME/$ORCHESTRATOR/.claude/settings.json" <<EOF
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume|compact",
        "hooks": [{ "type": "command", "command": "$BIN/orchestrator-context", "timeout": 30 }]
      }
    ]
  }
}
EOF
sed -e "s/<orquestrador>/$ORCHESTRATOR/g" -e "s/<slice>/$SLICE/g" "$HERE/templates/recover.md" |
    put_once "$HOME/recover/CLAUDE.md"

step "Telas de primeira vez do Claude Code"
# A escolha de tema, a confiança na pasta, o aviso do Remote Control e o do bypass travariam o
# serviço na subida, esperando uma tecla que ninguém aperta.
if python3 - "$CHECK" "$HOME/$ORCHESTRATOR" "$HOME/recover" <<'EOF'
import json, os, sys
from pathlib import Path
check, folders = sys.argv[1] == "1", sys.argv[2:]
home = Path.home()
changed = False

def load(p):
    try:
        return json.loads(p.read_text())
    except (OSError, ValueError):
        return {}

def save(p, data):
    tmp = p.with_suffix(p.suffix + ".install")
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(json.dumps(data, indent=2))
    os.replace(tmp, p)

cfg_path, settings_path = home / ".claude.json", home / ".claude" / "settings.json"
cfg, settings = load(cfg_path), load(settings_path)
want = [f for f in folders if not cfg.get("projects", {}).get(f, {}).get("hasTrustDialogAccepted")]
need = (want or not cfg.get("hasCompletedOnboarding") or not cfg.get("remoteDialogSeen")
        or not settings.get("skipDangerousModePermissionPrompt"))
if need and not check:
    for f in want:
        cfg.setdefault("projects", {}).setdefault(f, {})["hasTrustDialogAccepted"] = True
    # A escolha de tema da primeira abertura também espera uma tecla.
    cfg["hasCompletedOnboarding"] = True
    cfg.setdefault("theme", "dark")
    cfg["remoteDialogSeen"] = True
    settings["skipDangerousModePermissionPrompt"] = True
    save(cfg_path, cfg)
    save(settings_path, settings)
sys.exit(2 if need and check else 1 if need else 0)
EOF
then ok "pastas confiáveis, Remote Control e bypass aceitos"
else
    case $? in
        2) missing "telas de primeira vez ainda não aceitas" ;;
        *) done_ "pastas confiáveis, Remote Control e bypass aceitos" ;;
    esac
fi

step "Serviços"
# O linger mantém o /run/user/<uid> sem ninguém logado, e as units esperam o user-runtime-dir@ que o cria. Sem ele, depois de um reboot o socket de
# mensagens das sessões não tem onde ficar, e o orquestrador não enxerga os agentes.
if [ -f "/var/lib/systemd/linger/$USER" ]; then
    ok "linger ligado para $USER"
elif [ "$CHECK" = 1 ]; then
    missing "linger desligado para $USER"
else
    sudo loginctl enable-linger "$USER" && done_ "linger ligado para $USER"
fi
put "$UNITS/$ORCHESTRATOR.service" root 644 <<EOF
[Unit]
Description=Orquestrador dos agentes do Claude Code
After=network-online.target user-runtime-dir@$(id -u).service
Wants=network-online.target user-runtime-dir@$(id -u).service

[Service]
# A lista de pedidos: sem a primeira variável, os modelos novos não têm as ferramentas de tarefa.
Environment=CLAUDE_CODE_ENABLE_TODO_TOOLS=1
Environment=CLAUDE_CODE_TASK_LIST_ID=$ORCHESTRATOR
Type=forking
User=$USER
Slice=$SLICE.slice
MemoryHigh=768M
MemoryMax=1G
OOMPolicy=continue
ExecStart=/usr/bin/tmux -L $ORCHESTRATOR new-session -d -s $ORCHESTRATOR "$LOGIN_SHELL -lic $BIN/orchestrator-rc"
ExecStop=/usr/bin/tmux -L $ORCHESTRATOR kill-server
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
put "$UNITS/recover-rc.service" root 644 <<EOF
[Unit]
Description=Remote Control do Claude Code para o agente de recover
After=network-online.target user-runtime-dir@$(id -u).service
Wants=network-online.target user-runtime-dir@$(id -u).service

[Service]
Type=forking
User=$USER
Slice=recover.slice
OOMPolicy=continue
OOMScoreAdjust=-900
ExecStart=/usr/bin/tmux -L recover new-session -d -s recover "$LOGIN_SHELL -lic $BIN/recover-rc"
ExecStop=/usr/bin/tmux -L recover kill-server
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
put "$UNITS/sessions-restart.service" root 644 <<EOF
[Unit]
Description=Reinicia o orquestrador e o recover com biblioteca apagada, e retoma as sessões

[Service]
Type=oneshot
User=$USER
Slice=recover.slice
MemoryMax=256M
Environment=PATH=$BIN:/usr/local/bin:/usr/bin:/bin
Environment=TERM=xterm-256color
ExecStart=/usr/bin/python3 $BIN/sessions-restart
TimeoutStartSec=30min
EOF
put "$UNITS/sessions-restart.timer" root 644 <<'EOF'
[Unit]
Description=Procura sessão com biblioteca apagada depois do unattended-upgrade

[Timer]
# O apt-daily-upgrade.timer dispara às 6:00 com até 60 minutos de atraso sorteado.
OnCalendar=*-*-* 07:40

[Install]
WantedBy=timers.target
EOF
put "$UNITS/sessions-idle.service" root 644 <<EOF
[Unit]
Description=Encerra o agente e a sessão do recover parados há mais de 48 horas

[Service]
Type=oneshot
User=$USER
MemoryMax=128M
Environment=PATH=$BIN:/usr/local/bin:/usr/bin:/bin
ExecStart=/usr/bin/python3 $BIN/sessions-idle
EOF
put "$UNITS/sessions-idle.timer" root 644 <<'EOF'
[Unit]
Description=Procura agente esquecido de hora em hora

[Timer]
OnCalendar=hourly
RandomizedDelaySec=5min

[Install]
WantedBy=timers.target
EOF
if [ -d /etc/needrestart/conf.d ]; then
    # O needrestart reinicia todo serviço com biblioteca trocada e derrubaria a sessão no meio do
    # turno. Quem reinicia é o sessions-restart, que retoma as sessões depois. A entrada de reserva,
    # passo opcional do guia, já entra na regra.
    put /etc/needrestart/conf.d/always-on.conf root 644 <<EOF
\$nrconf{override_rc}{qr(^($ORCHESTRATOR|$ORCHESTRATOR-spawn|recover-rc)\\.service\$)} = 0;
EOF
fi

if [ "$CHECK" = 0 ] && [ "$CHANGED" = 1 ]; then
    sudo systemctl daemon-reload
fi
for t in sessions-restart.timer sessions-idle.timer; do
    if systemctl is-enabled -q "$t" 2>/dev/null; then ok "$t ligado"
    elif [ "$CHECK" = 1 ]; then missing "$t desligado"
    else sudo systemctl enable -q --now "$t" && done_ "$t ligado"
    fi
done
logged_in=0
[ -f "$HOME/.claude/.credentials.json" ] && logged_in=1
for s in "$ORCHESTRATOR" recover-rc; do
    if systemctl is-active -q "$s"; then
        ok "$s rodando"
    elif [ "$CHECK" = 1 ]; then
        missing "$s parado"
    elif [ "$logged_in" = 0 ]; then
        sudo systemctl enable -q "$s"
        missing "$s ligado no boot, mas parado: faça o login com claude e rode este script de novo"
    else
        sudo systemctl enable -q --now "$s" && done_ "$s rodando"
    fi
done

echo
if [ "$MISSING" -gt 0 ]; then
    echo "Faltam $MISSING itens."
    exit 1
fi
echo "Tudo certo. No app do Claude, a sessão $ORCHESTRATOR aparece pronta, e o recover abre pelo botão de nova sessão."

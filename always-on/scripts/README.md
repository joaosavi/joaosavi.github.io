# Instalador do Claude Code Always-On

Monta numa VPS Ubuntu o essencial do guia [Claude Code Always-On](https://joaosavi.github.io/always-on/): swap, o slice dos agentes com teto de memória, o recover, o orquestrador, o comando `agent` e os timers de manutenção. O Cockpit, a entrada de reserva e o ai-memory são passos opcionais do guia, e os scripts deles vêm junto em `bin/`.

A lista exata do que o `install.sh` escreve está no topo dele. Leia antes de rodar, e confira com `--check`, que não escreve nada.

Rode depois dos passos 1 a 5 do guia, com o usuário das sessões, sudo sem senha e o login do Claude Code feito:

```sh
curl -fsSL https://joaosavi.github.io/always-on/scripts/get.sh | sh
nano ~/always-on/config.env      # ORCHESTRATOR=<nome do orquestrador>
less ~/always-on/install.sh
~/always-on/install.sh --check   # mostra o que falta, sem escrever
~/always-on/install.sh
~/always-on/install.sh --check   # sai com 0 quando nada falta
```

O `install.sh` pode rodar de novo: grava só o arquivo que falta ou mudou. O `CLAUDE.md` e o `projects.json` do orquestrador ele cria uma vez, e depois quem edita é você.

| Arquivo | O que faz |
|---|---|
| `install.sh` | Instala e confere tudo, com os valores do `config.env` |
| `bin/agent` | Abre, lista e encerra os agentes, cada um num scope com o teto do projeto |
| `bin/orchestrator-rc` | Sobe o orquestrador ligado ao app, sempre na última conversa |
| `bin/orchestrator-spawn` | Opcional, fora do `install.sh`. Sobe a entrada de reserva: o modo servidor do Remote Control na pasta do orquestrador, que abre pelo app uma sessão nova já como orquestrador |
| `bin/recover-rc` | Sobe o recover no modo servidor do Remote Control |
| `bin/memstat` | Mostra o uso e os limites de cada slice e a pressão de memória |
| `bin/sessions-restart` | Depois da atualização do sistema, reinicia o serviço com biblioteca apagada e retoma as sessões |
| `bin/sessions-idle` | Encerra o agente parado há mais de 48 horas |
| `pc/` | O instalador do harness no seu computador e o que o `CLAUDE.md` ganha lá, para o `agent start --host` |
| `templates/` | O `CLAUDE.md` do orquestrador e do recover, e um `projects.json` de exemplo |

| `bin/cockpit-panel`, `bin/ai-memory-sync` | Opcionais, fora do `install.sh`: o painel do Cockpit como serviço e o espelho do ai-memory |

O nome do orquestrador e o slice ficam em `~/.config/always-on/env`, que o `agent`, o `orchestrator-rc`, o `orchestrator-spawn` e os timers leem.

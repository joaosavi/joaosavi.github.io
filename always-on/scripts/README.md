# Instalador do Claude Code Always-On

Monta numa VPS Ubuntu a infraestrutura do guia [Claude Code Always-On](https://joaosavi.github.io/always-on/): swap, o slice dos agentes com teto de memória, o recover, o orquestrador, o comando `agent`, os timers de manutenção e o Cockpit.

Rode depois dos passos 1 a 5 do guia, com o usuário das sessões, sudo sem senha e o login do Claude Code feito:

```sh
curl -fsSL https://joaosavi.github.io/always-on/scripts/get.sh | sh
nano ~/always-on/config.env      # ORCHESTRATOR=<nome do orquestrador>
~/always-on/install.sh
~/always-on/install.sh --check   # sai com 0 quando nada falta
```

O `install.sh` pode rodar de novo: grava só o arquivo que falta ou mudou. O `CLAUDE.md` e o `projects.json` do orquestrador ele cria uma vez, e depois quem edita é você.

| Arquivo | O que faz |
|---|---|
| `install.sh` | Instala e confere tudo, com os valores do `config.env` |
| `bin/agent` | Abre, lista e encerra os agentes, cada um num scope com o teto do projeto |
| `bin/orchestrator-rc` | Sobe o orquestrador ligado ao app, sempre na última conversa |
| `bin/recover-rc` | Sobe o recover no modo servidor do Remote Control |
| `bin/memstat` | Mostra o uso e os limites de cada slice e a pressão de memória |
| `bin/sessions-restart` | Depois da atualização do sistema, reinicia o serviço com biblioteca apagada e retoma as sessões |
| `bin/sessions-idle` | Encerra o agente parado há mais de 48 horas |
| `templates/` | O `CLAUDE.md` do orquestrador e do recover, e um `projects.json` de exemplo |

O nome do orquestrador e o slice ficam em `~/.config/always-on/env`, que o `agent`, o `orchestrator-rc` e os timers leem.

# Versões

Cockpit 1.6.0. O pacote leva a versão do lançamento, e cada mod leva a versão do lançamento em que mudou pela última vez.

Um mod que não mudou num lançamento mantém a versão, então o Claude Code não atualiza ele à toa.

| Mod | Versão |
| --- | --- |
| `cockpit` (pacote) | 1.6.0 |
| [`secret-guard`](https://joaosavi.github.io/cockpit/pt/md/secret-guard.md) | 1.3.0 |
| [`collision-guard`](https://joaosavi.github.io/cockpit/pt/md/collision-guard.md) | 1.3.0 |
| [`pipefail`](https://joaosavi.github.io/cockpit/pt/md/pipefail.md) | 1.3.0 |
| [`memory-guard`](https://joaosavi.github.io/cockpit/pt/md/memory-guard.md) | 1.3.0 |
| [`loop-breaker`](https://joaosavi.github.io/cockpit/pt/md/loop-breaker.md) | 1.3.0 |
| [`usage-limit`](https://joaosavi.github.io/cockpit/pt/md/usage-limit.md) | 1.3.0 |
| [`hud`](https://joaosavi.github.io/cockpit/pt/md/hud.md) | 1.3.0 |
| [`spinner-status`](https://joaosavi.github.io/cockpit/pt/md/spinner-status.md) | 1.0.0 |
| [`panel`](https://joaosavi.github.io/cockpit/pt/md/panel.md) | 1.6.0 |
| [`skill-loader`](https://joaosavi.github.io/cockpit/pt/md/skill-loader.md) | 1.3.0 |
| [`global-memory`](https://joaosavi.github.io/cockpit/pt/md/global-memory.md) | 1.3.0 |
| [`todo`](https://joaosavi.github.io/cockpit/pt/md/todo.md) | 1.5.0 |

## O que mudou

- **1.6.0**: o `panel` ganhou a vista Tasks, com as tarefas abertas da lista nativa agrupadas e filtradas por prioridade.
- **1.5.0**: o `todo` lista as tarefas abertas num grupo por estado, cada um ordenado por prioridade, a partir do metadata da tarefa ou de um assunto como `[dono] P1 espera: o que foi pedido`.
- **1.4.0**: mod novo `todo`, que mantém a lista de tarefas nativa na frente do agente.
- **1.3.0**: todo mod ganhou a opção `enabled`, e os guardas ganharam uma chave por passo. O `/cockpit:setup` desliga mods.
- **1.2.0**: o `usage-limit` passou a cuidar de cada janela por conta própria, com freio, commit e pausa separados para 5 horas e 7 dias, cada um com chave e porcentagem.
- **1.1.0**: o `secret-guard` passou a ler a pasta de segredos ao lado do arquivo de segredos.

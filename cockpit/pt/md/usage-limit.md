# `usage-limit`

Não deixa o limite de uso da conta acabar no meio de uma tarefa.

## Por que

Quando uma janela de 5 horas ou de 7 dias chega a 100%, a sessão para onde estiver, muitas vezes no meio de uma edição, e nada retoma. O mod desacelera antes disso, faz o agente commitar o trabalho, para numa reserva que fica para você e retoma a sessão sozinho quando a janela reinicia.

## As três etapas

Cada janela tem três etapas, cada uma com chave e porcentagem próprias:

| Etapa | Janela de 5 horas | Janela de 7 dias |
| --- | --- | --- |
| Freio: um subagente por vez | 90% | 97% |
| Commit: pede um commit `wip:` | 97% | 98% |
| Pausa: guarda o resto para você | 98% | 99% |

Os limites de 7 dias valem também para as janelas semanais por modelo, como `seven_day_opus`. Cada janela é julgada pelos próprios limites, e vale o resultado mais restritivo: janela pausada ganha de janela freada. Com duas janelas pausadas, segura a sessão a que reinicia por último.

## O que faz

- A partir do freio, roda um subagente por vez.
- A partir do commit, o agente recebe uma vez por janela o pedido de commitar o trabalho em andamento em cada repo que mudou, com mensagem `wip:` e sem push. Ele põe no stage só os arquivos que mudou, então o trabalho de outra sessão no mesmo repo fica de fora. Só a conversa principal recebe o pedido.
- Na pausa, toda chamada de ferramenta é recusada, menos um comando que só faz stage e commit (`git add`, `git commit`, `cd`, ligados por `&&`), para o trabalho ser commitado mesmo quando uma rajada de pedidos pula a etapa do commit. O agente escreve em até 3 linhas onde parou, e o mod agenda a retomada para a hora do reinício mais 2 minutos.
- Um prompt que você digita durante a pausa ganha um turno sem subagentes, pago com a reserva.
- Um prompt que ninguém digitou (uma rotina, outra sessão, uma notificação de tarefa) fica guardado e é entregue na retomada.
- A faixa acima do prompt mostra cada janela com barra, marca de pausa própria, porcentagem e hora do reinício, a partir de 75% por padrão. A barra fica amarela a partir do freio ou do commit da janela, e vermelha a partir da pausa.
- A status line embaixo do prompt mostra o estado enquanto o mod segura alguma coisa.

## Comandos

`/limit` mostra cada janela com as etapas, o estado e o que está guardado para a retomada. Em texto simples, então lê igual pelo Remote Control.

## Opções

| Opção | Padrão | O que faz |
| --- | --- | --- |
| `enabled` | `true` | Desligado, o mod não faz nada: sem freio, commit, pausa nem retomada, e o `/limit` some. Vale na próxima sessão, ou depois de `/reload-plugins`. |
| `fiveHourThrottle` | `true` | Freio na janela de 5 horas. |
| `fiveHourThrottleAt` | `90` | A partir dessa porcentagem da janela de 5 horas, um subagente por vez. |
| `fiveHourCommit` | `true` | Pedido de commit na janela de 5 horas. |
| `fiveHourCommitAt` | `97` | A partir dessa porcentagem da janela de 5 horas, pede ao agente uma vez por janela que commite sem push. |
| `fiveHourPause` | `true` | Pausa na janela de 5 horas. |
| `fiveHourPauseAt` | `98` | A sessão pausa nessa porcentagem da janela de 5 horas. |
| `sevenDayThrottle` | `true` | Freio nas janelas de 7 dias. |
| `sevenDayThrottleAt` | `97` | A partir dessa porcentagem de uma janela de 7 dias, um subagente por vez. |
| `sevenDayCommit` | `true` | Pedido de commit nas janelas de 7 dias. |
| `sevenDayCommitAt` | `98` | A partir dessa porcentagem de uma janela de 7 dias, pede ao agente uma vez por janela que commite sem push. |
| `sevenDayPause` | `true` | Pausa nas janelas de 7 dias. |
| `sevenDayPauseAt` | `99` | A sessão pausa nessa porcentagem de uma janela de 7 dias. |
| `timeZone` | vazio | Fuso IANA das horas de reinício mostradas, como `America/Sao_Paulo`. Vazio usa o do sistema. |
| `resume` | `true` | Retoma a sessão quando a janela reinicia, depois da pausa ou do erro de limite. Desligado, você retoma, e os prompts automáticos que chegam na pausa são descartados em vez de guardados. O nome antigo `resumeOnError` ainda funciona. |
| `bandFrom` | `75` | Mostra a faixa a partir dessa porcentagem da janela mais cheia. |

As opções por janela não têm padrão no manifesto, então as configurações de antes da 1.2 continuam valendo onde a opção nova não foi definida. `alert` define o freio de todas as janelas, `commitAt` o commit (`0` desliga) e `reserve` a pausa em 100 menos o valor. A opção da janela sempre ganha delas na própria etapa.

## O que grava

- `~/.local/state/mods/usage-limit/<dia>-<sessão>.jsonl`: uma linha por mudança de estado, recusa, prompt guardado e retomada, mais uma linha `session-summary` no fim da sessão.
- A última leitura das janelas, no armazenamento comum dos mods, em `windows`, para uma sessão nova começar da leitura que outra fez.

## Custo

O hook de `tool.call` somou uns 6 ms por chamada de ferramenta na máquina Linux do autor (60 chamadas medidas em outubro de 2026, estimativa).

## Limites

- A leitura chega com cada resposta do modelo, então uma rajada de pedidos em paralelo pode passar da pausa antes da próxima leitura. A retomada depois do erro de limite e o commit liberado na pausa cobrem esse caso.
- Um prompt de origem que o Claude Code não sabe classificar conta como seu e gasta a reserva.
- `/clear`, `/resume` e `/branch` cancelam a retomada agendada e descartam as mensagens guardadas da conversa anterior.
- Na pausa, o comando que só faz commit passa pela ferramenta Bash ou, no Windows sem Git Bash, pela ferramenta PowerShell.
- Testado só no Linux.

## Instalar só este mod

O pacote `cockpit` já instala o `usage-limit` com os outros. Para ter só ele:

terminal:

```
claude plugin marketplace add joaosavi/cockpit
claude plugin install usage-limit@cockpit
```

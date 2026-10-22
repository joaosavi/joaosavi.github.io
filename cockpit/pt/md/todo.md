# `todo`

Mantém a lista de tarefas nativa do Claude Code na frente do agente: as tarefas abertas no início da sessão e em cada prompt seu, o lembrete de que pedido novo vira tarefa antes de tudo, e a tarefa concluída movida para um arquivo de histórico.

## Por quê

As ferramentas de tarefa (`TaskCreate`, `TaskList`, `TaskUpdate`, `TaskGet`) gravam um JSON por tarefa em `~/.claude/tasks/<lista>/`, então a lista sobrevive à compactação, ao `--resume` e ao `--continue`. O modelo esquece que a lista existe. Depois da compactação ele trabalha pelo resumo, e o pedido que vivia só na conversa se perde. Uma sessão que recebe muitos pedidos, como um orquestrador que distribui trabalho a outros agentes, precisa da lista lida de volta do disco.

## O que faz

- No início da sessão, acrescenta uma nota com as tarefas abertas da lista da sessão.
- Em cada prompt seu, anexa as tarefas abertas e as concluídas desde o último prompt. Mensagem de outra sessão, notificação e agendamento não recebem nada.
- Com lista nomeada (`CLAUDE_CODE_TASK_LIST_ID`), o mesmo prompt leva a regra: pedido novo vira `TaskCreate` antes de qualquer trabalho, com o dono no assunto, como `[dono] o que foi pedido`.
- Move a tarefa concluída para `~/.local/state/mods/todo/<lista>.jsonl` e apaga o arquivo dela, para a lista guardar só o que está aberto. Vale para tarefa concluída pelo `TaskUpdate` e para arquivo que um script reescreveu.

## Ligue as ferramentas de tarefa

O Claude Code oferece as ferramentas de tarefa por padrão só no Opus 4.7, no Sonnet 4.6, no Haiku 4.5 e nos modelos anteriores. Num modelo mais novo, abra o Claude Code com a variável. Para dividir uma lista entre sessões, dê nome a ela também:

terminal:

```
CLAUDE_CODE_ENABLE_TODO_TOOLS=1 CLAUDE_CODE_TASK_LIST_ID=pedidos claude
```

## Opções

| Opção | Padrão | O que faz |
| --- | --- | --- |
| `enabled` | `true` | Desligado, o mod não faz nada. Vale na próxima sessão, ou depois de `/reload-plugins`. |
| `remind` | `true` | Com lista nomeada, cada prompt seu leva a regra do pedido. |
| `archive` | `true` | Move a tarefa concluída da lista para o histórico. Desligado, a concluída fica na lista. |

## O que grava

`~/.local/state/mods/todo/<dia>-<sessão>.jsonl`: uma linha por nota, contexto de prompt e arquivamento, mais uma linha `session-summary`. O histórico, uma linha por tarefa concluída, fica em `~/.local/state/mods/todo/<lista>.jsonl`. Cada linha tem `at`, `session` e `event`.

## Custo

As tarefas abertas vão inteiras em cada prompt seu, uns 15 tokens por tarefa, no máximo 30. O único hook de `tool.call` é no `TaskUpdate`.

## Limites

- No plano Team ou Enterprise, o guarda embutido `sec-default@builtin` ignora o hook `session.compact` de mod instalado pelo usuário, e a nota logo depois da compactação não aparece. O próximo prompt seu leva a lista. Um hook `SessionStart` com o matcher `compact` no `settings.json` da sessão imprime as tarefas abertas na hora.
- O id das tarefas volta a 1 quando todo arquivo saiu da lista. O histórico guarda o assunto ao lado de cada id.
- Testado só no Linux.

## Instalar só este mod

O pacote `cockpit` já instala o `todo` com os outros. Para ter só ele:

terminal:

```
claude plugin marketplace add joaosavi/cockpit
claude plugin install todo@cockpit
```

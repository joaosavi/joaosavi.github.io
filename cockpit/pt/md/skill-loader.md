# `skill-loader`

Carrega a skill certa na hora certa, para o `CLAUDE.md` não precisar de regra do tipo "carregue a skill X antes de Y".

## Por que

Uma regra no `CLAUDE.md` que manda carregar uma skill antes de editar um arquivo só funciona quando o agente lembra. O mod olha as chamadas de ferramenta e entrega a skill ele mesmo.

## O que faz

| Quando o agente | Skill |
| --- | --- |
| Lê ou escreve um `.ts`, `.tsx`, `.mts` ou `.cts` | `typescript-best-practices` |
| Lê ou escreve `SKILL.md`, `AGENTS.md` ou `CLAUDE.md` | `writing-for-agents` |
| Lê ou escreve `CONTEXT.md`, `CONTEXT-MAP.md` ou um arquivo em `adr/`, `adrs/` ou `decisions/` | `domain-modeling` |
| Lê ou escreve um `README`, ou roda `git commit`, `gh pr create` ou `gh pr edit` | `technical-writing` |

- Na leitura, o texto inteiro da skill vem junto com o arquivo. O Edit exige leitura antes, então a skill chega antes da edição.
- Numa escrita sem leitura (arquivo novo, commit, PR), o mod segura a chamada uma vez, com o texto da skill na recusa, e o agente repete a chamada.
- Quando o seu prompt traz um erro ou diz que algo quebrou, o mod lembra o agente de carregar `diagnosing-bugs`.

Cada skill carrega uma vez por conversa. A compactação zera a lista, porque o resumo pode perder o texto de uma skill.

## As skills

O mod traz as cinco skills que entrega, na pasta `skills/`, então funciona sem nada mais instalado. O Claude Code também lista elas como `skill-loader:<nome>`. O mod lê uma skill primeiro da própria pasta, depois de `<projeto>/.claude/skills/<nome>/SKILL.md` e depois de `~/.claude/skills/<nome>/SKILL.md`. As skills são de Matt Pocock, sob licença MIT.

## Opções

| Opção | Padrão | O que faz |
| --- | --- | --- |
| `enabled` | `true` | Desligado, o mod não faz nada: nenhuma skill é entregue e nada é segurado. Vale na próxima sessão, ou depois de `/reload-plugins`. |
| `holdWrites` | `true` | Segura uma vez a escrita, o commit ou o PR, com a skill na recusa, para o agente refazer seguindo a skill. Desligado, a chamada roda e a skill vem com o resultado. |
| `diagnoseReminder` | `true` | Lembra o agente de carregar `diagnosing-bugs` quando o seu prompt traz um erro ou diz que algo quebrou. |

## O que grava

`~/.local/state/mods/skill-loader/<dia>-<sessão>.jsonl`: uma linha por skill carregada, chamada segurada, skill que faltou e lembrete, mais uma linha `session-summary`. Cada linha tem `at`, `session` e `event`.

## Custo

O hook somou uns 2 ms por chamada de ferramenta na máquina Linux do autor (60 chamadas medidas em outubro de 2026, estimativa). Uma escrita segurada custa ao agente uma chamada a mais.

## Limites

- Subagentes ficam de fora: a skill entregue ali cairia na conversa principal.
- A detecção de erro reconhece frases comuns em inglês e em português e o formato de stack trace, então perde um erro descrito com outras palavras.
- Testado só no Linux.

## Instalar só este mod

O pacote `cockpit` já instala o `skill-loader` com os outros. Para ter só ele:

terminal:

```
claude plugin marketplace add joaosavi/cockpit
claude plugin install skill-loader@cockpit
```

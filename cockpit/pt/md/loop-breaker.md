# `loop-breaker`

Percebe quando o agente anda em círculo e manda ele parar e mudar de abordagem.

## Por que

Um agente que segue editando o mesmo arquivo depois da mesma falha gasta token e tempo sem chegar mais perto. Um empurrão curto na hora certa faz ele dar um passo atrás, o que uma regra no `CLAUDE.md` não garante.

## O que faz

O mod conta três sinais por loop do agente (a conversa principal e cada subagente), zerados no fim de cada turno:

- Tentativas de correção: edições num arquivo enquanto um comando que falhou não passou de novo.
- Erros repetidos: o mesmo erro voltando, ignorando números, caminhos e valores entre aspas.
- Chamadas repetidas: a mesma ferramenta com os mesmos argumentos, em sequência.

Quando uma contagem chega ao limite, o mod acrescenta uma nota ao resultado da ferramenta. A nota começa com `Loop check` e pede ao agente que escreva o que tentou e depois releia o código, forme uma hipótese nova ou pergunte a você. Nada é recusado.

## Opções

| Opção | Padrão | O que faz |
| --- | --- | --- |
| `enabled` | `true` | Desligado, o mod não faz nada: nada é contado, nenhum empurrão. Vale na próxima sessão, ou depois de `/reload-plugins`. |
| `editLimit` | `5` | Tentativas de correção num arquivo, num turno, antes do empurrão. |
| `errorLimit` | `3` | Vezes que o mesmo erro pode voltar num turno antes do empurrão. |
| `repeatLimit` | `3` | Chamadas idênticas em sequência antes do empurrão. |
| `editCheck` | `true` | Empurra depois de `editLimit` tentativas de correção num arquivo. |
| `errorCheck` | `true` | Empurra depois de o mesmo erro voltar `errorLimit` vezes. |
| `repeatCheck` | `true` | Empurra depois de `repeatLimit` chamadas idênticas em sequência. |

## O que grava

`~/.local/state/mods/loop-breaker/<dia>-<sessão>.jsonl`: uma linha por empurrão com o tipo e a contagem, mais uma linha `session-summary`. Cada linha tem `at`, `session` e `event`.

## Custo

O hook somou uns 2 ms por chamada de ferramenta na máquina Linux do autor (60 chamadas medidas em outubro de 2026, estimativa).

## Limites

- A falha é lida do código de saída e de palavras de falha na saída, então ferramenta que falha calada não conta.
- A contagem zera no fim de cada turno, então um loop que atravessa vários turnos passa.
- Testado só no Linux.

## Instalar só este mod

O pacote `cockpit` já instala o `loop-breaker` com os outros. Para ter só ele:

terminal:

```
claude plugin marketplace add joaosavi/cockpit
claude plugin install loop-breaker@cockpit
```

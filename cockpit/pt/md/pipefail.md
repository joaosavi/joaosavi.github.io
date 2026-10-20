# `pipefail`

Põe `set -o pipefail;` num comando que passa um teste, typecheck ou lint por `tail`, `head` ou `grep`.

## Por que

Um pipeline sai com o código do último comando. `yarn test | tail -20` sai com 0 quando o teste reprova, porque o `tail` deu certo, e o agente lê aprovado. Reescrever o comando não custa nada e poupa o agente de uma conclusão errada.

## O que faz

- Reconhece o executor onde ele roda: `yarn`, `npm run`, `pnpm` ou `bun run` com `test`, `e2e`, `typecheck`, `lint`, `check` e parecidos, ou com um script listado em `extraRunners`, e também `turbo run`, `vitest`, `jest`, `playwright test`, `tsc`, `vue-tsc`, `eslint`, `pytest`, `go test` e `cargo test`. Texto entre aspas e corpo de heredoc não contam.
- Põe `set -o pipefail;` na frente, roda e avisa o agente que um `| head` pode fazer o executor sair com 141 (SIGPIPE).
- Deixa em paz um comando que já fala em `pipefail`.

o que o mod reescreve:

```
yarn test | tail -20
# vira
set -o pipefail; yarn test | tail -20
```

## Opções

| Opção | Padrão | O que faz |
| --- | --- | --- |
| `extraRunners` | lista vazia | Nomes de script que também contam como executor quando um gerenciador de pacotes chama: `yarn <nome>`, `npm run <nome>`, `pnpm <nome>`, `bun run <nome>`. |

Ponha aqui o script de checagem do repo quando o código de saída dele diz se o código funciona, como um `verify` que roda lint, tipos e testes. O mod passa a reescrever `yarn verify | tail` também.

## O que grava

`~/.local/state/mods/pipefail/<dia>-<sessão>.jsonl`: uma linha por reescrita com o executor (`yarn vitest`, nunca o comando inteiro), mais uma linha `session-summary`. Cada linha tem `at`, `session` e `event`.

## Custo

O hook somou uns 2 ms por chamada Bash na máquina Linux do autor (56 chamadas medidas em outubro de 2026, estimativa).

## Limites

- Só `tail`, `head` e `grep` como filtro. `sed`, `awk` e outros ficam de fora.
- Executor escondido dentro de um script que o comando chama não aparece.
- Só a ferramenta Bash. No Windows sem Git Bash, os comandos passam pela ferramenta PowerShell e o mod não mexe. Testado só no Linux.

## Instalar só este mod

O pacote `cockpit` já instala o `pipefail` com os outros. Para ter só ele:

terminal:

```
claude plugin marketplace add joaosavi/cockpit
claude plugin install pipefail@cockpit
```

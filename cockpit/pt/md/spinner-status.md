# `spinner-status`

Troca a dica embaixo do spinner por uma linha própria: em que ponto a sessão está, escrita pelo Haiku, ou uma dica sobre os mods instalados que combina com o momento.

```
✻ Propagating… (6s · ↓ 90 tokens)
  ⎿  Now: Running the tests after the fix to the date filter
```

O spinner continua como o Claude Code desenha. A linha vai embaixo, cortada na largura da tela e em 100 caracteres. Um rótulo em negrito diz o que ela é: `Now:` para o ponto da sessão e `Mods:` para dica dos mods.

## Desligue a dica nativa

Um mod não remove a linha de dica do próprio Claude Code. Desligue no `settings.json`, ou as duas aparecem juntas. O `/cockpit:setup` já faz isso, e é a mesma chave da linha **Show tips** do `/config`.

~/.claude/settings.json:

```
{ "spinnerTipsEnabled": false }
```

## Os modos

| Modo | O que a linha mostra | Chamadas ao modelo |
| --- | --- | --- |
| `mixed` | O resumo da sessão e uma dica que o Haiku escolheu para o momento, trocando a cada 15 segundos. Antes da primeira resposta, uma dica do catálogo. É o padrão. | Uma por turno |
| `tips` | Uma dica do catálogo, nova a cada turno. | Nenhuma |
| `summary` | Só o resumo da sessão. Antes da primeira resposta, nada extra. | Uma por turno |

O catálogo tem uma dica por comando e por mod do Cockpit: `/panel`, `/hud`, `/limit`, `/ram`, e o que `memory-guard`, `loop-breaker`, `secret-guard`, `pipefail` e `usage-limit` fazem. Os rótulos e o catálogo são em inglês. Nos modos `mixed` e `summary`, o Haiku escreve na língua da configuração `language` do Claude Code, ou na língua em que você escreve.

## Opções

| Opção | Padrão | O que faz |
| --- | --- | --- |
| `enabled` | `true` | Desligado, o mod não faz nada e não chama modelo. |
| `mode` | `mixed` | `mixed`, `tips` ou `summary`. |
| `model` | `claude-haiku-4-5-20251001` | O modelo que escreve a linha: um apelido como `haiku` ou um id completo. |

## Custo

Cada turno da conversa principal faz no máximo uma chamada ao modelo, em segundo plano, quando o turno começa. O spinner nunca espera: mantém a linha anterior até a nova chegar. O modelo lê os 3 últimos prompts que você digitou e o texto do agente entre eles, no máximo 3.000 caracteres, sem chamada nem saída de ferramenta. A resposta tem teto de 150 tokens.

Numa sessão de teste, três turnos gastaram 1.574 tokens de entrada e 139 de saída: uns 525 e 46 por turno, ou cerca de US$ 0,0008 por turno no preço do Haiku 4.5. Cada chamada levou cerca de um segundo.

## A resposta é dado

A linha que o Haiku escreve é mostrada, nunca executada. O mod fica só com as linhas `NOW:` e `TIP:`, tira caracteres de controle e marcação, junta em uma linha e corta na largura. As instruções dizem ao modelo que o trecho da sessão é dado, não instrução.

## O que grava

No fim de cada sessão, uma linha `session-summary` em `~/.local/state/mods/spinner-status/<dia>-<sessão>.jsonl`, com os turnos, as chamadas por resultado, as puladas porque uma ainda rodava, os tokens, o tempo do modelo e o tamanho do trecho. Nunca grava o trecho nem a linha.

## Limites

- A chamada ao modelo passa pelo próprio Claude Code, sem comando próprio, então funciona igual no macOS, no Windows e no Linux. Testado só no Linux.
- A linha do spinner é da interface de terminal. Testado só em terminal.

## Instalar só este mod

O pacote `cockpit` já instala o `spinner-status` com os outros. Para ter só ele:

terminal:

```
claude plugin marketplace add joaosavi/cockpit
claude plugin install spinner-status@cockpit
```

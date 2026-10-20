# `hud`

Mostra o modelo, o projeto e a branch, o contexto, os limites do plano e a folga de memória, embaixo do prompt como status line ou acima dele na faixa. Durante um turno, a faixa mostra também a última nota que outro mod deixou num resultado de ferramenta, que de outro jeito só o modelo lê.

## Os quatro estilos

Escolha com a opção `style`. Cada estilo larga primeiro o campo menos útil quando o terminal é estreito, então nenhuma linha passa da largura. Abaixo, a saída real do `statusline.sh` para a mesma sessão.

### `refined`

Duas linhas com barras em degradê. O padrão.

```
Opus 5.5   acme-api   feat/billing  ● 1  ? 1     43m  ·  0 calls
ctx ●●○○○○ 38%   5h ●●●●○○ 64% 2h20m   7d ●●●●●○ 81%   mem 2.4G
```

### `blocks`

Cada campo com fundo colorido.

```
 Opus 5.5   acme-api   feat/billing  ● 1  ? 1                43m
 ctx 38%   5h 64%  resets 2h20m  7d 81%   mem 2.4G free 
```

### `minimal`

Campos escritos por extenso, barras finas.

```
acme-api  feat/billing  1 modified · 1 untracked  Opus 5.5 · 43m
ctx ━━──── 38%   5h ━━━━── 64% 2h20m   7d ━━━━━─ 81%   2.4G free
```

### `compact`

Uma linha quando cabe, duas quando não cabe.

```
acme-api  feat/billing ● 1 ? 1                          Opus 5.5
ctx 38% │ 5h 64% 2h20m │ 7d 81% │ mem 2.4G
```

## A status line

Um mod não desenha embaixo do prompt: esse lugar é do comando de status line das configurações. O mod traz um, `statusline/statusline.sh`, e o `/cockpit:setup` grava ele para você. Para gravar à mão no macOS ou no Linux, ponha isto no `~/.claude/settings.json`, com `band` em `off` para as linhas não aparecerem duas vezes:

~/.claude/settings.json:

```
{
  "statusLine": { "type": "command", "command": "~/.claude/plugins/marketplaces/cockpit/hud/statusline/statusline.sh", "refreshInterval": 5 },
  "pluginConfigs": { "hud@cockpit": { "options": { "band": "off", "style": "refined", "icons": "nerd" } } }
}
```

O script precisa do Node 22.18 ou mais novo. `refreshInterval` roda o script de novo a cada 5 segundos, para o git, o PR e o tempo de sessão ficarem em dia com a sessão parada. No Windows, o PowerShell não roda `.sh`: aponte o comando para `node ~/.claude/plugins/marketplaces/cockpit/hud/statusline/statusline.ts`, com barra normal.

### Git e o PR

O campo do git mostra a branch, os commits a enviar e a receber, os arquivos no stage, os mudados fora do stage e os não rastreados, ou `synced` quando não há nada. O PR é o pull request aberto da branch, do `gh pr view`, com os checks: passando, falhando ou rodando. O `gh` leva um segundo, então o script roda ele em segundo plano no máximo uma vez por minuto e mostra a última resposta enquanto isso. Sem `gh`, ou sem PR aberto, o campo some.

### Ícones

Com `icons` em `nerd`, o padrão, os campos de git, pasta, modelo e memória usam glifos da Nerd Font, que só aparecem se a fonte do terminal for uma. Com `unicode`, usam `↑ ↓ + ● ? ✓` e nenhum glifo para pasta, modelo e memória.

## A faixa acima do prompt

Sem a status line, o hud desenha na faixa acima do prompt. Com `band` em `panel`, o padrão, são duas linhas, com o lado direito da primeira encostado na última coluna:

```
Opus 5.5 · my-app  main●                              38m · 214 calls
ctx ▰▰▰▰▱▱▱▱▱▱  42%   5h ▰▰▰▰▰▰▱▱▱▱  61% resets 2h30m   7d ▰▰▰▰▱▱▱▱▱▱  44%   mem 1.9G free
```

Durante um turno, quando outro mod deixou uma nota, vem a linha de atividade, como `loop-breaker: repeated error`. Ela some quando o turno acaba. O Claude Code já desenha a ferramenta rodando, os erros dela, os subagentes e o tempo do turno, então a faixa deixa isso de fora.

| Campo | Cores |
| --- | --- |
| `ctx`, o contexto | verde abaixo de 60%, amarelo abaixo de 85%, vermelho a partir de 85% |
| `5h` e `7d`, as janelas do plano | verde abaixo de 75%, amarelo abaixo de 90%, vermelho a partir de 90% |
| `mem`, a memória que ainda cabe | amarelo abaixo de 1 GB, vermelho abaixo de 500 MB |
| Linha de atividade | amarelo |

Num terminal estreito, a faixa larga campos em vez de quebrar a linha: primeiro encurta as barras, depois tira o `mem`, depois mostra `ctx`, `5h` e `7d` só em porcentagem, e por fim tira a contagem até o reinício. Com `band` em `line`, desenha uma linha só:

```
Opus 5.5 │ my-app  main● │ ctx 42% │ 5h 61% │ 7d 44% │ mem 1.9G
```

## A janela do /hud

```
SESSION   Opus 5.5 · my-app  main● · 38m · 214 calls · ctx 42%
LIMITS    5h 61% resets 2h30m · 7d 44% resets 3d20h
MEMORY    session 1.5G · slice 3.0/5.0G · 1.9G fits
NOW       Bash yarn turbo run test 0:42 · 2 subagents
TODAY     2 skills · 1 loop nudge · 0 refusals
```

`MEMORY` mostra o cgroup da sessão e o grupo cujo limite define a folga, ou a memória da máquina sem cgroup. `TODAY` conta as linhas de hoje nos diários dos outros mods. A janela atualiza a cada 2 segundos enquanto está aberto; `r` atualiza na hora e `esc` fecha.

## Opções

No `/config`, ou em `pluginConfigs` no `~/.claude/settings.json`.

| Opção | Padrão | O que faz |
| --- | --- | --- |
| `band` | `panel` | `panel` desenha duas linhas acima do prompt, `line` uma, `off` nenhuma (o `/hud` continua). Use `off` com a status line. |
| `activity` | `true` | Mostra a linha de atividade durante o turno. |
| `memory` | `true` | Mostra a folga de memória na faixa e a linha `MEMORY`. |
| `bar` | `dots` | Glifos da barra: `blocks` (▰▱), `solid` (█░), `line` (━─), `dots` (●○) ou `squares` (■□). |
| `barWidth` | `10` | Células de uma barra cheia, de 4 a 30. Terminal estreito ainda encolhe. |
| `colors` | vazio | Cores de ok, alerta e crítico, separadas por espaço: nome, `#rrggbb` ou número de 256 cores. Vazio usa verde, amarelo e vermelho. |
| `hide` | vazio | Campos a esconder, separados por vírgula: `model`, `project`, `branch`, `age`, `calls`, `ctx`, `5h`, `7d`, `reset`, `mem`. |
| `barColor` | `gradient` | `gradient` pinta cada célula pela posição, do verde ao vermelho. `solid` pinta a barra inteira pela porcentagem. `tone` usa as três cores de `colors`. |
| `style` | `refined` | Layout da status line: `refined`, `blocks`, `minimal` ou `compact`. |
| `icons` | `nerd` | `nerd` para glifos da Nerd Font, `unicode` para marcas simples. |
| `contextBase` | `compact` | Contra o que o `ctx` mede. `compact`: 100% é a janela de auto-compact, quando menor que a do modelo. `window`: a janela inteira do modelo. Só na status line. |
| `timeZone` | vazio | Fuso IANA das horas mostradas e do que conta como hoje. Vazio usa o do sistema. |

## Custo

O hook que desenha a faixa não lê disco: só arruma valores que eventos e timers já leram. A cada 15 segundos, parado ou não, roda um `git status` (limite de 3 segundos) e uma leitura de memória. Durante um turno, um timer de 1 segundo lê a lista de agentes para o `/hud` e só redesenha com a janela aberta. Cada chamada de ferramenta pede dois redesenhos, e o Claude Code limita a 10 por segundo.

## Limites

- No macOS e no Windows não há limite por sessão, então o campo de memória mostra a máquina inteira. Essas leituras foram testadas só contra saída simulada.
- Quando a leitura falha, o campo de memória some.
- O campo de PR precisa do `gh` logado.
- A faixa, a status line e a janela do /hud são da interface de terminal. Testado só em terminal, e a configuração do Windows não foi testada.

## Instalar só este mod

O pacote `cockpit` já instala o `hud` com os outros. Para ter só ele:

terminal:

```
claude plugin marketplace add joaosavi/cockpit
claude plugin install hud@cockpit
```

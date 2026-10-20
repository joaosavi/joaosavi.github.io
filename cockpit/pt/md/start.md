# Início rápido

O Cockpit é um pacote de 11 mods para o [Claude Code](https://claude.com/product/claude-code). Os guardas barram o erro de um agente antes de ele custar caro: um segredo na saída de uma ferramenta, um pipe que esconde um teste reprovado, um build morto por falta de memória, um commit que leva junto a edição de outra sessão. Os instrumentos mostram em que ponto a sessão está, embaixo do prompt, embaixo do spinner e numa página com todas as sessões da máquina.

```
claude plugin marketplace add joaosavi/cockpit
claude plugin install cockpit@cockpit
```

-  **Instale o pacote** No terminal, adicione o marketplace e instale o `cockpit`. Ele traz os 11 mods como dependência.  [Ver a instalação passo a passo](https://joaosavi.github.io/cockpit/pt/md/install.md)
-  **Reinicie e rode o setup** Reinicie o Claude Code e digite `/cockpit:setup`. Ele faz quatro perguntas com prévia, grava a status line, a dica do spinner e o momento de compactar, e guarda um backup do arquivo que mudou. [Ver o que o setup pergunta](https://joaosavi.github.io/cockpit/pt/md/install.md)
-  **Trabalhe como sempre** Os guardas ficam quietos até agir. Digite `/panel` para o endereço da página das sessões e `/limit` para ver o limite do plano. [O que muda na primeira sessão](https://joaosavi.github.io/cockpit/pt/md/first-session.md)

## Como fica na tela

```
✻ Propagating… (6s · ↓ 90 tokens)
  ⎿  Now: Running the tests after the fix to the date filter

────────────────────────────────────────────────────────────────
❯ 
────────────────────────────────────────────────────────────────
Opus 5.5   acme-api   feat/billing  ● 1  ? 1     43m  ·  0 calls
ctx ●●○○○○ 38%   5h ●●●●○○ 64% 2h20m   7d ●●●●●○ 81%   mem 2.4G
```

Um turno rodando: a linha do `spinner-status`, o prompt e a status line do `hud` no estilo `refined`. Saída real dos mods.

## Guardas

Barram o erro antes de ele acontecer.

- `secret-guard`: Troca o valor de todo segredo por `<hidden:NOME>` na saída das ferramentas, antes de o agente ler, e devolve o valor real quando o agente edita um `.env`. [Leia mais](https://joaosavi.github.io/cockpit/pt/md/secret-guard.md)
- `collision-guard`: Avisa quando outra sessão da máquina editou o mesmo arquivo, e segura uma vez o comando git que levaria junto a edição não commitada dela. [Leia mais](https://joaosavi.github.io/cockpit/pt/md/collision-guard.md)
- `pipefail`: Põe `set -o pipefail;` num teste, typecheck ou lint passado por `tail`, `head` ou `grep`, para um teste reprovado não sair com código 0. [Leia mais](https://joaosavi.github.io/cockpit/pt/md/pipefail.md)
- `memory-guard` : Antes de typecheck, build, teste e Playwright, confere a folga de memória: roda como veio, com um processo só, espera ou recusa. Repete com um processo o comando morto com exit 137. [Leia mais](https://joaosavi.github.io/cockpit/pt/md/memory-guard.md)
- `loop-breaker`: Manda o agente parar e mudar de abordagem quando ele repete o mesmo erro, a mesma correção ou a mesma chamada. [Leia mais](https://joaosavi.github.io/cockpit/pt/md/loop-breaker.md)
- `usage-limit` : Cuida de cada janela do plano: um subagente por vez, commit do trabalho, pausa com reserva para você e retomada sozinha quando a janela reinicia. [Leia mais](https://joaosavi.github.io/cockpit/pt/md/usage-limit.md)

## Instrumentos

Mostram em que ponto a sessão está.

- `hud` : Modelo, projeto, branch e PR, contexto, limites do plano e memória numa status line embaixo do prompt. Quatro estilos. [Leia mais](https://joaosavi.github.io/cockpit/pt/md/hud.md)
- `spinner-status`: Troca a dica embaixo do spinner por uma linha do Haiku: em que ponto a sessão está, ou uma dica sobre os mods. [Leia mais](https://joaosavi.github.io/cockpit/pt/md/spinner-status.md)
- `panel` : Uma página local com um cartão por sessão da máquina: o estado, o que ela precisa de você, a ferramenta rodando e o próximo passo. [Leia mais](https://joaosavi.github.io/cockpit/pt/md/panel.md)
- `skill-loader`: Entrega a skill certa quando o agente mexe num arquivo ou escreve um commit, e lembra de diagnosticar antes de corrigir quando você cola um erro. [Leia mais](https://joaosavi.github.io/cockpit/pt/md/skill-loader.md)

## Memória

- `global-memory`: Acrescenta uma pasta de memória da máquina ao lado da memória de cada projeto, para o que vale na máquina chegar a toda sessão. [Leia mais](https://joaosavi.github.io/cockpit/pt/md/global-memory.md)

## O que você precisa ter

- Claude Code 2.1.287 ou mais novo, no macOS, no Windows ou no Linux. Os mods usam os function hooks do Claude Code, que estão em acesso antecipado e podem mudar de uma versão para outra.
- Node 22.18 ou mais novo, para o script da status line.
- Python 3.9 ou mais novo e `curl`, para a página do `panel`. O macOS e o Windows 10 em diante já trazem o `curl`.
- Uma [Nerd Font](https://www.nerdfonts.com/) no terminal, para os ícones da status line. Sem ela, escolha os ícones simples no setup.

A status line, a linha do spinner e os painéis fazem parte da interface de terminal do Claude Code. Rode o `claude` num terminal: Terminal ou iTerm no macOS, Windows Terminal ou PowerShell no Windows, ou o terminal do VS Code e do JetBrains. Os mods não foram testados no app Desktop nem no chat das extensões de IDE.

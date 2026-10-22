# O que muda na primeira sessão

Depois do setup e de um reinício, três coisas aparecem na tela. Os guardas não aparecem até agir.

## A status line

O `hud` desenha duas linhas embaixo do prompt: modelo, pasta, branch e as mudanças dela, depois o contexto usado, as janelas de 5 horas e de 7 dias do plano e a folga de memória.

```
Opus 5.5   acme-api   feat/billing  ● 1  ? 1     43m  ·  0 calls
ctx ●●○○○○ 38%   5h ●●●●○○ 64% 2h20m   7d ●●●●●○ 81%   mem 2.4G
```

As barras vão do verde ao vermelho conforme enchem. O `2h20m` depois da porcentagem de 5 horas é o tempo até essa janela reiniciar. Os outros três estilos estão na [página do hud](https://joaosavi.github.io/cockpit/pt/md/hud.md).

## A linha embaixo do spinner

Enquanto um turno roda, o Claude Code mostra uma dica embaixo do spinner. O `spinner-status` troca essa dica por uma linha do Haiku sobre o que o agente está fazendo agora.

```
✻ Propagating… (6s · ↓ 90 tokens)
  ⎿  Now: Running the tests after the fix to the date filter
```

`Now:` é o ponto em que a sessão está. `Mods:` é uma dica sobre os mods instalados.

## A página das sessões

O `panel` sobe uma página local com todas as sessões da máquina. Digite `/panel` para o endereço.

```
❯ /panel
  ⎿  panel: http://localhost:7777
     4 sessions: 1 need you, 2 working.
```

Abra o endereço no navegador. A sessão que espera você vem primeiro, com as opções que ela ofereceu em botões. A [página do panel](https://joaosavi.github.io/cockpit/pt/md/panel.md) mostra as seis vistas.

## Comandos para testar

| Comando | O que mostra |
| --- | --- |
| `/limit` | As janelas do plano, quando cada uma reinicia e o que o mod segura perto do limite. |
| `/hud` | A visão completa: sessão, limites, memória, o que roda agora e as ações dos mods hoje. |
| `/ram` | A folga de memória por grupo, ou da máquina, e o pico medido de cada comando pesado. |

## Quando um guarda age

O agente lê uma nota curta que começa com o nome do mod, como `pipefail:` ou `Loop check`, e costuma contar para você. A última nota também aparece na faixa acima do prompt enquanto o turno roda.

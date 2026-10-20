# Os comandos do Cockpit

Todo comando que o Cockpit acrescenta. Cada um também responde em texto simples, então funciona onde nenhuma janela é desenhada, como no Remote Control.

| Comando | Mod | O que mostra |
| --- | --- | --- |
| `/panel` | [panel](https://joaosavi.github.io/cockpit/pt/md/panel.md) | O endereço da página das sessões e quantas precisam de você. Sobe o servidor se ele não responde. Numa sessão aberta por SSH, imprime também o comando do túnel. |
| `/hud` | [hud](https://joaosavi.github.io/cockpit/pt/md/hud.md) | A visão completa: sessão, limites, memória, o que roda agora e as ações de hoje. |
| `/limit` | [usage-limit](https://joaosavi.github.io/cockpit/pt/md/usage-limit.md) | As janelas do plano com as etapas, o estado e o que está guardado para a retomada. |
| `/ram` | [memory-guard](https://joaosavi.github.io/cockpit/pt/md/memory-guard.md) | A folga de memória por grupo, ou da máquina, e o pico medido de cada comando pesado. |
| `/cockpit:setup` | cockpit | Roda o setup de novo, para mudar o estilo ou qualquer outra resposta. |

## Teclas nas janelas

Numa janela do Cockpit, `r` atualiza e `esc` fecha.

## Teclas na página do panel

`r` gera o resumo de todas as sessões de novo, ou `R` na Inbox, onde `r` vai para o campo de resposta. `esc` fecha o diálogo de envio, depois a gaveta Mods, depois a gaveta do Board. Cada vista tem as próprias teclas, na [página do panel](https://joaosavi.github.io/cockpit/pt/md/panel.md).

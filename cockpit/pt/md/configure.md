# Como mudar as opções e desligar um mod

Cada opção de mod é uma linha no `/config`. O setup cuida das poucas configurações que um plugin não grava sozinho.

## Mudar uma opção

Abra `/config` e role até o mod. A página de cada mod lista as opções, os padrões e o que fazem. A status line pega a mudança em até 5 segundos; os outros mods, depois de reiniciar o Claude Code ou rodar `/reload-plugins`.

## No arquivo de configurações

As mesmas opções ficam em `pluginConfigs` no `~/.claude/settings.json`, com a chave `<mod>@cockpit`. Serve para levar a mesma configuração para outra máquina:

~/.claude/settings.json:

```
{
  "pluginConfigs": {
    "hud@cockpit": { "options": { "style": "blocks", "icons": "unicode" } },
    "usage-limit@cockpit": { "options": { "timeZone": "America/Sao_Paulo" } },
    "collision-guard@cockpit": { "options": { "git": "note" } }
  }
}
```

## O que o setup grava

| Configuração | Valor | Por que |
| --- | --- | --- |
| `statusLine` | o script do `hud`, com `refreshInterval: 5` | Um plugin não desenha embaixo do prompt. |
| `spinnerTipsEnabled` | `false` | A linha do `spinner-status` substitui a dica do Claude Code em vez de ficar embaixo dela. |
| `autoCompactWindow` | `733000` num modelo de 1M, se você escolher | O Claude Code resume a conversa em uns 70% em vez de perto do fim. |
| `pluginConfigs` | `band: "off"` no hud, estilo, ícones, fuso | As suas respostas ao setup. Com a status line ligada, a faixa desliga para as linhas não aparecerem duas vezes. |
| `enabledPlugins` | `claude-hud@claude-hud` desligado, quando estava ligado | A status line dele é a que o hud substitui. |
| `pluginConfigs` | `enabled: false` em cada mod que você desligar, se pedir | Só quando você pede ao setup para desligar mods. |
| `extraKnownMarketplaces.cockpit` | `autoUpdate: true` | Os mods atualizam sozinhos. |

## Desligar um mod

Todo mod tem a opção **Enabled**. Desligue no `/config`, ou ponha `"enabled": false` na entrada do mod em `pluginConfigs`, e abra uma sessão nova ou rode `/reload-plugins`. Desligado, o mod não registra nenhum hook e não custa nada por chamada. O `/cockpit:setup` também desliga mods para você.

~/.claude/settings.json:

```
{
  "pluginConfigs": {
    "loop-breaker@cockpit": { "options": { "enabled": false } },
    "memory-guard@cockpit": { "options": { "refuse": false } }
  }
}
```

## Desligar um passo de um guarda

| Mod | Chaves |
| --- | --- |
| [`secret-guard`](https://joaosavi.github.io/cockpit/pt/md/secret-guard.md) | `fillCommands` |
| [`collision-guard`](https://joaosavi.github.io/cockpit/pt/md/collision-guard.md) | `editWarnings`, e `git: off` para a trava do git |
| [`memory-guard`](https://joaosavi.github.io/cockpit/pt/md/memory-guard.md) | `reduce`, `wait`, `refuse`, `retry137` |
| [`loop-breaker`](https://joaosavi.github.io/cockpit/pt/md/loop-breaker.md) | `editCheck`, `errorCheck`, `repeatCheck` |
| [`usage-limit`](https://joaosavi.github.io/cockpit/pt/md/usage-limit.md) | freio, commit e pausa de cada janela, e `resume` |
| [`skill-loader`](https://joaosavi.github.io/cockpit/pt/md/skill-loader.md) | `holdWrites`, `diagnoseReminder` |
| [`panel`](https://joaosavi.github.io/cockpit/pt/md/panel.md) | `answers`, `autostart` |

A página de cada mod diz o que cada chave desliga.

## Tirar os hooks de um mod

O Claude Code recusa desligar um plugin que outro plugin ligado exige, e o pacote `cockpit` exige todos os mods. Desligue o pacote primeiro e depois o mod:

terminal:

```
claude plugin disable cockpit@cockpit
claude plugin disable pipefail@cockpit
```

Os outros mods continuam ligados. Religar o pacote religa o mod.

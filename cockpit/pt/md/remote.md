# Como usar numa máquina remota

Quem roda o Claude Code numa máquina Linux remota por SSH usa os mods do mesmo jeito, e algumas partes fazem mais.

## Abrir a página por túnel

O `panel` escuta só no `127.0.0.1` da máquina onde as sessões rodam. Do seu computador, abra um túnel SSH e acesse `http://localhost:7777`. Numa sessão aberta por SSH, o `/panel` imprime esse comando com o nome da máquina.

no seu computador:

```
ssh -N -L 7777:127.0.0.1:7777 <host>
```

Para o túnel abrir a cada login SSH, ponha uma linha na entrada da máquina no `~/.ssh/config` do seu computador:

~/.ssh/config:

```
Host <host>
  LocalForward 7777 127.0.0.1:7777
```

## Rodar a página como serviço

Em vez de deixar uma sessão subir a página, rode o servidor no systemd. Ponha a opção `autostart` do `panel` em `false` e rode o servidor como unidade:

unidade do systemd:

```
[Service]
User=<usuario>
ExecStart=/usr/bin/python3 -I /home/<usuario>/.claude/plugins/marketplaces/cockpit/panel/server/panel.py
Environment=PANEL_CLAUDE=/home/<usuario>/.local/bin/claude
Restart=always
```

As variáveis `PANEL_PORT`, `PANEL_MODEL` e `PANEL_REFRESH_MINUTES` definem as opções do servidor. `PANEL_GROUPS` recebe uma lista de cgroups separados por vírgula, como `agents.slice`, para a página mostrar esses grupos e tudo embaixo deles.

## Limites de memória

Com as sessões embaixo de um limite de memória do cgroup v2, como o de um serviço do systemd ou de um container, o `memory-guard` mantém os comandos pesados dentro do limite mais apertado, o `hud` mostra o que sobra embaixo dele, o `/ram` mostra cada grupo e a página mostra a memória de cada grupo e o estado dos serviços.

## Remote Control e tmux

Todo comando do Cockpit responde também em texto, então funciona quando você conduz a sessão pelo [Remote Control](https://code.claude.com/docs/pt/remote-control), no claude.ai ou no app do celular, onde nenhuma janela é desenhada. A página liga a sessão ao claude.ai quando ela roda com Remote Control. Para uma sessão em tmux, o botão **tmux** copia o comando que entra no painel dela.

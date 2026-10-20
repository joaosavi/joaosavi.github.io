# Como instalar e configurar

Dois comandos no terminal, um reinício e um setup de quatro perguntas. Leva uns cinco minutos.

## Instalar

- **Adicione o marketplace e instale o pacote**
terminal:

```
claude plugin marketplace add joaosavi/cockpit
claude plugin install cockpit@cockpit
```
O segundo comando lista os mods que instala, como `+ 11 dependencies`.
- **Reinicie o Claude Code** A sessão nova carrega os mods. Uma sessão que já estava aberta pega com `/reload-plugins`.
- **Rode o setup**
dentro do Claude Code:

```
/cockpit:setup
```
Um plugin não consegue gravar sozinho a status line, a dica do spinner e o momento de compactar, porque esses ficam no seu `settings.json`. O setup faz isso, guarda um backup do arquivo que mudou e diz o que você vai notar.

## O que o setup pergunta

| Pergunta | Opções |
| --- | --- |
| Estilo da status line | `refined` (recomendado), `blocks`, `minimal` ou `compact`, cada um com a prévia desenhada pelo script de verdade, com a sua pasta e a sua branch. |
| Ícones | O setup imprime três ícones da Nerd Font e pergunta se aparecem. Se aparecem caixas, ele usa setas e marcas simples, que todo terminal desenha. |
| Fuso horário | Só quando o sistema está em UTC. Vale para os horários que os mods mostram e para o que conta como hoje. |
| Quando compactar | Mais cedo, em uns 70% de um modelo de 1M (recomendado, `733000`), o padrão do Claude Code perto do fim, ou na metade (`500000`). Pulada em modelo com janela menor que 200K. |

O setup também liga a atualização automática do marketplace, sem perguntar. Rode `/cockpit:setup` de novo quando quiser mudar uma resposta: ele lê o que está gravado e pergunta só o que falta.

## Conferir

terminal:

```
claude plugin list
```

Aparecem 12 entradas terminadas em `@cockpit`, cada uma `enabled`: o pacote e os 11 mods. Uma entrada `failed to load` é versão fora de passo; veja [Algo quebrou?](https://joaosavi.github.io/cockpit/pt/md/troubleshooting.md).

## Atualizações chegam sozinhas

Com a atualização automática ligada, o Claude Code atualiza cada mod que tem versão nova uns minutos depois da primeira mensagem de uma sessão, instala o mod que entrou no pacote e mostra `Plugin updated: <nome> · Run /reload-plugins to apply`. Para desligar, abra `/plugin`, vá em **Marketplaces** e escolha `cockpit`.

## macOS, Windows e Linux

Todos os mods rodam nos três sistemas, e foram testados só no Linux. Duas coisas mudam:

- O `memory-guard` e a memória do `hud` leem os limites de cgroup e o `/proc/meminfo` no Linux. No macOS leem o `vm_stat`, no Windows o PowerShell, e ali comparam com a memória da máquina inteira. As leituras do macOS e do Windows foram testadas só contra saída simulada.
- A página do `panel` mostra memória por cgroup, serviços do systemd e a fatia de CPU esperando disco só no Linux.

No Windows, o setup aponta a status line para o Node em vez do script `.sh`, porque o PowerShell não roda shell script.

## No plano Team ou Enterprise

Todo mod funciona igual em qualquer plano, menos o `global-memory`. O Team e o Enterprise rodam um guarda embutido que ignora plugin instalado pelo usuário nos dois hooks de que ele precisa, então ele instala e não faz nada até a sua organização listá-lo nas managed settings. Os outros mods rodam normalmente. A [página do global-memory](https://joaosavi.github.io/cockpit/pt/md/global-memory.md) mostra as duas configurações.

>  **Vindo do marketplace agent** O Cockpit se chamava `agent` até outubro de 2026. Troque toda chave `@agent` por `@cockpit` no `~/.claude/settings.json` e rode `claude plugin marketplace remove agent` antes dos passos acima. Remover um marketplace apaga as opções salvas dos plugins dele, então troque as chaves antes, ou rode `/cockpit:setup` de novo depois.

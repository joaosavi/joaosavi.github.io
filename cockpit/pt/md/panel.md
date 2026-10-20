# `panel`

Uma página local com todas as sessões do Claude Code no seu computador: se ela espera você, o que precisa, o que está fazendo agora e o que terminou. O resumo de cada sessão vem do `claude -p`, refeito a cada poucos minutos e quando você pede.

![A página do panel na vista Inbox: a máquina no topo, as sessões por urgência à esquerda e a sessão escolhida à direita](https://joaosavi.github.io/cockpit/img/panel-dark.png)

A página com sessões inventadas, na vista Inbox.

## Abrir a página

Digite `/panel` em qualquer sessão para o endereço, `http://localhost:7777` por padrão, e abra no navegador. O servidor sobe com a primeira sessão depois da instalação e continua rodando depois que ela termina. A página escuta só no `127.0.0.1`, então só o seu computador chega nela. Com as sessões em outra máquina, veja [Como usar numa máquina remota](https://joaosavi.github.io/cockpit/pt/md/remote.md).

## O que a página mostra

- O topo mostra o computador numa linha: o uso de 5 horas e semanal do plano com o tempo até cada reinício, memória, CPU do último minuto, disco e os tokens das sessões nas últimas 24 horas, hora a hora. Um número fica âmbar em 75% e vermelho em 90%. À direita ficam **Notify**, **Refresh all** e **Mods**.
- Cada sessão mostra o estado (`Working`, `Waiting for you`, `Blocked`, `Done`, `Idle`), um título, o projeto, a branch com arquivos mudados e commits à frente ou atrás, o modelo, a sua última mensagem, a ferramenta rodando agora, o resumo da tarefa, o próximo passo e o que terminou. Fecham o cartão o contexto usado até o ponto de compactar, os tokens das últimas 24 horas, a memória dos processos e há quanto tempo roda.
- A gaveta **Mods** mostra o computador completo, as últimas ações dos guardas, o que cada guarda fez hoje e quantos resumos a página fez hoje, com tokens e preço de API. No Linux mostra também a memória de cada cgroup com limite e o estado dos serviços do systemd.

## As cinco vistas

O seletor embaixo do topo escolhe a vista, e a página lembra. O endereço também aceita a vista no hash, como `#board`, e `#mods` abre a gaveta.

| Vista | O que mostra | Teclas |
| --- | --- | --- |
| **Inbox** | O padrão. As sessões por urgência à esquerda e a escolhida inteira à direita. | `j` e `k` ou setas movem, `1` a `4` escolhem opção, `r` vai para a resposta |
| **Board** | Colunas por estado, com cartões pequenos. Um cartão abre a sessão numa gaveta lateral. | `1` a `4` na gaveta, `esc` fecha |
| **Deck** | Uma grade de cartões completos, com filtros: todas, as que precisam de você, rodando, terminadas e encerradas. |  |
| **Focus** | Um cartão grande para a sessão que mais precisa de você, e as outras embaixo. | `n` e `p` ou setas movem |
| **Timeline** | Uma linha por sessão com os tokens hora a hora nas últimas 24 horas, e uma linha com todas juntas. |  |

**Working** vem do próprio Claude Code assim que um turno começa. **Waiting for you**, **Blocked**, **Done** e **Idle** vêm do resumo, que o `claude -p` escreve a partir da conversa: 20 segundos depois de um turno terminar, a cada 5 minutos para sessão que mudou, e quando você aperta **Refresh**.

## Responder uma sessão pela página

Quando uma sessão espera uma decisão, as opções dela viram botões. Aperte uma, ou o número dela, confira o texto e confirme. O campo de resposta manda qualquer texto do mesmo jeito. A página deixa o texto na caixa de entrada da sessão, o mod `panel` daquela sessão confere a caixa a cada 2 segundos e envia o texto como prompt seu, e o Claude Code roda quando a sessão fica parada. Funciona no macOS, no Windows e no Linux, no terminal, no app Desktop, numa IDE ou pelo Remote Control, com ou sem tmux.

>  **Opções em cinza** A sessão só aceita resposta quando o mod dela conferiu a caixa nos últimos 15 segundos. Até lá, as opções ficam em cinza e o campo de resposta some. Uma sessão com mod `panel` antigo fica assim até você rodar `/reload-plugins` nela. Se a sessão não pega a mensagem em 6 segundos, a página retira e avisa.

## Auditar os mods

A metade de baixo da gaveta **Mods** audita os mods pelos diários do último dia, 7 dias ou 30 dias. Cada linha mostra a versão, se está ligado, em quantas sessões rodou, o que fez, as falhas em vermelho, o tempo que os hooks somaram por chamada, a chamada mais lenta, o custo de API das chamadas a modelo e a última ação. Um mod sem nada gravado numa semana não trabalha na sua máquina.

![A gaveta Mods: o computador, os guardas e uma linha por mod com ações, falhas e tempo por chamada](https://joaosavi.github.io/cockpit/img/panel-mods.png)

## Opções

| Opção | Padrão | O que faz |
| --- | --- | --- |
| `enabled` | `true` | Desligado, o mod não faz nada: sem `/panel`, sem subir servidor, sem respostas; um servidor que já roda continua. Vale na próxima sessão, ou depois de `/reload-plugins`. |
| `port` | `7777` | A porta da página, no `127.0.0.1`. |
| `model` | `sonnet` | O modelo do `claude -p` em cada resumo: `sonnet`, `haiku` ou `opus`. |
| `refreshMinutes` | `5` | Uma sessão cuja conversa mudou ganha resumo novo nesse intervalo. |
| `autostart` | `true` | Sobe o servidor quando uma sessão começa e a porta não responde. Desligue quando um gerenciador de serviços roda o servidor. |
| `answers` | `true` | Deixa a página mandar texto para esta sessão como prompt seu. Desligado, a página mostra as opções da sessão em cinza e sem campo de resposta. |

## Subir o servidor à mão

A página precisa do Python 3.9 ou mais novo, como `python3`, `python` ou `py`, e do `curl`. Com `autostart` ligado, a primeira sessão sobe o servidor, e ele continua depois que ela termina. Para subir você mesmo, rode o arquivo do servidor na pasta do plugin, que é o `installPath` de `panel@cockpit` em `~/.claude/plugins/installed_plugins.json`:

terminal:

```
python3 -I <pasta do plugin>/server/panel.py
```

No Windows, use `python` ou `py` no lugar de `python3`. Ponha em `PANEL_CLAUDE` o caminho do `claude` quando ele não está no `PATH`.

## Como o resumo é feito

O servidor monta um digest da conversa de no máximo 48.000 caracteres: a mensagem que abriu a tarefa e as linhas mais novas que couberem, cada chamada de ferramenta cortada em uma linha. Manda para `claude -p --safe-mode --tools "" --no-session-persistence` com um schema JSON. A chamada não carrega hooks, plugins nem ferramentas, não guarda conversa própria e responde num formato fixo, na língua em que você escreve.

## Custo

Cada resumo é uma chamada `claude -p` e conta no limite do plano. Na máquina Linux do autor, em outubro de 2026, o resumo de uma sessão longa leu uns 48.000 tokens e levou de 6 a 10 segundos, com pico de 213 MB no servidor. No preço de API com `sonnet`, um resumo custou uns US$ 0,07, e com quatro sessões trabalhando a página gastou até US$ 2,40 por hora. No plano Pro ou Max, isso sai do uso do plano, não em dinheiro. O `haiku` custa umas 20 vezes menos por token, com resumo mais curto e menos exato.

## O que grava

- `~/.local/state/mods/panel/summaries/<sessão>.json`: o último resumo de cada sessão, com a hora e o tamanho da conversa que leu.
- `~/.local/state/mods/panel/<dia>-server.jsonl`: uma linha por resumo com o motivo, o tempo, o estado e os tokens, uma por falha e uma por resposta enviada com o tamanho. Nunca grava o conteúdo da sessão nem o que você mandou.

## Limites

- As sessões precisam rodar na mesma máquina e com o mesmo usuário do servidor.
- A página não tem login. Quem conecta na porta daquela máquina lê a página, pede resumo e digita nas sessões, então mantenha no `127.0.0.1`. O servidor recusa pedido vindo de página de outro site.
- Uma resposta enviada pela página espera a sessão parar. Durante um turno ela não chega ao agente e roda como turno novo depois.
- O estado vem do modelo e pode atrasar em relação à sessão. Sessão ocupada sempre aparece como `Working`.
- No macOS e no Windows não há grupos de memória, serviços nem espera de disco. Testado no Linux; os caminhos do macOS e do Windows rodam só em teste simulado.

## Instalar só este mod

O pacote `cockpit` já instala o `panel` com os outros. Para ter só ele:

terminal:

```
claude plugin marketplace add joaosavi/cockpit
claude plugin install panel@cockpit
```

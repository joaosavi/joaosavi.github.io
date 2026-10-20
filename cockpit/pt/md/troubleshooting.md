# Algo quebrou? A solução está aqui

Os problemas mais comuns e a solução de cada um.

| Sintoma | Solução |
| --- | --- |
| A status line não aparece, ou só muda quando chega mensagem | Falta o `statusLine` nas configurações, ou falta o `refreshInterval`. Rode `/cockpit:setup` de novo e reinicie o Claude Code. |
| A status line não mostra nada | O script precisa do Node 22.18 ou mais novo. Rode `node --version` e atualize o Node se for mais velho. |
| Os ícones aparecem como caixas ou interrogações | A fonte do terminal não tem os glifos da Nerd Font. Ponha `icons` em `unicode` no `hud` pelo `/config`, ou instale uma Nerd Font e escolha ela no terminal. |
| As barras parecem um borrão só | Algumas fontes desenham os glifos da barra colados. Ponha `bar` em `dots` ou `squares` no `hud`. |
| Aparecem duas linhas embaixo do spinner | A dica do Claude Code continua ligada. Ponha `"spinnerTipsEnabled": false` nas configurações, ou rode o setup de novo. |
| Um mod aparece como `failed to load` no `claude plugin list` | A cópia do marketplace e a versão instalada estão fora de passo. Rode `claude plugin marketplace update cockpit`, depois `claude plugin update cockpit@cockpit`, e reinicie. |
| As opções dos mods sumiram | Remover um marketplace apaga as opções salvas dos plugins dele. Rode `/cockpit:setup` de novo para gravar. |
| O `global-memory` não faz nada no plano Team ou Enterprise | Esses planos ignoram plugin instalado pelo usuário nos hooks de que ele precisa. Ele tem de entrar como plugin da organização; a [página dele](https://joaosavi.github.io/cockpit/pt/md/global-memory.md) mostra as managed settings. |
| O `/panel` diz que o servidor não está rodando | O servidor sobe quando uma sessão começa, a não ser que `autostart` esteja desligado. Confira que o Python 3.9 ou mais novo está instalado como `python3`, `python` ou `py` e que o `curl` roda, e abra uma sessão nova. Os erros do servidor ficam em `~/.local/state/mods/panel/server.log`. |
| A página deixa as opções de uma sessão em cinza | A sessão não conferiu a caixa de entrada nos últimos 15 segundos, quase sempre porque carregou um mod `panel` antigo. Rode `/reload-plugins` nela. |
| A gaveta Mods não mostra memória por grupo nem serviços | É o esperado no macOS e no Windows. A página só mostra memória por grupo para cgroup v2 com limite, e serviço só com systemd. |
| O `/ram` diz que não há leitura de memória | O `memory-guard` não achou o `/proc/meminfo` e o comando do sistema falhou: `sysctl` e `vm_stat` no macOS, PowerShell no Windows, ausente ou mais lento que o limite de tempo. Até uma leitura funcionar, os comandos pesados rodam como vieram. |
| Um comando git foi recusado com uma lista de arquivos | O `collision-guard` segurou, porque outra sessão da máquina tem edição não commitada no mesmo repo, embaixo dos caminhos que o comando nomeia. Nomeie só os seus arquivos, ou rode o mesmo comando de novo em até 2 minutos. |

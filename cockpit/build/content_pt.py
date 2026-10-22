"""As páginas em português da documentação do Cockpit. O texto segue os READMEs do repo joaosavi/cockpit."""
import lib
from lib import *

TITLE = 'Cockpit para Claude Code'
DESCRIPTION = 'Os 12 mods do Cockpit para o Claude Code: guardas que barram os erros de um agente e instrumentos que mostram em que ponto cada sessão está.'
LLMS_INTRO = 'Cada página abaixo é um arquivo Markdown. Para instalar: `claude plugin marketplace add joaosavi/cockpit` e `claude plugin install cockpit@cockpit`, depois reinicie o Claude Code e rode `/cockpit:setup`.'
FULL_LABEL = 'Todas as páginas num arquivo só'
OTHER_LABEL = 'English version'
GROUPS = [('Começar', 'zap', False), ('Guardas', 'shield', True), ('Instrumentos', 'gauge', True), ('Memória', 'db', False), ('Consultar', 'search', True)]
MOD_GROUPS = ('Guardas', 'Instrumentos', 'Memória')

P = []  # (grupo, id, ícone, rótulo da lateral, título, html)

def page(group, pid, icon, label, title, body):
    P.append((group, pid, icon, label, title, body))

MODS = [
    ('Guardas', [
        ('secret-guard', 'lock', 'Troca o valor de todo segredo por <code>&lt;hidden:NOME&gt;</code> na saída das ferramentas, antes de o agente ler, e devolve o valor real quando o agente edita um <code>.env</code>.', None),
        ('collision-guard', 'branch', 'Avisa quando outra sessão da máquina editou o mesmo arquivo, e segura uma vez o comando git que levaria junto a edição não commitada dela.', None),
        ('pipefail', 'funnel', 'Põe <code>set -o pipefail;</code> num teste, typecheck ou lint passado por <code>tail</code>, <code>head</code> ou <code>grep</code>, para um teste reprovado não sair com código 0.', None),
        ('memory-guard', 'mem', 'Antes de typecheck, build, teste e Playwright, confere a folga de memória: roda como veio, com um processo só, espera ou recusa. Repete com um processo o comando morto com exit 137.', '/ram'),
        ('loop-breaker', 'loop', 'Manda o agente parar e mudar de abordagem quando ele repete o mesmo erro, a mesma correção ou a mesma chamada.', None),
        ('usage-limit', 'gauge', 'Cuida de cada janela do plano: um subagente por vez, commit do trabalho, pausa com reserva para você e retomada sozinha quando a janela reinicia.', '/limit'),
    ]),
    ('Instrumentos', [
        ('hud', 'hud', 'Modelo, projeto, branch e PR, contexto, limites do plano e memória numa status line embaixo do prompt. Quatro estilos.', '/hud'),
        ('spinner-status', 'spinner', 'Troca a dica embaixo do spinner por uma linha do Haiku: em que ponto a sessão está, ou uma dica sobre os mods.', None),
        ('panel', 'grid', 'Uma página local com um cartão por sessão da máquina: o estado, o que ela precisa de você, a ferramenta rodando e o próximo passo.', '/panel'),
        ('skill-loader', 'book', 'Entrega a skill certa quando o agente mexe num arquivo ou escreve um commit, e lembra de diagnosticar antes de corrigir quando você cola um erro.', None),
    ]),
    ('Memória', [
        ('global-memory', 'globe', 'Acrescenta uma pasta de memória da máquina ao lado da memória de cada projeto, para o que vale na máquina chegar a toda sessão.', None),
        ('todo', 'tag', 'Mostra as tarefas abertas da lista nativa no início da sessão e em cada prompt seu, e arquiva a tarefa concluída.', None),
    ]),
]
def modgrid(group):
    return lib.modgrid(dict(MODS)[group])


# Quickstart
page('Começar', 'start', 'rocket', 'Início rápido', 'Início rápido', f'''
<p class="lead">O Cockpit é um pacote de 12 mods para o <a href="https://claude.com/product/claude-code" target="_blank" rel="noopener">Claude Code</a>. Os guardas barram o erro de um agente antes de ele custar caro: um segredo na saída de uma ferramenta, um pipe que esconde um teste reprovado, um build morto por falta de memória, um commit que leva junto a edição de outra sessão. Os instrumentos mostram em que ponto a sessão está, embaixo do prompt, embaixo do spinner e numa página com todas as sessões da máquina.</p>
<pre id="install-text" hidden>{INSTALL}</pre>
<ol class="quick">
  <li><span class="q-n">1</span><div><b>Instale o pacote</b><p>No terminal, adicione o marketplace e instale o <code>cockpit</code>. Ele traz os 12 mods como dependência.</p><button type="button" class="q-copy" data-copy-target="install-text">Copiar os comandos</button> <a class="q-go" href="#install">Ver a instalação passo a passo</a></div></li>
  <li><span class="q-n">2</span><div><b>Reinicie e rode o setup</b><p>Reinicie o Claude Code e digite <code>/cockpit:setup</code>. Ele faz quatro perguntas com prévia, grava a status line, a dica do spinner e o momento de compactar, e guarda um backup do arquivo que mudou.</p><a class="q-go" href="#install">Ver o que o setup pergunta</a></div></li>
  <li><span class="q-n">3</span><div><b>Trabalhe como sempre</b><p>Os guardas ficam quietos até agir. Digite <code>/panel</code> para o endereço da página das sessões e <code>/limit</code> para ver o limite do plano.</p><a class="q-go" href="#first-session">O que muda na primeira sessão</a></div></li>
</ol>

<h2>Como fica na tela</h2>
{term(SPINNER + chr(10) + chr(10) + PROMPT + chr(10) + statusline('refined'))}
<p class="figcap">Um turno rodando: a linha do <code>spinner-status</code>, o prompt e a status line do <code>hud</code> no estilo <code>refined</code>. Saída real dos mods.</p>

<h2>Guardas</h2>
<p>Barram o erro antes de ele acontecer.</p>
{modgrid('Guardas')}
<h2>Instrumentos</h2>
<p>Mostram em que ponto a sessão está.</p>
{modgrid('Instrumentos')}
<h2>Memória</h2>
{modgrid('Memória')}

<h2>O que você precisa ter</h2>
<ul>
  <li>Claude Code 2.1.287 ou mais novo, no macOS, no Windows ou no Linux. Os mods usam os function hooks do Claude Code, que estão em acesso antecipado e podem mudar de uma versão para outra.</li>
  <li>Node 22.18 ou mais novo, para o script da status line.</li>
  <li>Python 3.9 ou mais novo e <code>curl</code>, para a página do <code>panel</code>. O macOS e o Windows 10 em diante já trazem o <code>curl</code>.</li>
  <li>Uma <a href="https://www.nerdfonts.com/" target="_blank" rel="noopener">Nerd Font</a> no terminal, para os ícones da status line. Sem ela, escolha os ícones simples no setup.</li>
</ul>
<p>A status line, a linha do spinner e os painéis fazem parte da interface de terminal do Claude Code. Rode o <code>claude</code> num terminal: Terminal ou iTerm no macOS, Windows Terminal ou PowerShell no Windows, ou o terminal do VS Code e do JetBrains. Os mods não foram testados no app Desktop nem no chat das extensões de IDE.</p>
''')

page('Começar', 'install', 'download', 'Como instalar e configurar', 'Como instalar e configurar', f'''
<p class="lead">Dois comandos no terminal, um reinício e um setup de quatro perguntas. Leva uns cinco minutos.</p>
<h2>Instalar</h2>
<ol class="steps">
  <li><b>Adicione o marketplace e instale o pacote</b>{code(INSTALL)}<p>O segundo comando lista os mods que instala, como <code>+ 12 dependencies</code>.</p></li>
  <li><b>Reinicie o Claude Code</b><p>A sessão nova carrega os mods. Uma sessão que já estava aberta pega com <code>/reload-plugins</code>.</p></li>
  <li><b>Rode o setup</b>{code('/cockpit:setup', 'dentro do Claude Code')}<p>Um plugin não consegue gravar sozinho a status line, a dica do spinner e o momento de compactar, porque esses ficam no seu <code>settings.json</code>. O setup faz isso, guarda um backup do arquivo que mudou e diz o que você vai notar.</p></li>
</ol>

<h2>O que o setup pergunta</h2>
{table(['Pergunta', 'Opções'], [
    ('Estilo da status line', '<code>refined</code> (recomendado), <code>blocks</code>, <code>minimal</code> ou <code>compact</code>, cada um com a prévia desenhada pelo script de verdade, com a sua pasta e a sua branch.'),
    ('Ícones', 'O setup imprime três ícones da Nerd Font e pergunta se aparecem. Se aparecem caixas, ele usa setas e marcas simples, que todo terminal desenha.'),
    ('Fuso horário', 'Só quando o sistema está em UTC. Vale para os horários que os mods mostram e para o que conta como hoje.'),
    ('Quando compactar', 'Mais cedo, em uns 70% de um modelo de 1M (recomendado, <code>733000</code>), o padrão do Claude Code perto do fim, ou na metade (<code>500000</code>). Pulada em modelo com janela menor que 200K.'),
])}
<p>O setup também liga a atualização automática do marketplace, sem perguntar. Rode <code>/cockpit:setup</code> de novo quando quiser mudar uma resposta: ele lê o que está gravado e pergunta só o que falta.</p>

<h2>Conferir</h2>
{code('claude plugin list')}
<p>Aparecem 13 entradas terminadas em <code>@cockpit</code>, cada uma <code>enabled</code>: o pacote e os 12 mods. Uma entrada <code>failed to load</code> é versão fora de passo; veja <a href="#troubleshooting">Algo quebrou?</a>.</p>

<h2>Atualizações chegam sozinhas</h2>
<p>Com a atualização automática ligada, o Claude Code atualiza cada mod que tem versão nova uns minutos depois da primeira mensagem de uma sessão, instala o mod que entrou no pacote e mostra <code>Plugin updated: &lt;nome&gt; · Run /reload-plugins to apply</code>. Para desligar, abra <code>/plugin</code>, vá em <b>Marketplaces</b> e escolha <code>cockpit</code>.</p>

<h2>macOS, Windows e Linux</h2>
<p>Todos os mods rodam nos três sistemas, e foram testados só no Linux. Duas coisas mudam:</p>
<ul>
  <li>O <code>memory-guard</code> e a memória do <code>hud</code> leem os limites de cgroup e o <code>/proc/meminfo</code> no Linux. No macOS leem o <code>vm_stat</code>, no Windows o PowerShell, e ali comparam com a memória da máquina inteira. As leituras do macOS e do Windows foram testadas só contra saída simulada.</li>
  <li>A página do <code>panel</code> mostra memória por cgroup, serviços do systemd e a fatia de CPU esperando disco só no Linux.</li>
</ul>
<p>No Windows, o setup aponta a status line para o Node em vez do script <code>.sh</code>, porque o PowerShell não roda shell script.</p>

<h2>No plano Team ou Enterprise</h2>
<p>Todo mod funciona igual em qualquer plano, menos o <code>global-memory</code>. O Team e o Enterprise rodam um guarda embutido que ignora plugin instalado pelo usuário nos dois hooks de que ele precisa, então ele instala e não faz nada até a sua organização listá-lo nas managed settings. Os outros mods rodam normalmente. A <a href="#global-memory">página do global-memory</a> mostra as duas configurações.</p>
{callout('note', 'Vindo do marketplace agent', '<p>O Cockpit se chamava <code>agent</code> até outubro de 2026. Troque toda chave <code>@agent</code> por <code>@cockpit</code> no <code>~/.claude/settings.json</code> e rode <code>claude plugin marketplace remove agent</code> antes dos passos acima. Remover um marketplace apaga as opções salvas dos plugins dele, então troque as chaves antes, ou rode <code>/cockpit:setup</code> de novo depois.</p>')}
''')

page('Começar', 'first-session', 'firstrun', 'O que muda na primeira sessão', 'O que muda na primeira sessão', f'''
<p class="lead">Depois do setup e de um reinício, três coisas aparecem na tela. Os guardas não aparecem até agir.</p>
<h2>A status line</h2>
<p>O <code>hud</code> desenha duas linhas embaixo do prompt: modelo, pasta, branch e as mudanças dela, depois o contexto usado, as janelas de 5 horas e de 7 dias do plano e a folga de memória.</p>
{term(statusline('refined'), 'status line · refined')}
<p>As barras vão do verde ao vermelho conforme enchem. O <code>2h20m</code> depois da porcentagem de 5 horas é o tempo até essa janela reiniciar. Os outros três estilos estão na <a href="#hud">página do hud</a>.</p>
<h2>A linha embaixo do spinner</h2>
<p>Enquanto um turno roda, o Claude Code mostra uma dica embaixo do spinner. O <code>spinner-status</code> troca essa dica por uma linha do Haiku sobre o que o agente está fazendo agora.</p>
{term(SPINNER)}
<p><code>Now:</code> é o ponto em que a sessão está. <code>Mods:</code> é uma dica sobre os mods instalados.</p>
<h2>A página das sessões</h2>
<p>O <code>panel</code> sobe uma página local com todas as sessões da máquina. Digite <code>/panel</code> para o endereço.</p>
{term(PANEL_OUT)}
<p>Abra o endereço no navegador. A sessão que espera você vem primeiro, com as opções que ela ofereceu em botões. A <a href="#panel">página do panel</a> mostra as cinco vistas.</p>
<h2>Comandos para testar</h2>
{table(['Comando', 'O que mostra'], [
    ('<code>/limit</code>', 'As janelas do plano, quando cada uma reinicia e o que o mod segura perto do limite.'),
    ('<code>/hud</code>', 'A visão completa: sessão, limites, memória, o que roda agora e as ações dos mods hoje.'),
    ('<code>/ram</code>', 'A folga de memória por grupo, ou da máquina, e o pico medido de cada comando pesado.'),
])}
<h2>Quando um guarda age</h2>
<p>O agente lê uma nota curta que começa com o nome do mod, como <code>pipefail:</code> ou <code>Loop check</code>, e costuma contar para você. A última nota também aparece na faixa acima do prompt enquanto o turno roda.</p>
''')

# --- guardas ---
page('Guardas', 'secret-guard', 'lock', '<code>secret-guard</code>', 'secret-guard', f'''
{meta(VERS['secret-guard'])}
<p class="lead">Esconde o valor de todo segredo na saída das ferramentas antes de o agente ler.</p>
<h2>Por que</h2>
<p>Um segredo que chega à conversa vai para o modelo e fica no log da sessão, e a partir daí precisa ser trocado. A saída de ferramenta vaza segredo fácil: <code>env</code>, <code>cat .env</code>, um stack trace com string de conexão. O mod troca cada valor por <code>&lt;hidden:NOME&gt;</code> em todo resultado de ferramenta, nativa, de MCP ou de subagente.</p>
<h2>O que faz</h2>
<ul>
  <li>Os valores vêm do arquivo de segredos e de todo arquivo na pasta ao lado com o mesmo nome mais <code>.d</code> (<code>~/.secrets.d/</code> por padrão), de todo <code>.env*</code> embaixo da raiz de <code>.env</code> (5 níveis), quando você define uma, de variável de ambiente com nome de segredo (<code>TOKEN</code>, <code>SECRET</code>, <code>PASSWORD</code>, <code>KEY</code>, <code>AUTH</code> e outros) e da senha de toda URL <code>esquema://usuario:senha@</code>.</li>
  <li>Formatos conhecidos ficam escondidos mesmo fora de qualquer lista: GitHub, Anthropic, OpenAI, AWS, Google, Stripe, Slack, JWT e bloco de chave privada. Aparecem como <code>&lt;hidden:github&gt;</code>, <code>&lt;hidden:jwt&gt;</code> e assim por diante.</li>
  <li>Uma ferramenta que entrega segredo, como a CLI de um cofre de senhas, pode manter a própria lista <code>NOME="valor"</code> num arquivo da pasta de segredos sem mexer no seu arquivo. Arquivo com nome começando por ponto é ignorado, para a ferramenta gravar um temporário e renomear.</li>
  <li>Um valor que também aparece num arquivo <code>.example</code> já é público e continua visível.</li>
  <li>Quando o agente escreve <code>&lt;hidden:NOME&gt;</code> num <code>.env</code> ou no arquivo de segredos, o mod grava o valor real no lugar. O agente edita esses arquivos sem nunca ver um valor.</li>
  <li>Quando o agente escreve <code>&lt;hidden:NOME&gt;</code> num comando Bash, o mod roda o comando com o valor real, e a saída volta escondida. A conversa guarda o comando como foi escrito. O agente chama uma API com um token que nunca viu.</li>
  <li>Um marcador que o mod não consegue preencher barra o comando: um token conhecido só pelo formato, ou um nome com dois valores diferentes nos seus arquivos, como o mesmo <code>DATABASE_URL</code> em dois projetos. O agente recebe a instrução de ler o valor dentro do comando, da variável ou do <code>.env</code>.</li>
  <li>Se o próprio mod falha, ele retém a saída em vez de deixar passar sem conferir.</li>
</ul>
<h2>Opções</h2>
{opts([
    ('enabled', '<code>true</code>', 'Desligado, o mod não faz nada: todo valor aparece na saída como é. Vale na próxima sessão, ou depois de <code>/reload-plugins</code>.'),
    ('secretsFile', '<code>~/.secrets</code>', 'Arquivo <code>CHAVE=valor</code> em que todo valor é segredo, qualquer que seja o nome.'),
    ('envRoot', 'vazio', 'Pasta onde procurar arquivos <code>.env</code>, 5 níveis abaixo. Vazio não procura nenhum.'),
    ('minLength', '<code>12</code>', 'Valor mais curto fica de fora, menos formato conhecido e valor dos arquivos de segredos.'),
    ('fillCommands', '<code>true</code>', 'Roda o comando Bash que nomeia <code>&lt;hidden:NAME&gt;</code> com o valor real. Desligado, esse comando não roda, e o agente recebe a instrução de ler o valor dentro do comando.'),
])}
<p>Por padrão o mod não lê nenhum <code>.env</code>. Para cobrir os <code>.env</code> dos seus projetos, aponte <code>envRoot</code> para a pasta dos repos, como <code>~/code</code>. O mod varre a pasta ao começar, procura <code>.env</code> novo no máximo uma vez por minuto e refaz a lista pelo menos a cada 10 minutos.</p>
{diary('secret-guard', 'uma linha a cada lista refeita (com o tempo que levou), resultado escondido, marcador devolvido ou preenchido num comando e comando barrado, só com nome de segredo e contagem, mais uma linha <code>session-summary</code>. Os valores vivem só na memória do mod, nunca em disco.')}
<h2>Custo</h2>
<p>O hook somou uns 64 ms por chamada de ferramenta na máquina Linux do autor (60 chamadas medidas em outubro de 2026, estimativa), com <code>envRoot</code> numa pasta de uns 140 subdiretórios. A maior parte é conferir se um arquivo de origem mudou.</p>
<h2>Limites</h2>
<ul>
  <li>Um segredo mais curto que <code>minLength</code> e fora de formato conhecido fica visível. Valor do arquivo de segredos ou da pasta dele é escondido a partir de 6 caracteres, porque um cofre entrega senha de 8 a 11; abaixo de 6 é PIN ou palavra, e esconder embaralharia saída comum.</li>
  <li>Um segredo que o agente viu antes de o mod carregar continua na conversa.</li>
  <li>Um <code>.env</code> fora do <code>envRoot</code> não é lido, e os valores dele ficam visíveis se nenhuma outra fonte tiver.</li>
  <li>Preencher um marcador num comando deixa o agente usar o segredo, inclusive mandar para um servidor. Ele não faz mais do que já faria com <code>source .env</code>, mas o comando roda sem pedir permissão própria.</li>
  <li>Os marcadores só são preenchidos em comando Bash. No Windows sem Git Bash, um comando PowerShell com marcador roda como foi escrito. A saída de toda ferramenta continua escondida.</li>
  <li>Testado só no Linux. Os caminhos do macOS e do Windows têm teste unitário com ambiente simulado.</li>
</ul>
{install_one('secret-guard')}
''')

page('Guardas', 'collision-guard', 'branch', '<code>collision-guard</code>', 'collision-guard', f'''
{meta(VERS['collision-guard'])}
<p class="lead">Avisa quando duas sessões da mesma máquina mexem nos mesmos arquivos, e segura uma vez o comando git que levaria junto a edição não commitada da outra sessão.</p>
<h2>Por que</h2>
<p>Rodar várias sessões ao mesmo tempo é comum, e duas delas caem no mesmo repo com frequência. Na máquina Linux do autor, 11 pares de sessões editaram o mesmo repo com menos de 30 minutos de diferença em 8 dias, e 5 desses pares editaram o mesmo arquivo. O Edit do Claude Code já recusa um arquivo que mudou depois da leitura, então uma sessão não sobrescreve a outra em silêncio. O que ele não pega é o git: <code>git add -A</code> ou <code>git commit -a</code> numa sessão leva a edição pela metade da outra, e <code>git stash</code>, <code>checkout</code> ou <code>reset --hard</code> move ou descarta essa edição.</p>
<h2>O que faz</h2>
<ul>
  <li>Cada sessão mantém um registro em <code>~/.local/state/mods/collision-guard/sessions/&lt;sessão&gt;.json</code> com os arquivos que editou. Só ela escreve nele.</li>
  <li>Depois de uma edição, quando outra sessão viva também editou o arquivo e o git ainda mostra a mudança dela, o agente lê uma nota com o nome da sessão e há quanto tempo, e você vê um aviso. Fora de repo git, a outra edição vale por <code>windowMinutes</code>. Cada edição da outra sessão avisa uma vez.</li>
  <li>Antes de um comando git que faria stage, commit, stash, troca de branch ou descarte da edição não commitada de outra sessão, o mod segura o comando e lista os arquivos. O agente pode nomear só os arquivos dele, ou rodar o mesmo comando de novo em até 2 minutos para passar.</li>
  <li>Lê o <code>cd</code> do começo da linha e o <code>git -C &lt;pasta&gt;</code> para achar o repo. Texto entre aspas, como a mensagem de commit, não conta como comando.</li>
  <li>Um comando que nomeia caminhos, como <code>git add -A mods/</code> ou <code>git checkout -- src/a.ts</code>, só é segurado pelas edições da outra sessão embaixo desses caminhos. Curinga ou <code>:/</code> conta como o repo inteiro.</li>
  <li>Sessão encerrada marca o registro, e registro mais velho que <code>expireHours</code> sai quando uma sessão começa.</li>
</ul>
<h2>Opções</h2>
{opts([
    ('enabled', '<code>true</code>', 'Desligado, o mod não faz nada: nada é registrado, nada avisa, nenhum git é segurado. Vale na próxima sessão, ou depois de <code>/reload-plugins</code>.'),
    ('git', '<code>confirm</code>', '<code>confirm</code> segura uma vez o comando git arriscado. <code>note</code> deixa rodar e avisa o agente depois. <code>off</code> não mexe em comando git.'),
    ('windowMinutes', '<code>30</code>', 'Por quanto tempo a edição de outra sessão num arquivo fora de repo git ainda conta. Dentro de um repo, conta enquanto o git mostrar o arquivo como mudado.'),
    ('expireHours', '<code>24</code>', 'Sessão calada por esse tempo conta como encerrada, e o registro dela sai.'),
    ('editWarnings', '<code>true</code>', 'Avisa o agente, com um aviso na tela, quando outra sessão editou o mesmo arquivo. Desligado, as edições continuam registradas, então as outras sessões e a trava do git ainda as veem.'),
])}
{diary('collision-guard', 'uma linha por aviso (<code>edit-warned</code>, <code>git-held</code>, <code>git-confirmed</code>, <code>git-noted</code>) com a operação git e quantos arquivos, nunca o conteúdo, mais uma linha <code>session-summary</code>.')}
<h2>Custo</h2>
<p>Chamada que não é edição nem git não custa nada mensurável. Uma edição lê os registros das outras sessões e roda <code>git rev-parse</code> uma vez por pasta; quando outra sessão editou o mesmo arquivo, roda também <code>git status</code> nele. No primeiro teste real, a edição que achou colisão levou 444 ms de hook, e as outras menos de 60 ms (7 chamadas, outubro de 2026).</p>
<h2>Limites</h2>
<ul>
  <li>As sessões precisam dividir a máquina e a pasta home. Sessão em outro computador, ou num container com home própria, não aparece.</li>
  <li>Arquivo mudado por comando Bash (<code>sed -i</code>, um script, um formatador) não conta como edição. Só Edit, Write, MultiEdit e NotebookEdit contam.</li>
  <li><code>git checkout &lt;nome&gt;</code> lê igual com branch ou arquivo, então a nota diz "para outra branch ou uma versão antiga".</li>
  <li>Testado só no Linux. No Windows, os caminhos são comparados com barra normal, como o git imprime, e comando git pela ferramenta PowerShell é conferido como no Bash. Um <code>cd</code> para caminho do Git Bash como <code>/c/work</code> não é seguido.</li>
</ul>
{install_one('collision-guard')}
''')

page('Guardas', 'pipefail', 'funnel', '<code>pipefail</code>', 'pipefail', f'''
{meta(VERS['pipefail'])}
<p class="lead">Põe <code>set -o pipefail;</code> num comando que passa um teste, typecheck ou lint por <code>tail</code>, <code>head</code> ou <code>grep</code>.</p>
<h2>Por que</h2>
<p>Um pipeline sai com o código do último comando. <code>yarn test | tail -20</code> sai com 0 quando o teste reprova, porque o <code>tail</code> deu certo, e o agente lê aprovado. Reescrever o comando não custa nada e poupa o agente de uma conclusão errada.</p>
<h2>O que faz</h2>
<ul>
  <li>Reconhece o executor onde ele roda: <code>yarn</code>, <code>npm run</code>, <code>pnpm</code> ou <code>bun run</code> com <code>test</code>, <code>e2e</code>, <code>typecheck</code>, <code>lint</code>, <code>check</code> e parecidos, ou com um script listado em <code>extraRunners</code>, e também <code>turbo run</code>, <code>vitest</code>, <code>jest</code>, <code>playwright test</code>, <code>tsc</code>, <code>vue-tsc</code>, <code>eslint</code>, <code>pytest</code>, <code>go test</code> e <code>cargo test</code>. Texto entre aspas e corpo de heredoc não contam.</li>
  <li>Põe <code>set -o pipefail;</code> na frente, roda e avisa o agente que um <code>| head</code> pode fazer o executor sair com 141 (SIGPIPE).</li>
  <li>Deixa em paz um comando que já fala em <code>pipefail</code>.</li>
</ul>
{code('yarn test | tail -20' + chr(10) + '# vira' + chr(10) + 'set -o pipefail; yarn test | tail -20', 'o que o mod reescreve')}
<h2>Opções</h2>
{opts([('enabled', '<code>true</code>', 'Desligado, o mod não faz nada: nenhum comando é reescrito. Vale na próxima sessão, ou depois de <code>/reload-plugins</code>.'),
    ('extraRunners', 'lista vazia', 'Nomes de script que também contam como executor quando um gerenciador de pacotes chama: <code>yarn &lt;nome&gt;</code>, <code>npm run &lt;nome&gt;</code>, <code>pnpm &lt;nome&gt;</code>, <code>bun run &lt;nome&gt;</code>.')])}
<p>Ponha aqui o script de checagem do repo quando o código de saída dele diz se o código funciona, como um <code>verify</code> que roda lint, tipos e testes. O mod passa a reescrever <code>yarn verify | tail</code> também.</p>
{diary('pipefail', 'uma linha por reescrita com o executor (<code>yarn vitest</code>, nunca o comando inteiro), mais uma linha <code>session-summary</code>.')}
<h2>Custo</h2>
<p>O hook somou uns 2 ms por chamada Bash na máquina Linux do autor (56 chamadas medidas em outubro de 2026, estimativa).</p>
<h2>Limites</h2>
<ul>
  <li>Só <code>tail</code>, <code>head</code> e <code>grep</code> como filtro. <code>sed</code>, <code>awk</code> e outros ficam de fora.</li>
  <li>Executor escondido dentro de um script que o comando chama não aparece.</li>
  <li>Só a ferramenta Bash. No Windows sem Git Bash, os comandos passam pela ferramenta PowerShell e o mod não mexe. Testado só no Linux.</li>
</ul>
{install_one('pipefail')}
''')

page('Guardas', 'memory-guard', 'mem', '<code>memory-guard</code>', 'memory-guard', f'''
{meta(VERS['memory-guard'], '/ram')}
<p class="lead">Mantém typecheck, build, teste e Playwright dentro do limite de memória, e repete com um processo só o comando morto com exit 137. No Linux, o limite é o cgroup mais apertado ou a memória da máquina; no macOS e no Windows, a memória da máquina.</p>
<h2>Por que</h2>
<p>No Linux, quando a memória acaba ou um cgroup bate no <code>memory.max</code>, o kernel mata o maior processo, que quase sempre é o comando pesado, e o agente vê exit 137 sem saber por quê. O mod confere a folga antes do comando pesado e adapta o comando a ela.</p>
<h2>O que faz</h2>
<p>Antes de um comando pesado, o mod compara o pico esperado com a folga, menos a margem. A folga é a memória disponível da máquina, ou o que sobra embaixo do limite de cgroup mais apertado quando a sessão roda num, como num serviço do systemd ou num container:</p>
<ol class="steps">
  <li><b>Cabe</b><p>Roda como veio.</p></li>
  <li><b>Só cabe um processo</b><p>O mod põe <code>--concurrency=1</code>, <code>--workers=1</code> ou <code>--maxWorkers=1</code> e avisa o agente.</p></li>
  <li><b>Não cabe nada</b><p>Espera até <code>waitSeconds</code> a memória liberar.</p></li>
  <li><b>Não liberou</b><p>Recusa o comando e diz ao agente o que está usando a memória.</p></li>
</ol>
<p>Depois do comando, o mod guarda o pico medido para a próxima estimativa e repete com um processo o comando que morreu com exit 137. Até medir um comando, as estimativas são 1 GB para typecheck e build, 600 MB para teste e 500 MB para Playwright.</p>
<p>Sem limite de cgroup, como na maioria dos desktops e notebooks Linux, a folga é o <code>MemAvailable</code> do <code>/proc/meminfo</code>. No macOS são as páginas livres, inativas, especulativas e purgáveis do <code>vm_stat</code> contra o total de <code>sysctl -n hw.memsize</code>. No Windows é o <code>FreePhysicalMemory</code> contra o <code>TotalVisibleMemorySize</code>, lidos pelo PowerShell. Com limite de cgroup, conta o working set: <code>memory.current</code> menos <code>inactive_file</code>, que o kernel libera antes de matar alguém.</p>
<h2>Comandos</h2>
<p><code>/ram</code> mostra a folga, o uso e os limites de cada cgroup quando há, e os picos medidos. Diz que não há leitura quando o sistema não dá nenhuma. No terminal abre também a janela Memory, com uma barra por cgroup e a marca do alto, atualizado a cada 2 segundos. <code>r</code> atualiza e <code>esc</code> fecha.</p>
<h2>Opções</h2>
{opts([
    ('enabled', '<code>true</code>', 'Desligado, o mod não faz nada: comando pesado roda como veio, e o <code>/ram</code> some. Vale na próxima sessão, ou depois de <code>/reload-plugins</code>.'),
    ('margin', '<code>2</code>', 'Porcentagem de memória mantida livre: do <code>memory.max</code> de cada cgroup, ou do total da máquina sem limite de cgroup. A marca do alto só conta para cgroup sem max.'),
    ('waitSeconds', '<code>120</code>', 'Quanto tempo um comando pesado espera memória antes de ser recusado.'),
    ('reduce', '<code>true</code>', 'Quando só cabe um processo, põe <code>--concurrency=1</code>, <code>--workers=1</code> ou <code>--maxWorkers=1</code>.'),
    ('wait', '<code>true</code>', 'Quando nada cabe, espera até <code>waitSeconds</code>. Desligado, o passo seguinte vem na hora.'),
    ('refuse', '<code>true</code>', 'Quando a memória não libera, recusa o comando. Desligado, ele roda como veio e pode morrer.'),
    ('retry137', '<code>true</code>', 'Repete com um processo só o comando morto com exit 137.'),
])}
<h2>O que grava</h2>
<ul>
  <li><code>~/.local/state/mods/memory-guard/&lt;dia&gt;-&lt;sessão&gt;.jsonl</code>: uma linha por comando reduzido, recusado ou repetido e por pico medido, mais uma linha <code>session-summary</code> com o tempo que os comandos esperaram.</li>
  <li>Os últimos 3 picos medidos de cada comando, no armazenamento comum dos mods, em <code>peaks</code>.</li>
</ul>
<h2>Custo</h2>
<p>O hook somou uns 4 ms por chamada Bash na máquina Linux do autor, sem contar a espera por memória (56 chamadas medidas em outubro de 2026, estimativa). Cada comando pesado lê os arquivos de memória uma vez por segundo enquanto roda, para medir o pico. No macOS e no Windows a leitura roda um comando e vale por 10 segundos: <code>sysctl</code> e <code>vm_stat</code> levam poucos milissegundos, e o PowerShell cerca de um segundo para abrir (estimativa).</p>
<h2>Limites</h2>
<ul>
  <li>O pico é medido no cgroup inteiro, ou na máquina sem cgroup, então outra sessão começando junto infla a medida. Guardar só as 3 últimas deixa a inflada envelhecer.</li>
  <li>O <code>tsc</code> não tem flag de processo único, então typecheck que não cabe espera ou é recusado.</li>
  <li>Comando em segundo plano volta na hora e não dá medida.</li>
  <li>As leituras do macOS e do Windows foram testadas só contra saída simulada de <code>vm_stat</code>, <code>sysctl</code> e PowerShell. Ali a folga é da máquina inteira, sem limite por sessão, e a leitura pode ter até 10 segundos.</li>
  <li>Quando a leitura falha, o comando pesado roda como veio, nada espera nem é recusado e nenhum pico é guardado. <code>/ram</code> diz que não há leitura. A repetição com um processo depois de exit 137 continua valendo.</li>
</ul>
{install_one('memory-guard')}
''')

page('Guardas', 'loop-breaker', 'loop', '<code>loop-breaker</code>', 'loop-breaker', f'''
{meta(VERS['loop-breaker'])}
<p class="lead">Percebe quando o agente anda em círculo e manda ele parar e mudar de abordagem.</p>
<h2>Por que</h2>
<p>Um agente que segue editando o mesmo arquivo depois da mesma falha gasta token e tempo sem chegar mais perto. Um empurrão curto na hora certa faz ele dar um passo atrás, o que uma regra no <code>CLAUDE.md</code> não garante.</p>
<h2>O que faz</h2>
<p>O mod conta três sinais por loop do agente (a conversa principal e cada subagente), zerados no fim de cada turno:</p>
<ul>
  <li>Tentativas de correção: edições num arquivo enquanto um comando que falhou não passou de novo.</li>
  <li>Erros repetidos: o mesmo erro voltando, ignorando números, caminhos e valores entre aspas.</li>
  <li>Chamadas repetidas: a mesma ferramenta com os mesmos argumentos, em sequência.</li>
</ul>
<p>Quando uma contagem chega ao limite, o mod acrescenta uma nota ao resultado da ferramenta. A nota começa com <code>Loop check</code> e pede ao agente que escreva o que tentou e depois releia o código, forme uma hipótese nova ou pergunte a você. Nada é recusado.</p>
<h2>Opções</h2>
{opts([
    ('enabled', '<code>true</code>', 'Desligado, o mod não faz nada: nada é contado, nenhum empurrão. Vale na próxima sessão, ou depois de <code>/reload-plugins</code>.'),
    ('editLimit', '<code>5</code>', 'Tentativas de correção num arquivo, num turno, antes do empurrão.'),
    ('errorLimit', '<code>3</code>', 'Vezes que o mesmo erro pode voltar num turno antes do empurrão.'),
    ('repeatLimit', '<code>3</code>', 'Chamadas idênticas em sequência antes do empurrão.'),
    ('editCheck', '<code>true</code>', 'Empurra depois de <code>editLimit</code> tentativas de correção num arquivo.'),
    ('errorCheck', '<code>true</code>', 'Empurra depois de o mesmo erro voltar <code>errorLimit</code> vezes.'),
    ('repeatCheck', '<code>true</code>', 'Empurra depois de <code>repeatLimit</code> chamadas idênticas em sequência.'),
])}
{diary('loop-breaker', 'uma linha por empurrão com o tipo e a contagem, mais uma linha <code>session-summary</code>.')}
<h2>Custo</h2>
<p>O hook somou uns 2 ms por chamada de ferramenta na máquina Linux do autor (60 chamadas medidas em outubro de 2026, estimativa).</p>
<h2>Limites</h2>
<ul>
  <li>A falha é lida do código de saída e de palavras de falha na saída, então ferramenta que falha calada não conta.</li>
  <li>A contagem zera no fim de cada turno, então um loop que atravessa vários turnos passa.</li>
  <li>Testado só no Linux.</li>
</ul>
{install_one('loop-breaker')}
''')

page('Guardas', 'usage-limit', 'gauge', '<code>usage-limit</code>', 'usage-limit', f'''
{meta(VERS['usage-limit'], '/limit')}
<p class="lead">Não deixa o limite de uso da conta acabar no meio de uma tarefa.</p>
<h2>Por que</h2>
<p>Quando uma janela de 5 horas ou de 7 dias chega a 100%, a sessão para onde estiver, muitas vezes no meio de uma edição, e nada retoma. O mod desacelera antes disso, faz o agente commitar o trabalho, para numa reserva que fica para você e retoma a sessão sozinho quando a janela reinicia.</p>
<h2>As três etapas</h2>
<p>Cada janela tem três etapas, cada uma com chave e porcentagem próprias:</p>
{table(['Etapa', 'Janela de 5 horas', 'Janela de 7 dias'], [
    ('Freio: um subagente por vez', '90%', '97%'),
    ('Commit: pede um commit <code>wip:</code>', '97%', '98%'),
    ('Pausa: guarda o resto para você', '98%', '99%'),
])}
<p>Os limites de 7 dias valem também para as janelas semanais por modelo, como <code>seven_day_opus</code>. Cada janela é julgada pelos próprios limites, e vale o resultado mais restritivo: janela pausada ganha de janela freada. Com duas janelas pausadas, segura a sessão a que reinicia por último.</p>
<h2>O que faz</h2>
<ul>
  <li>A partir do freio, roda um subagente por vez.</li>
  <li>A partir do commit, o agente recebe uma vez por janela o pedido de commitar o trabalho em andamento em cada repo que mudou, com mensagem <code>wip:</code> e sem push. Ele põe no stage só os arquivos que mudou, então o trabalho de outra sessão no mesmo repo fica de fora. Só a conversa principal recebe o pedido.</li>
  <li>Na pausa, toda chamada de ferramenta é recusada, menos um comando que só faz stage e commit (<code>git add</code>, <code>git commit</code>, <code>cd</code>, ligados por <code>&amp;&amp;</code>), para o trabalho ser commitado mesmo quando uma rajada de pedidos pula a etapa do commit. O agente escreve em até 3 linhas onde parou, e o mod agenda a retomada para a hora do reinício mais 2 minutos.</li>
  <li>Um prompt que você digita durante a pausa ganha um turno sem subagentes, pago com a reserva.</li>
  <li>Um prompt que ninguém digitou (uma rotina, outra sessão, uma notificação de tarefa) fica guardado e é entregue na retomada.</li>
  <li>A faixa acima do prompt mostra cada janela com barra, marca de pausa própria, porcentagem e hora do reinício, a partir de 75% por padrão. A barra fica amarela a partir do freio ou do commit da janela, e vermelha a partir da pausa.</li>
  <li>A status line embaixo do prompt mostra o estado enquanto o mod segura alguma coisa.</li>
</ul>
<h2>Comandos</h2>
<p><code>/limit</code> mostra cada janela com as etapas, o estado e o que está guardado para a retomada. Em texto simples, então lê igual pelo Remote Control.</p>
<h2>Opções</h2>
{opts([
    ('enabled', '<code>true</code>', 'Desligado, o mod não faz nada: sem freio, commit, pausa nem retomada, e o <code>/limit</code> some. Vale na próxima sessão, ou depois de <code>/reload-plugins</code>.'),
    ('fiveHourThrottle', '<code>true</code>', 'Freio na janela de 5 horas.'),
    ('fiveHourThrottleAt', '<code>90</code>', 'A partir dessa porcentagem da janela de 5 horas, um subagente por vez.'),
    ('fiveHourCommit', '<code>true</code>', 'Pedido de commit na janela de 5 horas.'),
    ('fiveHourCommitAt', '<code>97</code>', 'A partir dessa porcentagem da janela de 5 horas, pede ao agente uma vez por janela que commite sem push.'),
    ('fiveHourPause', '<code>true</code>', 'Pausa na janela de 5 horas.'),
    ('fiveHourPauseAt', '<code>98</code>', 'A sessão pausa nessa porcentagem da janela de 5 horas.'),
    ('sevenDayThrottle', '<code>true</code>', 'Freio nas janelas de 7 dias.'),
    ('sevenDayThrottleAt', '<code>97</code>', 'A partir dessa porcentagem de uma janela de 7 dias, um subagente por vez.'),
    ('sevenDayCommit', '<code>true</code>', 'Pedido de commit nas janelas de 7 dias.'),
    ('sevenDayCommitAt', '<code>98</code>', 'A partir dessa porcentagem de uma janela de 7 dias, pede ao agente uma vez por janela que commite sem push.'),
    ('sevenDayPause', '<code>true</code>', 'Pausa nas janelas de 7 dias.'),
    ('sevenDayPauseAt', '<code>99</code>', 'A sessão pausa nessa porcentagem de uma janela de 7 dias.'),
    ('timeZone', 'vazio', 'Fuso IANA das horas de reinício mostradas, como <code>America/Sao_Paulo</code>. Vazio usa o do sistema.'),
    ('resume', '<code>true</code>', 'Retoma a sessão quando a janela reinicia, depois da pausa ou do erro de limite. Desligado, você retoma, e os prompts automáticos que chegam na pausa são descartados em vez de guardados. O nome antigo <code>resumeOnError</code> ainda funciona.'),
    ('bandFrom', '<code>75</code>', 'Mostra a faixa a partir dessa porcentagem da janela mais cheia.'),
])}
<p>As opções por janela não têm padrão no manifesto, então as configurações de antes da 1.2 continuam valendo onde a opção nova não foi definida. <code>alert</code> define o freio de todas as janelas, <code>commitAt</code> o commit (<code>0</code> desliga) e <code>reserve</code> a pausa em 100 menos o valor. A opção da janela sempre ganha delas na própria etapa.</p>
<h2>O que grava</h2>
<ul>
  <li><code>~/.local/state/mods/usage-limit/&lt;dia&gt;-&lt;sessão&gt;.jsonl</code>: uma linha por mudança de estado, recusa, prompt guardado e retomada, mais uma linha <code>session-summary</code> no fim da sessão.</li>
  <li>A última leitura das janelas, no armazenamento comum dos mods, em <code>windows</code>, para uma sessão nova começar da leitura que outra fez.</li>
</ul>
<h2>Custo</h2>
<p>O hook de <code>tool.call</code> somou uns 6 ms por chamada de ferramenta na máquina Linux do autor (60 chamadas medidas em outubro de 2026, estimativa).</p>
<h2>Limites</h2>
<ul>
  <li>A leitura chega com cada resposta do modelo, então uma rajada de pedidos em paralelo pode passar da pausa antes da próxima leitura. A retomada depois do erro de limite e o commit liberado na pausa cobrem esse caso.</li>
  <li>Um prompt de origem que o Claude Code não sabe classificar conta como seu e gasta a reserva.</li>
  <li><code>/clear</code>, <code>/resume</code> e <code>/branch</code> cancelam a retomada agendada e descartam as mensagens guardadas da conversa anterior.</li>
  <li>Na pausa, o comando que só faz commit passa pela ferramenta Bash ou, no Windows sem Git Bash, pela ferramenta PowerShell.</li>
  <li>Testado só no Linux.</li>
</ul>
{install_one('usage-limit')}
''')

# --- instrumentos ---
STYLES = [('refined', 'Duas linhas com barras em degradê. O padrão.'), ('blocks', 'Cada campo com fundo colorido.'),
          ('minimal', 'Campos escritos por extenso, barras finas.'), ('compact', 'Uma linha quando cabe, duas quando não cabe.')]
page('Instrumentos', 'hud', 'hud', '<code>hud</code>', 'hud', f'''
{meta(VERS['hud'], '/hud')}
<p class="lead">Mostra o modelo, o projeto e a branch, o contexto, os limites do plano e a folga de memória, embaixo do prompt como status line ou acima dele na faixa. Durante um turno, a faixa mostra também a última nota que outro mod deixou num resultado de ferramenta, que de outro jeito só o modelo lê.</p>
<h2>Os quatro estilos</h2>
<p>Escolha com a opção <code>style</code>. Cada estilo larga primeiro o campo menos útil quando o terminal é estreito, então nenhuma linha passa da largura. Abaixo, a saída real do <code>statusline.sh</code> para a mesma sessão.</p>
''' + ''.join(f'<h3><code>{s}</code></h3><p>{d}</p>' + term(statusline(s), f'status line · {s}') for s, d in STYLES) + f'''
<h2>A status line</h2>
<p>Um mod não desenha embaixo do prompt: esse lugar é do comando de status line das configurações. O mod traz um, <code>statusline/statusline.sh</code>, e o <code>/cockpit:setup</code> grava ele para você. Para gravar à mão no macOS ou no Linux, ponha isto no <code>~/.claude/settings.json</code>, com <code>band</code> em <code>off</code> para as linhas não aparecerem duas vezes:</p>
{code(STATUS_JSON, '~/.claude/settings.json')}
<p>O script precisa do Node 22.18 ou mais novo. <code>refreshInterval</code> roda o script de novo a cada 5 segundos, para o git, o PR e o tempo de sessão ficarem em dia com a sessão parada. No Windows, o PowerShell não roda <code>.sh</code>: aponte o comando para <code>node ~/.claude/plugins/marketplaces/cockpit/hud/statusline/statusline.ts</code>, com barra normal.</p>
<h3>Git e o PR</h3>
<p>O campo do git mostra a branch, os commits a enviar e a receber, os arquivos no stage, os mudados fora do stage e os não rastreados, ou <code>synced</code> quando não há nada. O PR é o pull request aberto da branch, do <code>gh pr view</code>, com os checks: passando, falhando ou rodando. O <code>gh</code> leva um segundo, então o script roda ele em segundo plano no máximo uma vez por minuto e mostra a última resposta enquanto isso. Sem <code>gh</code>, ou sem PR aberto, o campo some.</p>
<h3>Ícones</h3>
<p>Com <code>icons</code> em <code>nerd</code>, o padrão, os campos de git, pasta, modelo e memória usam glifos da Nerd Font, que só aparecem se a fonte do terminal for uma. Com <code>unicode</code>, usam <code>↑ ↓ + ● ? ✓</code> e nenhum glifo para pasta, modelo e memória.</p>
<h2>A faixa acima do prompt</h2>
<p>Sem a status line, o hud desenha na faixa acima do prompt. Com <code>band</code> em <code>panel</code>, o padrão, são duas linhas, com o lado direito da primeira encostado na última coluna:</p>
{term(BAND_PANEL, 'faixa · panel')}
<p>Durante um turno, quando outro mod deixou uma nota, vem a linha de atividade, como <code>loop-breaker: repeated error</code>. Ela some quando o turno acaba. O Claude Code já desenha a ferramenta rodando, os erros dela, os subagentes e o tempo do turno, então a faixa deixa isso de fora.</p>
{table(['Campo', 'Cores'], [
    ('<code>ctx</code>, o contexto', 'verde abaixo de 60%, amarelo abaixo de 85%, vermelho a partir de 85%'),
    ('<code>5h</code> e <code>7d</code>, as janelas do plano', 'verde abaixo de 75%, amarelo abaixo de 90%, vermelho a partir de 90%'),
    ('<code>mem</code>, a memória que ainda cabe', 'amarelo abaixo de 1 GB, vermelho abaixo de 500 MB'),
    ('Linha de atividade', 'amarelo'),
])}
<p>Num terminal estreito, a faixa larga campos em vez de quebrar a linha: primeiro encurta as barras, depois tira o <code>mem</code>, depois mostra <code>ctx</code>, <code>5h</code> e <code>7d</code> só em porcentagem, e por fim tira a contagem até o reinício. Com <code>band</code> em <code>line</code>, desenha uma linha só:</p>
{term(BAND_LINE, 'faixa · line')}
<h2>A janela do /hud</h2>
{term('SESSION   Opus 5.5 · my-app  main● · 38m · 214 calls · ctx 42%' + chr(10) + 'LIMITS    5h 61% resets 2h30m · 7d 44% resets 3d20h' + chr(10) + 'MEMORY    session 1.5G · slice 3.0/5.0G · 1.9G fits' + chr(10) + 'NOW       Bash yarn turbo run test 0:42 · 2 subagents' + chr(10) + 'TODAY     2 skills · 1 loop nudge · 0 refusals')}
<p><code>MEMORY</code> mostra o cgroup da sessão e o grupo cujo limite define a folga, ou a memória da máquina sem cgroup. <code>TODAY</code> conta as linhas de hoje nos diários dos outros mods. A janela atualiza a cada 2 segundos enquanto está aberto; <code>r</code> atualiza na hora e <code>esc</code> fecha.</p>
<h2>Opções</h2>
<p>No <code>/config</code>, ou em <code>pluginConfigs</code> no <code>~/.claude/settings.json</code>.</p>
{opts([
    ('enabled', '<code>true</code>', 'Desligado, o mod não faz nada: sem faixa, sem linha de atividade, sem <code>/hud</code>, e o script da status line imprime uma linha vazia. Vale na próxima sessão, ou depois de <code>/reload-plugins</code>.'),
    ('band', '<code>panel</code>', '<code>panel</code> desenha duas linhas acima do prompt, <code>line</code> uma, <code>off</code> nenhuma (o <code>/hud</code> continua). Use <code>off</code> com a status line.'),
    ('activity', '<code>true</code>', 'Mostra a linha de atividade durante o turno.'),
    ('memory', '<code>true</code>', 'Mostra a folga de memória na faixa e a linha <code>MEMORY</code>.'),
    ('bar', '<code>dots</code>', 'Glifos da barra: <code>blocks</code> (▰▱), <code>solid</code> (█░), <code>line</code> (━─), <code>dots</code> (●○) ou <code>squares</code> (■□).'),
    ('barWidth', '<code>10</code>', 'Células de uma barra cheia, de 4 a 30. Terminal estreito ainda encolhe.'),
    ('colors', 'vazio', 'Cores de ok, alerta e crítico, separadas por espaço: nome, <code>#rrggbb</code> ou número de 256 cores. Vazio usa verde, amarelo e vermelho.'),
    ('hide', 'vazio', 'Campos a esconder, separados por vírgula: <code>model</code>, <code>project</code>, <code>branch</code>, <code>age</code>, <code>calls</code>, <code>ctx</code>, <code>5h</code>, <code>7d</code>, <code>reset</code>, <code>mem</code>.'),
    ('barColor', '<code>gradient</code>', '<code>gradient</code> pinta cada célula pela posição, do verde ao vermelho. <code>solid</code> pinta a barra inteira pela porcentagem. <code>tone</code> usa as três cores de <code>colors</code>.'),
    ('style', '<code>refined</code>', 'Layout da status line: <code>refined</code>, <code>blocks</code>, <code>minimal</code> ou <code>compact</code>.'),
    ('icons', '<code>nerd</code>', '<code>nerd</code> para glifos da Nerd Font, <code>unicode</code> para marcas simples.'),
    ('contextBase', '<code>compact</code>', 'Contra o que o <code>ctx</code> mede. <code>compact</code>: 100% é a janela de auto-compact, quando menor que a do modelo. <code>window</code>: a janela inteira do modelo. Só na status line.'),
    ('timeZone', 'vazio', 'Fuso IANA das horas mostradas e do que conta como hoje. Vazio usa o do sistema.'),
])}
<h2>Custo</h2>
<p>O hook que desenha a faixa não lê disco: só arruma valores que eventos e timers já leram. A cada 15 segundos, parado ou não, roda um <code>git status</code> (limite de 3 segundos) e uma leitura de memória. Durante um turno, um timer de 1 segundo lê a lista de agentes para o <code>/hud</code> e só redesenha com a janela aberta. Cada chamada de ferramenta pede dois redesenhos, e o Claude Code limita a 10 por segundo.</p>
<h2>Limites</h2>
<ul>
  <li>No macOS e no Windows não há limite por sessão, então o campo de memória mostra a máquina inteira. Essas leituras foram testadas só contra saída simulada.</li>
  <li>Quando a leitura falha, o campo de memória some.</li>
  <li>O campo de PR precisa do <code>gh</code> logado.</li>
  <li>A faixa, a status line e a janela do /hud são da interface de terminal. Testado só em terminal, e a configuração do Windows não foi testada.</li>
</ul>
{install_one('hud')}
''')

page('Instrumentos', 'spinner-status', 'spinner', '<code>spinner-status</code>', 'spinner-status', f'''
{meta(VERS['spinner-status'], 'chama o Haiku')}
<p class="lead">Troca a dica embaixo do spinner por uma linha própria: em que ponto a sessão está, escrita pelo Haiku, ou uma dica sobre os mods instalados que combina com o momento.</p>
{term(SPINNER)}
<p>O spinner continua como o Claude Code desenha. A linha vai embaixo, cortada na largura da tela e em 100 caracteres. Um rótulo em negrito diz o que ela é: <code>Now:</code> para o ponto da sessão e <code>Mods:</code> para dica dos mods.</p>
<h2>Desligue a dica nativa</h2>
<p>Um mod não remove a linha de dica do próprio Claude Code. Desligue no <code>settings.json</code>, ou as duas aparecem juntas. O <code>/cockpit:setup</code> já faz isso, e é a mesma chave da linha <b>Show tips</b> do <code>/config</code>.</p>
{code('{ "spinnerTipsEnabled": false }', '~/.claude/settings.json')}
<h2>Os modos</h2>
{table(['Modo', 'O que a linha mostra', 'Chamadas ao modelo'], [
    ('<code>mixed</code>', 'O resumo da sessão e uma dica que o Haiku escolheu para o momento, trocando a cada 15 segundos. Antes da primeira resposta, uma dica do catálogo. É o padrão.', 'Uma por turno'),
    ('<code>tips</code>', 'Uma dica do catálogo, nova a cada turno.', 'Nenhuma'),
    ('<code>summary</code>', 'Só o resumo da sessão. Antes da primeira resposta, nada extra.', 'Uma por turno'),
])}
<p>O catálogo tem uma dica por comando e por mod do Cockpit: <code>/panel</code>, <code>/hud</code>, <code>/limit</code>, <code>/ram</code>, e o que <code>memory-guard</code>, <code>loop-breaker</code>, <code>secret-guard</code>, <code>pipefail</code> e <code>usage-limit</code> fazem. Os rótulos e o catálogo são em inglês. Nos modos <code>mixed</code> e <code>summary</code>, o Haiku escreve na língua da configuração <code>language</code> do Claude Code, ou na língua em que você escreve.</p>
<h2>Opções</h2>
{opts([
    ('enabled', '<code>true</code>', 'Desligado, o mod não faz nada e não chama modelo.'),
    ('mode', '<code>mixed</code>', '<code>mixed</code>, <code>tips</code> ou <code>summary</code>.'),
    ('model', '<code>claude-haiku-4-5-20251001</code>', 'O modelo que escreve a linha: um apelido como <code>haiku</code> ou um id completo.'),
])}
<h2>Custo</h2>
<p>Cada turno da conversa principal faz no máximo uma chamada ao modelo, em segundo plano, quando o turno começa. O spinner nunca espera: mantém a linha anterior até a nova chegar. O modelo lê os 3 últimos prompts que você digitou e o texto do agente entre eles, no máximo 3.000 caracteres, sem chamada nem saída de ferramenta. A resposta tem teto de 150 tokens.</p>
<p>Numa sessão de teste, três turnos gastaram 1.574 tokens de entrada e 139 de saída: uns 525 e 46 por turno, ou cerca de US$ 0,0008 por turno no preço do Haiku 4.5. Cada chamada levou cerca de um segundo.</p>
<h2>A resposta é dado</h2>
<p>A linha que o Haiku escreve é mostrada, nunca executada. O mod fica só com as linhas <code>NOW:</code> e <code>TIP:</code>, tira caracteres de controle e marcação, junta em uma linha e corta na largura. As instruções dizem ao modelo que o trecho da sessão é dado, não instrução.</p>
<h2>O que grava</h2>
<p>No fim de cada sessão, uma linha <code>session-summary</code> em <code>~/.local/state/mods/spinner-status/&lt;dia&gt;-&lt;sessão&gt;.jsonl</code>, com os turnos, as chamadas por resultado, as puladas porque uma ainda rodava, os tokens, o tempo do modelo e o tamanho do trecho. Nunca grava o trecho nem a linha.</p>
<h2>Limites</h2>
<ul>
  <li>A chamada ao modelo passa pelo próprio Claude Code, sem comando próprio, então funciona igual no macOS, no Windows e no Linux. Testado só no Linux.</li>
  <li>A linha do spinner é da interface de terminal. Testado só em terminal.</li>
</ul>
{install_one('spinner-status')}
''')

page('Instrumentos', 'panel', 'grid', '<code>panel</code>', 'panel', f'''
{meta(VERS['panel'], '/panel', 'chama o claude -p')}
<p class="lead">Uma página local com todas as sessões do Claude Code no seu computador: se ela espera você, o que precisa, o que está fazendo agora e o que terminou. O resumo de cada sessão vem do <code>claude -p</code>, refeito a cada poucos minutos e quando você pede.</p>
<div class="shot"><img src="../img/panel-dark.png" alt="A página do panel na vista Inbox: a máquina no topo, as sessões por urgência à esquerda e a sessão escolhida à direita" loading="lazy"></div>
<p class="figcap">A página com sessões inventadas, na vista Inbox.</p>
<h2>Abrir a página</h2>
<p>Digite <code>/panel</code> em qualquer sessão para o endereço, <code>http://localhost:7777</code> por padrão, e abra no navegador. O servidor sobe com a primeira sessão depois da instalação e continua rodando depois que ela termina. A página escuta só no <code>127.0.0.1</code>, então só o seu computador chega nela. Com as sessões em outra máquina, veja <a href="#remote">Como usar numa máquina remota</a>.</p>
<h2>O que a página mostra</h2>
<ul>
  <li>O topo mostra o computador numa linha: o uso de 5 horas e semanal do plano com o tempo até cada reinício, memória, CPU do último minuto, disco e os tokens das sessões nas últimas 24 horas, hora a hora. Um número fica âmbar em 75% e vermelho em 90%. À direita ficam <b>Notify</b>, <b>Refresh all</b> e <b>Mods</b>.</li>
  <li>Cada sessão mostra o estado (<code>Working</code>, <code>Waiting for you</code>, <code>Blocked</code>, <code>Done</code>, <code>Idle</code>), um título, o projeto, a branch com arquivos mudados e commits à frente ou atrás, o modelo, a sua última mensagem, a ferramenta rodando agora, o resumo da tarefa, o próximo passo e o que terminou. Fecham o cartão o contexto usado até o ponto de compactar, os tokens das últimas 24 horas, a memória dos processos e há quanto tempo roda.</li>
  <li>A gaveta <b>Mods</b> mostra o computador completo, as últimas ações dos guardas, o que cada guarda fez hoje e quantos resumos a página fez hoje, com tokens e preço de API. No Linux mostra também a memória de cada cgroup com limite e o estado dos serviços do systemd.</li>
</ul>
<h2>As cinco vistas</h2>
<p>O seletor embaixo do topo escolhe a vista, e a página lembra. O endereço também aceita a vista no hash, como <code>#board</code>, e <code>#mods</code> abre a gaveta.</p>
{table(['Vista', 'O que mostra', 'Teclas'], [
    ('<b>Inbox</b>', 'O padrão. As sessões por urgência à esquerda e a escolhida inteira à direita.', '<code>j</code> e <code>k</code> ou setas movem, <code>1</code> a <code>4</code> escolhem opção, <code>r</code> vai para a resposta'),
    ('<b>Board</b>', 'Colunas por estado, com cartões pequenos. Um cartão abre a sessão numa gaveta lateral.', '<code>1</code> a <code>4</code> na gaveta, <code>esc</code> fecha'),
    ('<b>Deck</b>', 'Uma grade de cartões completos, com filtros: todas, as que precisam de você, rodando, terminadas e encerradas.', ''),
    ('<b>Focus</b>', 'Um cartão grande para a sessão que mais precisa de você, e as outras embaixo.', '<code>n</code> e <code>p</code> ou setas movem'),
    ('<b>Timeline</b>', 'Uma linha por sessão com os tokens hora a hora nas últimas 24 horas, e uma linha com todas juntas.', ''),
], 'stack')}
<p><b>Working</b> vem do próprio Claude Code assim que um turno começa. <b>Waiting for you</b>, <b>Blocked</b>, <b>Done</b> e <b>Idle</b> vêm do resumo, que o <code>claude -p</code> escreve a partir da conversa: 20 segundos depois de um turno terminar, a cada 5 minutos para sessão que mudou, e quando você aperta <b>Refresh</b>.</p>
<h2>Responder uma sessão pela página</h2>
<p>Quando uma sessão espera uma decisão, as opções dela viram botões. Aperte uma, ou o número dela, confira o texto e confirme. O campo de resposta manda qualquer texto do mesmo jeito. A página deixa o texto na caixa de entrada da sessão, o mod <code>panel</code> daquela sessão confere a caixa a cada 2 segundos e envia o texto como prompt seu, e o Claude Code roda quando a sessão fica parada. Funciona no macOS, no Windows e no Linux, no terminal, no app Desktop, numa IDE ou pelo Remote Control, com ou sem tmux.</p>
{callout('note', 'Opções em cinza', '<p>A sessão só aceita resposta quando o mod dela conferiu a caixa nos últimos 15 segundos. Até lá, as opções ficam em cinza e o campo de resposta some. Uma sessão com mod <code>panel</code> antigo fica assim até você rodar <code>/reload-plugins</code> nela. Se a sessão não pega a mensagem em 6 segundos, a página retira e avisa.</p>')}
<h2>Auditar os mods</h2>
<p>A metade de baixo da gaveta <b>Mods</b> audita os mods pelos diários do último dia, 7 dias ou 30 dias. Cada linha mostra a versão, se está ligado, em quantas sessões rodou, o que fez, as falhas em vermelho, o tempo que os hooks somaram por chamada, a chamada mais lenta, o custo de API das chamadas a modelo e a última ação. Um mod sem nada gravado numa semana não trabalha na sua máquina.</p>
<div class="shot"><img src="../img/panel-mods.png" alt="A gaveta Mods: o computador, os guardas e uma linha por mod com ações, falhas e tempo por chamada" loading="lazy"></div>
<h2>Opções</h2>
{opts([
    ('enabled', '<code>true</code>', 'Desligado, o mod não faz nada: sem <code>/panel</code>, sem subir servidor, sem respostas; um servidor que já roda continua. Vale na próxima sessão, ou depois de <code>/reload-plugins</code>.'),
    ('port', '<code>7777</code>', 'A porta da página, no <code>127.0.0.1</code>.'),
    ('model', '<code>sonnet</code>', 'O modelo do <code>claude -p</code> em cada resumo: <code>sonnet</code>, <code>haiku</code> ou <code>opus</code>.'),
    ('refreshMinutes', '<code>5</code>', 'Uma sessão cuja conversa mudou ganha resumo novo nesse intervalo.'),
    ('autostart', '<code>true</code>', 'Sobe o servidor quando uma sessão começa e a porta não responde. Desligue quando um gerenciador de serviços roda o servidor.'),
    ('answers', '<code>true</code>', 'Deixa a página mandar texto para esta sessão como prompt seu. Desligado, a página mostra as opções da sessão em cinza e sem campo de resposta.'),
])}
<h2>Subir o servidor à mão</h2>
<p>A página precisa do Python 3.9 ou mais novo, como <code>python3</code>, <code>python</code> ou <code>py</code>, e do <code>curl</code>. Com <code>autostart</code> ligado, a primeira sessão sobe o servidor, e ele continua depois que ela termina. Para subir você mesmo, rode o arquivo do servidor na pasta do plugin, que é o <code>installPath</code> de <code>panel@cockpit</code> em <code>~/.claude/plugins/installed_plugins.json</code>:</p>
{code('python3 -I <pasta do plugin>/server/panel.py')}
<p>No Windows, use <code>python</code> ou <code>py</code> no lugar de <code>python3</code>. Ponha em <code>PANEL_CLAUDE</code> o caminho do <code>claude</code> quando ele não está no <code>PATH</code>.</p>
<h2>Como o resumo é feito</h2>
<p>O servidor monta um digest da conversa de no máximo 48.000 caracteres: a mensagem que abriu a tarefa e as linhas mais novas que couberem, cada chamada de ferramenta cortada em uma linha. Manda para <code>claude -p --safe-mode --tools "" --no-session-persistence</code> com um schema JSON. A chamada não carrega hooks, plugins nem ferramentas, não guarda conversa própria e responde num formato fixo, na língua em que você escreve.</p>
<h2>Custo</h2>
<p>Cada resumo é uma chamada <code>claude -p</code> e conta no limite do plano. Na máquina Linux do autor, em outubro de 2026, o resumo de uma sessão longa leu uns 48.000 tokens e levou de 6 a 10 segundos, com pico de 213 MB no servidor. No preço de API com <code>sonnet</code>, um resumo custou uns US$ 0,07, e com quatro sessões trabalhando a página gastou até US$ 2,40 por hora. No plano Pro ou Max, isso sai do uso do plano, não em dinheiro. O <code>haiku</code> custa umas 20 vezes menos por token, com resumo mais curto e menos exato.</p>
<h2>O que grava</h2>
<ul>
  <li><code>~/.local/state/mods/panel/summaries/&lt;sessão&gt;.json</code>: o último resumo de cada sessão, com a hora e o tamanho da conversa que leu.</li>
  <li><code>~/.local/state/mods/panel/&lt;dia&gt;-server.jsonl</code>: uma linha por resumo com o motivo, o tempo, o estado e os tokens, uma por falha e uma por resposta enviada com o tamanho. Nunca grava o conteúdo da sessão nem o que você mandou.</li>
</ul>
<h2>Limites</h2>
<ul>
  <li>As sessões precisam rodar na mesma máquina e com o mesmo usuário do servidor.</li>
  <li>A página não tem login. Quem conecta na porta daquela máquina lê a página, pede resumo e digita nas sessões, então mantenha no <code>127.0.0.1</code>. O servidor recusa pedido vindo de página de outro site.</li>
  <li>Uma resposta enviada pela página espera a sessão parar. Durante um turno ela não chega ao agente e roda como turno novo depois.</li>
  <li>O estado vem do modelo e pode atrasar em relação à sessão. Sessão ocupada sempre aparece como <code>Working</code>.</li>
  <li>No macOS e no Windows não há grupos de memória, serviços nem espera de disco. Testado no Linux; os caminhos do macOS e do Windows rodam só em teste simulado.</li>
</ul>
{install_one('panel')}
''')

page('Instrumentos', 'skill-loader', 'book', '<code>skill-loader</code>', 'skill-loader', f'''
{meta(VERS['skill-loader'])}
<p class="lead">Carrega a skill certa na hora certa, para o <code>CLAUDE.md</code> não precisar de regra do tipo "carregue a skill X antes de Y".</p>
<h2>Por que</h2>
<p>Uma regra no <code>CLAUDE.md</code> que manda carregar uma skill antes de editar um arquivo só funciona quando o agente lembra. O mod olha as chamadas de ferramenta e entrega a skill ele mesmo.</p>
<h2>O que faz</h2>
{table(['Quando o agente', 'Skill'], [
    ('Lê ou escreve um <code>.ts</code>, <code>.tsx</code>, <code>.mts</code> ou <code>.cts</code>', '<code>typescript-best-practices</code>'),
    ('Lê ou escreve <code>SKILL.md</code>, <code>AGENTS.md</code> ou <code>CLAUDE.md</code>', '<code>writing-for-agents</code>'),
    ('Lê ou escreve <code>CONTEXT.md</code>, <code>CONTEXT-MAP.md</code> ou um arquivo em <code>adr/</code>, <code>adrs/</code> ou <code>decisions/</code>', '<code>domain-modeling</code>'),
    ('Lê ou escreve um <code>README</code>, ou roda <code>git commit</code>, <code>gh pr create</code> ou <code>gh pr edit</code>', '<code>technical-writing</code>'),
])}
<ul>
  <li>Na leitura, o texto inteiro da skill vem junto com o arquivo. O Edit exige leitura antes, então a skill chega antes da edição.</li>
  <li>Numa escrita sem leitura (arquivo novo, commit, PR), o mod segura a chamada uma vez, com o texto da skill na recusa, e o agente repete a chamada.</li>
  <li>Quando o seu prompt traz um erro ou diz que algo quebrou, o mod lembra o agente de carregar <code>diagnosing-bugs</code>.</li>
</ul>
<p>Cada skill carrega uma vez por conversa. A compactação zera a lista, porque o resumo pode perder o texto de uma skill.</p>
<h2>As skills</h2>
<p>O mod traz as cinco skills que entrega, na pasta <code>skills/</code>, então funciona sem nada mais instalado. O Claude Code também lista elas como <code>skill-loader:&lt;nome&gt;</code>. O mod lê uma skill primeiro da própria pasta, depois de <code>&lt;projeto&gt;/.claude/skills/&lt;nome&gt;/SKILL.md</code> e depois de <code>~/.claude/skills/&lt;nome&gt;/SKILL.md</code>. As skills são de Matt Pocock, sob licença MIT.</p>
<h2>Opções</h2>
{opts([
    ('enabled', '<code>true</code>', 'Desligado, o mod não faz nada: nenhuma skill é entregue e nada é segurado. Vale na próxima sessão, ou depois de <code>/reload-plugins</code>.'),
    ('holdWrites', '<code>true</code>', 'Segura uma vez a escrita, o commit ou o PR, com a skill na recusa, para o agente refazer seguindo a skill. Desligado, a chamada roda e a skill vem com o resultado.'),
    ('diagnoseReminder', '<code>true</code>', 'Lembra o agente de carregar <code>diagnosing-bugs</code> quando o seu prompt traz um erro ou diz que algo quebrou.'),
])}
{diary('skill-loader', 'uma linha por skill carregada, chamada segurada, skill que faltou e lembrete, mais uma linha <code>session-summary</code>.')}
<h2>Custo</h2>
<p>O hook somou uns 2 ms por chamada de ferramenta na máquina Linux do autor (60 chamadas medidas em outubro de 2026, estimativa). Uma escrita segurada custa ao agente uma chamada a mais.</p>
<h2>Limites</h2>
<ul>
  <li>Subagentes ficam de fora: a skill entregue ali cairia na conversa principal.</li>
  <li>A detecção de erro reconhece frases comuns em inglês e em português e o formato de stack trace, então perde um erro descrito com outras palavras.</li>
  <li>Testado só no Linux.</li>
</ul>
{install_one('skill-loader')}
''')

page('Memória', 'global-memory', 'globe', '<code>global-memory</code>', 'global-memory', f'''
{meta(VERS['global-memory'])}
<p class="lead">Acrescenta uma pasta de memória da máquina ao lado da memória automática de cada projeto, para o que vale na máquina chegar a toda sessão, de qualquer pasta.</p>
<h2>Por que</h2>
<p>A memória automática do Claude Code é por projeto. Um fato da máquina, como onde uma ferramenta mora ou como se chega num serviço, salvo na memória de um projeto falta em todos os outros. O mod cria uma pasta global que toda sessão lê e diz ao agente que memória vai para lá.</p>
<h2>O que faz</h2>
<ul>
  <li>Reescreve a seção de memória do prompt de sistema para descrever as duas pastas e onde vai cada tipo: <code>user</code> e <code>feedback</code> vão para a global por padrão, <code>reference</code> vai para a global quando é sobre a máquina, e <code>project</code> fica sempre no projeto.</li>
  <li>Põe o <code>MEMORY.md</code> global nos arquivos de instrução, então o índice dele chega a toda sessão como o do projeto.</li>
  <li>Respeita o modo do Claude Code. Com memória só de leitura, a pasta global também fica só de leitura. Com memória automática desligada, ou sem a pasta global ou o <code>MEMORY.md</code> dela, o mod não muda nada.</li>
</ul>
<h2>Ligar</h2>
<p>O mod não cria nada. Crie a pasta e um <code>MEMORY.md</code> vazio, e ele começa na próxima sessão:</p>
{code('mkdir -p ~/.claude/global-memory && touch ~/.claude/global-memory/MEMORY.md')}
<p><code>globalDir</code> pode apontar para uma pasta dentro de um repo git, como <code>~/dotfiles/memory</code>, para as memórias terem versão e irem com você para outra máquina.</p>
{callout('warn', 'Nada de credencial', '<p>Toda sessão da máquina lê a pasta global. Nunca salve senha ou chave lá.</p>')}
<h2>No plano Team ou Enterprise</h2>
<p>O guarda embutido <code>sec-default@builtin</code> ignora mod instalado pelo usuário em <code>prompt.section</code> e <code>prompt.context</code>, os dois eventos de que este mod precisa. Liste ele em <code>prependPlugins</code> nas managed settings, antes do guarda, para contar como mod da organização:</p>
{code(chr(10).join(['{', '  "enabledPlugins": { "global-memory@cockpit": true },', '  "prependPlugins": ["global-memory@cockpit", "sec-default@builtin"]', '}']), 'managed settings')}
<p>No plano pessoal funciona como instalado; no Team ou Enterprise não faz nada até essas configurações entrarem.</p>
<h2>Opções</h2>
{opts([('enabled', '<code>true</code>', 'Desligado, o mod não faz nada: a seção de memória fica como o Claude Code escreveu. Vale na próxima sessão, ou depois de <code>/reload-plugins</code>.'),
    ('globalDir', '<code>~/.claude/global-memory</code>', 'Pasta da memória da máquina, com o próprio <code>MEMORY.md</code>.')])}
{diary('global-memory', 'uma linha a cada seção de memória reescrita, índice global acrescentado ou vez que o mod se afastou e por quê, mais uma linha <code>session-summary</code>.')}
<h2>Custo</h2>
<p>Nenhum por chamada de ferramenta: o mod não tem hook de <code>tool.call</code>. Ele lê o <code>MEMORY.md</code> global quando o prompt de sistema e o primeiro contexto são montados. O texto reescrito depende só da entrada, então o cache do prompt continua valendo.</p>
<h2>Limites</h2>
<ul>
  <li>A reescrita casa com o texto da seção de memória que o Claude Code 2.1.292 manda. Um texto diferente fica como está e entra no diário como <code>skipped-unrecognized</code>.</li>
  <li>Testado só no Linux.</li>
</ul>
{install_one('global-memory')}
''')

page('Memória', 'todo', 'tag', '<code>todo</code>', 'todo', f'''
{meta(VERS['todo'])}
<p class="lead">Mantém a lista de tarefas nativa do Claude Code na frente do agente: as tarefas abertas no início da sessão e em cada prompt seu, o lembrete de que pedido novo vira tarefa antes de tudo, e a tarefa concluída movida para um arquivo de histórico.</p>
<h2>Por quê</h2>
<p>As ferramentas de tarefa (<code>TaskCreate</code>, <code>TaskList</code>, <code>TaskUpdate</code>, <code>TaskGet</code>) gravam um JSON por tarefa em <code>~/.claude/tasks/&lt;lista&gt;/</code>, então a lista sobrevive à compactação, ao <code>--resume</code> e ao <code>--continue</code>. O modelo esquece que a lista existe. Depois da compactação ele trabalha pelo resumo, e o pedido que vivia só na conversa se perde. Uma sessão que recebe muitos pedidos, como um orquestrador que distribui trabalho a outros agentes, precisa da lista lida de volta do disco.</p>
<h2>O que faz</h2>
<ul>
  <li>No início da sessão, acrescenta uma nota com as tarefas abertas da lista da sessão.</li>
  <li>Em cada prompt seu, anexa as tarefas abertas e as concluídas desde o último prompt. Mensagem de outra sessão, notificação e agendamento não recebem nada.</li>
  <li>Com lista nomeada (<code>CLAUDE_CODE_TASK_LIST_ID</code>), o mesmo prompt leva a regra: pedido novo vira <code>TaskCreate</code> antes de qualquer trabalho, com o dono no assunto, como <code>[dono] o que foi pedido</code>.</li>
  <li>Move a tarefa concluída para <code>~/.local/state/mods/todo/&lt;lista&gt;.jsonl</code> e apaga o arquivo dela, para a lista guardar só o que está aberto. Vale para tarefa concluída pelo <code>TaskUpdate</code> e para arquivo que um script reescreveu.</li>
</ul>
<h2>Ordem da lista</h2>
<p>As tarefas abertas entram num grupo por estado, com a contagem, como <code>espera (2):</code>.</p>
<ul>
  <li>Prioridade e estado vêm de <code>metadata.priority</code> e <code>metadata.state</code> no arquivo da tarefa. Sem metadata, saem de um assunto como <code>[dono] P1 espera: o que foi pedido</code>: o número depois do <code>P</code>, logo após o dono, e a palavra antes dos dois-pontos.</li>
  <li>Tarefa sem estado entra no grupo do status nativo, <code>in_progress</code> ou <code>pending</code>.</li>
  <li>Dentro do grupo, as tarefas vão de P0 para cima, depois as sem prioridade, e então pelo id.</li>
  <li>O grupo da tarefa mais urgente abre. No empate, abre o grupo que tem tarefa em andamento.</li>
</ul>
<h2>Ligue as ferramentas de tarefa</h2>
<p>O Claude Code oferece as ferramentas de tarefa por padrão só no Opus 4.7, no Sonnet 4.6, no Haiku 4.5 e nos modelos anteriores. Num modelo mais novo, abra o Claude Code com a variável. Para dividir uma lista entre sessões, dê nome a ela também:</p>
{code('CLAUDE_CODE_ENABLE_TODO_TOOLS=1 CLAUDE_CODE_TASK_LIST_ID=pedidos claude')}
<h2>Opções</h2>
{opts([('enabled', '<code>true</code>', 'Desligado, o mod não faz nada. Vale na próxima sessão, ou depois de <code>/reload-plugins</code>.'),
    ('remind', '<code>true</code>', 'Com lista nomeada, cada prompt seu leva a regra do pedido.'),
    ('archive', '<code>true</code>', 'Move a tarefa concluída da lista para o histórico. Desligado, a concluída fica na lista.')])}
{diary('todo', 'uma linha por nota, contexto de prompt e arquivamento, mais uma linha <code>session-summary</code>. O histórico, uma linha por tarefa concluída, fica em <code>~/.local/state/mods/todo/&lt;lista&gt;.jsonl</code>.')}
<h2>Custo</h2>
<p>As tarefas abertas vão inteiras em cada prompt seu, uns 15 tokens por tarefa, no máximo 30. O único hook de <code>tool.call</code> é no <code>TaskUpdate</code>.</p>
<h2>Limites</h2>
<ul>
  <li>No plano Team ou Enterprise, o guarda embutido <code>sec-default@builtin</code> ignora o hook <code>session.compact</code> de mod instalado pelo usuário, e a nota logo depois da compactação não aparece. O próximo prompt seu leva a lista. Um hook <code>SessionStart</code> com o matcher <code>compact</code> no <code>settings.json</code> da sessão imprime as tarefas abertas na hora.</li>
  <li>O id das tarefas volta a 1 quando todo arquivo saiu da lista. O histórico guarda o assunto ao lado de cada id.</li>
  <li>Testado só no Linux.</li>
</ul>
{install_one('todo')}
''')

# --- consultar ---
page('Consultar', 'commands', 'term', 'Os comandos do Cockpit', 'Os comandos do Cockpit', f'''
<p class="lead">Todo comando que o Cockpit acrescenta. Cada um também responde em texto simples, então funciona onde nenhuma janela é desenhada, como no Remote Control.</p>
{table(['Comando', 'Mod', 'O que mostra'], [
    ('<code>/panel</code>', '<a href="#panel">panel</a>', 'O endereço da página das sessões e quantas precisam de você. Sobe o servidor se ele não responde. Numa sessão aberta por SSH, imprime também o comando do túnel.'),
    ('<code>/hud</code>', '<a href="#hud">hud</a>', 'A visão completa: sessão, limites, memória, o que roda agora e as ações de hoje.'),
    ('<code>/limit</code>', '<a href="#usage-limit">usage-limit</a>', 'As janelas do plano com as etapas, o estado e o que está guardado para a retomada.'),
    ('<code>/ram</code>', '<a href="#memory-guard">memory-guard</a>', 'A folga de memória por grupo, ou da máquina, e o pico medido de cada comando pesado.'),
    ('<code>/cockpit:setup</code>', 'cockpit', 'Roda o setup de novo, para mudar o estilo ou qualquer outra resposta.'),
], 'stack')}
<h2>Teclas nas janelas</h2>
<p>Numa janela do Cockpit, <code>r</code> atualiza e <code>esc</code> fecha.</p>
<h2>Teclas na página do panel</h2>
<p><code>r</code> gera o resumo de todas as sessões de novo, ou <code>R</code> na Inbox, onde <code>r</code> vai para o campo de resposta. <code>esc</code> fecha o diálogo de envio, depois a gaveta Mods, depois a gaveta do Board. Cada vista tem as próprias teclas, na <a href="#panel">página do panel</a>.</p>
''')

page('Consultar', 'configure', 'sliders', 'Como mudar as opções e desligar um mod', 'Como mudar as opções e desligar um mod', f'''
<p class="lead">Cada opção de mod é uma linha no <code>/config</code>. O setup cuida das poucas configurações que um plugin não grava sozinho.</p>
<h2>Mudar uma opção</h2>
<p>Abra <code>/config</code> e role até o mod. A página de cada mod lista as opções, os padrões e o que fazem. A status line pega a mudança em até 5 segundos; os outros mods, depois de reiniciar o Claude Code ou rodar <code>/reload-plugins</code>.</p>
<h2>No arquivo de configurações</h2>
<p>As mesmas opções ficam em <code>pluginConfigs</code> no <code>~/.claude/settings.json</code>, com a chave <code>&lt;mod&gt;@cockpit</code>. Serve para levar a mesma configuração para outra máquina:</p>
{code(chr(10).join(['{', '  "pluginConfigs": {', '    "hud@cockpit": { "options": { "style": "blocks", "icons": "unicode" } },', '    "usage-limit@cockpit": { "options": { "timeZone": "America/Sao_Paulo" } },', '    "collision-guard@cockpit": { "options": { "git": "note" } }', '  }', '}']), '~/.claude/settings.json')}
<h2>O que o setup grava</h2>
{table(['Configuração', 'Valor', 'Por que'], [
    ('<code>statusLine</code>', 'o script do <code>hud</code>, com <code>refreshInterval: 5</code>', 'Um plugin não desenha embaixo do prompt.'),
    ('<code>spinnerTipsEnabled</code>', '<code>false</code>', 'A linha do <code>spinner-status</code> substitui a dica do Claude Code em vez de ficar embaixo dela.'),
    ('<code>autoCompactWindow</code>', '<code>733000</code> num modelo de 1M, se você escolher', 'O Claude Code resume a conversa em uns 70% em vez de perto do fim.'),
    ('<code>pluginConfigs</code>', '<code>band: "off"</code> no hud, estilo, ícones, fuso', 'As suas respostas ao setup. Com a status line ligada, a faixa desliga para as linhas não aparecerem duas vezes.'),
    ('<code>enabledPlugins</code>', '<code>claude-hud@claude-hud</code> desligado, quando estava ligado', 'A status line dele é a que o hud substitui.'),
    ('<code>pluginConfigs</code>', '<code>enabled: false</code> em cada mod que você desligar, se pedir', 'Só quando você pede ao setup para desligar mods.'),
    ('<code>extraKnownMarketplaces.cockpit</code>', '<code>autoUpdate: true</code>', 'Os mods atualizam sozinhos.'),
], 'stack')}
<h2>Desligar um mod</h2>
<p>Todo mod tem a opção <b>Enabled</b>. Desligue no <code>/config</code>, ou ponha <code>"enabled": false</code> na entrada do mod em <code>pluginConfigs</code>, e abra uma sessão nova ou rode <code>/reload-plugins</code>. Desligado, o mod não registra nenhum hook e não custa nada por chamada. O <code>/cockpit:setup</code> também desliga mods para você.</p>
{code(chr(10).join(['{', '  "pluginConfigs": {', '    "loop-breaker@cockpit": { "options": { "enabled": false } },', '    "memory-guard@cockpit": { "options": { "refuse": false } }', '  }', '}']), '~/.claude/settings.json')}
<h2>Desligar um passo de um guarda</h2>
{table(['Mod', 'Chaves'], [
    ('<a href="#secret-guard"><code>secret-guard</code></a>', '<code>fillCommands</code>'),
    ('<a href="#collision-guard"><code>collision-guard</code></a>', '<code>editWarnings</code>, e <code>git: off</code> para a trava do git'),
    ('<a href="#memory-guard"><code>memory-guard</code></a>', '<code>reduce</code>, <code>wait</code>, <code>refuse</code>, <code>retry137</code>'),
    ('<a href="#loop-breaker"><code>loop-breaker</code></a>', '<code>editCheck</code>, <code>errorCheck</code>, <code>repeatCheck</code>'),
    ('<a href="#usage-limit"><code>usage-limit</code></a>', 'freio, commit e pausa de cada janela, e <code>resume</code>'),
    ('<a href="#skill-loader"><code>skill-loader</code></a>', '<code>holdWrites</code>, <code>diagnoseReminder</code>'),
    ('<a href="#panel"><code>panel</code></a>', '<code>answers</code>, <code>autostart</code>'),
])}
<p>A página de cada mod diz o que cada chave desliga.</p>
<h2>Tirar os hooks de um mod</h2>
<p>O Claude Code recusa desligar um plugin que outro plugin ligado exige, e o pacote <code>cockpit</code> exige todos os mods. Desligue o pacote primeiro e depois o mod:</p>
{code('claude plugin disable cockpit@cockpit' + chr(10) + 'claude plugin disable pipefail@cockpit')}
<p>Os outros mods continuam ligados. Religar o pacote religa o mod.</p>
''')

page('Consultar', 'remote', 'server', 'Como usar numa máquina remota', 'Como usar numa máquina remota', f'''
<p class="lead">Quem roda o Claude Code numa máquina Linux remota por SSH usa os mods do mesmo jeito, e algumas partes fazem mais.</p>
<h2>Abrir a página por túnel</h2>
<p>O <code>panel</code> escuta só no <code>127.0.0.1</code> da máquina onde as sessões rodam. Do seu computador, abra um túnel SSH e acesse <code>http://localhost:7777</code>. Numa sessão aberta por SSH, o <code>/panel</code> imprime esse comando com o nome da máquina.</p>
{code('ssh -N -L 7777:127.0.0.1:7777 <host>', 'no seu computador')}
<p>Para o túnel abrir a cada login SSH, ponha uma linha na entrada da máquina no <code>~/.ssh/config</code> do seu computador:</p>
{code('Host <host>' + chr(10) + '  LocalForward 7777 127.0.0.1:7777', '~/.ssh/config')}
<h2>Rodar a página como serviço</h2>
<p>Em vez de deixar uma sessão subir a página, rode o servidor no systemd. Ponha a opção <code>autostart</code> do <code>panel</code> em <code>false</code> e rode o servidor como unidade:</p>
{code(chr(10).join(['[Service]', 'User=<usuario>', 'ExecStart=/usr/bin/python3 -I /home/<usuario>/.claude/plugins/marketplaces/cockpit/panel/server/panel.py', 'Environment=PANEL_CLAUDE=/home/<usuario>/.local/bin/claude', 'Restart=always']), 'unidade do systemd')}
<p>As variáveis <code>PANEL_PORT</code>, <code>PANEL_MODEL</code> e <code>PANEL_REFRESH_MINUTES</code> definem as opções do servidor. <code>PANEL_GROUPS</code> recebe uma lista de cgroups separados por vírgula, como <code>agents.slice</code>, para a página mostrar esses grupos e tudo embaixo deles.</p>
<h2>Limites de memória</h2>
<p>Com as sessões embaixo de um limite de memória do cgroup v2, como o de um serviço do systemd ou de um container, o <code>memory-guard</code> mantém os comandos pesados dentro do limite mais apertado, o <code>hud</code> mostra o que sobra embaixo dele, o <code>/ram</code> mostra cada grupo e a página mostra a memória de cada grupo e o estado dos serviços.</p>
<h2>Remote Control e tmux</h2>
<p>Todo comando do Cockpit responde também em texto, então funciona quando você conduz a sessão pelo <a href="https://code.claude.com/docs/pt/remote-control" target="_blank" rel="noopener">Remote Control</a>, no claude.ai ou no app do celular, onde nenhuma janela é desenhada. A página liga a sessão ao claude.ai quando ela roda com Remote Control. Para uma sessão em tmux, o botão <b>tmux</b> copia o comando que entra no painel dela.</p>
''')

page('Consultar', 'data', 'shield', 'O que sai da sua máquina', 'O que sai da sua máquina', f'''
<p class="lead">O Cockpit roda dentro do Claude Code, na sua máquina. Dois mods mandam um trecho da sessão para um modelo pela sua própria conta. O resto fica local.</p>
<h2>O que sai</h2>
{table(['Mod', 'Manda', 'Quando'], [
    ('<code>panel</code>', 'Um trecho da conversa de cada sessão, pelo <code>claude -p</code>, para o <code>sonnet</code> por padrão', 'No <b>Refresh</b>, quando uma sessão para depois de um turno, e a cada 5 minutos para sessão que mudou'),
    ('<code>spinner-status</code>', 'Os últimos prompts e o último texto do agente, no máximo 3.000 caracteres, para o Haiku', 'Uma vez por turno, ou nunca no modo <code>tips</code>'),
    ('<code>hud</code>', 'Um <code>gh pr view</code> da branch atual, para o GitHub', 'No máximo uma vez por minuto, com o <code>gh</code> instalado'),
], 'stack')}
<p>Essas chamadas usam a mesma conta e os mesmos termos de dados do resto da sua sessão do Claude Code. Nenhum outro mod chama modelo.</p>
<h2>O que fica</h2>
<ul>
  <li>Todo mod grava um diário em <code>~/.local/state/mods/&lt;mod&gt;/</code>, uma linha por ação e um resumo por sessão. Um diário nunca guarda valor de segredo nem conteúdo de arquivo.</li>
  <li>O <code>collision-guard</code> guarda a lista de arquivos que cada sessão editou. Sessão encerrada marca o registro, e registro mais velho que <code>expireHours</code> (24 horas por padrão) sai quando uma sessão começa.</li>
  <li>O <code>secret-guard</code> mantém os valores de segredo só na memória, nunca em disco.</li>
  <li>O <code>panel</code> guarda o último resumo de cada sessão. A página não tem login e escuta só no <code>127.0.0.1</code>. Quem chega nessa porta lê a página e digita nas suas sessões, então não exponha.</li>
</ul>
''')

TROUBLE = [
    ('A status line não aparece, ou só muda quando chega mensagem', 'Falta o <code>statusLine</code> nas configurações, ou falta o <code>refreshInterval</code>. Rode <code>/cockpit:setup</code> de novo e reinicie o Claude Code.'),
    ('A status line não mostra nada', 'O script precisa do Node 22.18 ou mais novo. Rode <code>node --version</code> e atualize o Node se for mais velho.'),
    ('Os ícones aparecem como caixas ou interrogações', 'A fonte do terminal não tem os glifos da Nerd Font. Ponha <code>icons</code> em <code>unicode</code> no <code>hud</code> pelo <code>/config</code>, ou instale uma Nerd Font e escolha ela no terminal.'),
    ('As barras parecem um borrão só', 'Algumas fontes desenham os glifos da barra colados. Ponha <code>bar</code> em <code>dots</code> ou <code>squares</code> no <code>hud</code>.'),
    ('Aparecem duas linhas embaixo do spinner', 'A dica do Claude Code continua ligada. Ponha <code>"spinnerTipsEnabled": false</code> nas configurações, ou rode o setup de novo.'),
    ('Um mod aparece como <code>failed to load</code> no <code>claude plugin list</code>', 'A cópia do marketplace e a versão instalada estão fora de passo. Rode <code>claude plugin marketplace update cockpit</code>, depois <code>claude plugin update cockpit@cockpit</code>, e reinicie.'),
    ('As opções dos mods sumiram', 'Remover um marketplace apaga as opções salvas dos plugins dele. Rode <code>/cockpit:setup</code> de novo para gravar.'),
    ('O <code>global-memory</code> não faz nada no plano Team ou Enterprise', 'Esses planos ignoram plugin instalado pelo usuário nos hooks de que ele precisa. Ele tem de entrar como plugin da organização; a <a href="#global-memory">página dele</a> mostra as managed settings.'),
    ('O <code>/panel</code> diz que o servidor não está rodando', 'O servidor sobe quando uma sessão começa, a não ser que <code>autostart</code> esteja desligado. Confira que o Python 3.9 ou mais novo está instalado como <code>python3</code>, <code>python</code> ou <code>py</code> e que o <code>curl</code> roda, e abra uma sessão nova. Os erros do servidor ficam em <code>~/.local/state/mods/panel/server.log</code>.'),
    ('A página deixa as opções de uma sessão em cinza', 'A sessão não conferiu a caixa de entrada nos últimos 15 segundos, quase sempre porque carregou um mod <code>panel</code> antigo. Rode <code>/reload-plugins</code> nela.'),
    ('A gaveta Mods não mostra memória por grupo nem serviços', 'É o esperado no macOS e no Windows. A página só mostra memória por grupo para cgroup v2 com limite, e serviço só com systemd.'),
    ('O <code>/ram</code> diz que não há leitura de memória', 'O <code>memory-guard</code> não achou o <code>/proc/meminfo</code> e o comando do sistema falhou: <code>sysctl</code> e <code>vm_stat</code> no macOS, PowerShell no Windows, ausente ou mais lento que o limite de tempo. Até uma leitura funcionar, os comandos pesados rodam como vieram.'),
    ('Um comando git foi recusado com uma lista de arquivos', 'O <code>collision-guard</code> segurou, porque outra sessão da máquina tem edição não commitada no mesmo repo, embaixo dos caminhos que o comando nomeia. Nomeie só os seus arquivos, ou rode o mesmo comando de novo em até 2 minutos.'),
]
page('Consultar', 'troubleshooting', 'warn', 'Algo quebrou? A solução está aqui', 'Algo quebrou? A solução está aqui',
     '<p class="lead">Os problemas mais comuns e a solução de cada um.</p>' + table(['Sintoma', 'Solução'], TROUBLE, 'stack'))

page('Consultar', 'update', 'upload', 'Como atualizar e desinstalar', 'Como atualizar e desinstalar', f'''
<p class="lead">A atualização chega sozinha uns minutos depois da primeira mensagem de uma sessão. Dá para atualizar à mão e remover tudo com dois comandos.</p>
<h2>Atualização automática</h2>
<p>O setup liga a atualização automática do marketplace <code>cockpit</code>. O Claude Code atualiza o marketplace uma vez por sessão e cada mod com versão nova, um por um. A sessão aberta fica com as versões que carregou até você rodar <code>/reload-plugins</code>; a próxima sessão já carrega as novas.</p>
<h2>Atualizar à mão</h2>
<p>Atualizar o pacote não atualiza os mods, porque cada mod é um plugin. Para atualizar todos agora:</p>
{code(UPDATE_ALL)}
<p>Para um mod só, nomeie: <code>claude plugin update hud@cockpit</code>.</p>
<p>Mod novo numa versão não chega com a atualização: o pacote passa a listá-lo como dependência faltando. Instale pelo nome, como <code>claude plugin install todo@cockpit</code> na 1.4.0.</p>
<h2>Desinstalar</h2>
{code('claude plugin uninstall cockpit@cockpit' + chr(10) + 'claude plugin prune')}
<p>Desinstalar o pacote deixa os mods instalados; o <code>claude plugin prune</code> remove. O setup gravou <code>statusLine</code>, <code>spinnerTipsEnabled</code> e <code>autoCompactWindow</code> nas suas configurações e guardou um backup ao lado. Tire essas chaves à mão, ou volte o backup.</p>
<h2>Apagar os dados</h2>
<p>Os mods deixam os diários em <code>~/.local/state/mods/</code>. Apague essa pasta para remover tudo que o Cockpit gravou.</p>
''')

page('Consultar', 'versions', 'tag', 'Versões', 'Versões', f'''
<p class="lead">Cockpit {VERS['cockpit']}. O pacote leva a versão do lançamento, e cada mod leva a versão do lançamento em que mudou pela última vez.</p>
<p>Um mod que não mudou num lançamento mantém a versão, então o Claude Code não atualiza ele à toa.</p>
''' + table(['Mod', 'Versão'], [('<code>cockpit</code> (pacote)', VERS['cockpit'])] + [(f'<a href="#{m}"><code>{m}</code></a>', VERS[m]) for m in ORDER]) + '''
<h2>O que mudou</h2>
<ul>
  <li><b>1.5.0</b>: o <code>todo</code> lista as tarefas abertas num grupo por estado, cada um ordenado por prioridade, a partir do metadata da tarefa ou de um assunto como <code>[dono] P1 espera: o que foi pedido</code>.</li>
  <li><b>1.4.0</b>: mod novo <code>todo</code>, que mantém a lista de tarefas nativa na frente do agente.</li>
  <li><b>1.3.0</b>: todo mod ganhou a opção <code>enabled</code>, e os guardas ganharam uma chave por passo. O <code>/cockpit:setup</code> desliga mods.</li>
  <li><b>1.2.0</b>: o <code>usage-limit</code> passou a cuidar de cada janela por conta própria, com freio, commit e pausa separados para 5 horas e 7 dias, cada um com chave e porcentagem.</li>
  <li><b>1.1.0</b>: o <code>secret-guard</code> passou a ler a pasta de segredos ao lado do arquivo de segredos.</li>
</ul>
''')


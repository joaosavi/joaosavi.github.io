# `collision-guard`

Avisa quando duas sessões da mesma máquina mexem nos mesmos arquivos, e segura uma vez o comando git que levaria junto a edição não commitada da outra sessão.

## Por que

Rodar várias sessões ao mesmo tempo é comum, e duas delas caem no mesmo repo com frequência. Na máquina Linux do autor, 11 pares de sessões editaram o mesmo repo com menos de 30 minutos de diferença em 8 dias, e 5 desses pares editaram o mesmo arquivo. O Edit do Claude Code já recusa um arquivo que mudou depois da leitura, então uma sessão não sobrescreve a outra em silêncio. O que ele não pega é o git: `git add -A` ou `git commit -a` numa sessão leva a edição pela metade da outra, e `git stash`, `checkout` ou `reset --hard` move ou descarta essa edição.

## O que faz

- Cada sessão mantém um registro em `~/.local/state/mods/collision-guard/sessions/<sessão>.json` com os arquivos que editou. Só ela escreve nele.
- Depois de uma edição, quando outra sessão viva também editou o arquivo e o git ainda mostra a mudança dela, o agente lê uma nota com o nome da sessão e há quanto tempo, e você vê um aviso. Fora de repo git, a outra edição vale por `windowMinutes`. Cada edição da outra sessão avisa uma vez.
- Antes de um comando git que faria stage, commit, stash, troca de branch ou descarte da edição não commitada de outra sessão, o mod segura o comando e lista os arquivos. O agente pode nomear só os arquivos dele, ou rodar o mesmo comando de novo em até 2 minutos para passar.
- Lê o `cd` do começo da linha e o `git -C <pasta>` para achar o repo. Texto entre aspas, como a mensagem de commit, não conta como comando.
- Um comando que nomeia caminhos, como `git add -A mods/` ou `git checkout -- src/a.ts`, só é segurado pelas edições da outra sessão embaixo desses caminhos. Curinga ou `:/` conta como o repo inteiro.
- Sessão encerrada marca o registro, e registro mais velho que `expireHours` sai quando uma sessão começa.

## Opções

| Opção | Padrão | O que faz |
| --- | --- | --- |
| `enabled` | `true` | Desligado, o mod não faz nada: nada é registrado, nada avisa, nenhum git é segurado. Vale na próxima sessão, ou depois de `/reload-plugins`. |
| `git` | `confirm` | `confirm` segura uma vez o comando git arriscado. `note` deixa rodar e avisa o agente depois. `off` não mexe em comando git. |
| `windowMinutes` | `30` | Por quanto tempo a edição de outra sessão num arquivo fora de repo git ainda conta. Dentro de um repo, conta enquanto o git mostrar o arquivo como mudado. |
| `expireHours` | `24` | Sessão calada por esse tempo conta como encerrada, e o registro dela sai. |
| `editWarnings` | `true` | Avisa o agente, com um aviso na tela, quando outra sessão editou o mesmo arquivo. Desligado, as edições continuam registradas, então as outras sessões e a trava do git ainda as veem. |

## O que grava

`~/.local/state/mods/collision-guard/<dia>-<sessão>.jsonl`: uma linha por aviso (`edit-warned`, `git-held`, `git-confirmed`, `git-noted`) com a operação git e quantos arquivos, nunca o conteúdo, mais uma linha `session-summary`. Cada linha tem `at`, `session` e `event`.

## Custo

Chamada que não é edição nem git não custa nada mensurável. Uma edição lê os registros das outras sessões e roda `git rev-parse` uma vez por pasta; quando outra sessão editou o mesmo arquivo, roda também `git status` nele. No primeiro teste real, a edição que achou colisão levou 444 ms de hook, e as outras menos de 60 ms (7 chamadas, outubro de 2026).

## Limites

- As sessões precisam dividir a máquina e a pasta home. Sessão em outro computador, ou num container com home própria, não aparece.
- Arquivo mudado por comando Bash (`sed -i`, um script, um formatador) não conta como edição. Só Edit, Write, MultiEdit e NotebookEdit contam.
- `git checkout <nome>` lê igual com branch ou arquivo, então a nota diz "para outra branch ou uma versão antiga".
- Testado só no Linux. No Windows, os caminhos são comparados com barra normal, como o git imprime, e comando git pela ferramenta PowerShell é conferido como no Bash. Um `cd` para caminho do Git Bash como `/c/work` não é seguido.

## Instalar só este mod

O pacote `cockpit` já instala o `collision-guard` com os outros. Para ter só ele:

terminal:

```
claude plugin marketplace add joaosavi/cockpit
claude plugin install collision-guard@cockpit
```

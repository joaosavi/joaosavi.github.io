# `secret-guard`

Esconde o valor de todo segredo na saída das ferramentas antes de o agente ler.

## Por que

Um segredo que chega à conversa vai para o modelo e fica no log da sessão, e a partir daí precisa ser trocado. A saída de ferramenta vaza segredo fácil: `env`, `cat .env`, um stack trace com string de conexão. O mod troca cada valor por `<hidden:NOME>` em todo resultado de ferramenta, nativa, de MCP ou de subagente.

## O que faz

- Os valores vêm do arquivo de segredos e de todo arquivo na pasta ao lado com o mesmo nome mais `.d` (`~/.secrets.d/` por padrão), de todo `.env*` embaixo da raiz de `.env` (5 níveis), quando você define uma, de variável de ambiente com nome de segredo (`TOKEN`, `SECRET`, `PASSWORD`, `KEY`, `AUTH` e outros) e da senha de toda URL `esquema://usuario:senha@`.
- Formatos conhecidos ficam escondidos mesmo fora de qualquer lista: GitHub, Anthropic, OpenAI, AWS, Google, Stripe, Slack, JWT e bloco de chave privada. Aparecem como `<hidden:github>`, `<hidden:jwt>` e assim por diante.
- Uma ferramenta que entrega segredo, como a CLI de um cofre de senhas, pode manter a própria lista `NOME="valor"` num arquivo da pasta de segredos sem mexer no seu arquivo. Arquivo com nome começando por ponto é ignorado, para a ferramenta gravar um temporário e renomear.
- Um valor que também aparece num arquivo `.example` já é público e continua visível.
- Quando o agente escreve `<hidden:NOME>` num `.env` ou no arquivo de segredos, o mod grava o valor real no lugar. O agente edita esses arquivos sem nunca ver um valor.
- Quando o agente escreve `<hidden:NOME>` num comando Bash, o mod roda o comando com o valor real, e a saída volta escondida. A conversa guarda o comando como foi escrito. O agente chama uma API com um token que nunca viu.
- Um marcador que o mod não consegue preencher barra o comando: um token conhecido só pelo formato, ou um nome com dois valores diferentes nos seus arquivos, como o mesmo `DATABASE_URL` em dois projetos. O agente recebe a instrução de ler o valor dentro do comando, da variável ou do `.env`.
- Se o próprio mod falha, ele retém a saída em vez de deixar passar sem conferir.

## Opções

| Opção | Padrão | O que faz |
| --- | --- | --- |
| `enabled` | `true` | Desligado, o mod não faz nada: todo valor aparece na saída como é. Vale na próxima sessão, ou depois de `/reload-plugins`. |
| `secretsFile` | `~/.secrets` | Arquivo `CHAVE=valor` em que todo valor é segredo, qualquer que seja o nome. |
| `envRoot` | vazio | Pasta onde procurar arquivos `.env`, 5 níveis abaixo. Vazio não procura nenhum. |
| `minLength` | `12` | Valor mais curto fica de fora, menos formato conhecido e valor dos arquivos de segredos. |
| `fillCommands` | `true` | Roda o comando Bash que nomeia `<hidden:NAME>` com o valor real. Desligado, esse comando não roda, e o agente recebe a instrução de ler o valor dentro do comando. |

Por padrão o mod não lê nenhum `.env`. Para cobrir os `.env` dos seus projetos, aponte `envRoot` para a pasta dos repos, como `~/code`. O mod varre a pasta ao começar, procura `.env` novo no máximo uma vez por minuto e refaz a lista pelo menos a cada 10 minutos.

## O que grava

`~/.local/state/mods/secret-guard/<dia>-<sessão>.jsonl`: uma linha a cada lista refeita (com o tempo que levou), resultado escondido, marcador devolvido ou preenchido num comando e comando barrado, só com nome de segredo e contagem, mais uma linha `session-summary`. Os valores vivem só na memória do mod, nunca em disco. Cada linha tem `at`, `session` e `event`.

## Custo

O hook somou uns 64 ms por chamada de ferramenta na máquina Linux do autor (60 chamadas medidas em outubro de 2026, estimativa), com `envRoot` numa pasta de uns 140 subdiretórios. A maior parte é conferir se um arquivo de origem mudou.

## Limites

- Um segredo mais curto que `minLength` e fora de formato conhecido fica visível. Valor do arquivo de segredos ou da pasta dele é escondido a partir de 6 caracteres, porque um cofre entrega senha de 8 a 11; abaixo de 6 é PIN ou palavra, e esconder embaralharia saída comum.
- Um segredo que o agente viu antes de o mod carregar continua na conversa.
- Um `.env` fora do `envRoot` não é lido, e os valores dele ficam visíveis se nenhuma outra fonte tiver.
- Preencher um marcador num comando deixa o agente usar o segredo, inclusive mandar para um servidor. Ele não faz mais do que já faria com `source .env`, mas o comando roda sem pedir permissão própria.
- Os marcadores só são preenchidos em comando Bash. No Windows sem Git Bash, um comando PowerShell com marcador roda como foi escrito. A saída de toda ferramenta continua escondida.
- Testado só no Linux. Os caminhos do macOS e do Windows têm teste unitário com ambiente simulado.

## Instalar só este mod

O pacote `cockpit` já instala o `secret-guard` com os outros. Para ter só ele:

terminal:

```
claude plugin marketplace add joaosavi/cockpit
claude plugin install secret-guard@cockpit
```

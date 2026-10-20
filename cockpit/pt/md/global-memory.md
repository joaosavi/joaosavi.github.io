# `global-memory`

Acrescenta uma pasta de memória da máquina ao lado da memória automática de cada projeto, para o que vale na máquina chegar a toda sessão, de qualquer pasta.

## Por que

A memória automática do Claude Code é por projeto. Um fato da máquina, como onde uma ferramenta mora ou como se chega num serviço, salvo na memória de um projeto falta em todos os outros. O mod cria uma pasta global que toda sessão lê e diz ao agente que memória vai para lá.

## O que faz

- Reescreve a seção de memória do prompt de sistema para descrever as duas pastas e onde vai cada tipo: `user` e `feedback` vão para a global por padrão, `reference` vai para a global quando é sobre a máquina, e `project` fica sempre no projeto.
- Põe o `MEMORY.md` global nos arquivos de instrução, então o índice dele chega a toda sessão como o do projeto.
- Respeita o modo do Claude Code. Com memória só de leitura, a pasta global também fica só de leitura. Com memória automática desligada, ou sem a pasta global ou o `MEMORY.md` dela, o mod não muda nada.

## Ligar

O mod não cria nada. Crie a pasta e um `MEMORY.md` vazio, e ele começa na próxima sessão:

terminal:

```
mkdir -p ~/.claude/global-memory && touch ~/.claude/global-memory/MEMORY.md
```

`globalDir` pode apontar para uma pasta dentro de um repo git, como `~/dotfiles/memory`, para as memórias terem versão e irem com você para outra máquina.

>  **Nada de credencial** Toda sessão da máquina lê a pasta global. Nunca salve senha ou chave lá.

## No plano Team ou Enterprise

O guarda embutido `sec-default@builtin` ignora mod instalado pelo usuário em `prompt.section` e `prompt.context`, os dois eventos de que este mod precisa. Liste ele em `prependPlugins` nas managed settings, antes do guarda, para contar como mod da organização:

managed settings:

```
{
  "enabledPlugins": { "global-memory@cockpit": true },
  "prependPlugins": ["global-memory@cockpit", "sec-default@builtin"]
}
```

No plano pessoal funciona como instalado; no Team ou Enterprise não faz nada até essas configurações entrarem.

## Opções

| Opção | Padrão | O que faz |
| --- | --- | --- |
| `enabled` | `true` | Desligado, o mod não faz nada: a seção de memória fica como o Claude Code escreveu. Vale na próxima sessão, ou depois de `/reload-plugins`. |
| `globalDir` | `~/.claude/global-memory` | Pasta da memória da máquina, com o próprio `MEMORY.md`. |

## O que grava

`~/.local/state/mods/global-memory/<dia>-<sessão>.jsonl`: uma linha a cada seção de memória reescrita, índice global acrescentado ou vez que o mod se afastou e por quê, mais uma linha `session-summary`. Cada linha tem `at`, `session` e `event`.

## Custo

Nenhum por chamada de ferramenta: o mod não tem hook de `tool.call`. Ele lê o `MEMORY.md` global quando o prompt de sistema e o primeiro contexto são montados. O texto reescrito depende só da entrada, então o cache do prompt continua valendo.

## Limites

- A reescrita casa com o texto da seção de memória que o Claude Code 2.1.292 manda. Um texto diferente fica como está e entra no diário como `skipped-unrecognized`.
- Testado só no Linux.

## Instalar só este mod

O pacote `cockpit` já instala o `global-memory` com os outros. Para ter só ele:

terminal:

```
claude plugin marketplace add joaosavi/cockpit
claude plugin install global-memory@cockpit
```

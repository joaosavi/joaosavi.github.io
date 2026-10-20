# O que sai da sua máquina

O Cockpit roda dentro do Claude Code, na sua máquina. Dois mods mandam um trecho da sessão para um modelo pela sua própria conta. O resto fica local.

## O que sai

| Mod | Manda | Quando |
| --- | --- | --- |
| `panel` | Um trecho da conversa de cada sessão, pelo `claude -p`, para o `sonnet` por padrão | No **Refresh**, quando uma sessão para depois de um turno, e a cada 5 minutos para sessão que mudou |
| `spinner-status` | Os últimos prompts e o último texto do agente, no máximo 3.000 caracteres, para o Haiku | Uma vez por turno, ou nunca no modo `tips` |
| `hud` | Um `gh pr view` da branch atual, para o GitHub | No máximo uma vez por minuto, com o `gh` instalado |

Essas chamadas usam a mesma conta e os mesmos termos de dados do resto da sua sessão do Claude Code. Nenhum outro mod chama modelo.

## O que fica

- Todo mod grava um diário em `~/.local/state/mods/<mod>/`, uma linha por ação e um resumo por sessão. Um diário nunca guarda valor de segredo nem conteúdo de arquivo.
- O `collision-guard` guarda a lista de arquivos que cada sessão editou. Sessão encerrada marca o registro, e registro mais velho que `expireHours` (24 horas por padrão) sai quando uma sessão começa.
- O `secret-guard` mantém os valores de segredo só na memória, nunca em disco.
- O `panel` guarda o último resumo de cada sessão. A página não tem login e escuta só no `127.0.0.1`. Quem chega nessa porta lê a página e digita nas suas sessões, então não exponha.



# Esta máquina é o computador da pessoa

Esta sessão roda no computador da pessoa, aberta pelo orquestrador com `agent start --host`, e não
no servidor. O resto deste arquivo vem do servidor, e nele vale tudo menos o que esta seção corrige.

- O computador não tem o slice dos agentes nem teto por agente. Ele roda um agente por vez: suíte
  de teste e typecheck pesados rodam com um processo só.
- Ferramentas e serviços que só existem no servidor, peça ao orquestrador por `SendMessage`.
- Credencial só existe aqui quando o orquestrador abriu o agente com `--env`, que copia os `.env` do
  projeto e os apaga no `agent stop`. Não peça senha nem cole credencial na conversa.
- O repo fica no mesmo caminho relativo ao home que no servidor, clonado do GitHub. Commit e push
  saem daqui.

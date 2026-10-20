# Como atualizar e desinstalar

A atualização chega sozinha uns minutos depois da primeira mensagem de uma sessão. Dá para atualizar à mão e remover tudo com dois comandos.

## Atualização automática

O setup liga a atualização automática do marketplace `cockpit`. O Claude Code atualiza o marketplace uma vez por sessão e cada mod com versão nova, um por um. A sessão aberta fica com as versões que carregou até você rodar `/reload-plugins`; a próxima sessão já carrega as novas.

## Atualizar à mão

Atualizar o pacote não atualiza os mods, porque cada mod é um plugin. Para atualizar todos agora:

terminal:

```
claude plugin marketplace update cockpit
for m in $(claude plugin list | grep -o '[a-z-]*@cockpit'); do claude plugin update "$m"; done
```

Para um mod só, nomeie: `claude plugin update hud@cockpit`.

## Desinstalar

terminal:

```
claude plugin uninstall cockpit@cockpit
claude plugin prune
```

Desinstalar o pacote deixa os mods instalados; o `claude plugin prune` remove. O setup gravou `statusLine`, `spinnerTipsEnabled` e `autoCompactWindow` nas suas configurações e guardou um backup ao lado. Tire essas chaves à mão, ou volte o backup.

## Apagar os dados

Os mods deixam os diários em `~/.local/state/mods/`. Apague essa pasta para remover tudo que o Cockpit gravou.

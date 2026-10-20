# `memory-guard`

Mantém typecheck, build, teste e Playwright dentro do limite de memória, e repete com um processo só o comando morto com exit 137. No Linux, o limite é o cgroup mais apertado ou a memória da máquina; no macOS e no Windows, a memória da máquina.

## Por que

No Linux, quando a memória acaba ou um cgroup bate no `memory.max`, o kernel mata o maior processo, que quase sempre é o comando pesado, e o agente vê exit 137 sem saber por quê. O mod confere a folga antes do comando pesado e adapta o comando a ela.

## O que faz

Antes de um comando pesado, o mod compara o pico esperado com a folga, menos a margem. A folga é a memória disponível da máquina, ou o que sobra embaixo do limite de cgroup mais apertado quando a sessão roda num, como num serviço do systemd ou num container:

- **Cabe** Roda como veio.
- **Só cabe um processo** O mod põe `--concurrency=1`, `--workers=1` ou `--maxWorkers=1` e avisa o agente.
- **Não cabe nada** Espera até `waitSeconds` a memória liberar.
- **Não liberou** Recusa o comando e diz ao agente o que está usando a memória.

Depois do comando, o mod guarda o pico medido para a próxima estimativa e repete com um processo o comando que morreu com exit 137. Até medir um comando, as estimativas são 1 GB para typecheck e build, 600 MB para teste e 500 MB para Playwright.

Sem limite de cgroup, como na maioria dos desktops e notebooks Linux, a folga é o `MemAvailable` do `/proc/meminfo`. No macOS são as páginas livres, inativas, especulativas e purgáveis do `vm_stat` contra o total de `sysctl -n hw.memsize`. No Windows é o `FreePhysicalMemory` contra o `TotalVisibleMemorySize`, lidos pelo PowerShell. Com limite de cgroup, conta o working set: `memory.current` menos `inactive_file`, que o kernel libera antes de matar alguém.

## Comandos

`/ram` mostra a folga, o uso e os limites de cada cgroup quando há, e os picos medidos. Diz que não há leitura quando o sistema não dá nenhuma. No terminal abre também a janela Memory, com uma barra por cgroup e a marca do alto, atualizado a cada 2 segundos. `r` atualiza e `esc` fecha.

## Opções

| Opção | Padrão | O que faz |
| --- | --- | --- |
| `margin` | `2` | Porcentagem de memória mantida livre: do `memory.max` de cada cgroup, ou do total da máquina sem limite de cgroup. A marca do alto só conta para cgroup sem max. |
| `waitSeconds` | `120` | Quanto tempo um comando pesado espera memória antes de ser recusado. |

## O que grava

- `~/.local/state/mods/memory-guard/<dia>-<sessão>.jsonl`: uma linha por comando reduzido, recusado ou repetido e por pico medido, mais uma linha `session-summary` com o tempo que os comandos esperaram.
- Os últimos 3 picos medidos de cada comando, no armazenamento comum dos mods, em `peaks`.

## Custo

O hook somou uns 4 ms por chamada Bash na máquina Linux do autor, sem contar a espera por memória (56 chamadas medidas em outubro de 2026, estimativa). Cada comando pesado lê os arquivos de memória uma vez por segundo enquanto roda, para medir o pico. No macOS e no Windows a leitura roda um comando e vale por 10 segundos: `sysctl` e `vm_stat` levam poucos milissegundos, e o PowerShell cerca de um segundo para abrir (estimativa).

## Limites

- O pico é medido no cgroup inteiro, ou na máquina sem cgroup, então outra sessão começando junto infla a medida. Guardar só as 3 últimas deixa a inflada envelhecer.
- O `tsc` não tem flag de processo único, então typecheck que não cabe espera ou é recusado.
- Comando em segundo plano volta na hora e não dá medida.
- As leituras do macOS e do Windows foram testadas só contra saída simulada de `vm_stat`, `sysctl` e PowerShell. Ali a folga é da máquina inteira, sem limite por sessão, e a leitura pode ter até 10 segundos.
- Quando a leitura falha, o comando pesado roda como veio, nada espera nem é recusado e nenhum pico é guardado. `/ram` diz que não há leitura. A repetição com um processo depois de exit 137 continua valendo.

## Instalar só este mod

O pacote `cockpit` já instala o `memory-guard` com os outros. Para ter só ele:

terminal:

```
claude plugin marketplace add joaosavi/cockpit
claude plugin install memory-guard@cockpit
```

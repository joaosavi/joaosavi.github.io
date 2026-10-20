"""The English pages of the Cockpit docs. The text follows the READMEs of the joaosavi/cockpit repo."""
import lib
from lib import *

TITLE = 'Cockpit for Claude Code'
DESCRIPTION = 'The 11 Cockpit mods for Claude Code: guards that catch an agent\'s mistakes, and instruments that show where every session stands.'
LLMS_INTRO = 'Each page below is a Markdown file. To install: `claude plugin marketplace add joaosavi/cockpit` and `claude plugin install cockpit@cockpit`, then restart Claude Code and run `/cockpit:setup`.'
FULL_LABEL = 'Every page in one file'
OTHER_LABEL = 'Versão em português'
GROUPS = [('Get started', 'zap', False), ('Guards', 'shield', True), ('Instruments', 'gauge', True), ('Memory', 'db', False), ('Reference', 'search', True)]
MOD_GROUPS = ('Guards', 'Instruments', 'Memory')

P = []  # (group, id, icon, sidebar label, title, html)

def page(group, pid, icon, label, title, body):
    P.append((group, pid, icon, label, title, body))

MODS = [
    ('Guards', [
        ('secret-guard', 'lock', 'Replaces every secret value in tool output with <code>&lt;hidden:NAME&gt;</code> before the agent reads it, and writes the real value back when the agent edits a <code>.env</code> file.', None),
        ('collision-guard', 'branch', 'Warns when another session on this machine edited the same file, and holds a git command once when it would take that session\'s uncommitted edits along.', None),
        ('pipefail', 'funnel', 'Adds <code>set -o pipefail;</code> to a test, typecheck or lint run piped into <code>tail</code>, <code>head</code> or <code>grep</code>, so a failed run cannot exit 0.', None),
        ('memory-guard', 'mem', 'Keeps typecheck, build, test and Playwright runs under the memory limit: as written, with one process, after a wait, or refused. Reruns a command killed with exit 137 with one process.', '/ram'),
        ('loop-breaker', 'loop', 'Tells the agent to stop and change approach when it repeats the same error, the same fix or the same call.', None),
        ('usage-limit', 'gauge', 'Limits each plan window on its own: one subagent at a time, a work-in-progress commit, a pause that keeps a reserve for you, and a resume when the window resets.', '/limit'),
    ]),
    ('Instruments', [
        ('hud', 'hud', 'Model, project, git branch and PR, context window, plan limits and memory, in a status line under the prompt. Four styles.', '/hud'),
        ('spinner-status', 'spinner', 'Replaces the tip under the spinner with one line from Haiku: where the session stands, or a tip about these mods.', None),
        ('panel', 'grid', 'A local web page with a card for every session on this machine: its state, what it needs from you, the tool running now and the next step.', '/panel'),
        ('skill-loader', 'book', 'Delivers the right skill when the agent touches a matching file or writes a commit, and reminds it to diagnose before fixing when you paste an error.', None),
    ]),
    ('Memory', [
        ('global-memory', 'globe', 'Adds a machine-wide memory folder beside the per-project memory, so facts about the machine reach every session.', None),
    ]),
]

def modgrid(group):
    return lib.modgrid(dict(MODS)[group])

page('Get started', 'start', 'rocket', 'Quickstart', 'Quickstart', f'''
<p class="lead">Cockpit is a bundle of 11 mods for <a href="https://claude.com/product/claude-code" target="_blank" rel="noopener">Claude Code</a>. The guards stop an agent's mistake before it costs you: a secret in tool output, a pipe that hides a failed test, a build killed by the memory limit, a commit that sweeps in another session's edits. The instruments show where the session stands, under the prompt, under the spinner, and on a page with every session on the machine.</p>
<pre id="install-text" hidden>{INSTALL}</pre>
<ol class="quick">
  <li><span class="q-n">1</span><div><b>Install the bundle</b><p>In a terminal, add the marketplace and install <code>cockpit</code>. It brings the 11 mods as dependencies.</p><button type="button" class="q-copy" data-copy-target="install-text">Copy the commands</button> <a class="q-go" href="#install">See every install step</a></div></li>
  <li><span class="q-n">2</span><div><b>Restart and run the setup</b><p>Restart Claude Code and type <code>/cockpit:setup</code>. It asks four questions with previews, writes the status line, the spinner tip and when to compact, and keeps a backup of the file it changed.</p><a class="q-go" href="#install">See what the setup asks</a></div></li>
  <li><span class="q-n">3</span><div><b>Work as usual</b><p>The guards stay quiet until they act. Type <code>/panel</code> for the address of the session page, and <code>/limit</code> for the plan limits.</p><a class="q-go" href="#first-session">What changes in your first session</a></div></li>
</ol>

<h2>What it looks like</h2>
{term(SPINNER + chr(10) + chr(10) + PROMPT + chr(10) + statusline('refined'))}
<p class="figcap">A turn in progress: the <code>spinner-status</code> line, the prompt, and the <code>hud</code> status line in the <code>refined</code> style. Real output from the mods.</p>

<h2>Guards</h2>
<p>Stop a mistake before it lands.</p>
{modgrid('Guards')}
<h2>Instruments</h2>
<p>Show where the session stands.</p>
{modgrid('Instruments')}
<h2>Memory</h2>
{modgrid('Memory')}

<h2>Requirements</h2>
<ul>
  <li>Claude Code 2.1.287 or later, on macOS, Windows or Linux. Mods use Claude Code's function hooks, which are in early access and may change between releases.</li>
  <li>Node 22.18 or later, for the status line script.</li>
  <li>Python 3.9 or later and <code>curl</code>, for the <code>panel</code> page. macOS and Windows 10 or later ship <code>curl</code>.</li>
  <li>A <a href="https://www.nerdfonts.com/" target="_blank" rel="noopener">Nerd Font</a> in your terminal, for the status line icons. Without one, choose the plain icons during setup.</li>
</ul>
<p>The status line, the spinner line and the panes are part of Claude Code's terminal interface. Run <code>claude</code> in a terminal: Terminal or iTerm on macOS, Windows Terminal or PowerShell on Windows, or the terminal panel of VS Code or JetBrains. The mods are not tested in the Desktop app or in the chat panel of the IDE extensions.</p>
''')

page('Get started', 'install', 'download', 'Install and set up', 'Install and set up', f'''
<p class="lead">Two commands in a terminal, a restart, and a setup with four questions. It takes about five minutes.</p>
<h2>Install</h2>
<ol class="steps">
  <li><b>Add the marketplace and install the bundle</b>{code(INSTALL)}<p>The second command lists the mods it installs, as <code>+ 11 dependencies</code>.</p></li>
  <li><b>Restart Claude Code</b><p>The new session loads the mods. A session that was already open picks them up with <code>/reload-plugins</code>.</p></li>
  <li><b>Run the setup</b>{code('/cockpit:setup', 'inside Claude Code')}<p>A plugin cannot write the status line, the spinner tip or when to compact by itself, because they live in your <code>settings.json</code>. The setup writes them, keeps a backup of the file it changed, and tells you what you will notice.</p></li>
</ol>

<h2>What the setup asks</h2>
{table(['Question', 'Options'], [
    ('Status line style', '<code>refined</code> (recommended), <code>blocks</code>, <code>minimal</code> or <code>compact</code>, each with a preview drawn by the real script, with your own folder and branch.'),
    ('Icons', 'The setup prints three Nerd Font icons and asks whether they show. If you see boxes, it uses plain arrows and marks that every terminal draws.'),
    ('Time zone', 'Only when the system is on UTC. It sets the clock times the mods show and what counts as today.'),
    ('When to compact', 'Earlier, at about 70% of a 1M model (recommended, <code>733000</code>), Claude Code\'s default near the end, or at about half (<code>500000</code>). Skipped when the model\'s window is under 200K.'),
])}
<p>The setup also turns on auto-update for the marketplace, without asking. Run <code>/cockpit:setup</code> again to change an answer: it reads what is set and asks only about what you want to change.</p>

<h2>Check the install</h2>
{code('claude plugin list')}
<p>You should see 12 entries ending in <code>@cockpit</code>, each marked <code>enabled</code>: the bundle and the 11 mods. An entry marked <code>failed to load</code> points to a version mismatch; see <a href="#troubleshooting">Troubleshooting</a>.</p>

<h2>Updates install by themselves</h2>
<p>With auto-update on, a few minutes after the first message of a session, Claude Code updates every mod with a new version, installs any mod added to the bundle, and shows <code>Plugin updated: &lt;name&gt; · Run /reload-plugins to apply</code>. To turn it off, open <code>/plugin</code>, go to <b>Marketplaces</b>, and select <code>cockpit</code>.</p>

<h2>macOS, Windows and Linux</h2>
<p>Every mod runs on all three systems, and they are tested on Linux only. Two things differ:</p>
<ul>
  <li><code>memory-guard</code> and the memory figure of the <code>hud</code> read cgroup limits and <code>/proc/meminfo</code> on Linux. On macOS they read <code>vm_stat</code> and on Windows PowerShell, and there they compare against the whole machine's memory. The macOS and Windows readings are tested only against simulated output.</li>
  <li>The <code>panel</code> page shows memory by cgroup, systemd services and the share of CPU time spent waiting on disk only on Linux.</li>
</ul>
<p>On Windows, the setup points the status line at Node instead of the <code>.sh</code> script, because PowerShell cannot run a shell script.</p>

<h2>On a Team or Enterprise plan</h2>
<p>Every mod works the same on every plan, except <code>global-memory</code>. Team and Enterprise plans run a built-in guard that skips plugins you install yourself on the two hooks it needs, so it installs and does nothing until your organization lists it in managed settings. The other mods run as usual. The <a href="#global-memory">global-memory page</a> shows the two settings.</p>
{callout('note', 'Coming from the agent marketplace', '<p>Cockpit was called <code>agent</code> before October 2026. Rename every <code>@agent</code> key to <code>@cockpit</code> in <code>~/.claude/settings.json</code>, then run <code>claude plugin marketplace remove agent</code> before the steps above. Removing a marketplace deletes the saved options of its plugins, so rename the keys first, or run <code>/cockpit:setup</code> again afterwards.</p>')}
''')

page('Get started', 'first-session', 'firstrun', 'Your first session', 'Your first session', f'''
<p class="lead">After the setup and a restart, three things show on screen. The guards stay out of sight until they act.</p>
<h2>The status line</h2>
<p>The <code>hud</code> draws two rows under the prompt: the model, the folder, the git branch and its changes, then the context window, the 5-hour and 7-day plan windows, and the memory headroom.</p>
{term(statusline('refined'), 'status line · refined')}
<p>The bars turn from green to red as they fill. The <code>2h20m</code> after the 5-hour percent is the time until that window resets. The other three styles are on the <a href="#hud">hud page</a>.</p>
<h2>The line under the spinner</h2>
<p>While a turn runs, Claude Code shows a tip under the spinner. <code>spinner-status</code> replaces it with one line from Haiku about what the agent is doing right now.</p>
{term(SPINNER)}
<p><code>Now:</code> is where the session stands. <code>Mods:</code> is a tip about the mods you have.</p>
<h2>The session page</h2>
<p><code>panel</code> starts a local web page with every session on the machine. Type <code>/panel</code> for its address.</p>
{term(PANEL_OUT)}
<p>Open the address in a browser. A session that waits for you comes first, with the options it offered as buttons. The <a href="#panel">panel page</a> shows its five views.</p>
<h2>Commands to try</h2>
{table(['Command', 'What it shows'], [
    ('<code>/limit</code>', 'The plan windows, when each resets, and what the mod holds back near the limit.'),
    ('<code>/hud</code>', 'The full heads-up display: session, limits, memory, what runs now, and today\'s mod actions.'),
    ('<code>/ram</code>', 'Memory headroom per group, or of the machine, and the measured peak of each heavy command.'),
])}
<h2>When a guard acts</h2>
<p>The agent reads a short note that starts with the mod's name, such as <code>pipefail:</code> or <code>Loop check</code>, and usually tells you about it. The latest note also shows in the band above the prompt while the turn runs.</p>
''')

# --- guards ---
page('Guards', 'secret-guard', 'lock', '<code>secret-guard</code>', 'secret-guard', f'''
{meta(VERS['secret-guard'])}
<p class="lead">Hides every secret value in tool output before the agent reads it.</p>
<h2>Why</h2>
<p>A secret that reaches the transcript is sent to the model and kept in the session log, and from then on it must be rotated. Tool output leaks secrets easily: <code>env</code>, <code>cat .env</code>, a stack trace with a connection string. This mod replaces each value with <code>&lt;hidden:NAME&gt;</code> in every tool result, built-in, MCP and subagent alike.</p>
<h2>What it does</h2>
<ul>
  <li>The values come from the secrets file and every file in the folder beside it named like it plus <code>.d</code> (<code>~/.secrets.d/</code> by default), from every <code>.env*</code> file under the <code>.env</code> root (5 levels deep) when you set one, from environment variables with a secret-looking name (<code>TOKEN</code>, <code>SECRET</code>, <code>PASSWORD</code>, <code>KEY</code>, <code>AUTH</code> and others), and from the password of every <code>scheme://user:password@</code> URL.</li>
  <li>Known token formats are hidden even when no list has them: GitHub, Anthropic, OpenAI, AWS, Google, Stripe, Slack, JWT and private key blocks. They show as <code>&lt;hidden:github&gt;</code>, <code>&lt;hidden:jwt&gt;</code> and so on.</li>
  <li>A tool that hands out secrets, such as a password vault CLI, can keep its own <code>NAME="value"</code> list in a file in the secrets folder, without touching your secrets file. A file whose name starts with a dot is skipped, so the tool can write a temporary file and rename it into place.</li>
  <li>A value that also appears in a <code>.example</code> file is already public and stays visible.</li>
  <li>When the agent writes <code>&lt;hidden:NAME&gt;</code> into a <code>.env</code> file or the secrets file, the mod writes the real value in its place. The agent edits those files without ever seeing a value.</li>
  <li>When the agent writes <code>&lt;hidden:NAME&gt;</code> in a Bash command, the mod runs the command with the real value, and the output comes back hidden as usual. The transcript keeps the command as written. The agent can call an API with a token it never sees.</li>
  <li>A placeholder the mod cannot fill stops the command instead: a token known only by its format, or a name with two different values in your files, such as the same <code>DATABASE_URL</code> in two projects. The agent is told to read the value inside the command, from its variable or <code>.env</code> file.</li>
  <li>If the mod itself fails, it withholds the output instead of passing it unchecked.</li>
</ul>
<h2>Options</h2>
{opts([
    ('enabled', '<code>true</code>', 'Off, the mod does nothing: every value shows in tool output as it is. Takes effect in the next session, or after <code>/reload-plugins</code>.'),
    ('secretsFile', '<code>~/.secrets</code>', '<code>KEY=value</code> file whose every value is a secret, whatever its name.'),
    ('envRoot', 'empty', 'Folder searched for <code>.env</code> files, 5 levels deep. Empty searches none.'),
    ('minLength', '<code>12</code>', 'Shorter values are left alone, except known token formats and the values of the secrets files.'),
    ('fillCommands', '<code>true</code>', 'Run a Bash command that names <code>&lt;hidden:NAME&gt;</code> with the real value. Off, such a command does not run, and the agent is told to read the value inside the command.'),
])}
<p>By default the mod reads no <code>.env</code> files. To cover your projects' <code>.env</code> files too, set <code>envRoot</code> to the folder that holds your repos, such as <code>~/code</code>. The mod then scans it at start, checks its folders for new <code>.env</code> files at most once a minute, and rebuilds the list at least every 10 minutes.</p>
{diary('secret-guard', 'one line each time the list is rebuilt (with how long it took), a result is redacted, a placeholder is restored or filled in a command, or a command is stopped, with secret names and counts only, plus one <code>session-summary</code> line. The values live only in the mod\'s memory, never on disk.')}
<h2>Cost</h2>
<p>The hook added about 64 ms per tool call on the author's Linux machine (60 calls measured in October 2026, an estimate), with <code>envRoot</code> set to a folder of about 140 subfolders, most of it checking whether a source file changed.</p>
<h2>Limits</h2>
<ul>
  <li>A secret shorter than <code>minLength</code> that matches no known format stays visible. A value from the secrets file or its folder is hidden from 6 characters, because a vault hands out passwords of 8 to 11; under 6, a value is a PIN or a word, and hiding it would garble ordinary output.</li>
  <li>A secret that the agent already saw before this mod loaded is still in the transcript.</li>
  <li>A <code>.env</code> file outside <code>envRoot</code> is not read, so its values stay visible unless another source has them.</li>
  <li>Filling a placeholder in a command lets the agent use a secret, including sending it to a server. It cannot do more than it already could with <code>source .env</code>, but the command runs without a prompt of its own.</li>
  <li>Placeholders are filled back in Bash commands only. On Windows without Git Bash, a PowerShell command with a placeholder runs as written. Output of every tool is still hidden.</li>
  <li>Tested on Linux only. The macOS and Windows paths are covered by unit tests with a simulated environment.</li>
</ul>
{install_one('secret-guard')}
''')

page('Guards', 'collision-guard', 'branch', '<code>collision-guard</code>', 'collision-guard', f'''
{meta(VERS['collision-guard'])}
<p class="lead">Warns when two Claude Code sessions on the same machine work on the same files, and holds a git command once when it would take another session's uncommitted edits along.</p>
<h2>Why</h2>
<p>Running several sessions at once is common, and two of them often land in the same repo. On the author's Linux machine, 11 pairs of sessions edited the same repo less than 30 minutes apart in 8 days, and 5 of those pairs edited the same file. Claude Code's Edit already refuses a file changed since it was read, so one session does not silently overwrite the other. What it does not catch is git: <code>git add -A</code> or <code>git commit -a</code> in one session stages the other session's half-done edits, and <code>git stash</code>, <code>checkout</code> or <code>reset --hard</code> moves or discards them.</p>
<h2>What it does</h2>
<ul>
  <li>Each session keeps one record in <code>~/.local/state/mods/collision-guard/sessions/&lt;session&gt;.json</code> with the files it edited. Only that session writes it.</li>
  <li>After an edit, when another live session also edited that file and git still shows its change, the agent reads a note naming the session and how long ago, and you see a toast. Outside any git repo, the other edit counts for <code>windowMinutes</code>. Each edit of the other session warns once.</li>
  <li>Before a git command that would stage, commit, stash, switch away from or discard another session's uncommitted edits, the mod holds it and lists those files. The agent can name its own files instead, or run the same command again within 2 minutes to let it through.</li>
  <li>It reads <code>cd</code> earlier in the line and <code>git -C &lt;dir&gt;</code> to find the repo. Quoted text, such as a commit message, is not read as a command.</li>
  <li>A command that names paths, such as <code>git add -A mods/</code> or <code>git checkout -- src/a.ts</code>, is held only for the other session's edits under those paths. A wildcard or <code>:/</code> counts as the whole repo.</li>
  <li>Ended sessions mark their record, and records older than <code>expireHours</code> are removed when a session starts.</li>
</ul>
<h2>Options</h2>
{opts([
    ('enabled', '<code>true</code>', 'Off, the mod does nothing: no record, no warning, no git hold. Takes effect in the next session, or after <code>/reload-plugins</code>.'),
    ('git', '<code>confirm</code>', '<code>confirm</code> holds a risky git command once. <code>note</code> lets it run and tells the agent afterwards. <code>off</code> leaves git commands alone.'),
    ('windowMinutes', '<code>30</code>', 'How long another session\'s edit to a file outside any git repo still counts. Inside a repo, an edit counts while git shows the file as changed.'),
    ('expireHours', '<code>24</code>', 'A session silent this long counts as gone, and its record is removed.'),
    ('editWarnings', '<code>true</code>', 'Tell the agent, and show a toast, when another session edited the same file. Off, edits are still recorded, so the other sessions and the git guard still see them.'),
])}
{diary('collision-guard', 'one line per warning (<code>edit-warned</code>, <code>git-held</code>, <code>git-confirmed</code>, <code>git-noted</code>) with the git operation and how many files, never a file\'s content, plus one <code>session-summary</code> line.')}
<h2>Cost</h2>
<p>A tool call that is neither an edit nor a git command costs nothing measurable. An edit reads the other sessions' records and runs <code>git rev-parse</code> once per folder; when another session edited the same file, it also runs <code>git status</code> on it. In the first live test, the edit that found a collision took 444 ms of hook time, and the others under 60 ms (7 calls, October 2026).</p>
<h2>Limits</h2>
<ul>
  <li>Sessions must share the machine and the home folder. Sessions on another computer, or in a container with its own home, are not seen.</li>
  <li>A file changed by a Bash command (<code>sed -i</code>, a script, a formatter) is not recorded as an edit. Only Edit, Write, MultiEdit and NotebookEdit are.</li>
  <li><code>git checkout &lt;name&gt;</code> reads the same whether <code>&lt;name&gt;</code> is a branch or a file, so the note says "to another branch or an older version".</li>
  <li>Tested on Linux only. On Windows, paths are compared with forward slashes, as git prints them, and git commands through the PowerShell tool are checked like Bash ones. A <code>cd</code> to a Git Bash path such as <code>/c/work</code> is not followed.</li>
</ul>
{install_one('collision-guard')}
''')

page('Guards', 'pipefail', 'funnel', '<code>pipefail</code>', 'pipefail', f'''
{meta(VERS['pipefail'])}
<p class="lead">Adds <code>set -o pipefail;</code> to a command that pipes a test, typecheck or lint run into <code>tail</code>, <code>head</code> or <code>grep</code>.</p>
<h2>Why</h2>
<p>A pipeline exits with the code of its last command. <code>yarn test | tail -20</code> exits 0 when tests fail, because <code>tail</code> succeeded, and the agent reads a pass. Rewriting the command costs nothing and saves the agent a wrong conclusion.</p>
<h2>What it does</h2>
<ul>
  <li>Matches a runner where it runs: <code>yarn</code>, <code>npm run</code>, <code>pnpm</code> or <code>bun run</code> with <code>test</code>, <code>e2e</code>, <code>typecheck</code>, <code>lint</code>, <code>check</code> and similar scripts, or with a script named in <code>extraRunners</code>, plus <code>turbo run</code>, <code>vitest</code>, <code>jest</code>, <code>playwright test</code>, <code>tsc</code>, <code>vue-tsc</code>, <code>eslint</code>, <code>pytest</code>, <code>go test</code> and <code>cargo test</code>. Quoted text and heredoc bodies do not count.</li>
  <li>Puts <code>set -o pipefail;</code> in front, runs the command, and tells the agent that a <code>| head</code> can make a runner exit 141 (SIGPIPE).</li>
  <li>Leaves alone a command that already mentions <code>pipefail</code>.</li>
</ul>
{code('yarn test | tail -20' + chr(10) + '# becomes' + chr(10) + 'set -o pipefail; yarn test | tail -20', 'what the mod rewrites')}
<h2>Options</h2>
{opts([('enabled', '<code>true</code>', 'Off, the mod does nothing: no command is rewritten. Takes effect in the next session, or after <code>/reload-plugins</code>.'),
    ('extraRunners', 'empty list', 'Script names that also count as runners when a package manager calls them: <code>yarn &lt;name&gt;</code>, <code>npm run &lt;name&gt;</code>, <code>pnpm &lt;name&gt;</code>, <code>bun run &lt;name&gt;</code>.')])}
<p>Add a repo's own check script here when its exit code says whether the code works, such as <code>verify</code> for a script that runs lint, types and tests. The mod then rewrites <code>yarn verify | tail</code> too.</p>
{diary('pipefail', 'one line per rewrite naming the runner (<code>yarn vitest</code>, never the whole command), plus one <code>session-summary</code> line.')}
<h2>Cost</h2>
<p>The hook added about 2 ms per Bash call on the author's Linux machine (56 calls measured in October 2026, an estimate).</p>
<h2>Limits</h2>
<ul>
  <li>Only <code>tail</code>, <code>head</code> and <code>grep</code> as the filter. Other filters, such as <code>sed</code> or <code>awk</code>, are left alone.</li>
  <li>A runner hidden inside a script the command calls is not seen.</li>
  <li>Only the Bash tool. On Windows without Git Bash, commands run through the PowerShell tool and the mod leaves them alone. Tested on Linux only.</li>
</ul>
{install_one('pipefail')}
''')

page('Guards', 'memory-guard', 'mem', '<code>memory-guard</code>', 'memory-guard', f'''
{meta(VERS['memory-guard'], '/ram')}
<p class="lead">Keeps typecheck, build, test and Playwright runs under the memory limit, and reruns a command killed with exit 137 with one process. On Linux the limit is the tightest cgroup limit or the machine's memory; on macOS and Windows it is the machine's memory.</p>
<h2>Why</h2>
<p>On Linux, when memory runs out, or a cgroup reaches its <code>memory.max</code>, the kernel kills the largest process, which is usually the heavy command, and the agent sees exit 137 without knowing why. This mod checks the headroom before a heavy command runs and adapts the command to it.</p>
<h2>What it does</h2>
<p>Before a heavy command runs, the mod compares its expected peak with the headroom, minus the margin. The headroom is the machine's available memory, or the room left under the tightest cgroup limit when the session runs in one, as under a systemd service or in a container:</p>
<ol class="steps">
  <li><b>It fits</b><p>It runs as written.</p></li>
  <li><b>Only a single process fits</b><p>The mod adds <code>--concurrency=1</code>, <code>--workers=1</code> or <code>--maxWorkers=1</code> and tells the agent.</p></li>
  <li><b>Nothing fits</b><p>The mod waits up to <code>waitSeconds</code> for memory to free up.</p></li>
  <li><b>Memory does not free up</b><p>The mod refuses the command and tells the agent what uses the memory.</p></li>
</ol>
<p>After the command, the mod stores its measured peak for the next estimate, and reruns with a single process a command that died with exit 137. Until a command is measured, the estimates are 1 GB for typecheck and build, 600 MB for tests and 500 MB for Playwright.</p>
<p>Without a cgroup limit, as on most Linux desktops and laptops, the headroom is <code>MemAvailable</code> from <code>/proc/meminfo</code>. On macOS it is the free, inactive, speculative and purgeable pages of <code>vm_stat</code>, against the total of <code>sysctl -n hw.memsize</code>. On Windows it is <code>FreePhysicalMemory</code> against <code>TotalVisibleMemorySize</code>, read through PowerShell. Under a cgroup limit, it counts the working set: <code>memory.current</code> minus <code>inactive_file</code>, which the kernel frees before it kills anything.</p>
<h2>Commands</h2>
<p><code>/ram</code> shows the headroom, each cgroup's use and limits when there are any, and the measured peaks. It says there is no memory reading when the system gives none. In a terminal it also opens the Memory pane: a bar per cgroup with the high mark, refreshed every 2 seconds. Press <code>r</code> to refresh and <code>esc</code> to close.</p>
<h2>Options</h2>
{opts([
    ('enabled', '<code>true</code>', 'Off, the mod does nothing: heavy commands run as written, and <code>/ram</code> is gone. Takes effect in the next session, or after <code>/reload-plugins</code>.'),
    ('margin', '<code>2</code>', 'Share of memory kept free: of each cgroup\'s <code>memory.max</code>, or of the machine\'s total without a cgroup limit. The high mark counts only for a cgroup with no max.'),
    ('waitSeconds', '<code>120</code>', 'How long a heavy command waits for memory before it is refused.'),
    ('reduce', '<code>true</code>', 'When only a single process fits, add <code>--concurrency=1</code>, <code>--workers=1</code> or <code>--maxWorkers=1</code>.'),
    ('wait', '<code>true</code>', 'When nothing fits, wait up to <code>waitSeconds</code>. Off, the next step comes at once.'),
    ('refuse', '<code>true</code>', 'When memory does not free up, refuse the command. Off, it runs as written and may be killed.'),
    ('retry137', '<code>true</code>', 'Rerun with a single process a command killed with exit 137.'),
])}
<h2>What it records</h2>
<ul>
  <li><code>~/.local/state/mods/memory-guard/&lt;day&gt;-&lt;session&gt;.jsonl</code>: one line per reduced, refused or retried command and per measured peak, plus one <code>session-summary</code> line with the time commands waited.</li>
  <li>The last 3 measured peaks of each command, in the shared mod store under <code>peaks</code>.</li>
</ul>
<h2>Cost</h2>
<p>The hook added about 4 ms per Bash call on the author's Linux machine, not counting the time commands waited for memory (56 calls measured in October 2026, an estimate). Each heavy command also reads the memory files once a second while it runs, to measure its peak. On macOS and Windows a reading runs a command instead, and stays fresh for 10 seconds: <code>sysctl</code> and <code>vm_stat</code> take a few milliseconds, and PowerShell about a second to start (an estimate).</p>
<h2>Limits</h2>
<ul>
  <li>The peak is measured on the whole cgroup, or the whole machine without one, so another session starting at the same time inflates it. Keeping only the last 3 measurements lets an inflated one age out.</li>
  <li><code>tsc</code> has no flag for a single process, so a typecheck that does not fit waits or is refused.</li>
  <li>A background command returns at once and gives no measurement.</li>
  <li>The macOS and Windows readings are tested only against simulated <code>vm_stat</code>, <code>sysctl</code> and PowerShell output. There the headroom is the whole machine's, with no per-session limit, and a reading can be up to 10 seconds old.</li>
  <li>When the reading fails, heavy commands run as they came, nothing waits or is refused, and no peak is stored. <code>/ram</code> says there is no reading. The rerun with one process after an exit 137 still applies.</li>
</ul>
{install_one('memory-guard')}
''')

page('Guards', 'loop-breaker', 'loop', '<code>loop-breaker</code>', 'loop-breaker', f'''
{meta(VERS['loop-breaker'])}
<p class="lead">Notices when the agent goes in circles and tells it to stop and change approach.</p>
<h2>Why</h2>
<p>An agent that keeps editing the same file after the same failure burns tokens and time without getting closer. A short nudge at the right moment makes it step back, which a rule in <code>CLAUDE.md</code> does not do reliably.</p>
<h2>What it does</h2>
<p>The mod counts three signals per agent loop (the main conversation and each subagent), reset at the end of each turn:</p>
<ul>
  <li>Fix attempts: edits to one file while a command that failed has not passed again.</li>
  <li>Repeated errors: the same error coming back, with numbers, paths and quoted values ignored.</li>
  <li>Repeated calls: the same tool with the same arguments, in a row.</li>
</ul>
<p>When a count reaches its limit, the mod adds a note to the tool result. The note starts with <code>Loop check</code> and asks the agent to write what it tried, then re-read the code, form a new hypothesis, or ask you. Nothing is refused.</p>
<h2>Options</h2>
{opts([
    ('enabled', '<code>true</code>', 'Off, the mod does nothing: no count, no nudge. Takes effect in the next session, or after <code>/reload-plugins</code>.'),
    ('editLimit', '<code>5</code>', 'Fix attempts on one file in one turn before the nudge.'),
    ('errorLimit', '<code>3</code>', 'Times the same error may come back in one turn before the nudge.'),
    ('repeatLimit', '<code>3</code>', 'Identical tool calls in a row before the nudge.'),
    ('editCheck', '<code>true</code>', 'Nudge after <code>editLimit</code> fix attempts on one file.'),
    ('errorCheck', '<code>true</code>', 'Nudge after the same error comes back <code>errorLimit</code> times.'),
    ('repeatCheck', '<code>true</code>', 'Nudge after <code>repeatLimit</code> identical calls in a row.'),
])}
{diary('loop-breaker', 'one line per nudge with its kind and count, plus one <code>session-summary</code> line.')}
<h2>Cost</h2>
<p>The hook added about 2 ms per tool call on the author's Linux machine (60 calls measured in October 2026, an estimate).</p>
<h2>Limits</h2>
<ul>
  <li>A failure is read from the exit code and from failure words in the output, so a tool that fails silently is not counted.</li>
  <li>Counts reset at the end of each turn, so a loop that spans several turns is not caught.</li>
  <li>Tested on Linux only.</li>
</ul>
{install_one('loop-breaker')}
''')

page('Guards', 'usage-limit', 'gauge', '<code>usage-limit</code>', 'usage-limit', f'''
{meta(VERS['usage-limit'], '/limit')}
<p class="lead">Keeps the account usage limit from running out in the middle of a task.</p>
<h2>Why</h2>
<p>When a 5-hour or 7-day window reaches 100%, the session stops wherever it is, often mid-edit, and nothing resumes it. This mod slows down before that point, has the agent commit its work, stops at a reserve you keep for yourself, and resumes the session on its own when the window resets.</p>
<h2>The three stages</h2>
<p>Each window has three stages, each with its own switch and percentage:</p>
{table(['Stage', '5-hour window', '7-day window'], [
    ('Throttle: one subagent at a time', '90%', '97%'),
    ('Commit: ask for a <code>wip:</code> commit', '97%', '98%'),
    ('Pause: keep the rest for you', '98%', '99%'),
])}
<p>The 7-day limits also apply to the per-model weekly windows, such as <code>seven_day_opus</code>. Each window is judged by its own limits, and the most restrictive result applies: a paused window beats a throttled one. When two windows are paused, the one that resets last holds the session.</p>
<h2>What it does</h2>
<ul>
  <li>From the throttle, only one subagent runs at a time.</li>
  <li>From the commit stage, the agent is asked once per window to commit its work in progress in each repository it changed, with a <code>wip:</code> message and without pushing. It stages only the files it changed, so the work of another session in the same repository stays out. Only the main conversation gets the request.</li>
  <li>At the pause, every tool call is refused except a command that only stages and commits (<code>git add</code>, <code>git commit</code>, <code>cd</code>, chained with <code>&amp;&amp;</code>), so the work still gets committed when a burst of requests jumps straight past the commit stage. The agent writes in up to 3 lines where it stopped, and the mod schedules the resume for the reset time plus 2 minutes.</li>
  <li>A prompt you type during the pause gets one turn without subagents, spent from the reserve.</li>
  <li>A prompt nobody typed (a routine, another session, a task notification) is held and delivered with the resume.</li>
  <li>The band above the prompt shows each window with a bar, its own pause mark, the percent and the reset time, from 75% by default. Each bar turns yellow from its window's throttle or commit stage and red from its pause.</li>
  <li>The status line under the prompt shows the state while the mod holds something back.</li>
</ul>
<h2>Commands</h2>
<p><code>/limit</code> shows each window with its stages, the state, and what is held for the resume. Plain text, so it reads the same in Remote Control.</p>
<h2>Options</h2>
{opts([
    ('enabled', '<code>true</code>', 'Off, the mod does nothing: no throttle, commit, pause or resume, and <code>/limit</code> is gone. Takes effect in the next session, or after <code>/reload-plugins</code>.'),
    ('fiveHourThrottle', '<code>true</code>', 'Throttle in the 5-hour window.'),
    ('fiveHourThrottleAt', '<code>90</code>', 'From this share of the 5-hour window, one subagent at a time.'),
    ('fiveHourCommit', '<code>true</code>', 'Commit request in the 5-hour window.'),
    ('fiveHourCommitAt', '<code>97</code>', 'From this share of the 5-hour window, ask the agent once per window to commit without pushing.'),
    ('fiveHourPause', '<code>true</code>', 'Pause in the 5-hour window.'),
    ('fiveHourPauseAt', '<code>98</code>', 'The session pauses at this share of the 5-hour window.'),
    ('sevenDayThrottle', '<code>true</code>', 'Throttle in the 7-day windows.'),
    ('sevenDayThrottleAt', '<code>97</code>', 'From this share of a 7-day window, one subagent at a time.'),
    ('sevenDayCommit', '<code>true</code>', 'Commit request in the 7-day windows.'),
    ('sevenDayCommitAt', '<code>98</code>', 'From this share of a 7-day window, ask the agent once per window to commit without pushing.'),
    ('sevenDayPause', '<code>true</code>', 'Pause in the 7-day windows.'),
    ('sevenDayPauseAt', '<code>99</code>', 'The session pauses at this share of a 7-day window.'),
    ('timeZone', 'empty', 'IANA time zone of the reset times shown, such as <code>America/New_York</code>. Empty uses the system time zone.'),
    ('resume', '<code>true</code>', 'Resume the session when the window resets, after the pause or after the limit error. Off, you resume it, and automatic prompts that arrive during the pause are dropped instead of held. The older name <code>resumeOnError</code> still works.'),
    ('bandFrom', '<code>75</code>', 'Show the band from this share of the fullest window.'),
])}
<p>The window options have no default in the manifest, so the settings from before 1.2 still apply where they are unset. <code>alert</code> sets the throttle of every window, <code>commitAt</code> the commit (<code>0</code> turns it off), and <code>reserve</code> the pause at 100 minus its value. A window option always wins over them for its own stage.</p>
<h2>What it records</h2>
<ul>
  <li><code>~/.local/state/mods/usage-limit/&lt;day&gt;-&lt;session&gt;.jsonl</code>: one line per state change, refusal, held prompt and resume, plus one <code>session-summary</code> line when the session ends.</li>
  <li>The last reading of the windows, in the shared mod store under <code>windows</code>, so a new session starts from the reading another session took.</li>
</ul>
<h2>Cost</h2>
<p>The <code>tool.call</code> hook added about 6 ms per tool call on the author's Linux machine (60 calls measured in October 2026, an estimate).</p>
<h2>Limits</h2>
<ul>
  <li>The reading arrives with each model response, so a burst of parallel requests can pass the pause before the next reading. The resume after the limit error and the commit allowed during the pause cover that case.</li>
  <li>A prompt with an origin Claude Code cannot classify counts as yours and spends the reserve.</li>
  <li><code>/clear</code>, <code>/resume</code> and <code>/branch</code> cancel the scheduled resume and drop the held messages of the previous conversation.</li>
  <li>In the pause, the commit-only command passes through the Bash tool or, on Windows without Git Bash, the PowerShell tool.</li>
  <li>Tested on Linux only.</li>
</ul>
{install_one('usage-limit')}
''')

# --- instruments ---
STYLES = [('refined', 'Two rows with gradient bars. The default.'), ('blocks', 'Each field on its own colored background.'),
          ('minimal', 'Fields spelled out in words, thin bars.'), ('compact', 'One row when it fits, two when it does not.')]
page('Instruments', 'hud', 'hud', '<code>hud</code>', 'hud', f'''
{meta(VERS['hud'], '/hud')}
<p class="lead">Shows the model, the project and its git branch, the context window, the plan limits and the memory headroom, under the prompt as a status line or above it in the band. While a turn runs, the band adds the latest note another mod added to a tool result, which only the model reads otherwise.</p>
<h2>The four styles</h2>
<p>Pick one with the <code>style</code> option. Each style drops its least useful fields first when the terminal is narrow, so no row passes the width. Below is the real output of <code>statusline.sh</code> for the same session.</p>
''' + ''.join(f'<h3><code>{s}</code></h3><p>{d}</p>' + term(statusline(s), f'status line · {s}') for s, d in STYLES) + f'''
<h2>The status line</h2>
<p>A mod cannot draw rows under the prompt: that place belongs to the status line command of the settings. The mod ships one, <code>statusline/statusline.sh</code>, and <code>/cockpit:setup</code> writes it for you. To set it by hand on macOS or Linux, put this in <code>~/.claude/settings.json</code>, with <code>band</code> set to <code>off</code> so the rows do not show twice:</p>
{code(STATUS_JSON, '~/.claude/settings.json')}
<p>The script needs Node 22.18 or later. <code>refreshInterval</code> re-runs the script every 5 seconds, so git, the PR and the session time stay current while the session is idle. On Windows, PowerShell cannot run a <code>.sh</code> file: point the command at <code>node ~/.claude/plugins/marketplaces/cockpit/hud/statusline/statusline.ts</code>, with forward slashes.</p>
<h3>Git and the PR</h3>
<p>The git field shows the branch, then commits to push, commits to pull, files staged, files changed outside the stage and untracked files, or <code>synced</code> when there is nothing. The PR is the branch's open pull request from <code>gh pr view</code>, with its checks: passing, failing or running. <code>gh</code> takes about a second, so the script runs it in the background at most once a minute and shows the last answer meanwhile. Without <code>gh</code>, or without an open PR, the field is left out.</p>
<h3>Icons</h3>
<p>With <code>icons</code> set to <code>nerd</code>, the default, the git, folder, model and memory fields use Nerd Font glyphs, which show only when the terminal's font is a Nerd Font. With <code>unicode</code>, they use <code>↑ ↓ + ● ? ✓</code> and no glyph for the folder, the model and the memory.</p>
<h2>The band above the prompt</h2>
<p>Without the status line, the hud draws in the band above the prompt. With <code>band</code> at <code>panel</code>, the default, it draws two rows, with the right side of the first row flush with the last column:</p>
{term(BAND_PANEL, 'band · panel')}
<p>While a turn runs and another mod left a note, the activity row follows, such as <code>loop-breaker: repeated error</code>. It hides when the turn ends. Claude Code already draws the running tool, its errors, the subagents and the turn's time, so the band leaves them out.</p>
{table(['Field', 'Colors'], [
    ('<code>ctx</code>, the context window', 'green below 60%, yellow below 85%, red from 85%'),
    ('<code>5h</code> and <code>7d</code>, the plan windows', 'green below 75%, yellow below 90%, red from 90%'),
    ('<code>mem</code>, the memory that still fits', 'yellow below 1 GB, red below 500 MB'),
    ('Activity row', 'yellow'),
])}
<p>In a narrow terminal the band drops fields instead of wrapping: first it shortens the bars, then drops <code>mem</code>, then shows <code>ctx</code>, <code>5h</code> and <code>7d</code> as percents only, then drops the reset countdown. With <code>band</code> at <code>line</code>, it draws one row:</p>
{term(BAND_LINE, 'band · line')}
<h2>The /hud pane</h2>
{term(HUD_PANE, '/hud')}
<p><code>MEMORY</code> names the session's own cgroup and the group whose limit sets the headroom, or the machine's memory without a cgroup limit. <code>TODAY</code> counts today's lines in the other mods' diaries. The pane refreshes every 2 seconds while it is open; press <code>r</code> to refresh now and <code>esc</code> to close it.</p>
<h2>Options</h2>
<p>In <code>/config</code>, or under <code>pluginConfigs</code> in <code>~/.claude/settings.json</code>.</p>
{opts([
    ('enabled', '<code>true</code>', 'Off, the mod does nothing: no band, no activity row, no <code>/hud</code>, and the status line script prints an empty line. Takes effect in the next session, or after <code>/reload-plugins</code>.'),
    ('band', '<code>panel</code>', '<code>panel</code> draws two rows above the prompt, <code>line</code> one, <code>off</code> none (<code>/hud</code> still works). Use <code>off</code> with the status line.'),
    ('activity', '<code>true</code>', 'Shows the activity row while a turn runs.'),
    ('memory', '<code>true</code>', 'Shows the memory headroom in the band and the <code>MEMORY</code> row.'),
    ('bar', '<code>dots</code>', 'The bar glyphs: <code>blocks</code> (▰▱), <code>solid</code> (█░), <code>line</code> (━─), <code>dots</code> (●○) or <code>squares</code> (■□).'),
    ('barWidth', '<code>10</code>', 'Cells of a full-width bar, 4 to 30. A narrow terminal still shrinks the bars.'),
    ('colors', 'empty', 'The colors for ok, warning and critical, separated by spaces: a name, <code>#rrggbb</code> or a 256-color number. Empty uses green, yellow and red.'),
    ('hide', 'empty', 'Fields to leave out, separated by commas: <code>model</code>, <code>project</code>, <code>branch</code>, <code>age</code>, <code>calls</code>, <code>ctx</code>, <code>5h</code>, <code>7d</code>, <code>reset</code>, <code>mem</code>.'),
    ('barColor', '<code>gradient</code>', '<code>gradient</code> colors each cell by its place, green to red. <code>solid</code> colors the whole bar by its percent. <code>tone</code> keeps the three colors of <code>colors</code>.'),
    ('style', '<code>refined</code>', 'The status line layout: <code>refined</code>, <code>blocks</code>, <code>minimal</code> or <code>compact</code>.'),
    ('icons', '<code>nerd</code>', '<code>nerd</code> for Nerd Font glyphs, <code>unicode</code> for plain marks.'),
    ('contextBase', '<code>compact</code>', 'What <code>ctx</code> measures against. <code>compact</code>: 100% is the auto-compact window, when smaller than the model\'s. <code>window</code>: the model\'s full window. The status line only.'),
    ('timeZone', 'empty', 'The IANA time zone for the times shown and for what counts as today. Empty uses the system time zone.'),
])}
<h2>Cost</h2>
<p>The band's render hook does no I/O: it lays out values that events and timers already read. Every 15 seconds, idle or not, it runs one <code>git status</code> (3-second timeout) and a memory reading. During a turn, a 1-second timer reads the agent list for <code>/hud</code>, and redraws only while the pane is open. Each tool call adds two redraw requests, and Claude Code throttles redraws to 10 a second.</p>
<h2>Limits</h2>
<ul>
  <li>On macOS and Windows there is no per-session limit, so the memory field shows the whole machine. Those readings are tested only against simulated output.</li>
  <li>When the reading fails, the memory field is left out.</li>
  <li>The PR field needs the GitHub CLI, <code>gh</code>, signed in.</li>
  <li>The band, the status line and the pane are part of the terminal interface. Tested only in a terminal, and the Windows setup is not tested.</li>
</ul>
{install_one('hud')}
''')

page('Instruments', 'spinner-status', 'spinner', '<code>spinner-status</code>', 'spinner-status', f'''
{meta(VERS['spinner-status'], 'calls Haiku')}
<p class="lead">Replaces the tip under the spinner with one short line of its own: where the session stands, written by Haiku, or a tip about the mods you have installed that fits the moment.</p>
{term(SPINNER)}
<p>The spinner itself stays as Claude Code draws it. The line goes under it, cut to the width of the screen and to 100 characters. A bold label says what the line is: <code>Now:</code> for where the session stands and <code>Mods:</code> for a tip about the mods.</p>
<h2>Turn off the native tip</h2>
<p>A mod cannot remove Claude Code's own tip line. Turn it off in <code>settings.json</code>, or the two lines show together. <code>/cockpit:setup</code> already does this, and it is the same switch as the <b>Show tips</b> row of <code>/config</code>.</p>
{code('{ "spinnerTipsEnabled": false }', '~/.claude/settings.json')}
<h2>The modes</h2>
{table(['Mode', 'What the line shows', 'Model calls'], [
    ('<code>mixed</code>', 'The session summary, then a tip Haiku picked for the moment, swapping every 15 seconds. Before the first reply, a tip from the catalog. The default.', 'One per turn'),
    ('<code>tips</code>', 'A tip from the catalog, a new one each turn.', 'None'),
    ('<code>summary</code>', 'The session summary only. Before the first reply, nothing extra.', 'One per turn'),
])}
<p>The catalog has one tip for each command and mod of Cockpit: <code>/panel</code>, <code>/hud</code>, <code>/limit</code>, <code>/ram</code>, and what <code>memory-guard</code>, <code>loop-breaker</code>, <code>secret-guard</code>, <code>pipefail</code> and <code>usage-limit</code> do. The labels and the catalog are English. In <code>mixed</code> and <code>summary</code> modes, Haiku writes the line in Claude Code's <code>language</code> setting when it is set, and otherwise in the language you write in.</p>
<h2>Options</h2>
{opts([
    ('enabled', '<code>true</code>', 'Off, the mod does nothing and makes no model call.'),
    ('mode', '<code>mixed</code>', '<code>mixed</code>, <code>tips</code> or <code>summary</code>.'),
    ('model', '<code>claude-haiku-4-5-20251001</code>', 'The model that writes the line: an alias such as <code>haiku</code>, or a full model id.'),
])}
<h2>Cost</h2>
<p>Each main-loop turn starts at most one model call, in the background, when the turn starts. The spinner never waits for it: it keeps the previous line until the new one arrives. The model reads the last 3 prompts you typed and the agent's text between them, 3,000 characters at most, with no tool calls and no tool output. The reply is capped at 150 tokens.</p>
<p>In a test session, three turns spent 1,574 input and 139 output tokens in all: about 525 in and 46 out per turn, or about $0.0008 per turn at Haiku 4.5 prices. Each call took about one second.</p>
<h2>The reply is data</h2>
<p>The line Haiku writes is shown, never acted on. The mod keeps only the <code>NOW:</code> and <code>TIP:</code> lines, removes control characters and markup, folds each line to one, and cuts it to the width. The instructions tell the model that the session excerpt is data and not instructions.</p>
<h2>What it records</h2>
<p>At the end of each session, one <code>session-summary</code> line in <code>~/.local/state/mods/spinner-status/&lt;day&gt;-&lt;session&gt;.jsonl</code>, with the turns, the model calls by outcome, the calls skipped because one was still running, the tokens, the model time and the excerpt size. It never writes the excerpt or the line.</p>
<h2>Limits</h2>
<ul>
  <li>The model call goes through Claude Code itself, with no command of its own, so it works the same on macOS, Windows and Linux. Tested on Linux only.</li>
  <li>The spinner line is drawn by Claude Code's terminal interface. Tested only in a terminal.</li>
</ul>
{install_one('spinner-status')}
''')

page('Instruments', 'panel', 'grid', '<code>panel</code>', 'panel', f'''
{meta(VERS['panel'], '/panel', 'calls claude -p')}
<p class="lead">A local web page with every Claude Code session on your computer: whether it waits for you, what it needs, what it is doing now, and what it finished. Each session's summary comes from <code>claude -p</code>, refreshed every few minutes and when you ask.</p>
<div class="shot"><img src="img/panel-dark.png" alt="The panel page in the Inbox view: the machine in the header, the sessions by urgency on the left, and the selected session on the right" loading="lazy"></div>
<p class="figcap">The page with made-up sessions, in the Inbox view.</p>
<h2>Open the page</h2>
<p>Type <code>/panel</code> in any session for the address, <code>http://localhost:7777</code> by default, and open it in your browser. The server starts with the first session after you install the mod, and keeps running after that session ends. The page listens only on <code>127.0.0.1</code>, so only your own computer reaches it. When the sessions run on another machine, see <a href="#remote">Run on a remote machine</a>.</p>
<h2>What the page shows</h2>
<ul>
  <li>The header shows the computer in one line: the plan's 5-hour and weekly usage with the time left to each reset, memory, the CPU over the last minute, disk, and the tokens the sessions used in the last 24 hours, hour by hour. A figure turns amber at 75% and red at 90%. On the right are <b>Notify</b>, <b>Refresh all</b> and <b>Mods</b>.</li>
  <li>Each session shows its state (<code>Working</code>, <code>Waiting for you</code>, <code>Blocked</code>, <code>Done</code>, <code>Idle</code>), a title, the project, the git branch with its changed files and commits ahead or behind, the model, your last message, the tool running now, the summary of where the task stands, the next step and what it finished. Four figures close it: the context used against the point where it compacts, the tokens of the last 24 hours, the memory of the session's processes, and how long it has run.</li>
  <li>The <b>Mods</b> drawer shows the computer in full, the latest actions of the guards, what each guard did today, and how many summaries the page made today with their tokens and their price at API list prices. On Linux it also shows the memory of each cgroup with a limit and the state of their systemd services.</li>
</ul>
<h2>The five views</h2>
<p>The switcher under the header picks the view, and the page remembers it. The address also takes a view as its hash, such as <code>#board</code>, and <code>#mods</code> opens the drawer.</p>
{table(['View', 'What it shows', 'Keys'], [
    ('<b>Inbox</b>', 'The default. The sessions by urgency on the left, and the selected one in full on the right.', '<code>j</code> and <code>k</code> or the arrows move, <code>1</code> to <code>4</code> pick an option, <code>r</code> goes to the reply field'),
    ('<b>Board</b>', 'Columns by state, with small cards. A card opens the session in a side drawer.', '<code>1</code> to <code>4</code> in the drawer, <code>esc</code> closes it'),
    ('<b>Deck</b>', 'A grid of full cards, with filters for all sessions, the ones that need you, working, done and ended.', ''),
    ('<b>Focus</b>', 'One large card for the session that needs you most, and the others below it.', '<code>n</code> and <code>p</code> or the arrows move'),
    ('<b>Timeline</b>', 'A row per session with its tokens hour by hour over the last 24 hours, and a row for all sessions together.', ''),
], 'stack')}
<p><b>Working</b> comes from Claude Code itself, as soon as a turn starts. <b>Waiting for you</b>, <b>Blocked</b>, <b>Done</b> and <b>Idle</b> come from the summary, which <code>claude -p</code> writes from the transcript: 20 seconds after a turn ends, every 5 minutes for a session that changed, and when you press <b>Refresh</b>.</p>
<h2>Answer a session from the page</h2>
<p>When a session waits for a decision, its options are buttons. Press one, or its number key, check the text, and confirm. The reply field sends any text the same way. The page leaves the text in the session's inbox, the <code>panel</code> mod in that session checks the inbox every 2 seconds and submits the text as your prompt, and Claude Code runs it once the session is idle. It works on macOS, Windows and Linux, in a terminal, the Desktop app, an IDE or Remote Control, with or without tmux.</p>
{callout('note', 'Greyed-out options', '<p>A session takes answers only when its mod checked the inbox in the last 15 seconds. Until then its options are greyed out and its reply field is hidden. A session that loaded an older <code>panel</code> mod stays that way until you run <code>/reload-plugins</code> in it. When a session does not take a message within 6 seconds, the page withdraws it and says so.</p>')}
<h2>Audit the mods</h2>
<p>The lower half of the <b>Mods</b> drawer audits the mods from their diaries over the last day, 7 days or 30 days. Each row shows the mod's version, whether it is on, how many sessions it ran in, what it did, its failures in red, the time its hooks added per tool call, its slowest hook call, the API cost of its model calls, and its last action. A mod with nothing recorded for a week does no work on your machine.</p>
<div class="shot"><img src="img/panel-mods.png" alt="The Mods drawer: the computer, the guards, and one row per mod with its actions, failures and time per tool call" loading="lazy"></div>
<h2>Options</h2>
{opts([
    ('enabled', '<code>true</code>', 'Off, the mod does nothing: no <code>/panel</code>, no server start, no answers; a server already running keeps running. Takes effect in the next session, or after <code>/reload-plugins</code>.'),
    ('port', '<code>7777</code>', 'The port the page listens on, on <code>127.0.0.1</code>.'),
    ('model', '<code>sonnet</code>', 'The model <code>claude -p</code> uses for each summary: <code>sonnet</code>, <code>haiku</code> or <code>opus</code>.'),
    ('refreshMinutes', '<code>5</code>', 'A session whose transcript changed gets a new summary this often.'),
    ('autostart', '<code>true</code>', 'Start the server when a session starts and the port does not answer. Turn it off when a service manager runs the server.'),
    ('answers', '<code>true</code>', 'Let the page send text to this session as your prompt. Off, the page shows the session\'s options greyed out and no reply field.'),
])}
<h2>Start the server by hand</h2>
<p>The page needs Python 3.9 or later, as <code>python3</code>, <code>python</code> or <code>py</code>, and <code>curl</code>. With <code>autostart</code> on, the first session starts the server, and it keeps running after that session ends. To start it yourself, run the server file from the plugin folder, which is the <code>installPath</code> of <code>panel@cockpit</code> in <code>~/.claude/plugins/installed_plugins.json</code>:</p>
{code('python3 -I <plugin folder>/server/panel.py')}
<p>On Windows, use <code>python</code> or <code>py</code> in place of <code>python3</code>. Set <code>PANEL_CLAUDE</code> to the path of <code>claude</code> when it is not on the <code>PATH</code>.</p>
<h2>How the summary is made</h2>
<p>The server builds a digest of the transcript, at most 48,000 characters long: the message that opened the task, then the newest rows that fit, each tool call cut to one line. It sends the digest to <code>claude -p --safe-mode --tools "" --no-session-persistence</code> with a JSON schema. The call loads no hooks, plugins or tools, keeps no transcript of its own, and answers in a fixed shape, in the language you write in.</p>
<h2>Cost</h2>
<p>Each summary is one <code>claude -p</code> call, and it counts toward your plan's usage limits. On the author's Linux machine in October 2026, a summary of a long session read about 48,000 tokens and took 6 to 10 seconds, and the server's memory peaked at 213 MB during the call. At API list prices with <code>sonnet</code>, a summary cost about $0.07, and with four sessions working the page spent up to $2.40 an hour. On a Pro or Max plan the calls spend plan usage, not money. <code>haiku</code> costs about 20 times less per token, with shorter and less exact summaries.</p>
<h2>What it records</h2>
<ul>
  <li><code>~/.local/state/mods/panel/summaries/&lt;session&gt;.json</code>: the last summary of each session, with the time it was made and the transcript size it read.</li>
  <li><code>~/.local/state/mods/panel/&lt;day&gt;-server.jsonl</code>: one line per summary with the reason, the time, the state and the tokens, one line per failure, and one line per sent answer with its length. It never writes the session's content or what you sent.</li>
</ul>
<h2>Limits</h2>
<ul>
  <li>The sessions must run on the same machine, under the same user as the server.</li>
  <li>The page has no login. Anyone who can connect to the port on that machine can read it, start summaries and type into the sessions, so keep it on <code>127.0.0.1</code>. The server refuses a request that comes from a page on another site.</li>
  <li>An answer sent from the page waits until the session is idle. While a turn runs, it does not reach the agent, and it runs as a new turn after the current one ends.</li>
  <li>The state comes from the model and can lag behind the session. A busy session always shows <code>Working</code>.</li>
  <li>On macOS and Windows there are no memory groups, no services and no disk wait. Tested on Linux; the macOS and Windows code paths run only through simulated tests.</li>
</ul>
{install_one('panel')}
''')

page('Instruments', 'skill-loader', 'book', '<code>skill-loader</code>', 'skill-loader', f'''
{meta(VERS['skill-loader'])}
<p class="lead">Loads the right skill at the right moment, so <code>CLAUDE.md</code> needs no "load skill X before Y" rules.</p>
<h2>Why</h2>
<p>A rule in <code>CLAUDE.md</code> that says "load this skill before editing that file" works only when the agent remembers it. This mod watches the tool calls and delivers the skill itself.</p>
<h2>What it does</h2>
{table(['When the agent', 'Skill'], [
    ('Reads or writes a <code>.ts</code>, <code>.tsx</code>, <code>.mts</code> or <code>.cts</code> file', '<code>typescript-best-practices</code>'),
    ('Reads or writes <code>SKILL.md</code>, <code>AGENTS.md</code> or <code>CLAUDE.md</code>', '<code>writing-for-agents</code>'),
    ('Reads or writes <code>CONTEXT.md</code>, <code>CONTEXT-MAP.md</code> or a file under <code>adr/</code>, <code>adrs/</code> or <code>decisions/</code>', '<code>domain-modeling</code>'),
    ('Reads or writes a <code>README</code>, or runs <code>git commit</code>, <code>gh pr create</code> or <code>gh pr edit</code>', '<code>technical-writing</code>'),
])}
<ul>
  <li>On a read, the skill's full text comes with the file. Edit requires a read first, so the skill arrives before the edit.</li>
  <li>On a write without a read (a new file, a commit, a PR), the mod holds the call once, with the skill's text in the refusal, and the agent makes the call again.</li>
  <li>When your prompt carries an error or says something broke, the mod reminds the agent to load <code>diagnosing-bugs</code>.</li>
</ul>
<p>Each skill loads once per conversation. Compaction resets the list, because the summary can drop a skill's text.</p>
<h2>The skills</h2>
<p>The mod ships the five skills it delivers, in its <code>skills/</code> folder, so it works with nothing else installed. Claude Code also lists them as <code>skill-loader:&lt;name&gt;</code>. The mod reads a skill from its own folder first, then from <code>&lt;project&gt;/.claude/skills/&lt;name&gt;/SKILL.md</code>, then from <code>~/.claude/skills/&lt;name&gt;/SKILL.md</code>. The skills are by Matt Pocock, under the MIT license.</p>
<h2>Options</h2>
{opts([
    ('enabled', '<code>true</code>', 'Off, the mod does nothing: no skill is delivered and nothing is held. Takes effect in the next session, or after <code>/reload-plugins</code>.'),
    ('holdWrites', '<code>true</code>', 'Hold a write, a commit or a PR once, with the skill in the refusal, so the agent redoes it following the skill. Off, the call runs and the skill comes with its result.'),
    ('diagnoseReminder', '<code>true</code>', 'Remind the agent to load <code>diagnosing-bugs</code> when your prompt carries an error or says something broke.'),
])}
{diary('skill-loader', 'one line per skill loaded, held call, missing skill and reminder, plus one <code>session-summary</code> line.')}
<h2>Cost</h2>
<p>The hook added about 2 ms per tool call on the author's Linux machine (60 calls measured in October 2026, an estimate). A held write costs the agent one extra call.</p>
<h2>Limits</h2>
<ul>
  <li>Subagents are left alone: a skill delivered there would land in the main conversation.</li>
  <li>The error detection matches common English and Portuguese phrases and stack-trace shapes, so it misses an error described in other words.</li>
  <li>Tested on Linux only.</li>
</ul>
{install_one('skill-loader')}
''')

page('Memory', 'global-memory', 'globe', '<code>global-memory</code>', 'global-memory', f'''
{meta(VERS['global-memory'])}
<p class="lead">Adds a machine-wide memory folder beside the per-project auto memory, so facts about the machine reach every session from any folder.</p>
<h2>Why</h2>
<p>Claude Code's auto memory is per project. A fact about the machine, such as where a tool lives or how a service is reached, saved in one project's memory is missing from every other project. This mod adds one global folder that every session reads, and tells the agent which memories go there.</p>
<h2>What it does</h2>
<ul>
  <li>Rewrites the memory section of the system prompt to describe both folders and where each type of memory goes: <code>user</code> and <code>feedback</code> default to global, <code>reference</code> goes global when it is about the machine, and <code>project</code> always stays in the project.</li>
  <li>Adds the global <code>MEMORY.md</code> to the instruction files, so its index reaches every session the way the project index does.</li>
  <li>Keeps core's mode. When memory is read-only, the global folder is described as read-only too. When auto memory is off, or the global folder or its <code>MEMORY.md</code> is missing, the mod changes nothing.</li>
</ul>
<h2>Turn it on</h2>
<p>The mod creates nothing. Make the folder and an empty <code>MEMORY.md</code> in it, and the mod starts on the next session:</p>
{code('mkdir -p ~/.claude/global-memory && touch ~/.claude/global-memory/MEMORY.md')}
<p><code>globalDir</code> can point to a folder inside a git repo, such as <code>~/dotfiles/memory</code>, so the memories are versioned and can follow you to another machine.</p>
{callout('warn', 'No credentials', '<p>Every session on the machine reads the global folder. Never save a password or a key there.</p>')}
<h2>On a Team or Enterprise plan</h2>
<p>The built-in guard <code>sec-default@builtin</code> skips mods you install yourself on <code>prompt.section</code> and <code>prompt.context</code>, the two events this mod needs. List it in <code>prependPlugins</code> in managed settings, ahead of the guard, so it counts as your organization's:</p>
{code(MANAGED_JSON, 'managed settings')}
<p>On a personal plan it works as installed; on a Team or Enterprise plan it does nothing until these settings are in place.</p>
<h2>Options</h2>
{opts([('enabled', '<code>true</code>', 'Off, the mod does nothing: the memory section stays as Claude Code wrote it. Takes effect in the next session, or after <code>/reload-plugins</code>.'),
    ('globalDir', '<code>~/.claude/global-memory</code>', 'Folder of the machine-wide memory, with its own <code>MEMORY.md</code>.')])}
{diary('global-memory', 'one line each time the memory section is rewritten, the global index is added, or the mod steps aside and why, plus one <code>session-summary</code> line.')}
<h2>Cost</h2>
<p>None per tool call: the mod has no <code>tool.call</code> hook. It reads the global <code>MEMORY.md</code> when the system prompt and the first context are built. The rewritten text depends only on its input, so the prompt cache stays warm.</p>
<h2>Limits</h2>
<ul>
  <li>The rewrite matches the wording of the memory section Claude Code 2.1.292 sends. A different wording is left alone and logged as <code>skipped-unrecognized</code>.</li>
  <li>Tested on Linux only.</li>
</ul>
{install_one('global-memory')}
''')

# --- reference ---
page('Reference', 'commands', 'term', 'Commands', 'Commands', f'''
<p class="lead">Every command Cockpit adds. Each one also answers in plain text, so it works where no pane is drawn, such as Remote Control.</p>
{table(['Command', 'Mod', 'What it shows'], [
    ('<code>/panel</code>', '<a href="#panel">panel</a>', 'The address of the session page, and how many sessions need you. Starts the server when it does not answer. In a session opened over SSH, also prints the tunnel command.'),
    ('<code>/hud</code>', '<a href="#hud">hud</a>', 'The full heads-up display: session, limits, memory, now, today.'),
    ('<code>/limit</code>', '<a href="#usage-limit">usage-limit</a>', 'The plan windows with their stages, the state, and what is held for the resume.'),
    ('<code>/ram</code>', '<a href="#memory-guard">memory-guard</a>', 'Memory headroom per group, or of the machine, and the measured peak of each heavy command.'),
    ('<code>/cockpit:setup</code>', 'cockpit', 'Runs the setup again, to change the style or any other answer.'),
], 'stack')}
<h2>Keys inside a pane</h2>
<p>Press <code>r</code> to refresh it and <code>esc</code> to close it.</p>
<h2>Keys on the panel page</h2>
<p>Press <code>r</code> to summarize every session again, or <code>R</code> in Inbox, where <code>r</code> goes to the reply field. <code>esc</code> closes the send dialog, then the Mods drawer, then the Board drawer. Each view adds its own keys, listed on the <a href="#panel">panel page</a>.</p>
''')

page('Reference', 'configure', 'sliders', 'Configure and turn mods off', 'Configure and turn mods off', f'''
<p class="lead">Every mod option is a row in <code>/config</code>. The setup handles the few settings a plugin cannot write itself.</p>
<h2>Change an option</h2>
<p>Open <code>/config</code> and scroll to the mod. Each mod's page lists its options, their defaults and what they do. The status line picks up a change within five seconds; for the other mods, restart Claude Code or run <code>/reload-plugins</code>.</p>
<h2>In the settings file</h2>
<p>The same options live under <code>pluginConfigs</code> in <code>~/.claude/settings.json</code>, keyed by <code>&lt;mod&gt;@cockpit</code>. This is useful to share a setup across machines:</p>
{code(chr(10).join(['{', '  "pluginConfigs": {', '    "hud@cockpit": { "options": { "style": "blocks", "icons": "unicode" } },', '    "usage-limit@cockpit": { "options": { "timeZone": "Europe/Lisbon" } },', '    "collision-guard@cockpit": { "options": { "git": "note" } }', '  }', '}']), '~/.claude/settings.json')}
<h2>What the setup writes</h2>
{table(['Setting', 'Value', 'Why'], [
    ('<code>statusLine</code>', 'the <code>hud</code> script, with <code>refreshInterval: 5</code>', 'A plugin cannot draw under the prompt.'),
    ('<code>spinnerTipsEnabled</code>', '<code>false</code>', 'So the <code>spinner-status</code> line replaces Claude Code\'s tip instead of sitting under it.'),
    ('<code>autoCompactWindow</code>', '<code>733000</code> on a 1M model, if you choose it', 'Claude Code summarizes the conversation at about 70% instead of near the end.'),
    ('<code>pluginConfigs</code>', '<code>band: "off"</code> for the hud, style, icons, time zone', 'Your answers to the setup questions. With the status line on, the band goes off so the rows do not show twice.'),
    ('<code>enabledPlugins</code>', '<code>claude-hud@claude-hud</code> off, when it was on', 'Its status line is the one the hud replaces.'),
    ('<code>pluginConfigs</code>', '<code>enabled: false</code> for each mod you turn off, if you ask', 'Only when you ask the setup to turn mods off.'),
    ('<code>extraKnownMarketplaces.cockpit</code>', '<code>autoUpdate: true</code>', 'The mods update by themselves.'),
], 'stack')}
<h2>Turn one mod off</h2>
<p>Every mod has an <b>Enabled</b> option. Turn it off in <code>/config</code>, or set <code>"enabled": false</code> under the mod's <code>pluginConfigs</code> entry, then start a new session or run <code>/reload-plugins</code>. Off, the mod registers no hook and costs nothing per tool call. <code>/cockpit:setup</code> can also turn mods off for you.</p>
{code(chr(10).join(['{', '  "pluginConfigs": {', '    "loop-breaker@cockpit": { "options": { "enabled": false } },', '    "memory-guard@cockpit": { "options": { "refuse": false } }', '  }', '}']), '~/.claude/settings.json')}
<h2>Turn off one step of a guard</h2>
{table(['Mod', 'Switches'], [
    ('<a href="#secret-guard"><code>secret-guard</code></a>', '<code>fillCommands</code>'),
    ('<a href="#collision-guard"><code>collision-guard</code></a>', '<code>editWarnings</code>, and <code>git: off</code> for the git hold'),
    ('<a href="#memory-guard"><code>memory-guard</code></a>', '<code>reduce</code>, <code>wait</code>, <code>refuse</code>, <code>retry137</code>'),
    ('<a href="#loop-breaker"><code>loop-breaker</code></a>', '<code>editCheck</code>, <code>errorCheck</code>, <code>repeatCheck</code>'),
    ('<a href="#usage-limit"><code>usage-limit</code></a>', 'throttle, commit and pause for each window, and <code>resume</code>'),
    ('<a href="#skill-loader"><code>skill-loader</code></a>', '<code>holdWrites</code>, <code>diagnoseReminder</code>'),
    ('<a href="#panel"><code>panel</code></a>', '<code>answers</code>, <code>autostart</code>'),
])}
<p>Each mod's page says what each switch stops.</p>
<h2>Remove a mod's hooks entirely</h2>
<p>Claude Code refuses to disable a plugin that an enabled plugin requires, and the <code>cockpit</code> bundle requires every mod. Disable the bundle first, then the mod:</p>
{code('claude plugin disable cockpit@cockpit' + chr(10) + 'claude plugin disable pipefail@cockpit')}
<p>The other mods stay on. Enabling the bundle again turns the mod back on.</p>
''')

page('Reference', 'remote', 'server', 'Run on a remote machine', 'Run on a remote machine', f'''
<p class="lead">If you run Claude Code on a remote Linux machine over SSH, the mods work the same, and a few parts do more.</p>
<h2>Open the page through a tunnel</h2>
<p><code>panel</code> listens only on <code>127.0.0.1</code> of the machine where the sessions run. From your computer, open an SSH tunnel, then open <code>http://localhost:7777</code>. In a session opened over SSH, <code>/panel</code> prints this command with the machine's name.</p>
{code('ssh -N -L 7777:127.0.0.1:7777 <host>', 'on your computer')}
<p>To open the tunnel with every SSH login, add one line to the host's entry in <code>~/.ssh/config</code> on your computer:</p>
{code('Host <host>' + chr(10) + '  LocalForward 7777 127.0.0.1:7777', '~/.ssh/config')}
<h2>Run the page as a service</h2>
<p>Instead of letting a session start the page, run it under systemd. Set the <code>panel</code> option <code>autostart</code> to <code>false</code>, then run the server as a unit:</p>
{code(chr(10).join(['[Service]', 'User=<user>', 'ExecStart=/usr/bin/python3 -I /home/<user>/.claude/plugins/marketplaces/cockpit/panel/server/panel.py', 'Environment=PANEL_CLAUDE=/home/<user>/.local/bin/claude', 'Restart=always']), 'systemd unit')}
<p><code>PANEL_PORT</code>, <code>PANEL_MODEL</code> and <code>PANEL_REFRESH_MINUTES</code> set the server's options. Set <code>PANEL_GROUPS</code> to a comma-separated list of cgroup paths, such as <code>agents.slice</code>, to show those groups and everything under them on the page.</p>
<h2>Memory limits</h2>
<p>When sessions run under a cgroup v2 memory limit, as a systemd service or a container sets, <code>memory-guard</code> keeps heavy commands under the tightest limit, the <code>hud</code> shows the room left under it, <code>/ram</code> shows each group, and the page shows each group's memory and the state of its systemd services.</p>
<h2>Remote Control and tmux</h2>
<p>Every Cockpit command also answers in plain text, so it works when you drive a session over <a href="https://code.claude.com/docs/en/remote-control" target="_blank" rel="noopener">Remote Control</a> from claude.ai or the mobile app, where no pane is drawn. The page links a session to claude.ai when the session runs with Remote Control. For a session that runs in tmux, its <b>tmux</b> button copies the command that attaches to its pane.</p>
''')

page('Reference', 'data', 'shield', 'What leaves your machine', 'What leaves your machine', f'''
<p class="lead">Cockpit runs inside Claude Code on your machine. Two mods send an excerpt of the session to a model, through your own account. Everything else stays local.</p>
<h2>What leaves</h2>
{table(['Mod', 'Sends', 'When'], [
    ('<code>panel</code>', 'An excerpt of each session\'s transcript, through <code>claude -p</code>, to <code>sonnet</code> by default', 'On <b>Refresh</b>, when a session goes idle after a turn, and every 5 minutes for a session that changed'),
    ('<code>spinner-status</code>', 'The last few prompts and the agent\'s last text, at most 3,000 characters, to Haiku', 'Once per turn, or never in <code>tips</code> mode'),
    ('<code>hud</code>', 'A <code>gh pr view</code> request for the current branch, to GitHub', 'At most once a minute, when <code>gh</code> is installed'),
], 'stack')}
<p>These calls use the same account and the same data terms as the rest of your Claude Code session. No other mod calls a model.</p>
<h2>What stays</h2>
<ul>
  <li>Every mod writes a diary under <code>~/.local/state/mods/&lt;mod&gt;/</code>, one line per action and one summary per session. A diary never holds a secret value or a file's content.</li>
  <li><code>collision-guard</code> keeps the list of files each session edited. An ended session marks its record, and records older than <code>expireHours</code> (24 hours by default) are removed when a session starts.</li>
  <li><code>secret-guard</code> holds secret values in memory only, never on disk.</li>
  <li><code>panel</code> keeps the last summary of each session. The page has no login and listens only on <code>127.0.0.1</code>. Anyone who can reach that port can read it and type into your sessions, so do not expose it.</li>
</ul>
''')

TROUBLE = [
    ('The status line does not show, or only changes when a message arrives', 'The <code>statusLine</code> setting is missing, or has no <code>refreshInterval</code>. Run <code>/cockpit:setup</code> again, then restart Claude Code.'),
    ('The status line shows nothing at all', 'The script needs Node 22.18 or later. Run <code>node --version</code>, and update Node if it is older.'),
    ('Icons show as boxes or question marks', 'The terminal font has no Nerd Font glyphs. Set <code>icons</code> to <code>unicode</code> under <code>hud</code> in <code>/config</code>, or install a Nerd Font and select it in your terminal.'),
    ('The bars look like a single blurred shape', 'Some fonts draw the bar glyphs joined together. Set <code>bar</code> under <code>hud</code> to <code>dots</code> or <code>squares</code>.'),
    ('Two lines show under the spinner', 'Claude Code\'s own tip is still on. Set <code>"spinnerTipsEnabled": false</code> in your settings, or run the setup again.'),
    ('A mod shows <code>failed to load</code> in <code>claude plugin list</code>', 'The marketplace copy and the installed version are out of step. Run <code>claude plugin marketplace update cockpit</code>, then <code>claude plugin update cockpit@cockpit</code>, and restart.'),
    ('The mod options are gone', 'Removing a marketplace deletes the saved options of its plugins. Run <code>/cockpit:setup</code> again to write them back.'),
    ('<code>global-memory</code> does nothing on a Team or Enterprise plan', 'Those plans skip user-installed plugins on the hooks it needs. It must run as an organization plugin; its <a href="#global-memory">page</a> shows the managed settings.'),
    ('<code>/panel</code> says the page server is not running', 'The server starts when a session starts, unless <code>autostart</code> is off. Check that Python 3.9 or later is installed as <code>python3</code>, <code>python</code> or <code>py</code>, and that <code>curl</code> runs, then start a new session. The server writes its errors to <code>~/.local/state/mods/panel/server.log</code>.'),
    ('The page greys out the options of a session', 'The session has not checked its inbox in the last 15 seconds, usually because it loaded an older <code>panel</code> mod. Run <code>/reload-plugins</code> in that session.'),
    ('The Mods drawer shows no memory groups or services', 'That is expected on macOS and Windows. The page shows memory by group only for Linux cgroup v2 groups with a limit, and services only under systemd.'),
    ('<code>/ram</code> says there is no memory reading', '<code>memory-guard</code> found no <code>/proc/meminfo</code>, and the system command failed: <code>sysctl</code> and <code>vm_stat</code> on macOS, or PowerShell on Windows, missing or slower than its timeout. Until a reading works, heavy commands run as written.'),
    ('A git command was refused with a list of files', '<code>collision-guard</code> held it, because another session on this machine has uncommitted edits in the same repo, under the paths the command names. Name your own files instead, or run the same command again within 2 minutes.'),
]
page('Reference', 'troubleshooting', 'warn', 'Troubleshooting', 'Troubleshooting',
     '<p class="lead">The problems people hit most, and the fix for each.</p>' + table(['Symptom', 'Fix'], TROUBLE, 'stack'))

page('Reference', 'update', 'upload', 'Update and uninstall', 'Update and uninstall', f'''
<p class="lead">Updates arrive by themselves, a few minutes after the first message of a session. You can also update by hand, and remove everything in two commands.</p>
<h2>Automatic updates</h2>
<p>The setup turns on auto-update for the <code>cockpit</code> marketplace. Claude Code then refreshes the marketplace once per session and updates every Cockpit mod with a new version, each one on its own. The open session keeps the versions it loaded until you run <code>/reload-plugins</code>; the next session loads the new ones.</p>
<h2>Update by hand</h2>
<p>Updating the bundle does not update the mods: each mod is its own plugin. To update them all now:</p>
{code(UPDATE_ALL)}
<p>To update one mod, name it: <code>claude plugin update hud@cockpit</code>.</p>
<h2>Uninstall</h2>
{code('claude plugin uninstall cockpit@cockpit' + chr(10) + 'claude plugin prune')}
<p>Uninstalling the bundle leaves the mods installed; <code>claude plugin prune</code> removes them. The setup wrote <code>statusLine</code>, <code>spinnerTipsEnabled</code> and <code>autoCompactWindow</code> to your settings file and kept a backup next to it. Remove those keys by hand, or restore the backup.</p>
<h2>Remove the data</h2>
<p>The mods leave their diaries in <code>~/.local/state/mods/</code>. Delete that folder to remove everything Cockpit wrote.</p>
''')

page('Reference', 'versions', 'tag', 'Versions', 'Versions', f'''
<p class="lead">Cockpit {VERS['cockpit']}. The bundle carries the version of the release, and each mod carries the version of the release where it last changed.</p>
<p>A mod that did not change in a release keeps its version, so Claude Code does not update it.</p>
''' + table(['Mod', 'Version'], [('<code>cockpit</code> (bundle)', VERS['cockpit'])] + [(f'<a href="#{m}"><code>{m}</code></a>', VERS[m]) for m in ORDER]) + '''
<h2>What changed</h2>
<ul>
  <li><b>1.3.0</b>: every mod has an <code>enabled</code> option, and the guards have one switch per step. <code>/cockpit:setup</code> can turn mods off.</li>
  <li><b>1.2.0</b>: <code>usage-limit</code> limits each window on its own, with a separate throttle, commit and pause for the 5-hour and 7-day windows, each with its own switch and percentage.</li>
  <li><b>1.1.0</b>: <code>secret-guard</code> reads the secrets folder beside the secrets file.</li>
</ul>
''')

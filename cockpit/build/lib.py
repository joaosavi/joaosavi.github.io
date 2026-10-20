"""Shared pieces of the Cockpit docs: the always-on CSS and JS, the HTML helpers, and the Markdown export.

The pages live in content_en.py and content_pt.py. Run build.py to write cockpit/ and cockpit/pt/.
Needs the Cockpit repo at ~/cockpit, for the real status line output and the mod versions."""
import html, json, os, re
from html.parser import HTMLParser
from pathlib import Path

SITE = Path(__file__).resolve().parents[2]
COCKPIT = Path(os.environ.get('COCKPIT_REPO', Path.home() / 'cockpit'))
BASE_URL = 'https://joaosavi.github.io/cockpit/'

# build.py of the Cockpit repo imports markdown on load; only its ANSI converter is needed here
_src = (COCKPIT / 'docs/build.py').read_text()
_ns = {'html': html, 're': re, 'os': os, 'HERE': str(COCKPIT / 'docs')}
exec(_src[_src.index('BASIC = '):_src.index('# --- markdown')], _ns)
statusline = lambda style: _ns['statusline'](style, 64)
G = '<span class="g">'

VERS = {}
for _d in COCKPIT.glob('*/.claude-plugin/plugin.json'):
    _j = json.loads(_d.read_text())
    VERS[_j['name']] = _j['version']

# --- the always-on look -----------------------------------------------------------------------
_ao = (SITE / 'always-on/index.html').read_text()
_lines = _ao.split('\n')
_style_end = next(i for i, l in enumerate(_lines) if l.startswith('<style>[hidden]'))
HEAD_CSS = '\n'.join(_lines[_lines.index('<style>'):_style_end + 1])
_script = _ao[_ao.index('<script>') + len('<script>'):_ao.rindex('</script>')]

def _cut(js, start, end):
    a = js.index(start)
    return js[:a] + js[js.index(end, a):]

_script = _cut(_script, '  // telas da Oracle', '  // busca da lateral')
_script = _cut(_script, '  // progresso:', '  // grupos da lateral')
_script = _cut(_script, '  // pedido do setup', '  // tabela em cartões')
_script = _script.replace("location.hash = 'setup'", "location.hash = 'install'").replace('aoClosed', 'cpClosed').replace("'#inicio'", "'#start'")

def script(lang):
    if lang == 'pt':
        return _script
    s = _script
    for a, b in [("'Abrir o menu'", "'Open the menu'"), ("'Fechar o menu'", "'Close the menu'"), ('<small>Anterior</small>', '<small>Previous</small>'),
                 ('<small>Próxima</small>', '<small>Next</small>'), ("'Copiado'", "'Copied'"), ("'Selecionado, use Ctrl+C'", "'Selected, press Ctrl+C'")]:
        assert a in s, a
        s = s.replace(a, b)
    return s

EXTRA_CSS = '''<style>
/* Cockpit: clickable mod cards, page meta, terminal output, language switch. */
a.mod { display: block; text-decoration: none; color: var(--ink); transition: border-color .15s; }
a.mod:hover { border-color: var(--led); }
.meta { display: flex; flex-wrap: wrap; gap: 8px; margin: -4px 0 22px; }
.meta .pill { font-family: var(--f-mono); font-weight: 500; }
.pill.mute { background: var(--sunken); color: var(--muted); }
/* terminal window: title bar over the real output */
.tw { margin: 12px 0 28px; border: 1px solid #1d2330; border-radius: 14px; overflow: hidden; background: #0b0e13; box-shadow: var(--shadow); }
.tw-bar { display: flex; align-items: center; gap: 6px; padding: 9px 12px; background: #11151d; border-bottom: 1px solid #1d2330; }
.tw-bar i { width: 10px; height: 10px; border-radius: 50%; background: #2a313f; }
.tw-bar span { margin-left: 8px; font: 500 13px/1 var(--f-mono); color: #7d8597; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.tw pre.term { margin: 0; border: 0; border-radius: 0; box-shadow: none; }
.term b { font-weight: 700; }
.term .bl { color: #8fb4ff; }
.spin { position: relative; color: transparent !important; }
.spin::before { content: "✻"; position: absolute; left: 0; color: #f0b43c; }
@media (prefers-reduced-motion: no-preference) { .spin::before { animation: spin-glyph 1.2s steps(1) infinite; } }
@keyframes spin-glyph { 0% { content: "·"; } 16% { content: "✢"; } 33% { content: "✳"; } 50% { content: "✶"; } 66% { content: "✻"; } 83% { content: "✽"; } }
.shot { margin: 18px 0 8px; border: 1px solid var(--line); border-radius: 14px; overflow: hidden; background: var(--surface); }
.shot img { display: block; width: 100%; height: auto; }
.nav-group a code { background: none; border: 0; padding: 0; font-size: 13.5px; color: inherit; }
.top-right { margin-left: auto; display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
.gh, .lang-sw a { font: 500 13px/1 var(--f-mono); color: var(--muted); border: 1px solid var(--line); border-radius: 6px; padding: 7px 9px; white-space: nowrap; text-decoration: none; }
.gh:hover, .lang-sw a:hover { color: var(--ink); border-color: var(--line-strong); }
.lang-sw { display: flex; }
.lang-sw a + a { margin-left: -1px; }
.lang-sw a:first-child { border-radius: 6px 0 0 6px; }
.lang-sw a:last-child { border-radius: 0 6px 6px 0; }
.lang-sw a[aria-current] { color: var(--ink); background: var(--sunken); }
@media (max-width: 520px) { .gh { display: none; } }
</style>'''

# --- language strings -------------------------------------------------------------------------
T = {
    'en': dict(copy='Copy', opt='Option', default='Default', does='What it does', only_h='Install this mod alone',
               only_p='The <code>cockpit</code> bundle already installs <code>{n}</code> with the other mods. To install it alone:',
               rec_h='What it records', rec_tail='Each line has <code>at</code>, <code>session</code> and <code>event</code>.',
               day='&lt;day&gt;-&lt;session&gt;', terminal='terminal', search='Search the docs', empty='Nothing found. Try another word.',
               menu='Open the menu', toc='On this page', pager='Previous and next page', pages='Pages',
               agent='Copy for your agent', md='Markdown', llms='llms.txt', html_lang='en', alt_lang='pt', alt_href='pt/',
               agent_text='Read {url} with curl and help me with this part of Cockpit, the mods for Claude Code. The index of every page is at {idx}.',
               foot='Cockpit {v} · <a href="https://github.com/joaosavi/cockpit" target="_blank" rel="noopener">github.com/joaosavi/cockpit</a> · MIT license · Not affiliated with Anthropic · <a href="llms.txt">llms.txt</a> · Reviewed on October 20, 2026',
               gh='v{v} on GitHub', brand='Cockpit, documentation', more='Read more'),
    'pt': dict(copy='Copiar', opt='Opção', default='Padrão', does='O que faz', only_h='Instalar só este mod',
               only_p='O pacote <code>cockpit</code> já instala o <code>{n}</code> com os outros. Para ter só ele:',
               rec_h='O que grava', rec_tail='Cada linha tem <code>at</code>, <code>session</code> e <code>event</code>.',
               day='&lt;dia&gt;-&lt;sessão&gt;', terminal='terminal', search='Buscar na documentação', empty='Nada encontrado. Tente outra palavra.',
               menu='Abrir o menu', toc='Nesta página', pager='Página anterior e próxima', pages='Páginas',
               agent='Copiar para o agente', md='Markdown', llms='llms.txt', html_lang='pt-BR', alt_lang='en', alt_href='../',
               agent_text='Leia {url} com curl e me ajude com esta parte do Cockpit, os mods para o Claude Code. O índice de todas as páginas está em {idx}.',
               foot='Cockpit {v} · <a href="https://github.com/joaosavi/cockpit" target="_blank" rel="noopener">github.com/joaosavi/cockpit</a> · Licença MIT · Sem vínculo com a Anthropic · <a href="llms.txt">llms.txt</a> · Revisado em 20 de outubro de 2026',
               gh='v{v} no GitHub', brand='Cockpit, documentação', more='Leia mais'),
}
LANG = 'en'
def t(k):
    return T[LANG][k]

# --- icons ------------------------------------------------------------------------------------
IC = {
    'zap': 'M13 2 4 14h7l-1 8 9-12h-7z',
    'rocket': 'M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09zM12 15l-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2zM9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5',
    'download': 'M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3',
    'shield': 'M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z',
    'lock': 'M5 11h14v10H5zM7 11V7a5 5 0 0 1 10 0v4',
    'branch': 'M6 3v12M18 9a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM6 21a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM18 9a9 9 0 0 1-9 9',
    'funnel': 'M22 3H2l8 9.46V19l4 2v-8.54z',
    'mem': 'M6 19v-3M10 19v-3M14 19v-3M18 19v-3M8 11V9M16 11V9M12 11V9M2 15h20M4 5h16a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2z',
    'loop': 'M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8M21 3v5h-5M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16M8 16H3v5',
    'gauge': 'M12 14l4-4M3.34 19a10 10 0 1 1 17.32 0',
    'hud': 'M3 4h18v16H3zM3 15h18M7 18h4',
    'spinner': 'M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83',
    'grid': 'M3 3h7v7H3zM14 3h7v7h-7zM14 14h7v7h-7zM3 14h7v7H3z',
    'book': 'M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2zM22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z',
    'globe': 'M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20zM2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z',
    'db': 'M12 8c4.97 0 9-1.34 9-3s-4.03-3-9-3-9 1.34-9 3 4.03 3 9 3zM3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5M3 12c0 1.66 4 3 9 3s9-1.34 9-3',
    'search': 'M11 18a7 7 0 1 0 0-14 7 7 0 0 0 0 14zM20 20l-3.5-3.5',
    'term': 'M7 11l2-2-2-2M11 13h4M5 3h14a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z',
    'sliders': 'M4 21v-7M4 10V3M12 21v-9M12 8V3M20 21v-5M20 12V3M1 14h6M9 8h6M17 16h6',
    'server': 'M2 2h20v8H2zM2 14h20v8H2zM6 6h.01M6 18h.01',
    'warn': 'M21.73 18l-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3M12 9v4M12 17h.01',
    'upload': 'M12 3v12M7 8l5-5 5 5M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4',
    'tag': 'M12 2H2v10l9.29 9.29a1 1 0 0 0 1.41 0l6.59-6.59a1 1 0 0 0 0-1.41zM7 7h.01',
    'firstrun': 'M4 17l6-6-6-6M12 19h8',
}
def svg(name, w='1.8', cls='gen-ic'):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="{IC[name]}"/></svg>'

# --- pieces -----------------------------------------------------------------------------------
def code(text, label=None):
    return f'<div class="code"><div class="code-head"><span>{label or t("terminal")}</span><button class="copy">{t("copy")}</button></div><pre>{html.escape(text)}</pre></div>'

def table(head, rows, cls=''):
    h = ''.join(f'<th>{c}</th>' for c in head)
    b = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<div class="table-wrap{(" " + cls) if cls else ""}"><table><tr>{h}</tr>{b}</table></div>'

def opts(rows):
    return table([t('opt'), t('default'), t('does')], [(f'<code>{a}</code>', b, c) for a, b, c in rows], 'stack')

def callout(kind, label, body):
    icon = {'note': 'M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20zM12 16v-4M12 8h.01', 'warn': IC['warn']}[kind]
    return f'<div class="callout {kind}"><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="{icon}"/></svg><div><strong class="label">{label}</strong>{body}</div></div>'

def term(inner, title='claude · ~/acme-api'):
    return (f'<div class="tw" data-search="skip"><div class="tw-bar" aria-hidden="true"><i></i><i></i><i></i><span>{title}</span></div>'
            f'<pre class="term">{inner}</pre></div>')

SPINNER = ('<span class="a spin">✻</span> Propagating… <span class="d">(6s · ↓ 90 tokens)</span>\n'
           '  <span class="d">⎿</span>  <b>Now:</b> Running the tests after the fix to the date filter')
PROMPT = '<span class="d">' + '─' * 64 + '</span>\n<span class="d">❯</span> \n<span class="d">' + '─' * 64 + '</span>'
PANEL_OUT = ('<span class="d">❯</span> /panel\n  <span class="d">⎿</span>  panel: http://localhost:7777\n'
             '     4 sessions: <b class="a">1 need you</b>, <span class="bl">2 working</span>.')
HUD_PANE = ('<b class="d">SESSION</b>   <b>Opus 5.5</b> · my-app  <span class="bl">main</span><span class="a">●</span> · 38m · 214 calls · ctx <span class="g">42%</span>\n'
            '<b class="d">LIMITS</b>    5h <span class="g">61%</span> <span class="d">resets 2h30m</span> · 7d <span class="g">44%</span> <span class="d">resets 3d20h</span>\n'
            '<b class="d">MEMORY</b>    session 1.5G · slice 3.0/5.0G · <span class="g">1.9G fits</span>\n'
            '<b class="d">NOW</b>       <span class="a">Bash</span> yarn turbo run test <span class="d">0:42</span> · 2 subagents\n'
            '<b class="d">TODAY</b>     2 skills · 1 loop nudge · 0 refusals')
BAND_PANEL = ('<b>Opus 5.5</b> · my-app  <span class="bl">main</span><span class="a">●</span>                              <span class="d">38m · 214 calls</span>\n'
              'ctx ' + G + '▰▰▰▰</span><span class="d">▱▱▱▱▱▱</span>  ' + G + '42%</span>   5h ' + G + '▰▰▰▰▰▰</span><span class="d">▱▱▱▱</span>  ' + G + '61%</span> <span class="d">resets 2h30m</span>   7d ' + G + '▰▰▰▰</span><span class="d">▱▱▱▱▱▱</span>  ' + G + '44%</span>   mem ' + G + '1.9G free</span>')
BAND_LINE = '<b>Opus 5.5</b> <span class="d">│</span> my-app  <span class="bl">main</span><span class="a">●</span> <span class="d">│</span> ctx ' + G + '42%</span> <span class="d">│</span> 5h ' + G + '61%</span> <span class="d">│</span> 7d ' + G + '44%</span> <span class="d">│</span> mem ' + G + '1.9G</span>'
INSTALL = 'claude plugin marketplace add joaosavi/cockpit\nclaude plugin install cockpit@cockpit'
UPDATE_ALL = 'claude plugin marketplace update cockpit\n' + "for m in $(claude plugin list | grep -o '[a-z-]*@cockpit'); do claude plugin update \"$m\"; done"
STATUS_JSON = '\n'.join(['{', '  "statusLine": { "type": "command", "command": "~/.claude/plugins/marketplaces/cockpit/hud/statusline/statusline.sh", "refreshInterval": 5 },',
                         '  "pluginConfigs": { "hud@cockpit": { "options": { "band": "off", "style": "refined", "icons": "nerd" } } }', '}'])
MANAGED_JSON = '\n'.join(['{', '  "enabledPlugins": { "global-memory@cockpit": true },', '  "prependPlugins": ["global-memory@cockpit", "sec-default@builtin"]', '}'])
ORDER = ['secret-guard', 'collision-guard', 'pipefail', 'memory-guard', 'loop-breaker', 'usage-limit', 'hud', 'spinner-status', 'panel', 'skill-loader', 'global-memory']

def install_one(name):
    return f'<h2>{t("only_h")}</h2><p>{t("only_p").format(n=name)}</p>' + code(f'claude plugin marketplace add joaosavi/cockpit\nclaude plugin install {name}@cockpit')

def diary(name, what):
    return f'<h2>{t("rec_h")}</h2><p><code>~/.local/state/mods/{name}/{t("day")}.jsonl</code>: {what} {t("rec_tail")}</p>'

def meta(version, *pills):
    out = f'<span class="pill mute">v{version}</span>' + ''.join(f'<span class="pill led">{p}</span>' for p in pills)
    return f'<div class="meta">{out}</div>'

def modgrid(items):
    out = '<div class="mods">'
    for name, _, desc, cmd in items:
        c = f' <span class="mod-cmd">{cmd}</span>' if cmd else ''
        out += f'<a class="mod" href="#{name}"><div class="mod-h"><code>{name}</code>{c}</div><p>{desc}</p></a>'
    return out + '</div>'

# --- Markdown export, for llms.txt ------------------------------------------------------------
SKIP = {'script', 'style', 'svg', 'button'}
VOID = {'input', 'br', 'img', 'hr', 'meta', 'link', 'wbr', 'source', 'col', 'area'}
SKIP_CLASS = {'crumb', 'copy', 'page-actions', 'meta', 'q-n', 'mod-cmd', 'tw-bar'}
INLINE = ('p', 'div')

class Markdown(HTMLParser):
    """Turns one article into Markdown. In-page links become absolute links to the page's .md file."""
    def __init__(self, md_base):
        super().__init__()
        self.base, self.out, self.skip, self.pre, self.stack, self.row, self.rows, self.card = md_base, [], 0, False, [], 0, 0, False
        self.inline, self.label = 0, False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in VOID:
            if tag == 'img' and not self.skip:
                self.out.append(f'\n![{a.get("alt", "")}]({BASE_URL}img/{a.get("src", "").rsplit("/", 1)[-1]})\n')
            return
        cls = set((a.get('class') or '').split())
        hide = tag in SKIP or bool(SKIP_CLASS & cls) or a.get('hidden') is not None and tag == 'pre'
        self.stack.append(hide)
        if hide:
            self.skip += 1
        if self.skip:
            return
        if tag == 'a' and 'mod' in cls:
            self.card = True
            self.stack[-1] = ('card', a.get('href') or '')
            self.out.append('\n- ')
            return
        if self.card:
            if tag == 'code':
                self.out.append('`')
            return
        if 'code-head' in cls:
            self.label = True
            self.out.append('\n')
            return
        if 'callout' in cls:
            self.stack[-1] = 'inline'
            self.inline += 1
            self.out.append('\n> ')
            return
        if self.inline and tag in INLINE:
            self.out.append(' ')
            return
        if tag in ('h1', 'h2', 'h3'):
            self.out.append('\n\n' + '#' * int(tag[1]) + ' ')
        elif tag == 'table':
            self.rows = 0
            self.out.append('\n')
        elif tag == 'tr':
            self.row = 0
            self.out.append('\n|')
        elif tag in ('p', 'div', 'ol', 'ul'):
            self.out.append('\n')
        elif tag == 'li':
            self.stack[-1] = 'inline'
            self.inline += 1
            self.out.append('\n- ')
        elif tag in ('td', 'th'):
            self.row += 1
            self.out.append(' ')
        elif tag == 'pre':
            self.pre = True
            self.out.append('\n```\n')
        elif tag == 'code' and not self.pre:
            self.out.append('`')
        elif tag in ('b', 'strong') and not self.pre:
            self.out.append('**')
        elif tag == 'a':
            self.stack[-1] = ('a', a.get('href') or '')
            self.out.append('[')

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        top = self.stack.pop() if self.stack else False
        if top is True:
            self.skip -= 1
            return
        if self.skip:
            return
        if top == 'inline':
            self.inline -= 1
            if tag != 'li':
                self.out.append('\n')
            return
        if self.label and tag == 'div':
            self.label = False
            self.out.append(':\n')
            return
        if self.inline and tag in INLINE and not isinstance(top, tuple):
            self.out.append(' ')
            return
        if isinstance(top, tuple) and top[0] == 'card':
            self.card = False
            self.out.append(f' [{t("more")}]({self.base}{top[1][1:]}.md)')
            return
        if self.card:
            if tag == 'code':
                self.out.append('`')
            elif tag == 'div':
                self.out.append(': ')
            return
        if tag in ('td', 'th'):
            self.out.append(' |')
        elif tag == 'tr':
            self.rows += 1
            if self.rows == 1:
                self.out.append('\n|' + ' --- |' * self.row)
        elif tag == 'pre':
            self.pre = False
            self.out.append('\n```\n')
        elif tag == 'code' and not self.pre:
            self.out.append('`')
        elif tag in ('b', 'strong') and not self.pre:
            self.out.append('**')
        elif tag in ('p', 'div', 'h1', 'h2', 'h3', 'ul', 'ol'):
            self.out.append('\n')
        elif isinstance(top, tuple):
            href = top[1]
            if href.startswith('#'):
                href = f'{self.base}{href[1:]}.md'
            self.out.append(f']({href})')

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data if self.pre else re.sub(r'\s+', ' ', data))

def to_markdown(article_html, md_base):
    p = Markdown(md_base)
    p.feed(article_html)
    parts = ''.join(p.out).split('```')
    text = '```'.join(x if i % 2 else re.sub(r'\n[ \t]+', '\n', re.sub(r'[ \t]+\n', '\n', x)) for i, x in enumerate(parts))
    text = re.sub(r'\*\*\s*\*\*', '', text)
    return html.unescape(re.sub(r'\n{3,}', '\n\n', text).strip()) + '\n'

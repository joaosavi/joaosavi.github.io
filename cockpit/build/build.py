#!/usr/bin/env python3
"""Builds the Cockpit docs: cockpit/index.html in English, cockpit/pt/index.html in Portuguese, and for each
language llms.txt, llms-full.txt and one md/<page>.md per page.

Run after changing a content file: python3 cockpit/build/build.py"""
import html, importlib, re, shutil, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib

OUT = lib.SITE / 'cockpit'

def build(lang, out):
    lib.LANG = lang
    c = importlib.import_module(f'content_{lang}')
    t = lib.t
    v = lib.VERS['cockpit']
    url = lib.BASE_URL + ('pt/' if lang == 'pt' else '')
    md_base = url + 'md/'

    nav = ''
    for g, icon, fold in c.GROUPS:
        caret = '<span class="ng-caret" aria-hidden="true"></span>' if fold else ''
        nav += f'  <div class="nav-group"><h4><button type="button" class="ng-toggle" aria-expanded="true">{lib.svg(icon, "2", "")}{g}{caret}</button></h4>\n'
        for pg, pid, ic, label, _, _ in c.P:
            if pg == g:
                nav += f'    <a href="#{pid}" data-id="{pid}"><span class="nav-ic">{lib.svg(ic)}</span><span class="lbl">{label}</span></a>\n'
        nav += '  </div>\n'

    arts, mds = '', []
    for i, (g, pid, _, _, title, body) in enumerate(c.P):
        mod = g in c.MOD_GROUPS
        h1 = f'<h1><code style="font-size:.82em;background:none;border:0;padding:0">{title}</code></h1>' if mod else f'<h1>{title}</h1>'
        actions = (f'<div class="page-actions"><button type="button" class="pa-copy" data-agent="{pid}">{t("agent")}</button>'
                   f'<a href="md/{pid}.md">{t("md")}</a><a href="llms.txt">{t("llms")}</a></div>')
        art = (f'<article class="page" id="{pid}" data-title="{html.escape(title)}"{"" if i == 0 else " hidden"}>\n'
               f'  <div class="crumb">{g}</div>\n  {h1}\n  {actions}\n{body.strip()}\n</article>\n\n')
        arts += art
        mds.append((pid, title, lib.to_markdown(art, md_base)))

    alt = t('alt_href')
    sw = (f'<a href="{alt if lang == "pt" else "./"}" data-lang-link{"" if lang == "pt" else " aria-current=\"true\""}>EN</a>'
          f'<a href="{alt if lang == "en" else "./"}" data-lang-link{" aria-current=\"true\"" if lang == "pt" else ""}>PT</a>')
    agent_js = '''
<script>
(function () {
  // the language switch keeps the page you are on
  document.querySelectorAll('[data-lang-link]').forEach(function (a) {
    a.addEventListener('click', function () { if (location.hash) a.href = a.getAttribute('href') + location.hash; });
  });
  // copy a request that points the reader's agent at the Markdown of this page
  document.querySelectorAll('[data-agent]').forEach(function (b) {
    b.addEventListener('click', function () {
      var text = TEXT.replace('{url}', MD + b.dataset.agent + '.md').replace('{idx}', IDX);
      var old = b.textContent;
      var ok = function () { b.textContent = DONE; setTimeout(function () { b.textContent = old; }, 1600); };
      try { navigator.clipboard.writeText(text).then(ok, function () { location.href = 'md/' + b.dataset.agent + '.md'; }); } catch (e) { location.href = 'md/' + b.dataset.agent + '.md'; }
    });
  });
})();
</script>'''.replace('TEXT', repr(t('agent_text'))).replace('MD +', repr(md_base) + ' +').replace('IDX', repr(url + 'llms.txt')).replace('DONE', repr('Copied' if lang == 'en' else 'Copiado'))

    doc = f'''<!doctype html>
<html lang="{t('html_lang')}" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{c.TITLE}</title>
<meta name="description" content="{c.DESCRIPTION}">
<link rel="alternate" hreflang="en" href="{lib.BASE_URL}">
<link rel="alternate" hreflang="pt-BR" href="{lib.BASE_URL}pt/">
<link rel="alternate" type="text/plain" title="llms.txt" href="llms.txt">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=Public+Sans:ital,wght@0,400;0,500;0,600;1,400&family=JetBrains+Mono:wght@400;500&display=swap">
{lib.HEAD_CSS}
{lib.EXTRA_CSS}
</head>
<body>

<header class="topbar">
  <button class="menu-btn" id="menuBtn" aria-controls="sidebar" aria-expanded="false" aria-label="{t('menu')}"><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
  <a class="site-home" href="{'../../' if lang == 'pt' else '../'}">joaosavi</a><span class="site-sep" aria-hidden="true">/</span>
  <a class="brand" href="#start" aria-label="{t('brand')}">
    <span class="mark" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="{lib.IC['gauge']}"/></svg></span>
    <span class="wordmark">Cockpit</span>
  </a>
  <div class="top-right"><nav class="lang-sw" aria-label="Language">{sw}</nav><a class="gh" href="https://github.com/joaosavi/cockpit" target="_blank" rel="noopener">{t('gh').format(v=v)}</a></div>
</header>

<div class="shell">
<nav class="sidebar" id="sidebar" aria-label="{t('pages')}">
  <div class="side-search"><svg viewBox="0 0 24 24" fill="none" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg><input id="q" type="search" placeholder="{t('search')}" autocomplete="off" aria-label="{t('search')}"><kbd aria-hidden="true">/</kbd></div>
  <p class="side-empty" id="sideEmpty" hidden>{t('empty')}</p>
{nav}</nav>

<main id="main">

{arts}<nav class="pager" id="pager" aria-label="{t('pager')}"></nav>
<div class="foot">{t('foot').format(v=v)}</div>
</main>

<aside class="toc" id="toc" aria-label="{t('toc')}"><h5>{t('toc')}</h5><div id="tocList"></div></aside>
</div>

<script>{lib.script(lang)}</script>
{agent_js}

</body></html>
'''
    out.mkdir(parents=True, exist_ok=True)
    (out / 'index.html').write_text(doc)
    md = out / 'md'
    if md.exists():
        shutil.rmtree(md)
    md.mkdir()
    for pid, _, text in mds:
        (md / f'{pid}.md').write_text(text)
    lines = [f'# Cockpit {v}', '', f'> {c.DESCRIPTION}', '', c.LLMS_INTRO, '']
    for g, _, _ in c.GROUPS:
        lines += [f'## {g}', '']
        lines += [f'- [{html.unescape(re.sub("<[^>]+>", "", title))}]({md_base}{pid}.md)' for pg, pid, _, _, title, _ in c.P if pg == g]
        lines.append('')
    lines += ['## Optional', '', f'- [{c.FULL_LABEL}]({url}llms-full.txt)', f'- [{c.OTHER_LABEL}]({lib.BASE_URL}{"llms.txt" if lang == "pt" else "pt/llms.txt"})', '']
    (out / 'llms.txt').write_text('\n'.join(lines))
    (out / 'llms-full.txt').write_text(f'# Cockpit {v}\n\n' + '\n\n---\n\n'.join(text for _, _, text in mds))
    print(lang, len(c.P), 'pages', len(doc), 'bytes')

(OUT / 'img').mkdir(parents=True, exist_ok=True)
for f in ('panel-dark.png', 'panel-mods.png'):
    shutil.copy(lib.COCKPIT / 'docs/shots' / f, OUT / 'img' / f)
build('en', OUT)
build('pt', OUT / 'pt')

#!/usr/bin/env python3
"""Gera always-on/txt/<id>.txt, um por mini-guia, para o agente do setup ler com curl.

Rode depois de mudar o index.html: python3 always-on/build-txt.py
"""
import html
import re
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKIP = {"script", "style", "svg", "button"}
# Tags sem fechamento: não entram na pilha, ou a pilha desalinha e o resto da página some.
VOID = {"input", "br", "img", "hr", "meta", "link", "wbr", "source", "col", "area"}
SKIP_CLASS = {"demo", "crumb", "copy", "page-actions", "done-btn", "vals", "membar", "progress", "unfold"}


class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.out, self.skip, self.pre, self.stack = [], 0, False, []
        self.row, self.rows = 0, 0

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            if tag == "br" and not self.skip:
                self.out.append("\n")
            return
        cls = dict(attrs).get("class") or ""
        hide = tag in SKIP or bool(SKIP_CLASS & set(cls.split()))
        self.stack.append(hide)
        if hide:
            self.skip += 1
        if self.skip:
            return
        if tag in ("h1", "h2", "h3"):
            self.out.append("\n\n" + "#" * int(tag[1]) + " ")
        elif tag == "table":
            self.rows = 0
            self.out.append("\n")
        elif tag == "tr":
            self.row = 0
            self.out.append("\n|")
        elif tag in ("p", "div", "ol", "ul"):
            self.out.append("\n")
        elif tag == "iframe":
            self.out.append("\nVídeo: " + (dict(attrs).get("src") or "") + "\n")
        elif tag == "li":
            self.out.append("\n- ")
        elif tag in ("td", "th"):
            self.row += 1
            self.out.append(" ")
        elif tag == "pre":
            self.pre = True
            self.out.append("\n```\n")
        elif tag == "code" and not self.pre:
            self.out.append("`")
        elif tag == "br":
            self.out.append("\n")
        elif tag == "small":
            self.out.append(", ")
        elif tag == "a":
            href = dict(attrs).get("href") or ""
            self.stack[-1] = ("a", href)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        top = self.stack.pop() if self.stack else False
        if top is True:
            self.skip -= 1
            return
        if self.skip:
            return
        if tag in ("td", "th"):
            self.out.append(" |")
        elif tag == "tr":
            self.rows += 1
            if self.rows == 1:
                self.out.append("\n|" + " --- |" * self.row)
        if tag == "pre":
            self.pre = False
            self.out.append("\n```\n")
        elif tag == "code" and not self.pre:
            self.out.append("`")
        elif tag == "b" and self.out and not self.pre:
            self.out.append(". ")
        elif isinstance(top, tuple) and top[1]:
            href = top[1]
            if href.startswith("#"):
                href = f"txt/{href[1:]}.txt"
            self.out.append(f" ({href})")

    def handle_data(self, data):
        if self.skip:
            return
        self.out.append(data if self.pre else re.sub(r"\s+", " ", data))


src = (HERE / "index.html").read_text()
pages = re.findall(r'(<article class="page" id="([^"]+)" data-title="([^"]+)".*?</article>)', src, re.S)
(HERE / "txt").mkdir(exist_ok=True)
for old in (HERE / "txt").glob("*.txt"):
    old.unlink()
index = ["# Claude Code Always-On: mini-guias em texto", "",
         "Cada linha é um mini-guia. Baixe com: curl -s https://joaosavi.github.io/always-on/txt/<id>.txt", ""]
for block, pid, title in pages:
    p = Text()
    p.feed(block)
    parts = "".join(p.out).split("```")
    # fora dos blocos de código, tira a indentação que sobra do HTML
    text = "```".join(x if i % 2 else re.sub(r"\n[ \t]+", "\n", x) for i, x in enumerate(parts))
    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"
    (HERE / "txt" / f"{pid}.txt").write_text(html.unescape(text))
    index.append(f"- {pid}: {html.unescape(title)}")
(HERE / "txt" / "index.txt").write_text("\n".join(index) + "\n")
print(f"{len(pages)} mini-guias em {HERE / 'txt'}")

# -*- coding: utf-8 -*-
"""把 chapters/ 与附录合并成整体版 《复变函数与积分变换_教案.md》。"""
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'build'))
import texbook as tb

NL = chr(10)


def read_md(p):
    with open(p, encoding='utf-8') as f:
        return f.read().strip()


def main():
    cfg = tb.load_cfg()
    parts = []
    for ch in cfg['chapters']:
        title, files = tb.read_manifest(ch)
        num = tb.chapter_no(ch)
        head = ('# 第 %s 章 · %s' % (num, title)) if num is not None else ('# ' + title)
        parts.append(head)
        for rel in files:
            if rel.lower() in ('README.md', 'readme.md'):
                continue
            p = os.path.join(ROOT, 'chapters', ch, rel)
            if os.path.isfile(p):
                parts.append(tb.shift_heading(read_md(p)))
        parts.append('')
    for ad in cfg.get('appendices') or []:
        appdir = os.path.join(ROOT, ad['dir'])
        title, files = tb.read_manifest_dir(appdir)
        parts.append('# ' + title)
        for rel in files:
            if rel.lower() in ('README.md', 'readme.md'):
                continue
            p = os.path.join(appdir, rel)
            if os.path.isfile(p):
                parts.append(read_md(p))
    text = (NL * 2).join(parts) + NL
    out = os.path.join(ROOT, '复变函数与积分变换_教案.md')
    with open(out, 'w', encoding='utf-8') as f:
        f.write(text)
    print('[merge] written', out, '(', len(text), 'chars )')


if __name__ == '__main__':
    main()

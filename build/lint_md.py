# -*- coding: utf-8 -*-
"""Markdown 教案语法检查：发现常见会导致 pandoc/xelatex 失败的写法。

用法: python build/lint_md.py [--fix] [paths...]
"""
import os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BS = chr(92)

CJK = re.compile('[\u4e00-\u9fff]')


def math_spans(text):
    """粗略找 $...$ 与 $$...$$ 片段。"""
    spans = []
    # display $$...$$
    for m in re.finditer(r'\$\$(.+?)\$\$', text, re.S):
        spans.append((m.start(), m.end(), m.group(1), 'display'))
    # inline $...$
    for m in re.finditer(r'(?<!\$)\$([^$]+?)\$(?!\$)', text):
        spans.append((m.start(), m.end(), m.group(1), 'inline'))
    return spans


def check_file(path):
    with open(path, encoding='utf-8') as f:
        text = f.read()
    problems = []
    lines = text.split('\n')
    # 单反斜杠的 \( \) \[ \]（\\[...] 是合法的行距，跳过）
    for pat, name in [(BS + '(', r'\( 转义'),
                      (BS + ')', r'\) 转义'),
                      (BS + '[', r'\[ 转义'),
                      (BS + ']', r'\] 转义')]:
        i = 0
        while True:
            j = text.find(pat, i)
            if j < 0:
                break
            # 前面还有一个反斜杠 => 是 \\[...]，跳过
            if j > 0 and text[j - 1] == BS:
                i = j + 1
                continue
            line_no = text.count('\n', 0, j) + 1
            problems.append((line_no, name + '：' + repr(text[j:j + 20])))
            i = j + 1
    # 数学块内的中文/中文标点（\text{...} 内的是允许的）
    for start, end, body, kind in math_spans(text):
        slim = re.sub(r'\\text\{[^{}]*\}', '', body)
        for ch in slim:
            if CJK.match(ch) or ch in '，。、；：！？（）':
                line_no = text.count('\n', 0, start) + 1
                problems.append((line_no, '数学块内非\text的中文：' + ch + ' ' + repr(body[:60])))
                break
    # 控制字符（如 \b 被误写为退格）
    for j, ch in enumerate(text):
        if ord(ch) < 32 and ord(ch) not in (9, 10, 13):
            line_no = text.count('\n', 0, j) + 1
            problems.append((line_no, '控制字符 U+%04X' % ord(ch)))
            break
    # 连续 $$ 计数
    if text.count('$$') % 2 != 0:
        problems.append((0, '$$ 数量为奇数'))
    for end in re.findall(re.escape(BS) + 'begin\{(.+?)\}', text):
        m = re.findall(re.escape(BS) + 'end\{(.+?)\}', text)
        if m.count(end) < 1:
            problems.append((0, '未闭合 \\begin{' + end + '}'))
    return problems


def main():
    args = sys.argv[1:]
    fix = '--fix' in args
    paths = [a for a in args if not a.startswith('--')]
    if not paths:
        paths = sorted(glob.glob(os.path.join(ROOT, 'chapters', '*', '*.md'))) + \
                sorted(glob.glob(os.path.join(ROOT, '附录', '*', '*.md')))
    total = 0
    for path in paths:
        problems = check_file(path)
        if problems:
            total += len(problems)
            print(os.path.relpath(path, ROOT))
            for line_no, msg in problems[:20]:
                print('   L%s: %s' % (line_no, msg))
            if len(problems) > 20:
                print('   ... and %d more' % (len(problems) - 20))
    print('checked %d files, %d problems' % (len(paths), total))
    sys.exit(1 if total else 0)


if __name__ == '__main__':
    main()

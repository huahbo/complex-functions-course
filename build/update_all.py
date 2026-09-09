#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""一键更新：生成清单 -> 每章PDF -> 全书PDF -> 可编译TeX工程 -> 合并整体MD。"""
import os, sys, subprocess

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run(cmd, name):
    print()
    print('===== ' + name + ' =====')
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True,
                       encoding='utf-8', errors='replace')
    tail = p.stdout.strip()[-2000:]
    print(tail if tail else '(no stdout)')
    if p.stderr.strip():
        print('--stderr--')
        print(p.stderr.strip()[-1000:])
    return p.returncode


def main():
    argv = sys.argv[1:]
    no_compile = '--no-tex-compile' in argv
    codes = []
    codes.append(run([sys.executable, 'build/gen_manifest.py'], '1) 生成各章 pdf_manifest.txt'))
    codes.append(run([sys.executable, 'build/pdf_build.py'], '2) 每章 PDF'))
    codes.append(run([sys.executable, 'build/texbook.py', '--full'], '3) 全书 PDF'))
    tex_cmd = [sys.executable, 'build/emit_tex.py'] + ([] if no_compile else ['--compile'])
    codes.append(run(tex_cmd, '4) 可编译 TeX 工程' + ('（仅生成，不编译）' if no_compile else '')))
    codes.append(run([sys.executable, 'build/merge_md.py'], '5) 合并整体 MD'))
    print()
    print('ALL DONE  exit_codes=', codes)
    return 0 if all(c == 0 for c in codes) else 1


if __name__ == '__main__':
    sys.exit(main())

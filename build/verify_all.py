#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""最终校验：lint -> manifest check -> 每章PDF -> 全书PDF -> TeX -> merge。"""
import os, sys, subprocess

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run(cmd, name, must=True):
    print()
    print('===== ' + name + ' =====')
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True,
                       encoding='utf-8', errors='replace')
    tail = p.stdout.strip()[-2500:]
    print(tail if tail else '(no stdout)')
    if p.stderr.strip():
        print('--stderr--')
        print(p.stderr.strip()[-1500:])
    if must and p.returncode != 0:
        print('!! FAILED:', name)
    return p.returncode


def main():
    codes = []
    codes.append(run([sys.executable, 'build/lint_md.py'], '0) lint md'))
    codes.append(run([sys.executable, 'build/gen_manifest.py'], '1) gen manifests'))
    codes.append(run([sys.executable, 'build/pdf_build.py'], '2) per-chapter PDFs'))
    codes.append(run([sys.executable, 'build/texbook.py', '--full'], '3) full book PDF'))
    codes.append(run([sys.executable, 'build/emit_tex.py', '--compile'], '4) TeX compile'))
    codes.append(run([sys.executable, 'build/merge_md.py'], '5) merge MD'))
    print()
    print('VERIFY DONE  exit_codes=', codes)
    return 0 if all(c == 0 for c in codes) else 1


if __name__ == '__main__':
    sys.exit(main())

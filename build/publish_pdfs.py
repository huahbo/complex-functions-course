#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish all chapter / appendix / full-book PDFs to a dedicated single-commit branch.

Usage:
  python build/publish_pdfs.py
  python build/publish_pdfs.py --branch pdf --pdf-dir _pdfs --dry-run

The target branch is rebuilt from a throw-away repository and force-pushed, so it
always contains exactly ONE commit with the newest PDFs only: repeated builds never
accumulate old binary versions in the repository history.
Credentials come from the normal git machinery (CI: the credential persisted by
actions/checkout; local: the configured credential helper).
"""
import argparse
import glob
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_PDF_DIR = os.path.join(ROOT, "教材PDF")
BRANCH_README = [
    "# 教材 PDF 成品（构建产物）",
    "",
    "本分支由 main 分支的 build/publish_pdfs.py 自动发布：**永远只有一个提交，只保留最新一次构建的成品**，",
    "以免 PDF 二进制在仓库历史里反复累积。",
    "",
    "- 每章 PDF：01-复数和复平面 ～ 09-快速傅里叶变换",
    "- 习题与参考答案(附录).pdf",
    "- 复变函数与积分变换_教案.pdf（全书）",
    "",
    "内容源在 main 分支的 chapters/ 与 附录/ 目录；讲义的修改与勘误请提交到 main，",
    "由 CI 重新构建后再刷新本分支。",
    "",
]


def run(cmd, cwd=None, check=True):
    env = dict(os.environ)
    env["GIT_TERMINAL_PROMPT"] = "0"
    proc = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
    if check and proc.returncode != 0:
        sys.stderr.write("command failed: " + " ".join(cmd) + chr(10))
        sys.stderr.write((proc.stdout or "") + (proc.stderr or ""))
        raise SystemExit(proc.returncode)
    return proc


def collect_pdfs(pdf_dir):
    found = glob.glob(os.path.join(pdf_dir, "**", "*.pdf"), recursive=True)
    keep = []
    for path in found:
        parts = os.path.normpath(path).split(os.sep)
        if "_pilot" in parts:
            continue
        keep.append(path)
    return sorted(keep)


def credential_args(repo):
    """Reuse the http extraheader credential that actions/checkout stores locally."""
    proc = run(["git", "config", "--get-regexp", "^http[.].*extraheader$"], cwd=repo, check=False)
    args = []
    for line in (proc.stdout or "").splitlines():
        key, sep, value = line.partition(" ")
        if sep and key.strip():
            args.extend(["-c", key.strip() + "=" + value.strip()])
    return args


def default_remote():
    env_remote = os.environ.get("PDF_PUBLISH_REMOTE")
    if env_remote:
        return env_remote
    proc = run(["git", "remote", "get-url", "origin"], cwd=ROOT, check=False)
    return (proc.stdout or "").strip()


def init_repo(tmp, branch):
    proc = run(["git", "init", "-q", "-b", branch], cwd=tmp, check=False)
    if proc.returncode != 0:
        run(["git", "init", "-q"], cwd=tmp)
        run(["git", "symbolic-ref", "HEAD", "refs/heads/" + branch], cwd=tmp)


def main():
    ap = argparse.ArgumentParser(description="publish PDFs to a single-commit branch")
    ap.add_argument("--pdf-dir", default=DEFAULT_PDF_DIR, help="directory holding the built PDFs")
    ap.add_argument("--branch", default="pdf", help="target branch, always single-commit")
    ap.add_argument("--remote", default=None, help="remote URL (default: PDF_PUBLISH_REMOTE or origin)")
    ap.add_argument("--message", default="PDF 成品：仅最新一次构建", help="commit message")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    pdfs = collect_pdfs(args.pdf_dir)
    if not pdfs:
        raise SystemExit("no PDF found under " + args.pdf_dir)
    total = sum(os.path.getsize(p) for p in pdfs)
    print("collected " + str(len(pdfs)) + " pdf, " + str(round(total / 1048576.0, 2)) + " MB")
    for path in pdfs:
        print("  " + os.path.basename(path))

    remote = args.remote or default_remote()
    if not remote:
        raise SystemExit("no remote: pass --remote or set PDF_PUBLISH_REMOTE")
    if args.dry_run:
        print("dry-run: nothing pushed to " + args.branch)
        return 0

    tmp = tempfile.mkdtemp(prefix="pdf-publish-")
    try:
        for path in pdfs:
            shutil.copy2(path, os.path.join(tmp, os.path.basename(path)))
        with open(os.path.join(tmp, "README.md"), "w", encoding="utf-8") as fh:
            fh.write(chr(10).join(BRANCH_README))
        init_repo(tmp, args.branch)
        run(["git", "add", "-A"], cwd=tmp)
        run(["git",
             "-c", "user.name=pdf-publisher",
             "-c", "user.email=pdf-publisher@users.noreply.github.com",
             "commit", "-q", "-m", args.message], cwd=tmp)
        head = run(["git", "rev-parse", "--short", "HEAD"], cwd=tmp).stdout.strip()
        push = ["git"] + credential_args(ROOT) + ["push", "--force", remote,
                                               "HEAD:refs/heads/" + args.branch]
        run(push, cwd=tmp)
        print("published " + str(len(pdfs)) + " pdf as single commit " + head
              + " to branch " + args.branch + " of " + remote)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

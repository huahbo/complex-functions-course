# 复变函数与积分变换 · 教案项目

本项目将《复变函数与积分变换（第3版）》（北京邮电大学出版社，编写组）课程讲义整理为**可编辑的 Markdown / LaTeX / PDF 教案**，并配套 GitHub Actions CI：修改内容后自动重新生成每一章 PDF、全书 PDF、可编译 LaTeX 工程和合并版 Markdown。

## 内容范围

- **第1–5章（复变函数部分）**：由 5 个 PowerPoint 幻灯片 PDF 转写，逐页提取正文、公式与插图，并补充“本节目标 / 重点难点 / 常见错误 / 小结”等教案内容；
- **第6–9章（共形映射、傅里叶变换、拉普拉斯变换、快速傅里叶变换）**：按官方目录完整补充；
- **附录**：各章主要习题与参考答案（整理自经典教材与公开讲义）。

## 目录结构

- `chapters/`：唯一内容源（Markdown + images）
- `教材PDF/`：每章 PDF + 全书 PDF + 附录 PDF（生成物，不入主干；构建后由 `build/publish_pdfs.py` 发布到单提交的 `pdf` 分支）
- `教材TeX/`：可编译 LaTeX 工程（main.tex 及各章 chNN.tex）
- `复变函数与积分变换_教案.md`：整体合并版 Markdown
- `build/`：提取、转写辅助、构建与校验脚本
- `原始资料/`：原始幻灯片 PDF（版权考虑，**不入库**）
- `_work/`、`_research/`：本地中间产物（不入库）

## 日常更新流程

修改 `chapters/NN-xxx/*.md` 或图片后，运行：

```bash
python build/update_all.py
```

或在 GitHub 上 push 后等待 Actions 自动构建，到 Actions 页面下载：
- **curriculum-pdfs**：每章 PDF + 全书 PDF + 附录 PDF；
- **tex-project-and-merged-md**：可编译 TeX 工程 + 合并版 MD。

成品 PDF 不入主干，而是集中放在独立的 **pdf 分支**：一个永远只有单个提交的分支，只保留最新一次构建的成品，仓库历史不会随反复构建而膨胀。

下载入口（直接点开即可在线阅读或下载，不必等 CI）：

- 分支页面：https://github.com/huahbo/complex-functions-course/tree/pdf
- 内容：`01-复数和复平面` ～ `09-快速傅里叶变换` 每章 PDF、`习题与参考答案(附录).pdf`、`复变函数与积分变换_教案.pdf`（全书）

本地重新构建后发布：`python build/publish_pdfs.py`（默认推送到 origin 的 `pdf` 分支，同样是单提交覆盖旧版本）。

## 常用命令

```bash
python build/gen_manifest.py            # 同步各章文件清单
python build/pdf_build.py 01-复数和复平面   # 单章 PDF
python build/texbook.py --full          # 全书 PDF + 附录 PDF
python build/emit_tex.py --compile      # 可编译 LaTeX 工程
python build/merge_md.py                # 合并整体 MD
python build/lint_md.py                 # Markdown/LaTeX 语法检查
python build/verify_all.py              # 一键本地全量校验（等价 CI）
python build/publish_pdfs.py            # 发布最新 PDF 到单提交 pdf 分支
```

## GitHub Actions

- 触发：push 到 `chapters/`、`附录/`、`build/`、`README.md`、`.github/workflows/build.yml`，或手动 Run workflow；
- 环境：Ubuntu + TeX Live + pandoc + Noto CJK 字体；
- 产物：PDF 以 Actions Artifact 形式供下载，同时由 `publish` 任务把最新成品强制推送到单提交的 `pdf` 分支；TeX 工程与合并 MD 仍以 Artifact 形式提供。

## 版权与免责声明

> 本项目为**个人教学整理**：
>
> 1. 内容基于《复变函数与积分变换（第3版）》（北京邮电大学出版社，编写组）及公开教学资料二次整理；
> 2. **原始教材/幻灯片 PDF 未包含在本仓库中**，`pdf` 分支内的 PDF 均为本项目自行排版的教案成品；
> 3. 内容仅供个人学习与教学参考，**请勿用于商业传播**；
> 4. 若涉及版权问题，请联系作者删除或调整相关内容；
> 5. 第1–5章公式由幻灯片转写并经过 AI 辅助校对，第6–9章为依据标准知识的补充稿，可能存在笔误，**请以正式教材为准**；
> 6. 附录习题与答案整理自经典教材/公开讲义，编号与题目可能与原书不完全一致。

## 注意事项

- 内容源永远是 `chapters/` 下的 Markdown；
- `教材PDF/`、`教材TeX/` 是生成物；版式定制请改 `build/cover.tex`、`build/texbook_header.tex` 或 `教材TeX/user_style.tex`；
- `教材PDF/` 是本地生成目录，整个目录不入主干（已在 `.gitignore` 中忽略，含单章试验输出 `_pilot/`）；成品统一发布到 `pdf` 分支，无需手动提交 PDF；
- 若需要在线网页版（docsify + GitHub Pages），可在后续增加。

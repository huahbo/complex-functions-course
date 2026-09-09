# -*- coding: utf-8 -*-
"""从 原始资料/*.pdf 提取每页文字、嵌入图和页面截图，供转写使用。

输出:
  _work/raw/<ch>/page-XX.txt     每页文字（PyMuPDF 提取，中文正常）
  _work/pages/<ch>/pXX.png       每页渲染图（110dpi，供人工/AI 核对方程与图）
  chapters/<ch>/images/fig-pXX.png  从 PDF 中抽取的独立嵌入图
"""
import os, sys, glob, hashlib, shutil
import fitz

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, '原始资料')
WORK = os.path.join(ROOT, '_work')
NL = chr(10)

MAP = {
    '第一章': '01-复数和复平面',
    '第二章': '02-解析函数',
    '第三章': '03-复变函数的积分',
    '第四章': '04-解析函数的级数表示法',
    '第五章': '05-留数理论及其应用',
}


def chname(pdf):
    base = os.path.basename(pdf)
    for key, val in MAP.items():
        if key in base:
            return val
    raise RuntimeError('unknown pdf: ' + base)


def extract(pdf):
    ch = chname(pdf)
    raw_dir = os.path.join(WORK, 'raw', ch)
    pages_dir = os.path.join(WORK, 'pages', ch)
    img_dir = os.path.join(ROOT, 'chapters', ch, 'images')
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(pages_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)
    doc = fitz.open(pdf)
    seen = {}
    print('==== ' + os.path.basename(pdf) + ' -> ' + ch + ' (' + str(len(doc)) + ' pages) ====')
    for i, page in enumerate(doc):
        pno = i + 1
        text = page.get_text()
        with open(os.path.join(raw_dir, 'page-%02d.txt' % pno), 'w', encoding='utf-8') as f:
            f.write('>>>>>> 第 %d 页 ' % pno + NL)
            f.write(text + NL)
        # 页面渲染图（110 dpi）
        pix = page.get_pixmap(dpi=110)
        pix.save(os.path.join(pages_dir, 'p%02d.png' % pno))
        # 嵌入图：按 xref 去重
        for im in page.get_images(full=True):
            xref = im[0]
            if xref in seen:
                continue
            info = doc.extract_image(xref)
            h = hashlib.sha256(info['image']).hexdigest()[:16]
            ext = info['ext']
            if ext == 'jpeg':
                ext = 'jpg'
            fn = 'fig-p%02d-%s.%s' % (pno, h[:8], ext)
            with open(os.path.join(img_dir, fn), 'wb') as fo:
                fo.write(info['image'])
            seen[xref] = fn
            print('   img p%02d xref=%d -> %s (%dx%d, %d bytes)' % (pno, xref, fn, info['width'], info['height'], len(info['image'])))
    # 汇总每章文字到 transcript
    tr = os.path.join(WORK, 'raw', ch, 'transcript.txt')
    with open(tr, 'w', encoding='utf-8') as f:
        f.write('# ' + ch + ' 原始幻灯片文字层' + NL + NL)
        for pno in range(1, len(doc) + 1):
            p = os.path.join(raw_dir, 'page-%02d.txt' % pno)
            with open(p, encoding='utf-8') as fh:
                f.write(fh.read() + NL)
    print('   transcript:', tr)


def main():
    os.makedirs(WORK, exist_ok=True)
    pdfs = sorted(glob.glob(os.path.join(SRC, '*.pdf')))
    for pdf in pdfs:
        extract(pdf)
    print('DONE')


if __name__ == '__main__':
    main()

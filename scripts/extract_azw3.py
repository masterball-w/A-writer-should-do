#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""azw3 (KF8) 正文与索引式 TOC 提取脚本（A-writer-should-do 母 Skill 配套脚本）。

用法：
    python extract_azw3.py 输入.azw3 [-o 输出目录]

输出（UTF-8）：
    {输入文件名}_fulltext.txt  去除 style/script/标签后的纯正文
    {输入文件名}_toc.txt       索引式目录，每行：序号<TAB>标题<TAB>字符偏移

处理策略（按顺序尝试）：
    1. 优先使用 calibre 的 ebook-convert 将 azw3 转为 epub，再复用 extract_epub.py
       （azw3 为 Kindle KF8 私有容器，转 epub 是保真度最高的通用路径）
    2. calibre 不可用时，回退到 pip 包 mobi（pip install mobi）解包
    3. TOC 随 epub 的 NCX/nav 一并提取，缺失时用 h1-h6 标题索引兜底

注意：DRM 保护的 azw3 文件无法直接解包，须先自行移除 DRM。
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


def convert_with_calibre(input_path, workdir):
    exe = shutil.which('ebook-convert')
    if not exe:
        return None
    epub_out = os.path.join(workdir, 'converted.epub')
    result = subprocess.run([exe, input_path, epub_out],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if result.returncode == 0 and os.path.isfile(epub_out):
        return epub_out
    return None


def run_epub_extract(epub_path, outdir):
    import extract_epub
    saved_argv = sys.argv
    sys.argv = ['extract_epub.py', epub_path, '-o', outdir]
    try:
        extract_epub.main()
    finally:
        sys.argv = saved_argv


def run_mobi_fallback(input_path, outdir):
    import extract_mobi
    saved_argv = sys.argv
    sys.argv = ['extract_mobi.py', input_path, '-o', outdir]
    try:
        extract_mobi.main()
    finally:
        sys.argv = saved_argv


def main():
    parser = argparse.ArgumentParser(description='提取 azw3 正文与索引式 TOC')
    parser.add_argument('book', help='输入的 .azw3 文件路径')
    parser.add_argument('-o', '--outdir', help='输出目录，默认与输入文件同目录')
    args = parser.parse_args()

    input_path = args.book
    if not os.path.isfile(input_path):
        sys.exit('错误：找不到文件 %s' % input_path)
    outdir = args.outdir or os.path.dirname(os.path.abspath(input_path))
    stem = os.path.splitext(os.path.basename(input_path))[0]

    workdir = tempfile.mkdtemp(prefix='azw3_extract_')
    try:
        epub_path = convert_with_calibre(input_path, workdir)
        if epub_path:
            run_epub_extract(epub_path, outdir)
            for suffix in ('_fulltext.txt', '_toc.txt'):
                src = os.path.join(outdir, 'converted' + suffix)
                dst = os.path.join(outdir, stem + suffix)
                if os.path.isfile(src):
                    os.replace(src, dst)
            print('正文与目录已按 %s 前缀输出到：%s' % (stem, outdir))
            return

        print('提示：未找到 calibre（ebook-convert），尝试 mobi 包回退方案')
        try:
            run_mobi_fallback(input_path, outdir)
        except SystemExit as exc:
            if exc.code not in (None, 0):
                sys.exit('错误：azw3 提取失败。请安装以下任一依赖后重试：\n'
                         '  1) calibre（提供 ebook-convert 命令，推荐）\n'
                         '  2) pip install mobi\n'
                         '若文件含 DRM，须先自行移除 DRM。')
            raise
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


if __name__ == '__main__':
    main()

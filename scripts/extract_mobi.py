#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mobi 正文与索引式 TOC 提取脚本（A-writer-should-do 母 Skill 配套脚本）。

用法：
    python extract_mobi.py 输入.mobi [-o 输出目录]

输出（UTF-8）：
    {输入文件名}_fulltext.txt  去除 style/script/标签后的纯正文
    {输入文件名}_toc.txt       索引式目录，每行：序号<TAB>标题<TAB>字符偏移

处理策略（按顺序尝试）：
    1. 优先使用 pip 包 mobi（pip install mobi）直接解包出 HTML 正文
    2. mobi 包不可用时，回退到 calibre 的 ebook-convert 转 epub 后复用 extract_epub.py
    3. TOC 优先取解包目录中的 .ncx，缺失时用 h1-h6 标题索引兜底

注意：DRM 保护的 mobi 文件无法直接解包，须先自行移除 DRM。
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _text_clean import extract_heading_index, html_to_text  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

NCX_NS = 'http://www.daisy.org/z3986/2005/ncx/'


def _read_text(path):
    with open(path, 'rb') as f:
        data = f.read()
    for encoding in ('utf-8', 'gbk', 'latin-1'):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode('utf-8', 'ignore')


def _gather_html_files(tmpdir):
    htmls = []
    for root, _dirs, files in os.walk(tmpdir):
        for name in files:
            lower = name.lower()
            if lower.endswith(('.htm', '.html', '.xhtml')):
                htmls.append(os.path.join(root, name))

    def priority(path):
        lower = os.path.basename(path).lower()
        if lower.startswith('index') or lower.startswith('main') \
                or lower.startswith('book') or lower.startswith('part'):
            return 0
        return 1

    htmls.sort(key=lambda p: (priority(p), len(p), p))
    return htmls


def _parse_ncx_file(ncx_path):
    try:
        root = ET.parse(ncx_path).getroot()
    except ET.ParseError:
        return []
    entries = []

    def walk(node, depth):
        for child in node:
            if child.tag == '{%s}navPoint' % NCX_NS:
                label = ''
                for sub in child:
                    if sub.tag == '{%s}navLabel' % NCX_NS:
                        for t in sub.iter():
                            if t.tag == '{%s}text' % NCX_NS and t.text:
                                label += t.text
                if label.strip():
                    entries.append((depth, ' '.join(label.split())))
                walk(child, depth + 1)

    for node in root:
        if node.tag == '{%s}navMap' % NCX_NS:
            walk(node, 0)
    return entries


def extract_with_mobi(input_path, tmpdir):
    import mobi  # noqa: F401
    tempdir, filepath = mobi.extract(input_path)
    return tempdir, filepath


def convert_with_calibre(input_path, tmpdir):
    exe = shutil.which('ebook-convert')
    if not exe:
        return None
    epub_out = os.path.join(tmpdir, 'converted.epub')
    result = subprocess.run([exe, input_path, epub_out],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if result.returncode == 0 and os.path.isfile(epub_out):
        return epub_out
    return None


def main():
    parser = argparse.ArgumentParser(description='提取 mobi 正文与索引式 TOC')
    parser.add_argument('book', help='输入的 .mobi 文件路径')
    parser.add_argument('-o', '--outdir', help='输出目录，默认与输入文件同目录')
    args = parser.parse_args()

    input_path = args.book
    if not os.path.isfile(input_path):
        sys.exit('错误：找不到文件 %s' % input_path)
    outdir = args.outdir or os.path.dirname(os.path.abspath(input_path))
    stem = os.path.splitext(os.path.basename(input_path))[0]

    workdir = tempfile.mkdtemp(prefix='mobi_extract_')
    try:
        # 策略1：mobi pip 包解包
        unpack_dir = None
        try:
            unpack_dir, _filepath = extract_with_mobi(input_path, workdir)
        except ImportError:
            print('提示：未安装 mobi 包（pip install mobi），尝试 calibre 回退方案')
        except Exception as exc:
            print('提示：mobi 包解包失败（%s），尝试 calibre 回退方案' % exc)

        if unpack_dir and os.path.isdir(unpack_dir):
            html_files = _gather_html_files(unpack_dir)
            if not html_files:
                sys.exit('错误：解包目录中未找到 HTML 正文')
            texts = []
            doc_offsets = {}
            offset = 0
            for path in html_files:
                text = html_to_text(_read_text(path))
                if not text.strip():
                    continue
                doc_offsets[path] = offset
                texts.append(text)
                offset += len(text) + 1
            fulltext = '\n'.join(texts)
            if not fulltext.strip():
                sys.exit('错误：未能提取到任何正文文本')

            # TOC：优先 ncx，缺失时用标题兜底
            ncx_files = []
            for root, _dirs, files in os.walk(unpack_dir):
                for name in files:
                    if name.lower().endswith('.ncx'):
                        ncx_files.append(os.path.join(root, name))
            toc_entries = []
            for ncx_path in ncx_files:
                toc_entries = _parse_ncx_file(ncx_path)
                if toc_entries:
                    break
            if toc_entries:
                # ncx 无正文偏移映射时，按顺序均分定位不可靠，此处偏移记为章节序号对应文档起点
                offsets = sorted(doc_offsets.values())
                toc_out = []
                for i, (depth, title) in enumerate(toc_entries):
                    pos = offsets[i] if i < len(offsets) else 0
                    toc_out.append((depth, title, pos))
            else:
                toc_out = []
                for path in doc_offsets:
                    html = _read_text(path)
                    base = doc_offsets[path]
                    for title, html_pos in extract_heading_index(html):
                        toc_out.append((0, title, base + len(html_to_text(html[:html_pos]))))
        else:
            # 策略2：calibre 转 epub 后复用 epub 提取逻辑
            epub_path = convert_with_calibre(input_path, workdir)
            if not epub_path:
                sys.exit('错误：缺少解包依赖。请先安装其一：\n'
                         '  1) pip install mobi\n'
                         '  2) calibre（提供 ebook-convert 命令）\n'
                         '若文件含 DRM，须先自行移除 DRM。')
            import extract_epub
            sys.argv = ['extract_epub.py', epub_path, '-o', outdir]
            extract_epub.main()
            # epub 输出以 converted 命名，重命名为原文件名
            for suffix in ('_fulltext.txt', '_toc.txt'):
                src = os.path.join(outdir, 'converted' + suffix)
                dst = os.path.join(outdir, stem + suffix)
                if os.path.isfile(src):
                    os.replace(src, dst)
            print('正文与目录已按 %s 前缀输出到：%s' % (stem, outdir))
            return

        full_path = os.path.join(outdir, '%s_fulltext.txt' % stem)
        toc_path = os.path.join(outdir, '%s_toc.txt' % stem)
        with open(full_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(fulltext)
        toc_lines = ['%d\t%s%s\t%d' % (i + 1, '  ' * depth, title, pos)
                     for i, (depth, title, pos) in enumerate(toc_out)]
        with open(toc_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(toc_lines))
        print('正文已输出：%s（%d 字符）' % (full_path, len(fulltext)))
        print('目录已输出：%s（%d 个条目）' % (toc_path, len(toc_lines)))
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


if __name__ == '__main__':
    main()

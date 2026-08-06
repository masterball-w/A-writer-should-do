#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""epub 正文与索引式 TOC 提取脚本（A-writer-should-do 母 Skill 配套脚本）。

用法：
    python extract_epub.py 输入.epub [-o 输出目录]

输出（UTF-8）：
    {输入文件名}_fulltext.txt  去除 style/script/head/标签后的纯正文，按阅读顺序（spine）拼接
    {输入文件名}_toc.txt       索引式目录，每行：序号<TAB>层级缩进+标题<TAB>字符偏移
                               （偏移指向该条目对应内容在 _fulltext.txt 中的起始位置）

处理规则：
    1. 通过 META-INF/container.xml 定位 content.opf，按 spine 顺序拼接正文文档
    2. 去除 style/script/head/注释/标签等与文字无关的元素，只保留正文文本
    3. TOC 来源优先级：toc.ncx（NCX navMap）> EPUB3 nav 文档 > h1-h6 标题索引兜底

仅依赖 Python 标准库。
"""

import argparse
import os
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from urllib.parse import unquote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _text_clean import extract_heading_index, html_to_text  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

NCX_NS = 'http://www.daisy.org/z3986/2005/ncx/'


def _read_member(zf, path):
    try:
        data = zf.read(path)
    except KeyError:
        return None
    for encoding in ('utf-8', 'gbk', 'latin-1'):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode('utf-8', 'ignore')


def _norm(base_dir, href):
    href = unquote(href.split('#')[0].split('?')[0]).replace('\\', '/')
    if not href:
        return None
    joined = '/'.join(part for part in (base_dir + '/' + href).split('/') if part not in ('', '.'))
    parts = []
    for part in joined.split('/'):
        if part == '..':
            if parts:
                parts.pop()
        else:
            parts.append(part)
    return '/'.join(parts)


def _parse_opf(zf, opf_path):
    opf_text = _read_member(zf, opf_path)
    if opf_text is None:
        return [], None
    try:
        root = ET.fromstring(opf_text)
    except ET.ParseError:
        return [], None
    base_dir = os.path.dirname(opf_path).replace('\\', '/')
    manifest = {}
    for item in root.iter():
        if item.tag.endswith('}item') or item.tag == 'item':
            iid = item.get('id')
            href = item.get('href')
            if iid and href:
                manifest[iid] = _norm(base_dir, href)
    ncx_path = None
    for item in root.iter():
        tag = item.tag.split('}')[-1]
        if tag == 'item' and (item.get('media-type') == 'application/x-dtbncx+xml'
                              or (item.get('href') or '').lower().endswith('.ncx')):
            ncx_path = _norm(base_dir, item.get('href'))
            break
    spine = []
    for itemref in root.iter():
        tag = itemref.tag.split('}')[-1]
        if tag == 'itemref':
            idref = itemref.get('idref')
            if idref and idref in manifest:
                spine.append(manifest[idref])
    return spine, ncx_path


def _parse_ncx(zf, ncx_path):
    text = _read_member(zf, ncx_path)
    if text is None:
        return []
    try:
        root = ET.fromstring(text)
    except ET.ParseError:
        return []
    entries = []

    def walk(node, depth):
        for child in node:
            if child.tag == '{%s}navPoint' % NCX_NS:
                label = ''
                src = ''
                for sub in child:
                    if sub.tag == '{%s}navLabel' % NCX_NS:
                        for t in sub.iter():
                            if t.tag == '{%s}text' % NCX_NS and t.text:
                                label += t.text
                    elif sub.tag == '{%s}content' % NCX_NS:
                        src = sub.get('src') or ''
                if label.strip():
                    entries.append((depth, re.sub(r'\s+', ' ', label.strip()), src))
                walk(child, depth + 1)

    for node in root:
        if node.tag == '{%s}navMap' % NCX_NS:
            walk(node, 0)
    return entries


def _parse_nav(zf, nav_path):
    text = _read_member(zf, nav_path)
    if text is None:
        return []
    match = re.search(r'<nav\b[^>]*epub:type=["\']toc["\'][^>]*>(.*?)</nav>',
                      text, re.IGNORECASE | re.DOTALL)
    if not match:
        return []
    block = match.group(1)
    entries = []
    li_re = re.compile(r'<li\b[^>]*>(.*?)</li>', re.IGNORECASE | re.DOTALL)
    a_re = re.compile(r'<a\b([^>]*)>(.*?)</a>', re.IGNORECASE | re.DOTALL)
    href_re = re.compile(r'href\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE)
    for li in li_re.finditer(block):
        m = a_re.search(li.group(1))
        if not m:
            continue
        href_match = href_re.search(m.group(1))
        label = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        if not label or not href_match:
            continue
        entries.append((0, re.sub(r'\s+', ' ', label), href_match.group(1)))
    return entries


def _map_offsets(doc_offsets, entries, base_dir):
    """把 TOC 条目的 href 映射为 fulltext 字符偏移。"""
    result = []
    for depth, title, src in entries:
        target = _norm(base_dir, src) if src else None
        offset = doc_offsets.get(target)
        if offset is not None:
            result.append((depth, title, offset))
    return result


def _heading_fallback(spine_paths, htmls, doc_offsets):
    """NCX/nav 缺失时，用各正文文档的 h1-h6 标题构建索引式 TOC。"""
    entries = []
    for path, html in zip(spine_paths, htmls):
        doc_offset = doc_offsets.get(path, 0)
        for title, html_pos in extract_heading_index(html):
            text_offset = len(html_to_text(html[:html_pos]))
            entries.append((0, title, doc_offset + text_offset))
        if len(entries) > 500:
            break
    return entries


def _build_fulltext(zf, spine):
    seen = set()
    texts = []
    htmls = []
    doc_offsets = {}
    spine_paths = []
    offset = 0
    for path in spine:
        if path in seen:
            continue
        seen.add(path)
        html = _read_member(zf, path)
        if html is None:
            continue
        text = html_to_text(html)
        if not text.strip():
            continue
        doc_offsets[path] = offset
        texts.append(text)
        htmls.append(html)
        spine_paths.append(path)
        offset += len(text) + 1
    return '\n'.join(texts), doc_offsets, spine_paths, htmls


def main():
    parser = argparse.ArgumentParser(description='提取 epub 正文与索引式 TOC')
    parser.add_argument('epub', help='输入的 .epub 文件路径')
    parser.add_argument('-o', '--outdir', help='输出目录，默认与输入文件同目录')
    args = parser.parse_args()

    epub_path = args.epub
    if not os.path.isfile(epub_path):
        sys.exit('错误：找不到文件 %s' % epub_path)
    outdir = args.outdir or os.path.dirname(os.path.abspath(epub_path))
    stem = os.path.splitext(os.path.basename(epub_path))[0]

    with zipfile.ZipFile(epub_path) as zf:
        container = _read_member(zf, 'META-INF/container.xml')
        opf_path = None
        if container:
            match = re.search(r'<rootfile[^>]+full-path="([^"]+)"', container)
            if match:
                opf_path = match.group(1)
        if not opf_path:
            for name in zf.namelist():
                if name.lower().endswith('.opf'):
                    opf_path = name
                    break
        if not opf_path:
            sys.exit('错误：未找到 content.opf，该 epub 可能已损坏')

        spine, ncx_path = _parse_opf(zf, opf_path)
        fulltext, doc_offsets, spine_paths, htmls = _build_fulltext(zf, spine)
        if not fulltext.strip():
            sys.exit('错误：未能提取到任何正文文本')

        base_dir = os.path.dirname(opf_path).replace('\\', '/')
        toc_entries = []
        if ncx_path:
            toc_entries = _map_offsets(doc_offsets, _parse_ncx(zf, ncx_path), base_dir)
        if not toc_entries:
            nav_path = None
            for name in zf.namelist():
                if name.lower().split('/')[-1] in ('nav.xhtml', 'nav.html', 'toc.xhtml'):
                    nav_path = name
                    break
            if nav_path:
                toc_entries = _map_offsets(doc_offsets, _parse_nav(zf, nav_path), base_dir)
        if not toc_entries:
            toc_entries = _heading_fallback(spine_paths, htmls, doc_offsets)

    toc_lines = ['%d\t%s%s\t%d' % (i + 1, '  ' * depth, title, offset)
                 for i, (depth, title, offset) in enumerate(toc_entries)]

    full_path = os.path.join(outdir, '%s_fulltext.txt' % stem)
    toc_path = os.path.join(outdir, '%s_toc.txt' % stem)
    with open(full_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(fulltext)
    with open(toc_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(toc_lines))

    print('正文已输出：%s（%d 字符）' % (full_path, len(fulltext)))
    print('目录已输出：%s（%d 个条目）' % (toc_path, len(toc_lines)))


if __name__ == '__main__':
    main()

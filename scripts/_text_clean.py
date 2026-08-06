#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""共用文本清洗模块（仅供同目录提取脚本调用，非独立命令行工具）。

职责：从 HTML/XHTML 中去除 style、script、head 等与正文无关的元素，
只保留正文文本；并提供标题索引提取，用于生成索引式 TOC。

仅依赖 Python 标准库，无第三方依赖。
"""

import re

# 需整体删除（含内容）的标签
_STRIP_CONTENT_TAGS = (
    'style', 'script', 'head', 'title', 'meta', 'link', 'noscript', 'svg', 'template',
)
# 块级标签：其后补一个换行，保证段落分隔
_BLOCK_TAGS = (
    'p', 'div', 'br', 'li', 'ul', 'ol', 'table', 'tr', 'blockquote',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'section', 'article',
    'header', 'footer', 'figure', 'hr',
)

_HEADING_RE = re.compile(
    r'<(h[1-6])\b[^>]*>(.*?)</\1>',
    re.IGNORECASE | re.DOTALL,
)

_COMMON_ENTITIES = {
    'amp': '&', 'lt': '<', 'gt': '>', 'quot': '"', 'apos': "'", 'nbsp': ' ',
}


def _decode_entities(text):
    def repl(match):
        name = match.group(1)
        if name in _COMMON_ENTITIES:
            return _COMMON_ENTITIES[name]
        if name.startswith('#'):
            code = name[1:]
            try:
                num = int(code[1:], 16) if code[:1] in ('x', 'X') else int(code)
                return chr(num)
            except (ValueError, OverflowError):
                return match.group(0)
        return match.group(0)

    return re.sub(r'&([a-zA-Z]+|#[0-9]+|#[xX][0-9a-fA-F]+);', repl, text)


def html_to_text(html):
    """去除与正文无关的元素，返回纯文本。

    删除对象：HTML 注释、style/script/head/title/meta/link/svg 等标签及其内容、
    全部行内与块级标签外壳。块级标签位置补换行，连续空行压缩为一个，
    行首尾空白去除。返回文本以换行分隔段落，不含任何标签与样式。
    """
    text = re.sub(r'<!--.*?-->', '\n', html, flags=re.DOTALL)
    for tag in _STRIP_CONTENT_TAGS:
        text = re.sub(
            r'<%s\b[^>]*>.*?</%s\s*>' % (tag, tag), '\n', text,
            flags=re.IGNORECASE | re.DOTALL,
        )
        text = re.sub(r'<%s\b[^>]*/?>' % tag, '', text, flags=re.IGNORECASE)
    text = re.sub(r'<\?xml.*?\?>', '', text, flags=re.DOTALL)
    text = re.sub(r'<!DOCTYPE[^>]*>', '', text, flags=re.IGNORECASE)
    for tag in _BLOCK_TAGS:
        text = re.sub(r'</?%s\b[^>]*>' % tag, '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<[^>]+>', '', text)
    text = _decode_entities(text)
    lines = [line.strip() for line in text.split('\n')]
    result = []
    for line in lines:
        if line:
            result.append(line)
        elif result and result[-1] != '':
            result.append('')
    return '\n'.join(result).strip('\n')


def extract_heading_index(html):
    """从 HTML 中提取 h1-h6 标题，返回 [(标题, 标题在原文HTML中的字符偏移), ...]。

    调用方（提取脚本）负责把 HTML 偏移换算为正文文本偏移。
    用作 NCX/nav 目录缺失时的 TOC 兜底来源。
    """
    items = []
    for match in _HEADING_RE.finditer(html):
        raw = match.group(2)
        raw = re.sub(r'<[^>]+>', '', raw)
        title = _decode_entities(raw).strip()
        title = re.sub(r'\s+', ' ', title)
        if title:
            items.append((title, match.start()))
    return items

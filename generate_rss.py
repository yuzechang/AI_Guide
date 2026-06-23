#!/usr/bin/env python3
"""
RSS Feed 生成器
从 blog/ 目录扫描博客文章，提取元数据，生成标准 RSS 2.0 格式的 feed.xml
"""

import os
import re
import json
from datetime import datetime, timezone
from email.utils import formatdate
import calendar
from html import unescape

# 项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BLOG_DIR = os.path.join(BASE_DIR, "blog")
OUTPUT_FILE = os.path.join(BASE_DIR, "feed.xml")

# RSS 频道配置
CHANNEL_TITLE = "AI Nav Blog – Open-Source AI Tools Guides"
CHANNEL_LINK = "https://yuzec.com/blog"
CHANNEL_DESC = "In-depth guides, comparisons, and tutorials for open-source AI tools and frameworks."
CHANNEL_LANG = "en-us"
FEED_URL = "https://yuzec.com/feed.xml"


def extract_tag(content: str, pattern: str) -> str:
    """从 HTML 内容中提取单个匹配值"""
    m = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
    return m.group(1).strip() if m else ""


def parse_blog_file(filepath: str):
    """解析单个博客 HTML 文件，提取 RSS 所需元数据"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 提取 <title> 并去掉常见后缀（先反转义 HTML 实体，避免双重转义）
    title = unescape(extract_tag(content, r"<title>(.*?)</title>"))
    for suffix in [" – AI Nav", " | AI Nav", " - AI Nav"]:
        if title.endswith(suffix):
            title = title[: -len(suffix)]
            break

    # 提取 <meta name="description">（先反转义 HTML 实体）
    desc = unescape(extract_tag(content, r'<meta\s+name="description"\s+content="([^"]*)"'))
    if not desc:
        desc = unescape(extract_tag(content, r'<meta\s+content="([^"]*)"\s+name="description"'))

    # 提取 canonical URL
    canonical = extract_tag(content, r'<link\s+rel="canonical"\s+href="([^"]*)"')

    # 从 JSON-LD 中提取 datePublished
    date_published = ""
    json_ld_blocks = re.findall(
        r'<script\s+type="application/ld\+json">(.*?)</script>',
        content,
        re.DOTALL | re.IGNORECASE,
    )
    for block in json_ld_blocks:
        try:
            data = json.loads(block.strip())
            if isinstance(data, dict) and "datePublished" in data:
                date_published = data["datePublished"]
                break
        except (json.JSONDecodeError, KeyError):
            continue

    # 如果 JSON-LD 中没有，尝试从 og:article:published_time 获取
    if not date_published:
        og_time = extract_tag(
            content,
            r'<meta\s+property="article:published_time"\s+content="([^"]*)"',
        )
        if og_time:
            date_published = og_time[:10]  # 取 YYYY-MM-DD 部分

    if not title or not canonical or not date_published:
        return None

    return {
        "title": title,
        "link": canonical,
        "description": desc,
        "date_published": date_published,  # YYYY-MM-DD
    }


def date_to_rfc2822(date_str: str) -> str:
    """将 YYYY-MM-DD 转换为 RFC 2822 格式（RSS pubDate 要求）"""
    dt = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    # email.utils.formatdate 生成 RFC 2822 格式
    return formatdate(calendar.timegm(dt.timetuple()), usegmt=True)


def escape_xml(text: str) -> str:
    """转义 XML 特殊字符"""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def generate_feed(articles) -> str:
    """生成 RSS 2.0 XML 内容"""
    now_rfc2822 = formatdate(usegmt=True)

    items_xml = ""
    for article in articles:
        items_xml += f"""    <item>
      <title>{escape_xml(article['title'])}</title>
      <link>{escape_xml(article['link'])}</link>
      <description><![CDATA[{article['description']}]]></description>
      <pubDate>{date_to_rfc2822(article['date_published'])}</pubDate>
      <guid isPermaLink="true">{escape_xml(article['link'])}</guid>
    </item>\n"""

    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{escape_xml(CHANNEL_TITLE)}</title>
    <link>{CHANNEL_LINK}</link>
    <description>{escape_xml(CHANNEL_DESC)}</description>
    <language>{CHANNEL_LANG}</language>
    <atom:link href="{FEED_URL}" rel="self" type="application/rss+xml"/>
    <lastBuildDate>{now_rfc2822}</lastBuildDate>
{items_xml}  </channel>
</rss>"""
    return feed


def main():
    articles = []

    # 扫描 blog/*.html，排除 blog/index.html
    for filename in os.listdir(BLOG_DIR):
        if not filename.endswith(".html"):
            continue
        if filename == "index.html":
            continue

        filepath = os.path.join(BLOG_DIR, filename)
        article = parse_blog_file(filepath)
        if article:
            articles.append(article)
            print(f"  [✓] {filename} → {article['date_published']} | {article['title'][:60]}")
        else:
            print(f"  [!] {filename} → 元数据不完整，已跳过")

    if not articles:
        print("未找到有效博客文章，feed.xml 未生成。")
        return

    # 按发布日期倒序排列（最新在前）
    articles.sort(key=lambda a: a["date_published"], reverse=True)

    # 生成 feed.xml
    feed_content = generate_feed(articles)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(feed_content)

    print(f"\n共解析 {len(articles)} 篇文章，feed.xml 已生成：{OUTPUT_FILE}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""generate_compare.py — 生成 /compare/ 对比页"""

import json
from pathlib import Path
from datetime import date
from jinja2 import Environment, FileSystemLoader, select_autoescape

BASE_DIR      = Path(__file__).parent
DATA_FILE     = BASE_DIR / "data.json"
COMPARE_FILE  = BASE_DIR / "compare_data.json"
TEMPLATES_DIR = BASE_DIR / "templates"
COMPARE_DIR   = BASE_DIR / "compare"
SITEMAP_FILE  = BASE_DIR / "sitemap.xml"

BASE_URL = "https://yuzec.com"
TODAY    = date.today().isoformat()

def main():
    with open(DATA_FILE, encoding="utf-8") as f:
        all_tools = {t["id"]: t for t in json.load(f)["tools"]}

    with open(COMPARE_FILE, encoding="utf-8") as f:
        compares = json.load(f)

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html"]),
    )
    template = env.get_template("compare.j2")
    COMPARE_DIR.mkdir(exist_ok=True)

    generated = 0
    for cmp in compares:
        tool_a_id = cmp["tool_a_id"]
        tool_b_id = cmp["tool_b_id"]

        # 从 data.json 取工具数据；若不存在则构造最小占位数据
        tool_a = all_tools.get(tool_a_id, {
            "id": tool_a_id, "name": cmp["title"].split(" vs ")[0],
            "starsLabel": "N/A", "githubUrl": "#", "license": "N/A",
            "descEn": "", "expert_take": ""
        })
        tool_b = all_tools.get(tool_b_id, {
            "id": tool_b_id, "name": cmp["title"].split(" vs ")[-1],
            "starsLabel": "N/A", "githubUrl": "#", "license": "N/A",
            "descEn": "", "expert_take": ""
        })

        name_a = tool_a.get("name", tool_a_id)
        name_b = tool_b.get("name", tool_b_id)

        seo_title = f"{name_a} vs {name_b} (2025): Which Should You Choose? | AI Nav"
        seo_desc  = (f"Compare {name_a} and {name_b} side-by-side. "
                     f"Features, pricing, pros, cons, and expert recommendation. "
                     f"Find out which is right for your use case.")[:160]

        ctx = {
            "cmp":             cmp,
            "tool_a":          tool_a,
            "tool_b":          tool_b,
            "seo_title":       seo_title,
            "seo_desc":        seo_desc,
            "base_url":        BASE_URL,
            "today":           TODAY,
            "related_compares": cmp.get("related_compares", []),
        }

        out_path = COMPARE_DIR / f"{cmp['slug']}.html"
        html = template.render(**ctx)
        out_path.write_text(html, encoding="utf-8")
        generated += 1
        print(f"  ✅ compare/{cmp['slug']}.html")

    print(f"\n[compare] 生成 {generated} 个对比页 → {COMPARE_DIR.name}/")

    # 更新 sitemap：追加 compare 页面
    update_sitemap(compares)


def update_sitemap(compares):
    """将 compare 页面追加到现有 sitemap.xml"""
    sitemap_path = SITEMAP_FILE
    if not sitemap_path.exists():
        print("[sitemap] sitemap.xml 不存在，跳过更新")
        return

    content = sitemap_path.read_text(encoding="utf-8")

    # 先移除已有的 compare URL（避免重复）
    import re
    content = re.sub(
        r'\s*<url>\s*<loc>[^<]*/compare/[^<]*</loc>.*?</url>',
        '', content, flags=re.DOTALL
    )

    new_urls = []
    for cmp in compares:
        loc = f"{BASE_URL}/compare/{cmp['slug']}"
        new_urls.append(
            f"  <url>\n"
            f"    <loc>{loc}</loc>\n"
            f"    <lastmod>{TODAY}</lastmod>\n"
            f"    <changefreq>monthly</changefreq>\n"
            f"    <priority>0.85</priority>\n"
            f"  </url>"
        )

    insert_before = "</urlset>"
    content = content.replace(insert_before, "\n".join(new_urls) + "\n" + insert_before)
    sitemap_path.write_text(content, encoding="utf-8")

    url_count = content.count("<url>")
    print(f"[sitemap] 已更新，共 {url_count} 个 URL（含 {len(compares)} 个对比页）")


if __name__ == "__main__":
    main()

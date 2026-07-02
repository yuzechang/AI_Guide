#!/usr/bin/env python3
"""
批量将没有 pros/cons 的工具页改为 noindex。
运行：python3 patch_noindex_thin_pages.py
      python3 patch_noindex_thin_pages.py --dry-run   (仅预览，不修改)
      python3 patch_noindex_thin_pages.py --revert    (恢复所有工具页为 index)
"""

import json
import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOOLS_DIR = os.path.join(BASE_DIR, "tools")
DATA_FILE = os.path.join(BASE_DIR, "data.json")

DRY_RUN = "--dry-run" in sys.argv
REVERT  = "--revert"  in sys.argv


def load_data():
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)["tools"]


def tool_ids_without_pros(tools):
    return {t["id"] for t in tools if not (t.get("pros") and len(t["pros"]) > 0)}


def patch_file(path: str, to_noindex: bool):
    with open(path, encoding="utf-8") as f:
        html = f.read()

    if to_noindex:
        # index,follow → noindex,follow
        new_html = re.sub(
            r'<meta\s+name="robots"\s+content="index,\s*follow">',
            '<meta name="robots" content="noindex, follow">',
            html,
        )
    else:
        # noindex,follow → index,follow
        new_html = re.sub(
            r'<meta\s+name="robots"\s+content="noindex,\s*follow">',
            '<meta name="robots" content="index, follow">',
            html,
        )

    if new_html == html:
        return False  # 没有变化
    if not DRY_RUN:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_html)
    return True


def main():
    tools = load_data()
    thin_ids = tool_ids_without_pros(tools)

    print(f"总工具数: {len(tools)}")
    print(f"无 pros/cons (薄内容): {len(thin_ids)}")
    print(f"有 pros/cons (保留 index): {len(tools) - len(thin_ids)}")
    if DRY_RUN:
        print("[dry-run 模式，不实际修改文件]")
    if REVERT:
        print("[revert 模式，将所有工具页恢复为 index]")
    print()

    changed = skipped = not_found = 0

    all_ids = {t["id"] for t in tools}
    target_ids = all_ids if REVERT else thin_ids
    to_noindex = not REVERT

    for tid in sorted(target_ids):
        fpath = os.path.join(TOOLS_DIR, f"{tid}.html")
        if not os.path.exists(fpath):
            not_found += 1
            continue

        ok = patch_file(fpath, to_noindex)
        if ok:
            changed += 1
            action = "→ noindex" if to_noindex else "→ index"
            print(f"  {'[dry]' if DRY_RUN else '[OK] '} {tid}.html {action}")
        else:
            skipped += 1

    print()
    action_word = "noindex" if to_noindex else "index"
    print(f"已{'模拟' if DRY_RUN else ''}修改: {changed} 个文件 → {action_word}")
    print(f"跳过 (已是目标状态): {skipped}")
    print(f"文件不存在: {not_found}")

    if not DRY_RUN and not REVERT:
        print()
        print("下一步: 运行 python3 generate.py --sitemap-only 重新生成 sitemap.xml")
        print("        然后推送到 GitHub 并重新提交 Search Console sitemap")


if __name__ == "__main__":
    main()

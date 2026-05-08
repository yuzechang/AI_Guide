#!/usr/bin/env python3
"""
自动更新 data.json 中各工具的 GitHub Star 数。
运行方式：python scripts/update_stars.py
依赖：pip install requests
可选环境变量：GITHUB_TOKEN（提升 API 限速上限，无需必填）
"""

import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    import requests
except ImportError:
    raise SystemExit("请先安装依赖: pip install requests")

# ── 路径配置 ──────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
DATA_FILE  = SCRIPT_DIR.parent / "data.json"

# ── GitHub API 请求头 ─────────────────────────────────────────────────────────
TOKEN = os.environ.get("GITHUB_TOKEN", "")
HEADERS = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"


def format_stars(n: int) -> str:
    """将整数 star 数格式化为易读标签，如 93041 → '93k+'"""
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M+"
    if n >= 1_000:
        k = n / 1_000
        if k >= 100:
            return f"{int(k)}k+"
        if k >= 10:
            return f"{k:.0f}k+"
        return f"{k:.1f}k+"
    return str(n)


def extract_repo(github_url: str) -> str | None:
    """从 GitHub URL 提取 'owner/repo'，失败返回 None"""
    m = re.search(r"github\.com/([^/]+/[^/?#]+)", github_url)
    return m.group(1).rstrip("/") if m else None


def fetch_stars(repo: str) -> int | None:
    """查询单个仓库的当前 star 数，失败返回 None"""
    url = f"https://api.github.com/repos/{repo}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            return resp.json().get("stargazers_count")
        if resp.status_code == 403:
            # 触发速率限制
            reset = resp.headers.get("X-RateLimit-Reset", "")
            print(f"  ⚠️  Rate limited. Reset at {reset}. 等待 60s 后重试…")
            time.sleep(60)
            resp2 = requests.get(url, headers=HEADERS, timeout=10)
            if resp2.status_code == 200:
                return resp2.json().get("stargazers_count")
        print(f"  ✗ HTTP {resp.status_code} for {repo}")
    except requests.RequestException as e:
        print(f"  ✗ 请求失败 {repo}: {e}")
    return None


def main() -> None:
    if not DATA_FILE.exists():
        raise SystemExit(f"找不到数据文件: {DATA_FILE}")

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    tools = data.get("tools", [])
    updated_count = 0
    skipped_count = 0

    print(f"🔄 开始更新 {len(tools)} 个工具的 GitHub Stars…\n")

    for tool in tools:
        repo = extract_repo(tool.get("githubUrl", ""))
        if not repo:
            print(f"  ⚠️  跳过（无效 URL）: {tool.get('name')}")
            skipped_count += 1
            continue

        stars = fetch_stars(repo)
        if stars is None:
            print(f"  ⚠️  跳过（API 失败）: {repo}")
            skipped_count += 1
            continue

        old_label = tool.get("starsLabel", "?")
        new_label = format_stars(stars)
        tool["stars"]      = stars
        tool["starsLabel"] = new_label
        updated_count += 1

        change = ""
        if old_label != new_label:
            change = f"  ({old_label} → {new_label})"
        print(f"  ✓ {tool['name']:30s}  ★ {new_label}{change}")

        # 避免触发 GitHub API 速率限制（60 req/h 无 token，5000/h 有 token）
        time.sleep(0.5 if TOKEN else 1.2)

    # 更新时间戳
    data["updatedAt"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # 同步生成 data.js，供直接打开 HTML 时使用（无需 HTTP 服务器）
    js_file = DATA_FILE.parent / "data.js"
    with open(js_file, "w", encoding="utf-8") as f:
        f.write(f"window.TOOLS_DATA = {json.dumps(data, ensure_ascii=False)};")

    print(f"\n✅ 完成！更新 {updated_count} 个，跳过 {skipped_count} 个")
    print(f"📅 updatedAt → {data['updatedAt']}")
    print(f"📁 data.json → {DATA_FILE}")
    print(f"📁 data.js   → {js_file}")


if __name__ == "__main__":
    main()

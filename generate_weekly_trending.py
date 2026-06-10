#!/usr/bin/env python3
"""
每周 GitHub Stars 涨幅榜生成器
用法：python3 generate_weekly_trending.py
输出：weekly-trending.html
说明：每次 GitHub Actions 更新 data.json 后运行此脚本
"""

import json
import sys
from pathlib import Path
from datetime import date, timedelta

# ─── 路径 ────────────────────────────────────────────────────────────────────
BASE_DIR      = Path(__file__).parent
DATA_FILE     = BASE_DIR / "data.json"
SNAPSHOT_FILE = BASE_DIR / "data_snapshot_prev.json"
OUTPUT_FILE   = BASE_DIR / "weekly-trending.html"

BASE_URL = "https://yuzec.com"
TODAY    = date.today().isoformat()

# 本周起始日（上一个周一）
def get_week_start():
    today = date.today()
    days_since_monday = today.weekday()
    return (today - timedelta(days=days_since_monday)).isoformat()

WEEK_START = get_week_start()


# ─── 数字格式化 ───────────────────────────────────────────────────────────────
def fmt_stars(n: int) -> str:
    """将数字格式化为带逗号的字符串，如 12345 → 12,345"""
    return f"{n:,}"


def fmt_pct(delta: int, prev: int) -> str:
    """计算增幅百分比字符串"""
    if prev <= 0:
        return "N/A"
    return f"+{delta / prev * 100:.1f}%"


# ─── HTML 生成辅助 ────────────────────────────────────────────────────────────
def rank_medal(rank: int) -> str:
    """1-3 名返回金银铜颜色 class"""
    return {1: "rank-gold", 2: "rank-silver", 3: "rank-bronze"}.get(rank, "rank-normal")


def category_label(cat: str) -> str:
    return {
        "ai-tools": "AI Tools",
        "skill":    "Framework",
        "agent":    "Agent",
    }.get(cat, cat)


def category_color(cat: str) -> str:
    return {
        "ai-tools": "#818cf8",
        "skill":    "#34d399",
        "agent":    "#fbbf24",
    }.get(cat, "#94a3b8")


# ─── 主逻辑 ───────────────────────────────────────────────────────────────────
def load_data():
    """读取 data.json，返回 tools 列表"""
    with open(DATA_FILE, encoding="utf-8") as f:
        data = json.load(f)
    return data.get("tools", [])


def load_or_create_snapshot(tools: list) -> tuple[dict, bool]:
    """
    读取上周快照。
    - 如果快照不存在：保存当前数据作为基准，返回 (snapshot, is_first_run=True)
    - 如果快照存在：返回 (snapshot, is_first_run=False)
    快照格式：{ tool_id: stars }
    """
    if not SNAPSHOT_FILE.exists():
        snapshot = {t["id"]: t.get("stars", 0) for t in tools}
        with open(SNAPSHOT_FILE, "w", encoding="utf-8") as f:
            json.dump(snapshot, f, indent=2, ensure_ascii=False)
        print("首次运行：已保存快照，下次运行将生成真实涨幅数据")
        return snapshot, True

    with open(SNAPSHOT_FILE, encoding="utf-8") as f:
        snapshot = json.load(f)
    return snapshot, False


def save_snapshot(tools: list):
    """将当前 stars 数据保存为新快照（覆盖旧快照）"""
    snapshot = {t["id"]: t.get("stars", 0) for t in tools}
    with open(SNAPSHOT_FILE, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)
    print(f"快照已更新 → {SNAPSHOT_FILE.name}")


def calc_trending(tools: list, snapshot: dict) -> list:
    """
    计算涨幅，过滤无效数据，返回按增量降序排序的 Top 10 列表。
    每条记录：{ id, name, category, stars, delta, delta_pct, descEn, githubUrl }
    """
    results = []
    for t in tools:
        tid = t["id"]
        if tid not in snapshot:
            continue
        prev_stars = snapshot[tid]
        curr_stars = t.get("stars", 0)
        delta = curr_stars - prev_stars
        if delta <= 0:
            continue
        results.append({
            "id":        tid,
            "name":      t.get("name", tid),
            "category":  t.get("category", "ai-tools"),
            "stars":     curr_stars,
            "prev":      prev_stars,
            "delta":     delta,
            "delta_pct": fmt_pct(delta, prev_stars),
            "descEn":    t.get("descEn", ""),
            "githubUrl": t.get("githubUrl", ""),
        })

    results.sort(key=lambda x: x["delta"], reverse=True)
    return results[:10]


# ─── HTML 生成 ────────────────────────────────────────────────────────────────
def build_card(rank: int, tool: dict) -> str:
    medal_class = rank_medal(rank)
    cat_label   = category_label(tool["category"])
    cat_color   = category_color(tool["category"])
    tool_url    = f"/tools/{tool['id']}.html"

    # 1-3 名的边框样式
    border_style = {
        1: "border: 1px solid rgba(255,215,0,0.35); background: linear-gradient(135deg, rgba(255,215,0,0.06) 0%, rgba(17,24,39,1) 60%);",
        2: "border: 1px solid rgba(192,192,192,0.3); background: linear-gradient(135deg, rgba(192,192,192,0.05) 0%, rgba(17,24,39,1) 60%);",
        3: "border: 1px solid rgba(205,127,50,0.3); background: linear-gradient(135deg, rgba(205,127,50,0.05) 0%, rgba(17,24,39,1) 60%);",
    }.get(rank, "border: 1px solid var(--border);")

    return f"""
    <div class="trend-card" style="{border_style}">
      <div class="trend-rank {medal_class}">#{rank}</div>
      <div class="trend-body">
        <div class="trend-header">
          <a href="{tool_url}" class="trend-name">{tool['name']}</a>
          <span class="trend-cat-badge" style="background:rgba({_hex_to_rgba(cat_color)},0.12);color:{cat_color};border:1px solid rgba({_hex_to_rgba(cat_color)},0.25)">{cat_label}</span>
        </div>
        <p class="trend-desc">{tool['descEn']}</p>
        <div class="trend-stats">
          <span class="trend-delta">+{fmt_stars(tool['delta'])} stars this week</span>
          <span class="trend-pct">{tool['delta_pct']} growth</span>
          <span class="trend-total">⭐ {fmt_stars(tool['stars'])} total</span>
        </div>
        <div class="trend-links">
          <a href="{tool_url}" class="trend-link-btn">View Details →</a>
          <a href="{tool['githubUrl']}" target="_blank" rel="noopener" class="trend-link-gh">GitHub ↗</a>
        </div>
      </div>
    </div>"""


def _hex_to_rgba(hex_color: str) -> str:
    """将 #RRGGBB 转为 R,G,B 字符串，用于 rgba() 插值"""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"{r},{g},{b}"


def build_placeholder_page() -> str:
    """首次运行时，生成占位提示页（避免空页面）"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Weekly Trending AI Tools – GitHub Stars This Week | AI Nav</title>
  <meta name="description" content="The fastest-growing open source AI tools this week, ranked by new GitHub stars gained. Updated every Monday.">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{BASE_URL}/weekly-trending">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/shared.css">
  <script src="assets/lang.js"></script>
  <style>
    .placeholder-box {{
      max-width: 640px; margin: 48px auto; text-align: center;
      padding: 48px 32px;
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
    }}
    .placeholder-icon {{ font-size: 56px; margin-bottom: 20px; }}
    .placeholder-title {{ font-size: 22px; font-weight: 700; color: var(--text); margin-bottom: 12px; }}
    .placeholder-desc {{ font-size: 15px; color: var(--text-2); line-height: 1.7; }}
    .placeholder-date {{ display: inline-block; margin-top: 20px; padding: 6px 16px;
      background: var(--accent-dim); border: 1px solid var(--accent); border-radius: 20px;
      font-size: 13px; color: var(--accent); }}
  </style>
</head>
<body>

<!-- Header -->
<header>
  <div class="header-inner">
    <a href="index.html" class="logo">
      <span class="logo-icon">⚡</span>
      <span>AI<span class="logo-accent">.</span>Nav</span>
    </a>
    <div class="header-spacer"></div>
    <nav style="display:flex;gap:16px;align-items:center">
      <a href="index.html" class="nav-home" style="font-weight:500;font-size:14px">Directory</a>
      <a href="blog/index.html" style="font-weight:500;font-size:14px;color:var(--text-2)">Blog</a>
      <a href="about.html" style="font-weight:500;font-size:14px;color:var(--text-2)">About</a>
      <a href="https://game.yuzec.com" target="_blank" rel="noopener" class="nav-game-link">🎮 小游戏</a>
    </nav>
    <button data-langbtn="en" style="display:none"></button>
    <button data-langbtn="zh" style="display:none"></button>
    <a href="https://github.com/yuzechang/AI_Guide" target="_blank" rel="noopener" class="gh-link" aria-label="GitHub">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.477 2 2 6.477 2 12c0 4.418 2.865 8.166 6.839 9.489.5.092.682-.217.682-.482 0-.237-.009-.868-.013-1.703-2.782.604-3.369-1.341-3.369-1.341-.454-1.155-1.11-1.462-1.11-1.462-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.087 2.91.831.092-.646.35-1.086.636-1.336-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.27.098-2.647 0 0 .84-.269 2.75 1.025A9.578 9.578 0 0112 6.836a9.59 9.59 0 012.504.337c1.909-1.294 2.747-1.025 2.747-1.025.546 1.377.202 2.394.1 2.647.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743 0 .267.18.578.688.48C19.138 20.161 22 16.416 22 12c0-5.523-4.477-10-10-10z"/></svg>
    </a>
  </div>
</header>

<!-- Breadcrumb -->
<div class="breadcrumb">
  <a href="index.html">Home</a>
  <span class="breadcrumb-sep">›</span>
  <span class="breadcrumb-cur">Weekly Trending</span>
</div>

<div class="page-wrap">
  <div class="placeholder-box">
    <div class="placeholder-icon">📊</div>
    <div class="placeholder-title">This Week's Data Is Being Collected</div>
    <p class="placeholder-desc">
      We just set up our weekly tracking baseline on <strong>{TODAY}</strong>.<br>
      Come back next Monday to see which AI tools gained the most GitHub stars this week.
    </p>
    <span class="placeholder-date">📅 Next update: {(date.today() + timedelta(days=7 - date.today().weekday())).isoformat()}</span>
    <div style="margin-top:28px">
      <a href="open-source-ai-leaderboard.html" class="cta-btn" style="margin-right:10px">View All-Time Leaderboard →</a>
      <a href="index.html" class="cta-btn-outline">Browse All Tools</a>
    </div>
  </div>
</div>

<!-- Footer -->
<footer>
  <div class="footer-inner">
    <div class="footer-grid">
      <div class="footer-brand">
        <div class="logo"><span class="logo-icon">⚡</span><span>AI<span class="logo-accent">.</span>Nav</span></div>
        <p>A curated directory of the best open-source AI tools, agent frameworks, and skill libraries from GitHub.</p>
      </div>
      <div class="footer-col">
        <h4>Categories</h4>
        <ul>
          <li><a href="index.html#ai-tools">AI Tools</a></li>
          <li><a href="index.html#skill">Skill Frameworks</a></li>
          <li><a href="index.html#agent">AI Agents</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Site</h4>
        <ul>
          <li><a href="blog/index.html">Blog</a></li>
          <li><a href="about.html">About</a></li>
          <li><a href="contact.html">Contact</a></li>
          <li><a href="privacy-policy.html">Privacy Policy</a></li>
          <li><a href="sitemap.xml">Sitemap</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Resources</h4>
        <ul>
          <li><a href="https://github.com/trending" target="_blank" rel="noopener">GitHub Trending</a></li>
          <li><a href="https://github.com/Hannibal046/Awesome-LLM" target="_blank" rel="noopener">Awesome LLM</a></li>
          <li><a href="https://github.com/e2b-dev/awesome-ai-agents" target="_blank" rel="noopener">Awesome Agents</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© 2025 AI Nav · All tools are open-source, hosted on GitHub.</p>
      <p>Built for the AI community ❤️</p>
    </div>
  </div>
</footer>

</body>
</html>"""


def build_full_page(trending: list) -> str:
    """生成完整的涨幅榜页面"""
    top1 = trending[0]
    total_delta = sum(t["delta"] for t in trending)

    # 生成卡片 HTML
    cards_html = "\n".join(build_card(i + 1, t) for i, t in enumerate(trending))

    # FAQ 动态数据
    faq3_answer = (
        f"{top1['name']} is currently the fastest-growing AI tool on GitHub, "
        f"gaining +{fmt_stars(top1['delta'])} new stars as of {TODAY}."
    )

    # JSON-LD Schema
    schema = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "headline": "This Week's Fastest-Growing AI Tools by GitHub Stars",
                "description": (
                    f"Weekly ranking of the top 10 AI tools with the highest GitHub star growth. "
                    f"This week's leader: {top1['name']} with +{fmt_stars(top1['delta'])} new stars."
                ),
                "url": f"{BASE_URL}/weekly-trending",
                "datePublished": WEEK_START,
                "dateModified": TODAY,
                "author": {"@type": "Organization", "name": "AI Nav"},
                "publisher": {
                    "@type": "Organization",
                    "name": "AI Nav",
                    "url": BASE_URL
                }
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": "How often is this trending list updated?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "Every Monday, after our automated GitHub Actions pipeline syncs the latest star counts for all 300+ tracked tools."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": "What does \"GitHub stars gained this week\" measure?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "The difference in GitHub stars between this Monday and last Monday for each tool. It reflects real community interest and developer adoption trends."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": "Which AI tool is growing the fastest right now?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": faq3_answer
                        }
                    }
                ]
            }
        ]
    }, indent=2, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Weekly Trending AI Tools – GitHub Stars This Week | AI Nav</title>
  <meta name="description" content="The fastest-growing open source AI tools this week, ranked by new GitHub stars gained. Updated every Monday.">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{BASE_URL}/weekly-trending">

  <!-- Open Graph -->
  <meta property="og:type" content="article">
  <meta property="og:title" content="Weekly Trending AI Tools – GitHub Stars This Week | AI Nav">
  <meta property="og:description" content="{top1['name']} leads this week with +{fmt_stars(top1['delta'])} new GitHub stars. See the full Top 10 fastest-growing AI tools.">
  <meta property="og:url" content="{BASE_URL}/weekly-trending">
  <meta property="og:site_name" content="AI Nav">

  <!-- Schema.org -->
  <script type="application/ld+json">
{schema}
  </script>

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/shared.css">
  <script src="assets/lang.js"></script>
  <style>
    /* ── 涨幅榜专属样式 ── */
    .trending-hero-meta {{
      display: flex; gap: 10px; align-items: center; flex-wrap: wrap;
      margin-bottom: 12px;
    }}
    .trending-date-tag {{
      display: inline-flex; align-items: center; gap: 6px;
      padding: 5px 14px; border-radius: 20px;
      background: rgba(52,211,153,0.1); border: 1px solid rgba(52,211,153,0.3);
      font-size: 13px; color: #34d399; font-weight: 500;
    }}
    .trend-card {{
      border-radius: var(--radius);
      padding: 20px 22px;
      margin-bottom: 14px;
      display: flex; gap: 18px; align-items: flex-start;
      transition: transform 0.15s, box-shadow 0.15s;
    }}
    .trend-card:hover {{
      transform: translateY(-2px);
      box-shadow: 0 6px 24px rgba(0,0,0,0.35);
    }}
    .trend-rank {{
      font-size: 22px; font-weight: 800;
      min-width: 42px; flex-shrink: 0; text-align: center;
      padding-top: 2px;
    }}
    .rank-gold   {{ color: #FFD700; text-shadow: 0 0 12px rgba(255,215,0,0.4); }}
    .rank-silver {{ color: #C0C0C0; text-shadow: 0 0 10px rgba(192,192,192,0.3); }}
    .rank-bronze {{ color: #CD7F32; text-shadow: 0 0 10px rgba(205,127,50,0.3); }}
    .rank-normal {{ color: var(--text-3); }}
    .trend-body  {{ flex: 1; min-width: 0; }}
    .trend-header {{
      display: flex; align-items: center; gap: 10px; flex-wrap: wrap;
      margin-bottom: 6px;
    }}
    .trend-name {{
      font-size: 17px; font-weight: 700; color: var(--text);
      transition: color 0.15s;
    }}
    .trend-name:hover {{ color: var(--accent); }}
    .trend-cat-badge {{
      display: inline-block; padding: 2px 10px; border-radius: 12px;
      font-size: 11px; font-weight: 600; letter-spacing: 0.04em;
    }}
    .trend-desc {{
      font-size: 13px; color: var(--text-2); margin-bottom: 12px;
      line-height: 1.55; display: -webkit-box;
      -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
    }}
    .trend-stats {{
      display: flex; gap: 14px; flex-wrap: wrap; align-items: center;
      margin-bottom: 12px;
    }}
    .trend-delta {{
      font-size: 18px; font-weight: 800; color: #34d399;
      letter-spacing: -0.02em;
    }}
    .trend-pct {{
      font-size: 13px; font-weight: 600; color: #86efac;
      background: rgba(52,211,153,0.1); padding: 2px 8px;
      border-radius: 6px; border: 1px solid rgba(52,211,153,0.2);
    }}
    .trend-total {{
      font-size: 13px; color: var(--text-3);
    }}
    .trend-links {{ display: flex; gap: 10px; flex-wrap: wrap; }}
    .trend-link-btn {{
      display: inline-flex; align-items: center;
      padding: 6px 14px; border-radius: var(--radius-sm);
      background: var(--accent-dim); border: 1px solid var(--accent);
      font-size: 12px; font-weight: 600; color: var(--accent);
      transition: background 0.15s, color 0.15s;
    }}
    .trend-link-btn:hover {{ background: var(--accent); color: #fff; }}
    .trend-link-gh {{
      display: inline-flex; align-items: center;
      padding: 6px 14px; border-radius: var(--radius-sm);
      background: transparent; border: 1px solid var(--border);
      font-size: 12px; font-weight: 500; color: var(--text-3);
      transition: border-color 0.15s, color 0.15s;
    }}
    .trend-link-gh:hover {{ border-color: var(--border-bright); color: var(--text); }}

    /* 统计摘要卡 */
    .key-stats-box {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 22px 24px;
      margin: 28px 0;
      font-size: 14px; color: var(--text-2); line-height: 1.8;
    }}
    .key-stats-box strong {{ color: var(--text); }}
    .key-stats-title {{
      font-size: 13px; font-weight: 700; color: var(--text-3);
      text-transform: uppercase; letter-spacing: 0.08em;
      margin-bottom: 10px;
    }}

    /* AdSense 占位 */
    .ad-slot {{
      width: 100%; min-height: 90px;
      background: rgba(255,255,255,0.02);
      border: 1px dashed var(--border);
      border-radius: var(--radius-sm);
      display: flex; align-items: center; justify-content: center;
      font-size: 11px; color: var(--text-3);
      margin: 28px 0;
    }}

    /* FAQ */
    .faq-section {{ margin-top: 36px; }}
    .faq-section h2 {{ font-size: 18px; font-weight: 700; margin-bottom: 16px; }}

    /* 响应式 */
    @media (max-width: 600px) {{
      .trend-card {{ flex-direction: column; gap: 10px; }}
      .trend-rank {{ font-size: 18px; min-width: auto; }}
      .trend-delta {{ font-size: 15px; }}
    }}
  </style>
</head>
<body>

<!-- Header -->
<header>
  <div class="header-inner">
    <a href="index.html" class="logo">
      <span class="logo-icon">⚡</span>
      <span>AI<span class="logo-accent">.</span>Nav</span>
    </a>
    <div class="header-spacer"></div>
    <nav style="display:flex;gap:16px;align-items:center">
      <a href="index.html" class="nav-home" style="font-weight:500;font-size:14px">Directory</a>
      <a href="blog/index.html" style="font-weight:500;font-size:14px;color:var(--text-2)">Blog</a>
      <a href="about.html" style="font-weight:500;font-size:14px;color:var(--text-2)">About</a>
      <a href="https://game.yuzec.com" target="_blank" rel="noopener" class="nav-game-link">🎮 小游戏</a>
    </nav>
    <button data-langbtn="en" style="display:none"></button>
    <button data-langbtn="zh" style="display:none"></button>
    <a href="https://github.com/yuzechang/AI_Guide" target="_blank" rel="noopener" class="gh-link" aria-label="GitHub">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.477 2 2 6.477 2 12c0 4.418 2.865 8.166 6.839 9.489.5.092.682-.217.682-.482 0-.237-.009-.868-.013-1.703-2.782.604-3.369-1.341-3.369-1.341-.454-1.155-1.11-1.462-1.11-1.462-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.087 2.91.831.092-.646.35-1.086.636-1.336-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.27.098-2.647 0 0 .84-.269 2.75 1.025A9.578 9.578 0 0112 6.836a9.59 9.59 0 012.504.337c1.909-1.294 2.747-1.025 2.747-1.025.546 1.377.202 2.394.1 2.647.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743 0 .267.18.578.688.48C19.138 20.161 22 16.416 22 12c0-5.523-4.477-10-10-10z"/></svg>
    </a>
  </div>
</header>

<!-- Breadcrumb -->
<div class="breadcrumb">
  <a href="index.html">Home</a>
  <span class="breadcrumb-sep">›</span>
  <span class="breadcrumb-cur">Weekly Trending</span>
</div>

<!-- Page Hero -->
<div class="page-hero" style="margin-top: 16px;">
  <div class="page-hero-inner">
    <div class="trending-hero-meta">
      <span class="article-badge">📈 Weekly Trending</span>
      <span class="trending-date-tag">📅 Week of {WEEK_START} — Updated every Monday</span>
    </div>
    <h1 class="article-title" style="margin-top:12px">
      This Week's Fastest-Growing<br><span class="gradient">AI Tools</span>
    </h1>
    <p class="article-desc">
      The top 10 open-source AI tools ranked by new GitHub stars gained this week.
      Star counts updated every Monday via our automated pipeline tracking 300+ tools.
    </p>
  </div>
</div>

<!-- Main Content -->
<div class="page-wrap">
  <div class="content">

    <!-- Key Stats 摘要 -->
    <div class="key-stats-box">
      <div class="key-stats-title">📊 This Week in Numbers</div>
      <p>
        This week, <strong>{top1['name']}</strong> gained the most GitHub stars with
        <strong>+{fmt_stars(top1['delta'])} new stars</strong>,
        bringing its total to <strong>{fmt_stars(top1['stars'])} stars</strong> as of {TODAY}.
      </p>
      <p style="margin-top:8px">
        The top 10 fastest-growing AI tools collectively gained
        <strong>{fmt_stars(total_delta)} new GitHub stars</strong> this week.
      </p>
    </div>

    <!-- Top 10 涨幅卡片 -->
    <h2 style="font-size:18px;font-weight:700;margin-bottom:18px">Top 10 by Stars Gained This Week</h2>
    {cards_html}

    <!-- AdSense 广告位 -->
    <div class="ad-slot">
      <!-- Google AdSense: replace with actual ad unit -->
      <!-- <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-XXXXXXXX" data-ad-slot="XXXXXXXX" data-ad-format="auto"></ins> -->
      Advertisement
    </div>

    <!-- 上期回顾 -->
    <div style="margin:24px 0;padding:16px 20px;background:var(--card);border:1px solid var(--border);border-radius:var(--radius)">
      <p style="font-size:13px;color:var(--text-2)">
        📅 <strong style="color:var(--text)">Previous Weeks:</strong>
        Historical weekly trending data is available in our
        <a href="open-source-ai-leaderboard.html" style="color:var(--accent)">open-source AI leaderboard</a>.
        Full weekly archives coming soon.
      </p>
    </div>

    <!-- FAQ -->
    <div class="faq-section">
      <h2>Frequently Asked Questions</h2>

      <div class="faq-item">
        <div class="faq-q" onclick="this.parentElement.classList.toggle('open')">
          <span>How often is this trending list updated?</span>
          <span class="faq-arr">▾</span>
        </div>
        <div class="faq-a">
          <div class="faq-a-inner">
            Every Monday, after our automated GitHub Actions pipeline syncs the latest star counts
            for all 300+ tracked tools. The delta is calculated by comparing this week's snapshot
            with last week's baseline.
          </div>
        </div>
      </div>

      <div class="faq-item">
        <div class="faq-q" onclick="this.parentElement.classList.toggle('open')">
          <span>What does "GitHub stars gained this week" measure?</span>
          <span class="faq-arr">▾</span>
        </div>
        <div class="faq-a">
          <div class="faq-a-inner">
            The difference in GitHub stars between this Monday and last Monday for each tool.
            It reflects real community interest and developer adoption momentum —
            a tool gaining 2,000 stars in one week is getting significant attention regardless of its total star count.
          </div>
        </div>
      </div>

      <div class="faq-item">
        <div class="faq-q" onclick="this.parentElement.classList.toggle('open')">
          <span>Which AI tool is growing the fastest right now?</span>
          <span class="faq-arr">▾</span>
        </div>
        <div class="faq-a">
          <div class="faq-a-inner">
            {faq3_answer}
            Check the rankings above for the full Top 10 and browse
            <a href="tools/{top1['id']}.html" style="color:var(--accent)">{top1['name']}'s detail page</a>
            to learn more.
          </div>
        </div>
      </div>
    </div>

    <!-- 内链导航 -->
    <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:36px;">
      <a href="open-source-ai-leaderboard.html" class="cta-btn">All-Time Leaderboard →</a>
      <a href="index.html" class="cta-btn-outline">Browse All 300+ Tools</a>
      <a href="blog/index.html" class="cta-btn-outline">Read Our Blog</a>
    </div>

  </div>
</div>

<!-- Footer -->
<footer>
  <div class="footer-inner">
    <div class="footer-grid">
      <div class="footer-brand">
        <div class="logo"><span class="logo-icon">⚡</span><span>AI<span class="logo-accent">.</span>Nav</span></div>
        <p>A curated directory of the best open-source AI tools, agent frameworks, and skill libraries from GitHub.</p>
      </div>
      <div class="footer-col">
        <h4>Categories</h4>
        <ul>
          <li><a href="index.html#ai-tools">AI Tools</a></li>
          <li><a href="index.html#skill">Skill Frameworks</a></li>
          <li><a href="index.html#agent">AI Agents</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Site</h4>
        <ul>
          <li><a href="blog/index.html">Blog</a></li>
          <li><a href="about.html">About</a></li>
          <li><a href="contact.html">Contact</a></li>
          <li><a href="privacy-policy.html">Privacy Policy</a></li>
          <li><a href="sitemap.xml">Sitemap</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Resources</h4>
        <ul>
          <li><a href="https://github.com/trending" target="_blank" rel="noopener">GitHub Trending</a></li>
          <li><a href="https://github.com/Hannibal046/Awesome-LLM" target="_blank" rel="noopener">Awesome LLM</a></li>
          <li><a href="https://github.com/e2b-dev/awesome-ai-agents" target="_blank" rel="noopener">Awesome Agents</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© 2025 AI Nav · All tools are open-source, hosted on GitHub.</p>
      <p>Built for the AI community ❤️</p>
    </div>
  </div>
</footer>

<!-- FAQ 交互脚本 -->
<script>
document.querySelectorAll('.faq-q').forEach(btn => {{
  btn.addEventListener('click', () => {{
    const item = btn.parentElement;
    const wasOpen = item.classList.contains('open');
    document.querySelectorAll('.faq-item.open').forEach(el => el.classList.remove('open'));
    if (!wasOpen) item.classList.add('open');
  }});
}});
</script>

</body>
</html>"""


# ─── 入口 ─────────────────────────────────────────────────────────────────────
def main():
    print("=" * 50)
    print("每周 GitHub Stars 涨幅榜生成器")
    print("=" * 50)

    # 1. 读取数据
    tools = load_data()
    print(f"已加载 {len(tools)} 个工具")

    # 2. 读取/创建快照
    snapshot, is_first_run = load_or_create_snapshot(tools)

    if is_first_run:
        # 首次运行：生成占位提示页
        html = build_placeholder_page()
        OUTPUT_FILE.write_text(html, encoding="utf-8")
        print(f"已生成占位提示页 → {OUTPUT_FILE.name}")
        print("\n提示：weekly-trending 页面已添加到网站，请确认 sitemap.xml 中包含以下条目：")
        print(f"  <loc>https://yuzec.com/weekly-trending</loc>")
        return

    # 3. 计算涨幅
    trending = calc_trending(tools, snapshot)
    print(f"有涨幅的工具：{sum(1 for t in tools if t['id'] in snapshot and t.get('stars', 0) > snapshot[t['id']])} 个")

    if not trending:
        print("本周没有检测到 stars 增量（可能快照与当前数据相同）")
        print("提示：如需测试，可手动删除 data_snapshot_prev.json 后重新运行")
        # 仍然生成一个占位页
        html = build_placeholder_page()
        OUTPUT_FILE.write_text(html, encoding="utf-8")
        print(f"已生成占位页 → {OUTPUT_FILE.name}")
        return

    # 4. 打印统计
    print(f"\n本周 Top {len(trending)} 涨幅工具：")
    for i, t in enumerate(trending, 1):
        print(f"  {i:2d}. {t['name']:<30s} +{fmt_stars(t['delta']):>8s} stars  ({t['delta_pct']})")
    total_delta = sum(t["delta"] for t in trending)
    print(f"\nTop 10 本周总增量：+{fmt_stars(total_delta)} stars")
    print(f"最大涨幅工具：{trending[0]['name']} (+{fmt_stars(trending[0]['delta'])} stars)")

    # 5. 生成 HTML
    html = build_full_page(trending)
    OUTPUT_FILE.write_text(html, encoding="utf-8")
    file_size_kb = OUTPUT_FILE.stat().st_size / 1024
    print(f"\n已生成 → {OUTPUT_FILE.name}（{file_size_kb:.1f} KB）")

    # 6. 更新快照
    save_snapshot(tools)

    # 7. sitemap 提示
    print("\n提示：请确认 sitemap.xml 中包含以下条目（generate.py 的 generate_sitemap 函数可添加）：")
    print(f"  <loc>https://yuzec.com/weekly-trending</loc>")
    print(f"  <lastmod>{TODAY}</lastmod>")
    print(f"  <changefreq>weekly</changefreq>")
    print(f"  <priority>0.85</priority>")
    print("=" * 50)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
generate_thin_content.py — 为缺少 pros/cons/faqs/use_cases 的工具批量生成内容
使用 Claude API (claude-haiku-4-5) 并发生成，进度实时保存到 data.json

用法:
  python3 generate_thin_content.py               # 处理全部薄内容工具
  python3 generate_thin_content.py --limit 20    # 只处理前 N 个（测试用）
  python3 generate_thin_content.py --workers 5   # 并发数（默认 5）
"""

import json
import os
import sys
import time
import argparse
import threading
from pathlib import Path
from typing import Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

import anthropic

BASE_DIR  = Path(__file__).parent
DATA_FILE = BASE_DIR / "data.json"
client    = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
lock      = threading.Lock()

# ─── 提示词 ────────────────────────────────────────────────────────────────────

SYSTEM = """You are a technical writer creating concise, accurate content for an AI tools directory.
Return ONLY valid JSON. No markdown fences, no explanation."""

def build_prompt(tool: dict) -> str:
    return f"""Generate pros, cons, FAQs, use_cases, and install_guide for this open-source AI tool.

Tool name: {tool['name']}
Description: {tool.get('descEn', '')}
GitHub: {tool.get('githubUrl', '')}
Stars: {tool.get('starsLabel', tool.get('stars', 0))}
Category: {tool.get('category', '')}
Tags: {', '.join(tool.get('tags', []))}
Expert take: {tool.get('expert_take', '')}

Return JSON in this exact structure:
{{
  "pros": ["<4 specific pros, each 10-20 words, fact-based>"],
  "cons": ["<2 realistic cons>"],
  "faqs": [
    {{"q": "<question>", "a": "<answer, 2-3 sentences>"}},
    {{"q": "<question>", "a": "<answer>"}},
    {{"q": "<question>", "a": "<answer>"}},
    {{"q": "<question>", "a": "<answer>"}}
  ],
  "use_cases": [
    {{"icon": "<emoji>", "title": "<15 words max>", "desc": "<30-40 words, concrete outcome>"}},
    {{"icon": "<emoji>", "title": "<title>", "desc": "<desc>"}},
    {{"icon": "<emoji>", "title": "<title>", "desc": "<desc>"}}
  ],
  "install_guide": {{
    "cmd": "<install/clone command>",
    "run": "<how to run it>",
    "note": "<one practical note about requirements or first-run>"
  }}
}}

Rules:
- pros/cons must be specific to THIS tool, not generic
- FAQs must answer real questions users have about THIS tool
- use_cases must name concrete measurable outcomes
- install_guide.cmd must be a real command from the GitHub repo"""

# ─── 生成单个工具 ──────────────────────────────────────────────────────────────

def generate_one(tool: dict, idx: int, total: int) -> Optional[dict]:
    name = tool['name']
    for attempt in range(3):
        try:
            resp = client.messages.create(
                model="claude-haiku-4-5",
                max_tokens=1200,
                system=SYSTEM,
                messages=[{"role": "user", "content": build_prompt(tool)}],
            )
            text = resp.content[0].text.strip()
            # 去掉可能的 markdown 包裹
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
            generated = json.loads(text)
            print(f"[{idx}/{total}] ✓ {name}")
            return generated
        except json.JSONDecodeError as e:
            print(f"[{idx}/{total}] ✗ JSON 解析失败 {name} (attempt {attempt+1}): {e}")
            time.sleep(2)
        except anthropic.RateLimitError:
            wait = 10 * (attempt + 1)
            print(f"[{idx}/{total}] 限流，等待 {wait}s …")
            time.sleep(wait)
        except Exception as e:
            print(f"[{idx}/{total}] 错误 {name} (attempt {attempt+1}): {e}")
            time.sleep(3)
    return None

# ─── 主流程 ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit",   type=int, default=0,  help="只处理前 N 个工具（0=全部）")
    parser.add_argument("--workers", type=int, default=5,  help="并发线程数")
    parser.add_argument("--ids",     type=str, default="", help="指定 id（逗号分隔）")
    args = parser.parse_args()

    # 读取数据
    with open(DATA_FILE, encoding="utf-8") as f:
        data = json.load(f)
    tools = data if isinstance(data, list) else data.get("tools", [])

    # 选出需要处理的工具
    if args.ids:
        id_set = set(args.ids.split(","))
        targets = [t for t in tools if t.get("id") in id_set and not t.get("pros")]
    else:
        targets = [t for t in tools if not t.get("pros")]

    if args.limit:
        targets = targets[:args.limit]

    total = len(targets)
    print(f"待处理: {total} 个工具（并发={args.workers}）")
    if total == 0:
        print("无需处理，退出。")
        return

    # 并发生成
    results: dict[str, dict] = {}
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(generate_one, t, i + 1, total): t
            for i, t in enumerate(targets)
        }
        for future in as_completed(futures):
            tool = futures[future]
            generated = future.result()
            if generated:
                results[tool["id"]] = generated
                # 实时写入 data.json（加锁）
                with lock:
                    for t in tools:
                        if t.get("id") == tool["id"] and generated:
                            t["pros"]          = generated.get("pros", [])
                            t["cons"]          = generated.get("cons", [])
                            t["faqs"]          = generated.get("faqs", [])
                            t["use_cases"]     = generated.get("use_cases", [])
                            t["install_guide"] = generated.get("install_guide", {})
                    with open(DATA_FILE, "w", encoding="utf-8") as f:
                        json.dump(tools if isinstance(data, list) else {**data, "tools": tools},
                                  f, indent=2, ensure_ascii=False)

    print(f"\n完成: {len(results)}/{total} 成功，{total - len(results)} 失败")
    print("运行 `python3 generate.py --force` 重新生成页面")

if __name__ == "__main__":
    main()

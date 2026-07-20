#!/usr/bin/env python3
"""
enrich_compare.py — 为缺少 sections+faqs 的 compare 页批量生成内容
目标：让所有 compare 页达到 1000+ 词，从薄内容变为有深度的对比指南

用法:
  python3 enrich_compare.py            # 处理全部薄 compare 条目
  python3 enrich_compare.py --limit 3  # 测试前 N 个
"""

import json, os, time, argparse, threading
from pathlib import Path
from typing import Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import anthropic

BASE_DIR     = Path(__file__).parent
COMPARE_FILE = BASE_DIR / "compare_data.json"
client       = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
lock         = threading.Lock()

SYSTEM = "You are a senior developer writing in-depth tool comparison guides. Return ONLY valid JSON, no markdown fences."

def build_prompt(item: dict) -> str:
    title  = item.get("title", "")
    intro  = item.get("intro", "")
    verdict = item.get("verdict", "")
    choose_a = item.get("choose_a", "")
    choose_b = item.get("choose_b", "")
    table  = json.dumps(item.get("table", []), ensure_ascii=False)
    name_a = item.get("tool_a_id", "").replace("-", " ").title()
    name_b = item.get("tool_b_id", "").replace("-", " ").title()

    return f"""Write detailed sections and FAQs for this tool comparison page.

Title: {title}
Intro: {intro}
Verdict: {verdict}
Choose {name_a} when: {choose_a}
Choose {name_b} when: {choose_b}
Comparison table: {table}

Generate 3 sections + 4 FAQs. Each section should be 100-150 words covering a specific real-world dimension (e.g. Performance, Learning Curve, Community & Ecosystem, Enterprise Readiness, Pricing Deep-Dive).

Return JSON:
{{
  "sections": [
    {{"id": "<slug>", "title": "<Section Title>", "content": "<100-150 word paragraph specific to these two tools>"}},
    {{"id": "<slug>", "title": "<Section Title>", "content": "<paragraph>"}},
    {{"id": "<slug>", "title": "<Section Title>", "content": "<paragraph>"}}
  ],
  "faqs": [
    {{"q": "<question users actually ask about {name_a} vs {name_b}>", "a": "<2-3 sentence answer>"}},
    {{"q": "<question>", "a": "<answer>"}},
    {{"q": "<question>", "a": "<answer>"}},
    {{"q": "<question>", "a": "<answer>"}}
  ]
}}

Rules:
- Sections must name BOTH tools specifically, not generic advice
- FAQs must reflect real search intent (e.g. "Is X faster than Y?", "Can I switch from X to Y?")
- No filler phrases like "both tools are great" or "it depends on your needs" without specifics"""


def process_one(item: dict, idx: int, total: int) -> Optional[dict]:
    slug = item.get("slug", "?")
    for attempt in range(3):
        try:
            resp = client.messages.create(
                model="claude-haiku-4-5",
                max_tokens=2000,
                system=SYSTEM,
                messages=[{"role": "user", "content": build_prompt(item)}],
            )
            text = resp.content[0].text.strip()
            if text.startswith("```"):
                lines = text.split("\n")
                text = "\n".join(lines[1:])
                if text.endswith("```"):
                    text = text[:-3]
            result = json.loads(text)
            print(f"[{idx}/{total}] ✓ {slug}")
            return result
        except json.JSONDecodeError as e:
            print(f"[{idx}/{total}] JSON错误 {slug} (attempt {attempt+1}): {e}")
            time.sleep(2)
        except anthropic.RateLimitError:
            wait = 10 * (attempt + 1)
            print(f"[{idx}/{total}] 限流，等 {wait}s …")
            time.sleep(wait)
        except Exception as e:
            print(f"[{idx}/{total}] 错误 {slug} (attempt {attempt+1}): {e}")
            time.sleep(3)
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit",   type=int, default=0)
    parser.add_argument("--workers", type=int, default=5)
    args = parser.parse_args()

    with open(COMPARE_FILE, encoding="utf-8") as f:
        raw = json.load(f)
    items = raw if isinstance(raw, list) else list(raw.values())

    # 只处理缺 sections 或 faqs 的条目
    targets = [x for x in items if not x.get("sections") or not x.get("faqs")]
    if args.limit:
        targets = targets[:args.limit]

    total = len(targets)
    print(f"待处理: {total} 个薄 compare 条目 | 并发: {args.workers}")

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(process_one, t, i+1, total): t for i, t in enumerate(targets)}
        ok = 0
        for future in as_completed(futures):
            item   = futures[future]
            result = future.result()
            if result:
                ok += 1
                with lock:
                    # 找到对应条目并更新
                    slug = item.get("slug")
                    if isinstance(raw, list):
                        for x in raw:
                            if x.get("slug") == slug:
                                x["sections"] = result.get("sections", [])
                                x["faqs"]     = result.get("faqs", [])
                    else:
                        if slug in raw:
                            raw[slug]["sections"] = result.get("sections", [])
                            raw[slug]["faqs"]     = result.get("faqs", [])
                    with open(COMPARE_FILE, "w", encoding="utf-8") as f:
                        json.dump(raw, f, indent=2, ensure_ascii=False)

    print(f"\n完成: {ok}/{total} 成功")
    print("运行 `python3 generate_compare.py` 重新生成 compare 页面")

if __name__ == "__main__":
    main()

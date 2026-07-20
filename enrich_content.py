#!/usr/bin/env python3
"""
enrich_content.py — 批量重写 expert_take + 生成 features_custom
- expert_take: 禁止模板句式，强制具体竞品比较 + 明确谁用/谁不用
- features_custom: 该工具专属功能列表，替代通用 TAG_FEATURES

用法:
  python3 enrich_content.py                     # 全量处理
  python3 enrich_content.py --mode expert_take  # 只重写 expert_take
  python3 enrich_content.py --mode features     # 只生成 features_custom
  python3 enrich_content.py --limit 5           # 测试前 N 个
  python3 enrich_content.py --workers 6         # 并发数
"""

import json, os, time, argparse, threading
from pathlib import Path
from typing import Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import anthropic

BASE_DIR  = Path(__file__).parent
DATA_FILE = BASE_DIR / "data.json"
client    = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
lock      = threading.Lock()

SYSTEM = "You are a senior developer advocate writing for an AI tools directory. Return ONLY valid JSON, no markdown fences."

# ── expert_take prompt ────────────────────────────────────────────────────────

BANNED_OPENINGS = [
    "A well-regarded project", "A specialized tool", "has found solid traction",
    "has established itself", "has gained", "is a solid choice"
]

def prompt_expert_take(tool: dict) -> str:
    banned = ", ".join(f'"{b}"' for b in BANNED_OPENINGS)
    return f"""Write a 3-sentence expert_take for this open-source AI tool.

Tool: {tool['name']} ({tool.get('starsLabel', tool.get('stars', ''))  } GitHub stars)
Description: {tool.get('descEn', '')}
Category: {tool.get('category', '')} | Tags: {', '.join(tool.get('tags', []))}
Key strength: {(tool.get('pros') or [''])[0]}

Rules (STRICTLY enforce):
1. NEVER start with these banned phrases: {banned}
2. Sentence 1: Name a SPECIFIC use case + why this tool fits it better than doing it another way
3. Sentence 2: Name ONE direct competitor and state a concrete difference (speed, ease, features)
4. Sentence 3: State who should NOT use it (be specific about the limitation)
5. Include the actual star count ({tool.get('starsLabel', '')}) once naturally
6. Max 60 words total

Return JSON: {{"expert_take": "<text>"}}"""

# ── features_custom prompt ────────────────────────────────────────────────────

def prompt_features(tool: dict) -> str:
    return f"""Generate 4-5 Key Features for this open-source AI tool.

Tool: {tool['name']}
Description: {tool.get('descEn', '')}
Tags: {', '.join(tool.get('tags', []))}
Pros: {json.dumps(tool.get('pros', [])[:3])}

Rules:
- Each feature must be SPECIFIC to {tool['name']}, not generic AI tool boilerplate
- Avoid phrases like "Seamless integration", "Battle-tested", "Enterprise-ready" unless literally true
- Use concrete numbers or specifics when known (e.g. "40+ model providers", "4-bit quantization")

Return JSON:
{{
  "features_custom": [
    {{"icon": "<emoji>", "title": "<name, ≤5 words>", "desc": "<25-35 words, specific outcome or capability>"}},
    ...
  ]
}}"""

# ── API call ──────────────────────────────────────────────────────────────────

def call_api(prompt: str, tool_name: str, idx: int, total: int, label: str) -> Optional[dict]:
    for attempt in range(3):
        try:
            resp = client.messages.create(
                model="claude-haiku-4-5",
                max_tokens=600,
                system=SYSTEM,
                messages=[{"role": "user", "content": prompt}],
            )
            text = resp.content[0].text.strip()
            if text.startswith("```"):
                text = "\n".join(text.split("\n")[1:])
                if text.endswith("```"):
                    text = text[:-3]
            return json.loads(text)
        except json.JSONDecodeError as e:
            print(f"[{idx}/{total}] JSON 错误 {tool_name}/{label} (attempt {attempt+1}): {e}")
            time.sleep(2)
        except anthropic.RateLimitError:
            wait = 10 * (attempt + 1)
            print(f"[{idx}/{total}] 限流，等 {wait}s …")
            time.sleep(wait)
        except Exception as e:
            print(f"[{idx}/{total}] 错误 {tool_name}/{label} (attempt {attempt+1}): {e}")
            time.sleep(3)
    return None

# ── worker ────────────────────────────────────────────────────────────────────

def process_tool(tool: dict, idx: int, total: int, mode: str) -> Optional[dict]:
    updates = {}

    if mode in ("expert_take", "both"):
        result = call_api(prompt_expert_take(tool), tool["name"], idx, total, "expert")
        if result and result.get("expert_take"):
            updates["expert_take"] = result["expert_take"]

    if mode in ("features", "both"):
        result = call_api(prompt_features(tool), tool["name"], idx, total, "features")
        if result and result.get("features_custom"):
            updates["features_custom"] = result["features_custom"]

    if updates:
        print(f"[{idx}/{total}] ✓ {tool['name']} ({', '.join(updates.keys())})")
    return updates if updates else None

# ── main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode",    choices=["expert_take", "features", "both"], default="both")
    parser.add_argument("--limit",   type=int, default=0)
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--force",   action="store_true", help="重写已有内容（默认跳过已有 features_custom）")
    args = parser.parse_args()

    with open(DATA_FILE, encoding="utf-8") as f:
        raw = json.load(f)
    tools = raw if isinstance(raw, list) else raw.get("tools", [])

    # 选目标：expert_take 全量重写（消除模板），features_custom 跳过已有的
    if args.mode == "features" and not args.force:
        targets = [t for t in tools if not t.get("features_custom")]
    elif args.mode == "expert_take":
        # 只重写有模板克隆的
        TEMPLATES = ["A well-regarded project", "A specialized tool", "has found solid traction",
                     "has established itself", "has gained", "is a solid choice"]
        targets = [t for t in tools if any(tmpl in (t.get("expert_take") or "") for tmpl in TEMPLATES)]
    else:
        targets = list(tools)

    if args.limit:
        targets = targets[:args.limit]

    total = len(targets)
    print(f"模式: {args.mode} | 待处理: {total} | 并发: {args.workers}")

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(process_tool, t, i + 1, total, args.mode): t
            for i, t in enumerate(targets)
        }
        ok = 0
        for future in as_completed(futures):
            tool    = futures[future]
            updates = future.result()
            if updates:
                ok += 1
                with lock:
                    for t in tools:
                        if t.get("id") == tool.get("id"):
                            t.update(updates)
                    out = tools if isinstance(raw, list) else {**raw, "tools": tools}
                    with open(DATA_FILE, "w", encoding="utf-8") as f:
                        json.dump(out, f, indent=2, ensure_ascii=False)

    print(f"\n完成: {ok}/{total} 成功")
    print("运行 `python3 generate.py --force` 重新生成页面")

if __name__ == "__main__":
    main()

"""
批量更新 10 个手写工具页面：添加 favorites.js、voting.js、收藏按钮、对比链接
"""
import re, os

BASE = os.path.dirname(__file__)

PAGES = {
    "cursor": "tools/cursor.html",
    "chatgpt": "tools/chatgpt.html",
    "claude-code": "tools/claude-code.html",
    "ollama": "tools/ollama.html",
    "langchain": "tools/langchain.html",
    "stable-diffusion": "tools/stable-diffusion.html",
    "llama-cpp": "tools/llama-cpp.html",
    "vllm": "tools/vllm.html",
    "autogpt": "tools/autogpt.html",
    "dify": "tools/dify.html",
}

SCRIPTS_INSERT = """\
<script src="../assets/favorites.js" defer></script>
<script src="../assets/voting.js" defer></script>
<script>
document.addEventListener('DOMContentLoaded', function() {{
  initFavoriteBtn('{tool_id}');
  initVoting('{tool_id}');
}});
</script>
<script src="../assets/cookie-consent.js" defer></script>"""

def patch(tool_id, path):
    full_path = os.path.join(BASE, path)
    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 跳过已处理的文件
    if "favorites.js" in content:
        print(f"  [skip] {path} 已包含 favorites.js")
        return

    # 1. 在 cta-btn-outline 的结束标签 </a> 后紧跟的 </div> 前插入按钮
    #    匹配 "cta-btn-outline" 所在 <a>...</a> 后的第一个 </div>
    FAV_BTN = (
        f'\n      <button id="favoriteBtn" class="fav-btn">♡ Save</button>\n'
        f'      <a href="../index.html?compare={tool_id}" class="tool-compare-btn">⚖️ Compare</a>'
    )

    # 找到 cta-btn-outline 的 </a> 后最近的 </div>
    pattern = r'(class="cta-btn-outline"[^>]*>(?:.*?)</a>[\s\n]*?)(</div>)'
    # 使用 DOTALL 匹配多行
    match = re.search(pattern, content, re.DOTALL)
    if match:
        # 替换第一个匹配（hero 区域的按钮组 div 结束）
        old = match.group(0)
        new = match.group(1) + FAV_BTN + "\n    " + match.group(2)
        content = content.replace(old, new, 1)
    else:
        print(f"  [warn] {path}: 未找到 cta-btn-outline 按钮模式，跳过按钮插入")

    # 2. 替换 cookie-consent.js 脚本引用，在前面插入 favorites.js 和 voting.js
    COOKIE_SCRIPT = '<script src="../assets/cookie-consent.js" defer></script>'
    if COOKIE_SCRIPT in content:
        replacement = SCRIPTS_INSERT.format(tool_id=tool_id)
        content = content.replace(COOKIE_SCRIPT, replacement, 1)
    else:
        print(f"  [warn] {path}: 未找到 cookie-consent.js，尝试插入到 </body>")
        content = content.replace(
            "</body>",
            SCRIPTS_INSERT.format(tool_id=tool_id) + "\n</body>",
            1
        )

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  [ok] {path}")

if __name__ == "__main__":
    for tid, p in PAGES.items():
        patch(tid, p)
    print("完成")

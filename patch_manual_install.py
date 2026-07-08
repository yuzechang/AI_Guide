#!/usr/bin/env python3
"""
为 6 个 MANUAL_PAGES 的 Getting Started 区域注入 <pre><code> 安装命令区块。
"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))
TOOLS_DIR = os.path.join(BASE, "tools")

# ─── 各页面替换映射 ─────────────────────────────────────────────

PATCHES = {
    "ollama.html": {
        "old": '''      <p>
        To get started with Ollama, visit the
        <a href="https://github.com/ollama/ollama" target="_blank" rel="noopener">GitHub repository</a>
        and follow the installation instructions in the README.
        Many AI tools provide Docker images for quick deployment:
        check the repository for the latest <code>docker-compose.yml</code> or installer script.
      </p>
      <div class="alert alert-info">''',
        "new": '''      <div style="background:var(--code-bg,#0d1117);border:1px solid var(--border);border-radius:8px;padding:16px 20px;margin:16px 0;overflow-x:auto">
        <pre style="margin:0;font-size:13px;color:#e6edf3;font-family:'JetBrains Mono',monospace,monospace"><code>curl -fsSL https://ollama.com/install.sh | sh</code></pre>
        <pre style="margin:8px 0 0;font-size:13px;color:#e6edf3;font-family:'JetBrains Mono',monospace,monospace"><code>ollama run llama3.2</code></pre>
      </div>
      <div class="alert alert-info">💡 macOS: <code>brew install ollama</code>. Windows: download .msi from <a href="https://ollama.com" target="_blank" rel="noopener">ollama.com</a>. First model download is ~2-4GB. For GPU acceleration, ensure NVIDIA drivers / CUDA / Metal are installed.</div>
      <div class="alert alert-info">'''
    },
    "stable-diffusion.html": {
        "old": '''      <p>
        To get started with Stable Diffusion WebUI, visit the
        <a href="https://github.com/AUTOMATIC1111/stable-diffusion-webui" target="_blank" rel="noopener">GitHub repository</a>
        and follow the installation instructions in the README.
        Many AI tools provide Docker images for quick deployment:
        check the repository for the latest <code>docker-compose.yml</code> or installer script.
      </p>
      <div class="alert alert-info">''',
        "new": '''      <div style="background:var(--code-bg,#0d1117);border:1px solid var(--border);border-radius:8px;padding:16px 20px;margin:16px 0;overflow-x:auto">
        <pre style="margin:0;font-size:13px;color:#e6edf3;font-family:'JetBrains Mono',monospace,monospace"><code>git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui</code></pre>
        <pre style="margin:8px 0 0;font-size:13px;color:#e6edf3;font-family:'JetBrains Mono',monospace,monospace"><code>cd stable-diffusion-webui && ./webui.sh</code></pre>
      </div>
      <div class="alert alert-info">💡 Windows: run <code>webui-user.bat</code>. Requires NVIDIA GPU 6GB+ VRAM (or <code>--use-cpu</code> for CPU-only). Python 3.10 recommended. First launch downloads several GB of model checkpoints.</div>
      <div class="alert alert-info">'''
    },
    "llama-cpp.html": {
        "old": '''      <p>
        To get started with llama.cpp, visit the
        <a href="https://github.com/ggerganov/llama.cpp" target="_blank" rel="noopener">GitHub repository</a>
        and follow the installation instructions in the README.
        Many AI tools provide Docker images for quick deployment:
        check the repository for the latest <code>docker-compose.yml</code> or installer script.
      </p>
      <div class="alert alert-info">''',
        "new": '''      <div style="background:var(--code-bg,#0d1117);border:1px solid var(--border);border-radius:8px;padding:16px 20px;margin:16px 0;overflow-x:auto">
        <pre style="margin:0;font-size:13px;color:#e6edf3;font-family:'JetBrains Mono',monospace,monospace"><code>git clone https://github.com/ggerganov/llama.cpp && cd llama.cpp && make -j</code></pre>
        <pre style="margin:8px 0 0;font-size:13px;color:#e6edf3;font-family:'JetBrains Mono',monospace,monospace"><code>./llama-cli -m model.gguf -p "Hello, world!"</code></pre>
      </div>
      <div class="alert alert-info">💡 macOS Apple Silicon: <code>make LLAMA_METAL=1</code>. Linux NVIDIA: <code>make LLAMA_CUDA=1</code>. Download GGUF models from Hugging Face (search "TheBloke" or "bartowski"). No Python or Docker required—pure C/C++ binary.</div>
      <div class="alert alert-info">'''
    },
    "autogpt.html": {
        "old": '''      <p>
        To get started with AutoGPT, visit the
        <a href="https://github.com/Significant-Gravitas/AutoGPT" target="_blank" rel="noopener">GitHub repository</a>
        and follow the installation instructions in the README.
        Agent frameworks typically require an API key for the LLM backend
        (OpenAI, Anthropic, or a local model via Ollama).
      </p>
      <div class="alert alert-info">''',
        "new": '''      <div style="background:var(--code-bg,#0d1117);border:1px solid var(--border);border-radius:8px;padding:16px 20px;margin:16px 0;overflow-x:auto">
        <pre style="margin:0;font-size:13px;color:#e6edf3;font-family:'JetBrains Mono',monospace,monospace"><code>git clone https://github.com/Significant-Gravitas/AutoGPT && cd AutoGPT</code></pre>
        <pre style="margin:8px 0 0;font-size:13px;color:#e6edf3;font-family:'JetBrains Mono',monospace,monospace"><code>docker compose up -d</code></pre>
      </div>
      <div class="alert alert-info">💡 Requires Docker and an OpenAI or Anthropic API key. Set <code>OPENAI_API_KEY</code> or <code>ANTHROPIC_API_KEY</code> in <code>.env</code> before starting. Web UI at <a href="http://localhost:8000" target="_blank" rel="noopener">http://localhost:8000</a>.</div>
      <div class="alert alert-info">'''
    },
    "dify.html": {
        "old": '''      <p>
        To get started with Dify, visit the
        <a href="https://github.com/langgenius/dify" target="_blank" rel="noopener">GitHub repository</a>
        and follow the installation instructions in the README.
        Agent frameworks typically require an API key for the LLM backend
        (OpenAI, Anthropic, or a local model via Ollama).
      </p>
      <div class="alert alert-info">''',
        "new": '''      <div style="background:var(--code-bg,#0d1117);border:1px solid var(--border);border-radius:8px;padding:16px 20px;margin:16px 0;overflow-x:auto">
        <pre style="margin:0;font-size:13px;color:#e6edf3;font-family:'JetBrains Mono',monospace,monospace"><code>git clone https://github.com/langgenius/dify && cd dify/docker</code></pre>
        <pre style="margin:8px 0 0;font-size:13px;color:#e6edf3;font-family:'JetBrains Mono',monospace,monospace"><code>docker compose up -d</code></pre>
      </div>
      <div class="alert alert-info">💡 Requires Docker & Docker Compose. Web UI at <a href="http://localhost:80" target="_blank" rel="noopener">http://localhost:80</a>. For production, configure PostgreSQL and Redis in <code>.env</code>. Cloud sandbox available at <a href="https://dify.ai" target="_blank" rel="noopener">dify.ai</a> for quick evaluation.</div>
      <div class="alert alert-info">'''
    },
    "cursor.html": {
        "old": '''      <h2 id="getting-started">Getting Started</h2>
      <ol>
        <li>Download Cursor from <a href="https://cursor.com" target="_blank" rel="noopener">cursor.com</a> for your OS.</li>
        <li>On first launch, import your VS Code settings (optional but recommended).</li>
        <li>Open a project and try <code>Cmd/Ctrl + K</code> to edit with AI inline, or <code>Cmd/Ctrl + I</code> for Composer.</li>
        <li>Create a <code>.cursorrules</code> file in your project root with your coding standards.</li>
        <li>Try Agent mode: open Composer, enable Agent, and describe a full feature to implement.</li>
      </ol>''',
        "new": '''      <h2 id="getting-started">Getting Started</h2>
      <div style="background:var(--code-bg,#0d1117);border:1px solid var(--border);border-radius:8px;padding:16px 20px;margin:16px 0;overflow-x:auto">
        <pre style="margin:0;font-size:13px;color:#e6edf3;font-family:'JetBrains Mono',monospace,monospace"><code># macOS: brew install --cask cursor
# Windows/Linux: download from https://cursor.com</code></pre>
      </div>
      <div class="alert alert-info">💡 Free tier includes 2000 completions and 50 slow premium requests per month. Pro ($20/mo) unlocks unlimited completions and 500 fast premium requests. Agent mode uses premium model credits.</div>
      <ol>
        <li>Download Cursor from <a href="https://cursor.com" target="_blank" rel="noopener">cursor.com</a> for your OS.</li>
        <li>On first launch, import your VS Code settings (optional but recommended).</li>
        <li>Open a project and try <code>Cmd/Ctrl + K</code> to edit with AI inline, or <code>Cmd/Ctrl + I</code> for Composer.</li>
        <li>Create a <code>.cursorrules</code> file in your project root with your coding standards.</li>
        <li>Try Agent mode: open Composer, enable Agent, and describe a full feature to implement.</li>
      </ol>''',
    },
}

changed = 0
for fname, patch in PATCHES.items():
    fpath = os.path.join(TOOLS_DIR, fname)
    with open(fpath, encoding="utf-8") as f:
        html = f.read()

    if patch["old"] not in html:
        print(f"[WARN] {fname} — 匹配文本未找到（可能已修改过），跳过")
        continue

    new_html = html.replace(patch["old"], patch["new"])
    if new_html == html:
        print(f"[SKIP] {fname} — 替换未生效")
        continue

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(new_html)
    changed += 1
    print(f"[OK] {fname} — 已注入安装命令代码块")

print(f"\n完成: {changed}/6 个页面已更新")

"""
为每篇博客文章末尾插入「Nolan 实际用法」模块（在 </article> 之前）
这个模块提供第一人称视角，是 E-E-A-T 中 Experience 的直接体现。
"""
import os, re

BASE = os.path.dirname(__file__)
BLOG_DIR = os.path.join(BASE, 'blog')

# 每篇博客的 Nolan 用法模块内容
NOLAN_SECTIONS = {
    "autogen-vs-crewai-vs-langgraph.html": """
      <div class="expert-take" style="margin-top:32px; margin-bottom:8px">
        <p><strong>What I actually use:</strong> LangGraph, for this project. I use it to prototype multi-step data pipelines that feed into AI_Guide's weekly trending page. The explicit state graph means I can inspect exactly what happened when something breaks — which happens more than I'd like. CrewAI was my first choice and I got a working prototype in an afternoon. Switched to LangGraph when I needed a human approval step before publishing, which CrewAI made awkward. AutoGen I've only used for research experiments where the conversation log is the output, not a side effect. If I were starting a new agent project today with no constraints, I'd prototype in CrewAI and migrate to LangGraph once the workflow stabilizes.</p>
        <cite>— Nolan (yuzc), maintainer of AI Nav</cite>
      </div>""",
    "ai-code-editors-compared-2026.html": """
      <div class="expert-take" style="margin-top:32px; margin-bottom:8px">
        <p><strong>What I actually use:</strong> Cursor, for everything in this project — from generating the 300+ tool detail pages to writing the comparison articles. The multi-file context makes it possible to have conversations like "this template generates all tool pages, update the FAQ section to match this format." One thing that surprised me: Cursor's @codebase gets noticeably slower on repos with many generated files, because it indexes dist/ and generated/ folders it shouldn't. The fix is adding them to .cursorignore — took me two hours to figure that out. Windsurf's Cascade is genuinely better for some autonomous tasks. I haven't switched because the friction of moving muscle memory isn't worth it yet.</p>
        <cite>— Nolan (yuzc), maintainer of AI Nav</cite>
      </div>""",
    "ai-code-assistants-2026.html": """
      <div class="expert-take" style="margin-top:32px; margin-bottom:8px">
        <p><strong>What I actually use:</strong> Cursor as my primary, Cline for tasks where I want agent-level file operations without leaving my workflow. The combination that works for me: Cursor for day-to-day coding and conversation, Cline when I need it to execute a multi-step task autonomously while I do something else. GitHub Copilot I dropped when Cursor's Tab autocomplete consistently predicted my next edit more accurately. The killer feature I didn't expect to value: seeing diffs before accepting, which Cursor does better than any alternative I've tried.</p>
        <cite>— Nolan (yuzc), maintainer of AI Nav</cite>
      </div>""",
    "ai-coding-assistants-compared.html": """
      <div class="expert-take" style="margin-top:32px; margin-bottom:8px">
        <p><strong>What I actually use:</strong> Cursor, day-to-day. I switched from GitHub Copilot after finding that Cursor's multi-file context made a real difference for this project — AI_Guide has 300+ generated pages with shared templates, and being able to ask "why does this tool page look different from the others" actually works. Aider I keep installed as a fallback for when I'm in a terminal SSH session and don't want to open a full IDE. The learning curve for Aider's git workflow is real, but once you're past it, the commit-as-checkpoint pattern is genuinely useful.</p>
        <cite>— Nolan (yuzc), maintainer of AI Nav</cite>
      </div>""",
    "langchain-vs-llamaindex.html": """
      <div class="expert-take" style="margin-top:32px; margin-bottom:8px">
        <p><strong>What I actually use:</strong> Neither, for most of this project — but I've built with both. LangChain for a document ingestion pipeline that feeds tool descriptions from GitHub READMEs into AI_Guide's data.json. LlamaIndex for a prototype Q&A system over the tools database. The LlamaIndex version was faster to get working for the retrieval part; the LangChain version was more flexible once I needed to add post-processing steps. From tracking GitHub star growth for both over 18 months: LlamaIndex's growth rate has outpaced LangChain's since late 2025. That's not a quality judgment — LangChain has 3x the absolute stars — but it tells you something about where developer curiosity is pointing.</p>
        <cite>— Nolan (yuzc), maintainer of AI Nav</cite>
      </div>""",
    "rag-pipeline-guide.html": """
      <div class="expert-take" style="margin-top:32px; margin-bottom:8px">
        <p><strong>What I actually use:</strong> A simple RAG pipeline over AI_Guide's tool descriptions using LlamaIndex + Chroma, running locally. The surprise: chunking strategy matters more than the embedding model for this use case. I tried three embedding models and two chunking strategies — the chunking change improved retrieval precision by more than any model swap. The stack I'd recommend for someone starting: LlamaIndex for the orchestration, Chroma for local development (zero config), migrate to Qdrant when you hit the point of needing complex filtering. Don't optimize the embedding model until you've optimized the chunking.</p>
        <cite>— Nolan (yuzc), maintainer of AI Nav</cite>
      </div>""",
    "build-production-rag-pipeline.html": """
      <div class="expert-take" style="margin-top:32px; margin-bottom:8px">
        <p><strong>What I actually use:</strong> Chroma for prototyping, Qdrant for anything that needs to stay up. Chroma's zero-config setup is genuinely a superpower for getting a RAG system running in an hour — I use it whenever I'm building a proof-of-concept. The production migration from Chroma to Qdrant is straightforward, which is the main reason I use Chroma for prototypes instead of Qdrant from the start. One thing the guides don't emphasize enough: the evaluation loop. I spent 80% of my time on a recent project debugging why certain queries returned wrong results, not on the pipeline itself. Build your evaluation set before you optimize anything else.</p>
        <cite>— Nolan (yuzc), maintainer of AI Nav</cite>
      </div>""",
    "run-llm-locally-guide.html": """
      <div class="expert-take" style="margin-top:32px; margin-bottom:8px">
        <p><strong>What I actually use:</strong> Ollama, exclusively. I run it on a MacBook Pro M3 Max and use it for drafting tool descriptions for AI_Guide before sending to a larger model for final polish. The Ollama + Open WebUI combination is genuinely good enough for most writing tasks. The model I land on for writing: Mistral 7B Instruct — faster than larger models, good enough for structured text, and the quality delta from Llama 3.1 8B is minimal for this use case. One thing that surprised me: the quantization level matters less than you'd expect above Q4. The jump from Q8 to Q4 is noticeable; from Q6 to Q8 is barely perceptible for writing tasks.</p>
        <cite>— Nolan (yuzc), maintainer of AI Nav</cite>
      </div>""",
    "llm-inference-optimization.html": """
      <div class="expert-take" style="margin-top:32px; margin-bottom:8px">
        <p><strong>What I actually use:</strong> vLLM for serving, when I have a GPU available. The PagedAttention memory management is not just a benchmark advantage — it's the difference between a service that degrades gracefully under load and one that crashes. SGLang I've been evaluating for structured generation tasks; the RadixAttention makes a real difference when you're generating the same type of output repeatedly (like tool descriptions from a template). For most people reading this: if you're doing local inference on consumer hardware, Ollama is the right choice. vLLM's complexity is only justified when you're serving multiple users or need batching.</p>
        <cite>— Nolan (yuzc), maintainer of AI Nav</cite>
      </div>""",
    "vector-databases-compared.html": """
      <div class="expert-take" style="margin-top:32px; margin-bottom:8px">
        <p><strong>What I actually use:</strong> Chroma for local development, Qdrant for anything beyond that. I've built with Weaviate and Milvus too, but both felt over-engineered for a project the size of AI_Guide. Qdrant's filtering performance is the practical reason I chose it for production — once you're combining semantic search with metadata filters (like "tools with 10k+ stars in the agent category"), Chroma's performance degrades and Qdrant stays fast. The thing nobody tells you when comparing vector databases: the operational complexity difference matters more than the benchmark numbers at most scales. Chroma requires zero ops; Qdrant requires minimal ops; Milvus requires dedicated ops attention.</p>
        <cite>— Nolan (yuzc), maintainer of AI Nav</cite>
      </div>""",
    "open-source-llms-guide-2026.html": """
      <div class="expert-take" style="margin-top:32px; margin-bottom:8px">
        <p><strong>What I actually use:</strong> Mistral 7B for local tasks, Qwen2.5 14B when I need better reasoning and have the VRAM. I track GitHub star growth for 300+ AI tools and the open-source LLM space is the most volatile part of the index — models that were "best in class" six months ago have been superseded multiple times. My practical take: don't optimize for the current best model. Optimize for the infrastructure (Ollama, vLLM) that lets you swap models without rewriting your application. The model you're running in 6 months will be better than anything available today, and the ones that age well are the ones with the best instruction-following consistency, not raw benchmark scores.</p>
        <cite>— Nolan (yuzc), maintainer of AI Nav</cite>
      </div>""",
    "open-source-multimodal-ai-2026.html": """
      <div class="expert-take" style="margin-top:32px; margin-bottom:8px">
        <p><strong>What I actually use:</strong> LLaVA via Ollama for local image analysis tasks — specifically, for analyzing screenshots of tool UIs when writing descriptions for AI_Guide. The quality is good enough for "describe what this interface does" but not for fine-grained layout analysis. InternVL2 is notably better for detailed visual reasoning tasks, but the Ollama integration is less mature. The multimodal space is moving faster than any other area I track — the star growth rate for multimodal tools has been the highest in the entire AI_Guide index over the past 6 months.</p>
        <cite>— Nolan (yuzc), maintainer of AI Nav</cite>
      </div>""",
    "comfyui-vs-a1111-vs-fooocus.html": """
      <div class="expert-take" style="margin-top:32px; margin-bottom:8px">
        <p><strong>What I actually use:</strong> ComfyUI, for anything beyond a quick test. I started with AUTOMATIC1111 because the community resources are unmatched — any LoRA or workflow you find online will have A1111 instructions. Switched to ComfyUI after I needed to build a reproducible image generation pipeline. The node graph is initially intimidating, but once you understand it, it's actually easier to debug than A1111's hidden extension interactions. Fooocus I recommend to people who ask "how do I get started with image generation without learning anything" — the output quality is excellent and the learning curve is essentially zero. One practical issue with all three: they assume you have discrete GPU VRAM that most people don't have.</p>
        <cite>— Nolan (yuzc), maintainer of AI Nav</cite>
      </div>""",
    "claude-vs-chatgpt-vs-gemini-2026.html": """
      <div class="expert-take" style="margin-top:32px; margin-bottom:8px">
        <p><strong>What I actually use:</strong> Claude for writing and coding (including building AI_Guide itself), ChatGPT for tasks where plugin integrations matter, Gemini for large context window tasks. Claude's code generation is consistently the best for my use case — writing Jinja2 templates, Python generation scripts, and debugging generate.py. The thing that's harder to benchmark: Claude pushes back when a request is unclear in a way that catches my mistakes before I run bad code. ChatGPT's broader tool ecosystem (DALL-E, web browsing, code interpreter in one place) is genuinely useful for research tasks. I don't have a strong recommendation — use the one that fits your workflow, and test with your actual tasks rather than benchmark leaderboards.</p>
        <cite>— Nolan (yuzc), maintainer of AI Nav</cite>
      </div>""",
    "mcp-tools-guide-2026.html": """
      <div class="expert-take" style="margin-top:32px; margin-bottom:8px">
        <p><strong>What I actually use:</strong> Several MCP servers with Claude Code for building AI_Guide — the filesystem MCP for bulk file operations, and a custom MCP server for querying the tools database. The practical upside of MCP over plain function calling: the separation of concern means I can use the same MCP servers across different AI clients without rewriting integrations. The current limitation I run into: MCP server discovery is still manual — there's no package manager equivalent, so finding reliable servers requires digging through GitHub. That's the gap the tools in this guide are starting to fill.</p>
        <cite>— Nolan (yuzc), maintainer of AI Nav</cite>
      </div>""",
    "ai-agent-frameworks-guide-2025.html": """
      <div class="expert-take" style="margin-top:32px; margin-bottom:8px">
        <p><strong>What I actually use:</strong> I've cycled through most frameworks in this guide while building AI_Guide's automation pipeline — from the weekly GitHub Stars update to the content generation scripts. My practical conclusion: the framework matters less than the task structure. When the task is linear (fetch → process → generate), no framework beats plain Python. When the task needs memory, branching, or retries, LangGraph's explicit state is worth the verbosity. The frameworks I see getting the most sustained developer interest based on GitHub star growth: LangGraph (accelerating), CrewAI (steady), AutoGen (plateauing). That trajectory tells you something about where the community is finding practical value.</p>
        <cite>— Nolan (yuzc), maintainer of AI Nav</cite>
      </div>""",
    "ai-prompt-engineering-guide-2026.html": """
      <div class="expert-take" style="margin-top:32px; margin-bottom:8px">
        <p><strong>What I actually use:</strong> Chain-of-thought for any task involving multi-step reasoning (writing tool comparisons, debugging code), structured output prompting for data extraction, and explicit persona context for writing tasks. The technique I rely on most that doesn't get enough coverage: showing the model what you don't want. Negative examples ("don't write it like this:") consistently outperform positive instructions alone for stylistic tasks. The one thing I'd tell someone new to prompt engineering: invest time in your system prompts, not individual queries. A well-written system prompt that captures your context, preferences, and constraints is worth more than any chain-of-thought trick.</p>
        <cite>— Nolan (yuzc), maintainer of AI Nav</cite>
      </div>""",
    "vllm-vs-ollama-production.html": """
      <div class="expert-take" style="margin-top:32px; margin-bottom:8px">
        <p><strong>What I actually use:</strong> Ollama locally, vLLM when I need to serve a model to multiple users or want proper batching. The decision point is simpler than most guides make it: if you're the only user, Ollama. If there are multiple concurrent users, vLLM. Everything else — throughput benchmarks, PagedAttention, continuous batching — matters only once you've crossed that threshold. One thing that surprised me setting up vLLM: the memory requirements are less predictable than Ollama, because PagedAttention allocates memory dynamically. Budget 20-30% more GPU VRAM than your model needs to avoid OOM errors under load.</p>
        <cite>— Nolan (yuzc), maintainer of AI Nav</cite>
      </div>""",
}

def patch_blog(fname, section_html):
    path = os.path.join(BLOG_DIR, fname)
    if not os.path.exists(path):
        print(f'  [skip] {fname}: 文件不存在')
        return

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'expert-take' in content and 'What I actually use' in content:
        print(f'  [skip] {fname}: 已有 Nolan 模块')
        return

    # 插入到 </article> 之前
    if '</article>' not in content:
        print(f'  [warn] {fname}: 未找到 </article>')
        return

    new_content = content.replace('</article>', section_html + '\n    </article>', 1)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'  [ok] {fname}')

for fname, section in NOLAN_SECTIONS.items():
    patch_blog(fname, section)

print('完成')

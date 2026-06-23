"""
为 49 个对比页生成差异化 meta description
每个 description 包含：核心差异点 + Stars 数字 + 使用场景
"""
import json, re, os

BASE = os.path.dirname(__file__)

with open(os.path.join(BASE, 'data.json')) as f:
    data = json.load(f)

TOOLS = {t['id']: t for t in data['tools']}

# 手写的差异化 description，格式：{compare-slug: description}
# 优先使用手写版本，其余自动生成
CUSTOM = {
    "cursor-vs-aider": "Cursor ($20/mo, IDE-native) vs Aider (free, terminal-native): Cursor wins for multi-file agent workflows; Aider wins for git-centric developers. {a_stars} vs {b_stars} GitHub Stars. Updated 2026.",
    "cursor-vs-github-copilot": "Cursor ($20/mo, context-aware edits) vs GitHub Copilot ($10-19/mo, IDE extension): Cursor excels at large refactors; Copilot integrates natively with VS Code. {a_stars} vs {b_stars} GitHub Stars.",
    "cline-vs-cursor": "Cline (free, VS Code extension with full file access) vs Cursor (paid, purpose-built IDE): Cline is the open-source alternative for developers who want agent-level coding without switching editors. {a_stars} vs {b_stars} Stars.",
    "langchain-vs-llamaindex": "LangChain (chains & agents, {a_stars} Stars) vs LlamaIndex (RAG & retrieval, {b_stars} Stars): LangChain for complex multi-step logic; LlamaIndex for document Q&A and search pipelines. 2026 benchmark included.",
    "langchain-vs-langgraph": "LangGraph is LangChain's stateful graph layer — same ecosystem, but adds explicit state machines for production agents. Use LangChain for quick chains; LangGraph for workflows that need loops, branching, or human-in-the-loop. {a_stars} vs {b_stars} Stars.",
    "langgraph-vs-crewai": "LangGraph (state graph, explicit control) vs CrewAI (role-based, conversational): LangGraph requires more code but handles complex branching; CrewAI gets multi-agent up in 30 lines. {a_stars} vs {b_stars} GitHub Stars.",
    "langgraph-vs-autogen": "LangGraph (explicit state, code-first) vs AutoGen (conversation-based, Microsoft-backed): LangGraph for fine-grained control; AutoGen for quick multi-agent chat workflows. {a_stars} vs {b_stars} Stars.",
    "crewai-vs-autogen": "CrewAI (role-based crews, simple setup) vs AutoGen (conversation graphs, Microsoft-backed): CrewAI in 30 lines; AutoGen for complex multi-agent communication patterns. {a_stars} vs {b_stars} GitHub Stars.",
    "autogpt-vs-autogen": "AutoGPT (autonomous task agent, first-gen) vs AutoGen (framework for multi-agent conversations): AutoGPT for hands-off task execution; AutoGen for building custom agent systems. {a_stars} vs {b_stars} Stars.",
    "dspy-vs-langchain": "DSPy (declarative LM programming, auto-optimization) vs LangChain (imperative chains): DSPy compiles prompts automatically; LangChain gives manual control. {a_stars} vs {b_stars} Stars. Best for different philosophies.",
    "ollama-vs-llama-cpp": "Ollama (model management + API server, one-line install) vs llama.cpp (raw C++ inference, maximum control): Ollama for developers; llama.cpp for researchers needing low-level access. {a_stars} vs {b_stars} Stars.",
    "ollama-vs-gpt4all": "Ollama (CLI + REST API, developer-focused) vs GPT4All (GUI + local chat, user-focused): Ollama for integrating local LLMs into apps; GPT4All for non-technical users. {a_stars} vs {b_stars} Stars.",
    "vllm-vs-ollama": "vLLM (production inference server, batching, 24x throughput) vs Ollama (local dev, model management): vLLM for serving LLMs at scale; Ollama for local development. {a_stars} vs {b_stars} GitHub Stars.",
    "vllm-vs-sglang": "vLLM (widest model compatibility) vs SGLang (RadixAttention, optimized for structured generation): SGLang 2-5x faster on repetitive prompts; vLLM easier to deploy. {a_stars} vs {b_stars} Stars.",
    "vllm-vs-lmdeploy": "vLLM (PagedAttention, broad model support) vs LMDeploy (TurboMind engine, optimized for LLaMA/Qwen): LMDeploy faster on supported models; vLLM more versatile. {a_stars} vs {b_stars} Stars.",
    "vllm-vs-tgi": "vLLM (Python-first, async engine) vs TGI (Hugging Face native, gRPC): TGI integrates with HF Hub natively; vLLM better community support and faster iteration. {a_stars} vs {b_stars} Stars.",
    "chroma-vs-qdrant": "Chroma (zero-config, local-first, Python-native) vs Qdrant (Rust, production-grade, gRPC + filtering): Chroma for prototyping; Qdrant for production with complex filtering. {a_stars} vs {b_stars} Stars.",
    "chroma-vs-weaviate": "Chroma (simple local setup, minimal config) vs Weaviate (multi-modal, modules, cloud-managed): Chroma for fast RAG prototyping; Weaviate for enterprise multi-modal search. {a_stars} vs {b_stars} Stars.",
    "qdrant-vs-milvus": "Qdrant (Rust, fast filtering, cloud-native) vs Milvus (billion-scale, distributed, GPU support): Qdrant for mid-scale production; Milvus for billion-vector enterprise workloads. {a_stars} vs {b_stars} Stars.",
    "comfyui-vs-stable-diffusion-webui": "ComfyUI (node-based workflow, advanced control) vs AUTOMATIC1111 (feature-rich UI, huge extensions library): ComfyUI for power users building pipelines; A1111 for quick generation with community extensions. {a_stars} vs {b_stars} Stars.",
    "fooocus-vs-comfyui": "Fooocus (Midjourney-like UX, minimal setup) vs ComfyUI (node graph, unlimited control): Fooocus for beautiful results without configuration; ComfyUI for custom pipelines. {a_stars} vs {b_stars} Stars.",
    "flux-vs-stable-diffusion": "FLUX.1 (Black Forest Labs, state-of-art quality 2024-2026) vs Stable Diffusion (ecosystem leader, 10k+ models): FLUX for best output quality; SD for community resources and LoRA library. {a_stars} vs {b_stars} Stars.",
    "sd-webui-vs-invokeai": "AUTOMATIC1111 (largest extension ecosystem, community-driven) vs InvokeAI (professional workflow, unified canvas): A1111 for plugin variety; InvokeAI for professional image editing workflows. {a_stars} vs {b_stars} Stars.",
    "dify-vs-flowise": "Dify (full LLM app platform, built-in RAG + datasets) vs Flowise (LangChain visual builder, simpler): Dify for production LLM applications; Flowise for quick LangChain prototyping. {a_stars} vs {b_stars} Stars.",
    "langflow-vs-flowise": "Langflow (visual LangChain + data science) vs Flowise (simpler visual builder): Langflow for complex data pipelines; Flowise for rapid no-code chatbot prototyping. {a_stars} vs {b_stars} Stars.",
    "n8n-vs-dify": "n8n (general automation + AI nodes, 600+ integrations) vs Dify (LLM-first app platform, AI-native): n8n to add AI into existing workflows; Dify to build AI-first products. {a_stars} vs {b_stars} Stars.",
    "n8n-vs-langchain": "n8n (no-code automation with LLM nodes) vs LangChain (code-first LLM framework): n8n for business automation with AI; LangChain for developers building custom LLM logic. {a_stars} vs {b_stars} Stars.",
    "open-webui-vs-librechat": "Open WebUI (Ollama-native, self-hosted ChatGPT UI) vs LibreChat (multi-model, supports 30+ providers): Open WebUI for local LLM users; LibreChat for teams needing multi-provider access. {a_stars} vs {b_stars} Stars.",
    "anything-llm-vs-privateGPT": "AnythingLLM (multi-model, teams, document workspace) vs PrivateGPT (offline-first, privacy-absolute): AnythingLLM for teams with multiple docs; PrivateGPT for zero-data-leak local deployment. {a_stars} vs {b_stars} Stars.",
    "khoj-vs-anything-llm": "Khoj (personal AI assistant, notes + web search) vs AnythingLLM (team document workspace): Khoj for personal knowledge management; AnythingLLM for team document Q&A. {a_stars} vs {b_stars} Stars.",
    "llamafile-vs-ollama": "Llamafile (single executable, runs anywhere, no install) vs Ollama (model manager + API, dev-friendly): Llamafile for portability; Ollama for local development with API integration. {a_stars} vs {b_stars} Stars.",
    "aider-vs-openhands": "Aider (terminal pair programming, git-integrated) vs OpenHands (full software engineering agent, web UI): Aider for line-by-line coding help; OpenHands for autonomous multi-step software tasks. {a_stars} vs {b_stars} Stars.",
    "gpt-engineer-vs-aider": "GPT Engineer (project scaffolding from spec) vs Aider (ongoing coding partner, git-native): GPT Engineer for starting projects; Aider for iterating on existing codebases. {a_stars} vs {b_stars} Stars.",
    "swe-agent-vs-openhands": "SWE-agent (GitHub issue solver, research-focused) vs OpenHands (full-featured software agent, plugin ecosystem): SWE-agent for automated PR generation; OpenHands for broader development tasks. {a_stars} vs {b_stars} Stars.",
    "phidata-vs-crewai": "Phidata (full-stack agent toolkit + built-in tools) vs CrewAI (role-based multi-agent crews): Phidata for agents with storage, memory, and knowledge; CrewAI for coordinated role-based teams. {a_stars} vs {b_stars} Stars.",
    "smolagents-vs-crewai": "SmolAgents (Hugging Face, code-first, minimal) vs CrewAI (role-based, task orchestration): SmolAgents for code execution agents; CrewAI for multi-role task delegation. {a_stars} vs {b_stars} Stars.",
    "pydantic-ai-vs-langchain": "PydanticAI (type-safe, dependency injection, structured) vs LangChain (mature ecosystem, broad integrations): PydanticAI for production type-safety; LangChain for ecosystem and community. {a_stars} vs {b_stars} Stars.",
    "llama-factory-vs-axolotl": "LLaMA-Factory (GUI + CLI fine-tuning, 100+ models) vs Axolotl (flexible YAML config, power users): LLaMA-Factory for teams; Axolotl for researchers who want fine-grained control. {a_stars} vs {b_stars} Stars.",
    "unsloth-vs-llama-factory": "Unsloth (2x faster training, 80% less VRAM) vs LLaMA-Factory (broader model support, web UI): Unsloth for resource-constrained fine-tuning; LLaMA-Factory for easier multi-model training. {a_stars} vs {b_stars} Stars.",
    "deepspeed-vs-unsloth": "DeepSpeed (distributed training, ZeRO sharding, enterprise scale) vs Unsloth (single-GPU optimization, consumer hardware): DeepSpeed for multi-GPU clusters; Unsloth for fast fine-tuning on one GPU. {a_stars} vs {b_stars} Stars.",
    "peft-vs-trl": "PEFT (LoRA/QLoRA parameter-efficient fine-tuning) vs TRL (RLHF, DPO, reward model training): PEFT for adapter-based fine-tuning; TRL for alignment and preference training. {a_stars} vs {b_stars} Stars.",
    "mlflow-vs-langfuse": "MLflow (full ML lifecycle, 10+ year ecosystem) vs Langfuse (LLM-native observability, traces + evals): MLflow for traditional ML tracking; Langfuse for LLM prompt debugging and cost analysis. {a_stars} vs {b_stars} Stars.",
    "langchain-vs-haystack": "LangChain (broader ecosystem, agents + chains) vs Haystack (production NLP pipelines, document processing): LangChain for flexible agent building; Haystack for document-heavy enterprise search. {a_stars} vs {b_stars} Stars.",
    "llamaindex-vs-haystack": "LlamaIndex (LLM data framework, 35+ data connectors) vs Haystack (modular NLP pipeline, enterprise-ready): LlamaIndex for LLM-first RAG; Haystack for production document processing at scale. {a_stars} vs {b_stars} Stars.",
    "whisper-vs-faster-whisper": "OpenAI Whisper (reference implementation, all languages) vs Faster Whisper (4x speed, CTranslate2, same accuracy): Use Faster Whisper in production; Whisper for reference or fine-tuning. {a_stars} vs {b_stars} Stars.",
    "whisperx-vs-faster-whisper": "WhisperX (word-level timestamps + diarization) vs Faster Whisper (pure speed): WhisperX for subtitles and speaker separation; Faster Whisper for maximum throughput. {a_stars} vs {b_stars} Stars.",
    "text-gen-webui-vs-ollama": "Oobabooga text-gen-webui (desktop UI, 50+ loader backends) vs Ollama (CLI + REST API, model management): text-gen-webui for local UI experimentation; Ollama for integrating local LLMs into apps. {a_stars} vs {b_stars} Stars.",
}

def get_stars_label(tool_id):
    if tool_id in TOOLS:
        return TOOLS[tool_id].get('starsLabel', '?k+')
    return '?k+'

def slug_to_ids(slug):
    """从 a-vs-b 格式提取两个工具 id"""
    if '-vs-' in slug:
        parts = slug.split('-vs-', 1)
        return parts[0], parts[1]
    return slug, slug

def auto_description(slug, a_id, b_id):
    a = TOOLS.get(a_id, {})
    b = TOOLS.get(b_id, {})
    a_name = a.get('name', a_id)
    b_name = b.get('name', b_id)
    a_stars = a.get('starsLabel', '?k+')
    b_stars = b.get('starsLabel', '?k+')
    a_desc = a.get('descEn', '')[:60]
    b_desc = b.get('descEn', '')[:60]
    return (
        f"{a_name} ({a_stars} GitHub Stars, {a_desc}) vs "
        f"{b_name} ({b_stars} Stars, {b_desc}). "
        f"Side-by-side comparison of features, use cases, and expert recommendation. 2026."
    )

compare_dir = os.path.join(BASE, 'compare')
updated = 0
skipped = 0

for fname in sorted(os.listdir(compare_dir)):
    if not fname.endswith('.html') or fname == 'index.html':
        continue
    slug = fname[:-5]  # remove .html
    path = os.path.join(compare_dir, fname)

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    a_id, b_id = slug_to_ids(slug)
    a_stars = get_stars_label(a_id)
    b_stars = get_stars_label(b_id)

    if slug in CUSTOM:
        new_desc = CUSTOM[slug].format(a_stars=a_stars, b_stars=b_stars)
    else:
        new_desc = auto_description(slug, a_id, b_id)

    # 替换 meta description
    old_pattern = re.compile(r'<meta name="description" content="[^"]*">')
    new_tag = f'<meta name="description" content="{new_desc}">'
    new_content, n = old_pattern.subn(new_tag, content, count=1)

    if n == 0:
        print(f'  [skip] {fname}: 未找到 description')
        skipped += 1
        continue

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    updated += 1

print(f'完成: 更新 {updated} 个对比页，跳过 {skipped} 个')

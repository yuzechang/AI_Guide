"""
为 49 个对比页重写 <title> 标签
原版全是 "{A} vs {B} (2026): Which Should You Choose?" — 无区分度，CTR 极低
新版：给出具体结论/核心差异，让用户一眼看懂值不值得点
"""
import re, os

BASE = os.path.dirname(__file__)
COMPARE_DIR = os.path.join(BASE, 'compare')

# 手写优化版 title，优先使用
# 规则：包含核心差异/使用场景/结论，不超过60字符（含品牌）
CUSTOM_TITLES = {
    "cursor-vs-aider":
        "Cursor vs Aider (2026): IDE vs Terminal — Picking the Right AI Coder | AI Nav",
    "cursor-vs-github-copilot":
        "Cursor vs GitHub Copilot (2026): Better Context vs Tighter VS Code Integration | AI Nav",
    "cursor-vs-continue":
        "Cursor vs Continue (2026): Paid IDE vs Free VS Code Extension Compared | AI Nav",
    "cursor-vs-claude-code":
        "Cursor vs Claude Code (2026): Interactive Edits vs Agentic Autonomy | AI Nav",
    "cline-vs-cursor":
        "Cline vs Cursor (2026): Free Open-Source Agent vs $20/mo IDE | AI Nav",
    "aider-vs-openhands":
        "Aider vs OpenHands (2026): Terminal Pair Programmer vs Full Agent | AI Nav",
    "gpt-engineer-vs-aider":
        "GPT Engineer vs Aider (2026): Project Scaffolding vs Ongoing Coding Partner | AI Nav",
    "swe-agent-vs-openhands":
        "SWE-agent vs OpenHands (2026): GitHub Issue Solver vs Full Dev Agent | AI Nav",
    "langchain-vs-llamaindex":
        "LangChain vs LlamaIndex (2026): Chains & Agents vs RAG & Retrieval | AI Nav",
    "langchain-vs-langgraph":
        "LangChain vs LangGraph (2026): Quick Chains vs Stateful Production Agents | AI Nav",
    "langchain-vs-haystack":
        "LangChain vs Haystack (2026): Flexible Agents vs Enterprise NLP Pipelines | AI Nav",
    "langchain-vs-dspy":
        "LangChain vs DSPy (2026): Manual Prompts vs Auto-Optimized Programs | AI Nav",
    "langgraph-vs-crewai":
        "LangGraph vs CrewAI (2026): Explicit Control vs Fast Multi-Agent Setup | AI Nav",
    "langgraph-vs-autogen":
        "LangGraph vs AutoGen (2026): Code-First State vs Conversation Graphs | AI Nav",
    "crewai-vs-autogen":
        "CrewAI vs AutoGen (2026): Role-Based Crews vs MS Conversation Agents | AI Nav",
    "autogpt-vs-autogen":
        "AutoGPT vs AutoGen (2026): Autonomous Tasks vs Custom Agent Frameworks | AI Nav",
    "phidata-vs-crewai":
        "Phidata vs CrewAI (2026): Full-Stack Agent Toolkit vs Role-Based Teams | AI Nav",
    "smolagents-vs-crewai":
        "SmolAgents vs CrewAI (2026): Code-First Minimal Agent vs Multi-Role Teams | AI Nav",
    "pydantic-ai-vs-langchain":
        "PydanticAI vs LangChain (2026): Type-Safe Production vs Ecosystem Breadth | AI Nav",
    "dspy-vs-langchain":
        "DSPy vs LangChain (2026): Compiled Prompts vs Manual Chain Building | AI Nav",
    "vllm-vs-ollama":
        "vLLM vs Ollama (2026): Production Inference Server vs Local Dev Setup | AI Nav",
    "vllm-vs-sglang":
        "vLLM vs SGLang (2026): Broad Compatibility vs Faster Structured Output | AI Nav",
    "vllm-vs-lmdeploy":
        "vLLM vs LMDeploy (2026): Versatile vs Faster on LLaMA/Qwen Models | AI Nav",
    "vllm-vs-tgi":
        "vLLM vs TGI (2026): Python-First Async vs Hugging Face Native gRPC | AI Nav",
    "ollama-vs-llama-cpp":
        "Ollama vs llama.cpp (2026): Easy Model Manager vs Raw C++ Inference | AI Nav",
    "ollama-vs-gpt4all":
        "Ollama vs GPT4All (2026): Developer API vs Non-Technical Desktop App | AI Nav",
    "ollama-vs-lm-studio":
        "Ollama vs LM Studio (2026): CLI + API vs Point-and-Click GUI | AI Nav",
    "llamafile-vs-ollama":
        "Llamafile vs Ollama (2026): Single Portable Exe vs Dev-Friendly API | AI Nav",
    "text-gen-webui-vs-ollama":
        "Oobabooga vs Ollama (2026): 50+ Loaders Desktop UI vs Clean REST API | AI Nav",
    "chroma-vs-qdrant":
        "Chroma vs Qdrant (2026): Zero-Config Prototype vs Production Filtering | AI Nav",
    "chroma-vs-weaviate":
        "Chroma vs Weaviate (2026): Simple Local RAG vs Multi-Modal Enterprise Search | AI Nav",
    "qdrant-vs-milvus":
        "Qdrant vs Milvus (2026): Mid-Scale Production vs Billion-Vector Enterprise | AI Nav",
    "comfyui-vs-stable-diffusion-webui":
        "ComfyUI vs AUTOMATIC1111 (2026): Node Workflows vs Massive Extension Library | AI Nav",
    "fooocus-vs-comfyui":
        "Fooocus vs ComfyUI (2026): Zero-Config Beautiful Results vs Full Pipeline Control | AI Nav",
    "flux-vs-stable-diffusion":
        "FLUX vs Stable Diffusion (2026): Best Quality 2026 vs Largest Ecosystem | AI Nav",
    "sd-webui-vs-invokeai":
        "AUTOMATIC1111 vs InvokeAI (2026): Most Extensions vs Professional Canvas | AI Nav",
    "dify-vs-flowise":
        "Dify vs Flowise (2026): Full LLM App Platform vs Quick LangChain Builder | AI Nav",
    "langflow-vs-flowise":
        "Langflow vs Flowise (2026): Data Science Pipelines vs Rapid No-Code Bots | AI Nav",
    "n8n-vs-dify":
        "n8n vs Dify (2026): 600+ Integrations vs AI-Native App Builder | AI Nav",
    "n8n-vs-langchain":
        "n8n vs LangChain (2026): No-Code Automation vs Code-First LLM Framework | AI Nav",
    "open-webui-vs-librechat":
        "Open WebUI vs LibreChat (2026): Ollama-Native vs 30-Provider Multi-Model | AI Nav",
    "anything-llm-vs-privateGPT":
        "AnythingLLM vs PrivateGPT (2026): Team Docs Workspace vs Offline-First Privacy | AI Nav",
    "khoj-vs-anything-llm":
        "Khoj vs AnythingLLM (2026): Personal AI Assistant vs Team Document Q&A | AI Nav",
    "llama-factory-vs-axolotl":
        "LLaMA-Factory vs Axolotl (2026): GUI Fine-Tuning vs Power-User YAML Config | AI Nav",
    "unsloth-vs-llama-factory":
        "Unsloth vs LLaMA-Factory (2026): 2x Faster Training vs Broader Model Support | AI Nav",
    "deepspeed-vs-unsloth":
        "DeepSpeed vs Unsloth (2026): Multi-GPU Clusters vs Fast Single-GPU Training | AI Nav",
    "peft-vs-trl":
        "PEFT vs TRL (2026): LoRA Adapters vs RLHF & Alignment Training | AI Nav",
    "mlflow-vs-langfuse":
        "MLflow vs Langfuse (2026): Full ML Lifecycle vs LLM-Native Observability | AI Nav",
    "llamaindex-vs-haystack":
        "LlamaIndex vs Haystack (2026): LLM-First RAG vs Enterprise NLP at Scale | AI Nav",
    "whisper-vs-faster-whisper":
        "Whisper vs Faster-Whisper (2026): Reference vs 4x Speed Same Accuracy | AI Nav",
    "whisperx-vs-faster-whisper":
        "WhisperX vs Faster-Whisper (2026): Word Timestamps + Diarization vs Raw Speed | AI Nav",
}

def patch_title(fname, new_title):
    path = os.path.join(COMPARE_DIR, fname)
    if not os.path.exists(path):
        print(f'  [skip] {fname}: 文件不存在')
        return False

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = re.sub(
        r'<title>[^<]*</title>',
        f'<title>{new_title}</title>',
        content,
        count=1
    )

    if new_content == content:
        print(f'  [skip] {fname}: title 未变化')
        return False

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True

updated = 0
skipped = 0

for slug, title in CUSTOM_TITLES.items():
    fname = slug + '.html'
    if patch_title(fname, title):
        print(f'  [ok] {fname}')
        updated += 1
    else:
        skipped += 1

print(f'\n完成：更新 {updated} 个对比页 title，跳过 {skipped} 个')

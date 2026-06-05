#!/usr/bin/env python3
"""
generate.py – 静态工具详情页批量生成器
SSG (Static Site Generation) 思路：从 data.json 读取数据，渲染 Jinja2 模板，
输出到 tools/{id}.html，并同步更新 sitemap.xml。

用法:
  python3 generate.py                    # 生成全部新页面（跳过已有手写页）
  python3 generate.py --ids cursor,dify  # 只生成指定工具
  python3 generate.py --force            # 强制覆盖（含手写页）
  python3 generate.py --sitemap-only     # 只更新 sitemap
  python3 generate.py --dry-run          # 只打印计划，不写文件
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import date
from jinja2 import Environment, FileSystemLoader, select_autoescape

# ─── 路径 ───────────────────────────────────────────────────────────────────
BASE_DIR      = Path(__file__).parent
DATA_FILE     = BASE_DIR / "data.json"
COMPARE_FILE  = BASE_DIR / "compare_data.json"
TEMPLATES_DIR = BASE_DIR / "templates"
TOOLS_DIR     = BASE_DIR / "tools"
CATEGORY_DIR  = BASE_DIR / "category"
SITEMAP_FILE  = BASE_DIR / "sitemap.xml"

BASE_URL = "https://yuzec.com"
TODAY    = date.today().isoformat()

# ─── 手写详情页（id → html 文件名，跳过自动生成）────────────────────────────
MANUAL_PAGES = {
    "cursor":       "cursor",
    "claude-code":  "claude-code",
    "chatgpt":      "chatgpt",
    "ollama":       "ollama",
    "langchain":    "langchain",
    "sd-webui":     "stable-diffusion",
    "llama-cpp":    "llama-cpp",
    "vllm":         "vllm",
    "autogpt":      "autogpt",
    "dify":         "dify",
}

# ─── Tag → 功能描述 ──────────────────────────────────────────────────────────
TAG_FEATURES = {
    "llm":              ("🤖", "LLM Integration",        "Seamless integration with major LLMs including GPT-4o, Claude 4, Llama 3, and Mistral for text generation and reasoning."),
    "rag":              ("🧠", "RAG Pipeline",            "Retrieval-Augmented Generation that grounds LLM responses in your own documents and real-time data sources."),
    "code":             ("💻", "Code Intelligence",       "AI-powered code generation, completion, review, and refactoring across all major programming languages."),
    "chat":             ("💬", "Conversational AI",       "Multi-turn dialogue management with context retention, conversation history, and session persistence."),
    "local":            ("🏠", "Local Deployment",        "Run entirely on your own hardware—no cloud dependency, no data egress, full privacy by design."),
    "privacy":          ("🔒", "Privacy-First",           "All data stays in your infrastructure with no external telemetry, cold storage, or third-party access."),
    "image":            ("🎨", "Image Generation",        "AI-powered image synthesis and editing using state-of-the-art diffusion models (SDXL, FLUX, etc.)."),
    "audio":            ("🎙️", "Audio Processing",        "Speech recognition, synthesis, and audio analysis with support for real-time and batch workloads."),
    "speech":           ("🎙️", "Speech Capabilities",    "Text-to-speech, speech-to-text, and voice interface support with multi-language coverage."),
    "generative":       ("✨", "Generative AI",           "Create novel content—images, text, audio, video—using state-of-the-art generative models."),
    "framework":        ("⚙️", "Modular Framework",       "Extensible architecture with plugin support; customize and extend for your specific use case."),
    "workflow":         ("🔄", "Workflow Orchestration",  "Visual or programmatic pipeline composition for complex multi-step AI workflows with branching logic."),
    "agent":            ("🤖", "Agent Capabilities",      "Autonomous task execution with planning, tool use, self-correction, and iterative goal pursuit."),
    "autonomous":       ("🚀", "Autonomous Execution",    "Self-directed task completion—set a goal and the system plans and executes without step-by-step guidance."),
    "vector-db":        ("🗄️", "Vector Storage",         "Efficient storage and similarity search for high-dimensional embeddings at millions-of-record scale."),
    "embeddings":       ("🧮", "Embeddings",              "Dense vector representations enabling semantic search, clustering, and retrieval by meaning."),
    "inference":        ("⚡", "High-Performance Inference","Optimized model inference with quantization support, batching, and sub-second latency."),
    "search":           ("🔍", "Semantic Search",         "Vector-based similarity search finds relevant content by meaning—not just keyword matching."),
    "sql":              ("🗃️", "SQL & Structured Data",  "Natural language interfaces for querying relational databases, spreadsheets, and structured APIs."),
    "data":             ("📈", "Data Analysis",           "Statistical analysis, chart generation, and insight extraction from structured datasets."),
    "multi-modal":      ("🌐", "Multimodal",              "Unified handling of text, images, audio, and video inputs and outputs in a single pipeline."),
    "productivity":     ("⚡", "Developer Productivity",  "Streamline workflows and automate repetitive tasks to measurably increase engineering output."),
    "platform":         ("🏗️", "Platform",               "Comprehensive infrastructure for building, testing, and deploying AI applications at scale."),
    "no-code":          ("🧩", "No-Code Builder",         "Visual drag-and-drop interface for building AI applications without writing application code."),
    "sdk":              ("📦", "SDK & Client Libraries",  "Official SDKs in Python, JavaScript, Go, and more for programmatic integration."),
    "visualization":    ("📊", "Visualization",           "Charts, graphs, and dashboards for understanding model outputs, latency, and data distributions."),
    "open-source":      ("🔓", "Open Source",             "MIT/Apache licensed—inspect, fork, modify, and self-host with no vendor lock-in."),
    "web-ui":           ("🖥️", "Web Interface",          "Browser-based GUI accessible from any device without local installation required."),
    "microsoft":        ("🪟", "Microsoft Ecosystem",    "Deep integration with Azure, GitHub, VS Code, and the broader Microsoft developer platform."),
    "research":         ("🔬", "Research-Grade",          "Designed for AI/ML research with experiment tracking, reproducibility, and ablation study support."),
    "education":        ("📚", "Educational",             "Learning-focused with tutorials, worked examples, and structured curricula for onboarding."),
    "structured-output":("📋", "Structured Output",       "Enforce typed, validated responses from LLMs using Pydantic, JSON Schema, or custom validators."),
    "nlp":              ("🔤", "NLP Processing",          "Natural language processing including tokenization, named entity recognition, and parsing."),
    "fine-tuning":      ("🎯", "Fine-Tuning",             "Customize pre-trained models on domain-specific data for improved accuracy and specialization."),
    "training":         ("🏋️", "Model Training",         "Full training capabilities from scratch or continued pre-training on custom large-scale datasets."),
    "deployment":       ("☁️", "Deployment",              "Production infrastructure with auto-scaling, rolling updates, health checks, and monitoring."),
    "api":              ("🔌", "API Integration",         "RESTful APIs and webhooks for integrating AI capabilities into existing systems and services."),
    "memory":           ("💾", "Memory Management",       "Persistent short-term and long-term memory for agents and chatbots across sessions."),
}

# ─── 分类元数据 ──────────────────────────────────────────────────────────────
CATEGORY_INFO = {
    "ai-tools": {
        "label": "AI Tool", "labelCn": "AI 工具", "icon": "🤖",
        "color": "#818cf8", "app_category": "AIApplication",
        "type": "end-user AI application",
        "use_cases": [
            {"icon": "🚀", "title": "Rapid Prototyping",       "desc": "Build and test AI-powered features in hours, not weeks, with ready-made interfaces and integrations."},
            {"icon": "⚡", "title": "Developer Productivity",  "desc": "Automate repetitive coding, documentation, and analysis tasks to reclaim hours in every sprint."},
            {"icon": "🔍", "title": "Research & Analysis",     "desc": "Process large volumes of text, images, or structured data with AI to extract actionable insights."},
            {"icon": "🏠", "title": "Local & Private AI",      "desc": "Run AI workloads on your own hardware for complete data privacy—no cloud subscription required."},
        ],
        "faq": [
            ("Is {name} free to use?",
             "{name} is open-source and free to self-host (MIT or Apache license). Some advanced cloud-hosted tiers have pricing. Check the GitHub repository and official website for the latest licensing and pricing details."),
            ("Does {name} require a GPU?",
             "It depends on the specific workload. Many AI tools run on CPU with acceptable performance for light use. For intensive image generation or large model inference, a modern NVIDIA GPU (8GB+ VRAM) significantly improves speed."),
            ("What are the best alternatives to {name}?",
             "The AI Nav directory lists 100+ tools in the AI Tools category. Use the tag filter to find tools with similar capabilities, or browse the 'Similar Tools' section on this page for direct alternatives."),
            ("Can {name} be self-hosted for enterprise privacy?",
             "Yes. As an open-source project, {name} can be deployed on your own servers, Kubernetes cluster, or private cloud. This eliminates data egress concerns and satisfies compliance requirements like SOC 2, HIPAA, and GDPR."),
        ]
    },
    "skill": {
        "label": "Skill Framework", "labelCn": "技能框架", "icon": "⚙️",
        "color": "#34d399", "app_category": "DeveloperApplication",
        "type": "developer framework for building AI applications",
        "use_cases": [
            {"icon": "🏗️", "title": "LLM Application Development", "desc": "Build production-grade apps powered by language models with structured pipelines, retry logic, and observability."},
            {"icon": "📚", "title": "RAG & Knowledge Systems",     "desc": "Create document Q&A and knowledge base systems that ground LLM responses in proprietary data."},
            {"icon": "🤖", "title": "Agent Orchestration",         "desc": "Compose multi-step AI workflows where models plan, use tools, and iterate autonomously toward goals."},
            {"icon": "🔌", "title": "Model Provider Abstraction",  "desc": "Write once, run with any LLM provider—switch between OpenAI, Anthropic, and local models without code changes."},
        ],
        "faq": [
            ("What languages does {name} support?",
             "{name} primarily targets Python, with many frameworks also providing JavaScript/TypeScript SDKs. Check the GitHub repository for the full list of supported languages and official client libraries."),
            ("Is {name} production-ready?",
             "Yes. {name} is used in production by thousands of engineering teams globally. The project has a stable API, comprehensive test suite, and an active maintainer team that releases regular security and bug-fix patches."),
            ("How do I install and get started with {name}?",
             "Install via pip: `pip install {name_slug}` (Python) or `npm install {name_slug}` (Node.js). The GitHub repository README contains a quickstart guide with working code examples. Most frameworks have active community support on Discord or GitHub Discussions."),
            ("Does {name} work with local LLMs like Ollama?",
             "Most modern AI frameworks support local LLM backends via Ollama's OpenAI-compatible API at http://localhost:11434/v1. Set the `base_url` parameter to your local endpoint to run entirely offline without any cloud API costs."),
        ]
    },
    "agent": {
        "label": "AI Agent", "labelCn": "AI 智能体", "icon": "🚀",
        "color": "#fbbf24", "app_category": "AIApplication",
        "type": "autonomous AI agent system",
        "use_cases": [
            {"icon": "🔍", "title": "Research Automation",        "desc": "Gather, analyze, and synthesize information from the web, databases, and documents autonomously."},
            {"icon": "💻", "title": "Code Generation & Debugging", "desc": "Implement features, fix bugs, write tests, and refactor codebases with minimal human intervention."},
            {"icon": "📊", "title": "Data Processing Pipelines",   "desc": "Build automated workflows that ingest, transform, validate, and analyze data at scale."},
            {"icon": "🌐", "title": "Multi-Step Task Execution",   "desc": "Complete complex goals requiring planning across many tools, APIs, and decision branches."},
        ],
        "faq": [
            ("What can {name} do autonomously?",
             "{name} can browse the web, read and write files, execute code in a sandbox, call external APIs, and chain these actions to complete complex multi-step goals—all without human confirmation at each step."),
            ("How much does running {name} cost?",
             "The software itself is MIT-licensed and free. It requires an LLM API (OpenAI, Anthropic, or local Ollama). A typical task costs $0.50–$5 in API usage with GPT-4o. Always set a token budget limit to prevent runaway costs on long tasks."),
            ("Is it safe to run {name} without supervision?",
             "For production-critical systems, always run with human-in-the-loop confirmation enabled. {name} includes confirmation prompts for destructive actions by default. Never grant access to credentials or production infrastructure without explicit scope limits."),
            ("How does {name} compare to prompt chaining?",
             "{name} goes beyond prompt chaining by adding dynamic planning, real tool execution, and self-correction loops. Unlike a fixed chain of prompts, it adapts its approach based on intermediate results—making it suitable for open-ended tasks where the exact steps aren't known in advance."),
        ]
    },
}

# ─── Category 页面 SEO 配置 ──────────────────────────────────────────────────
CATEGORY_SEO = {
    "ai-tools": {
        "slug": "ai-tools",
        "seo_title": "Best Open Source AI Tools 2026 – 100 Top AI Applications | AI Nav",
        "seo_desc": "Discover the 100 best open source AI tools in 2026, ranked by GitHub stars. Covers local LLMs, image generation, coding assistants, voice AI, and developer tools.",
        "h1": "Best Open Source AI Tools 2026",
        "intro": "A curated ranking of the 100 most popular open-source AI tools, sorted by GitHub stars. From local LLMs and image generators to coding assistants and voice models—find the right tool for your project.",
    },
    "skill": {
        "slug": "skill",
        "seo_title": "Best AI Skill Frameworks & LLM Libraries 2026 – Top 100 | AI Nav",
        "seo_desc": "Explore 100 top open-source AI skill frameworks and LLM libraries in 2026. Includes LangChain, Transformers, vLLM, LlamaIndex, and more, ranked by GitHub stars.",
        "h1": "Best AI Skill Frameworks & LLM Libraries 2026",
        "intro": "A curated ranking of 100 open-source developer frameworks and libraries for building production-ready LLM applications. Covers RAG pipelines, inference engines, fine-tuning toolkits, embeddings, and vector databases.",
    },
    "agent": {
        "slug": "agent",
        "seo_title": "Best AI Agent Frameworks 2026 – 100 Autonomous AI Systems | AI Nav",
        "seo_desc": "Browse 100 top open-source AI agent frameworks in 2026, ranked by GitHub stars. Covers AutoGPT, n8n, MetaGPT, browser automation, and multi-agent orchestration.",
        "h1": "Best Open Source AI Agent Frameworks 2026",
        "intro": "A curated ranking of 100 open-source autonomous AI agent frameworks, sorted by GitHub stars. From multi-agent orchestration and browser automation to code agents and LLM workflow systems.",
    },
}

# ─── 博客文章 → 工具关联映射 ──────────────────────────────────────────────────
BLOG_ARTICLES = [
    {
        "url": "/blog/ai-agent-frameworks-guide-2025.html",
        "title": "LangChain vs AutoGen vs CrewAI: Which Framework to Use in 2026?",
        "desc": "Side-by-side comparison of the top 5 agent frameworks with real code examples.",
        "tags": {"llm", "framework", "agent", "rag", "workflow"},
        "ids":  {"langchain", "autogen", "crewai", "llamaindex", "dify"},
    },
    {
        "url": "/blog/run-llm-locally-guide.html",
        "title": "How to Run LLMs Locally: Ollama vs llama.cpp vs LM Studio",
        "desc": "Step-by-step guide with hardware requirements and performance benchmarks.",
        "tags": {"local", "privacy"},
        "ids":  {"ollama", "llama-cpp", "lm-studio"},
    },
    {
        "url": "/blog/rag-pipeline-guide.html",
        "title": "Building a Production RAG Pipeline: The Complete Guide",
        "desc": "Architecture, chunking strategies, vector stores, reranking, and evaluation.",
        "tags": {"rag", "embeddings", "vector-db", "search"},
        "ids":  {"langchain", "llamaindex", "qdrant", "chroma", "weaviate", "milvus"},
    },
    {
        "url": "/blog/ai-coding-assistants-compared.html",
        "title": "Best AI Coding Assistants in 2026: Cursor vs Aider vs Copilot",
        "desc": "Honest comparison with score grids, decision matrix, and real-world trade-offs.",
        "tags": {"code", "productivity"},
        "ids":  {"cursor", "aider", "copilot", "continue-dev"},
    },
    {
        "url": "/blog/llm-inference-optimization.html",
        "title": "vLLM vs TGI vs llama.cpp: Which Inference Engine Is Fastest?",
        "desc": "Production benchmark data on throughput, latency, and quantization trade-offs.",
        "tags": {"inference", "deployment"},
        "ids":  {"vllm", "tgi", "llama-cpp", "text-generation-inference"},
    },
    {
        "url": "/blog/langchain-vs-llamaindex.html",
        "title": "LangChain vs LlamaIndex: Which RAG Framework to Choose in 2026?",
        "desc": "Head-to-head comparison of architecture, performance, and real-world use cases.",
        "tags": {"rag", "framework", "llm", "embeddings"},
        "ids":  {"langchain", "llamaindex"},
    },
    {
        "url": "/blog/vector-databases-compared.html",
        "title": "Vector Database Showdown: Chroma vs Qdrant vs Weaviate vs Milvus",
        "desc": "Performance benchmarks, feature comparison, and deployment considerations.",
        "tags": {"vector-db", "embeddings", "search", "rag"},
        "ids":  {"chroma", "qdrant", "weaviate", "milvus", "pgvector"},
    },
    {
        "url": "/blog/vllm-vs-ollama-production.html",
        "title": "vLLM vs Ollama vs LocalAI: Production Inference in 2026",
        "desc": "Real throughput numbers, GPU memory usage, and deployment trade-offs.",
        "tags": {"inference", "local", "deployment"},
        "ids":  {"vllm", "ollama", "localai"},
    },
    {
        "url": "/blog/comfyui-vs-a1111-vs-fooocus.html",
        "title": "ComfyUI vs Automatic1111 vs Fooocus: Which Image Generator Wins?",
        "desc": "Hands-on comparison of UI, workflow flexibility, and output quality.",
        "tags": {"image", "local"},
        "ids":  {"comfyui", "stable-diffusion", "fooocus"},
    },
    {
        "url": "/blog/autogen-vs-crewai-vs-langgraph.html",
        "title": "AutoGen vs CrewAI vs LangGraph: Multi-Agent Frameworks Compared",
        "desc": "Architecture differences, orchestration patterns, and when to use each.",
        "tags": {"agent", "framework", "llm", "workflow"},
        "ids":  {"autogen", "crewai", "langgraph"},
    },
    {
        "url": "/blog/open-source-llms-guide-2026.html",
        "title": "Best Open Source LLMs in 2026: Llama 3 vs Mistral vs Qwen vs Gemma",
        "desc": "Benchmark scores, hardware requirements, and scenario-based selection guide.",
        "tags": {"local", "llm", "inference"},
        "ids":  {"ollama", "llama-cpp", "lm-studio", "vllm"},
    },
    {
        "url": "/blog/ai-code-assistants-2026.html",
        "title": "Best AI Coding Assistants in 2026: Cursor vs Cline vs Copilot vs Aider",
        "desc": "Deep dive into 5 tools with pricing, model support, and a 7-scenario decision matrix.",
        "tags": {"code", "productivity"},
        "ids":  {"cursor", "aider", "cline", "continue-dev"},
    },
    {
        "url": "/blog/build-production-rag-pipeline.html",
        "title": "Build a Production RAG Pipeline in 2026: Architecture to Deployment",
        "desc": "Chunking strategies, embedding models, hybrid search, reranking, and evaluation.",
        "tags": {"rag", "embeddings", "vector-db", "framework"},
        "ids":  {"langchain", "llamaindex", "qdrant", "chroma", "weaviate"},
    },
]


# ─── SEO title / description templates ──────────────────────────────────────
TITLE_TEMPLATES = {
    "ai-tools": "{name} Review 2026 | {desc_short} – AI Nav",
    "skill":    "{name} Guide 2026 | {desc_short} – AI Nav",
    "agent":    "{name} Review 2026 | {desc_short} – AI Nav",
}
DESC_TEMPLATES = {
    "ai-tools": "{desc} Open-source, {stars} GitHub stars. Find alternatives, features, and use cases.",
    "skill":    "{desc} {stars} GitHub stars. Installation guide, use cases, and comparison with alternatives.",
    "agent":    "{desc} {stars} GitHub stars. Features, pricing, and how to get started.",
}


# ─── Helpers ─────────────────────────────────────────────────────────────────

# ─── Tag → 适用/不适用场景规则 ────────────────────────────────────────────────
# 每个 tag 对应 (fit_items, not_fit_items)，每项为字符串
TAG_FIT_RULES = {
    "local": (
        ["Privacy-sensitive projects (healthcare, legal, internal enterprise data) — code and data never leave your infrastructure",
         "Developers or students with no ongoing API budget",
         "Offline or air-gapped deployment environments with no internet access"],
        ["Workloads requiring large-scale distributed inference beyond local hardware limits",
         "Non-technical first-time users (local deployment has a real setup overhead)"]
    ),
    "privacy": (
        ["Teams handling PII / PHI / regulated data (GDPR, HIPAA, SOC 2 require data not to leave your control)",
         "Financial and legal projects that require data sovereignty"],
        ["Small projects prioritizing out-of-the-box convenience over strict data controls"]
    ),
    "fine-tuning": (
        ["Teams with domain-specific labeled data who need customized model behavior",
         "Enterprise applications that need the model to specialize in vertical terminology and output formats"],
        ["Environments without GPUs (fine-tuning requires 16GB+ VRAM minimum)",
         "Datasets smaller than a few thousand examples (too little data for meaningful fine-tuning gains)"]
    ),
    "training": (
        ["AI research teams doing from-scratch pre-training or large-scale continued training",
         "Academic projects experimenting with model architecture"],
        ["Production deployment scenarios that only need inference (inference frameworks are more efficient)",
         "Small and mid-size teams without multi-GPU clusters"]
    ),
    "rag": (
        ["Teams that need LLMs to answer questions grounded in private documents (knowledge base Q&A, enterprise search)",
         "Applications that need to reduce hallucination and cite sources"],
        ["Real-time data scenarios (RAG retrieval has latency, not suitable for sub-100ms response requirements)",
         "Very small corpora (<100 documents) — fitting everything in context is simpler"]
    ),
    "agent": (
        ["Teams automating multi-step tasks that require tool use and dynamic planning",
         "Engineering and operations teams looking to reduce repetitive manual workflows"],
        ["Compliance-sensitive scenarios requiring fully predictable, auditable step-by-step outputs",
         "Simple single-turn Q&A applications (Agent architecture adds unnecessary complexity)"]
    ),
    "autonomous": (
        ["Batch task scenarios where you set a goal and let AI execute end-to-end",
         "Research projects exploring the boundaries of AI autonomous capability"],
        ["Mission-critical production systems (autonomous execution has unpredictable failure modes — human approval gates are needed)",
         "Budget-sensitive projects (unsupervised execution can generate large API costs)"]
    ),
    "code": (
        ["Development teams looking to improve code generation, completion, and review throughput",
         "Individual developers who want AI-assisted coding integrated directly into their IDE"],
        ["Non-technical users (code tools require programming fundamentals)",
         "Codebases with strict audit requirements (AI-generated code must pass human review before merging)"]
    ),
    "image": (
        ["Content creators and designers who need concept images or reference art quickly",
         "E-commerce and marketing teams that need large volumes of image assets at lower cost than outsourcing"],
        ["Scenarios requiring photorealistic reproduction of real scenes (diffusion models have creative variance, not guaranteed accuracy)",
         "Copyright-sensitive commercial use (AI-generated image copyright is still legally contested)"]
    ),
    "vector-db": (
        ["Engineering teams building semantic search, recommendation systems, or RAG retrieval layers",
         "Applications doing similarity search across millions of vectors or more"],
        ["Small apps that only need simple keyword search (Elasticsearch or SQLite is simpler)",
         "Datasets under 100K records (a standard database with pgvector extension is sufficient)"]
    ),
    "embeddings": (
        ["NLP applications that need to convert text or images into vectors for downstream search or clustering",
         "Teams building semantic similarity matching or text classification systems"],
        ["Traditional information retrieval use cases that only need TF-IDF-style sparse search"]
    ),
    "inference": (
        ["Teams serving low-latency LLM APIs in production (p99 < 500ms)",
         "Inference services handling high-concurrency LLM requests with request batching"],
        ["Exploratory research or single-machine light inference (high configuration cost with low return)",
         "Environments without GPU servers (high-performance inference frameworks require CUDA or ROCm)"]
    ),
    "no-code": (
        ["Non-technical business users who need to build AI workflows without writing code",
         "Rapid prototyping phases where you want to test AI logic before committing to engineering"],
        ["Engineering teams requiring deep API customization or complex integration logic (no-code platforms have hard ceilings)"]
    ),
    "workflow": (
        ["Product and data teams who need to visually manage multi-step AI pipelines",
         "Organizations that want non-engineers to be able to maintain and modify AI workflows"],
        ["Simple single-step LLM calls (introducing a workflow engine is over-engineering)"]
    ),
    "search": (
        ["Applications that need to find content by semantic similarity rather than exact keywords (document retrieval, FAQ matching)",
         "Multi-language content retrieval (semantic search generalizes across languages better than keywords)"],
        ["Scenarios requiring exact string or regex matching (traditional full-text search is more precise)"]
    ),
    "multi-modal": (
        ["Applications processing text, image, and audio inputs together",
         "Enterprise apps requiring mixed text-image understanding (invoice processing, document parsing)"],
        ["Pure text-only scenarios (multimodal models have higher inference overhead)"]
    ),
    "chat": (
        ["Teams building customer service bots, conversational assistants, or internal knowledge Q&A",
         "Applications requiring multi-turn context dialogue management"],
        ["Batch processing scenarios that need single-turn stateless API calls"]
    ),
}

# 分类通用的适用/不适用（兜底）
CATEGORY_FIT_DEFAULTS = {
    "ai-tools": (
        ["Developers and end users who want to use AI capabilities quickly without building integrations from scratch",
         "Teams that need a ready-to-use UI interface"],
        ["Pure backend engineering scenarios requiring deep API customization (framework libraries are a better fit)"]
    ),
    "skill": (
        ["Engineers with Python experience building LLM capabilities at the application layer",
         "Teams that need portability across different LLM providers (OpenAI, Anthropic, local models)"],
        ["Non-technical users (libraries require programming experience)",
         "Users who just need existing products like ChatGPT"]
    ),
    "agent": (
        ["Engineering and operations teams automating repetitive multi-step workflows",
         "Researchers exploring the boundaries of AI agent capabilities"],
        ["Compliance-critical production scenarios where every step must be fully auditable",
         "Budget-constrained projects worried about API cost runaway (always set token limits in agents)"]
    ),
}


def get_who_should_use(tool):
    """基于工具 tags 和 category 生成适用/不适用场景（各 3-4 条，工具特有）。"""
    tags = tool.get("tags", [])
    category = tool.get("category", "ai-tools")
    fit_items, not_fit_items = [], []
    seen_fit, seen_not = set(), set()

    for tag in tags:
        if tag in TAG_FIT_RULES:
            fits, nots = TAG_FIT_RULES[tag]
            for item in fits:
                if item not in seen_fit and len(fit_items) < 4:
                    fit_items.append(item)
                    seen_fit.add(item)
            for item in nots:
                if item not in seen_not and len(not_fit_items) < 3:
                    not_fit_items.append(item)
                    seen_not.add(item)
        if len(fit_items) >= 4 and len(not_fit_items) >= 3:
            break

    # 用分类默认值补足
    default_fits, default_nots = CATEGORY_FIT_DEFAULTS.get(
        category, CATEGORY_FIT_DEFAULTS["skill"]
    )
    for item in default_fits:
        if item not in seen_fit and len(fit_items) < 3:
            fit_items.append(item)
    for item in default_nots:
        if item not in seen_not and len(not_fit_items) < 2:
            not_fit_items.append(item)

    return {"fit_for": fit_items, "not_fit_for": not_fit_items}


def get_blog_links(tool):
    """返回与工具相关的博客文章（最多 3 篇），按 id 精确匹配优先，其次 tag 匹配。"""
    tool_tags = set(tool.get("tags", []))
    tool_id = tool["id"]
    exact, fuzzy = [], []
    for article in BLOG_ARTICLES:
        entry = {"url": article["url"], "title": article["title"], "desc": article["desc"]}
        if tool_id in article["ids"]:
            exact.append(entry)
        elif bool(tool_tags & article["tags"]):
            fuzzy.append(entry)
    seen, result = set(), []
    for entry in exact + fuzzy:
        if entry["url"] not in seen:
            seen.add(entry["url"])
            result.append(entry)
        if len(result) >= 3:
            break
    return result


def get_features(tool):
    """从 tags 提取功能特性列表（最多 6 条，去重）。"""
    seen = set()
    feats = []
    for tag in tool.get("tags", []):
        if tag in TAG_FEATURES and tag not in seen:
            icon, title, desc = TAG_FEATURES[tag]
            feats.append({"icon": icon, "title": title, "desc": desc})
            seen.add(tag)
        if len(feats) >= 6:
            break
    return feats


def get_related(tool, all_tools, n=6):
    """同类别相关工具（同 tag 优先，stars 次之，排除自身），最多 n 个。"""
    same_tags = set(tool.get("tags", []))
    candidates = [
        t for t in all_tools
        if t["category"] == tool["category"] and t["id"] != tool["id"]
    ]
    candidates.sort(key=lambda t: (
        -len(set(t.get("tags", [])) & same_tags),
        -t.get("stars", 0)
    ))
    return candidates[:n]


def build_compare_index(compare_file):
    """从 compare_data.json 构建 tool_id -> compare页列表 的映射。"""
    if not compare_file.exists():
        return {}
    with open(compare_file, encoding="utf-8") as f:
        compares = json.load(f)
    index = {}
    for c in compares:
        a_id, b_id = c["tool_a_id"], c["tool_b_id"]
        a_name = c["title"].split(" vs ")[0].strip()
        b_name = c["title"].split(" vs ")[-1].strip()
        index.setdefault(a_id, []).append({
            "slug": c["slug"], "other_id": b_id, "other_name": b_name
        })
        index.setdefault(b_id, []).append({
            "slug": c["slug"], "other_id": a_id, "other_name": a_name
        })
    return index


def get_faqs(tool, cat_info, cat_count):
    """格式化 FAQ 文本，替换占位符。"""
    fmt = dict(
        name=tool["name"],
        name_slug=tool["id"],
        category_label=cat_info["label"],
        category_count=cat_count,
    )
    return [{"q": q.format(**fmt), "a": a.format(**fmt)} for q, a in cat_info["faq"]]


def build_seo(tool, cat_info):
    """生成 SEO title 和 meta description。"""
    desc = tool.get("descEn", "")
    # 截短描述用于 title
    desc_short = desc[:60].rstrip()
    if len(desc) > 60:
        # 找最后一个空格截断
        sp = desc_short.rfind(" ")
        desc_short = (desc_short[:sp] if sp > 30 else desc_short).rstrip(".,;:")

    title = TITLE_TEMPLATES[tool["category"]].format(
        name=tool["name"], desc_short=desc_short
    )
    seo_desc = DESC_TEMPLATES[tool["category"]].format(
        desc=desc, stars=tool.get("starsLabel", ""),
    )
    # 保证 meta description ≤ 160 字符
    if len(seo_desc) > 160:
        seo_desc = seo_desc[:157] + "…"
    return title, seo_desc


def _tool_priority(tool):
    """按 GitHub stars 分级设置 sitemap 优先级。"""
    stars = tool.get("stars", 0)
    if tool["id"] in MANUAL_PAGES:
        return "0.95"
    if stars >= 50000:
        return "0.9"
    if stars >= 20000:
        return "0.85"
    if stars >= 5000:
        return "0.8"
    return "0.7"


def generate_category_pages(env, all_tools):
    """生成三个分类聚合页：/category/ai-tools.html, /category/skill.html, /category/agent.html。"""
    CATEGORY_DIR.mkdir(exist_ok=True)
    template = env.get_template("category.j2")
    # 构建 tool_id → filename 映射
    tool_filenames = {t["id"]: MANUAL_PAGES.get(t["id"], t["id"]) for t in all_tools}
    generated = 0
    for cat_key, seo in CATEGORY_SEO.items():
        tools = sorted(
            [t for t in all_tools if t["category"] == cat_key],
            key=lambda t: t.get("stars", 0), reverse=True
        )
        total_stars = sum(t.get("stars", 0) for t in tools)
        if total_stars >= 1_000_000:
            total_stars_label = f"{total_stars // 1_000_000:.1f}M+"
        else:
            total_stars_label = f"{total_stars // 1000}K+"
        ctx = {
            "seo_title":        seo["seo_title"],
            "seo_desc":         seo["seo_desc"],
            "h1":               seo["h1"],
            "intro":            seo["intro"],
            "cat_slug":         seo["slug"],
            "cat":              CATEGORY_INFO[cat_key],
            "tools":            tools,
            "tool_filenames":   tool_filenames,
            "total_stars_label": total_stars_label,
            "base_url":         BASE_URL,
            "today":            TODAY,
        }
        out_path = CATEGORY_DIR / f"{seo['slug']}.html"
        html = template.render(**ctx)
        out_path.write_text(html, encoding="utf-8")
        generated += 1
    print(f"[category] 已生成 {generated} 个分类聚合页 → {CATEGORY_DIR.name}/")
    return generated


def generate_sitemap(tools_dir, all_tools):
    """生成完整 sitemap.xml，包含首页、静态页、所有工具页（按 stars 设置优先级）。"""
    urls = []

    # 首页
    urls.append(dict(
        loc=f"{BASE_URL}/",
        lastmod=TODAY, changefreq="weekly", priority="1.0",
        alternates=True
    ))
    # 静态页（cleanUrls:true → 无 .html 后缀）
    for page, slug, prio, freq in [
        ("about.html",          "about",          "0.7", "monthly"),
        ("contact.html",        "contact",        "0.5", "monthly"),
        ("privacy-policy.html", "privacy-policy", "0.3", "yearly"),
    ]:
        urls.append(dict(loc=f"{BASE_URL}/{slug}", lastmod=TODAY, changefreq=freq, priority=prio))

    # 分类聚合页（cleanUrls:true → 无 .html 后缀）
    for cat_key in ["ai-tools", "skill", "agent"]:
        slug = CATEGORY_SEO[cat_key]["slug"]
        cat_path = CATEGORY_DIR / f"{slug}.html"
        if cat_path.exists():
            urls.append(dict(loc=f"{BASE_URL}/category/{slug}", lastmod=TODAY, changefreq="weekly", priority="0.85"))

    # 特殊手写页（不在 data.json，需单独列出）
    EXTRA_PAGES = [
        ("cursor",      "0.95", "weekly"),
        ("claude-code", "0.95", "weekly"),
        ("chatgpt",     "0.95", "weekly"),
    ]
    for slug, prio, freq in EXTRA_PAGES:
        page_path = tools_dir / f"{slug}.html"
        if page_path.exists():
            urls.append(dict(loc=f"{BASE_URL}/tools/{slug}", lastmod=TODAY, changefreq=freq, priority=prio))

    # Blog 文章页
    blog_dir = BASE_DIR / "blog"
    if blog_dir.exists():
        for blog_file in sorted(blog_dir.glob("*.html")):
            if blog_file.name != "index.html":
                slug = blog_file.stem
                urls.append(dict(loc=f"{BASE_URL}/blog/{slug}", lastmod=TODAY, changefreq="monthly", priority="0.8"))
        # blog index
        blog_index = blog_dir / "index.html"
        if blog_index.exists():
            urls.insert(4, dict(loc=f"{BASE_URL}/blog", lastmod=TODAY, changefreq="weekly", priority="0.85"))

    # 工具页（cleanUrls:true → 无 .html 后缀，与 canonical 保持一致）
    sorted_tools = sorted(all_tools, key=lambda t: t.get("stars", 0), reverse=True)
    for t in sorted_tools:
        tid = t["id"]
        filename = MANUAL_PAGES.get(tid, tid)
        page_path = tools_dir / f"{filename}.html"
        if page_path.exists():
            prio = _tool_priority(t)
            freq = "weekly" if t.get("stars", 0) >= 20000 else "monthly"
            urls.append(dict(
                loc=f"{BASE_URL}/tools/{filename}",
                lastmod=TODAY, changefreq=freq, priority=prio
            ))

    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"')
    lines.append('        xmlns:xhtml="http://www.w3.org/1999/xhtml">')
    for u in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{u['loc']}</loc>")
        lines.append(f"    <lastmod>{u['lastmod']}</lastmod>")
        lines.append(f"    <changefreq>{u['changefreq']}</changefreq>")
        lines.append(f"    <priority>{u['priority']}</priority>")
        if u.get("alternates"):
            lines.append(f'    <xhtml:link rel="alternate" hreflang="en" href="{BASE_URL}/?lang=en"/>')
            lines.append(f'    <xhtml:link rel="alternate" hreflang="zh-CN" href="{BASE_URL}/?lang=zh"/>')
            lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE_URL}/"/>')
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines)


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="AI Nav 静态页面生成器")
    parser.add_argument("--ids",           help="逗号分隔的工具 ID，只生成这些", default="")
    parser.add_argument("--force",         action="store_true", help="强制覆盖已有页面（含手写页）")
    parser.add_argument("--force-auto",    action="store_true", help="强制覆盖自动生成页（跳过手写页）")
    parser.add_argument("--sitemap-only",  action="store_true", help="只更新 sitemap.xml")
    parser.add_argument("--dry-run",       action="store_true", help="打印计划但不写文件")
    parser.add_argument("--no-category",   action="store_true", help="跳过分类聚合页生成")
    args = parser.parse_args()

    # 加载数据
    with open(DATA_FILE, encoding="utf-8") as f:
        data = json.load(f)
    all_tools = data.get("tools", [])
    print(f"[generate] 读取 {len(all_tools)} 个工具")

    # 构建对比页索引
    compare_index = build_compare_index(COMPARE_FILE)

    # 初始化 Jinja2
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html"]),
    )
    # 注册 tojson filter（Jinja2 默认有，但确保安全序列化）
    template = env.get_template("tool_detail.j2")

    TOOLS_DIR.mkdir(exist_ok=True)

    # 确定要生成哪些工具
    if args.ids:
        target_ids = set(args.ids.split(","))
        tools_to_gen = [t for t in all_tools if t["id"] in target_ids]
    else:
        tools_to_gen = all_tools

    # 构建分类计数（用于 FAQ 占位符）
    cat_counts = {}
    for t in all_tools:
        cat_counts[t["category"]] = cat_counts.get(t["category"], 0) + 1

    # 生成页面
    generated = skipped_manual = skipped_exists = errors = 0

    if not args.sitemap_only:
        for tool in tools_to_gen:
            tid = tool["id"]

            # 手写页处理
            if tid in MANUAL_PAGES and not args.force:
                skipped_manual += 1
                continue

            # 输出路径（手写页用自定义文件名，否则用 id）
            filename = MANUAL_PAGES.get(tid, tid) if args.force else tid
            out_path = TOOLS_DIR / f"{filename}.html"

            # 已存在且不强制覆盖（--force-auto 对非手写页也强制覆盖）
            is_auto_force = args.force_auto and tid not in MANUAL_PAGES
            if out_path.exists() and not args.force and not is_auto_force:
                skipped_exists += 1
                continue

            if args.dry_run:
                print(f"  [dry-run] 将生成 tools/{filename}.html  ({tool['name']})")
                generated += 1
                continue

            try:
                cat_info = CATEGORY_INFO.get(tool["category"], CATEGORY_INFO["ai-tools"])
                seo_title, seo_desc = build_seo(tool, cat_info)
                ctx = {
                    "tool":            tool,
                    "cat":             cat_info,
                    "features":        get_features(tool),
                    "related":         get_related(tool, all_tools),
                    "faqs":            get_faqs(tool, cat_info, cat_counts.get(tool["category"], 0)),
                    "compare_pages":   compare_index.get(tool["id"], []),
                    "blog_links":      get_blog_links(tool),
                    "who_should_use":  get_who_should_use(tool),
                    "seo_title":       seo_title,
                    "seo_desc":        seo_desc,
                    "base_url":        BASE_URL,
                    "today":           TODAY,
                }
                html = template.render(**ctx)
                out_path.write_text(html, encoding="utf-8")
                generated += 1
            except Exception as e:
                print(f"  [ERROR] {tid}: {e}", file=sys.stderr)
                errors += 1

        print(f"[generate] 生成 {generated} 页 | 跳过手写 {skipped_manual} | 跳过已有 {skipped_exists} | 错误 {errors}")

    # 生成分类聚合页
    if not args.sitemap_only and not args.dry_run and not args.no_category:
        generate_category_pages(env, all_tools)

    # 更新 sitemap.xml
    if not args.dry_run:
        sitemap_xml = generate_sitemap(TOOLS_DIR, all_tools)
        SITEMAP_FILE.write_text(sitemap_xml, encoding="utf-8")
        # 统计 sitemap URL 数量
        url_count = sitemap_xml.count("<url>")
        print(f"[sitemap] 已更新，共 {url_count} 个 URL → {SITEMAP_FILE.name}")
    else:
        print("[sitemap] dry-run: 将更新 sitemap.xml")


if __name__ == "__main__":
    main()

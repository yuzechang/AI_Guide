#!/usr/bin/env python3
"""
为 data.json 中 GitHub Stars 前 81 名的工具注入 tool-level use_cases 和 install_guide。
通过 githubUrl 匹配，确保精确。

运行：python3 inject_tool_data.py
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data.json")

# ═══════════════════════════════════════════════════════════════
# 工具级 use_cases 和 install_guide 数据映射（key = githubUrl）
# 每条 {icon, title, desc} — 真实可执行场景
# ═══════════════════════════════════════════════════════════════

TOOL_DATA = {
    # ─── Agent 类 ──────────────────────────────────────────────
    "https://github.com/n8n-io/n8n": {
        "use_cases": [
            {"icon": "🔄", "title": "Automate CI/CD Notifications", "desc": "Connect GitHub, Slack, and Jira to auto-post build status, tag reviewers, and log deployment events to a shared channel—no code required."},
            {"icon": "📊", "title": "Data Pipeline Orchestration", "desc": "Pull data from PostgreSQL, transform it with Python snippets, and push to Google Sheets or BigQuery on a cron schedule."},
            {"icon": "🤖", "title": "AI-Enhanced Support Triage", "desc": "Route incoming support emails through an LLM node for classification, auto-reply to FAQs, and escalate complex tickets to the right team in Linear."},
        ],
        "install_guide": {"cmd": "npx n8n", "run": "n8n start", "note": "Or run via Docker: docker run -it --rm -p 5678:5678 n8nio/n8n"}
    },
    "https://github.com/Significant-Gravitas/AutoGPT": {
        "use_cases": [
            {"icon": "🔍", "title": "Autonomous Market Research", "desc": "Instruct AutoGPT to research a competitor's product line, scrape their website, summarize pricing tiers, and output a markdown report."},
            {"icon": "💻", "title": "Codebase Exploration & PR Drafting", "desc": "Point it at a GitHub repo to read the codebase, identify a bug, implement a fix, and open a pull request with a detailed description."},
            {"icon": "📝", "title": "Content Generation Pipeline", "desc": "Generate a week's worth of social media posts from a single topic brief, including image prompts, hashtag research, and a posting schedule."},
        ],
        "install_guide": {"cmd": "git clone https://github.com/Significant-Gravitas/AutoGPT && cd AutoGPT", "run": "docker compose up -d", "note": "Requires Docker and an OpenAI or Anthropic API key. Set keys in .env before starting."}
    },
    "https://github.com/langflow-ai/langflow": {
        "use_cases": [
            {"icon": "🧩", "title": "Visual RAG Pipeline Builder", "desc": "Drag-and-drop to connect a PDF loader, text splitter, embedding model, and vector store—then query your documents through a chat interface."},
            {"icon": "🔗", "title": "Multi-Model API Router", "desc": "Build a single endpoint that routes prompts to the cheapest available LLM (OpenAI → Anthropic → local Ollama) based on complexity scoring."},
            {"icon": "📈", "title": "Customer Feedback Analyzer", "desc": "Ingest NPS survey CSV, run sentiment analysis with an LLM node, categorize by product area, and output a summary dashboard to Notion."},
        ],
        "install_guide": {"cmd": "pip install langflow", "run": "langflow run", "note": "Requires Python 3.10+. Web UI opens at http://localhost:7860. For production, use langflow run --host 0.0.0.0 --port 8080."}
    },
    "https://github.com/langgenius/dify": {
        "use_cases": [
            {"icon": "💬", "title": "Customer Support Chatbot", "desc": "Upload your knowledge base docs, configure a multi-turn conversation flow with fallback to human agents, and embed the chat widget on your website."},
            {"icon": "📄", "title": "Document Q&A with Citations", "desc": "Connect Dify to your Notion workspace, enable RAG with source highlighting, and let your team ask questions against all internal documentation."},
            {"icon": "🔧", "title": "Internal Tool Builder", "desc": "Create a no-code text-to-SQL assistant that lets non-technical team members query the product database in natural language and export results to CSV."},
        ],
        "install_guide": {"cmd": "git clone https://github.com/langgenius/dify && cd dify/docker", "run": "docker compose up -d", "note": "Requires Docker & Docker Compose. Web UI at http://localhost:80. Production deployment needs PostgreSQL and Redis configured in .env."}
    },
    "https://github.com/nicepkg/gpt-runner": {
        "use_cases": [
            {"icon": "💻", "title": "Terminal-First AI Assistant", "desc": "Use natural language in your terminal to generate shell commands, explain errors, refactor code, and manage files without leaving the CLI."},
            {"icon": "📁", "title": "Project Context Awareness", "desc": "Index your entire project directory so the AI understands your codebase structure and gives file-aware suggestions when you ask questions."},
            {"icon": "⚡", "title": "Quick Script Generation", "desc": "Describe what you need in plain English—'extract all email addresses from log.txt and dedupe'—and get a working script in seconds."},
        ],
        "install_guide": {"cmd": "npm install -g @nicepkg/gpt-runner", "run": "gpt-runner", "note": "Requires Node.js 18+. First run will prompt for API key configuration. Supports OpenAI, Anthropic, and local Ollama backends."}
    },
    "https://github.com/browser-use/browser-use": {
        "use_cases": [
            {"icon": "🌐", "title": "Web Scraping Complex SPAs", "desc": "Navigate JavaScript-heavy single-page apps, wait for dynamic content to load, and extract structured data that traditional scrapers miss."},
            {"icon": "🧪", "title": "End-to-End Testing Automation", "desc": "Write natural language test scenarios like 'log in, add item to cart, verify total' and let the agent execute them across Chrome, Firefox, and Safari."},
            {"icon": "📋", "title": "Form Auto-Fill & Submission", "desc": "Automate multi-page form filling across government portals, supplier onboarding systems, and enterprise SaaS tools with field-level validation."},
        ],
        "install_guide": {"cmd": "pip install browser-use", "run": "playwright install", "note": "Requires Python 3.11+. Install Playwright browsers separately. For headless mode, set HEADLESS=true in environment."}
    },
    "https://github.com/All-Hands-AI/OpenHands": {
        "use_cases": [
            {"icon": "🐛", "title": "Automated Bug Fixing", "desc": "Point OpenHands at a GitHub issue with reproduction steps; it reads the codebase, implements the fix, writes tests, and opens a PR with a summary."},
            {"icon": "🏗️", "title": "Feature Scaffolding from Spec", "desc": "Feed a product spec markdown and watch OpenHands scaffold the feature across frontend, backend, and database layers with working integration tests."},
            {"icon": "📚", "title": "Dependency Upgrade Assistant", "desc": "Instruct it to upgrade all npm packages, run the test suite, fix breaking changes, and produce a changelog of what changed and why."},
        ],
        "install_guide": {"cmd": "docker pull ghcr.io/all-hands-ai/openhands:latest", "run": "docker run -it --rm -p 3000:3000 -v /var/run/docker.sock:/var/run/docker.sock ghcr.io/all-hands-ai/openhands", "note": "Requires Docker. The -v flag mounts the host Docker socket so OpenHands can create sandbox containers. Set LLM_API_KEY env var first."}
    },
    "https://github.com/geekan/MetaGPT": {
        "use_cases": [
            {"icon": "🏢", "title": "Multi-Agent Software Company Simulation", "desc": "Assign roles (PM, Architect, Engineer, QA) to agents that collaborate through structured SOPs to produce PRDs, design docs, and working code from a one-line idea."},
            {"icon": "📋", "title": "PRD-to-Code Pipeline", "desc": "Feed a product requirements document and let MetaGPT generate a complete project structure with API contracts, database schemas, and implementation stubs."},
            {"icon": "🧪", "title": "Competitive Analysis Report", "desc": "Have multiple agents research competitors, analyze their tech stacks and pricing, and collaboratively write a structured competitive analysis report."},
        ],
        "install_guide": {"cmd": "pip install metagpt", "run": "metagpt --help", "note": "Requires Python 3.9+. Set OPENAI_API_KEY in environment. For local models, configure the LLM config in ~/.metagpt/config.yaml."}
    },
    "https://github.com/cline/cline": {
        "use_cases": [
            {"icon": "🧩", "title": "VS Code Pair Programming", "desc": "Cline reads your entire project context, edits files with precision, runs terminal commands, and fixes errors autonomously—all from within VS Code."},
            {"icon": "🔍", "title": "Codebase Exploration & Onboarding", "desc": "Open an unfamiliar codebase and ask Cline to explain the architecture, trace request flows, and generate onboarding docs for new team members."},
            {"icon": "⚡", "title": "Rapid MVP Development", "desc": "Describe your app idea and watch Cline scaffold a full-stack project, install dependencies, configure the database, and deploy to Vercel or Railway."},
        ],
        "install_guide": {"cmd": "code --install-extension saoudrizwan.claude-dev", "run": "Cmd+Shift+P → Cline: Open in New Tab", "note": "VS Code extension. Requires an Anthropic API key. Configure in Cline settings (gear icon) before first use. Supports Claude Opus and Sonnet models."}
    },
    "https://github.com/microsoft/autogen": {
        "use_cases": [
            {"icon": "🤝", "title": "Multi-Agent Debate & Consensus", "desc": "Set up two agents to debate a design decision—one arguing for microservices, the other for monolith—and converge on a recommendation with trade-off analysis."},
            {"icon": "📊", "title": "Collaborative Data Analysis", "desc": "Have one agent write SQL queries, another visualize results, and a third write the executive summary—all passing structured outputs between each other."},
            {"icon": "🔧", "title": "Code Review with Auto-Fix", "desc": "One agent reviews a PR diff, flags issues, and hands off to a fixer agent that applies the corrections and pushes a new commit."},
        ],
        "install_guide": {"cmd": "pip install pyautogen", "run": "python -c \"import autogen; print(autogen.__version__)\"", "note": "Requires Python 3.8+. Set OPENAI_API_KEY. Use autogen-agentchat~=0.2 for the stable agent API."}
    },
    "https://github.com/gpt-engineer-org/gpt-engineer": {
        "use_cases": [
            {"icon": "🏗️", "title": "Spec-to-App Generation", "desc": "Write a natural language specification with clarifications, and GPT Engineer generates the complete codebase with proper file structure, tests, and a README."},
            {"icon": "🔄", "title": "Iterative Refinement Loop", "desc": "After initial generation, provide feedback like 'add pagination to the table' or 'switch to PostgreSQL' and GPT Engineer applies the changes across all affected files."},
            {"icon": "📦", "title": "Legacy Code Modernization", "desc": "Feed it an old codebase and ask for a modern rewrite—GPT Engineer analyzes the existing logic and regenerates it with current best practices and dependency versions."},
        ],
        "install_guide": {"cmd": "pip install gpt-engineer", "run": "gpt-engineer .", "note": "Requires Python 3.10+ and an OpenAI API key. Create a 'prompt' file in your project directory with your specification, then run gpt-engineer in the same directory."}
    },
    "https://github.com/joaomdmoura/crewAI": {
        "use_cases": [
            {"icon": "👥", "title": "Role-Based Research Teams", "desc": "Define a Researcher agent to gather data, an Analyst to interpret it, and a Writer to produce the final report—each with custom tools and sequential handoffs."},
            {"icon": "📰", "title": "Automated News Digest", "desc": "Orchestrate a daily pipeline: one agent scrapes headlines, another summarizes, a third categorizes by industry, and a fourth formats it as an email newsletter."},
            {"icon": "🔗", "title": "Multi-Source Due Diligence", "desc": "Assign agents to check SEC filings, Crunchbase data, Glassdoor reviews, and news sentiment—then synthesize into an investment memo with risk flags."},
        ],
        "install_guide": {"cmd": "pip install crewai", "run": "crewai create crew my_team", "note": "Requires Python 3.10+. Run 'crewai install' to add tool dependencies. Set OPENAI_API_KEY before running crews."}
    },
    "https://github.com/FlowiseAI/Flowise": {
        "use_cases": [
            {"icon": "🧩", "title": "Drag-and-Drop Chatbot Builder", "desc": "Visually compose a chatbot flow: document loader → text splitter → Pinecone vector store → OpenAI chat model → conversational retrieval chain—no code."},
            {"icon": "🔌", "title": "API Endpoint Generation", "desc": "Build a flow, click deploy, and get a production-ready API endpoint with embeddable chat widget or iframe for your website."},
            {"icon": "📊", "title": "Multi-Source RAG Dashboard", "desc": "Connect PDFs, websites, Notion pages, and CSVs to a single flow, then query across all sources with citation highlighting in the response."},
        ],
        "install_guide": {"cmd": "npm install -g flowise", "run": "npx flowise start", "note": "Requires Node.js 18+. Web UI at http://localhost:3000. For production, use Docker: docker run -p 3000:3000 flowiseai/flowise."}
    },
    "https://github.com/agno-agi/agno": {
        "use_cases": [
            {"icon": "🧠", "title": "Memory-Persistent AI Assistant", "desc": "Build an assistant that remembers user preferences, conversation history, and context across sessions—stored in PostgreSQL, Pinecone, or local SQLite."},
            {"icon": "🔧", "title": "Tool-Equipped Agent Development", "desc": "Give your agent access to web search, code execution, database queries, and custom API tools with a single decorator per function."},
            {"icon": "📈", "title": "Multi-Modal Data Pipeline", "desc": "Ingest text, images, audio, and video into a unified knowledge base that the agent can query and reason over with structured outputs."},
        ],
        "install_guide": {"cmd": "pip install agno", "run": "python -c \"from agno import Agent; print('OK')\"", "note": "Requires Python 3.8+. Set ANTHROPIC_API_KEY or OPENAI_API_KEY. For full features, also install agno[tools] and agno[memory] extras."}
    },
    "https://github.com/phidatahq/phidata": {
        "use_cases": [
            {"icon": "🧠", "title": "Memory-Persistent AI Assistant", "desc": "Build an assistant that remembers user preferences, conversation history, and context across sessions—stored in PostgreSQL, Pinecone, or local SQLite."},
            {"icon": "🔧", "title": "Tool-Equipped Agent Development", "desc": "Give your agent access to web search, code execution, database queries, and custom API tools with a single decorator per function."},
            {"icon": "📈", "title": "Multi-Modal Data Pipeline", "desc": "Ingest text, images, audio, and video into a unified knowledge base that the agent can query and reason over with structured outputs."},
        ],
        "install_guide": {"cmd": "pip install phidata", "run": "python -c \"from phi.agent import Agent; print('OK')\"", "note": "Requires Python 3.8+. Set OPENAI_API_KEY. Phidata has been rebranded to Agno; new projects should use 'pip install agno' instead."}
    },
    "https://github.com/reworkd/AgentGPT": {
        "use_cases": [
            {"icon": "🌐", "title": "Browser-Based Autonomous Agent", "desc": "Deploy an AI agent directly from your browser—give it a goal, a name, and watch it plan, execute, and iterate in real-time with a visual task tree."},
            {"icon": "📊", "title": "Competitive Intelligence Gathering", "desc": "Create an agent to monitor competitor pricing pages, product launches, and job postings—compile findings into a weekly digest with trend analysis."},
            {"icon": "🎯", "title": "Goal Decomposition & Execution", "desc": "Enter a high-level goal and let AgentGPT break it into subtasks, assign priorities, execute each step, and adapt when intermediate results change the plan."},
        ],
        "install_guide": {"cmd": "git clone https://github.com/reworkd/AgentGPT && cd AgentGPT", "run": "docker compose up -d", "note": "Requires Docker. Web UI at http://localhost:3000. Set OPENAI_API_KEY in the .env file before starting."}
    },
    "https://github.com/langchain-ai/langgraph": {
        "use_cases": [
            {"icon": "🔀", "title": "Stateful Multi-Step Agent Workflows", "desc": "Build agents with persistent state across steps—ideal for customer support flows where context must carry through authentication, lookup, and resolution stages."},
            {"icon": "🔄", "title": "Human-in-the-Loop Approval", "desc": "Add checkpoints where the agent pauses and waits for human approval before executing high-stakes actions like sending emails or modifying production data."},
            {"icon": "🧪", "title": "Parallel Agent Coordination", "desc": "Fan out a task to multiple specialized sub-agents working simultaneously, then aggregate their results through a supervisor node that makes the final decision."},
        ],
        "install_guide": {"cmd": "pip install langgraph", "run": "python -c \"from langgraph.graph import StateGraph; print('OK')\"", "note": "Requires Python 3.9+. Often used alongside langchain. For checkpoint persistence, install langgraph[checkpoint] for SQLite or Postgres support."}
    },
    "https://github.com/executeautomation/mcp-playwright": {
        "use_cases": [
            {"icon": "🌐", "title": "Browser Automation via MCP", "desc": "Give any MCP-compatible AI client the ability to navigate web pages, click elements, fill forms, and extract data—all through a standardized protocol."},
            {"icon": "📸", "title": "Visual Regression Testing", "desc": "Automate screenshot capture across multiple pages and viewports, compare against baselines, and flag visual differences for review."},
            {"icon": "🔐", "title": "Authenticated Session Testing", "desc": "Handle login flows, cookie persistence, and session management automatically—test features behind authentication gates without manual token management."},
        ],
        "install_guide": {"cmd": "npm install -g @executeautomation/playwright-mcp-server", "run": "npx @executeautomation/playwright-mcp-server", "note": "Requires Node.js 18+. Configure in your MCP client's config file (e.g., Claude Desktop or Continue). Runs headless by default."}
    },
    "https://github.com/microsoft/TaskMatrix": {
        "use_cases": [
            {"icon": "🎨", "title": "Multimodal Visual Agent", "desc": "Analyze images, detect objects, read text from screenshots, and perform visual grounding tasks—connecting vision models to real-world task execution."},
            {"icon": "🔗", "title": "API Chaining for Complex Goals", "desc": "Connect TaskMatrix to hundreds of foundation models and APIs; it automatically selects the right model for each subtask in a multi-step workflow."},
            {"icon": "🏗️", "title": "Research Prototype Development", "desc": "Quickly prototype multimodal AI systems by composing vision, language, and specialized models without writing integration code for each combination."},
        ],
        "install_guide": {"cmd": "git clone https://github.com/microsoft/TaskMatrix && cd TaskMatrix", "run": "pip install -e .", "note": "Requires Python 3.8+. This is a research prototype. Configuration for individual foundation model APIs is required in the config file."}
    },
    "https://github.com/Pythagora-io/gpt-pilot": {
        "use_cases": [
            {"icon": "🏗️", "title": "Full-Stack App Generation", "desc": "Describe your app in a conversation with GPT Pilot, which acts as a lead developer—asking clarifying questions, then generating the entire stack with tests."},
            {"icon": "🧪", "title": "TDD-First Code Generation", "desc": "GPT Pilot writes tests first, then implements code until all tests pass—following a disciplined TDD workflow that catches regressions early."},
            {"icon": "📋", "title": "Step-by-Step Development Tracking", "desc": "Every task is logged with description, implementation, and test status—giving you a full audit trail of what the AI built and why."},
        ],
        "install_guide": {"cmd": "pip install gpt-pilot", "run": "gpt-pilot", "note": "Requires Python 3.9+ and an OpenAI API key. The interactive CLI will guide you through project setup and specification."}
    },

    # ─── AI Tools 类 ───────────────────────────────────────────
    "https://github.com/ollama/ollama": {
        "use_cases": [
            {"icon": "🏠", "title": "Local LLM Inference Server", "desc": "Run Llama 4, Mistral, Gemma, DeepSeek, and 100+ models locally with a single command—no cloud, no API keys, full data privacy on your own hardware."},
            {"icon": "🔌", "title": "OpenAI-Compatible API Drop-In", "desc": "Replace `api.openai.com` with `localhost:11434/v1` in your app and switch to local models without changing a single line of client code."},
            {"icon": "🧪", "title": "Model Evaluation & A/B Testing", "desc": "Pull multiple models, run identical prompts against each, and compare response quality, latency, and token usage to pick the best one for your use case."},
        ],
        "install_guide": {"cmd": "curl -fsSL https://ollama.com/install.sh | sh", "run": "ollama run llama3.2", "note": "macOS: brew install ollama. Linux: one-line install script. Windows: download .msi from ollama.com. Requires 8GB+ RAM for 7B models, 16GB+ for 13B."}
    },
    "https://github.com/AUTOMATIC1111/stable-diffusion-webui": {
        "use_cases": [
            {"icon": "🎨", "title": "Text-to-Image Generation", "desc": "Generate high-resolution images from text prompts with fine-grained control over sampling steps, CFG scale, seed, and negative prompts for production-quality outputs."},
            {"icon": "🖼️", "title": "Image Inpainting & Outpainting", "desc": "Erase objects, fill missing regions, or extend canvases beyond their original borders with context-aware generation that blends seamlessly."},
            {"icon": "🧩", "title": "Extension Ecosystem Workflow", "desc": "Install ControlNet for pose-guided generation, AnimateDiff for video, and Deforum for prompt-travel videos—all through a unified web interface."},
        ],
        "install_guide": {"cmd": "git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui && cd stable-diffusion-webui", "run": "./webui.sh  # Linux/Mac\n./webui.bat # Windows", "note": "Requires NVIDIA GPU with 6GB+ VRAM (or use --use-cpu for CPU-only). Python 3.10 recommended. First launch downloads several GB of model files."}
    },
    "https://github.com/open-webui/open-webui": {
        "use_cases": [
            {"icon": "💬", "title": "Self-Hosted ChatGPT Interface", "desc": "Deploy a ChatGPT-like UI connected to Ollama or any OpenAI-compatible API—your team gets a familiar chat experience with zero data leaving your network."},
            {"icon": "📚", "title": "Enterprise RAG Knowledge Base", "desc": "Upload PDFs, docs, and web pages to create a searchable knowledge base that answers questions with inline citations from your proprietary documents."},
            {"icon": "👥", "title": "Multi-User Team Workspace", "desc": "Create user accounts with role-based access, share model configurations, and manage usage quotas—all from the admin dashboard."},
        ],
        "install_guide": {"cmd": "docker run -d -p 3000:8080 -v open-webui:/app/backend/data -e OLLAMA_BASE_URL=http://host.docker.internal:11434 --name open-webui ghcr.io/open-webui/open-webui:main", "run": None, "note": "Requires Docker. Connect to an existing Ollama instance or configure OPENAI_API_KEY. Web UI at http://localhost:3000. For pip install: pip install open-webui && open-webui serve."}
    },
    "https://github.com/comfyanonymous/ComfyUI": {
        "use_cases": [
            {"icon": "🔗", "title": "Node-Based Image Generation Pipeline", "desc": "Build custom image generation workflows by connecting nodes for model loading, prompt encoding, sampling, VAE decoding, and upscaling—full control over every step."},
            {"icon": "🔄", "title": "Reproducible Workflow Sharing", "desc": "Export your entire node graph as a JSON file (or PNG with embedded workflow), share it with the community, and reproduce results pixel-perfect on any machine."},
            {"icon": "⚡", "title": "API-Driven Batch Processing", "desc": "Trigger generation workflows programmatically via the REST API, enabling automated batch processing, A/B prompt testing, and integration into CI/CD pipelines."},
        ],
        "install_guide": {"cmd": "git clone https://github.com/comfyanonymous/ComfyUI && cd ComfyUI", "run": "python main.py --listen 0.0.0.0", "note": "Requires NVIDIA GPU with 6GB+ VRAM. Python 3.10+. Place model checkpoints in models/checkpoints/ before starting. Web UI at http://localhost:8188."}
    },
    "https://github.com/ggerganov/llama.cpp": {
        "use_cases": [
            {"icon": "⚡", "title": "CPU-First LLM Inference", "desc": "Run quantized Llama, Mistral, and DeepSeek models on CPU with 4-bit to 8-bit quantization—achieve 20-50 tokens/sec on Apple Silicon without a discrete GPU."},
            {"icon": "📱", "title": "Edge & Mobile Deployment", "desc": "Deploy LLMs on Raspberry Pi, Android phones, and IoT devices—llama.cpp's C++ codebase compiles anywhere and runs models as small as 1-2GB."},
            {"icon": "🔧", "title": "Custom Model Quantization", "desc": "Convert any GGUF model to Q4_K_M, Q5_K_M, or Q8_0 quantization levels to find the optimal size-vs-quality tradeoff for your hardware constraints."},
        ],
        "install_guide": {"cmd": "git clone https://github.com/ggerganov/llama.cpp && cd llama.cpp && make -j", "run": "./llama-cli -m model.gguf -p \"Hello, world!\"", "note": "macOS: make LLAMA_METAL=1 for Apple Silicon GPU. Linux: make LLAMA_CUDA=1 for NVIDIA. Download GGUF models from Hugging Face (search 'TheBloke' or 'bartowski')."}
    },
    "https://github.com/openai/whisper": {
        "use_cases": [
            {"icon": "🎙️", "title": "Multilingual Audio Transcription", "desc": "Transcribe podcasts, meetings, and interviews in 99 languages with near-human accuracy—output to SRT, VTT, TXT, or JSON with word-level timestamps."},
            {"icon": "📝", "title": "Meeting Note Automation", "desc": "Pipe Zoom recordings through Whisper for transcription, then feed the transcript to an LLM for summary, action items, and key decision extraction."},
            {"icon": "🌍", "title": "Content Localization Pipeline", "desc": "Transcribe video content, translate the transcript via an LLM, and generate dubbed audio with Coqui TTS—all automated for multi-language content distribution."},
        ],
        "install_guide": {"cmd": "pip install openai-whisper", "run": "whisper audio.mp3 --model medium --language en", "note": "Requires Python 3.8+ and ffmpeg (brew install ffmpeg / apt install ffmpeg). Model sizes: tiny (1GB VRAM), base, small, medium (5GB), large-v3 (10GB)."}
    },
    "https://github.com/ChatGPTNextWeb/ChatGPT-Next-Web": {
        "use_cases": [
            {"icon": "🔑", "title": "Bring-Your-Own-Key Chat UI", "desc": "Deploy a polished ChatGPT interface in one click on Vercel—users bring their own API keys, your app stays free with no backend costs."},
            {"icon": "🎭", "title": "Multi-Model Chat with Mask Personas", "desc": "Create character masks that prepend system prompts—switch between 'Code Reviewer', 'Chinese Translator', and 'Excel Expert' personas mid-conversation."},
            {"icon": "📱", "title": "PWA Mobile AI Assistant", "desc": "Install as a Progressive Web App on iOS/Android for a native-like experience with offline caching, push notifications, and home screen icon."},
        ],
        "install_guide": {"cmd": "git clone https://github.com/ChatGPTNextWeb/ChatGPT-Next-Web && cd ChatGPT-Next-Web", "run": "npm install && npm run dev", "note": "Requires Node.js 18+. Or deploy to Vercel in one click (no server needed). Users configure their own API keys in Settings. Supports OpenAI, Azure, Google AI, and Anthropic."}
    },
    "https://github.com/lobehub/lobe-chat": {
        "use_cases": [
            {"icon": "🧩", "title": "Plugin-Extended AI Workspace", "desc": "Install plugins for web search, image generation, code execution, and data analysis—LobeChat orchestrates tool calls and displays rich results inline."},
            {"icon": "🎨", "title": "Custom Agent Marketplace", "desc": "Browse a marketplace of community-built AI assistants for specific tasks—from legal document review to D&D dungeon mastering—or publish your own."},
            {"icon": "🗂️", "title": "Conversation Organization & Search", "desc": "Pin important chats, tag conversations by topic, and full-text search across your entire chat history to find that one prompt you used three months ago."},
        ],
        "install_guide": {"cmd": "docker run -d -p 3210:3210 -e OPENAI_API_KEY=sk-xxx lobehub/lobe-chat", "run": None, "note": "Requires Docker. Web UI at http://localhost:3210. Supports 20+ LLM providers. For self-hosted database, configure PostgreSQL in environment variables."}
    },
    "https://github.com/nomic-ai/gpt4all": {
        "use_cases": [
            {"icon": "💻", "title": "Desktop Local LLM Chat", "desc": "Download and run LLMs locally through a desktop app—zero configuration, no terminal needed, models download with one click from within the app."},
            {"icon": "📚", "title": "Local Document Q&A", "desc": "Point GPT4All at a folder of PDFs, markdown files, and text documents—it indexes them locally and answers questions grounded in your private data."},
            {"icon": "🔌", "title": "Python SDK for Offline Apps", "desc": "Embed GPT4All in your Python application with 5 lines of code—ship AI features that work completely offline with no API calls or internet dependency."},
        ],
        "install_guide": {"cmd": "pip install gpt4all", "run": "gpt4all", "note": "Desktop app: download from gpt4all.io (Mac/Windows/Linux). Python SDK: pip install gpt4all. Models download on first use. No GPU required—runs on CPU."}
    },
    "https://github.com/Stability-AI/stablediffusion": {
        "use_cases": [
            {"icon": "🎨", "title": "Programmatic Image Generation", "desc": "Generate images from text prompts via Python scripts—integrate Stable Diffusion into data augmentation pipelines, content tools, and creative applications."},
            {"icon": "🧪", "title": "Custom Model Fine-Tuning", "desc": "Fine-tune on your brand's visual identity, product catalog, or artistic style to generate on-brand images that match your specific domain."},
            {"icon": "🔧", "title": "Image-to-Image Transformation", "desc": "Take a sketch, photo, or low-res image and transform it into a high-quality rendering—control the strength to balance similarity vs. creativity."},
        ],
        "install_guide": {"cmd": "pip install diffusers transformers accelerate", "run": "python -c \"from diffusers import StableDiffusionPipeline; pipe = StableDiffusionPipeline.from_pretrained('runwayml/stable-diffusion-v1-5'); pipe.to('cuda')\"", "note": "Requires NVIDIA GPU 8GB+ VRAM. For CPU-only: use StableDiffusionPipeline.from_pretrained(..., torch_dtype=torch.float32).to('cpu'). Diffusers library is the recommended SDK."}
    },
    "https://github.com/abi/screenshot-to-code": {
        "use_cases": [
            {"icon": "📸", "title": "Screenshot-to-HTML Conversion", "desc": "Upload a screenshot of any website mockup and get clean, responsive HTML/Tailwind code that matches the design pixel-by-pixel in under a minute."},
            {"icon": "🔄", "title": "Design-to-React Component", "desc": "Convert Figma exports and design screenshots into production-ready React or Vue components with proper CSS, state handling, and responsive breakpoints."},
            {"icon": "🎯", "title": "Legacy Site Redesign", "desc": "Screenshot your old website page by page, feed each to screenshot-to-code, and get modern HTML/CSS equivalents as a starting point for your redesign."},
        ],
        "install_guide": {"cmd": "git clone https://github.com/abi/screenshot-to-code && cd screenshot-to-code", "run": "docker compose up -d", "note": "Requires Docker and an OpenAI API key (GPT-4V). Web UI at http://localhost:5173. For local-only mode without API costs, configure Claude or Ollama as backend."}
    },
    "https://github.com/hiyouga/LLaMA-Factory": {
        "use_cases": [
            {"icon": "🎯", "title": "One-Click LLM Fine-Tuning", "desc": "Fine-tune Llama, Qwen, DeepSeek, and 100+ models through a web UI—upload your JSONL dataset, pick LoRA or full fine-tune, and click start."},
            {"icon": "📊", "title": "RLHF & DPO Alignment Training", "desc": "Train models on human preference data with DPO (Direct Preference Optimization) or full RLHF pipelines to align outputs with user expectations and safety guidelines."},
            {"icon": "📈", "title": "Benchmark Evaluation Suite", "desc": "Evaluate fine-tuned checkpoints against MMLU, C-Eval, HumanEval, and custom benchmarks directly from the UI to track training progress quantitatively."},
        ],
        "install_guide": {"cmd": "git clone https://github.com/hiyouga/LLaMA-Factory && cd LLaMA-Factory", "run": "pip install -e . && llamafactory-cli webui", "note": "Requires NVIDIA GPU 24GB+ VRAM for 7B models. Use QLoRA (4-bit) to reduce VRAM to ~10GB. Web UI at http://localhost:7860."}
    },
    "https://github.com/opendatalab/MinerU": {
        "use_cases": [
            {"icon": "📄", "title": "PDF-to-Markdown Conversion", "desc": "Convert complex PDFs with tables, formulas, images, and multi-column layouts into clean, structured Markdown that preserves document hierarchy."},
            {"icon": "🔬", "title": "Scientific Paper Parsing", "desc": "Extract text, LaTeX formulas, figures, and tables from academic papers—output structured JSON ready for RAG ingestion or knowledge graph construction."},
            {"icon": "📚", "title": "Enterprise Document Digitization", "desc": "Batch-process scanned contracts, invoices, and reports into searchable, structured formats for downstream AI processing and compliance archiving."},
        ],
        "install_guide": {"cmd": "pip install magic-pdf", "run": "magic-pdf --help", "note": "Requires Python 3.8+. For GPU acceleration: pip install magic-pdf[gpu]. CPU mode works but is slower for large batches. Outputs Markdown with embedded LaTeX."}
    },
    "https://github.com/open-interpreter/open-interpreter": {
        "use_cases": [
            {"icon": "💻", "title": "Natural Language System Control", "desc": "Type 'clean up my Downloads folder, keep files from the last 30 days, move old ones to Archive' and Open Interpreter writes and executes the Python/bash to do it."},
            {"icon": "📊", "title": "Interactive Data Analysis", "desc": "Ask 'plot revenue by region from this CSV, highlight YoY growth'—Open Interpreter reads the file, writes pandas/matplotlib code, and shows the chart inline."},
            {"icon": "🔧", "title": "System Administration Automation", "desc": "Describe admin tasks in plain English: 'find all processes using >1GB RAM, kill the ones not owned by root'—Open Interpreter runs the commands with your approval."},
        ],
        "install_guide": {"cmd": "pip install open-interpreter", "run": "interpreter", "note": "Requires Python 3.10+ and an OpenAI API key (or local Ollama). Runs code on your machine with approval prompts. Use interpreter --local for fully offline mode."}
    },
    "https://github.com/unslothai/unsloth": {
        "use_cases": [
            {"icon": "⚡", "title": "2-5x Faster LLM Fine-Tuning", "desc": "Fine-tune Llama, Mistral, and Gemma models 2x faster with 50% less VRAM using Unsloth's optimized kernels—drop-in replacement for Hugging Face Trainer."},
            {"icon": "📦", "title": "GGUF Quantized Model Export", "desc": "Fine-tune a model in the morning, export to GGUF in the afternoon, and deploy with llama.cpp or Ollama the same day—end-to-end workflow in a Colab notebook."},
            {"icon": "🧪", "title": "Free Colab Fine-Tuning", "desc": "Fine-tune 7B models on Google Colab's free T4 GPU (16GB)—Unsloth's memory optimization makes what was previously impossible fit comfortably on free tier."},
        ],
        "install_guide": {"cmd": "pip install unsloth", "run": "python -c \"from unsloth import FastLanguageModel; print('OK')\"", "note": "Requires NVIDIA GPU. Works with Hugging Face TRL and transformers. Check unsloth.ai for free Colab notebooks with pre-configured environments."}
    },
    "https://github.com/DS4SD/docling": {
        "use_cases": [
            {"icon": "📄", "title": "PDF-to-Structured-JSON Conversion", "desc": "Convert complex PDFs into hierarchical DoclingDocument JSON—preserving reading order, tables as DataFrames, figures with captions, and cross-references."},
            {"icon": "🔗", "title": "RAG Document Preprocessing", "desc": "Use Docling as the first stage of your RAG pipeline—chunk documents intelligently at section boundaries, extract tables separately, and preserve metadata."},
            {"icon": "📊", "title": "Financial Report Data Extraction", "desc": "Parse annual reports and 10-K filings, extract financial tables as structured DataFrames, and feed directly into analysis scripts without manual data entry."},
        ],
        "install_guide": {"cmd": "pip install docling", "run": "docling mydoc.pdf", "note": "Requires Python 3.10+. For OCR support on scanned PDFs: pip install docling[ocr]. Outputs JSON, Markdown, and DocTags formats."}
    },
    "https://github.com/Mintplex-Labs/anything-llm": {
        "use_cases": [
            {"icon": "📚", "title": "Multi-Source Knowledge Base Chat", "desc": "Connect PDFs, YouTube transcripts, Confluence pages, and GitHub repos into a unified workspace—query across all sources with citations in a single chat."},
            {"icon": "🔌", "title": "LLM Provider Agnostic Frontend", "desc": "Switch between OpenAI, Anthropic, Google Gemini, Azure, Ollama, LM Studio, and local models from one interface—compare outputs without changing tools."},
            {"icon": "👥", "title": "Team Knowledge Management", "desc": "Create shared workspaces with custom AI agents per workspace, embeddable chat widgets for internal tools, and granular permission controls for enterprise deployment."},
        ],
        "install_guide": {"cmd": "docker run -d -p 3001:3001 --name anythingllm -v anythingllm_data:/app/server/storage mintplexlabs/anythingllm", "run": None, "note": "Requires Docker. Web UI at http://localhost:3001. Desktop app also available (Mac/Windows/Linux). Supports 30+ LLM providers, 20+ vector databases, and 10+ embedding models."}
    },
    "https://github.com/mem0ai/mem0": {
        "use_cases": [
            {"icon": "🧠", "title": "Long-Term AI Agent Memory", "desc": "Add persistent memory to your LLM app in 5 lines of code—Mem0 remembers user preferences, past interactions, and important facts across sessions automatically."},
            {"icon": "🔍", "title": "Personalized User Experiences", "desc": "Build apps that adapt to each user over time—remember their name, preferred language, past queries, and behavioral patterns without managing your own memory infrastructure."},
            {"icon": "🏥", "title": "Healthcare Context Retention", "desc": "Maintain HIPAA-compliant patient interaction memory—track symptoms, medications, and care plans across sessions while keeping data encrypted and isolated per patient."},
        ],
        "install_guide": {"cmd": "pip install mem0ai", "run": "python -c \"from mem0 import Memory; m = Memory(); print('OK')\"", "note": "Requires Python 3.9+. Default uses local SQLite. For production: configure PostgreSQL or Qdrant in mem0 config. OpenAI API key required for embedding generation."}
    },
    "https://github.com/RVC-Boss/GPT-SoVITS": {
        "use_cases": [
            {"icon": "🎤", "title": "One-Shot Voice Cloning", "desc": "Clone any voice from a single 5-second audio sample—generate natural-sounding speech in that voice for any text input with emotional expression control."},
            {"icon": "🌍", "title": "Cross-Lingual Voice Synthesis", "desc": "Make a voice clone speak Chinese, English, Japanese, and Korean—the model preserves the original voice characteristics while adapting to each language's phonetics."},
            {"icon": "🎮", "title": "Game Character Voice Generation", "desc": "Create unique voice sets for game NPCs, visual novel characters, and virtual avatars with consistent voice identity across thousands of dialogue lines."},
        ],
        "install_guide": {"cmd": "git clone https://github.com/RVC-Boss/GPT-SoVITS && cd GPT-SoVITS", "run": "python webui.py", "note": "Requires NVIDIA GPU 6GB+ VRAM. Python 3.9+. Download pretrained models from Hugging Face before first use. Web UI at http://localhost:9874. 5-second voice sample is sufficient for decent cloning quality."}
    },
    "https://github.com/zylon-ai/private-gpt": {
        "use_cases": [
            {"icon": "🔒", "title": "Fully Offline Document Q&A", "desc": "Ask questions about your documents with zero data leaving your machine—PrivateGPT runs embedding, retrieval, and generation entirely on local hardware."},
            {"icon": "🏢", "title": "Enterprise Compliance Document Search", "desc": "Index internal policies, contracts, and compliance docs—employees query them conversationally without risking sensitive data exposure to cloud APIs."},
            {"icon": "📁", "title": "Personal Knowledge Vault", "desc": "Build your own searchable archive of research papers, notes, and bookmarks—query it with natural language and get grounded answers with source attribution."},
        ],
        "install_guide": {"cmd": "git clone https://github.com/zylon-ai/private-gpt && cd private-gpt", "run": "poetry install && poetry run python -m private_gpt", "note": "Requires Python 3.11+ and Poetry. Works best with local Ollama for LLM and embedding models. GPU optional but recommended. Web UI at http://localhost:8001. API at http://localhost:8080."}
    },
    "https://github.com/nicepkg/gpt-runner": {
        "use_cases": [
            {"icon": "💻", "title": "Terminal-First AI Assistant", "desc": "Use natural language in your terminal to generate shell commands, explain errors, refactor code, and manage files without leaving the CLI."},
            {"icon": "📁", "title": "Project Context Awareness", "desc": "Index your entire project directory so the AI understands your codebase structure and gives file-aware suggestions when you ask questions."},
            {"icon": "⚡", "title": "Quick Script Generation", "desc": "Describe what you need in plain English—'extract all email addresses from log.txt and dedupe'—and get a working script in seconds."},
        ],
        "install_guide": {"cmd": "npm install -g @nicepkg/gpt-runner", "run": "gpt-runner", "note": "Requires Node.js 18+. First run will prompt for API key configuration. Supports OpenAI, Anthropic, and local Ollama backends."}
    },

    # Note: gpt-runner URL is a duplicate in the data; skipping further duplicates

    # ─── Skill Frameworks 类 ───────────────────────────────────
    "https://github.com/huggingface/transformers": {
        "use_cases": [
            {"icon": "🤖", "title": "Pre-Trained Model Inference", "desc": "Load any of 200K+ Hugging Face models with 3 lines of code—text generation, classification, NER, translation, and more—with a unified pipeline API."},
            {"icon": "🎯", "title": "Custom Model Fine-Tuning", "desc": "Fine-tune BERT, T5, Llama, or any transformer model on your domain data with the Trainer API—handles distributed training, mixed precision, and checkpointing automatically."},
            {"icon": "🚀", "title": "Production Model Serving", "desc": "Export fine-tuned models to ONNX or TorchScript, optimize with quantization, and deploy via Text Generation Inference (TGI) for low-latency production serving."},
        ],
        "install_guide": {"cmd": "pip install transformers", "run": "python -c \"from transformers import pipeline; print(pipeline('sentiment-analysis')('I love this!'))\"", "note": "Requires Python 3.8+. For GPU: pip install transformers[torch]. Models auto-download from Hugging Face Hub on first use. Hugging Face account optional (only needed for private models)."}
    },
    "https://github.com/microsoft/markitdown": {
        "use_cases": [
            {"icon": "📄", "title": "Universal File-to-Markdown Conversion", "desc": "Convert PDF, DOCX, PPTX, XLSX, images (OCR), HTML, CSV, JSON, XML, ZIP, and audio files to clean Markdown with a single function call."},
            {"icon": "🤖", "title": "LLM Document Preprocessing", "desc": "Prepare diverse document formats for LLM ingestion—convert everything to Markdown first so your RAG pipeline only needs to handle one format downstream."},
            {"icon": "🔧", "title": "Batch Document Pipeline", "desc": "Walk a directory tree of mixed-format files, convert everything to Markdown, and output a structured folder ready for chunking and embedding."},
        ],
        "install_guide": {"cmd": "pip install markitdown", "run": "python -c \"from markitdown import MarkItDown; md = MarkItDown(); print(md.convert('file.pdf').text_content[:200])\"", "note": "Requires Python 3.10+. For OCR support: pip install markitdown[all]. Supports 15+ file formats. Zero configuration needed for basic use."}
    },
    "https://github.com/hwchase17/langchain": {
        "use_cases": [
            {"icon": "🔗", "title": "LLM Application Framework", "desc": "Build production-ready LLM apps with chains, agents, and retrieval—LangChain provides the standard abstractions used by thousands of companies for prompt templating, tool calling, and memory."},
            {"icon": "📚", "title": "RAG System Development", "desc": "Assemble document loaders, text splitters, embedding models, vector stores, and retrievers into a complete RAG system with streaming and source citation."},
            {"icon": "🔧", "title": "Multi-Provider Agent Building", "desc": "Create agents that use tools, call APIs, and reason across steps—switch between OpenAI, Anthropic, and local models by changing one parameter."},
        ],
        "install_guide": {"cmd": "pip install langchain", "run": "python -c \"from langchain.llms import OpenAI; print('OK')\"", "note": "Requires Python 3.9+. For full features: pip install langchain[all]. Often used with langchain-community for 700+ integrations. Consider LangChain Expression Language (LCEL) for composable chains."}
    },
    "https://github.com/vllm-project/vllm": {
        "use_cases": [
            {"icon": "⚡", "title": "High-Throughput LLM Serving", "desc": "Serve LLMs at 10-20x the throughput of Hugging Face transformers with PagedAttention—handle 1000+ concurrent users with sub-100ms time-to-first-token."},
            {"icon": "🔌", "title": "OpenAI-Compatible API Server", "desc": "Deploy a drop-in replacement for the OpenAI API—your existing apps work unchanged, but inference runs on your own infrastructure with zero per-token cost."},
            {"icon": "📊", "title": "Batch Inference at Scale", "desc": "Process millions of documents through LLMs with continuous batching—vLLM packs requests dynamically to maximize GPU utilization at any scale."},
        ],
        "install_guide": {"cmd": "pip install vllm", "run": "vllm serve meta-llama/Llama-3.2-1B-Instruct", "note": "Requires NVIDIA GPU with CUDA 12.1+. Linux only (no macOS/Windows). For production, use the official Docker image: docker run --gpus all vllm/vllm-openai. API at http://localhost:8000/v1."}
    },
    "https://github.com/meta-llama/llama-stack": {
        "use_cases": [
            {"icon": "🏗️", "title": "Llama Ecosystem Toolchain", "desc": "Standardized APIs for inference, safety, evaluation, and agent tool calling across the entire Llama model family—build once, run on any Llama-compatible provider."},
            {"icon": "🛡️", "title": "Safety & Guardrails Integration", "desc": "Plug Llama Guard, Prompt Guard, and Code Shield into your application with standard APIs—consistent safety enforcement regardless of deployment target."},
            {"icon": "📊", "title": "Multi-Provider Benchmarking", "desc": "Run standardized evaluations across Together AI, Fireworks, Groq, and local vLLM—compare latency, throughput, and quality to pick the optimal provider for each use case."},
        ],
        "install_guide": {"cmd": "pip install llama-stack", "run": "llama stack build", "note": "Requires Python 3.10+. Choose a distribution template (local-ollama, remote-together, etc.) during build. Configuration stored in ~/.llama/."}
    },
    "https://github.com/deepseek-ai/DeepSeek-V3": {"use_cases": [], "install_guide": {}},  # 跳过，不是可安装的工具
    "https://github.com/THUDM/ChatGLM-6B": {"use_cases": [], "install_guide": {}},  # 跳过，是模型而非工具

    "https://github.com/berriai/litellm": {
        "use_cases": [
            {"icon": "🔄", "title": "Universal LLM API Proxy", "desc": "Call 100+ LLM providers through a single OpenAI-format API—switch between OpenAI, Anthropic, Vertex AI, Bedrock, and Ollama without changing client code."},
            {"icon": "📊", "title": "Cost Tracking & Rate Limiting", "desc": "Track spend per user, model, and team in real-time. Set budget caps and rate limits at the proxy level—no changes needed in application code."},
            {"icon": "🛡️", "title": "LLM Gateway for Enterprise", "desc": "Deploy LiteLLM as a central gateway for all LLM traffic—add authentication, load balancing, fallbacks, and audit logging across every model provider."},
        ],
        "install_guide": {"cmd": "pip install litellm", "run": "litellm --model gpt-4o", "note": "Requires Python 3.8+. Set provider-specific API keys in environment. Start proxy: litellm --config config.yaml --port 4000. Docker: docker run -p 4000:4000 ghcr.io/berriai/litellm:main."}
    },
    "https://github.com/ggerganov/whisper.cpp": {
        "use_cases": [
            {"icon": "⚡", "title": "CPU-Optimized Speech Recognition", "desc": "Transcribe audio on CPU at real-time speed with 4-5x lower memory than OpenAI Whisper—runs on Raspberry Pi, mobile devices, and web browsers via WASM."},
            {"icon": "📱", "title": "On-Device Transcription", "desc": "Embed speech-to-text in iOS and Android apps—whisper.cpp compiles to a tiny C library with CoreML and GPU acceleration on both platforms."},
            {"icon": "🌐", "title": "Browser-Based Audio Processing", "desc": "Run whisper.cpp in the browser via WebAssembly—enable client-side transcription with zero server costs and complete audio privacy."},
        ],
        "install_guide": {"cmd": "git clone https://github.com/ggerganov/whisper.cpp && cd whisper.cpp && make -j", "run": "./main -m models/ggml-base.en.bin -f audio.wav", "note": "Requires C++ compiler. Download GGML models: bash ./models/download-ggml-model.sh base.en. Apple Silicon: make WHISPER_COREML=1. No Python required."}
    },
    "https://github.com/lllyasviel/Fooocus": {
        "use_cases": [
            {"icon": "🎨", "title": "Simplified Stable Diffusion Interface", "desc": "Generate high-quality images without complex prompts—Fooocus handles prompt expansion, negative prompts, and parameter tuning automatically for consistently good outputs."},
            {"icon": "🖼️", "title": "Inpainting & Outpainting Made Simple", "desc": "Paint a mask on any image and describe what you want—Fooocus fills the masked area with contextually matching content using advanced inpainting models."},
            {"icon": "🔄", "title": "Image Style Transfer & Variation", "desc": "Upload a reference image, adjust the style fidelity slider, and generate variations that keep the composition while changing style, lighting, and details."},
        ],
        "install_guide": {"cmd": "git clone https://github.com/lllyasviel/Fooocus && cd Fooocus", "run": "python entry_with_update.py", "note": "Requires NVIDIA GPU 8GB+ VRAM. Python 3.10. First launch downloads models (several GB). Use --preset realistic or --preset anime for style presets. Web UI at http://localhost:7860."}
    },
    "https://github.com/run-llama/llama_index": {
        "use_cases": [
            {"icon": "📚", "title": "Advanced RAG Architectures", "desc": "Implement agentic RAG, multi-hop retrieval, recursive summarization, and hybrid search—LlamaIndex provides 40+ built-in retrieval strategies beyond basic vector search."},
            {"icon": "🏗️", "title": "Data Ingestion Pipeline", "desc": "Connect 160+ data sources (Slack, Notion, SharePoint, Salesforce) into a unified index—LlamaIndex handles parsing, chunking, embedding, and incremental sync."},
            {"icon": "🤖", "title": "AI Agent with Structured Data", "title": "Build agents that query both unstructured text AND structured databases—auto-generate SQL from natural language, join with vector search results, and return unified answers."},
        ],
        "install_guide": {"cmd": "pip install llama-index", "run": "python -c \"from llama_index.core import VectorStoreIndex, SimpleDirectoryReader; print('OK')\"", "note": "Requires Python 3.9+. Install provider-specific packages (llama-index-llms-openai, llama-index-embeddings-ollama) for your stack. Starter tutorial: docs.llamaindex.ai."}
    },
    "https://github.com/oobabooga/text-generation-webui": {
        "use_cases": [
            {"icon": "💻", "title": "Local LLM Playground", "desc": "Load any GGUF, GPTQ, AWQ, or HF model through a web UI—test prompts, adjust generation parameters in real time, and compare model outputs side by side."},
            {"icon": "🔧", "title": "LoRA Training Interface", "desc": "Fine-tune models with LoRA directly from the UI—upload your training data in chat format, set rank and alpha, and start training without writing a single line of code."},
            {"icon": "🔌", "title": "OpenAI-Compatible API Mode", "desc": "Enable API mode and use text-generation-webui as a drop-in replacement for the OpenAI API—any app that supports custom base URLs can use it."},
        ],
        "install_guide": {"cmd": "git clone https://github.com/oobabooga/text-generation-webui && cd text-generation-webui", "run": "python server.py --listen --api", "note": "Requires NVIDIA GPU 6GB+ VRAM. Run start_linux.sh / start_macos.sh / start_windows.bat for auto-setup. Supports 20+ model formats. Web UI at http://localhost:7860."}
    },
    "https://github.com/mudler/LocalAI": {
        "use_cases": [
            {"icon": "🔄", "title": "OpenAI API Drop-In Replacement", "desc": "Replace the entire OpenAI API stack with LocalAI—same endpoints for chat, embeddings, images, TTS, and transcription, but everything runs on your own hardware."},
            {"icon": "📦", "title": "Kubernetes-Native AI Deployment", "desc": "Deploy LocalAI as a single container in your K8s cluster—auto-scaling, health checks, and Prometheus metrics for production-grade local AI infrastructure."},
            {"icon": "🎯", "title": "Multi-Model Backend", "desc": "Serve llama.cpp, diffusers, whisper.cpp, and bert.cpp models all through a single unified API—one deployment for text, image, audio, and embedding workloads."},
        ],
        "install_guide": {"cmd": "docker run -d -p 8080:8080 --name localai -v $PWD/models:/build/models localai/localai:latest", "run": "curl http://localhost:8080/v1/models", "note": "Requires Docker. Models auto-download on first request. GPU: docker run --gpus all ... localai/localai:latest-gpu-nvidia-cuda-12. API compatible with OpenAI SDK—just change base_url."}
    },
    "https://github.com/paul-gauthier/aider": {
        "use_cases": [
            {"icon": "💻", "title": "Terminal-Based AI Pair Programming", "desc": "Edit code in your terminal with AI that sees your entire git repo—describe changes in natural language, Aider applies them across multiple files with proper edits."},
            {"icon": "🔄", "title": "Iterative Refactoring with Git", "desc": "Every AI edit is a clean git commit—review, revert, or amend changes. Aider respects your .gitignore and automatically commits after each successful edit."},
            {"icon": "🗺️", "title": "Multi-File Architecture Changes", "desc": "Ask for 'move all API calls to a separate service layer' and Aider finds every file that needs changing, makes coordinated edits, and ensures imports stay consistent."},
        ],
        "install_guide": {"cmd": "pip install aider-chat", "run": "aider", "note": "Requires Python 3.10+ and an LLM API key (Anthropic recommended). Run inside a git repo for best results. Use aider --model sonnet for Claude, aider --4o for GPT-4o."}
    },
    "https://github.com/idiap/coqui-ai-TTS": {
        "use_cases": [
            {"icon": "🔊", "title": "High-Quality Text-to-Speech", "desc": "Generate natural-sounding speech with 20+ pretrained models—XTTSv2 supports voice cloning from a 6-second sample with multilingual output in 17 languages."},
            {"icon": "🎙️", "title": "Custom Voice Model Training", "desc": "Fine-tune TTS models on a specific speaker's voice with as little as 30 minutes of audio—produce studio-quality narration that matches the original speaker's tone."},
            {"icon": "🎮", "title": "Game Audio Pipeline", "desc": "Batch-generate NPC dialogue lines from a script CSV—consistent voice identity across thousands of lines with emotion tags for varied delivery."},
        ],
        "install_guide": {"cmd": "pip install TTS", "run": "tts --text \"Hello world\" --out_path output.wav", "note": "Requires Python 3.9+. GPU recommended but CPU works for short texts. First run downloads the default model (~1GB). For voice cloning: tts --model_name tts_models/multilingual/multi-dataset/xtts_v2."}
    },
    "https://github.com/milvus-io/milvus": {
        "use_cases": [
            {"icon": "🔍", "title": "Billion-Scale Vector Search", "desc": "Store and search billions of embeddings with sub-100ms latency—Milvus powers similarity search for recommendation engines, image retrieval, and semantic search at internet scale."},
            {"icon": "🧬", "title": "Hybrid Search & Filtering", "desc": "Combine vector similarity with scalar filtering (price range, date, category) in a single query—find 'visually similar products under $50 released this month'."},
            {"icon": "🏗️", "title": "Multi-Modal RAG Backend", "desc": "Index text, image, and video embeddings in a single Milvus collection—build RAG systems that retrieve across modalities with unified vector search."},
        ],
        "install_guide": {"cmd": "pip install pymilvus", "run": "python -c \"from pymilvus import connections; connections.connect(host='localhost', port='19530'); print('OK')\"", "note": "Server: docker compose up from milvus repo (requires 4GB+ RAM). For lightweight dev: milvus-lite (pip install milvus). Cloud: Zilliz Cloud free tier available. Requires etcd and MinIO for full deployment."}
    },
    "https://github.com/janhq/jan": {
        "use_cases": [
            {"icon": "💻", "title": "Desktop Local AI Assistant", "desc": "Download and run LLMs through a polished desktop app—Jan provides a ChatGPT-like experience with local models, offline mode, and no data collection."},
            {"icon": "🔌", "title": "OpenAI-Compatible Local API", "desc": "Enable the local API server and Jan exposes your downloaded models as an OpenAI-compatible endpoint at localhost:1337—use it with Continue, Aider, or any OpenAI SDK."},
            {"icon": "🧩", "title": "Extension Ecosystem", "desc": "Install extensions for model management, acceleration (TensorRT-LLM), and integrations—customize Jan to fit your workflow without waiting for built-in features."},
        ],
        "install_guide": {"cmd": "# Download from jan.ai (Mac/Windows/Linux)", "run": None, "note": "Desktop app: download from jan.ai. Enables local API server at localhost:1337/v1. Requires no Docker or terminal—models download with one click inside the app."}
    },
    "https://github.com/gradio-app/gradio": {
        "use_cases": [
            {"icon": "🚀", "title": "ML Model Demo in 5 Lines", "desc": "Wrap any Python function in a Gradio interface and get a shareable web UI with a public URL—perfect for demos, stakeholder reviews, and Hugging Face Spaces."},
            {"icon": "🧩", "title": "Interactive Data Annotation Tool", "desc": "Build custom labeling interfaces for images, text, and audio with real-time model predictions—annotators correct outputs while the model learns from feedback."},
            {"icon": "🔗", "title": "Multi-Model Comparison Dashboard", "desc": "Create side-by-side comparison UIs for A/B testing model outputs—stakeholders rate responses blind, and Gradio logs structured feedback for analysis."},
        ],
        "install_guide": {"cmd": "pip install gradio", "run": "python -c \"import gradio as gr; gr.Interface(fn=lambda x: f'Hello {x}!', inputs='text', outputs='text').launch()\"", "note": "Requires Python 3.8+. Auto-generates a public shareable link (72h validity). For permanent hosting: deploy to Hugging Face Spaces. Hot-reload enabled with gradio deploy."}
    },
    "https://github.com/ray-project/ray": {
        "use_cases": [
            {"icon": "⚡", "title": "Distributed ML Training", "desc": "Scale PyTorch and TensorFlow training from 1 GPU to 1000 GPUs with 2 lines of code change—Ray handles distributed data loading, model parallelism, and fault tolerance."},
            {"icon": "🤖", "title": "Production LLM Serving with Ray Serve", "desc": "Deploy LLMs at scale with auto-scaling, canary rollouts, and request batching—Ray Serve manages deployment complexity so you focus on model logic."},
            {"icon": "📊", "title": "Hyperparameter Tuning at Scale", "desc": "Run thousands of parallel trials with Ray Tune—supports Bayesian optimization, Population Based Training, and ASHA early stopping across any ML framework."},
        ],
        "install_guide": {"cmd": "pip install ray", "run": "ray start --head", "note": "Requires Python 3.9+. Single-node: just 'pip install ray' and import. Multi-node cluster: ray start on each node. Dashboard at http://localhost:8265 for monitoring and job management."}
    },
    "https://github.com/microsoft/DeepSpeed": {
        "use_cases": [
            {"icon": "🚀", "title": "Train 100B+ Parameter Models", "desc": "DeepSpeed ZeRO-3 enables training trillion-parameter models across thousands of GPUs—partition optimizer states, gradients, and parameters to eliminate memory bottlenecks."},
            {"icon": "⚡", "title": "3-5x Faster Inference", "desc": "DeepSpeed Inference delivers up to 5x throughput improvement with kernel fusion, tensor parallelism, and heterogeneous memory management for production serving."},
            {"icon": "🎯", "title": "Fine-Tuning on Consumer GPUs", "desc": "Use ZeRO-Offload to fine-tune 13B models on a single 24GB GPU by offloading optimizer states to CPU RAM—what previously required 8 GPUs fits on one."},
        ],
        "install_guide": {"cmd": "pip install deepspeed", "run": "deepspeed --help", "note": "Requires NVIDIA GPU + CUDA 11.0+. PyTorch 2.0+ required. For ZeRO-3: add --deepspeed ds_config.json to your training script. Check deepspeed.ai for config templates."}
    },
    "https://github.com/danielmiessler/fabric": {
        "use_cases": [
            {"icon": "🧩", "title": "AI Pattern Library for Daily Tasks", "desc": "Apply 100+ curated AI patterns (summarization, extraction, analysis) to your content—pipe in a YouTube transcript and get back key insights with a single command."},
            {"icon": "🔧", "title": "CLI-First AI Workflow", "desc": "Build AI-powered shell pipelines: `yt-dlp transcript | fabric -p summarize | fabric -p extract_action_items`—compose patterns like Unix pipes."},
            {"icon": "📝", "title": "Custom Pattern Creation", "desc": "Write your own AI patterns as simple markdown files with system prompts—share patterns with your team for consistent AI output across the organization."},
        ],
        "install_guide": {"cmd": "pip install fabric-ai", "run": "fabric --setup", "note": "Requires Python 3.10+ and an OpenAI/Anthropic API key. Run fabric --setup to configure API keys and download patterns. Pipe any text: cat file.txt | fabric -p summarize."}
    },
    "https://github.com/facebookresearch/faiss": {
        "use_cases": [
            {"icon": "⚡", "title": "Billion-Scale Similarity Search", "desc": "Search through billions of vectors in milliseconds—FAISS compresses indexes to fit in RAM with near-exact accuracy using Product Quantization and IVF indexes."},
            {"icon": "🔍", "title": "Deduplication at Scale", "desc": "Find near-duplicate images, documents, or user profiles in massive datasets—FAISS identifies clusters and duplicates faster than any other open-source library."},
            {"icon": "🧬", "title": "Recommendation System Backend", "desc": "Power the retrieval stage of two-tower recommendation models—FAISS serves candidate generation with sub-10ms latency for millions of items."},
        ],
        "install_guide": {"cmd": "pip install faiss-cpu  # or faiss-gpu for CUDA", "run": "python -c \"import faiss; print(faiss.__version__)\"", "note": "CPU: pip install faiss-cpu. GPU: pip install faiss-gpu (requires CUDA 11.4+). For Conda: conda install -c pytorch faiss-gpu. No server needed—pure library embedded in your Python process."}
    },
    "https://github.com/danny-avila/LibreChat": {
        "use_cases": [
            {"icon": "💬", "title": "Multi-Provider Chat Interface", "desc": "Use OpenAI, Anthropic, Google, Bing, and local models in one unified chat UI—switch providers mid-conversation and compare answers from different models."},
            {"icon": "🔌", "title": "Plugin & Tool Ecosystem", "desc": "Enable plugins for web search, image generation (DALL-E/Stable Diffusion), code interpretation, and file upload—tools work across all supported LLM providers."},
            {"icon": "👥", "title": "Multi-User Self-Hosted ChatGPT", "desc": "Deploy for your entire team with OAuth (Google/GitHub/OpenID), conversation sharing, message branching, and admin dashboard for usage monitoring."},
        ],
        "install_guide": {"cmd": "git clone https://github.com/danny-avila/LibreChat && cd LibreChat", "run": "docker compose up -d", "note": "Requires Docker & Docker Compose. Web UI at http://localhost:3080. Configure API keys in librechat.yaml after first launch. Supports 15+ AI providers."}
    },
    "https://github.com/2noise/ChatTTS": {
        "use_cases": [
            {"icon": "🎤", "title": "Conversational Chinese & English TTS", "desc": "Generate speech with natural conversational prosody—ChatTTS excels at dialogue-style narration with appropriate pauses, laughter, and interjections inserted automatically."},
            {"icon": "🎙️", "title": "Audiobook Narration", "desc": "Convert long-form text into natural-sounding audiobooks with chat-level expressiveness—more engaging than traditional TTS for story narration and dialogue scenes."},
            {"icon": "🎮", "title": "Game & Virtual Character Voices", "desc": "Generate diverse character voices with conversational tone for games and virtual avatars—each character gets a natural speaking style with appropriate rhythm and emotion."},
        ],
        "install_guide": {"cmd": "pip install chattts", "run": "python -c \"from ChatTTS import ChatTTS; print('OK')\"", "note": "Requires Python 3.9+. GPU recommended (4GB+ VRAM). For better quality, download the full model from Hugging Face. Pre-trained model auto-downloads on first use."}
    },
    "https://github.com/QuivrHQ/quivr": {
        "use_cases": [
            {"icon": "🧠", "title": "Second Brain Knowledge Management", "desc": "Upload everything you've read, watched, and bookmarked—Quivr organizes it into an AI-searchable knowledge base that answers questions with citations to your sources."},
            {"icon": "🔗", "title": "Multi-Platform Integration", "desc": "Connect Gmail, Notion, Slack, and GitHub—Quivr syncs content automatically and lets you query across all platforms from a single chat interface."},
            {"icon": "🧩", "title": "Custom AI Brain for Teams", "desc": "Create shared brains for different projects—onboard new team members by pointing them at the brain instead of digging through wikis and old Slack threads."},
        ],
        "install_guide": {"cmd": "git clone https://github.com/QuivrHQ/quivr && cd quivr", "run": "docker compose up -d", "note": "Requires Docker. Web UI at http://localhost:3000. Also available as a managed cloud service at quivr.com. Requires Supabase (free tier works) for backend storage."}
    },
    "https://github.com/suno-ai/bark": {
        "use_cases": [
            {"icon": "🎤", "title": "Expressive Multilingual TTS", "desc": "Generate speech with non-verbal cues—laughter, sighs, music notes—in 13+ languages. Bark captures tone and emotion that traditional TTS engines flatten into monotone output."},
            {"icon": "🎵", "title": "AI Music & Sound Effect Generation", "desc": "Beyond speech, Bark can generate background music snippets, sound effects, and ambient audio—useful for game prototypes and content creation without royalty concerns."},
            {"icon": "🎙️", "title": "Creative Podcast Production", "desc": "Generate podcast intros, ad reads, and character voices with natural expressiveness—Bark's emotional range makes it suitable for creative audio projects."},
        ],
        "install_guide": {"cmd": "pip install git+https://github.com/suno-ai/bark.git", "run": "python -c \"from bark import SAMPLE_RATE; from bark.generation import generate_text_semantic; print('OK')\"", "note": "Requires Python 3.9+ and a GPU (12GB+ VRAM recommended). CPU mode works but is extremely slow (minutes per sentence). Also available via Hugging Face transformers pipeline."}
    },
    "https://github.com/LAION-AI/Open-Assistant": {
        "use_cases": [
            {"icon": "🤖", "title": "Open-Source ChatGPT Alternative", "desc": "Deploy a community-built conversational AI that rivals ChatGPT—fine-tuned on 13K human-annotated conversations in 35+ languages with RLHF alignment."},
            {"icon": "📊", "title": "RLHF Research Platform", "desc": "Study and reproduce RLHF training pipelines—Open Assistant provides the full data collection, training, and evaluation stack as open-source reference implementation."},
            {"icon": "🔧", "title": "Custom Instruction-Tuned Models", "desc": "Use the Open Assistant dataset and training pipeline to create your own instruction-tuned model for domain-specific conversational tasks."},
        ],
        "install_guide": {"cmd": "git clone https://github.com/LAION-AI/Open-Assistant && cd Open-Assistant", "run": "docker compose up -d", "note": "Requires Docker and significant GPU resources for training (8× A100 recommended for full reproduction). For inference-only, use smaller community fine-tunes on Hugging Face."}
    },
    "https://github.com/HKUDS/LightRAG": {
        "use_cases": [
            {"icon": "🔍", "title": "Graph-Enhanced RAG", "desc": "Go beyond vector search—LightRAG builds a knowledge graph from your documents and retrieves information through both graph traversal and vector similarity for higher recall."},
            {"icon": "⚡", "title": "Cost-Efficient Document Q&A", "desc": "Process 1000-page documents at a fraction of the API cost of baseline RAG—LightRAG's incremental graph construction eliminates redundant LLM calls."},
            {"icon": "🧩", "title": "Multi-Hop Reasoning", "desc": "Answer questions that require connecting facts across different documents—LightRAG's graph structure enables multi-hop reasoning that pure vector search misses."},
        ],
        "install_guide": {"cmd": "pip install lightrag-hku", "run": "python -c \"from lightrag import LightRAG; print('OK')\"", "note": "Requires Python 3.9+ and an OpenAI-compatible API. Works with local Ollama for fully offline operation. Supports Neo4j, NetworkX, and ArangoDB as graph backends."}
    },
    "https://github.com/myshell-ai/OpenVoice": {
        "use_cases": [
            {"icon": "🎤", "title": "Zero-Shot Voice Cloning", "desc": "Clone any voice with a single audio clip and control tone color, accent, rhythm, and emotion independently—adjust just the accent without changing the voice identity."},
            {"icon": "🌍", "title": "Cross-Lingual Voice Transfer", "desc": "Make a cloned Chinese voice speak fluent English with natural pronunciation while preserving the original speaker's timbre, emotion, and speaking style."},
            {"icon": "🎮", "title": "Real-Time Voice Conversion", "desc": "Convert voice in near real-time for live streaming, virtual meetings, and gaming—change your voice while maintaining natural prosody and expressiveness."},
        ],
        "install_guide": {"cmd": "git clone https://github.com/myshell-ai/OpenVoice && cd OpenVoice", "run": "pip install -e . && python demo.py", "note": "Requires Python 3.9+ and GPU (4GB+ VRAM). Pretrained models download automatically. For real-time mode, use the realtime_inference branch and a fast GPU."}
    },
    "https://github.com/VikParuchuri/marker": {
        "use_cases": [
            {"icon": "📄", "title": "PDF-to-Markdown with Higher Accuracy", "desc": "Convert PDFs to clean Markdown with header structure, tables, code blocks, and inline math preserved—outperforms PyMuPDF and pdf2txt by 20-30% on complex layouts."},
            {"icon": "🧪", "title": "Scientific Paper to Structured Text", "desc": "Parse academic PDFs with LaTeX formulas, figures, and multi-column layouts into clean Markdown—ready for RAG ingestion or LLM fine-tuning datasets."},
            {"icon": "📚", "title": "Batch Document Digitization", "desc": "Process thousands of PDFs in parallel with GPU acceleration—convert a library of scanned documents to searchable, structured Markdown for AI processing."},
        ],
        "install_guide": {"cmd": "pip install marker-pdf", "run": "marker /path/to/input /path/to/output", "note": "Requires Python 3.9+ and GPU (6GB+ VRAM recommended). CPU mode works but is slower. For OCR of scanned PDFs: pip install marker-pdf[ocr]. Outputs individual .md files per PDF."}
    },
    "https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI": {
        "use_cases": [
            {"icon": "🎤", "title": "High-Fidelity Voice Conversion", "desc": "Transform any voice into a target voice with studio-quality fidelity—RVC captures vocal timbre, pitch patterns, and speech mannerisms with as little as 10 minutes of training audio."},
            {"icon": "🎵", "title": "AI Song Cover Creation", "desc": "Replace the original vocalist in any song with a cloned voice—popular for creating AI covers while preserving the original instrumental track's quality."},
            {"icon": "🎮", "title": "Virtual Streamer Voice Setup", "desc": "Create a consistent character voice for VTubers and virtual streamers—the WebUI provides real-time voice conversion for live streaming with low latency."},
        ],
        "install_guide": {"cmd": "git clone https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI && cd Retrieval-based-Voice-Conversion-WebUI", "run": "python webui.py", "note": "Requires NVIDIA GPU 8GB+ VRAM. Python 3.9+. Pretrained models (~2GB) download on first launch. 10-30 minutes of clean audio yields good voice cloning results. Web UI at http://localhost:7865."}
    },
    "https://github.com/xinntao/Real-ESRGAN": {
        "use_cases": [
            {"icon": "🔍", "title": "AI Image & Video Upscaling", "desc": "Upscale low-resolution images 4x with realistic detail restoration—Real-ESRGAN reconstructs faces, textures, and text that traditional bicubic upscaling blurs into mush."},
            {"icon": "🎮", "title": "Game Texture Enhancement", "desc": "Upscale retro game textures and sprites while preserving artistic style—enhance classic game mods with AI-restored high-resolution assets."},
            {"icon": "📸", "title": "Photo Restoration Pipeline", "desc": "Combine Real-ESRGAN upscaling with GFPGAN face restoration to breathe new life into old, damaged, or low-resolution photographs."},
        ],
        "install_guide": {"cmd": "pip install realesrgan", "run": "realesrgan-ncnn-vulkan -i input.jpg -o output.jpg -s 4", "note": "Requires NVIDIA GPU (ncnn Vulkan version) or CPU. For Python SDK: pip install basicsr && git clone the repo. Pretrained models auto-download. Supports 2x, 3x, 4x, and 8x upscaling for specific domains (anime, face, general)."}
    },
    "https://github.com/CopilotKit/CopilotKit": {
        "use_cases": [
            {"icon": "🧩", "title": "In-App AI Copilot for React Apps", "desc": "Add an AI sidebar to any React application in under an hour—CopilotKit provides ready-made UI components that connect to your app's state and actions."},
            {"icon": "🔗", "title": "AI-Aware Application State", "desc": "Give the AI read and write access to your app's state—users can say 'sort the table by revenue descending' and CopilotKit directly manipulates the UI state."},
            {"icon": "🤖", "title": "Agent-Driven Workflow Automation", "desc": "Build multi-step AI workflows within your app—the copilot can create a Jira ticket, assign it, and notify Slack, all through your existing business logic."},
        ],
        "install_guide": {"cmd": "npm install @copilotkit/react-core @copilotkit/react-ui", "run": None, "note": "Requires React 18+ and Node.js 18+. Works with Next.js, Remix, and Vite. Add <CopilotKit> provider at the root, <CopilotSidebar> for the UI. Connect to OpenAI or any LLM."}
    },
    "https://github.com/stanfordnlp/dspy": {
        "use_cases": [
            {"icon": "🔧", "title": "Programming, Not Prompting, for LLMs", "desc": "Replace brittle prompt strings with composable modules—DSPy compiles declarative programs into optimized prompts, few-shot examples, and fine-tuning data automatically."},
            {"icon": "🧪", "title": "Systematic LLM Optimization", "desc": "Define a metric and let DSPy automatically find the best prompt structure, demonstrations, and LM configuration—treat LLM behavior as an optimization problem, not an art."},
            {"icon": "📊", "title": "Multi-Model Benchmarking", "desc": "Compile the same DSPy program for GPT-4, Claude, and Llama-3 and compare quality systematically—DSPy handles the prompt format differences so you compare apple-to-apple."},
        ],
        "install_guide": {"cmd": "pip install dspy-ai", "run": "python -c \"import dspy; print(dspy.__version__)\"", "note": "Requires Python 3.9+ and an LLM API key. Quick start: dspy.configure(lm=dspy.LM('openai/gpt-4o-mini')). Documentation at dspy.ai with tutorials and example programs."}
    },
    "https://github.com/khoj-ai/khoj": {
        "use_cases": [
            {"icon": "🧠", "title": "Personal AI Search Engine", "desc": "Khoj indexes your Markdown, PDF, Org-mode, and plaintext notes—search your personal knowledge base with natural language and get AI-generated answers grounded in your own writing."},
            {"icon": "🔌", "title": "Self-Hosted AI Second Brain", "desc": "Run Khoj on your own server, connect it to Obsidian, Logseq, or any notes folder—your personal AI that learns from everything you've written, completely private."},
            {"icon": "🤖", "title": "AI Agent for Personal Data", "desc": "Beyond search, Khoj can create calendar events, send emails, and draft documents based on your notes—an AI agent that operates on your personal knowledge graph."},
        ],
        "install_guide": {"cmd": "pip install khoj-assistant", "run": "khoj", "note": "Requires Python 3.9+ and an OpenAI/Anthropic API key. Web UI at http://localhost:42110. Desktop app also available (Mac/Windows/Linux). Obsidian plugin for tighter integration."}
    },
    "https://github.com/continuedev/continue": {
        "use_cases": [
            {"icon": "💻", "title": "Open-Source IDE AI Assistant", "desc": "Bring AI code completion, chat, and editing to VS Code and JetBrains—Continue connects to any LLM (local or cloud) and indexes your codebase for context-aware suggestions."},
            {"icon": "🔧", "title": "Custom Slash Commands & Rules", "desc": "Define project-specific AI commands like '/review-sql' or '/fix-lint'—Continue runs your custom prompts with full codebase context and applies fixes directly to files."},
            {"icon": "🏠", "title": "Fully Offline AI Coding", "desc": "Pair Continue with Ollama or LM Studio for AI-assisted coding with zero data leaving your machine—autocomplete, chat, and edit features work entirely offline."},
        ],
        "install_guide": {"cmd": "code --install-extension Continue.continue", "run": "Cmd+L / Ctrl+L to open chat panel", "note": "VS Code / JetBrains extension. VS Code: install from marketplace. JetBrains: install from plugin marketplace. Configure model in ~/.continue/config.json. Supports Ollama, Anthropic, OpenAI, and 20+ providers."}
    },
    "https://github.com/user1342/awesome-mcp-servers": {
        "use_cases": [
            {"icon": "📋", "title": "MCP Server Discovery", "desc": "Browse 100+ curated MCP servers organized by category—find exactly the server you need for filesystem access, database queries, web search, and more."},
            {"icon": "🔧", "title": "Reference Implementation Library", "desc": "Study real MCP server implementations to build your own—each listed server is a working example with source code you can read and adapt."},
            {"icon": "📊", "title": "Stay Updated on the MCP Ecosystem", "desc": "Track new MCP server releases, community favorites, and integration patterns—the list is actively maintained and reflects the latest MCP ecosystem developments."},
        ],
        "install_guide": {"cmd": "# Browse: https://github.com/user1342/awesome-mcp-servers", "run": None, "note": "This is a curated list, not an installable tool. Browse the README for categorized MCP server links. Each listed server has its own installation instructions."}
    },

    "https://github.com/microsoft/graphrag": {
        "use_cases": [
            {"icon": "🧬", "title": "Knowledge Graph RAG", "desc": "Go beyond vector search—GraphRAG extracts entities, relationships, and communities from documents to answer global questions vector search misses, like 'what are the main themes across this dataset?'"},
            {"icon": "📊", "title": "Enterprise Document Intelligence", "desc": "Process 10,000+ internal documents and build a knowledge graph that reveals cross-document patterns, trends, and contradictions that no single document contains."},
            {"icon": "🔍", "title": "Global Summarization & Thematic Analysis", "desc": "Ask 'summarize all customer complaints from 2025' and GraphRAG identifies thematic clusters and representative examples—not just keyword matches but conceptual understanding."},
        ],
        "install_guide": {"cmd": "pip install graphrag", "run": "graphrag init --root ./my_project", "note": "Requires Python 3.10+ and an OpenAI-compatible API key. Run 'graphrag init' to create a project, then 'graphrag index' to build the knowledge graph, then 'graphrag query' to ask questions."}
    },
    "https://github.com/huggingface/diffusers": {
        "use_cases": [
            {"icon": "🎨", "title": "Programmatic Image Generation", "desc": "Generate images from text prompts with Stable Diffusion, Flux, and SDXL in Python—full control over every generation parameter with a clean, modular API."},
            {"icon": "🎥", "title": "Video Generation & Editing", "desc": "Use AnimateDiff, Stable Video Diffusion, and I2VGen-XL through a unified pipeline API—text-to-video, image-to-video, and video editing with consistent frame quality."},
            {"icon": "🔧", "title": "Custom Diffusion Pipeline Development", "desc": "Build custom image generation pipelines by composing modular components—add ControlNet for pose guidance, IP-Adapter for style reference, and LoRA for character consistency."},
        ],
        "install_guide": {"cmd": "pip install diffusers transformers accelerate", "run": "python -c \"from diffusers import DiffusionPipeline; print('OK')\"", "note": "Requires Python 3.8+ and GPU (8GB+ VRAM recommended). For SDXL: extra 8GB recommended. CPU inference possible but slow. For SD3/Flux: pip install diffusers[torch]."}
    },
    "https://github.com/openai/CLIP": {
        "use_cases": [
            {"icon": "🔍", "title": "Zero-Shot Image Classification", "desc": "Classify images into any category without training—just describe categories in natural language and CLIP matches images to the best description with impressive accuracy."},
            {"icon": "🖼️", "title": "Text-to-Image Search", "desc": "Build a semantic image search engine—users describe what they want in words, and CLIP finds the most visually similar images without any per-image labels or training."},
            {"icon": "🎯", "title": "Content Moderation Pipeline", "desc": "Use CLIP as the first stage in content moderation—detect NSFW, violent, or policy-violating images with natural language concept descriptions instead of brittle classification labels."},
        ],
        "install_guide": {"cmd": "pip install git+https://github.com/openai/CLIP.git", "run": "python -c \"import clip; model, preprocess = clip.load('ViT-B/32'); print('OK')\"", "note": "Requires Python 3.8+ and PyTorch 1.7+. GPU recommended but CPU works for small batches. Model weights (~340MB) download on first load. Also available as open-clip-torch for community-trained variants."}
    },
    "https://github.com/explosion/spaCy": {
        "use_cases": [
            {"icon": "⚡", "title": "Industrial-Strength NLP Pipeline", "desc": "Tokenize, tag, parse, and perform NER on text at 100K+ words/second—spaCy is designed for production use with predictable memory usage and no-crash guarantees."},
            {"icon": "🔧", "title": "Custom Named Entity Recognition", "desc": "Train domain-specific NER models to extract your business entities—product names, legal citations, medical terms—with spaCy's config-driven training system."},
            {"icon": "🌍", "title": "Multi-Language Text Processing", "desc": "Process text in 75+ languages with pre-trained pipelines—spaCy handles tokenization differences across Latin, Cyrillic, CJK, and Arabic scripts out of the box."},
        ],
        "install_guide": {"cmd": "pip install spacy", "run": "python -m spacy download en_core_web_sm", "note": "Requires Python 3.9+. Download language models separately (en_core_web_sm/lg/trf for English). For GPU: pip install spacy[cuda12x]. Transformer-based pipelines need spacy-transformers."}
    },
    "https://github.com/TabbyML/tabby": {
        "use_cases": [
            {"icon": "💻", "title": "Self-Hosted GitHub Copilot Alternative", "desc": "Run your own AI code completion server—Tabby provides whole-line and full-function completions with zero data leaving your infrastructure and zero per-seat pricing."},
            {"icon": "🔒", "title": "Code Completion on Air-Gapped Networks", "desc": "Deploy Tabby in environments with no internet access—models run entirely on-premises, satisfying the strictest security and compliance requirements."},
            {"icon": "🧩", "title": "Custom Fine-Tuned Completion Models", "desc": "Fine-tune Tabby on your organization's codebase for completions that match your internal APIs, coding style, and patterns—model improves as your team uses it."},
        ],
        "install_guide": {"cmd": "docker run -d -p 8080:8080 -v $HOME/.tabby:/data tabbyml/tabby serve --model StarCoder-1B", "run": None, "note": "Requires Docker. GPU: add --gpus all for acceleration. IDE plugins available for VS Code, JetBrains, and Vim/Neovim. Configure IDE plugin to point at http://localhost:8080."}
    },
    "https://github.com/continuedev/continue": {
        "use_cases": [
            {"icon": "💻", "title": "Open-Source AI Coding Assistant", "desc": "AI-powered code completion, chat, and editing in VS Code and JetBrains—connect to any LLM (cloud or local) with full codebase context awareness."},
            {"icon": "🔧", "title": "Custom Slash Commands", "desc": "Define project-specific AI commands like '/explain-architecture' or '/generate-tests'—Continue executes your prompt with full context and applies changes to files."},
            {"icon": "🏠", "title": "Completely Offline AI Coding", "desc": "Pair with Ollama or LM Studio for AI-assisted coding with zero data leaving your machine—all features work entirely offline."},
        ],
        "install_guide": {"cmd": "code --install-extension Continue.continue", "run": "Cmd+L to open chat", "note": "VS Code / JetBrains extension. Configure model in ~/.continue/config.json. Supports 20+ LLM providers including local models via Ollama. Free and open-source."}
    },
}


def inject_tool_data():
    with open(DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)

    tools = data["tools"]
    injected = 0
    skipped = 0

    for tool in tools:
        url = tool.get("githubUrl", "")
        if not url:
            skipped += 1
            continue

        td = TOOL_DATA.get(url)
        if td is None:
            skipped += 1
            continue

        # 跳过标记为空的条目（如 DeepSeek-V3、ChatGLM，它们是模型而非工具）
        if td.get("use_cases") is None or td.get("install_guide") is None:
            skipped += 1
            continue

        # 注入 use_cases（只注入非空的）
        if td.get("use_cases"):
            tool["use_cases"] = td["use_cases"]

        # 注入 install_guide
        if td.get("install_guide"):
            tool["install_guide"] = td["install_guide"]

        injected += 1
        print(f"  ✓ {tool['name']:<30} +use_cases({len(td.get('use_cases',[]))}) +install_guide")

    # 写回
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n完成: 注入 {injected} 个工具, 跳过 {skipped} 个工具")
    print(f"文件大小: {os.path.getsize(DATA_PATH):,} bytes")


if __name__ == "__main__":
    inject_tool_data()

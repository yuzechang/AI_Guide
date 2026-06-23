"""添加 3 个高价值对比页条目到 compare_data.json"""
import json, os

BASE = os.path.dirname(__file__)

with open(os.path.join(BASE, 'compare_data.json'), encoding='utf-8') as f:
    data = json.load(f)

# 检查是否已添加
existing_slugs = {e['slug'] for e in data}

new_entries = [
  {
    "slug": "cursor-vs-claude-code",
    "title": "Cursor vs Claude Code",
    "tool_a_id": "cursor",
    "tool_b_id": "claude-code",
    "intro": "Cursor and Claude Code represent two different philosophies for AI-assisted development in 2026. Cursor is a full IDE (VS Code fork) with AI baked in. Claude Code is a terminal agent that works alongside your existing editor and executes tasks autonomously. Both are powerful, but they solve different problems. This comparison covers where each excels, when to use both together, and how to decide based on your actual workflow.",
    "verdict": "Use Cursor for day-to-day coding: autocomplete, multi-file edits, asking questions about your codebase. Use Claude Code for autonomous tasks like migrations, refactors, or adding tests across all files. Many experienced developers use both. If you can only pick one: Cursor for beginners, Claude Code for developers comfortable with terminal workflows.",
    "table": [
      {"feature": "Interface", "a": "Full IDE (VS Code fork)", "b": "Terminal CLI / VS Code extension", "winner": ""},
      {"feature": "Pricing", "a": "$20/mo Pro", "b": "Included in Claude Max / API billing", "winner": ""},
      {"feature": "Autonomy level", "a": "Interactive (approve each change)", "b": "Agent (runs tasks end-to-end)", "winner": "b"},
      {"feature": "Multi-file editing", "a": "Composer mode (with approval)", "b": "Autonomous with bash + file tools", "winner": "b"},
      {"feature": "Context window", "a": "Codebase index + current files", "b": "200k tokens (Claude Sonnet/Opus)", "winner": "b"},
      {"feature": "Model choice", "a": "GPT-4o, Claude, Gemini", "b": "Claude Sonnet/Opus only", "winner": "a"},
      {"feature": "Inline autocomplete", "a": "Best-in-class Tab completion", "b": "Not applicable (CLI agent)", "winner": "a"},
      {"feature": "Git integration", "a": "Standard IDE git", "b": "Native, reads git history", "winner": "b"},
      {"feature": "IDE lock-in", "a": "Must use Cursor IDE", "b": "Works in any editor + terminal", "winner": "b"},
      {"feature": "Learning curve", "a": "Low (VS Code users adapt fast)", "b": "Medium (requires CLI comfort)", "winner": "a"}
    ],
    "desc_a": "Cursor is an AI-first IDE forked from VS Code. It adds deep AI capabilities: Tab autocomplete that understands your whole codebase, Composer mode for multi-file edits, and built-in chat with @codebase context. The interactive model means you see and approve every change. Supports multiple model providers including GPT-4o, Claude Sonnet, and Gemini. The free tier is generous; Pro at $20/month removes limits.",
    "desc_b": "Claude Code is Anthropic's terminal-native coding agent. It runs in your terminal, reads your files and git history, executes bash commands, and makes autonomous multi-file changes to accomplish a task you describe in natural language. It uses Claude Sonnet or Opus with a 200k+ token context window. Available in the Claude Max subscription ($100/mo) or via API billing.",
    "choose_a": [
      "You want AI autocomplete integrated into every line you write",
      "You prefer interactive, approve-each-change workflows",
      "You are a VS Code user who wants AI features without switching editors",
      "You want to choose from multiple LLM providers",
      "You are new to AI coding tools and want a visual interface"
    ],
    "choose_b": [
      "You want to delegate multi-step tasks and come back to results",
      "You prefer your current editor and do not want to switch",
      "You are comfortable in the terminal and with git workflows",
      "You work on large refactors, migrations, or repetitive multi-file changes",
      "You need the largest context window for understanding big codebases"
    ],
    "sections": [
      {
        "id": "workflow",
        "title": "Interactive vs Agentic: The Real Difference",
        "content": "The fundamental difference is not features, it is the workflow model. Cursor is interactive: every suggestion is a proposal you accept or reject in real time. Claude Code is agentic: you give it a task, it plans and executes autonomously, then reports back. Interactive is better when you are exploring, learning a codebase, or making design decisions alongside the code. Agentic is better when the task is well-defined and you want to delegate it: adding tests, updating an API contract, migrating a pattern. Most developers end up using both."
      },
      {
        "id": "cost",
        "title": "Cost Comparison: Flat vs Usage-Based",
        "content": "Cursor Pro is $20/month flat, predictable. Claude Code is usage-based: included in Claude Max ($100/month) or billed per token via the API. A typical autonomous coding session costs roughly $0.50-2.00 in tokens. For developers doing heavy agentic work, this adds up faster than Cursor's flat fee. For occasional use, the API model is cheaper. The break-even is roughly 10-40 substantial tasks per month."
      }
    ],
    "faqs": [
      {"q": "Can I use Cursor and Claude Code together?", "a": "Yes, and many developers do. A common workflow: use Cursor for interactive coding (autocomplete, quick edits, questions), use Claude Code for autonomous tasks running in a terminal window while you continue in Cursor. They do not conflict since Claude Code makes file changes that Cursor picks up automatically."},
      {"q": "Is Claude Code free?", "a": "Claude Code is included in the Claude Max subscription ($100/month). Without Max, you pay per API token, typically $0.50-3.00 per coding session. There is no free tier for heavy agentic use."},
      {"q": "Which is better for beginners?", "a": "Cursor, by a significant margin. The interactive IDE model, visual diffs, and approve-each-change workflow are much more learnable. Claude Code rewards users who understand their codebase and can write clear task descriptions, which requires experience."},
      {"q": "Which has better context awareness?", "a": "For whole-codebase tasks, Claude Code's 200k token window gives it an edge on medium-sized projects. For interactive line-by-line coding, Cursor's codebase index and retrieval is more practical since you do not need to load the full project into context every keystroke."},
      {"q": "Does Claude Code work in VS Code?", "a": "Yes, Claude Code has a VS Code extension. You can also run it in any terminal alongside any editor. The terminal version is the primary interface; the VS Code extension adds convenience."}
    ],
    "related_compares": [
      {"slug": "cursor-vs-aider", "title": "Cursor vs Aider", "desc": "Compare Cursor with Aider, the terminal-native AI pair programmer"},
      {"slug": "cline-vs-cursor", "title": "Cline vs Cursor", "desc": "Cline: the free open-source alternative to Cursor"},
      {"slug": "cursor-vs-github-copilot", "title": "Cursor vs GitHub Copilot", "desc": "Compare the two most popular AI coding assistants"}
    ]
  },
  {
    "slug": "ollama-vs-lm-studio",
    "title": "Ollama vs LM Studio",
    "tool_a_id": "ollama",
    "tool_b_id": "lm-studio",
    "intro": "Ollama and LM Studio are the two most popular tools for running large language models locally in 2026. Both let you run Llama, Mistral, Qwen and other open-source models on your own hardware. But they serve different users: Ollama is built for developers who want a local LLM API to integrate into applications, while LM Studio is built for users who want a desktop chat interface without writing code.",
    "verdict": "Choose Ollama if you are a developer integrating local LLMs into apps, scripts, or services via REST API. Choose LM Studio if you want a polished desktop UI for chatting with local models without any command-line work. Both support the same models. Many developers install Ollama for their apps and LM Studio for personal exploration.",
    "table": [
      {"feature": "Interface", "a": "CLI + REST API", "b": "Desktop GUI (Mac/Windows/Linux)", "winner": ""},
      {"feature": "API compatibility", "a": "OpenAI-compatible REST API", "b": "OpenAI-compatible local server", "winner": ""},
      {"feature": "Model library", "a": "Ollama library (100+ curated models)", "b": "Hugging Face GGUF (thousands)", "winner": "b"},
      {"feature": "Install", "a": "Single command", "b": "Desktop app installer", "winner": ""},
      {"feature": "Technical skill required", "a": "Low-medium (comfortable with CLI)", "b": "Low (point-and-click)", "winner": "b"},
      {"feature": "Model management", "a": "CLI: ollama pull / ollama list", "b": "GUI model browser + downloader", "winner": "b"},
      {"feature": "Apple Silicon performance", "a": "Excellent (Metal GPU)", "b": "Excellent (Metal GPU)", "winner": ""},
      {"feature": "API for app integration", "a": "Purpose-built for this", "b": "Local server mode available", "winner": "a"},
      {"feature": "Open source", "a": "Yes (MIT, 174k+ stars)", "b": "No (free for personal use)", "winner": "a"},
      {"feature": "Price", "a": "Free, open-source", "b": "Free for personal use", "winner": ""}
    ],
    "desc_a": "Ollama is an open-source tool with 174k+ GitHub stars that makes running large language models locally as simple as running a container. Install it, run ollama pull llama3.2, and you have a local Llama model accessible via a REST API on localhost:11434. The API is OpenAI-compatible, so any app built for OpenAI can switch to Ollama with a one-line change. Ollama handles quantization, memory management, and GPU acceleration automatically. It is the de facto standard for local LLM integration in developer projects.",
    "desc_b": "LM Studio is a desktop application for running LLMs locally with a polished GUI. It includes a model browser that connects directly to Hugging Face, letting you search and download any GGUF-format model without command-line work. The built-in chat interface looks like a consumer AI chat app. LM Studio also includes a local server mode exposing an OpenAI-compatible API. Not open-source, but free for personal use.",
    "choose_a": [
      "You are building apps or scripts that need local LLM access via API",
      "You prefer CLI workflows and want minimal overhead",
      "You care about open-source and community support",
      "You need the API to run as a persistent background service",
      "You want the largest community of tutorials and integrations"
    ],
    "choose_b": [
      "You want a chat interface without writing any code",
      "You want to browse and try models from Hugging Face with a GUI",
      "You are evaluating many models visually before integrating them",
      "You want to compare models side-by-side in a visual interface",
      "You are new to local LLMs and want guided model discovery"
    ],
    "sections": [
      {
        "id": "performance",
        "title": "Performance: Same Models, Similar Speed",
        "content": "Ollama and LM Studio both use llama.cpp or similar quantized inference engines under the hood and both support Metal GPU acceleration on Apple Silicon. For the same model and quantization level, performance is essentially identical. The practical difference: Ollama's API handles concurrent requests better for multi-user scenarios, while LM Studio is optimized for single-user interactive chat."
      },
      {
        "id": "model-selection",
        "title": "Model Selection: Curated Library vs Hugging Face",
        "content": "Ollama maintains its own curated library with optimized versions of popular models. This makes discovery easy but limits you to what Ollama has packaged. LM Studio connects directly to Hugging Face, giving access to thousands of GGUF models including fine-tunes and research variants not on Ollama's list. If you need a specific fine-tuned model from Hugging Face, LM Studio is easier. If you want the top 20 most popular models with zero configuration, Ollama is faster."
      }
    ],
    "faqs": [
      {"q": "Is LM Studio better than Ollama?", "a": "Neither is objectively better. LM Studio is better for non-technical users who want a GUI and for exploring models from Hugging Face. Ollama is better for developers integrating local LLMs into applications. Both deliver comparable performance on the same hardware."},
      {"q": "Can I use both Ollama and LM Studio?", "a": "Yes. Many developers use LM Studio for personal exploration (testing new models) and Ollama for app integration. They can run simultaneously on different ports."},
      {"q": "Does Ollama have a GUI?", "a": "Ollama is CLI-only, but several third-party GUIs work with its API, most notably Open WebUI (25k+ GitHub stars), which provides a ChatGPT-like interface for Ollama models."},
      {"q": "Which supports more models?", "a": "LM Studio has access to more models via Hugging Face (thousands of GGUF models). Ollama has 100+ curated optimized models covering all major ones. For most use cases, both have what you need."},
      {"q": "Is Ollama open source?", "a": "Yes, Ollama is fully open-source under the MIT license with 174k+ GitHub stars. LM Studio is proprietary but free for personal use."}
    ],
    "related_compares": [
      {"slug": "ollama-vs-llama-cpp", "title": "Ollama vs llama.cpp", "desc": "Compare Ollama with the underlying inference engine"},
      {"slug": "ollama-vs-gpt4all", "title": "Ollama vs GPT4All", "desc": "Another popular local LLM desktop option"},
      {"slug": "vllm-vs-ollama", "title": "vLLM vs Ollama", "desc": "When to scale up from Ollama to vLLM"}
    ]
  },
  {
    "slug": "langchain-vs-dspy",
    "title": "LangChain vs DSPy",
    "tool_a_id": "langchain",
    "tool_b_id": "dspy",
    "intro": "LangChain and DSPy represent two fundamentally different approaches to building LLM applications. LangChain is imperative: you write explicit chains and prompts, controlling every step. DSPy is declarative: you write what you want to achieve and let the framework optimize how to get there, automatically tuning prompts through a compile step. Both have strong GitHub communities, but they attract very different developers. This comparison explains when each approach is the right choice.",
    "verdict": "Choose LangChain if you need a production-ready framework with broad integrations and want explicit control over prompts. Choose DSPy if prompt quality is critical, you have a labeled evaluation set, and you want the framework to find better prompts than you would write by hand. DSPy is higher investment upfront; LangChain gets you to production faster.",
    "table": [
      {"feature": "Programming model", "a": "Imperative (you write the prompts)", "b": "Declarative (compiler writes the prompts)", "winner": ""},
      {"feature": "GitHub Stars", "a": "140k+", "b": "22k+", "winner": "a"},
      {"feature": "Learning curve", "a": "Medium (many abstractions)", "b": "High (new mental model)", "winner": "a"},
      {"feature": "Prompt optimization", "a": "Manual", "b": "Automatic (BootstrapFewShot, MIPRO)", "winner": "b"},
      {"feature": "Evaluation-driven", "a": "Optional", "b": "Required (needs labeled examples)", "winner": ""},
      {"feature": "Integrations", "a": "100+ integrations (industry standard)", "b": "40+ LLM providers", "winner": "a"},
      {"feature": "Production deployments", "a": "Industry standard", "b": "Research + growing production use", "winner": "a"},
      {"feature": "RAG support", "a": "Built-in (LCEL, retrievers)", "b": "RAG optimizers available", "winner": ""},
      {"feature": "Multi-agent", "a": "Via LangGraph", "b": "Via multi-step programs", "winner": ""},
      {"feature": "Reproducibility", "a": "Manual (you control prompts)", "b": "High (compiled programs versioned)", "winner": "b"}
    ],
    "desc_a": "LangChain (140k+ GitHub stars) is the most widely deployed framework for building LLM applications. It provides chains for multi-step pipelines, agents with tool use, retrievers for RAG, memory management, and integrations with 100+ LLM providers and vector stores. The LangChain Expression Language (LCEL) lets you compose pipelines declaratively while keeping full prompt control. LangChain's breadth is its biggest asset and its biggest liability: the API surface is large.",
    "desc_b": "DSPy (22k+ GitHub stars, from Stanford NLP) treats prompt engineering as a compilation problem. Instead of writing prompts manually, you define your task as a program with typed input/output signatures, then run a compilation step that automatically finds optimal prompts through few-shot learning and optimization algorithms. DSPy programs are deterministic, versioned, and testable. The key requirement: you need a labeled evaluation set for the optimizer to work.",
    "choose_a": [
      "You need to ship to production quickly with broad integrations",
      "You are building chatbots, agents, or RAG systems with well-known patterns",
      "Your team is already familiar with LangChain",
      "You need the largest ecosystem of tutorials and community help",
      "You prefer explicit control over every part of your LLM pipeline"
    ],
    "choose_b": [
      "Prompt quality is the bottleneck and you have evaluation examples",
      "You are building classification, extraction, or structured generation tasks",
      "You want to eliminate prompt brittleness from model updates",
      "You are willing to invest in the new declarative programming model",
      "You want compiled, versioned, testable LLM programs"
    ],
    "sections": [
      {
        "id": "philosophy",
        "title": "Imperative vs Declarative: The Core Difference",
        "content": "In LangChain, you write explicit instructions for every step of your pipeline. You control the prompt template, the chain logic, and the output parsing. In DSPy, you define signatures that describe what goes in and what comes out, then run the optimizer. The optimizer tries many prompt strategies against your evaluation set and finds the one that maximizes your metric. Control is better when you know exactly what you want. Optimization is better when you need to hit a performance target and are not sure which prompt strategy works best."
      },
      {
        "id": "evaluation",
        "title": "DSPy's Requirement: You Need Labeled Examples",
        "content": "DSPy's optimizer is only as good as your evaluation function and labeled data. You need 20-100 labeled examples before DSPy can start optimizing. For teams without this infrastructure, LangChain is faster to adopt. For teams that already do LLM evaluation, DSPy fits naturally since your evaluation set becomes the input to optimization. The investment pays off when you are iterating on the same task repeatedly and want prompts to improve automatically as models evolve."
      }
    ],
    "faqs": [
      {"q": "Is DSPy better than LangChain?", "a": "For well-defined NLP tasks (classification, extraction, structured generation), DSPy's optimized prompts typically outperform hand-written LangChain prompts on quality metrics. For flexible production applications with many integrations, LangChain is more practical. They optimize for different goals: DSPy for quality, LangChain for ecosystem and velocity."},
      {"q": "Can I use DSPy with LangChain?", "a": "Yes, they are composable. A common pattern: use DSPy to optimize your core reasoning modules, then wrap them in LangChain for retrieval, memory, and tool use. DSPy modules can be called from LangChain chains."},
      {"q": "Does DSPy work with local models?", "a": "Yes, DSPy supports local models via Ollama, vLLM, and other OpenAI-compatible endpoints. Optimization works with any model, though smaller models may produce lower-quality compiled programs."},
      {"q": "What is DSPy's compile step?", "a": "DSPy's compile step (optimization) takes your program, evaluation set, and a metric function, then runs multiple prompt strategies through a search algorithm to find the combination that maximizes your metric. The result is a compiled program with baked-in examples and instructions."},
      {"q": "Is LangChain still worth learning in 2026?", "a": "Yes. LangChain remains the most widely deployed LLM framework. LangGraph (built on LangChain) is increasingly the standard for production agentic systems. DSPy is worth learning alongside LangChain for the optimization concepts, even if you continue using LangChain for most projects."}
    ],
    "related_compares": [
      {"slug": "langchain-vs-llamaindex", "title": "LangChain vs LlamaIndex", "desc": "Compare the two most popular LLM frameworks"},
      {"slug": "langchain-vs-haystack", "title": "LangChain vs Haystack", "desc": "Compare for enterprise NLP pipelines"},
      {"slug": "dspy-vs-langchain", "title": "DSPy vs LangChain", "desc": "Declarative vs imperative LLM programming"}
    ]
  }
]

added = 0
for entry in new_entries:
    if entry['slug'] in existing_slugs:
        print(f'  [skip] {entry["slug"]}: 已存在')
    else:
        data.append(entry)
        existing_slugs.add(entry['slug'])
        added += 1
        print(f'  [ok] {entry["slug"]}')

with open(os.path.join(BASE, 'compare_data.json'), 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'完成：添加 {added} 个条目，compare_data.json 现有 {len(data)} 个')

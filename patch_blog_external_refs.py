#!/usr/bin/env python3
"""
为 5 篇核心博客添加「📚 References & Data Sources」外部引用区块。
插入位置：FAQ 段落后、Related Articles 段落前。
"""

import os

BASE = os.path.dirname(os.path.abspath(__file__))
BLOG = os.path.join(BASE, "blog")

# 5 篇目标博客 + 各自的外部引用 HTML
REFS = {

    "claude-vs-chatgpt-vs-gemini-2026.html": """
      <!-- 📚 External References & Data Sources -->
      <h2 id="references">📚 References & Data Sources</h2>
      <ul>
        <li><a href="https://chat.lmsys.org" target="_blank" rel="noopener">LMSys Chatbot Arena</a> — Live leaderboard ranking 100+ LLMs via 2M+ human preference votes. Claude 3.5 Sonnet and GPT-4o consistently rank in the top 5.</li>
        <li><a href="https://www.swebench.com" target="_blank" rel="noopener">SWE-bench Verified</a> — The standard benchmark for evaluating AI coding agents on real-world GitHub issues. Claude 3.5 Sonnet leads with 49.0% resolved.</li>
        <li><a href="https://docs.anthropic.com/en/docs/about-claude/models" target="_blank" rel="noopener">Anthropic Model Card: Claude</a> — Official model specifications, capabilities, safety evaluations, and usage guidelines.</li>
        <li><a href="https://platform.openai.com/docs/models" target="_blank" rel="noopener">OpenAI Model Documentation</a> — Official GPT-4o and o-series model specs, pricing, rate limits, and API reference.</li>
        <li><a href="https://ai.google.dev/gemini-api/docs/models" target="_blank" rel="noopener">Google Gemini Model Guide</a> — Official Gemini 1.5 Pro / Flash model capabilities, context window details, and API integration docs.</li>
        <li><a href="https://artificialanalysis.ai" target="_blank" rel="noopener">Artificial Analysis</a> — Independent, continuously-updated benchmark comparing LLM quality, speed, and pricing across all major providers.</li>
      </ul>
""",

    "ai-agent-frameworks-guide-2025.html": """
      <!-- 📚 External References & Data Sources -->
      <h2 id="references">📚 References & Data Sources</h2>
      <ul>
        <li><a href="https://arxiv.org/abs/2308.08155" target="_blank" rel="noopener">AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation</a> — Microsoft Research paper introducing the multi-agent conversation framework (arXiv 2308.08155).</li>
        <li><a href="https://arxiv.org/abs/2308.00352" target="_blank" rel="noopener">MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework</a> — ICLR 2024 paper on the multi-role agent architecture for software development.</li>
        <li><a href="https://arxiv.org/abs/2402.01680" target="_blank" rel="noopener">SWE-Agent: Agent-Computer Interfaces for Automated Software Engineering</a> — Princeton research on enabling agents to use real development tools.</li>
        <li><a href="https://docs.crewai.com" target="_blank" rel="noopener">CrewAI Official Documentation</a> — Production guides, tool integrations, and deployment patterns for role-based multi-agent systems.</li>
        <li><a href="https://langchain-ai.github.io/langgraph/" target="_blank" rel="noopener">LangGraph Documentation</a> — Official docs for building stateful, multi-actor agent workflows with LangChain's graph framework.</li>
        <li><a href="https://github.com/microsoft/autogen" target="_blank" rel="noopener">Microsoft AutoGen GitHub</a> — Reference implementation, sample code, and community contributions for the AutoGen agent framework.</li>
      </ul>
""",

    "build-production-rag-pipeline.html": """
      <!-- 📚 External References & Data Sources -->
      <h2 id="references">📚 References & Data Sources</h2>
      <ul>
        <li><a href="https://arxiv.org/abs/2005.11401" target="_blank" rel="noopener">Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks</a> — The seminal RAG paper by Lewis et al. (Meta AI, 2020) introducing the retrieval-augmented generation paradigm.</li>
        <li><a href="https://arxiv.org/abs/2312.10997" target="_blank" rel="noopener">RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval</a> — Stanford research on hierarchical document summarization for improved multi-hop retrieval.</li>
        <li><a href="https://milvus.io/docs" target="_blank" rel="noopener">Milvus Vector Database Documentation</a> — Official docs covering index types (IVF_FLAT, HNSW, DiskANN), performance tuning, and production deployment.</li>
        <li><a href="https://www.pinecone.io/learn/" target="_blank" rel="noopener">Pinecone Learning Center</a> — Comprehensive guides on embedding strategies, chunking methods, metadata filtering, and hybrid search patterns.</li>
        <li><a href="https://docs.llamaindex.ai" target="_blank" rel="noopener">LlamaIndex Documentation</a> — Official framework docs covering 40+ retrieval strategies, data connectors, and agentic RAG patterns.</li>
        <li><a href="https://huggingface.co/spaces/mteb/leaderboard" target="_blank" rel="noopener">MTEB Leaderboard (Hugging Face)</a> — Massive Text Embedding Benchmark ranking 200+ embedding models across classification, clustering, and retrieval tasks.</li>
      </ul>
""",

    "open-source-llms-guide-2026.html": """
      <!-- 📚 External References & Data Sources -->
      <h2 id="references">📚 References & Data Sources</h2>
      <ul>
        <li><a href="https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard" target="_blank" rel="noopener">Open LLM Leaderboard (Hugging Face)</a> — Standardized evaluation of open-source LLMs on MMLU, ARC, HellaSwag, TruthfulQA, and other benchmarks.</li>
        <li><a href="https://llm-stats.com" target="_blank" rel="noopener">LLM Stats</a> — Up-to-date comparisons of open-source models: parameter counts, context windows, VRAM requirements, and provider availability.</li>
        <li><a href="https://github.com/ggerganov/llama.cpp" target="_blank" rel="noopener">llama.cpp GitHub</a> — The core inference engine powering most local LLM deployments. Readme contains supported models, quantization formats, and hardware requirements.</li>
        <li><a href="https://ollama.com/library" target="_blank" rel="noopener">Ollama Model Library</a> — Official catalog of ready-to-run models with quantization levels, sizes, and pull commands for local inference.</li>
        <li><a href="https://arxiv.org/abs/2407.21783" target="_blank" rel="noopener">Llama 3 Herd of Models (Meta AI, 2024)</a> — The technical report for the Llama 3 family, detailing architecture, training data composition, and benchmark performance.</li>
        <li><a href="https://crfm.stanford.edu/helm/latest/" target="_blank" rel="noopener">HELM: Holistic Evaluation of Language Models (Stanford CRFM)</a> — Comprehensive, multi-metric evaluation framework that assesses LLMs across 42 scenarios including fairness, bias, and robustness.</li>
      </ul>
""",

    "vllm-vs-ollama-production.html": """
      <!-- 📚 External References & Data Sources -->
      <h2 id="references">📚 References & Data Sources</h2>
      <ul>
        <li><a href="https://arxiv.org/abs/2309.06180" target="_blank" rel="noopener">Efficient Memory Management for Large Language Model Serving with PagedAttention</a> — The vLLM paper (SOSP 2023) introducing PagedAttention, the core innovation behind vLLM's 10-20x throughput gains.</li>
        <li><a href="https://docs.vllm.ai" target="_blank" rel="noopener">vLLM Official Documentation</a> — Production deployment guides, supported model list, quantization options, and performance tuning parameters.</li>
        <li><a href="https://ollama.com/blog" target="_blank" rel="noopener">Ollama Engineering Blog</a> — Technical deep-dives on model quantization, GPU scheduling, and infrastructure from the Ollama team.</li>
        <li><a href="https://github.com/ggerganov/llama.cpp" target="_blank" rel="noopener">llama.cpp GitHub</a> — The inference backend that powers Ollama. Readme documents all quantization formats (Q4_K_M to Q8_0) and their memory-vs-quality tradeoffs.</li>
        <li><a href="https://artificialanalysis.ai/providers" target="_blank" rel="noopener">Artificial Analysis: LLM Provider Benchmarks</a> — Independent throughput, latency, and cost-per-token comparisons across 20+ inference providers including vLLM-based deployments.</li>
        <li><a href="https://github.com/vllm-project/vllm/tree/main/benchmarks" target="_blank" rel="noopener">vLLM Benchmark Suite</a> — Official benchmark scripts for measuring serving throughput, latency distribution, and GPU utilization under load.</li>
      </ul>
""",

}

# 插入锚点：在 FAQ section 之后的第一个 </ul> 结束标签后插入
# 更稳定的方式：在 "Related Articles" 的 <h3 之前插入
INSERT_BEFORE = '        <h3>Related Articles</h3>'

changed = 0
for fname in ["claude-vs-chatgpt-vs-gemini-2026.html",
              "ai-agent-frameworks-guide-2025.html",
              "build-production-rag-pipeline.html",
              "open-source-llms-guide-2026.html",
              "vllm-vs-ollama-production.html"]:
    ref_html = REFS[fname]
    fpath = os.path.join(BLOG, fname)
    with open(fpath, encoding="utf-8") as f:
        html = f.read()

    if "📚 References & Data Sources" in html:
        print(f"[SKIP] {fname} — 已有外部引用区块")
        continue

    if INSERT_BEFORE not in html:
        print(f"[WARN] {fname} — 未找到 'Related Articles' 锚点，手动检查")
        continue

    new_html = html.replace(INSERT_BEFORE, ref_html + "\n" + INSERT_BEFORE)
    if new_html == html:
        print(f"[SKIP] {fname} — 替换未生效")
        continue

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(new_html)
    changed += 1
    print(f"[OK] {fname} — 已添加外部引用区块")

print(f"\n完成: {changed} 篇博客已更新")

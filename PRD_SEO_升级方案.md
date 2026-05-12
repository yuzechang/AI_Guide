# AI_Guide — 工具列表站升级为程序化 SEO 内容站
## 产品需求文档（PRD）v1.0

**文档状态**: Draft  
**版本**: 1.0  
**日期**: 2026-05-08  
**项目**: yuzec.com / AI_Guide  
**目标**: 将"AI工具导航列表站"升级为"AI工具内容型SEO站（Programmatic SEO架构）"

---

## 目录

1. [文档概览](#1-文档概览)
2. [现状分析](#2-现状分析)
3. [用户价值分析](#3-用户价值分析)
4. [产品架构设计](#4-产品架构设计)
5. [功能模块详细说明](#5-功能模块详细说明)
6. [技术实现方案](#6-技术实现方案)
7. [SEO 关键词策略](#7-seo-关键词策略)
8. [页面 SEO 标准模板](#8-页面-seo-标准模板)
9. [变现策略](#9-变现策略)
10. [外链建设策略](#10-外链建设策略)
11. [迭代路线图](#11-迭代路线图)
12. [监控指标体系](#12-监控指标体系)
13. [风险与约束](#13-风险与约束)
14. [快速启动核对清单](#14-快速启动核对清单)

---

## 1. 文档概览

### 1.1 文档目标

本 PRD 为 AI_Guide 从"工具列表展示站"升级为"程序化 SEO 内容站（Programmatic SEO Site）"的完整产品需求文档。升级的核心动因是：当前站点页面数量极少（thin content），无法被 Google 大量收录，无法排名长尾关键词，因此无法产生 AdSense 曝光收益和 Affiliate 点击转化。

本文档描述的不是一次功能迭代，而是一次产品架构重建。

### 1.2 成功指标

| 目标 | 指标 | 当前基线 | 目标值 | 度量窗口 |
|------|------|---------|--------|---------|
| Google 收录数量 | Google Search Console 已收录 URL 数 | <10 页 | ≥200 页 | 上线后 90 天 |
| 自然搜索流量 | 月 Organic Sessions | 预估 <100 | ≥5,000 | 上线后 180 天 |
| 关键词排名 | 排名前 50 的长尾关键词数量 | 0 | ≥50 | 上线后 180 天 |
| AdSense 收益 | 月 RPM / 月总收益 | $0 | $50（启动期） | 上线后 90 天 |
| Affiliate 转化 | 月 Affiliate 点击数 | 0 | ≥500 | 上线后 120 天 |
| 页面生成效率 | 新增一个工具的页面生成耗时 | 手动（N/A） | <30 秒（自动化） | 系统上线即达 |

---

## 2. 现状分析

### 2.1 当前问题

| 问题 | 说明 |
|------|------|
| Thin Content | 全站仅为工具列表页，缺乏深度内容 |
| 无独立 SEO 页面 | 每个工具没有独立的可索引详情页 |
| JS 渲染依赖 | 内容依赖 data.json + 客户端 JS 渲染，Google 爬虫不友好 |
| sitemap 过浅 | 仅有少量页面，未覆盖工具详情 |
| 无内容型页面 | 缺乏教程、FAQ、对比等内容 |

### 2.2 现有资产（可利用）

- **300 个工具数据** (`data.json`)，3 个分类：ai-tools / skill / agent
- **已生成 303 个 tools/*.html 页面**（Jinja2 模板 + generate.py）
- **现有模板框架**：`templates/tool_detail.j2` 含 Schema.org、FAQ、面包屑
- **域名权重**：yuzec.com 已有基础 SEO 配置（robots.txt、sitemap.xml）
- **GitHub Actions 基础设施**：update_stars.py 自动更新 stars

---

## 3. 用户价值分析

### 3.1 目标用户群画像

**主要用户 — "找工具的开发者" (Developer-Seeker)**

描述：25-40 岁，软件工程师、独立开发者或技术产品经理，在 Google 搜索特定 AI 工具的名称、用途、对比或使用教程。

核心搜索意图：
- `Cursor vs GitHub Copilot`
- `Claude Code how to use`
- `best AI coding assistant 2025`
- `Windsurf IDE review`
- `open source AI agent framework`

**次要用户 — "学习 AI 工具的内容创作者" (Creator-Learner)**

描述：内容创作者、YouTuber、Newsletter 作者，需要了解某工具的核心功能和 Prompt 示例，在自己的内容中引用或测评。

### 3.2 核心使用场景

| 场景 | 用户动作 | 站点响应 |
|------|---------|---------|
| 工具调研 | Google 搜索 "Cursor IDE review" | 命中 /tools/cursor.html 详情页，提供完整评测 |
| 工具对比 | Google 搜索 "Cursor vs Copilot" | 命中对比页面（Phase 2） |
| 使用教程 | Google 搜索 "how to use Claude Code" | 命中 AI 开发工具专区页面，包含步骤 + Prompt 示例 |
| 工具发现 | 直接访问首页 | 通过分类导航和热门榜单发现感兴趣工具 |
| Affiliate 点击 | 在详情页看到官方链接 | 点击 Affiliate 链接跳转，产生转化 |

---

## 4. 产品架构设计

### 4.1 信息架构

```
AI_Guide 站点
├── / (首页)
│   ├── Hero 区（主关键词植入：Best AI Tools Directory 2026）
│   ├── 分类导航区（Coding / Writing / Image / Agents / Skill Frameworks）
│   ├── 热门工具区（Top 10，按 GitHub Stars 排序）
│   └── 最新工具区（按 updatedAt 排序）
│
├── /tools/ (工具详情页集合，核心 SEO 资产)
│   ├── /tools/cursor.html          ← 手写增强页
│   ├── /tools/claude-code.html     ← 手写增强页
│   ├── /tools/chatgpt.html         ← 手写增强页
│   ├── /tools/langchain.html       ← 手写增强页
│   └── ... (300 个 data.json 条目自动生成)
│
├── /category/ (分类聚合页，Phase 2)
│   ├── /category/ai-coding-tools.html
│   ├── /category/ai-writing-tools.html
│   ├── /category/ai-image-tools.html
│   └── /category/ai-agent-frameworks.html
│
├── /compare/ (竞品对比页，Phase 2)
│   └── /compare/cursor-vs-github-copilot.html
│
├── /blog/ (教程/内容文章，Phase 3)
│   └── /blog/how-to-use-claude-code.html
│
├── sitemap.xml      ← 自动生成，覆盖所有 /tools/
├── robots.txt
└── data.json        ← 单一数据源（Single Source of Truth）
```

### 4.2 data.json 字段扩展计划

现有字段：`id, name, nameCn, category, githubUrl, stars, starsLabel, descEn, descCn, tags`

**Phase 1 新增字段**（必须，支撑内容生成）：

```json
{
  "slug": "cursor",
  "website": "https://cursor.sh",
  "affiliateUrl": "https://cursor.sh?ref=ainav",
  "license": "Proprietary",
  "pricing": "freemium",
  "pricingDetail": "免费版可用，Pro $20/月",
  "features": ["AI 代码补全（Tab 键触发）", "Chat 面板对话式编程", "多文件上下文理解"],
  "useCases": ["前端开发者快速搭建 React 组件", "后端开发者生成 CRUD 接口"],
  "pros": ["上手极快，兼容 VS Code 插件", "多文件编辑能力强"],
  "cons": ["Pro 版月费较高", "大型项目 context 窗口有限"],
  "faqs": [
    {"q": "Cursor 和 GitHub Copilot 有什么区别？", "a": "Cursor 是独立编辑器..."},
    {"q": "Cursor 免费版有哪些限制？", "a": "免费版每月提供 50 次..."},
    {"q": "Cursor 支持哪些编程语言？", "a": "基于 VS Code，支持所有主流语言..."}
  ],
  "updatedAt": "2026-05-01",
  "featured": true,
  "seoKeywords": ["Cursor IDE", "Cursor AI editor", "AI code editor"]
}
```

---

## 5. 功能模块详细说明

### 模块 1：工具详情页自动生成【P0 · 核心】

**优先级**: P0 — 整个升级方案的核心，不完成此模块则其他模块无意义。

**功能描述**:
- 基于 data.json 为每个工具生成独立静态 HTML 文件
- 输出路径：`/tools/{id}.html`
- 使用 Jinja2（已有）或 Nunjucks 模板渲染
- **现状**：已有 303 个生成页面 + generate.py + tool_detail.j2，需升级质量

**验收标准**:
```
- /tools/ 目录下 N 个工具对应 N 个 .html 文件
- 每个文件含完整 <head>：title、description、canonical
- 每个文件含 JSON-LD schema（SoftwareApplication + FAQPage + BreadcrumbList）
- 每个文件含工具名称、简介（≥100字）、功能列表、FAQ（≥3条）
- 每个文件的 Affiliate 链接指向 affiliateUrl 字段（无则降级到 githubUrl）
- 生成全量页面耗时 <30 秒
```

---

### 模块 2：首页结构重建【P0】

**优先级**: P0 — 首页是 Google 收录的锚点，也是用户第一落点。

**功能描述**:
- Hero 区覆盖主关键词（"Best Open Source AI Tools Directory 2026"）
- 分类导航区：AI Coding / AI Writing / AI Image / AI Agents / Skill Frameworks
- 热门工具区：取 stars 排名前 10
- 最新工具区：取 updatedAt 最新 10 条
- 搜索框：前端实时搜索（基于 data.json，Fuse.js 模糊搜索）

**验收标准**:
```
- Hero 区 H1 标签包含核心关键词
- 热门工具区展示 10 条，按 stars 降序
- 最新工具区展示 10 条，按 updatedAt 降序
- 搜索框输入后 <500ms 内展示匹配结果
- 搜索结果点击跳转到对应 /tools/ 详情页
- PageSpeed Insights 移动端评分 ≥85
```

---

### 模块 3：全站 SEO 规范【P0】

**每页必须包含的 SEO 元素**：

| 元素 | 标准 |
|------|------|
| `<title>` | 50-60 字符，含工具名和核心关键词 |
| `<meta description>` | 150-160 字符，含主要关键词，CTA 动词结尾 |
| `<link rel="canonical">` | 指向本页面绝对 URL |
| Open Graph | og:title / og:description / og:image / og:url |
| Twitter Card | twitter:card / twitter:title / twitter:description |
| JSON-LD Schema | SoftwareApplication + FAQPage + BreadcrumbList |
| H 标签层级 | 页面唯一一个 `<h1>` |
| 图片 alt | 所有图片非空 alt |

---

### 模块 4：sitemap 自动生成【P0】

**功能描述**:
- 自动生成 sitemap.xml，覆盖：首页 + 所有 /tools/ 页面 + /category/ 页面
- 每个 URL 包含 `<lastmod>`（取 updatedAt 字段）和 `<changefreq>`（weekly）
- 与 GitHub Actions 联动，每次 data.json 变更自动重建
- 提交到 Google Search Console

**验收标准**:
```
- sitemap.xml 存在于根目录
- 包含首页 URL
- 包含所有 /tools/{id}.html 的 URL
- 每个 URL 含 <loc>、<lastmod>、<changefreq>
- sitemap.xml 通过 XML validator 验证无错误
```

---

### 模块 5：AI 开发工具专区内容增强【P1】

**目标工具**: Cursor、Claude Code、OpenAI API、Windsurf、v0（Vercel）、Bolt

**每页增加内容**：

| 内容项 | 字数建议 |
|--------|---------|
| 使用教程（分步骤） | 500-800 字 |
| Prompt 示例（≥3条） | 每条 50-100 字 |
| 开发场景说明 | 200-300 字 |
| API / 工作流说明 | 300-500 字 |

**验收标准**:
```
- 6 个指定工具详情页正文字数 ≥1,500 字
- 包含"使用教程"模块，步骤 ≥3 步
- 包含"Prompt 示例"模块，示例 ≥3 条
- 包含"API / 工作流说明"模块
```

---

### 模块 6：分类聚合页【P1】

- 为每个 category 生成聚合页 `/category/{category-slug}.html`
- 页面 H1 / title 优化为分类关键词（如 "Best AI Coding Tools 2026"）
- 展示该分类下所有工具卡片（名称、简介、链接）
- 被 sitemap.xml 覆盖

---

### 模块 7：GitHub Actions 自动化部署【P0】

**触发条件**：Push 到 main 分支，或 data.json 有变更

**执行流程**：
1. Checkout 仓库
2. 安装依赖（Python 3 + Jinja2）
3. 运行 `generate.py --force`（生成所有 /tools/ HTML）
4. 运行 sitemap 生成脚本
5. 提交生成文件回仓库 → Vercel 自动部署

---

## 6. 技术实现方案

### 6.1 技术栈

| 组件 | 技术选型 | 理由 |
|------|---------|------|
| 生成脚本 | Python 3 + Jinja2 | 已有基础，维护成本低 |
| 模板 | Jinja2 (`.j2`) | 已有 `tool_detail.j2`，继续扩展 |
| 前端搜索 | Fuse.js（CDN） | 纯前端模糊搜索，无需后端 |
| 部署 | Vercel（主）+ GitHub Pages（备） | 静态站最佳支持，自动 HTTPS |
| CI/CD | GitHub Actions | 免费，与仓库集成紧密 |

### 6.2 目录结构（目标态）

```
ai_guide/
├── .github/
│   └── workflows/
│       ├── update_stars.yml        # 已有：每周更新 stars
│       └── build.yml               # 新增：内容变更时重建页面
├── templates/
│   ├── tool_detail.j2              # 已有，继续升级
│   ├── category.j2                 # 新增：分类聚合页模板
│   └── index.j2                    # 新增：首页模板（可选）
├── scripts/
│   ├── update_stars.py             # 已有
│   └── generate_sitemap.py         # 新增：独立 sitemap 生成
├── assets/
│   └── shared.css                  # 已有
├── tools/                          # 自动生成（不手动编辑）
├── category/                       # 新增，自动生成
├── data.json                       # 单一数据源，扩展字段
├── generate.py                     # 已有，继续升级
├── index.html                      # 手动维护（或 Phase 2 改为模板生成）
├── sitemap.xml                     # 自动生成
└── robots.txt
```

### 6.3 robots.txt 标准内容

```
User-agent: *
Allow: /
Disallow: /src/
Disallow: /node_modules/

Sitemap: https://yuzec.com/sitemap.xml
```

---

## 7. SEO 关键词策略

### 7.1 核心关键词（Head Keywords）

站点最高流量天花板，通过内容集群权重积累自然攀升：

| 关键词 | 月搜索量（估算） | KD | 搜索意图 | 优先级 |
|--------|-----------------|-----|----------|--------|
| best AI tools 2025 | 40,000+ | 72 | 商业调研 | 高 |
| AI tools list | 22,000+ | 65 | 信息型 | 高 |
| AI tools for developers | 8,000+ | 58 | 商业调研 | 高 |
| open source AI tools | 6,000+ | 45 | 信息型 | **极高**（竞争低）|
| AI agent tools | 5,500+ | 52 | 商业调研 | 高 |
| AI coding assistant | 9,000+ | 61 | 商业调研 | 高 |

> **策略**：开源工具导航站天然占据 "open source AI tools" 差异化定位，KD 显著低于通用词，建议作为突破口。

### 7.2 分类关键词

#### Coding / Developer 分类

| 关键词 | 月搜索量 | KD | 对应落地页 |
|--------|---------|-----|-----------|
| AI coding tools | 9,000 | 61 | /category/coding |
| AI code review tool | 3,500 | 44 | /category/coding |
| AI code completion tool | 4,200 | 50 | /category/coding |
| AI pair programmer | 2,800 | 38 | /category/coding |

#### Writing / Content 分类

| 关键词 | 月搜索量 | KD | 对应落地页 |
|--------|---------|-----|-----------|
| AI writing assistant | 14,000 | 66 | /category/writing |
| AI content generator | 8,500 | 63 | /category/writing |
| free AI writing tool | 6,800 | 55 | /category/writing |

#### AI Agents 分类

| 关键词 | 月搜索量 | KD | 对应落地页 |
|--------|---------|-----|-----------|
| AI agent framework | 4,200 | 42 | /category/agents |
| open source AI agent | 2,100 | 35 | /category/agents |
| LLM agent framework | 1,800 | 33 | /category/agents |

#### Skill Frameworks 分类（差异化机会最大）

| 关键词 | 月搜索量 | KD | 备注 |
|--------|---------|-----|------|
| AI skill framework | 900 | 22 | **竞争极低，优先占位** |
| LLM prompting framework | 1,200 | 28 | 技术开发者词 |
| AI agent skill library | 600 | 18 | 几乎无竞争 |

### 7.3 工具级长尾关键词模板（Programmatic SEO 核心）

每个工具详情页围绕以下 5 种模板生成标题，单工具页可自然覆盖 20-50 个长尾词：

| 模板类型 | URL Slug | Title 示例 |
|---------|---------|-----------|
| 评测/Review | `/tools/{slug}` | `Cursor Review 2025: Features, Pricing & Verdict` |
| 使用教程 | `/tools/{slug}#guide` | `How to Use Cursor: A Complete Guide for Developers` |
| 替代品搜索 | `/tools/{slug}#alternatives` | `Best Cursor Alternatives in 2025 (Free & Paid)` |
| 竞品对比 | `/compare/{slug}-vs-{competitor}` | `Cursor vs GitHub Copilot: Which Is Better in 2025?` |
| 定价页 | `/tools/{slug}#pricing` | `Cursor Pricing 2025: Free Plan, Pro & Enterprise Costs` |

**低竞争变体**：
- `{Tool Name} for {use case}` — 如 "Cursor for Python developers"
- `Is {Tool Name} free?` — 直接触达免费工具搜索流量
- `{Tool Name} GitHub` — 开源工具高价值词

### 7.4 FAQ 关键词策略（覆盖 People Also Ask）

每个工具详情页 FAQ 区块（使用 FAQPage Schema），覆盖最常见 PAA 问题：

| FAQ 模板 | 触发的 PAA 类词 | 回答长度 |
|---------|--------------|---------|
| Is {Tool Name} free to use? | "{tool} free" / "{tool} free plan" | 60-80 字 |
| What can {Tool Name} do? | "{tool} features" / "what is {tool}" | 100-120 字 |
| How does {Tool Name} compare to {Competitor}? | "{tool} vs {competitor}" | 80-100 字 |
| Is {Tool Name} safe to use? | "{tool} safe" / "{tool} privacy" | 60 字 |
| Does {Tool Name} have an API? | "{tool} API" / "{tool} integration" | 60 字 |
| What are the best alternatives to {Tool Name}? | "{tool} alternatives" | 80 字 |
| Who makes {Tool Name}? | "{tool} company" | 40-60 字 |
| What programming languages does {Tool Name} support? | 适用 Coding 类工具 | 列举语言列表 |

### 7.5 内容集群（Topic Cluster）规划

```
yuzec.com — 权重流向示意

[支柱页 Pillar Pages]
├── / 首页                    ← "best AI tools" 系列词
├── /category/coding          ← AI Coding 集群入口
├── /category/agents          ← AI Agents 集群入口
└── /category/skill-frameworks ← 差异化定位，竞争最低

[集群内容 Cluster Pages — 以 Coding 为例]
/category/coding
    ├── /tools/cursor           ← 工具评测 + FAQ
    ├── /compare/cursor-vs-copilot  ← 对比页
    ├── /tools/cursor#alternatives  ← 替代品
    └── /blog/best-ai-coding-tools  ← 类目博文（Phase 3）

[内链规则]
分类页 → 工具详情页（传递权重）
工具详情页 → 相关工具页（双向）
工具详情页 → 对比页（补充语境）
```

**优先建设顺序**：
1. **0-3 个月**：300 工具详情页质量提升 + 分类支柱页
2. **3-6 个月**：高搜索量工具的 Alternatives 区块 + vs 对比页
3. **6-12 个月**：编辑型博客内容，建立主题权威

---

## 8. 页面 SEO 标准模板

### 8.1 工具详情页 Title 模板

```
{Tool Name} Review 2025 – Features, Pricing & Alternatives | AI_Guide
```
> 规则：不超过 60 字符，核心词靠前，品牌词放末尾

**分类变体**：
```
# 开源工具（突出差异化）
{Tool Name}: Open Source {Category} AI Tool – How It Works 2025 | AI_Guide

# 主流商业工具
{Tool Name} Review 2025: Honest Pros, Cons & Pricing | AI_Guide
```

### 8.2 工具详情页 Meta Description 模板

```
Discover what {Tool Name} does, how it works, and whether it's worth it in 2025.
Compare pricing, features & top alternatives. Find the right AI tool now.
```
> 规则：不超过 155 字符，包含主要关键词，CTA 动词结尾

**分类变体**：
```
# Coding 类
{Tool Name} is an AI coding tool for {language/use case}. Compare features,
pricing & open-source alternatives. See if it fits your dev workflow.

# Agent 类
{Tool Name} is an {autonomous/LLM-powered} AI agent framework. Explore
capabilities, setup guide & how it compares to AutoGPT and LangChain.
```

### 8.3 JSON-LD SoftwareApplication Schema 模板

```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "{Tool Name}",
  "description": "{工具的一句话描述，100字以内}",
  "url": "https://yuzec.com/tools/{tool-slug}",
  "applicationCategory": "DeveloperApplication",
  "operatingSystem": "Web, Windows, macOS, Linux",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD",
    "description": "Free plan available. Pro plan starts at $XX/month."
  },
  "author": {
    "@type": "Organization",
    "name": "{Tool Developer/Company Name}",
    "url": "{Tool Official Website}"
  },
  "dateModified": "2025-{MM}-{DD}",
  "keywords": "{Tool Name}, AI tool, {category}",
  "featureList": ["{Feature 1}", "{Feature 2}", "{Feature 3}"],
  "license": "{MIT/Apache 2.0/Proprietary}"
}
```

**配套 FAQPage Schema**：
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Is {Tool Name} free to use?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "{简洁回答，60-80字}"
      }
    }
  ]
}
```

> **注意**：`aggregateRating` 字段只在收集了真实评分数据后才加入，否则不填，防止 Google 人工审核降权。

### 8.4 OpenGraph 标签模板

```html
<meta property="og:type" content="website" />
<meta property="og:site_name" content="AI_Guide – yuzec.com" />
<meta property="og:title" content="{Tool Name} Review 2025 – Features, Pricing & Alternatives" />
<meta property="og:description" content="Discover what {Tool Name} does, how it works..." />
<meta property="og:url" content="https://yuzec.com/tools/{tool-slug}" />
<meta property="og:image" content="https://yuzec.com/assets/og-default.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{Tool Name} Review 2025 – Features, Pricing & Alternatives" />
<meta name="twitter:description" content="Is {Tool Name} the right AI tool for you? ..." />
<meta name="twitter:image" content="https://yuzec.com/assets/og-default.png" />
```

### 8.5 H 标签层级规范

```
h1: {Tool Name} — {tagline}                （页面唯一，含主关键词）
  h2: What is {Tool Name}?                  （工具简介区）
  h2: Key Features                          （功能列表）
  h2: Use Cases                             （使用场景）
  h2: Pros & Cons                           （优缺点）
  h2: Pricing                               （定价）
  h2: Frequently Asked Questions            （FAQ，触发 FAQ Rich Result）
  h2: Similar Tools                         （相关推荐）
```

---

## 9. 变现策略

### 9.1 AdSense 广告位规划

**原则**：不影响 Core Web Vitals，不降低 CLS 分数。

| 广告位置 | 广告格式 | 页面类型 | 预期 RPM | 注意事项 |
|---------|---------|---------|---------|---------|
| 功能列表下方（内容中段） | 响应式 | 工具详情页 | $3-8 | 用户基本信息获取后的自然停顿点 |
| 侧边栏顶部（sticky） | 300x250 | 工具详情页（桌面端） | $4-10 | 仅桌面端，移动端隐藏 |
| FAQ 区块上方 | 响应式 336x280 | 工具详情页 | $1.5-2.2 | 阅读深度最高位置 |
| 内容末尾（相关工具前） | 970x90 横幅 | 工具详情页 | $2-3 | 已读完内容的高意图状态 |
| 首页分区间隔 | 响应式 | 首页 | $1-3 | 热门区和最新区之间 |

**CLS 防抖处理**（必须实现）：
```css
.adsense-container {
  min-height: 250px;
  width: 100%;
}
```

**申请时机**：Phase 1 完成后，≥50 个内容页、每页 ≥800 字时申请，通过率最高。

**预期收益估算**：

| 流量规模 | 月 PV | 预期 RPM | 月 AdSense 收益 |
|---------|-------|---------|---------------|
| 早期 | 5,000 | $2-4 | $10-20 |
| 成长期 | 50,000 | $4-8 | $200-400 |
| 成熟期 | 500,000 | $6-12 | $3,000-6,000 |

### 9.2 Affiliate 变现规划

**逻辑**：每个工具"访问官网"按钮指向 affiliateUrl（含 ref 参数），用户注册/付费后获得佣金。

**高价值 Affiliate 项目**：

| 项目 | 佣金结构 | 适配度 |
|------|---------|--------|
| Cursor | $20/订阅用户 | **极高**，Coding 类核心工具 |
| OpenAI API | 收入分成 20%（90天） | **极高**，覆盖大多数工具 |
| Claude (Anthropic) | CPA（通过合作伙伴计划） | **极高**，Agents 类工具 |
| GitHub Copilot | $10/月活用户 | 高，Coding 分类 |
| Jasper AI | 25-30% 经常性佣金 | 高，Writing 分类 |
| Copy.ai | 45% 首年 | 中，Writing 分类 |
| DigitalOcean | $25/每次注册 | 中，AI 工具部署相关 |

**Affiliate 链接嵌入位置**：

| 位置 | 预期转化率 | 说明 |
|------|-----------|------|
| 工具卡片 Hero CTA 按钮 | 2-5% | 用户明确有访问意图 |
| Alternatives 页面推荐卡片 | 4-8% | 用户主动比较替代方案，付费意愿最强 |
| 对比表格"立即使用"列 | 3-7% | 处于决策终点 |
| 正文上下文链接 | 1-3% | 每篇文章不超过 3 个 |

**CTA 文案优化**：

| 不推荐 | 推荐 | 理由 |
|-------|------|------|
| Click Here | Try {Tool Name} Free | 明确行动 + 降低摩擦 |
| Visit Website | Start Building with {Tool Name} | 面向用户目标 |
| Learn More | See {Tool Name} Pricing | 匹配商业调研意图 |

**合规要求（必须执行）**：
- 含 Affiliate 链接页面必须有 Disclosure 声明
- 所有 Affiliate 链接带 `rel="nofollow sponsored"` 属性
- 不在 AdSense 页面旁堆砌 Affiliate 链接

**Affiliate Disclosure 标准文案**：
```
Disclosure: This page contains affiliate links. If you click and purchase,
we may earn a commission at no extra cost to you. This helps support
AI_Guide's operations. We only recommend tools we believe are genuinely useful.
```

---

## 10. 外链建设策略

### 策略 1：工具 GitHub 仓库反向曝光

**操作路径**：
1. 向工具 GitHub README.md 提交 PR，在 "Resources" 章节增加 yuzec.com 收录链接
2. 在工具 Issues/Discussions 提交目录收录请求

**预期产出**：每月 10-15 个有效外链，DA 40-70，持续性强

---

### 策略 2：Awesome List 提交

**操作路径**：
1. 搜索 GitHub 上 `awesome-ai-tools`、`awesome-llm`、`awesome-agents` 等仓库
2. 提交 PR 将 yuzec.com 作为"AI Tool Directories"资源添加
3. 重点目标：`awesome-chatgpt-prompts`（47k stars）等高权重仓库

**预期产出**：每月 5-8 个高质量外链，来源 DA 95+（github.com）

---

### 策略 3：工具开发者合作

**操作路径**：
1. 找到工具官网 "Featured In" 或 "Press" 页面
2. 发邮件请求对方在官网添加 yuzec.com 链接
3. 一旦有 GA 数据可提供流量证明

**预期产出**：成功率约 15-25%，每月 3-5 个来自 SaaS 官网的外链

---

### 策略 4：原创数据报告数字公关

**操作路径**：
1. 制作"2025 State of Open Source AI Tools"报告（基于 300+ 工具数据库）
2. 统计洞察：哪个分类工具增长最快、License 分布、Stars 增长趋势等
3. 发布为独立落地页，向 HackerNews、Dev.to、InfoQ 投递

**预期产出**：一次成功可带来 15-40 个高质量外链，效果持续 3-6 个月

---

### 策略 5：社区分发（Reddit / HackerNews / Product Hunt）

**操作路径**：
1. Reddit r/MachineLearning、r/artificial 等社区分享工具发现和对比分析
2. HackerNews "Show HN" 发布工具数据库或对比分析帖
3. Product Hunt 发布 AI_Guide Launch，获取初始外链和社区关注

**规则**：必须提供真实价值，先建立社区参与记录再分享

---

## 11. 迭代路线图

### Phase 1 — SEO 基础建设（目标：4 周完成）✅ 已完成

**核心目标**：建立可被 Google 收录的内容站基础设施

| 任务 | 优先级 | 预估工时 | 状态 |
|------|--------|---------|------|
| 扩展 data.json 字段（website, affiliateUrl, license, faqs, pros, cons） | P0 | 8h | ✅ |
| 补全 20-50 个核心工具的完整数据 | P0 | 16h | ✅ 35条 |
| 升级 tool_detail.j2 模板（添加 pros/cons 对比、定价、Affiliate CTA） | P0 | 8h | ✅ |
| 升级 generate.py（支持新字段、增量更新、日志输出） | P0 | 6h | ✅ |
| 独立 sitemap 生成脚本（覆盖 /tools/ + /category/） | P0 | 3h | ✅ |
| 配置 GitHub Actions 自动化 build.yml | P0 | 3h | ✅ |
| 首页 Hero 区 SEO 优化（H1 含核心关键词） | P0 | 4h | ✅ |
| 提交 sitemap 到 Google Search Console | P0 | 1h | ⏳ 需手动操作 |
| 申请 Google AdSense（≥50 页后） | P1 | 2h | ✅ pub-2761695780807828 已申请 |

**Phase 1 完成标准**：
- Google Search Console 显示 sitemap 已处理，URL ≥50
- 生成全量页面 <30 秒
- GitHub Actions 可正常触发并提交生成文件

---

### Phase 2 — 内容深度 + 变现启动（第 5-10 周）✅ 大部分完成

**核心目标**：提升内容质量，覆盖高价值关键词，开启变现

| 任务 | 优先级 | 预估工时 | 状态 |
|------|--------|---------|------|
| AI 开发工具专区 6 个页面内容增强（≥1500 字/页） | P1 | 24h | ✅ cursor/claude-code/chatgpt/vllm 等已完成 |
| 生成分类聚合页（/category/） | P1 | 8h | ✅ ai-tools/skill/agent 3个页面 |
| 嵌入 Affiliate 链接 + Disclosure 声明 | P1 | 4h | ✅ affiliateUrl + rel=nofollow sponsored |
| 添加 AdSense 代码（审核通过后） | P1 | 3h | ⏳ 待 AdSense 审核通过后植入 |
| 添加相关工具推荐模块（内链建设） | P1 | 6h | ❌ 未完成 |
| 工具数据扩充至 100+ 条完整字段 | P1 | 16h | ⚠️ 当前 81/300，未达 100 |
| FAQ Schema 验证（Google Rich Results Test） | P2 | 4h | ❌ 未完成 |

**Phase 2 完成标准**：
- Google Search Console 已收录 URL ≥100
- AdSense 已获批并有展示数据
- 月自然搜索流量 ≥1,000 Sessions

---

### Phase 3 — 规模化内容 + 精细化变现（第 11-24 周）⏳ 进行中

| 任务 | 优先级 | 状态 |
|------|--------|------|
| 工具数据扩充至 200+ 条完整字段 | P1 | ⚠️ 当前 81/300 |
| 工具对比页 /compare/ 生成逻辑（50 个高流量词） | P1 | ⚠️ 当前 3/50 |
| Markdown 博客文章系统（20 篇使用教程） | P2 | ❌ 未开始 |
| AdSense 广告位 A/B 测试 | P2 | ❌ 待审核通过 |
| 接入 Hotjar / Clarity 用户行为分析 | P2 | ❌ 未开始 |
| 申请高佣金 Affiliate 项目（Jasper、Surfer SEO 等） | P2 | ❌ 未开始 |
| Newsletter 订阅系统 | P3 | ❌ 未开始 |

**Phase 3 成功信号**：
- 月自然搜索流量 ≥5,000 Sessions
- ≥50 个关键词排名 Google 前 50
- AdSense 月收益 ≥$50
- Affiliate 月点击 ≥500

---

## 12. 监控指标体系

### 指标 1：自然搜索点击量（非品牌词）

- **工具**：Google Search Console → 效果 → 过滤"不包含品牌词"
- **频率**：每周
- **预警**：连续 2 周点击量下降 >10%，触发排查

### 指标 2：索引覆盖率

- **工具**：Google Search Console → 覆盖率报告
- **计算**：已索引页面数 / Sitemap 提交页面数
- **目标**：300 个详情页，90 天内索引率 ≥85%

### 指标 3：Core Web Vitals

| 指标 | 移动端目标 | 桌面端目标 |
|-----|---------|---------|
| LCP | < 2.5 秒 | < 2.0 秒 |
| INP | < 200 毫秒 | < 150 毫秒 |
| CLS | < 0.1 | < 0.05 |

### 指标 4：关键词排名分布

- **工具**：Google Search Console 位置报告（免费）或 Ahrefs（付费）
- **关注区间**：Top 3（维护）、4-10（优化优先区）、11-20（低垂果实）
- **频率**：每周核心词，每月全量

### 指标 5：外链获取速度

- **工具**：Ahrefs Site Explorer 或 Moz Link Explorer
- **核心**：引用域名数月环比增长率、新增 DA 40+ 外链数量
- **目标**：每月净增引用域名 20-50 个

---

## 13. 风险与约束

### 13.1 主要风险

| 风险 | 可能性 | 影响 | 缓解措施 |
|------|-------|------|---------|
| Google Helpful Content 政策打压批量生成内容 | 中 | 高 | 每页 ≥800 字，FAQ ≥3 条，信息唯一性保证；避免纯 AI 生成不经校审 |
| AdSense 申请被拒 | 中 | 中 | 申请时 ≥50 页内容，有隐私政策页，Affiliate Disclosure 已添加 |
| Affiliate 链接被 Google 识别为 Spam | 低 | 高 | 严格执行 `rel="nofollow sponsored"`，不堆砌链接 |
| 工具数据更新不及时导致内容失效 | 高 | 中 | 季度数据审查机制，updatedAt 字段强制更新 |
| Core Web Vitals 分数低（广告 CLS） | 中 | 中 | 广告容器预留最小高度，不使用插页广告 |

### 13.2 技术约束

- **无服务端**：所有功能必须在静态 HTML + 客户端 JS 内实现
- **无数据库**：data.json 是唯一数据源，建议工具数量 ≤500 条
- **构建时间**：GitHub Actions 免费计划 2,000 分钟/月，300 页构建 <2 分钟
- **Vercel 免费计划**：100GB 带宽/月，静态站通常足够

### 13.3 显式排除（不做的事）

| 排除项 | 原因 | 重新考虑的条件 |
|-------|------|-------------|
| 动态渲染（Next.js / Nuxt.js） | 违反"纯静态"约束 | 月流量 >100K 且 SEO 瓶颈确认来自渲染层 |
| 用户注册 / 收藏功能 | 需要后端 | 验证强烈用户需求后单独立项 |
| 实时价格爬取 | 法律风险 + 技术复杂度 | Phase 3 评估 |
| 多语言（中文）SEO 版本 | 分散 SEO 权重，当前首要目标为英文 | 英文站 DA ≥20 后评估 |
| 工具评分系统 | 无后端支持；伪造评分有 Google 惩罚风险 | 接入 G2 等第三方数据源 |

---

## 14. 快速启动核对清单

Phase 1 上线前必须核对：

**内容**
- [ ] data.json 包含 ≥50 个工具，每个工具含完整 slug、description、features、faqs 字段
- [ ] 每个工具 description 字段 ≥100 字，且无重复内容

**SEO**
- [ ] 每个生成页面 title 唯一，长度 50-60 字符
- [ ] 每个生成页面 meta description 唯一，长度 150-160 字符
- [ ] 每个生成页面包含 canonical URL（绝对路径）
- [ ] 每个生成页面包含 JSON-LD SoftwareApplication schema
- [ ] 每个生成页面包含 FAQPage schema（≥3 条 FAQ）
- [ ] sitemap.xml 覆盖所有 /tools/ 页面
- [ ] robots.txt 正确配置，/tools/ 路径未被 Disallow

**合规**
- [ ] 含 Affiliate 链接页面有 Disclosure 声明
- [ ] 所有 Affiliate 链接带 `rel="nofollow sponsored"`
- [ ] 隐私政策页面存在（privacy-policy.html）

**自动化**
- [ ] GitHub Actions workflow 可正常触发
- [ ] 生成脚本包含错误日志输出
- [ ] 校验脚本在 CI 中作为必须通过的 step

**性能**
- [ ] 广告容器预留最小高度（防 CLS）
- [ ] 首页 PageSpeed Insights 移动端评分 ≥85
- [ ] 工具详情页 PageSpeed Insights 移动端评分 ≥80

---

*文档版本 v1.0 | 适用阶段：产品上线前 SEO 规划 + 上线后前 12 个月执行参考*

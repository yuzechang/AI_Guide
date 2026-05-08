# ⚡ AI Guide — AI Tools Navigation

> 精选 300+ 开源 AI 工具导航站，涵盖 AI Tools、Skill 框架、Agent 智能体三大类，数据每周自动更新。
>
> A curated directory of 300+ open-source AI tools, skill frameworks and agent systems. Auto-updated weekly via GitHub Actions.

🌐 **在线访问** → [yuzechang.github.io/AI_Guide](https://yuzechang.github.io/AI_Guide/)

---

## 📦 收录范围

| 分类 | 数量 | 说明 |
|------|------|------|
| 🤖 **AI Tools** | 100 | 面向终端用户的 AI 应用：图像生成、语音、本地 LLM、编程助手等 |
| ⚙️ **Skill** | 100 | 开发者构建 AI 应用的框架/库：向量数据库、推理引擎、微调框架等 |
| 🚀 **Agent** | 100 | 自主智能体框架：多 Agent 编排、浏览器控制、代码智能体等 |

代表项目：`AutoGPT` `llama.cpp` `LangChain` `vLLM` `Dify` `Browser Use` `CrewAI` `Transformers` 等。

---

## ✨ 功能特性

- **中英双语**：一键切换界面语言
- **实时搜索**：按名称、描述、标签秒级过滤
- **分类筛选**：Tab 快速切换三大类别
- **标签浏览**：按 `llm` `rag` `code` 等标签聚合
- **自动更新**：GitHub Actions 每周刷新 Star 数，页面展示「X 天前更新」
- **Google AdSense**：预留 4 处广告位，替换 ID 即可启用
- **SEO 完整**：Meta Tags / Open Graph / Schema.org / sitemap.xml / robots.txt
- **无需服务器**：双轨加载（`data.js` 内嵌 + `fetch` 动态），直接双击打开即用

---

## 🚀 快速开始

### 本地预览

```bash
# 直接打开（无需服务器）
open index.html

# 或启动本地 HTTP 服务
python3 -m http.server 8080
# 浏览器访问 http://localhost:8080
```

### 部署到 GitHub Pages

1. Fork 本仓库
2. 进入 **Settings → Pages**，Source 选 `main` 分支 `/ (root)`
3. 约 1 分钟后访问 `https://<你的用户名>.github.io/AI_Guide/`

### 启用 Star 自动更新

进入 **Settings → Actions → General → Workflow permissions**，选择 **Read and write permissions** 并保存。之后每周一凌晨 3 点（UTC）自动刷新所有仓库的 Star 数。

也可在 Actions 页面手动触发：**Actions → Auto-update GitHub Stars → Run workflow**。

---

## 🔧 自定义配置

### 替换域名

```bash
# 全局替换（将 yourdomain.com 换成你的真实域名）
grep -rl "yourdomain.com" . | xargs sed -i '' 's/yourdomain.com/你的域名/g'
```

### 启用 Google AdSense

在 `index.html` 中搜索 `ADSENSE_`，取消对应注释块，填入你的 Publisher ID 和 Slot ID：

| 广告位 | 位置 | 尺寸 |
|--------|------|------|
| `ADSENSE_BANNER_TOP_728x90` | Hero 区下方 | 728×90 |
| `ADSENSE_INFEED` | 工具卡片流中 | In-feed |
| `ADSENSE_SIDEBAR_300x250` | 侧边栏 | 300×250 |
| `ADSENSE_FOOTER_320x100` | 页脚 | 320×100 |

### 新增工具

在 `data.json` 的 `tools` 数组末尾追加：

```json
{
  "id": "unique-id",
  "name": "Tool Name",
  "nameCn": "工具中文名",
  "category": "ai-tools",
  "githubUrl": "https://github.com/owner/repo",
  "stars": 5000,
  "starsLabel": "5k+",
  "descEn": "One-line English description",
  "descCn": "一句话中文简介",
  "tags": ["tag1", "tag2", "tag3"]
}
```

修改 `data.json` 后执行以下命令同步到 `data.js`：

```bash
python3 -c "
import json
with open('data.json') as f: d = json.load(f)
with open('data.js', 'w') as f: f.write('window.TOOLS_DATA = ' + json.dumps(d, ensure_ascii=False) + ';')
print('data.js updated,', len(d['tools']), 'tools')
"
```

---

## 📁 文件结构

```
AI_Guide/
├── index.html          # 主页面（CSS + JS 内嵌，单文件）
├── data.json           # 工具数据（由 update_stars.py 自动维护）
├── data.js             # 同上，供直接打开 HTML 时加载
├── robots.txt          # 搜索引擎爬虫配置
├── sitemap.xml         # 站点地图
└── scripts/
    └── update_stars.py # GitHub API 自动刷新 Star 数
```

`.github/workflows/update-stars.yml` 定义每周自动执行的 Actions 任务。

---

## 🛠 技术栈

- **前端**：原生 HTML / CSS / JavaScript，零依赖，无构建步骤
- **数据**：JSON 静态文件，GitHub Actions 自动刷新
- **SEO**：Schema.org JSON-LD、hreflang、Open Graph、Twitter Card
- **部署**：任意静态托管平台（GitHub Pages / Vercel / Netlify）

---

## 📄 License

MIT © [yuzechang](https://github.com/yuzechang)

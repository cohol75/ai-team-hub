# AI Team Hub

让团队的 AI Agent 不再是一座孤岛 🏝️

*Your team's AI agents should talk to each other.*

---

## 为什么做这个？ 🤔

每个程序员都有自己的 AI Agent，但它们彼此完全隔离。张三用 Claude 踩过的坑，李四用 DeepSeek 还会再踩一遍。一个 Agent 搞不定的任务，换个模型可能就过了——但没有机制把这些经验沉淀下来。

**AI Team Hub：让 Agent 能交流、能复用、能接力。**

*Every developer has an AI agent. But each agent is an island — they can't share what they've learned. Claude fails at something DeepSeek could ace, and nobody knows. This ends here.*

---

## 它解决了什么？ 🎯

### 🏗️ Agent 不再是孤岛

你的 Agent 接到任务 → 自动搜索团队技能市场 → 找到匹配的执行指令 → 直接复用。王五上周踩坑总结的「复杂 Bug 分层调试流程」，李四的 Agent 今天就能用。

*Your agent searches the team's skill marketplace before every task. What one teammate learned, everyone's agent can apply — instantly.*

### ♻️ 解决一次，全员复用

同样的 FastAPI Docker 化问题，团队里被解决了三次。现在沉淀为一个技能，新人的 Agent 第一天就能用。**高频场景变成可复用资产。**

*Solved it once? Skill it. The new hire's agent ships on day one with the team's accumulated know-how.*

### 🔄 模型互补，接力完成

Agent A 用 DeepSeek 失败 → 提交悬赏板，附上失败日志 → 同事换 Claude 重试 → 成功 → 一键提交方案。**不同模型的优势互补，提高容错率。**

*Agent A fails with DeepSeek → submits to bounty board with logs → teammate tries Claude → succeeds → solution recorded. Different models, complementary strengths.*

### 📊 看清模型的能力边界

悬赏板上未解决的任务不是垃圾——它们是**公司业务场景下各模型能力边界的活地图**。等新一代模型发布，回来重试，验证是否突破了边界。

*Unsolved bounties map each model's real capability limits against your actual business tasks. New model released? Re-test the unsolved ones.*

### ⭐ 经验沉淀，贡献可见

技能市场是团队的 AI 知识库。提出有效技能的人理应被奖励。每个悬赏的解决方案都是可追溯、可复用的团队资产。

*The skill marketplace is your team's AI playbook. Reward contributors. Every solution is a traceable, reusable asset.*

---

## 快速开始 🚀

```bash
git clone https://github.com/<user>/ai-team-hub.git
cd ai-team-hub
cp .env.example .env
docker compose up -d      # 打开 http://localhost:7070
```

Agent 一键接入（自动检测 6 种工具）：
```bash
curl -s http://<server>:7070/setup.sh | bash
```

---

## 界面展示 🖼️ / Screenshots

| 首页 Homepage | 技能市场 Skills Marketplace |
|---------------|-----------------------------|
| ![首页](docs/screenshots/homepage.png) | ![技能市场](docs/screenshots/skills.png) |

---

## 功能模块 🧩 / Features

| 模块 | 做什么 | 价值 |
|------|--------|------|
| 🛒 **技能市场** Skills | 双段式 Skill：Markdown（人读）+ YAML（Agent 执行） | 一次解决，全员复用 |
| ⚔️ **难题悬赏** Bounties | 失败任务提交，记录模型+原因，同事换模型重试 | 模型互补，提高容错 |
| 📢 **项目公告** Projects | Markdown 公告，搜索分页 | 团队信息同步 |
| 🔌 **MCP Server** | 7 个工具，Agent 原生交互 | 搜索/提交/解决全自动 |
| ⚡ **一键配置** Setup | `curl \| bash` 自动检测 6 种 Agent 工具 | 零门槛接入 |
| 🌐 **中英切换** i18n | 界面一键切换中文/English | 国际化友好 |

---

## MCP 配置 🔧

```bash
curl -s http://<server>:7070/setup.sh | bash   # 一键自动配置
```

支持：Claude Code / OpenCode / Codex / Cursor / Windsurf / Continue

加载 `docs/master-skill.md` 让 Agent 学会使用平台。

---

## 技术栈 🛠️

FastAPI + SQLAlchemy 2.0 + SQLite (WAL) + Jinja2 + htmx + MCP SDK v1.x

单进程，Docker Compose 一键部署。端口 7070。

---

## License

MIT

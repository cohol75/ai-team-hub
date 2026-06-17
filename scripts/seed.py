"""Seed the database with demo data."""
import subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import delete
from app.database import engine, Base, Session
from app.models import Project, Skill, Problem, ProblemAttempt

Base.metadata.create_all(bind=engine)

from app.database import SessionLocal
db = SessionLocal()

# Clean existing
db.execute(delete(ProblemAttempt))
db.execute(delete(Problem))
db.execute(delete(Skill))
db.execute(delete(Project))
db.flush()

# Projects
projects = [
    Project(title="团队 Claude Code 使用规范 v1.0", content="## 背景\n\n为了统一团队使用 Claude Code 的方式...\n\n## 规范\n\n1. 所有代码变更前先运行 `claude review`\n2. 提交 PR 前检查是否有可用 Skill\n3. 遇到难题及时提交到悬赏板", author="张三"),
    Project(title="新项目脚手架工具发布", content="## 发布说明\n\n之前用 Claude Code 帮我们生成了新项目脚手架 `project-scaffold`。\n\n### 功能\n- 自动生成 FastAPI 项目结构\n- 内置 Dockerfile 和 docker-compose\n- 预设 CI/CD 模板", author="李四"),
    Project(title="本周技能分享会通知", content="## 时间\n本周五 16:00\n\n## 内容\n每人分享一个这周新学的 Claude Code 技巧，整理成 Skill 发布到技能市场。", author="张三"),
]
db.add_all(projects)

# Skills
skills = [
    Skill(
        name="python-code-review",
        title="Python 代码审查助手",
        human_section="## 功能描述\n\n对 Python 代码进行自动审查。检查 PEP 8 风格、类型安全、异常处理和性能。\n\n### 使用方式\n将代码粘贴到对话中，调用此技能即可。",
        agent_section="""name: python-code-review
version: "1.0.0"
description: "Automated Python code review"
category: code-review
model: claude-opus-4
model_provider: anthropic
tags:
  - python
  - review
steps:
  - step: 1
    action: analyze
    instruction: "Read Python code and identify style, type safety, and performance issues"
    expected_output: "List of issues with severity levels"
  - step: 2
    action: generate
    instruction: "Generate fix suggestions with code examples for each issue"
    expected_output: "Markdown report with fixes"
""",
        model_used="claude-opus-4",
        model_provider="anthropic",
        category="code-review",
        tags="python,review,lint",
        author="李四",
    ),
    Skill(
        name="fastapi-docker-deploy",
        title="FastAPI 项目 Docker 化部署",
        human_section="## 功能描述\n\n将 FastAPI 项目自动化 Docker 化，生成 Dockerfile、docker-compose.yml 和 nginx 配置。\n\n### 前置条件\n- 项目使用 requirements.txt 管理依赖\n- Python 3.10+",
        agent_section="""name: fastapi-docker-deploy
version: "1.0.0"
description: "Generate Docker deployment configs for FastAPI projects"
category: deployment
model: claude-opus-4
model_provider: anthropic
tags:
  - fastapi
  - docker
  - deployment
steps:
  - step: 1
    action: analyze
    instruction: "Scan project structure: entry point, dependencies, port number"
    expected_output: "Project metadata: entry module, python version, port"
  - step: 2
    action: generate
    instruction: "Generate optimized Dockerfile with multi-stage build"
    expected_output: "Dockerfile content"
  - step: 3
    action: generate
    instruction: "Generate docker-compose.yml with service and volume configs"
    expected_output: "docker-compose.yml content"
""",
        model_used="claude-opus-4",
        model_provider="anthropic",
        category="deployment",
        tags="fastapi,docker,deployment",
        author="张三",
    ),
    Skill(
        name="error-debugging-workflow",
        title="复杂 Bug 分层调试工作流",
        human_section="## 功能描述\n\n遇到复杂 Bug 时的系统化调试流程。从顶层现象到底层根因，逐步缩小范围。\n\n### 适用场景\n- 生产环境偶发 Bug\n- 分布式系统跨服务错误\n- 难以复现的问题",
        agent_section="""name: error-debugging-workflow
version: "1.0.0"
description: "Systematic debugging workflow for complex bugs"
category: debugging
model: deepseek-v3
model_provider: deepseek
tags:
  - debugging
  - workflow
  - troubleshooting
steps:
  - step: 1
    action: analyze
    instruction: "Gather all available error information: stack traces, logs, reproduction steps"
    expected_output: "Structured error summary"
  - step: 2
    action: analyze
    instruction: "Formulate 3-5 hypotheses ranked by likelihood"
    expected_output: "Hypothesis list with confidence scores"
  - step: 3
    action: execute
    command: "grep -r 'ERROR' logs/ | head -50"
    instruction: "Search logs for related error patterns"
    expected_output: "Filtered log entries matching error patterns"
""",
        model_used="deepseek-v3",
        model_provider="deepseek",
        category="debugging",
        tags="debugging,workflow,troubleshooting",
        author="王五",
    ),
]
db.add_all(skills)

# Problems
problems = [
    Problem(
        title="用 DeepSeek 无法正确生成 CI/CD 配置",
        original_task="## 任务描述\n\n需要为新项目生成 GitHub Actions CI/CD 配置。Python 项目，包含 lint、test、deploy 三个阶段。\n\n使用 DeepSeek V3 生成 3 次，YAML 缩进均出错。",
        processing_logs='[{"model": "deepseek-v3", "status": "failed", "result": "YAML indentation errors", "timestamp": "2026-06-17 09:30"}, {"model": "zhipu-glm-4", "status": "failed", "result": "Output truncated", "timestamp": "2026-06-17 09:45"}]',
        status="open",
        submitter="王五",
    ),
    Problem(
        title="Claude 无法正确识别图片中的表格数据",
        original_task="## 任务描述\n\n需要从 30 张扫描件中提取表格数据为 CSV。试了 Claude 的视觉功能，表格边界识别不准确，合并单元格处理错误。",
        processing_logs='[{"model": "claude-sonnet-4-6", "status": "failed", "result": "Table boundary detection incorrect on merged cells", "timestamp": "2026-06-16 14:20"}, {"model": "gpt-4o", "status": "failed", "result": "Hallucinated extra rows in empty areas", "timestamp": "2026-06-16 15:00"}]',
        status="open",
        submitter="李四",
    ),
    Problem(
        title="长文档翻译质量不稳定",
        original_task="## 任务描述\n\n翻译一篇 50 页的技术白皮书（中→英）。用 DeepSeek V3 分段翻译，前 10 页质量尚可，后面出现术语不一致和漏译。",
        processing_logs='[{"model": "deepseek-v3", "status": "failed", "result": "Term inconsistency after page 10, some paragraphs untranslated", "timestamp": "2026-06-15 11:00"}]',
        status="resolved",
        submitter="张三",
        resolver="李四",
        resolution="## 解决方案\n\n使用 Claude Opus 4 分段翻译 + 术语表约束：\n1. 先提取全文关键术语建立中英对照表\n2. 每段翻译时在 prompt 中传入术语表\n3. 翻译完成后用另一个 Claude 会话做一致性审查",
    ),
]
db.add_all(problems)
db.flush()

# Attempts on the resolved problem
attempts = [
    ProblemAttempt(
        problem_id=problems[2].id,
        solver="李四",
        model_used="claude-opus-4",
        approach="建立术语表约束 + 分段翻译，每段 prompt 都包含完整术语映射",
        result="翻译质量一致，术语统一，全部段落完整。成功。",
    ),
]
db.add_all(attempts)

db.commit()
db.close()

print("Seed data inserted:")
print(f"  Projects: {len(projects)}")
print(f"  Skills: {len(skills)}")
print(f"  Problems: {len(problems)} (1 resolved)")
print(f"  Attempts: {len(attempts)}")

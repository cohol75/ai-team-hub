"""Lightweight i18n — no external dependencies. Language via ?lang= query param or cookie."""

from fastapi import Request

LANG = {
    # ---- Layout ----
    "app_title": {"zh": "AI Team Hub", "en": "AI Team Hub"},
    "mcp_ready": {"zh": "MCP 已就绪", "en": "MCP Ready"},
    "copy_to_run": {"zh": "点击复制，终端执行", "en": "Click to copy, run in terminal"},
    "dry_run_hint": {"zh": "加 --dry-run 可预览", "en": "Add --dry-run to preview"},
    "lang_switch": {"zh": "English", "en": "中文"},

    # ---- Nav ----
    "nav_home": {"zh": "首页", "en": "Home"},
    "nav_collab": {"zh": "协作", "en": "Collaborate"},
    "nav_projects": {"zh": "项目公告", "en": "Projects"},
    "nav_skills": {"zh": "技能市场", "en": "Skills"},
    "nav_problems": {"zh": "难题悬赏", "en": "Problems"},

    "guide_title": {"zh": "使用指南", "en": "Usage Guide"},
    "guide_back": {"zh": "← 返回首页", "en": "← Back to Home"},

    # ---- Home ----
    "home_welcome": {"zh": "团队 AI 协作中心", "en": "Team AI Collaboration Hub"},
    "home_subtitle": {"zh": "发布项目、分享技能、悬赏难题，让团队 AI 能力持续积累。", "en": "Share projects, publish skills, bounty problems — grow your team's AI capabilities."},
    "home_projects": {"zh": "项目公告", "en": "Projects"},
    "home_skills": {"zh": "技能市场", "en": "Skills"},
    "home_problems": {"zh": "难题悬赏", "en": "Bounty Board"},
    "home_open_problems": {"zh": "开放难题", "en": "open problems"},
    "home_new_project": {"zh": "发布项目", "en": "New Project"},
    "home_new_skill": {"zh": "提交技能", "en": "New Skill"},
    "home_new_problem": {"zh": "提交难题", "en": "New Problem"},
    "home_view_all": {"zh": "查看全部", "en": "View All"},
    "home_recent_projects": {"zh": "最近项目", "en": "Recent Projects"},
    "home_recent_skills": {"zh": "最新技能", "en": "Recent Skills"},
    "home_no_projects": {"zh": "暂无项目公告", "en": "No projects yet"},
    "home_no_skills": {"zh": "暂无技能，去提交第一个", "en": "No skills yet, submit the first one"},
    "home_skills_count": {"zh": "个技能", "en": "skills"},
    "home_problems_count": {"zh": "个待解决的难题", "en": "open problems"},
    "home_tagline": {"zh": "团队协作平台 · 技能复用 · 难题众包", "en": "Team Collaboration · Skill Reuse · Crowdsourced Solutions"},
    "home_guide_title": {"zh": "如何用好 AI Team Hub？", "en": "How to Get the Most Out of AI Team Hub?"},
    "home_guide_link": {"zh": "了解详情 →", "en": "Learn More →"},

    # ---- Skills ----
    "skills_title": {"zh": "技能市场", "en": "Skill Marketplace"},
    "skills_my": {"zh": "我的技能", "en": "My Skills"},
    "skills_submit": {"zh": "+ 提交技能", "en": "+ Submit Skill"},
    "skills_search": {"zh": "搜索技能...", "en": "Search skills..."},
    "skills_all_categories": {"zh": "全部分类", "en": "All Categories"},
    "skills_guide_title": {"zh": "如何使用技能市场？", "en": "How to use the Skill Marketplace?"},
    "skills_guide_1": {"zh": "点击技能卡片右上角的 ☆ 收藏你需要的技能", "en": "Click the ☆ on skill cards to save skills you need"},
    "skills_guide_2": {"zh": "点击顶部「我的技能」只看已收藏", "en": "Click 'My Skills' to see only saved ones"},
    "skills_guide_3": {"zh": "配置 MCP 后，Agent 会自动搜索并使用你收藏的技能", "en": "After MCP setup, your agent will auto-search and use saved skills"},
    "skills_setup_mcp": {"zh": "一键配置 MCP：", "en": "One-liner MCP setup:"},
    "skills_copy_cmd": {"zh": "复制命令", "en": "Copy"},
    "skills_no_match": {"zh": "没有匹配的技能", "en": "No matching skills"},
    "skills_empty": {"zh": "暂无技能", "en": "No skills yet"},
    "skills_submit_first": {"zh": "提交第一个", "en": "submit the first one"},
    "skills_view_detail": {"zh": "查看详情 →", "en": "Details →"},
    "skills_my_count": {"zh": "个", "en": ""},
    "skills_copy_mcp_call": {"zh": "复制 MCP 调用参数", "en": "Copy MCP Call"},
    "skills_copy_names": {"zh": "复制名称列表", "en": "Copy Names"},
    "skills_agent_hint": {"zh": "告诉你的 Agent：调用 search_skills 时带上 names 参数，只搜索你选的技能。", "en": "Tell your agent: pass names to search_skills to only search your selected skills."},

    # ---- Skill Detail ----
    "skill_edit": {"zh": "编辑", "en": "Edit"},
    "skill_delete": {"zh": "删除", "en": "Delete"},
    "skill_my_skill": {"zh": "我的技能", "en": "My Skill"},
    "skill_author": {"zh": "作者", "en": "Author"},
    "skill_model": {"zh": "模型", "en": "Model"},
    "skill_category": {"zh": "分类", "en": "Category"},
    "skill_usage": {"zh": "使用说明", "en": "Usage Guide"},
    "skill_agent_section": {"zh": "Agent 执行指令", "en": "Agent Instructions"},
    "skill_copy": {"zh": "复制", "en": "Copy"},
    "skill_back": {"zh": "← 返回技能市场", "en": "← Back to Skills"},

    # ---- Skill Form ----
    "skill_form_title_new": {"zh": "提交新技能", "en": "Submit New Skill"},
    "skill_form_title_edit": {"zh": "编辑技能", "en": "Edit Skill"},
    "skill_form_human_label": {"zh": "使用说明（给人看，Markdown）", "en": "Usage Guide (for humans, Markdown)"},
    "skill_form_human_placeholder": {"zh": "## 功能描述\n...\n\n### 适用场景\n...\n\n### 前置条件\n...\n\n### 注意事项\n...\n\n### 示例输出\n...", "en": "## What it does\n...\n\n### When to use\n...\n\n### Prerequisites\n...\n\n### Notes\n...\n\n### Example output\n..."},
    "skill_form_human_hint": {"zh": "请尽量详细！包含：解决什么问题、适用场景、前置条件、注意事项、示例输出。不要一句话概括。", "en": "Be detailed! Include: what problem it solves, when to use, prerequisites, notes, example output. Don't summarize in one sentence."},
    "skill_form_agent_label": {"zh": "Agent 执行指令（YAML 格式）", "en": "Agent Instructions (YAML format)"},
    "skill_form_title_field": {"zh": "技能标题", "en": "Skill Title"},
    "skill_form_model": {"zh": "使用的模型", "en": "Model Used"},
    "skill_form_model_placeholder": {"zh": "如 claude-opus-4", "en": "e.g. claude-opus-4"},
    "skill_form_author": {"zh": "提交者", "en": "Author"},
    "skill_form_tags": {"zh": "标签（逗号分隔）", "en": "Tags (comma separated)"},
    "skill_form_submit": {"zh": "提交技能", "en": "Submit Skill"},
    "skill_form_cancel": {"zh": "取消", "en": "Cancel"},

    # ---- Problems ----
    "problems_title": {"zh": "难题悬赏", "en": "Bounty Board"},
    "problems_submit": {"zh": "+ 提交难题", "en": "+ Submit Problem"},
    "problems_search": {"zh": "搜索难题...", "en": "Search problems..."},
    "problems_all_status": {"zh": "全部状态", "en": "All Status"},
    "problems_open": {"zh": "开放", "en": "Open"},
    "problems_in_progress": {"zh": "处理中", "en": "In Progress"},
    "problems_resolved": {"zh": "已解决", "en": "Resolved"},
    "problems_submitter": {"zh": "提交者", "en": "Submitter"},
    "problems_attempts": {"zh": "次尝试", "en": " attempts"},
    "problems_no_match": {"zh": "没有匹配的难题", "en": "No matching problems"},
    "problems_empty": {"zh": "暂无难题", "en": "No problems yet"},
    "problems_submit_first": {"zh": "提交第一个", "en": "submit the first one"},
    "problems_view_detail": {"zh": "查看详情 →", "en": "Details →"},

    # ---- Problem Detail ----
    "problem_solver": {"zh": "解决者", "en": "Solver"},
    "problem_failed_records": {"zh": "失败记录 — 已尝试的模型 / API", "en": "Failed Attempts — Models / APIs Tried"},
    "problem_failed_badge": {"zh": "失败", "en": "Failed"},
    "problem_original_task": {"zh": "原始任务要求", "en": "Original Task"},
    "problem_attempts_title": {"zh": "同事尝试", "en": "Teammate Attempts"},
    "problem_approach": {"zh": "方法", "en": "Approach"},
    "problem_result": {"zh": "结果", "en": "Result"},
    "problem_resolution_title": {"zh": "✅ 解决方案", "en": "✅ Solution"},
    "problem_how_to_takeover": {"zh": "💡 如何接手这个任务？", "en": "💡 How to Take Over?"},
    "problem_takeover_1": {"zh": "复制上面的「原始任务要求」，粘贴给你的 Agent（Claude Code / OpenCode 等）", "en": "Copy the 'Original Task' above and paste it to your agent"},
    "problem_takeover_2": {"zh": "换一个模型试试 — 上面列出的模型都已经失败了，换不同的可能有惊喜", "en": "Try a DIFFERENT model — the ones listed above already failed"},
    "problem_takeover_3": {"zh": "执行完成后，在下面填写你的尝试记录，帮助后续同事了解进展", "en": "After trying, record your attempt below to help colleagues"},
    "problem_takeover_4": {"zh": "如果成功了，在底部「标记已解决」并附上解决方案", "en": "If successful, mark it resolved with your solution"},
    "problem_submit_attempt": {"zh": "📝 提交尝试记录", "en": "📝 Submit Attempt"},
    "problem_your_name": {"zh": "你的名字", "en": "Your Name"},
    "problem_model_used": {"zh": "使用的模型", "en": "Model Used"},
    "problem_approach_label": {"zh": "尝试方法（可选）", "en": "Approach (optional)"},
    "problem_approach_placeholder": {"zh": "你用的什么策略？换了什么 prompt？用了什么工具？", "en": "What strategy? Different prompt? Any tools?"},
    "problem_result_label": {"zh": "运行结果 （成功或失败，越详细越好）", "en": "Result (success or failure, more detail helps)"},
    "problem_submit_btn": {"zh": "提交尝试记录", "en": "Submit Attempt"},
    "problem_mark_resolved": {"zh": "✅ 标记为已解决", "en": "✅ Mark as Resolved"},
    "problem_resolver_field": {"zh": "解决者", "en": "Resolver"},
    "problem_solution_field": {"zh": "解决方案（支持 Markdown）", "en": "Solution (Markdown supported)"},
    "problem_solution_placeholder": {"zh": "## 解决方案\n\n### 使用的模型\n...\n\n### 关键方法\n...\n\n### 经验教训\n...", "en": "## Solution\n\n### Model used\n...\n\n### Key approach\n...\n\n### Lessons learned\n..."},
    "problem_resolve_btn": {"zh": "标记已解决", "en": "Mark Resolved"},
    "problem_back": {"zh": "← 返回难题列表", "en": "← Back to Problems"},
    "problem_delete": {"zh": "删除", "en": "Delete"},

    # ---- Problem Form ----
    "problem_form_title": {"zh": "提交新难题", "en": "Submit New Problem"},
    "problem_form_title_field": {"zh": "难题标题", "en": "Problem Title"},
    "problem_form_task": {"zh": "原始任务要求（Markdown）", "en": "Original Task (Markdown)"},
    "problem_form_logs": {"zh": "处理日志（JSON 数组）", "en": "Processing Logs (JSON array)"},
    "problem_form_logs_hint": {"zh": "Agent 会自动填写此项", "en": "Agent auto-fills this"},
    "problem_form_submitter": {"zh": "提交者", "en": "Submitter"},
    "problem_form_submit_btn": {"zh": "提交难题", "en": "Submit Problem"},

    # ---- Projects ----
    "projects_title": {"zh": "项目公告", "en": "Projects"},
    "projects_new": {"zh": "发布项目", "en": "New Project"},
    "projects_search": {"zh": "搜索项目...", "en": "Search projects..."},
    "projects_edit": {"zh": "编辑", "en": "Edit"},
    "projects_delete": {"zh": "删除", "en": "Delete"},
    "projects_back": {"zh": "← 返回项目列表", "en": "← Back to Projects"},
    "projects_form_title_new": {"zh": "发布新项目", "en": "New Project"},
    "projects_form_title_edit": {"zh": "编辑项目", "en": "Edit Project"},
    "projects_form_title_field": {"zh": "项目标题", "en": "Title"},
    "projects_form_content": {"zh": "内容（Markdown）", "en": "Content (Markdown)"},
    "projects_form_author": {"zh": "发布者", "en": "Author"},
    "projects_form_submit": {"zh": "发布", "en": "Publish"},

    # ---- Pagination ----
    "pagination_page": {"zh": "第", "en": "Page "},
    "pagination_of": {"zh": "页，共", "en": " of "},
    "pagination_prev": {"zh": "上一页", "en": "Prev"},
    "pagination_next": {"zh": "下一页", "en": "Next"},
    "pagination_items": {"zh": "条", "en": " items"},
}

# Category and model names don't need translation (they're code values)
# But we translate the display labels for common ones
CATEGORY_LABELS = {
    "code-review": {"zh": "代码审查", "en": "Code Review"},
    "debugging": {"zh": "调试", "en": "Debugging"},
    "deployment": {"zh": "部署", "en": "Deployment"},
    "testing": {"zh": "测试", "en": "Testing"},
    "architecture": {"zh": "架构", "en": "Architecture"},
    "documentation": {"zh": "文档", "en": "Documentation"},
    "refactoring": {"zh": "重构", "en": "Refactoring"},
    "performance": {"zh": "性能", "en": "Performance"},
    "security": {"zh": "安全", "en": "Security"},
    "data-processing": {"zh": "数据处理", "en": "Data Processing"},
    "frontend": {"zh": "前端", "en": "Frontend"},
    "devops": {"zh": "DevOps", "en": "DevOps"},
    "other": {"zh": "其他", "en": "Other"},
}


def get_locale(request: Request) -> str:
    """Detect language: query param > cookie > default zh."""
    lang = request.query_params.get("lang")
    if lang in ("zh", "en"):
        return lang
    lang = request.cookies.get("lang")
    if lang in ("zh", "en"):
        return lang
    return "zh"


def t(key: str, locale: str = "zh") -> str:
    """Translate a key. Falls back to key name if not found."""
    entry = LANG.get(key)
    if entry:
        return entry.get(locale, entry.get("zh", key))
    return key


def cat_label(cat: str, locale: str = "zh") -> str:
    """Translate a category value."""
    entry = CATEGORY_LABELS.get(cat)
    if entry:
        return entry.get(locale, cat)
    return cat

import json
import logging

from mcp.server.fastmcp import FastMCP

from app.database import engine
from sqlalchemy.orm import Session

from app.models.skill import Skill
from app.models.problem import Problem, ProblemAttempt
from app.models.project import Project

logger = logging.getLogger(__name__)

mcp = FastMCP("AI Team Hub")


def _get_db() -> Session:
    return Session(engine)


@mcp.tool(description="Search the skill marketplace for relevant skills by keyword. Use the optional names parameter to limit search to specific skills you know about.")
def search_skills(query: str, names: list[str] | None = None) -> str:
    """Search skills by keyword. Returns matching skills with name, title, and category.

    Args:
        query: Keyword to search for in title, description, and tags
        names: Optional list of skill names (slugs) to limit search scope. If omitted, searches all enabled skills.
    """
    db = _get_db()
    try:
        q = db.query(Skill).filter(Skill.enabled == True)
        if names:
            q = q.filter(Skill.name.in_(names))
        results = (
            q.filter(
                Skill.title.contains(query)
                | Skill.human_section.contains(query)
                | Skill.tags.contains(query)
            )
            .limit(20)
            .all()
        )
        if not results:
            hint = f" (scoped to {len(names)} skills)" if names else ""
            return json.dumps({"message": f"No skills found for '{query}'{hint}", "query": query}, ensure_ascii=False)

        items = [
            {
                "id": s.id,
                "name": s.name,
                "title": s.title,
                "category": s.category,
                "model_used": s.model_used,
                "author": s.author,
            }
            for s in results
        ]
        return json.dumps({"skills": items, "count": len(items)}, ensure_ascii=False, indent=2)
    finally:
        db.close()


@mcp.tool(description="Retrieve a specific skill's full agent instructions by its slug name (e.g., 'python-code-review')")
def get_skill(name: str) -> str:
    """Get the full agent section (YAML instructions) for a skill by its slug name."""
    db = _get_db()
    try:
        skill = db.query(Skill).filter(Skill.name == name).first()
        if not skill:
            return json.dumps(
                {"error": f"Skill '{name}' not found", "hint": "Use search_skills to find available skills"},
                ensure_ascii=False,
            )
        return skill.agent_section
    finally:
        db.close()


@mcp.tool(description="Submit a failed task to the problem bounty board for colleagues to help solve")
def submit_error(
    title: str,
    task_summary: str,
    submitter: str,
    logs: str = "[]",
) -> str:
    """Submit a failed task to the problem board.

    Args:
        title: Short title for the problem
        task_summary: Detailed description of the original task and what went wrong
        submitter: Your name
        logs: JSON array of attempt logs, e.g. [{"model": "deepseek-v3", "status": "failed", "result": "...", "timestamp": "..."}]
    """
    db = _get_db()
    try:
        problem = Problem(
            title=title,
            original_task=task_summary,
            processing_logs=logs,
            submitter=submitter,
        )
        db.add(problem)
        db.commit()
        db.refresh(problem)
        return json.dumps(
            {
                "message": "Problem submitted successfully",
                "problem_id": problem.id,
                "status": problem.status,
                "url_hint": f"/problems/{problem.id}",
            },
            ensure_ascii=False,
            indent=2,
        )
    finally:
        db.close()


@mcp.tool(description="Browse the problem bounty board, optionally filtered by status (open/in_progress/resolved)")
def list_problems(status: str = "") -> str:
    """List problems on the bounty board.

    Args:
        status: Filter by status — 'open', 'in_progress', 'resolved', or '' for all
    """
    db = _get_db()
    try:
        query = db.query(Problem)
        if status:
            query = query.filter(Problem.status == status)
        results = query.order_by(Problem.created_at.desc()).limit(30).all()

        if not results:
            hint = f" (filtered by status='{status}')" if status else ""
            return json.dumps({"message": "No problems found" + hint, "problems": []}, ensure_ascii=False)

        items = [
            {
                "id": p.id,
                "title": p.title,
                "status": p.status,
                "submitter": p.submitter,
                "attempts_count": len(p.attempts) if p.attempts else 0,
                "created_at": p.created_at.strftime("%Y-%m-%d %H:%M") if p.created_at else "",
            }
            for p in results
        ]
        return json.dumps({"problems": items, "count": len(items)}, ensure_ascii=False, indent=2)
    finally:
        db.close()


@mcp.tool(description="Post an announcement to the team project board")
def post_announcement(title: str, content: str, author: str) -> str:
    """Post a new project announcement.

    Args:
        title: Announcement title
        content: Announcement content (Markdown supported)
        author: Your name
    """
    db = _get_db()
    try:
        project = Project(title=title, content=content, author=author)
        db.add(project)
        db.commit()
        db.refresh(project)
        return json.dumps(
            {
                "message": "Announcement posted successfully",
                "project_id": project.id,
                "url_hint": f"/projects/{project.id}",
            },
            ensure_ascii=False,
            indent=2,
        )
    finally:
        db.close()


@mcp.tool(description="Submit a solution that resolved a problem on the bounty board")
def resolve_problem(
    problem_id: int,
    resolver: str,
    solution: str,
    model_used: str = "",
    approach: str = "",
) -> str:
    """Submit a successful resolution to a problem.

    Use this when you or a teammate has successfully solved a problem from the bounty board.
    This marks the problem as resolved and records the solution for the team.

    Args:
        problem_id: The problem ID (from list_problems)
        resolver: Name of the person who solved it
        solution: Full solution description (Markdown supported) — what worked and why
        model_used: Which model succeeded (e.g. 'claude-opus-4', 'deepseek-v3')
        approach: Brief description of the approach that worked
    """
    db = _get_db()
    try:
        problem = db.query(Problem).filter(Problem.id == problem_id).first()
        if not problem:
            return json.dumps({"error": f"Problem {problem_id} not found"}, ensure_ascii=False)

        # Record the attempt
        if approach or model_used:
            attempt = ProblemAttempt(
                problem_id=problem.id,
                solver=resolver,
                model_used=model_used,
                approach=approach,
                result=f"Success: {solution[:500]}",
            )
            db.add(attempt)

        # Mark as resolved
        problem.status = "resolved"
        problem.resolver = resolver
        problem.resolution = solution
        db.commit()

        return json.dumps(
            {
                "message": "Problem resolved successfully",
                "problem_id": problem.id,
                "url_hint": f"/problems/{problem.id}",
            },
            ensure_ascii=False,
            indent=2,
        )
    finally:
        db.close()


@mcp.tool(description="Record an attempt on a problem (even if unsuccessful, helps others learn)")
def add_attempt(
    problem_id: int,
    solver: str,
    model_used: str = "",
    approach: str = "",
    result: str = "",
) -> str:
    """Record your attempt at solving a problem. Even failed attempts help colleagues learn what doesn't work.

    Args:
        problem_id: The problem ID
        solver: Your name
        model_used: Which model you tried
        approach: What strategy/prompt/technique you tried
        result: What happened — success, partial success, or failure details
    """
    db = _get_db()
    try:
        problem = db.query(Problem).filter(Problem.id == problem_id).first()
        if not problem:
            return json.dumps({"error": f"Problem {problem_id} not found"}, ensure_ascii=False)

        attempt = ProblemAttempt(
            problem_id=problem.id,
            solver=solver,
            model_used=model_used,
            approach=approach,
            result=result,
        )
        db.add(attempt)

        # Auto-transition to in_progress if currently open
        if problem.status == "open":
            problem.status = "in_progress"

        db.commit()
        db.refresh(attempt)

        return json.dumps(
            {
                "message": "Attempt recorded",
                "attempt_id": attempt.id,
                "problem_id": problem.id,
                "problem_status": problem.status,
            },
            ensure_ascii=False,
            indent=2,
        )
    finally:
        db.close()


def setup_mcp(app):
    """Mount MCP server onto a FastAPI/Starlette app."""
    app.mount("/mcp", mcp.sse_app())
    logger.info("MCP server mounted at /mcp")

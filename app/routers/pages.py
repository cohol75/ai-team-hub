from pathlib import Path
from fastapi import APIRouter, Depends, Request, Query, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse, PlainTextResponse
from sqlalchemy.orm import Session
from markdown import markdown

from app.database import get_db
from app.models.skill import Skill
from app.models.problem import Problem
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.schemas.skill import SkillCreate, SkillUpdate
from app.schemas.problem import ProblemCreate, ProblemUpdate, AttemptCreate
from app.services import project as project_service
from app.services import skill as skill_service
from app.services import problem as problem_service
from app.i18n import t, get_locale, cat_label
import json

router = APIRouter(tags=["pages"])

SETUP_SCRIPT = None


def get_setup_script():
    global SETUP_SCRIPT
    if SETUP_SCRIPT is None:
        script_path = Path(__file__).parent.parent.parent / "scripts" / "setup.sh"
        if script_path.exists():
            SETUP_SCRIPT = script_path.read_text()
    return SETUP_SCRIPT


@router.get("/setup.sh")
def serve_setup_script():
    script = get_setup_script()
    if not script:
        raise HTTPException(404, "Setup script not found")
    return PlainTextResponse(script, media_type="text/plain")


@router.get("/lang/{locale}")
def set_language(locale: str):
    response = RedirectResponse("/", status_code=303)
    if locale in ("zh", "en"):
        response.set_cookie(key="lang", value=locale, max_age=365 * 24 * 3600)
    return response

TEMPLATES = None


def get_templates():
    global TEMPLATES
    if TEMPLATES is None:
        from jinja2 import Environment, FileSystemLoader, select_autoescape
        from pathlib import Path

        templates_dir = Path(__file__).parent.parent / "templates"
        TEMPLATES = Environment(
            loader=FileSystemLoader(str(templates_dir)),
            autoescape=select_autoescape(["html"]),
        )
    return TEMPLATES


def render(name: str, request: Request, **context):
    locale = get_locale(request)
    return HTMLResponse(get_templates().get_template(name).render(
        **context, request=request, markdown=markdown,
        t=lambda key: t(key, locale),
        locale=locale,
        cat_label=lambda cat: cat_label(cat, locale),
    ))


# ---- Index ----

@router.get("/", response_class=HTMLResponse)
def index_page(request: Request, db: Session = Depends(get_db)):
    recent_projects, _ = project_service.list_projects(db, page=1, per_page=5)
    skills_count = db.query(Skill).count()
    open_problems_count = db.query(Problem).filter(Problem.status == "open").count()
    recent_skills, _ = skill_service.list_skills(db, page=1, per_page=5)
    return render(
        "index.html",
        request,
        projects=recent_projects,
        skills=recent_skills,
        skills_count=skills_count,
        open_problems_count=open_problems_count,
    )


@router.get("/guide", response_class=HTMLResponse)
def guide_page(request: Request):
    return render("guide.html", request)


# ---- Project Pages ----

@router.get("/projects", response_class=HTMLResponse)
def projects_page(
    request: Request,
    page: int = Query(1, ge=1),
    search: str = Query(""),
    db: Session = Depends(get_db),
):
    items, total = project_service.list_projects(db, page=page, search=search)
    per_page = 20
    total_pages = (total + per_page - 1) // per_page
    return render(
        "projects/list.html",
        request,
        projects=items,
        page=page,
        total=total,
        search=search,
        total_pages=total_pages,
    )


@router.get("/projects/new", response_class=HTMLResponse)
def new_project_page(request: Request):
    return render("projects/form.html", request, project=None)


@router.post("/projects/new")
def create_project_form(
    title: str = Form(...),
    content: str = Form(...),
    author: str = Form(...),
    db: Session = Depends(get_db),
):
    data = ProjectCreate(title=title, content=content, author=author)
    project = project_service.create_project(db, data)
    return RedirectResponse(f"/projects/{project.id}", status_code=303)


@router.get("/projects/{project_id}", response_class=HTMLResponse)
def project_detail_page(request: Request, project_id: int, db: Session = Depends(get_db)):
    project = project_service.get_project(db, project_id)
    if not project:
        raise HTTPException(404, "Project not found")
    return render("projects/detail.html", request, project=project)


@router.get("/projects/{project_id}/edit", response_class=HTMLResponse)
def edit_project_page(request: Request, project_id: int, db: Session = Depends(get_db)):
    project = project_service.get_project(db, project_id)
    if not project:
        raise HTTPException(404, "Project not found")
    return render("projects/form.html", request, project=project)


@router.post("/projects/{project_id}/edit")
def update_project_form(
    project_id: int,
    title: str = Form(...),
    content: str = Form(...),
    author: str = Form(...),
    db: Session = Depends(get_db),
):
    project = project_service.get_project(db, project_id)
    if not project:
        raise HTTPException(404, "Project not found")
    data = ProjectUpdate(title=title, content=content, author=author)
    project_service.update_project(db, project, data)
    return RedirectResponse(f"/projects/{project_id}", status_code=303)


# ---- Skill Pages ----

@router.get("/skills", response_class=HTMLResponse)
def skills_page(
    request: Request,
    page: int = Query(1, ge=1),
    search: str = Query(""),
    category: str = Query(""),
    model: str = Query(""),
    db: Session = Depends(get_db),
):
    items, total = skill_service.list_skills(db, page=page, search=search, category=category, model=model)
    per_page = 20
    total_pages = (total + per_page - 1) // per_page
    return render(
        "skills/list.html",
        request,
        skills=items,
        page=page,
        total=total,
        search=search,
        category=category,
        model=model,
        total_pages=total_pages,
    )


@router.get("/skills/new", response_class=HTMLResponse)
def new_skill_page(request: Request):
    return render("skills/form.html", request, skill=None, error=None)


@router.post("/skills/new")
def create_skill_form(
    request: Request,
    title: str = Form(...),
    human_section: str = Form(...),
    agent_section: str = Form(...),
    model_used: str = Form(""),
    model_provider: str = Form(""),
    category: str = Form("other"),
    tags: str = Form(""),
    author: str = Form(...),
    db: Session = Depends(get_db),
):
    data = SkillCreate(
        title=title, human_section=human_section, agent_section=agent_section,
        model_used=model_used, model_provider=model_provider,
        category=category, tags=tags, author=author,
    )
    try:
        skill_obj = skill_service.create_skill(db, data)
        return RedirectResponse(f"/skills/{skill_obj.id}", status_code=303)
    except ValueError as e:
        return render("skills/form.html", request, skill=data, error=str(e))


@router.get("/skills/{skill_id}", response_class=HTMLResponse)
def skill_detail_page(request: Request, skill_id: int, db: Session = Depends(get_db)):
    skill_obj = skill_service.get_skill(db, skill_id)
    if not skill_obj:
        raise HTTPException(404, "Skill not found")
    return render("skills/detail.html", request, skill=skill_obj)


@router.get("/skills/{skill_id}/edit", response_class=HTMLResponse)
def edit_skill_page(request: Request, skill_id: int, db: Session = Depends(get_db)):
    skill_obj = skill_service.get_skill(db, skill_id)
    if not skill_obj:
        raise HTTPException(404, "Skill not found")
    return render("skills/form.html", request, skill=skill_obj, error=None)


@router.post("/skills/{skill_id}/edit")
def update_skill_form(
    request: Request,
    skill_id: int,
    title: str = Form(...),
    human_section: str = Form(...),
    agent_section: str = Form(...),
    model_used: str = Form(""),
    model_provider: str = Form(""),
    category: str = Form("other"),
    tags: str = Form(""),
    author: str = Form(...),
    db: Session = Depends(get_db),
):
    skill_obj = skill_service.get_skill(db, skill_id)
    if not skill_obj:
        raise HTTPException(404, "Skill not found")
    data = SkillUpdate(
        title=title, human_section=human_section, agent_section=agent_section,
        model_used=model_used, model_provider=model_provider,
        category=category, tags=tags, author=author,
    )
    try:
        skill_obj = skill_service.update_skill(db, skill_obj, data)
        return RedirectResponse(f"/skills/{skill_id}", status_code=303)
    except ValueError as e:
        return render("skills/form.html", request, skill=skill_obj, error=str(e))


# ---- Problem Pages ----

@router.get("/problems", response_class=HTMLResponse)
def problems_page(
    request: Request,
    page: int = Query(1, ge=1),
    status: str = Query(""),
    search: str = Query(""),
    db: Session = Depends(get_db),
):
    items, total = problem_service.list_problems(db, page=page, status=status, search=search)
    per_page = 20
    total_pages = (total + per_page - 1) // per_page
    return render(
        "problems/list.html",
        request,
        problems=items,
        page=page,
        total=total,
        status=status,
        search=search,
        total_pages=total_pages,
    )


@router.get("/problems/new", response_class=HTMLResponse)
def new_problem_page(request: Request):
    return render("problems/form.html", request, problem=None)


@router.post("/problems/new")
def create_problem_form(
    title: str = Form(...),
    original_task: str = Form(...),
    processing_logs: str = Form("[]"),
    submitter: str = Form(...),
    db: Session = Depends(get_db),
):
    data = ProblemCreate(
        title=title, original_task=original_task,
        processing_logs=processing_logs, submitter=submitter,
    )
    problem = problem_service.create_problem(db, data)
    return RedirectResponse(f"/problems/{problem.id}", status_code=303)


@router.get("/problems/{problem_id}", response_class=HTMLResponse)
def problem_detail_page(request: Request, problem_id: int, db: Session = Depends(get_db)):
    problem = problem_service.get_problem(db, problem_id)
    if not problem:
        raise HTTPException(404, "Problem not found")
    return render("problems/detail.html", request, problem=problem, json=json)


@router.post("/problems/{problem_id}/attempts")
def add_attempt_form(
    problem_id: int,
    solver: str = Form(...),
    model_used: str = Form(""),
    approach: str = Form(""),
    result: str = Form(""),
    db: Session = Depends(get_db),
):
    problem = problem_service.get_problem(db, problem_id)
    if not problem:
        raise HTTPException(404, "Problem not found")
    data = AttemptCreate(solver=solver, model_used=model_used, approach=approach, result=result)
    problem_service.add_attempt(db, problem, data)
    return RedirectResponse(f"/problems/{problem_id}", status_code=303)


@router.post("/problems/{problem_id}/resolve")
def resolve_problem_form(
    problem_id: int,
    resolver: str = Form(...),
    resolution: str = Form(...),
    db: Session = Depends(get_db),
):
    problem = problem_service.get_problem(db, problem_id)
    if not problem:
        raise HTTPException(404, "Problem not found")
    data = ProblemUpdate(status="resolved", resolver=resolver, resolution=resolution)
    problem_service.update_problem(db, problem, data)
    return RedirectResponse(f"/problems/{problem_id}", status_code=303)

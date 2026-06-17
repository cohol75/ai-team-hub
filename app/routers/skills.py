from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.skill import SkillCreate, SkillUpdate, SkillResponse, SkillListResponse, SkillToggleRequest
from app.services import skill as skill_service

router = APIRouter(prefix="/api/skills", tags=["skills"])


@router.get("", response_model=SkillListResponse)
def list_skills(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    search: str = Query(""),
    category: str = Query(""),
    model: str = Query(""),
    tag: str = Query(""),
    enabled_only: bool = Query(False),
    db: Session = Depends(get_db),
):
    items, total = skill_service.list_skills(db, page, per_page, search, category, model, tag, enabled_only)
    return SkillListResponse(
        items=[SkillResponse.model_validate(s) for s in items],
        total=total,
        page=page,
        per_page=per_page,
    )


@router.get("/by-name/{name}", response_model=SkillResponse)
def get_skill_by_name(name: str, db: Session = Depends(get_db)):
    skill = skill_service.get_skill_by_name(db, name)
    if not skill:
        raise HTTPException(404, "Skill not found")
    return SkillResponse.model_validate(skill)


@router.get("/{skill_id}", response_model=SkillResponse)
def get_skill(skill_id: int, db: Session = Depends(get_db)):
    skill = skill_service.get_skill(db, skill_id)
    if not skill:
        raise HTTPException(404, "Skill not found")
    return SkillResponse.model_validate(skill)


@router.post("", response_model=SkillResponse, status_code=201)
def create_skill(data: SkillCreate, db: Session = Depends(get_db)):
    existing = skill_service.get_skill_by_name(db, data.agent_section.split("\n")[0])
    try:
        return SkillResponse.model_validate(skill_service.create_skill(db, data))
    except ValueError as e:
        raise HTTPException(422, str(e))


@router.put("/{skill_id}", response_model=SkillResponse)
def update_skill(skill_id: int, data: SkillUpdate, db: Session = Depends(get_db)):
    skill = skill_service.get_skill(db, skill_id)
    if not skill:
        raise HTTPException(404, "Skill not found")
    try:
        return SkillResponse.model_validate(skill_service.update_skill(db, skill, data))
    except ValueError as e:
        raise HTTPException(422, str(e))


@router.delete("/{skill_id}", status_code=204)
def delete_skill(skill_id: int, db: Session = Depends(get_db)):
    skill = skill_service.get_skill(db, skill_id)
    if not skill:
        raise HTTPException(404, "Skill not found")
    skill_service.delete_skill(db, skill)


@router.get("/{skill_id}/raw", response_class=PlainTextResponse)
def get_skill_raw(skill_id: int, db: Session = Depends(get_db)):
    """Return raw agent YAML for agent consumption."""
    skill = skill_service.get_skill(db, skill_id)
    if not skill:
        raise HTTPException(404, "Skill not found")
    return skill.agent_section


@router.patch("/{skill_id}/toggle", response_model=SkillResponse)
def toggle_skill(skill_id: int, data: SkillToggleRequest, db: Session = Depends(get_db)):
    skill = skill_service.toggle_skill(db, skill_id, data.enabled)
    if not skill:
        raise HTTPException(404, "Skill not found")
    return SkillResponse.model_validate(skill)

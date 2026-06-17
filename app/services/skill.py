import yaml

from sqlalchemy.orm import Session

from app.models.skill import Skill
from app.schemas.skill import SkillCreate, SkillUpdate, AgentSectionSpec


def validate_agent_yaml(agent_section: str) -> tuple[AgentSectionSpec | None, str | None]:
    """Validate the agent section YAML. Returns (parsed_spec, error_message)."""
    try:
        data = yaml.safe_load(agent_section)
    except yaml.YAMLError as e:
        return None, f"YAML 解析失败: {e}"

    if not isinstance(data, dict):
        return None, "Agent 段必须是 YAML 字典/mapping"

    try:
        spec = AgentSectionSpec(**data)
        # Validate steps are sequential
        expected_step = 1
        for step in spec.steps:
            if step.step != expected_step:
                return None, f"步骤编号不连续：期望 {expected_step}，实际 {step.step}"
            if step.action == "execute" and not step.command:
                return None, f"步骤 {step.step} 的 action 为 execute 时必须提供 command"
            expected_step += 1
        return spec, None
    except Exception as e:
        return None, str(e)


def create_skill(db: Session, data: SkillCreate) -> Skill:
    spec, error = validate_agent_yaml(data.agent_section)
    if error:
        raise ValueError(error)

    skill = Skill(
        name=spec.name,
        title=data.title,
        human_section=data.human_section,
        agent_section=data.agent_section,
        model_used=data.model_used or spec.model or "",
        model_provider=data.model_provider or spec.model_provider or "",
        category=data.category or spec.category,
        tags=data.tags or ",".join(spec.tags),
        author=data.author,
    )
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill


def update_skill(db: Session, skill: Skill, data: SkillUpdate) -> Skill:
    update_data = data.model_dump(exclude_unset=True)

    # Re-validate agent section if updated
    if "agent_section" in update_data:
        agent_yaml = update_data["agent_section"]
        spec, error = validate_agent_yaml(agent_yaml)
        if error:
            raise ValueError(error)
        # Update name if it changed in YAML
        if spec.name != skill.name:
            existing = db.query(Skill).filter(Skill.name == spec.name, Skill.id != skill.id).first()
            if existing:
                raise ValueError(f"技能名称 '{spec.name}' 已被占用")

    for key, value in update_data.items():
        setattr(skill, key, value)

    db.commit()
    db.refresh(skill)
    return skill


def get_skill(db: Session, skill_id: int) -> Skill | None:
    return db.query(Skill).filter(Skill.id == skill_id).first()


def get_skill_by_name(db: Session, name: str) -> Skill | None:
    return db.query(Skill).filter(Skill.name == name).first()


def list_skills(
    db: Session,
    page: int = 1,
    per_page: int = 20,
    search: str = "",
    category: str = "",
    model: str = "",
    tag: str = "",
    enabled_only: bool = False,
) -> tuple[list[Skill], int]:
    query = db.query(Skill)
    if enabled_only:
        query = query.filter(Skill.enabled == True)
    if search:
        query = query.filter(
            Skill.title.contains(search) | Skill.human_section.contains(search)
        )
    if category:
        query = query.filter(Skill.category == category)
    if model:
        query = query.filter(Skill.model_used.contains(model))
    if tag:
        query = query.filter(Skill.tags.contains(tag))

    total = query.count()
    items = (
        query.order_by(Skill.created_at.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )
    return items, total


def toggle_skill(db: Session, skill_id: int, enabled: bool) -> Skill | None:
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if skill:
        skill.enabled = enabled
        db.commit()
        db.refresh(skill)
    return skill


def delete_skill(db: Session, skill: Skill) -> None:
    db.delete(skill)
    db.commit()

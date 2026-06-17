from sqlalchemy.orm import Session, joinedload

from app.models.problem import Problem, ProblemAttempt
from app.schemas.problem import ProblemCreate, ProblemUpdate, AttemptCreate


def list_problems(
    db: Session,
    page: int = 1,
    per_page: int = 20,
    status: str = "",
    search: str = "",
) -> tuple[list[Problem], int]:
    query = db.query(Problem)
    if status:
        query = query.filter(Problem.status == status)
    if search:
        query = query.filter(
            Problem.title.contains(search) | Problem.original_task.contains(search)
        )
    total = query.count()
    items = (
        query.options(joinedload(Problem.attempts))
        .order_by(Problem.created_at.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )
    return items, total


def get_problem(db: Session, problem_id: int) -> Problem | None:
    return (
        db.query(Problem)
        .options(joinedload(Problem.attempts))
        .filter(Problem.id == problem_id)
        .first()
    )


def create_problem(db: Session, data: ProblemCreate) -> Problem:
    problem = Problem(**data.model_dump())
    db.add(problem)
    db.commit()
    db.refresh(problem)
    return problem


def update_problem(db: Session, problem: Problem, data: ProblemUpdate) -> Problem:
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(problem, key, value)
    db.commit()
    db.refresh(problem)
    return problem


def add_attempt(db: Session, problem: Problem, data: AttemptCreate) -> ProblemAttempt:
    attempt = ProblemAttempt(problem_id=problem.id, **data.model_dump())
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return attempt


def delete_problem(db: Session, problem: Problem) -> None:
    db.delete(problem)
    db.commit()

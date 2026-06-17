from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.problem import (
    ProblemCreate, ProblemUpdate, ProblemResponse, ProblemListResponse,
    AttemptCreate, AttemptResponse,
)
from app.services import problem as problem_service

router = APIRouter(prefix="/api/problems", tags=["problems"])


@router.get("", response_model=ProblemListResponse)
def list_problems(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    status: str = Query(""),
    search: str = Query(""),
    db: Session = Depends(get_db),
):
    items, total = problem_service.list_problems(db, page, per_page, status, search)
    return ProblemListResponse(
        items=[ProblemResponse.model_validate(p) for p in items],
        total=total,
        page=page,
        per_page=per_page,
    )


@router.get("/{problem_id}", response_model=ProblemResponse)
def get_problem(problem_id: int, db: Session = Depends(get_db)):
    problem = problem_service.get_problem(db, problem_id)
    if not problem:
        raise HTTPException(404, "Problem not found")
    return ProblemResponse.model_validate(problem)


@router.post("", response_model=ProblemResponse, status_code=201)
def create_problem(data: ProblemCreate, db: Session = Depends(get_db)):
    return ProblemResponse.model_validate(problem_service.create_problem(db, data))


@router.patch("/{problem_id}/status", response_model=ProblemResponse)
def update_status(
    problem_id: int,
    status: str = Query(...),
    resolver: str = Query(""),
    resolution: str = Query(""),
    db: Session = Depends(get_db),
):
    problem = problem_service.get_problem(db, problem_id)
    if not problem:
        raise HTTPException(404, "Problem not found")
    if status not in ("open", "in_progress", "resolved"):
        raise HTTPException(400, "Invalid status")
    update = ProblemUpdate(status=status)
    if resolver:
        update.resolver = resolver
    if resolution:
        update.resolution = resolution
    return ProblemResponse.model_validate(problem_service.update_problem(db, problem, update))


@router.post("/{problem_id}/attempts", response_model=AttemptResponse, status_code=201)
def add_attempt(problem_id: int, data: AttemptCreate, db: Session = Depends(get_db)):
    problem = problem_service.get_problem(db, problem_id)
    if not problem:
        raise HTTPException(404, "Problem not found")
    attempt = problem_service.add_attempt(db, problem, data)
    return AttemptResponse.model_validate(attempt)


@router.delete("/{problem_id}", status_code=204)
def delete_problem(problem_id: int, db: Session = Depends(get_db)):
    problem = problem_service.get_problem(db, problem_id)
    if not problem:
        raise HTTPException(404, "Problem not found")
    problem_service.delete_problem(db, problem)

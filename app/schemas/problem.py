from datetime import datetime
from pydantic import BaseModel, Field, field_serializer


class ProblemCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    original_task: str = Field(min_length=1)
    processing_logs: str = Field(default="[]")
    submitter: str = Field(min_length=1, max_length=100)


class ProblemUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    original_task: str | None = Field(default=None, min_length=1)
    processing_logs: str | None = None
    status: str | None = None
    resolver: str | None = None
    resolution: str | None = None


class AttemptCreate(BaseModel):
    solver: str = Field(min_length=1, max_length=100)
    model_used: str = ""
    approach: str = ""
    result: str = ""


class AttemptResponse(BaseModel):
    id: int
    problem_id: int
    solver: str
    model_used: str
    approach: str
    result: str
    created_at: datetime

    model_config = {"from_attributes": True}

    @field_serializer("created_at")
    def serialize_datetime(self, dt: datetime) -> str:
        return dt.strftime("%Y-%m-%d %H:%M:%S")


class ProblemResponse(BaseModel):
    id: int
    title: str
    original_task: str
    processing_logs: str
    status: str
    submitter: str
    resolver: str
    resolution: str
    created_at: datetime
    updated_at: datetime
    attempts: list[AttemptResponse] = []

    model_config = {"from_attributes": True}

    @field_serializer("created_at", "updated_at")
    def serialize_datetime(self, dt: datetime) -> str:
        return dt.strftime("%Y-%m-%d %H:%M:%S")


class ProblemListResponse(BaseModel):
    items: list[ProblemResponse]
    total: int
    page: int
    per_page: int

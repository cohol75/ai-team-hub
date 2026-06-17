from datetime import datetime
from pydantic import BaseModel, Field, field_serializer, field_validator
import re

VALID_CATEGORIES = [
    "code-review", "debugging", "deployment", "testing",
    "architecture", "documentation", "refactoring",
    "performance", "security", "data-processing",
    "frontend", "devops", "other",
]

VALID_ACTIONS = ["analyze", "execute", "generate", "review", "test", "deploy"]
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


class AgentStep(BaseModel):
    step: int = Field(ge=1, le=20)
    action: str
    instruction: str = Field(min_length=10, max_length=5000)
    expected_output: str = Field(min_length=10, max_length=1000)
    command: str | None = Field(default=None, max_length=2000)

    @field_validator("action")
    @classmethod
    def check_action(cls, v: str) -> str:
        if v not in VALID_ACTIONS:
            raise ValueError(f"Action must be one of: {', '.join(VALID_ACTIONS)}")
        return v


class AgentSectionSpec(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    version: str = "1.0.0"
    description: str = Field(min_length=10, max_length=500)
    category: str = Field(default="other")
    model: str | None = None
    model_provider: str | None = None
    tags: list[str] = []
    input_description: str | None = None
    output_description: str | None = None
    dependencies: list[str] = []
    steps: list[AgentStep] = Field(min_length=1, max_length=20)

    @field_validator("name")
    @classmethod
    def check_name(cls, v: str) -> str:
        if not SLUG_RE.match(v):
            raise ValueError("Name must be lowercase slug: a-z, 0-9, hyphens")
        if len(v) < 3:
            raise ValueError("Name must be at least 3 characters")
        return v

    @field_validator("category")
    @classmethod
    def check_category(cls, v: str) -> str:
        if v not in VALID_CATEGORIES:
            raise ValueError(f"Category must be one of: {', '.join(VALID_CATEGORIES)}")
        return v

    @field_validator("version")
    @classmethod
    def check_version(cls, v: str) -> str:
        if not re.match(r"^\d+\.\d+\.\d+$", v):
            raise ValueError("Version must be semver format: X.Y.Z")
        return v


class SkillCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    human_section: str = Field(min_length=10)
    agent_section: str = Field(min_length=10)
    model_used: str = ""
    model_provider: str = ""
    category: str = "other"
    tags: str = ""
    author: str = Field(min_length=1, max_length=100)


class SkillUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    human_section: str | None = Field(default=None, min_length=10)
    agent_section: str | None = Field(default=None, min_length=10)
    model_used: str | None = None
    model_provider: str | None = None
    category: str | None = None
    tags: str | None = None
    author: str | None = Field(default=None, min_length=1, max_length=100)


class SkillToggleRequest(BaseModel):
    enabled: bool


class SkillResponse(BaseModel):
    id: int
    name: str
    title: str
    human_section: str
    agent_section: str
    model_used: str
    model_provider: str
    category: str
    tags: str
    author: str
    enabled: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

    @field_serializer("created_at", "updated_at")
    def serialize_datetime(self, dt: datetime) -> str:
        return dt.strftime("%Y-%m-%d %H:%M:%S")


class SkillListResponse(BaseModel):
    items: list[SkillResponse]
    total: int
    page: int
    per_page: int

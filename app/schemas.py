from pydantic import BaseModel, Field, HttpUrl, ConfigDict
from typing import Optional, Literal
from datetime import datetime


class ProjectCreate(BaseModel):
    title: str = Field(min_length=3, max_length=150)
    description: str = Field(min_length=10)
    domain: str = Field(min_length=2, max_length=100)
    github_url: HttpUrl
    demo_url: HttpUrl


class ProjectResponse(BaseModel):
    id: int
    title: str
    description: str
    domain: str
    github_url: str
    demo_url: str
    status: str
    feedback_remarks: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ModerationRequest(BaseModel):
    status: Literal["Pending", "Approved", "Rejected"]
    feedback_remarks: Optional[str] = Field(default=None, max_length=1000)


class ProjectListResponse(BaseModel):
    total_items: int
    total_pages: int
    current_page: int
    page_size: int
    projects: list[ProjectResponse]
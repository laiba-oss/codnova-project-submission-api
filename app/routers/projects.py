
import os
import secrets

from dotenv import load_dotenv
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Header,
    status
)
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import get_db
from app.models import ProjectSubmission
from app.schemas import (
    ProjectCreate,
    ProjectResponse,
    ModerationRequest,
    ProjectListResponse
)

load_dotenv()

router = APIRouter(prefix="/projects", tags=["Projects"])


# Admin authorization
def verify_admin(
    admin_key: str = Header(..., alias="X-Admin-Key")
):
    expected_key = os.getenv("ADMIN_API_KEY")

    if not expected_key or not secrets.compare_digest(
        admin_key, expected_key
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin authorization failed"
        )


# Submit a new project
@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED
)
def submit_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db)
):
    new_project = ProjectSubmission(
        title=project_data.title,
        description=project_data.description,
        domain=project_data.domain,
        github_url=str(project_data.github_url),
        demo_url=str(project_data.demo_url)
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project


# Search, filter and paginate projects
@router.get("/", response_model=ProjectListResponse)
def list_projects(
    search: str = Query(default="", max_length=150),
    domain: str | None = None,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(ProjectSubmission)

    if search:
        query = query.filter(
            or_(
                ProjectSubmission.title.ilike(f"%{search}%"),
                ProjectSubmission.description.ilike(f"%{search}%")
            )
        )

    if domain:
        query = query.filter(
            ProjectSubmission.domain.ilike(domain)
        )

    total_items = query.count()
    total_pages = (total_items + limit - 1) // limit

    projects = (
        query.order_by(ProjectSubmission.created_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "total_items": total_items,
        "total_pages": total_pages,
        "current_page": page,
        "page_size": limit,
        "projects": projects
    }


# Admin moderation
@router.patch(
    "/{project_id}/moderate",
    response_model=ProjectResponse
)
def moderate_project(
    project_id: int,
    moderation: ModerationRequest,
    _admin: None = Depends(verify_admin),
    db: Session = Depends(get_db)
):
    project = db.query(ProjectSubmission).filter(
        ProjectSubmission.id == project_id
    ).first()

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    project.status = moderation.status
    project.feedback_remarks = moderation.feedback_remarks

    db.commit()
    db.refresh(project)

    return project


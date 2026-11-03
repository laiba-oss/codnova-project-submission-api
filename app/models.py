from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base


class ProjectSubmission(Base):
    __tablename__ = "project_submissions"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    domain = Column(String(100), nullable=False)

    github_url = Column(String(500), nullable=False)
    demo_url = Column(String(500), nullable=False)

    status = Column(
        String(20),
        nullable=False,
        default="Pending"
    )

    feedback_remarks = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now()
    )
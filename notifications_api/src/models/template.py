import uuid

from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID

# from sqlalchemy.orm import relationship

from src.db.postgres import Base

# from src.models.role_permission import RolePermission


class Template(Base):
    """Model representing a notification template."""

    __tablename__ = "templates"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = Column(String(255), nullable=False, unique=True)
    description = Column(String(500))
    template_content = Column(Text, nullable=False)

    def __repr__(self) -> str:
        """String representation of the Template object."""
        return f"<Template {self.name}>"

from uuid import UUID
from pydantic import BaseModel


class NotificationCreate(BaseModel):
    """Schema for creating a new template."""

    name: str
    description: str | None = None
    template_content: str


class Notification(BaseModel):
    """Schema for representing a template."""

    id: UUID
    name: str
    description: str | None
    template_content: str

    class Config:
        from_attributes = True

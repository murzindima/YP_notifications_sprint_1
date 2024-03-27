from uuid import UUID
from pydantic import BaseModel


class NotificationCreate(BaseModel):
    """Schema for creating a new template."""

    template_id: UUID | str
    template_content: dict
    template_rendered: str | None = None
    recipient_email: str


class Notification(BaseModel):
    """Schema for representing a template."""

    id: UUID
    recipient_email: str
    template_id: UUID | str
    template_content: dict
    template_rendered: str | None

    class Config:
        from_attributes = True

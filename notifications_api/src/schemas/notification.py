from uuid import UUID
from pydantic import BaseModel


class NotificationCreate(BaseModel):
    """Schema for creating a new template."""

    template_id: UUID | str
    context: dict
    recipients: list[str]


class Notification(BaseModel):
    """Schema for representing a template."""

    id: UUID
    recipients: list[str]
    template_id: UUID | str
    context: dict

    class Config:
        from_attributes = True

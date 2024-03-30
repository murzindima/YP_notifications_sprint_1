from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel


class NotificationType(StrEnum):
    """Enum for notification types."""

    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"


class NotificationCreate(BaseModel):
    """Schema for creating a new template."""

    template_id: UUID | str
    context: dict
    recipients: list[str]
    notification_type: NotificationType


class Notification(BaseModel):
    """Schema for representing a template."""

    id: UUID
    recipients: list[str]
    template_id: UUID | str
    context: dict

    class Config:
        from_attributes = True

import enum
import uuid

from sqlalchemy import Column, String, Text, DateTime, func, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID

from src.db.postgres import Base


# from sqlalchemy.orm import relationship

# from src.models.role_permission import RolePermission


class DeliveryStatus(enum.Enum):
    pending = "pending"
    sent = "sent"
    failed = "failed"


class Notification(Base):
    """Model representing an individual notification."""

    __tablename__ = "notifications"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    recipients = Column(JSON, nullable=False)
    template_id = Column(UUID(as_uuid=True), nullable=False)
    context = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    sent_at = Column(DateTime(timezone=True))
    status = Column(
        Enum(DeliveryStatus), default=DeliveryStatus.pending, nullable=False
    )

    def __repr__(self) -> str:
        """String representation of the Notification object."""
        return f"<Notification to {self.recipient_email}>"

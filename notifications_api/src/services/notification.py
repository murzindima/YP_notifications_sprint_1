from functools import lru_cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres import get_session
from src.models.notification import Notification as NotificationModel
from src.schemas.notification import Notification as NotificationSchema
from src.services.base import BaseService
from src.services.data_repository.postgres import PostgresService


class NotificationService(BaseService):
    """Service class for managing roles, extending the BaseService."""


@lru_cache
def get_notification_service(
    pg_session: AsyncSession = Depends(get_session),
) -> NotificationService:
    """Dependency function to get an instance of the NotificationService."""
    return NotificationService(
        model_schema_class=NotificationSchema,
        postgres_service=PostgresService(
            session=pg_session, model_class=NotificationModel
        ),
    )

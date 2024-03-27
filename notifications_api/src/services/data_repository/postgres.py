from uuid import UUID

from src.services.data_repository.postgres_crud import PostgresCrudService
from src.models.notification import Notification as NotificationModel


class PostgresService(PostgresCrudService):
    """A data storage service implementation for working with Postgres."""

    async def get_notification(self, notification_id: UUID) -> NotificationModel | None:
        """Retrieve a role."""
        async with self.session.begin():
            model = await self.session.get(NotificationModel, notification_id)
            return model

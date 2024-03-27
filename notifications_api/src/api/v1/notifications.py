from fastapi import APIRouter, Depends, status

from src.schemas.notification import Notification as NotificationSchema
from src.schemas.notification import NotificationCreate as NotificationCreateSchema
from src.services.notification import NotificationService, get_notification_service

router = APIRouter()


@router.post(
    "/", response_model=NotificationSchema, status_code=status.HTTP_201_CREATED
)
async def create_notifications(
    notification: NotificationCreateSchema,
    notification_service: NotificationService = Depends(get_notification_service),
) -> NotificationSchema:
    """Creates a new notification."""
    notification = await notification_service.create_model(notification)
    return notification

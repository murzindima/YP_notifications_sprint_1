from fastapi import APIRouter, Depends, status, HTTPException

from src.schemas.notification import Notification as NotificationSchema
from src.schemas.notification import NotificationCreate as NotificationCreateSchema
from src.services.notification import NotificationService, get_notification_service

router = APIRouter()


@router.post(
    "/", response_model=NotificationSchema, status_code=status.HTTP_201_CREATED
)
async def create_notification(
    notification: NotificationCreateSchema,
    notification_service: NotificationService = Depends(get_notification_service),
) -> NotificationSchema:
    """Creates a new notification."""
    template = await notification_service.get_model_by_id(notification.template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    notification_id = await notification_service.create_model(notification)

    return {"notification_id": notification_id, "message": "Notification queued."}

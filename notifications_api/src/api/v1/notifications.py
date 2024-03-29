from fastapi import APIRouter, Depends, status, HTTPException

from src.schemas.notification import Notification as NotificationSchema
from src.schemas.notification import NotificationCreate as NotificationCreateSchema
from src.services.notification import NotificationService, get_notification_service
from src.services.rabbitmq import RabbitMQPublisherService
from src.services.template import TemplateService, get_template_service

rabbitmq_service = RabbitMQPublisherService()

router = APIRouter()


@router.post(
    "/", response_model=NotificationSchema, status_code=status.HTTP_201_CREATED
)
async def create_notification(
    notification: NotificationCreateSchema,
    notification_service: NotificationService = Depends(get_notification_service),
    template_service: TemplateService = Depends(get_template_service),
) -> NotificationSchema:
    """Creates a new notification."""
    template = await template_service.get_model_by_id(notification.template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    created_notification = await notification_service.create_model(notification)

    message_body = {
        "notification_id": str(created_notification.id),
        "recipients": notification.recipients,
        "template": template.template,
        "context": notification.context,
    }
    await rabbitmq_service.publish_message(
        exchange_name="notifications", routing_key="notifications", message=message_body
    )

    return created_notification

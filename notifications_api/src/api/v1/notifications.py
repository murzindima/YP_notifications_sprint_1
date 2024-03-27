from fastapi import APIRouter, Depends, status, HTTPException

from src.schemas.notification import Notification as NotificationSchema
from src.schemas.notification import NotificationCreate as NotificationCreateSchema
from src.services.notification import NotificationService, get_notification_service
from src.services.template import TemplateService, get_template_service

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
    template_raw = await template_service.get_model_by_id(str(notification.template_id))
    if not template_raw:
        raise HTTPException(status_code=404, detail="Template not found")

    from jinja2 import Template
    template = Template(template_raw.template_content)
    template_rendered = template.render(**notification.template_content)
    notification.template_rendered = template_rendered

    notification = await notification_service.create_model(notification)

    return notification

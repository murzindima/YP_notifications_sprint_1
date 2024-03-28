import json

import aio_pika
from fastapi import APIRouter, Depends, status, HTTPException
from jinja2 import Template

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
    template_raw = await template_service.get_model_by_id(notification.template_id)
    if not template_raw:
        raise HTTPException(status_code=404, detail="Template not found")

    template = Template(template_raw.template_content)
    template_rendered = template.render(**notification.template_content)

    notification.template_rendered = template_rendered

    created_notification = await notification_service.create_model(notification)

    connection = await aio_pika.connect_robust("amqp://user:password@rabbitmq/")
    async with connection:
        channel = await connection.channel()

        exchange = await channel.declare_exchange(
            "emails12", aio_pika.ExchangeType.DIRECT, durable=True
        )
        queue = await channel.declare_queue("welcome23", durable=True)
        await queue.bind(exchange, "welcome23")

        message_body = json.dumps(
            {
                "recipient_email": notification.recipient_email,
                "template_rendered": template_rendered,
            }
        ).encode()

        message = aio_pika.Message(
            body=message_body, delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )

        await exchange.publish(message, routing_key="welcome23")

    return created_notification

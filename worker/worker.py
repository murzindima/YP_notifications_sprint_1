import asyncio
import json

import aio_pika
import aiohttp
import asyncpg
from jinja2 import Template

from base import EmailSender
from config import settings, logger

email_sender = EmailSender()
# sms_sender = SMSSender()
# push_sender = PushSender()


notification_senders = {
    "email": email_sender,
    #    'sms': sms_sender,
    #    'push': push_sender,
}


class RabbitMQConsumer:
    def __init__(self, queue_name: str, rabbitmq_host: str = "localhost") -> None:
        self.queue_name = queue_name
        self.rabbitmq_host = rabbitmq_host

    async def consume(self, callback: callable) -> None:
        connection = await aio_pika.connect_robust(
            f"amqp://user:password@{self.rabbitmq_host}/"
        )

        async with connection:
            channel = await connection.channel()
            await channel.set_qos(prefetch_count=100)

            queue = await channel.declare_queue(self.queue_name, durable=True)

            async for message in queue:
                async with message.process():
                    await callback(message.body)


async def get_admin_jwt_token() -> dict[str, any]:
    try:
        async with aiohttp.ClientSession() as session:
            response = await session.post(
                settings.login_url, json=settings.admin_credentials
            )
            if response.status == 200:
                return await response.json()
            else:
                logger.error(
                    "Failed to get admin JWT token. Status code: %s", response.status
                )
                return {}
    except aiohttp.ClientError as e:
        logger.error("Error getting admin JWT token: %s", str(e))
        return {}


async def get_user_info(user_id: str, headers: dict[str, str]) -> dict[str, any]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                settings.user_url + user_id, headers=headers
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(
                        "Failed to get user info. Status code: %s", response.status
                    )
                    return {}
    except aiohttp.ClientError as e:
        logger.error("Error getting user info: %s", str(e))
        return {}


async def update_notification_status(notification_id: str, new_status: str) -> None:
    try:
        conn = await asyncpg.connect(settings.dsn)
    except asyncpg.exceptions.PostgresError as e:
        logger.error("Error connecting to database: %s", str(e))
        return
    try:
        await conn.execute(
            "UPDATE notifications SET status = $1 WHERE id = $2",
            new_status,
            notification_id,
        )
        logger.info("Notification status updated successfully")
    except asyncpg.exceptions.PostgresError as e:
        logger.error("Error updating notification status: %s", str(e))
    finally:
        await conn.close()


async def form_and_send_message(
    user_id: str,
    headers: dict[str, str],
    template: str,
    context: dict[str, any],
    notification_type: str,
):
    user = await get_user_info(user_id, headers)
    if user:
        template = Template(template)
        rendered_message = template.render(context)
        subject = "Subject"

        sender = notification_senders.get(notification_type)

        if not sender:
            logger.error(f"Unsupported notification type: {notification_type}")
            return

        if notification_type == "email":
            recipient = user["email"]
        elif notification_type == "sms":
            recipient = user[
                "phone"
            ]
        elif notification_type == "push":
            recipient = user[
                "device_id"
            ]
        else:
            logger.error(f"Unsupported notification type: {notification_type}")
            return

        await sender.send(recipient, subject, rendered_message)
    else:
        logger.error("Failed to obtain user info")


async def process_message(body: str) -> None:
    try:
        message_data = json.loads(body)
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding message body: {str(e)}")
        return
    try:
        admin_jwt_token = await get_admin_jwt_token()
        headers = {"Authorization": "Bearer " + admin_jwt_token["access_token"]}
        notification_type = message_data.get("notification_type", "email")
        for recipient in message_data["recipients"]:
            await form_and_send_message(
                recipient,
                headers,
                message_data["template"],
                message_data["context"],
                notification_type,
            )
        await update_notification_status(message_data["notification_id"], "sent")
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        await update_notification_status(message_data["notification_id"], "failed")


async def main() -> None:
    consumer = RabbitMQConsumer(settings.queue_name, settings.rabbitmq_host)
    logger.info("Starting worker")
    await consumer.consume(process_message)


if __name__ == "__main__":
    asyncio.run(main())

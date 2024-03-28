import json
from typing import Any, Dict

import aio_pika

from src.core.config import rabbitmq_settings as rmq


class RabbitMQPublisherService:
    def __init__(
        self,
        amqp_url: str = f"amqp://{rmq.username}:{rmq.password}@{rmq.host}:{rmq.port}/",
    ):
        self._amqp_url = amqp_url
        self._connection = None
        self._channel = None

    async def _ensure_connected(self):
        if not self._connection or self._connection.is_closed:
            self._connection = await aio_pika.connect_robust(self._amqp_url)
        if not self._channel or self._channel.is_closed:
            self._channel = await self._connection.channel()

    async def publish_message(
        self, exchange_name: str, routing_key: str, message: Dict[str, Any]
    ) -> None:
        await self._ensure_connected()

        exchange = await self._channel.declare_exchange(
            exchange_name, aio_pika.ExchangeType.DIRECT, durable=True
        )
        queue = await self._channel.declare_queue(routing_key, durable=True)
        await queue.bind(exchange, routing_key)

        message_body = json.dumps(message).encode()
        message = aio_pika.Message(
            body=message_body, delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )

        await exchange.publish(message, routing_key=routing_key)

    async def close(self):
        if self._channel:
            await self._channel.close()
        if self._connection:
            await self._connection.close()

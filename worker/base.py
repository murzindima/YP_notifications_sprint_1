from abc import ABC, abstractmethod
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib

from config import settings, logger


class NotificationSender(ABC):
    @abstractmethod
    async def send(self, recipient: str, subject: str, body: str):
        pass


class SMSSender(NotificationSender):
    async def send(self, recipient: str, subject: str, body: str):
        pass


class PushSender(NotificationSender):
    async def send(self, recipient: str, subject: str, body: str):
        pass


class EmailSender(NotificationSender):
    async def send(self, recipient: str, subject: str, body: str):
        message = MIMEMultipart()
        message["From"] = settings.smtp_username
        message["To"] = recipient
        message["Subject"] = subject
        message.attach(MIMEText(body, "html"))

        try:
            await aiosmtplib.send(
                message,
                hostname=settings.smtp_server,
                port=settings.smtp_port,
                username=settings.smtp_username,
                password=settings.smtp_password,
                use_tls=True,
            )
            logger.info(f"Email sent successfully to {recipient}")
        except Exception as e:
            logger.error(f"Error sending email to {recipient}: {str(e)}")

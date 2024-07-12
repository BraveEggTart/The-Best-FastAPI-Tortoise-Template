import logging

from fastapi import APIRouter
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from app.schemas.response import Success
from app.config import settings

logger = logging.getLogger(__name__)
routes = APIRouter()

mail_conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USER,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=False,
)

mail = FastMail(mail_conf)


@routes.get(
    "/email",
    tags=["General"],
    summary="邮件",
    description="发送邮件",
    response_model=Success,
)
async def simple_send():
    html = """
    <p>Thanks for using Fastapi-mail</p> 
    """
    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=["xx@xx.com"],
        body=html,
        subtype=MessageType.html)

    await mail.send_message(message)
    return Success()

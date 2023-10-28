from celery import shared_task
from celery.utils.log import get_task_logger

from src.user.email import send_reset_password_email


logger = get_task_logger(__name__)


@shared_task(name="send_reset_password_email_task")
def send_reset_password_email_task(reset_password_url: str, email: str):
    """
    Celery task for sending reset password email asynchronously. 
    """
    logger.info("Sending reset password email")
    return send_reset_password_email(reset_password_url, email)

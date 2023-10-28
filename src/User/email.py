from django.core.mail import send_mail

from core.settings import EMAIL_HOST_USER


def send_reset_password_email(reset_password_url: str, email: str) -> None:
    """
    Function to send reset password email.
    """
    subject = "Reset password"
    message = f"Click here to reset your password: {reset_password_url}"
    from_email = EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)

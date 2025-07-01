from django.core.mail import EmailMessage, EmailMultiAlternatives
from backend.core.services.email.base import EmailService

class DjangoEmailService(EmailService):

    def send_email(self, subject, content, from_email, to, content_type):
        message = EmailMessage(
            subject=subject,
            body=content,
            from_email=from_email,
            to=to
        )
        subtype = content_type.split("/")[1]
        message.content_subtype = subtype

        message.send()

    def send_multipart_email(self, subject, from_email, to, content):
        message = EmailMultiAlternatives(
            subject=subject,
            body="",
            from_email=from_email,
            to=to
        )
        for email_content in content:
            message.attach_alternative(email_content["content"], email_content["content_type"])

        message.send()
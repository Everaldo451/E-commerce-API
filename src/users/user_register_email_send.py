from backend.core.services.email.base import EmailService, EmailContentPart

class UserRegisterEmailSend:

    def __init__(self, email_service:EmailService):
        self.email_service = email_service

    def send(self, username:str ,email:str):
        text_content:EmailContentPart = {
            "content_type": "text/plain",
            "content": f"Welcome to our E-commerce, {username}"
        }
        html_content:EmailContentPart = {
            "content_type": "text/html",
            "content": f""
        }
        self.email_service.send_multipart_email(
            "Confirm your email",
            from_email="",
            to=[email],
            content=[text_content, html_content]
        )
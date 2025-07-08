from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.core.services.email.implementations.django import DjangoEmailService
from backend.core.permissions import IsNotAuthenticated, IsCurrentUserOrAdmin

from .models import User
from .serializer import UserSerializer
from .user_register_email_send import UserRegisterEmailSend

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action=="create":
            return [IsNotAuthenticated()]
        return [
            permissions.IsAuthenticated(),
            IsCurrentUserOrAdmin()
        ]
    
    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated or user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=user.id)
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        email = response.data.get("email")
        username = response.data.get("username")

        django_email_service = DjangoEmailService()
        register_email_send = UserRegisterEmailSend(django_email_service)
        try:
            register_email_send.send(username, email)
        except Exception as error:
            django_email_service.error_handler(error)

        return response

    @action(detail=False, methods=["GET"], permission_classes=(permissions.IsAuthenticated,))
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

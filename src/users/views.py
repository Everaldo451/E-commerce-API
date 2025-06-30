from rest_framework import viewsets, permissions
from rest_framework.request import Request
from .models import User
from .serializer import UserSerializer

class IsAdminOrPostMethod(permissions.BasePermission):
    def has_permission(self, request:Request, view):
        return (request.user.is_authenticated and request.user.is_staff) or request.method=="POST"
    

class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrPostMethod,)

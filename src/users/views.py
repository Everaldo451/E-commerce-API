from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User
from .serializer import UserSerializer

class IsNotAuthenticatedAndPostMethod(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_authenticated and request.method=="POST"
    

class IsCurrentUserOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj == request.user
    

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        (permissions.IsAuthenticated & IsCurrentUserOrAdmin) | IsNotAuthenticatedAndPostMethod,
    )

    @action(detail=False, methods=["GET"], permission_classes=(permissions.IsAuthenticated,))
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

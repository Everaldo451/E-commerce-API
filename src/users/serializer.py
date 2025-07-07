from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'is_staff']
        read_only_fields = ['id', 'is_staff']
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["email"], 
            validated_data["first_name"],
            validated_data["last_name"],
            validated_data["password"],
            username=validated_data["username"]
        )
        return user
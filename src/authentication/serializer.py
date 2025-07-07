from rest_framework import serializers
from django.contrib.auth import authenticate
from users.serializer import UserSerializer

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(write_only=True)

    def validate(self, data):

        email = data.get("email")
        password = data.get("password")

        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError('Invalid email or password credentials.')
        data['user'] = user
        return data
    

class LoginResponseSerializer(serializers.Serializer):
    user = UserSerializer()
    tokens = serializers.DictField(
        child=serializers.DictField(), 
        allow_empty=False
    )

class RefreshResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()
    

class LogoutResponseSerializer(serializers.Serializer):
    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()
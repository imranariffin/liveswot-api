import re

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework import status

from .models import User


email_validation = {'max_length': 255}
password_validation = {
    'max_length': 128,
    'min_length': 8,
    'write_only': True,
}
token_validation = {'max_length': 255, 'read_only': True}


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.CharField(**email_validation)
    password = serializers.CharField(**password_validation)
    token = serializers.CharField(**token_validation)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'token']

    def validate(self, data):
        # return super(RegistrationSerializer, self).validate(data)

        email = data.get('email', None)

        emailregex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(emailregex, email):
            raise serializers.ValidationError(
                detail='Email is not valid',
                code=status.HTTP_400_BAD_REQUEST)

        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255, read_only=True)
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(**token_validation)

    class Meta:
        model = User
        fields = ['email', 'username', 'email', 'password', 'token']

    def validate(self, data):

        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                detail='An email address is required to login',
                code=status.HTTP_400_BAD_REQUEST
            )

        if password is None:
            raise serializers.ValidationError(
                detail='A password is required to login',
                code=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                detail='There is no such user with the email and password',
                code=status.HTTP_404_NOT_FOUND)

        if not user.is_active:
            raise serializers.ValidationError(
                detail='The user is inactive',
                code=status.HTTP_403_FORBIDDEN)

        return {
            'email': user.email,
            'username': user.username,
            'token': user.token,
        }

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.contrib.auth.hashers import check_password

from .models import User
from .validators import validate_signup, validate_login

from .serializers import deserialize, serialize_response


@api_view(['POST'])
@deserialize
@validate_signup
def signup(request):
    email = request.body['user']['email']
    username = request.body['user']['username']
    password = request.body['user']['password']
    user = None

    try:
        user = User.objects.get(username=username)
        return Response({
            'data': {
                'errors': ['Username `{}` already exist'.format(username)]
            }
        }, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        pass

    try:
        user = User.objects.create_user(
            email=email,
            password=password,
            username=username)
        user.save()
    except:
        return Response({
            'errors': ['Error occurred when creating user']
        }, status=status.HTTP_400_BAD_REQUEST)

    return Response({
        'data': {
            'user': {
                'email': user.email,
                'username': user.username,
                'token': user.token,
            }
        }
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@deserialize
@validate_login
@serialize_response
def login(request):
    email = request.body['user']['email']
    password = request.body['user']['password']
    user = None

    email_password_error_msg = 'There is no such user with the email and password'
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return (
            None,
            status.HTTP_400_BAD_REQUEST,
            [email_password_error_msg],
        )

    if not check_password(password, user.password):
        return (
            None,
            status.HTTP_400_BAD_REQUEST,
            [email_password_error_msg],
        )

    return (
        user,
        status.HTTP_200_OK,
        None
    )
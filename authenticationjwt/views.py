from rest_framework import status
from rest_framework.decorators import api_view

from django.contrib.auth.hashers import check_password

from .models import User
from swot_members.models import SwotMember, Invite
from .validators import validate_signup, validate_login

from .serializers import deserialize, serialize_response


@api_view(['POST'])
@deserialize
@validate_signup
@serialize_response
def signup(request):
    email = request.body['user']['email']
    username = request.body['user']['username']
    password = request.body['user']['password']
    user = None

    try:
        User.objects.get(username=username)
        return (
            None,
            status.HTTP_400_BAD_REQUEST,
            ['Username `{}` already exist'.format(username)],
        )
    except User.DoesNotExist:
        pass

    try:
        user = User.objects.create_user(
            email=email,
            password=password,
            username=username)
        user.save()
    except:
        return (
            None,
            status.HTTP_400_BAD_REQUEST,
            ['Error occurred when creating user'],
        )

    # convert all invitations to membership
    for inv in Invite.objects.filter(email=email):
        try:
            SwotMember.objects.create(
                member_id=user.id,
                added_by_id=inv.added_by_id,
                swot_id=inv.swot_id
            )
        except:
            pass

    return (
        user,
        status.HTTP_201_CREATED,
        None
    )


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
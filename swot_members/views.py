from django.db import IntegrityError

from rest_framework.decorators import api_view
from rest_framework import status

from core.serializers import deserialize
from core.decorators import authenticate

from swot.models import Swot

from .utils import send_invite_email
from .models import SwotMember, Invite
from .serializers import serialize

from authenticationjwt.models import User


@api_view(['POST'])
@authenticate
@deserialize
@serialize
def add_members(request, swot_id, email):
    user_id = int(request.user.id)
    swot_id = int(swot_id)
    swot = None
    user_to_add = None

    try:
        user_to_add = User.objects.get(email=email)
    except User.DoesNotExist:
        Invite.objects.create(
            email=email,
            added_by_id=user_id,
            swot_id=swot_id
        )
        send_invite_email(request.user.email, email)
        return (
            None,
            status.HTTP_204_NO_CONTENT,
            None
        )

    try:
        swot = Swot.objects.get(id=swot_id)
    except Swot.DoesNotExist:
        err_msg = 'Cannot add user `{}` to non-existing swot `{}`'
        return (
            None,
            status.HTTP_404_NOT_FOUND,
            [err_msg.format(email, swot_id)]
        )

    if swot.created_by_id != user_id:
        return (
            None,
            status.HTTP_403_FORBIDDEN,
            ['Not allowed']
        )

    swot_member = None
    try:
        swot_member = SwotMember.objects.create(
            added_by_id=user_id,
            member_id=user_to_add.id,
            swot_id=swot_id
        )
    except IntegrityError, ie:
        return None, status.HTTP_400_BAD_REQUEST, [ie.message]

    return swot_member, status.HTTP_201_CREATED, None


@api_view(['GET'])
@authenticate
@deserialize
@serialize
def get_members(request, swot_id):
    user_id = int(request.user.id)
    swot_id = int(swot_id)

    try:
        Swot.objects.get(id=swot_id)
    except Swot.DoesNotExist, sdne:
        return None, status.HTTP_404_NOT_FOUND, [sdne.message]

    members = [member for member in SwotMember.objects.filter(swot_id=swot_id)]

    if user_id not in set([m.member_id for m in members]):
        return None, status.HTTP_403_FORBIDDEN, ['Not a member']

    return (
        members,
        status.HTTP_200_OK,
        None
    )
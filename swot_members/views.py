from django.db import IntegrityError

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from core.serializers import deserialize
from core.decorators import authenticate

from swot.models import Swot

from .models import SwotMember

from authenticationjwt.models import User


def serialize(func):

    def serialize_member(data):
        if data is None:
            return {}

        return {
            'membershipId': data.id,
            'memberId': data.member_id,
            'swotId': data.swot_id,
            'addedById': data.added_by_id,
            'created': data.created
        }

    def _serialize(request, *args, **kwargs):
        data, status, errors = func(request, *args, **kwargs)

        if errors:
            return Response({
                'errors': errors
            }, status=status)

        return Response({
            'data': serialize_member(data),
        }, status=status)

    return _serialize


@api_view(['POST'])
@authenticate
@deserialize
@serialize
def get_add_members(request, swot_id, member_id):
    user_id = request.user.id
    swot = None

    try:
        User.objects.get(id=member_id)
    except User.DoesNotExist:
        err_msg = 'Cannot add non-existing user `{}` to swot `{}`'
        return (
            None,
            status.HTTP_404_NOT_FOUND,
            [err_msg.format(member_id, swot_id)]
        )

    try:
        swot = Swot.objects.get(id=swot_id)
    except Swot.DoesNotExist:
        err_msg = 'Cannot add user `{}` to non-existing swot `{}`'
        return (
            None,
            status.HTTP_404_NOT_FOUND,
            [err_msg.format(member_id, swot_id)]
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
            member_id=member_id,
            swot_id=swot_id
        )
    except IntegrityError, ie:
        return None, status.HTTP_400_BAD_REQUEST, ie.message

    return swot_member, status.HTTP_201_CREATED, None

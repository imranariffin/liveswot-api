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


@api_view(['GET', 'POST'])
@authenticate
@deserialize
@serialize
def get_add_members(request, swot_id, member_id):
    user_id = request.user.id
    swot = None

    try:
        User.objects.get(id=member_id)
    except User.DoesNotExist:
        return (
            None,
            status.HTTP_404_NOT_FOUND,
            ['User does not exist']
        )

    try:
        swot = Swot.objects.get(id=swot_id)
    except Swot.DoesNotExist:
        return (
            None,
            status.HTTP_404_NOT_FOUND,
            ['Swot does not exist']
        )

    if swot.created_by_id != user_id:
        return (
            None,
            status.HTTP_403_FORBIDDEN,
            ['']
        )

    swot_member = None
    try:
        SwotMember.objects.create(
            added_by_id=user_id,
            member_id=member_id,
            swot_id=swot_id
        )
    except IntegrityError, ie:
        return None, status.HTTP_400_BAD_REQUEST, ie.message

    return swot_member, status.HTTP_201_CREATED, None

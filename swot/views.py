from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.decorators import api_view

from swot.models import Swot
from swot.serializers import serialize

from core.decorators import authenticate
from core.serializers import deserialize
from swot_members.models import SwotMember


@api_view(['GET', 'POST'])
@authenticate
@deserialize
@serialize
def swot_list(request):
    if request.method == 'GET':
        user = request.user
        swots = Swot.objects.filter(created_by_id=user.id)

        return (
            [swot for swot in swots],
            status.HTTP_200_OK,
            None
        )

    swot = None
    user_id = request.user.id
    title = request.body['title']
    description = request.body['title']

    try:
        swot = Swot(created_by_id=user_id, title=title, description=description)
        swot.save()
    except:
        return (
            None,
            status.HTTP_400_BAD_REQUEST,
            ['Error occured when creating swot']
        )

    # creator automatically becomes member of swot
    SwotMember.objects.create(
        member_id=user_id,
        swot_id=swot.id,
        added_by_id=user_id,
    ).save()

    return (
        swot,
        status.HTTP_201_CREATED,
        None,
    )


@api_view(['PUT', 'DELETE'])
@authenticate
@deserialize
@serialize
def swot_detail(request, swot_id):
    swot_id = int(swot_id)
    swot = None

    try:
        swot = Swot.objects.get(id=swot_id)
    except ObjectDoesNotExist:
        return (
            None,
            status.HTTP_404_NOT_FOUND,
            ['Swot id={} does not exist'],
        )

    user_id = request.user.id
    creator_id = swot.created_by_id

    if user_id != creator_id:
        return (
            None,
            status.HTTP_403_FORBIDDEN,
            ['Only creator can delete swot']
        )

    if request.method == 'DELETE':
        try:
            swot.delete()
        except:
            return (
                None,
                status.HTTP_400_BAD_REQUEST,
                ['Error occurred when deleting swot {}'.format(swot_id)]
            )

        return (
            None,
            status.HTTP_204_NO_CONTENT,
            None,
        )

    else:
        data = request.body
        if 'title' in data:
            swot.title = data['title']
        if 'description' in data:
            swot.description = data['description']

        try:
            swot.save()
        except:
            return (
                None,
                status.HTTP_400_BAD_REQUEST
                ['Error occurred when updating Swot {}'.format(swot_id)]
            )

        return (
            swot,
            status.HTTP_200_OK,
            None,
        )

from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from swot.models import Swot
from swot.serializers import SwotSerializer

from core.decorators import authenticate
from core.serializers import deserialize


@api_view(['GET', 'POST'])
@authenticate
@deserialize
def swot_list(request):
    if request.method == 'GET':
        user = request.user
        swots = Swot.objects.filter(created_by_id=user.id)
        serialized = [{
            'swotId': swot.id,
            'creatorId': user.id,
            'title': swot.title,
            'description': swot.description,
        } for swot in swots]

        return Response(
            {'data': serialized},
            status=status.HTTP_200_OK
        )

    user_id = request.user.id
    title = request.body['title']
    description = request.body['title']

    try:
        swot = Swot(created_by_id=user_id, title=title, description=description)
        swot.save()
    except:
        return Response({
            'errors': ['Error occured when creating swot']
        }, status=status.HTTP_400_BAD_REQUEST)

    return Response({
        'data': {
            'swotId': swot.id,
            'creatorId': swot.created_by_id,
            'title': swot.title,
            'description': swot.description,
        }
    }, status=status.HTTP_201_CREATED)


@api_view(['PUT', 'DELETE'])
@authenticate
@deserialize
def swot_detail(request, swot_id):
    swot_id = int(swot_id)
    swot = None

    try:
        swot = Swot.objects.get(id=swot_id)
    except ObjectDoesNotExist:
        return Response(
            {'errors': ['Swot id={} does not exist']},
            status=status.HTTP_404_NOT_FOUND
        )

    user_id = request.user.id
    creator_id = swot.created_by_id

    if user_id != creator_id:
        return Response({
            'errors': ['Only creator can delete swot']
        }, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'DELETE':
        try:
            swot.delete()
        except:
            return Response({
                'errors': ['Error occurred when deleting swot {}'.format(swot_id)],
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {'data': {}},
            status=status.HTTP_204_NO_CONTENT
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
            return Response({
                'errors': ['Error occurred when updating Swot {}'.format(swot_id)],
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'data': {
                'swotId': swot.id,
                'creatorId': swot.created_by_id,
                'title': swot.title,
                'description': swot.description,
            }
        }, status=status.HTTP_200_OK)


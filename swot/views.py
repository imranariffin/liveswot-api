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
        swots = Swot.objects.filter(owner_id=user.id)
        serialized = [SwotSerializer(swot).data for swot in swots]

        return Response(
            {'data': serialized},
            status=status.HTTP_200_OK
        )

    user_id = request.user.id
    title = request.body['title']
    description = request.body['title']
    swot = None

    try:
        swot = Swot(owner_id=user_id, title=title, description=description)
        swot.save()
    except:
        return Response({
            'errors': ['Error occured when creating swot']
        }, status=status.HTTP_400_BAD_REQUEST)

    return Response({
        'data': {
            'swotId': swot.id,
            'userId': user_id,
            'title': title,
            'description': description,
        }
    }, status=status.HTTP_201_CREATED)


@api_view(['PUT', 'DELETE'])
@authenticate
@deserialize
def swot_detail(request, swot_id):
    return Response({}, status=status.HTTP_200_OK)
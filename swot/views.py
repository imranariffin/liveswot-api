from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from swot.models import Swot
from swot.serializers import SwotSerializer
from core.decorators import authenticate


@api_view(['GET', 'POST'])
@authenticate
def swot_list(request):
    if request.method == 'GET':
        user = request.user
        swots = Swot.objects.filter(owner_id=user.id)
        serialized = [SwotSerializer(swot).data for swot in swots]

        return Response(
            {'data': serialized},
            status=status.HTTP_200_OK
        )

    return Response({}, status=status.HTTP_201_CREATED)
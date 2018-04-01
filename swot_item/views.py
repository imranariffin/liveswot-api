from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from swot_item.models import SwotItem
from swot_item.serializers import SwotItemSerializer, serialize_request
from swot_item.validators import validate

from core.serializers import deserialize

from core.decorators import authenticate


@api_view(http_method_names=['GET', 'POST'])
@authenticate
@deserialize
@validate
def swot_item_list(request):
    if request.method == 'GET':
        swots = SwotItem.objects.all()
        serialized = [SwotItemSerializer(swot).data for swot in swots]
        return Response({'data': serialized})
    else:
        data = request.body

        card_type = data['cardType']
        text = data['text']

        swot_item = SwotItem.objects.create(cardType=card_type, text=text, )
        serialized = SwotItemSerializer(swot_item).data

        return Response({'data': serialized}, status=status.HTTP_201_CREATED)


@api_view(['PUT', 'DELETE'])
@authenticate
@deserialize
@validate
def swot_item_detail(request, swot_item_id):
    swot_item_id = int(swot_item_id)

    try:
        swot = SwotItem.objects.get(id=swot_item_id)
    except SwotItem.DoesNotExist as dne:
        return Response({'errors': [dne.message]}, status=status.HTTP_404_NOT_FOUND)

    user_id = request.user.id

    if swot.created_by_id != user_id:
        return Response({
            'errors': ['Only creator can update Swot Item']
        }, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        data = request.body

        if 'text' in data:
            swot.text = data['text']

        try:
            swot.save()
        except ValueError as ve:
            return Response({'errors': [ve.message]}, status=status.HTTP_400_BAD_REQUEST)

        try:
            serialized = SwotItemSerializer(swot).data
        except ValidationError as ve:
            return Response({'errors': [msg for msg in ve.detail]})

        return Response({'data': serialized}, status=status.HTTP_200_OK)

from rest_framework.decorators import api_view
from rest_framework import status

from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from swot_item.models import SwotItem
from swot_item.serializers import SwotItemSerializer
from swot_item.validators import validate

from core.serializers import deserialize

from core.decorators import authenticate


@api_view(http_method_names=['GET', 'POST'])
@authenticate
@deserialize
@validate
def swot_item_list(request, swot_id):
    swot_id = int(swot_id)

    if request.method == 'GET':
        swot_items = SwotItem.objects.filter(swot_id=swot_id)
        serialized = [{
            'swotItemId': swot_item.id,
            'swotId': swot_item.swot_id,
            'creatorId': swot_item.created_by_id,
            'text': swot_item.text,
            'cardType': swot_item.cardType,
            'score': swot_item.score,
        } for swot_item in swot_items]
        return Response({'data': serialized})
    else:
        data = request.body

        card_type = data['cardType']
        text = data['text']
        user_id = request.user.id

        swot_item = SwotItem.objects.create(swot_id=swot_id,
                                            created_by_id=user_id,
                                            text=text,
                                            cardType=card_type)

        return Response({'data': {
            'swotItemId': swot_item.id,
            'swotId': swot_item.swot_id,
            'creatorId': swot_item.created_by_id,
            'text': swot_item.text,
            'cardType': swot_item.cardType,
            'score': swot_item.score,
        }}, status=status.HTTP_201_CREATED)


@api_view(['PUT', 'DELETE'])
@authenticate
@deserialize
@validate
def swot_item_detail(request, swot_item_id):
    swot_item_id = int(swot_item_id)
    swot_item = None

    try:
        swot_item = SwotItem.objects.get(id=swot_item_id)
    except SwotItem.DoesNotExist as dne:
        return Response({'errors': [dne.message]}, status=status.HTTP_404_NOT_FOUND)

    user_id = request.user.id

    if swot_item.created_by_id != user_id:
        return Response({
            'errors': ['Only creator can update/delete Swot Item']
        }, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        data = request.body

        if 'text' in data:
            swot_item.text = data['text']

        try:
            swot_item.save()
        except:
            return Response({
                'errors': ['Error occurred when updating Swot Item']
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'data': {
                'swotItemId': swot_item.id,
                'swotId': swot_item.swot_id,
                'creatorId': user_id,
                'text': swot_item.text,
                'cardType': swot_item.cardType,
                'score': swot_item.score,
            }
        }, status=status.HTTP_200_OK)

    try:
        swot_item.delete()
        return Response({'data': {}}, status=status.HTTP_204_NO_CONTENT)
    except:
        return Response({
           'errors': ['Error occurred when deleting Swot Item']
        }, status=status.HTTP_400_BAD_REQUEST)
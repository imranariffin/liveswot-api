from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from swot_item.models import SwotItem
from swot_item.validators import validate
from swot_item.serializers import serialize

from core.serializers import deserialize
from core.decorators import authenticate


@api_view(http_method_names=['GET', 'POST'])
@authenticate
@deserialize
@validate
@serialize
def swot_item_list(request, swot_id):
    swot_id = int(swot_id)

    if request.method == 'GET':
        swot_items = SwotItem.objects.filter(swot_id=swot_id)

        return (
            [item for item in swot_items],
            status.HTTP_200_OK,
            None
        )
    else:
        data = request.body

        card_type = data['cardType']
        text = data['text']
        user_id = request.user.id

        swot_item = SwotItem.objects.create(swot_id=swot_id,
                                            created_by_id=user_id,
                                            text=text,
                                            cardType=card_type)
        return (
            swot_item,
            status.HTTP_201_CREATED,
            None
        )


@api_view(['PUT', 'DELETE'])
@authenticate
@deserialize
@validate
@serialize
def swot_item_detail(request, swot_item_id):
    swot_item_id = int(swot_item_id)
    swot_item = None

    try:
        swot_item = SwotItem.objects.get(id=swot_item_id)
    except SwotItem.DoesNotExist as dne:
        return (
            None,
            status.HTTP_404_NOT_FOUND,
            [dne.message]
        )

    user_id = request.user.id

    if swot_item.created_by_id != user_id:
        return (
            None,
            status.HTTP_403_FORBIDDEN,
            ['Only creator can update/delete Swot Item']
        )

    if request.method == 'PUT':
        data = request.body

        if 'text' in data:
            swot_item.text = data['text']

        try:
            swot_item.save()
        except:
            return (
                None,
                status.HTTP_400_BAD_REQUEST,
                ['Error occurred when updating Swot Item']
            )

        return (
            swot_item,
            status.HTTP_200_OK,
            None
        )

    try:
        swot_item.delete()
        return (
            None,
            status.HTTP_204_NO_CONTENT,
            None
        )
    except:
        return (
            None,
            status.HTTP_400_BAD_REQUEST,
            ['Error occurred when deleting Swot Item']
        )

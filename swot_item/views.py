from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

import json

from swot_item.models import SwotItem
from swot_item.serializers import SwotItemSerializer


@api_view(http_method_names=['GET', 'POST'])
@authentication_classes((IsAuthenticated,))
def swot_list(request):
    if request.method == 'GET':
        swots = SwotItem.objects.all()
        serialized = [SwotItemSerializer(swot).data for swot in swots]
        return Response({'data': serialized})
    else:
        data = json.loads(request.body)

        errors = []
        if 'cardType' not in data:
            errors.append({'cardType': 'required'})
        if 'text' not in data:
            errors.append({'text': 'required'})
        if errors:
            return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

        card_type = data['cardType']
        text = data['text']
        swot = SwotItem.objects.create(cardType=card_type, text=text)
        serialized = SwotItemSerializer(swot).data

        return Response({'data': serialized})


@api_view(['PUT', 'DELETE'])
@authentication_classes((IsAuthenticated,))
def swot_detail(request, pk):

    if request.method == 'PUT':

        data = json.loads(request.body)

        try:
            swot = SwotItem.objects.get(pk=pk)
        except SwotItem.DoesNotExist as dne:
            return Response({'errors': [dne.message]}, status=status.HTTP_404_NOT_FOUND)

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

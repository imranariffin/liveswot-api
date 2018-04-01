from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from swot_item.models import SwotItem, CARD_TYPES

import json


class SwotItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SwotItem
        fields = ('id', 'cardType', 'text')


def serialize_request(func):
    def wrap(request, *args, **kwargs):

        if request.method == 'POST':
            try:
                request.body = json.loads(request.body)
            except:
                return Response(
                    {'errors': ['Error during serialization']},
                    status=status.HTTP_400_BAD_REQUEST)

            required = ('text', 'cardType')
            errors = []
            for arg in required:
                if arg not in request.body:
                    errors.append('required: {}'.format(arg))
                    continue
                if request.body[arg] == '':
                    errors.append('`{}` field cannot be empty')
                    continue
                if arg == 'cardType' and request.body[arg] not in CARD_TYPES:
                    card_type = request.body[arg]
                    errors.append('`{}` is not a valid cardType option'.format(card_type))
            if errors:
                return Response(
                    {'errors': errors},
                    status=status.HTTP_400_BAD_REQUEST)

        return func(request, *args, **kwargs)

    wrap.__doc__ = func.__doc__
    wrap.__name__ = func.__name__

    return wrap

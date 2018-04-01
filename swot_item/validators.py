from rest_framework import status
from rest_framework.response import Response
from swot_item.models import CARD_TYPES


def validate(func):
    def _validate(request, *args, **kwargs):

        if request.method in ('POST', 'PUT',):
            body = request.body
            errors = []

            if 'text' not in body:
                errors.append('`text` field is required')
            elif not body['text']:
                errors.append('`text` field cannot be empty')

            if 'cardType' not in body:
                errors.append('`cardType` field is required')
            elif not body['cardType']:
                errors.append('`cardType` field cannot be empty')
            elif body['cardType'] not in CARD_TYPES:
                errors.append('wrong `cardType` `{}`'.format(body['cardType']))

            if errors:
                return Response({
                    'errors': errors
                }, status=status.HTTP_400_BAD_REQUEST)

        return func(request, *args, **kwargs)
    return _validate

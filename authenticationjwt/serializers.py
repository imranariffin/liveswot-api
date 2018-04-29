# import re
import json

from rest_framework.response import Response


def deserialize(func):
    def _deserialize(request, *args, **kwargs):
        if request.method in ('POST', 'PUT',):
            body = json.loads(request.body)

            if 'username' not in body['user']:
                email = body['user']['email']
                body['user']['username'] = email[:email.find('@')]

            request.body = body
        return func(request, *args, **kwargs)
    return _deserialize


def serialize_response(func):
    def serialize(request, *args, **kwargs):
        user, status, errors = func(request, *args, **kwargs)
        if errors:
            return Response({
                'errors': errors
            }, status=status)

        return Response({
            'data': {
                'user': {
                    'userId': user.id,
                    'email': user.email,
                    'username': user.username,
                    'token': user.token,
                }
            }
        }, status=status)
    return serialize

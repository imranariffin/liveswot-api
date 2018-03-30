import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from django.http.response import HttpResponseBadRequest
from authenticationjwt.models import User
import re

from backend.urls import URL_API_AUTH


def _get_user(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY)
    except:
        msg = 'Invalid authentication. Could not decode token'
        raise exceptions.AuthenticationFailed(msg)

    try:
        user = User.objects.get(pk=payload['id'])
    except User.DoesNotExist:
        msg = 'No user matching the token provided'
        raise exceptions.AuthenticationFailed(msg)
    if not user.is_active:
        msg = 'This user has been deactivated'
        raise exceptions.AuthenticationFailed(msg)

    return user


regex = re.compile(URL_API_AUTH)


def is_not_protected(endpoint):
    endpoint = endpoint[1::]
    return not regex.match(endpoint) is None


def jwt_middleware(get_response):

    def get_user(auth_header):

        auth_header_prefix = 'Bearer'.lower()

        if not auth_header or len(auth_header) != 2:
            msg = 'Authorization token malformed'
            raise exceptions.AuthenticationFailed(msg)

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            msg = 'Authorization prefix does not match'
            raise exceptions.AuthenticationFailed(msg)

        return _get_user(token)

    def authenticate(request):

        endpoint = request.path
        if is_not_protected(endpoint):
            return get_response(request)

        auth_header = authentication.get_authorization_header(request).split()
        try:
            user = get_user(auth_header)
        except exceptions.AuthenticationFailed as e:
            return HttpResponseBadRequest('{\"error\":\"Errrorrrr\"}', content_type='application/json')

        request.user = user
        return get_response(request)

    return authenticate

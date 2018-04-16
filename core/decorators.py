import jwt

from rest_framework.response import Response
from rest_framework import authentication, exceptions, status

from django.conf import settings

from authenticationjwt.models import User


def authenticate(func):

    def _get_user(token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except:
            msg = 'Invalid authentication. Could not decode token'
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(pk=payload['userId'])
        except User.DoesNotExist:
            msg = 'No user matching the token provided'
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = 'This user has been deactivated'
            raise exceptions.AuthenticationFailed(msg)

        return user

    def get_user(auth_header):
        auth_header_prefix = 'Bearer'.lower()

        if not auth_header or len(auth_header) != 2:
            msg = 'Authorization token malformed'
            raise exceptions.AuthenticationFailed(
                msg,
                code=status.HTTP_403_FORBIDDEN)

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            msg = 'Authorization prefix does not match'
            raise exceptions.AuthenticationFailed(
                msg,
                code=status.HTTP_403_FORBIDDEN)

        return _get_user(token)

    def _requires_authentication(request, *args, **kwargs):
        auth_header = authentication.get_authorization_header(request).split()

        try:
            user = get_user(auth_header)
        except exceptions.AuthenticationFailed as af:
            return Response(
                {'errors': [af.detail]},
                status=status.HTTP_403_FORBIDDEN)

        request.user = user

        return func(request, *args, **kwargs)

    return _requires_authentication

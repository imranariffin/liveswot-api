import re

from rest_framework import status
from rest_framework.response import Response


email_validation = {
    'max_length': 255
}
password_validation = {
    'max_length': 128,
    'min_length': 8,
}


def validate_email(user):
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    max_length = email_validation['max_length']

    if 'email' not in user:
        return ['`email` field is required']
    if not user['email']:
        return ['`email` field cannot be empty']

    errors = []
    email = user['email']

    if len(email) > max_length:
        msg = 'Field `email` must not exceed {} characters'
        errors.append(msg.format(max_length))
    if not re.match(email_regex, email):
        errors.append('Email is not valid')

    return errors


def validate_password(user):
    max_length = password_validation['max_length']
    min_length = password_validation['min_length']

    if 'password' not in user:
        return ['`password` field is required']
    elif not user['password']:
        return ['`password` field cannot be empty']

    errors = []
    password = user['password']

    if len(password) > max_length:
        msg = 'Field `password` must not exceed {} characters'
        errors.append(msg.format(max_length))
    if len(password) < min_length:
        msg = 'Field `password` must not be less than {} characters'
        errors.append(msg.format(min_length))

    return errors


def validate_signup(func):
    def _validate(request, *args, **kwargs):
        if request.method in ('POST',):
            body = request.body
            errors = []

            if 'user' not in body:
                errors.append('User information fields are required')
            else:
                user = body['user']
                errors.extend(validate_email(user))
                errors.extend(validate_password(user))

            if errors:
                return Response({
                    'errors': errors
                }, status=status.HTTP_400_BAD_REQUEST)

        return func(request, *args, **kwargs)
    return _validate


def validate_login(func):
    def _validate(request, *args, **kwargs):
        if request.method in ('POST',):
            body = request.body
            errors = []

            if 'user' not in body:
                errors.append('User information fields are required')
            else:
                user = body['user']
                errors.extend(validate_email(user))
                errors.extend(validate_password(user))

            if errors:
                return Response({
                    'errors': errors
                }, status=status.HTTP_400_BAD_REQUEST)

        return func(request, *args, **kwargs)
    return _validate

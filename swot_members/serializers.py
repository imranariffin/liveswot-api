from rest_framework.response import Response
from authenticationjwt.models import User


def serialize(func):

    def serialize_member(data):
        if data is None:
            return {}

        return {
            'userName': User.objects.get(pk=data.member_id).username,
            'membershipId': data.id,
            'memberId': data.member_id,
            'swotId': data.swot_id,
            'addedById': data.added_by_id,
            'created': data.created
        }

    def _serialize(request, *args, **kwargs):
        data, status, errors = func(request, *args, **kwargs)

        if errors:
            return Response({
                'errors': errors
            }, status=status)

        if type(data) == list:
            return Response({
                'data': [serialize_member(d) for d in data]
            }, status=status)

        return Response({
            'data': serialize_member(data),
        }, status=status)

    return _serialize
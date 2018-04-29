from rest_framework.response import Response

from authenticationjwt.models import User


def get_create_username(vote):
    return User.objects.get(pk=vote.created_by_id).username


def serialize(func):

    def serialize_vote(vote):
        if vote is None:
            return {}
        return {
            'voteId': vote.id,
            'swotItemId': vote.swot_item_id,
            'creatorId': vote.created_by_id,
            'voteType': vote.voteType,
            'creatorUsername': get_create_username(vote),
        }

    def _serialize(request, *args, **kwargs):
        data, status, errors = func(request, *args, **kwargs)

        if errors:
            return Response({
                'errors': errors
            }, status=status)

        if type(data) == list:
            return Response({
                'data': [
                    serialize_vote(vote) for vote in data
                ]}, status=status)

        return Response({
            'data': serialize_vote(data)
        }, status=status)

    return _serialize

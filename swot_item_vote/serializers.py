from rest_framework.response import Response

from authenticationjwt.models import User

from swot_item_vote.models import Vote

from utils.sorting import confidence


def get_item_confidence(swot_item_id):
    votes = Vote.objects.filter(swot_item_id=swot_item_id)
    ups = len([v for v in votes if v.voteType == 'up'])
    downs = len([v for v in votes if v.voteType == 'down'])

    return confidence(ups, downs)


def get_create_username(vote):
    return User.objects.get(pk=vote.created_by_id).username


def serialize(func):

    def serialize_vote(vote, extras={}):
        if vote is None:
            return {}

        serialized = {
            'voteId': vote.id,
            'swotItemId': vote.swot_item_id,
            'creatorId': vote.created_by_id,
            'voteType': vote.voteType,
            'creatorUsername': get_create_username(vote),
        }

        if extras:
            for k in extras:
                serialized[k] = extras[k]

        return serialized

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

        if data is None:
            return Response({
                'data': serialize_vote(data)
            }, status=status)

        score = get_item_confidence(data.swot_item_id)

        return Response({
            'data': serialize_vote(data, {'swotItemScore': score})
        }, status=status)

    return _serialize

from rest_framework import serializers

from models import Vote

import json


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('id', 'item', 'voteType')


def deserialize(func):
    def _deserialize(request, *args, **kwargs):
        if request.method == 'POST':
            request.body = json.loads(request.body)
        return func(request, *args, **kwargs)
    return _deserialize

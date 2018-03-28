from rest_framework import serializers

from swot.models import SwotItem, Vote


class SwotItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SwotItem
        fields = ('id', 'cardType', 'text')


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('id', 'item', 'voteType')

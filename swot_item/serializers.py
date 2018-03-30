from rest_framework import serializers

from swot_item.models import SwotItem


class SwotItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SwotItem
        fields = ('id', 'cardType', 'text')

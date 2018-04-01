from rest_framework import serializers

from swot.models import Swot


class SwotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Swot
        fields = ('id', 'title', 'description', 'created_by_id',)

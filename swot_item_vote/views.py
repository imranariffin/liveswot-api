from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from serializers import VoteSerializer

from swot_item_vote.models import Vote
from swot_item.models import SwotItem

from core.decorators import authenticate
from core.serializers import deserialize


@api_view(['GET', 'POST'])
@authenticate
@deserialize
def vote_list(request, swot_item_id):
    swot_item_id = int(swot_item_id)

    if request.method == 'GET':
        votes = Vote.objects.filter(item__swot_id=swot_item_id)
        serialized = [VoteSerializer(vote).data for vote in votes]

        return Response(
            {'data': serialized},
            status=status.HTTP_200_OK)
    else:
        try:
            swot_item = SwotItem.objects.get(pk=swot_item_id)
        except ObjectDoesNotExist:
            return Response(
                {'errors': ['Swot Item {} does not exist'.format(swot_item_id)]},
                status=status.HTTP_404_NOT_FOUND)

        vote_type = request.body['voteType']
        user_id = request.user.id

        try:
            existing_vote = Vote.objects.get(item__swot_id=swot_item_id)
            existing_vote.delete()

            if existing_vote.voteType == vote_type:
                return Response({'data': {}}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            pass

        vote = Vote(item=swot_item, voteType=vote_type)

        try:
            vote.save()
        except:
            return Response(
                {'errors': ['Error saving vote']},
                status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'data': {
                'swotItemId': swot_item_id,
                'userId': user_id,
                'voteType': vote_type,
            }
        }, status=status.HTTP_201_CREATED)
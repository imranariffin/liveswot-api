from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from swot_item_vote.models import Vote
from swot_item.models import SwotItem

from swot.models import Swot
from authenticationjwt.models import User

from core.decorators import authenticate
from core.serializers import deserialize


def get_create_username(vote):
    return User.objects.get(pk=vote.created_by_id).username,


def get_creator_usernames(votes):
    return dict([
        (
            vote.id,
            get_create_username(vote)
        ) for vote in votes
    ])


@api_view(['GET'])
@authenticate
@deserialize
def vote_list(request, swot_id):
    user_id = request.user.id
    swot = None

    try:
        swot = Swot.objects.get(id=swot_id)
    except ObjectDoesNotExist:
        return Response({
            'errors': ['Swot {} does not exist'.format(swot_id)],
        }, status=status.HTTP_404_NOT_FOUND)

    votes = Vote.objects.filter(swot_id=swot_id)
    creator_usernames = get_creator_usernames(votes)

    return Response({
        'data': [{
            'voteId': vote.id,
            'swotItemId': vote.swot_item_id,
            'creatorId': vote.created_by_id,
            'voteType': vote.voteType,
            'creatorUsername': creator_usernames[vote.id],
        } for vote in votes]
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@authenticate
@deserialize
def vote(request, swot_item_id):
    swot_item_id = int(swot_item_id)
    vote_type = request.body['voteType']
    user_id = request.user.id
    swot_item = None

    try:
        swot_item = SwotItem.objects.get(id=swot_item_id)
    except ObjectDoesNotExist:
        return Response({
            'errors': ['Swot Item does {} not exist'.format(swot_item_id)]
        }, status=status.HTTP_404_NOT_FOUND)

    try:
        existing_vote = Vote.objects.get(swot_item_id=swot_item_id)
        existing_vote_type = existing_vote.voteType
        existing_vote.delete()

        if existing_vote_type == vote_type:
            return Response({'data': {}}, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        pass

    vote = None
    try:
        vote = Vote(
            created_by_id=user_id,
            swot_item_id=swot_item_id,
            swot_id=swot_item.swot_id,
            voteType=vote_type
        )
    except IntegrityError, ie:
        return Response(
            {'errors': [ie]},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        vote.save()
    except:
        return Response(
            {'errors': ['Error saving vote']},
            status=status.HTTP_400_BAD_REQUEST)

    return Response({
        'data': {
            'voteId': vote.id,
            'swotItemId': swot_item_id,
            'creatorId': user_id,
            'creatorUsername': get_create_username(vote),
            'voteType': vote_type,
        }
    }, status=status.HTTP_201_CREATED)
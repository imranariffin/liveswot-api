from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from rest_framework.decorators import api_view
from rest_framework import status

from swot_item_vote.models import Vote
from swot_item.models import SwotItem

from .serializers import serialize

from swot.models import Swot

from core.decorators import authenticate
from core.serializers import deserialize

from utils.sorting import confidence


@api_view(['GET'])
@authenticate
@deserialize
@serialize
def vote_list(request, swot_id):

    try:
        Swot.objects.get(id=swot_id)
    except ObjectDoesNotExist:
        return (
            None,
            status.HTTP_404_NOT_FOUND,
            ['Swot {} does not exist'.format(swot_id)]
        )

    votes = Vote.objects.filter(swot_id=swot_id)

    return (
        [vote for vote in votes],
        status.HTTP_200_OK,
        None
    )


@api_view(['POST'])
@authenticate
@deserialize
@serialize
def vote(request, swot_item_id):
    swot_item_id = int(swot_item_id)
    vote_type = request.body['voteType']
    user_id = request.user.id
    swot_item = None

    try:
        swot_item = SwotItem.objects.get(id=swot_item_id)
    except ObjectDoesNotExist:
        return (
            None,
            status.HTTP_404_NOT_FOUND,
            ['Swot Item does {} not exist'.format(swot_item_id)]
        )

    try:
        existing_vote = Vote.objects.get(
            swot_item_id=swot_item_id,
            created_by_id=user_id
        )
        existing_vote_type = existing_vote.voteType
        existing_vote.delete()

        if existing_vote_type == vote_type:
            return (
                None,
                status.HTTP_200_OK,
                None
            )

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
        return (
            None,
            status.HTTP_400_BAD_REQUEST,
            [ie]
        )

    try:
        vote.save()
    except:
        return (
            None,
            status.HTTP_400_BAD_REQUEST,
            ['Error saving vote']
        )

    votes = Vote.objects.filter(swot_item_id=swot_item_id)
    ups = len([v for v in votes if v.voteType == 'up'])
    downs = len([v for v in votes if v.voteType == 'down'])

    SwotItem.objects\
        .filter(pk=swot_item_id)\
        .update(score=confidence(ups, downs))

    return (
        vote,
        status.HTTP_201_CREATED,
        None,
    )

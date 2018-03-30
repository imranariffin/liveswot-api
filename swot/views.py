from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound, HttpResponseBadRequest

from rest_framework.decorators import api_view, authentication_classes
from rest_framework import mixins, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

import json

from swot.models import SwotItem, Vote
from swot.serializers import SwotItemSerializer, VoteSerializer


@api_view(http_method_names=['GET', 'POST'])
@authentication_classes((IsAuthenticated,))
def swot_list(request):
    if request.method == 'GET':
        swots = SwotItem.objects.all()
        serialized = [SwotItemSerializer(swot).data for swot in swots]
        return Response({'data': serialized})
    else:
        data = json.loads(request.body)

        errors = []
        if 'cardType' not in data:
            errors.append({'cardType': 'required'})
        if 'text' not in data:
            errors.append({'text': 'required'})
        if errors:
            return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

        card_type = data['cardType']
        text = data['text']
        swot = SwotItem.objects.create(cardType=card_type, text=text)
        serialized = SwotItemSerializer(swot).data

        return Response({'data': serialized})


@api_view(['PUT', 'DELETE'])
@authentication_classes((IsAuthenticated,))
def swot_detail(request, pk):

    if request.method == 'PUT':

        data = json.loads(request.body)

        try:
            swot = SwotItem.objects.get(pk=pk)
        except SwotItem.DoesNotExist as dne:
            return Response({'errors': [dne.message]}, status=status.HTTP_404_NOT_FOUND)

        if 'text' in data:
            swot.text = data['text']

        try:
            swot.save()
        except ValueError as ve:
            return Response({'errors': [ve.message]}, status=status.HTTP_400_BAD_REQUEST)

        try:
            serialized = SwotItemSerializer(swot).data
        except ValidationError as ve:
            return Response({'errors': [msg for msg in ve.detail]})

        return Response({'data': serialized}, status=status.HTTP_200_OK)


class VoteList(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    """
    Request types: GET, POST
    List all votes, or create a new vote for a specific item
    """
    serializer_class = VoteSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        swot_item_id = int(kwargs['pk'])
        item = SwotItem.objects.filter(id=swot_item_id).first()
        self.queryset = Vote.objects.filter(item=item)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        swot_item_id = int(kwargs['pk'])
        item = SwotItem.objects.filter(id=swot_item_id).first()

        if item is None:
            return HttpResponseNotFound()

        voteType = request.data['voteType']
        if voteType is None or (voteType != 'up' and voteType != 'down'):
            return HttpResponseBadRequest()

        new_vote_type = None
        try:
            vote = Vote.objects.get(item_id=swot_item_id)
            new_vote_type = vote.voteType
            vote.delete()
        except ObjectDoesNotExist as e:
            pass

        last_vote = None
        vote_count = sum(map(
            lambda v: 1 if v.voteType == 'up' else -1,
            Vote.objects.filter(item=item))
        )

        if new_vote_type == voteType:
            return Response({
                'last_vote': last_vote,
                'vote': vote_count,
            })

        new_vote = VoteSerializer(
            Vote.objects.create(item=item, voteType=voteType)
        ).data

        return Response({
            'last_vote': new_vote,
            'vote': vote_count + (1 if new_vote['voteType'] == 'up' else -1),
        })

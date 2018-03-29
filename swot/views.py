from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound, HttpResponseBadRequest
from django.http.response import HttpResponse
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import mixins, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http.response import JsonResponse
from django.core import serializers
import json

from swot.models import SwotItem, Vote
from swot.serializers import SwotItemSerializer, VoteSerializer


# class SwotItemList(mixins.ListModelMixin,
#                    mixins.CreateModelMixin,
#                    generics.GenericAPIView):
#     """
#     Request types: GET, POST
#     List all items, or create a new item.
#     """
#     queryset = SwotItem.objects.all()
#     serializer_class = SwotItemSerializer
#     permission_classes = (IsAuthenticated,)
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

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


class SwotItemDetail(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     generics.GenericAPIView):
    """
    Request types: GET, PUT, DELETE
    Retrieve, update or delete an item.
    """
    queryset = SwotItem.objects.all()
    serializer_class = SwotItemSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


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

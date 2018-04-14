from django.db import models

from authenticationjwt.models import User

from swot_item.models import SwotItem

from swot.models import Swot


class Vote(models.Model):
    class Meta:
        unique_together = (('created_by', 'swot_item'),)

    VOTE_TYPES = (('up', 'UP'), ('down', 'DOWN'))

    created = models.DateTimeField(auto_now_add=True)
    voteType = models.CharField(choices=VOTE_TYPES,
                                max_length=4,
                                blank=False,
                                null=False)
    created_by = models.ForeignKey(User,
                                   on_delete=models.SET_NULL,
                                   blank=False,
                                   null=True,
                                   related_name='+',
                                   related_query_name='+')
    swot_item = models.ForeignKey(SwotItem,
                                  on_delete=models.SET_NULL,
                                  blank=False,
                                  null=True,
                                  related_name='+',
                                  related_query_name='+')
    swot = models.ForeignKey(Swot,
                             on_delete=models.SET_NULL,
                             blank=False,
                             null=True,
                             related_name='+',
                             related_query_name='+')

    def __str__(self):
        return '[Vote id={}]'.format(self.id)

    def __repr__(self):
        return self.__str__()


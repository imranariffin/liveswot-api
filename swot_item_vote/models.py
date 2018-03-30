from django.db import models

from swot_item.models import SwotItem


class Vote(models.Model):
    VOTE_TYPES = (('up', 'UP'), ('down', 'DOWN'))

    created = models.DateTimeField(auto_now_add=True)
    voteType = models.CharField(choices=VOTE_TYPES, max_length=4)
    item = models.ForeignKey(SwotItem,
                             on_delete=models.SET_NULL,
                             blank=True,
                             null=True,
                             related_name='+',
                             related_query_name='+')

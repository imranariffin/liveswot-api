from django.db import models

from swot.models import Swot

CARD_TYPES = ('strength', 'weakness', 'opportunity', 'threat',)


class SwotItem(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    cardType = models.CharField(max_length=11)
    text = models.TextField()
    swot = models.ForeignKey(Swot,
                             on_delete=models.SET_NULL,
                             blank=True,
                             null=True,
                             related_name='+',
                             related_query_name='+')

    class Meta:
        ordering = ('created',)

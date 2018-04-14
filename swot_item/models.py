from django.db import models

from swot.models import Swot

from authenticationjwt.models import User


CARD_TYPES = ('strength', 'weakness', 'opportunity', 'threat',)


class SwotItem(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    cardType = models.CharField(max_length=11)
    text = models.TextField()
    created_by = models.ForeignKey(User,
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

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return '[SwotItem id={}]'.format(self.id)

    def __repr__(self):
        return self.__str__()

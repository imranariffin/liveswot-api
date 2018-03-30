from django.db import models


class SwotItem(models.Model):
    CARD_TYPES = (
        ('strength', 'Strength'), ('weakness', 'Weakness'),
        ('opportunity', 'Opportunity'), ('threat', 'Threat'))

    created = models.DateTimeField(auto_now_add=True)
    cardType = models.CharField(choices=CARD_TYPES, max_length=11)
    text = models.TextField()

    class Meta:
        ordering = ('created',)

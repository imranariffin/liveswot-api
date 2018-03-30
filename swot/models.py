from django.db import models
from authenticationjwt.models import User


class Swot(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    title = models.TextField(max_length=40)
    description = models.TextField(max_length=100)
    owner = models.ForeignKey(User,
                              on_delete=models.SET_NULL,
                              blank=True,
                              null=True,
                              related_name='+',
                              related_query_name='+')

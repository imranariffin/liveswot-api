from django.conf.urls import url

from swot_item_vote import views

urlpatterns = [
    url(
        r'(?P<swot_id>[0-9]+)/items/votes/$',
        views.vote_list,
        name='get'
    ),
    url(
        r'items/(?P<swot_item_id>[0-9]+)/votes/$',
        views.vote,
        name='post'
    ),
]
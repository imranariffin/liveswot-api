from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns

from swot_item import views as swotitemviews

urlpatterns = [

    url(
        r'^admin/',
        admin.site.urls
    ),
    url(
        r'^api/auth/',
        include('authenticationjwt.urls', namespace='authenticationjwt')
    ),
    url(
        r'^api/swots/',
        include('swot.urls', namespace='swot')
    ),
    url(
        r'^api/items/$',
        swotitemviews.swot_item_list,
        name='get_post_delete_swot_item',
    ),
    url(
        r'^api/items/(?P<pk>[0-9]+)/$',
        swotitemviews.swot_item_detail,
        name='delete_swot_item',
    ),
    url(
        r'^api/votes/(?P<swot_item_id>[0-9]+)/',
        include('swot_item_vote.urls', namespace='swot_item_vote')
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)

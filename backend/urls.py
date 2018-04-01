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
        include('swot_item_vote.urls', namespace='swot_item_vote')
    ),
    url(
        r'^api/swots/(?P<swot_id>[0-9]+)/items/$',
        swotitemviews.swot_item_list,
        name='get_post_swot_item',
    ),
    url(
        r'^api/swots/items/(?P<swot_item_id>[0-9]+)/$',
        swotitemviews.swot_item_detail,
        name='put_delete_swot_item',
    ),
    url(
        r'^api/swots/',
        include('swot.urls', namespace='swot')
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)

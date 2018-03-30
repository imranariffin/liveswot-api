from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns

from swot import views as swotviews

URL_API_AUTH = r'^api/auth/'
URL_ADMIN = r'^admin/'
URL_API_SWOT_ITEM = r'^api/swot-item/$'
URL_API_SWOT_ITEM_DETAIL = r'^api/swot-item/(?P<pk>[0-9]+)/$'
URL_API_SWOT_ITEM_DETAIL_VOTE = r'^api/swot-item/(?P<pk>[0-9]+)/vote/$'

urlpatterns = [

    url(
        URL_API_AUTH,
        include('authenticationjwt.urls', namespace='authenticationjwt')
    ),
    url(
        URL_ADMIN,
        admin.site.urls
    ),
    url(
        URL_API_SWOT_ITEM,
        swotviews.swot_list,
        name='get_post_delete_swot_item',
    ),
    url(
        URL_API_SWOT_ITEM_DETAIL,
        swotviews.swot_detail,
        name='delete_swot_item',
    ),
    url(
        URL_API_SWOT_ITEM_DETAIL_VOTE,
        swotviews.VoteList.as_view(),
        name='get_post_vote',
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)

from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns

from swot import views

urlpatterns = [

    url(r'^api/auth/', include('authenticationjwt.urls', namespace='authenticationjwt')),

    url(r'^admin/', admin.site.urls),
    url(
        r'^api/swot-item/$',
        views.SwotItemList.as_view(),
        name='get_post_delete_swot_item',
    ),
    url(
        r'^api/swot-item/(?P<pk>[0-9]+)/$',
        views.SwotItemDetail.as_view(),
        name='delete_swot_item',
    ),
    url(
        r'^api/swot-item/(?P<pk>[0-9]+)/vote/$',
        views.VoteList.as_view(),
        name='get_post_vote',
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)

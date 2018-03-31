from django.conf.urls import url

from swot import views

urlpatterns = [

    url(
        r'(?P<swot_id>[0-9]+)/$',
        views.swot_detail,
        name='put_delete'
    ),
    url(
        r'$',
        views.swot_list,
        name='get_post'
    ),

]

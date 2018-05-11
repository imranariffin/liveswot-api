from django.conf.urls import url

from swot_members import views

urlpatterns = [
    url(
        r'(?P<member_id>[0-9]+)/swots/(?P<swot_id>[0-9]+)/$',
        views.get_add_members,
        name='post'
    ),
]

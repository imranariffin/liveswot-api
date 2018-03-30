from django.conf.urls import url

from swot import views

urlpatterns = [
    url(
        r'$',
        views.swot_list,
        name='get_post'
    ),
]
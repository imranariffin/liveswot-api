from django.conf.urls import url

from swot_item_vote import views

urlpatterns = [
    url(
        r'$',
        views.vote_list,
        name='get_post'
    ),
]
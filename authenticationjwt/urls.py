from django.conf.urls import url

from .views import login, signup

urlpatterns = [
    url(
        r'^signup/?$',
        signup,
        name='signup'
    ),
    url(
        r'^login/?$',
        login,
        name='login'
    ),
]

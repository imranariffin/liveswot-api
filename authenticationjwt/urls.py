from django.conf.urls import url

from .views import RegistrationAPIView, LoginAPIView

urlpatterns = [
    url(
        r'^signup/?$',
        RegistrationAPIView.as_view(),
        name='signup'
    ),
    url(
        r'^login/?$',
        LoginAPIView.as_view(),
        name='login'
    ),
]

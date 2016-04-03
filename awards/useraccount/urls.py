from django.conf.urls import patterns, url
from useraccount.views import SignupView, LoginView, LogoutView

urlpatterns = patterns(
    '',
    url(r'^register/$', SignupView.as_view(), name='user_register'),
    url(r'^login/$', LoginView.as_view(), name='user_login'),
    url(r'^logout/$', LogoutView.as_view(), name='user_logout'),
)

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from useraccount.views import SignupView, LoginView, LogoutView, UserSignupView, MyProfile

urlpatterns = patterns(
    '',
    url(r'^register/$', SignupView.as_view(), name='user_register'),
    url(r'^login/$', LoginView.as_view(), name='user_login'),
    url(r'^logout/$', LogoutView.as_view(), name='user_logout'),

    url(r'^signup/$', UserSignupView.as_view(), name='user_signup'),

    url(r'^my-profile/$', login_required(MyProfile.as_view()), name='my_profile'),


)

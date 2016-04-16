from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from useraccount.views import SignupView, UserLogin, LogoutView, UserSignupView, MyProfile, MyUploads, \
    EditMyProfile

urlpatterns = patterns(
    '',
    url(r'^register/$', SignupView.as_view(), name='user_register'),
    url(r'^login/$', UserLogin.as_view(), name='user_login'),
    url(r'^logout/$', LogoutView.as_view(), name='user_logout'),

    url(r'^signup/$', UserSignupView.as_view(), name='user_signup'),

    url(r'^my-profile/$', login_required(MyProfile.as_view()), name='my_profile'),

    url(r'^my-uploads/$', login_required(MyUploads.as_view()), name='my_uploads'),

    url(r'^edit-profile/$', login_required(EditMyProfile.as_view()), name='edit_myprofile'),
)

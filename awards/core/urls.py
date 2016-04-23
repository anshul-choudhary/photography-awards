from django.conf.urls import patterns, url

from . import views
from core.views import HomeView, FileUploadHandler, BestPhotographerProfile

urlpatterns = patterns(
    '',
    url(r'^$', views.HomeView.as_view(), name='home'),

    url(r'^faqs$', views.FaqsView.as_view(), name='faqs'),

    url(r'^photographers$', views.PhotographersView.as_view(), name='photographers'),

    url(r'^faqs$', views.FaqsView.as_view(), name='faqs'),

    # file upload handler
    url(
        r'fileuploadhandler/(?P<operation>\w+)/$',
        FileUploadHandler.as_view(),
        name='file_upload_handler'
    ),

    url(r'^profile/(?P<key>\w+)/$', BestPhotographerProfile.as_view(), name='bestphotographersprofile'),

)

#
# testpattern = patterns(
#     '',
#     url(r'^test$', views.TestView.as_view(), name='home'),
# )

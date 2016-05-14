from django.conf.urls import patterns, url

from . import views
from core.views import HomeView, FileUploadHandler, BestPhotographerProfile, MonthHomeView, DummyHomeView, \
    PhotographerSectionFilter

urlpatterns = patterns(
    '',
    url(r'^$', views.DummyHomeView.as_view(), name='home'),

    url(r'^test$', views.HomeView.as_view(), name='home'),

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

    url(r'^month/(?P<key>\w+)/$', MonthHomeView.as_view(), name='month_home'),



    url(r'^(?P<key1>\w+)-(?P<key2>\w+)/$', PhotographerSectionFilter.as_view(), name='photographer_filter'),
)

#
# testpattern = patterns(
#     '',
#     url(r'^test$', views.TestView.as_view(), name='home'),
# )

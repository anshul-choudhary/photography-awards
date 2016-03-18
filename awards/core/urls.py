from django.conf.urls import patterns, url

from . import views
from core.views import HomeView

urlpatterns = patterns(
    '',
    url(r'^$', views.HomeView.as_view(), name='home'),


    # file upload handler
    # url(
    #     r'fileuploadhandler/(?P<operation>\w+)/$',
    #     FileUploadHandler.as_view(),
    #     name='file_upload_handler'
    # ),
)

#
# testpattern = patterns(
#     '',
#     url(r'^test$', views.TestView.as_view(), name='home'),
# )

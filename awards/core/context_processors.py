from django.conf import settings


def contextprocessor_samplelists(request):

    ctx = {}
    ctx['STATIC_URL'] = settings.STATIC_URL
    return ctx

def media_globals(request):
    ''' Media files information '''

    c_dic = {}
    c_dic['url_prefix_media'] = 'http://{http_host}{media_url}'.format(
        http_host=request.META.get('HTTP_HOST'),
        media_url=settings.MEDIA_URL
    )
    c_dic['url_prefix_static'] = 'http://{http_host}{static_url}'.format(
        http_host=request.META.get('HTTP_HOST'),
        static_url=settings.STATIC_URL
    )
    c_dic['url_prefix'] = settings.EMAIL_SITE_URL
    return c_dic

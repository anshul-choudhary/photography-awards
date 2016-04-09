from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import Footer


class HomeView(APIView):
    ''' Home Page view '''

    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        ''' Receives the request '''

        ctx = {}
        #Fetch Footer
        FooterQuerySet = Footer.objects.filter(active=True).order_by('priority')[:4]
        footer = []
        for obj in FooterQuerySet:
            footer.append({'link': obj.link1, 'img': obj.image.all()[0].image.path})
        ctx['footer'] = footer

        return Response(ctx, template_name=self.template_name)



class FaqsView(APIView):
    ''' Home Page view '''

    template_name = 'joinus.html'

    def get(self, request, *args, **kwargs):
        ''' Receives the request '''

        return Response({}, template_name=self.template_name)



class PhotographersView(APIView):
    ''' Home Page view '''

    template_name = 'photographers.html'

    def get(self, request, *args, **kwargs):
        ''' Receives the request '''

        return Response({}, template_name=self.template_name)








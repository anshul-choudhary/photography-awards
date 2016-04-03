from rest_framework.response import Response
from rest_framework.views import APIView


class HomeView(APIView):
    ''' Home Page view '''

    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        ''' Receives the request '''

        return Response({}, template_name=self.template_name)



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








from rest_framework.response import Response
from rest_framework.views import APIView


class SignupView(APIView):
    ''' Home Page view '''

    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        ''' Receives the request '''

        return Response({}, template_name=self.template_name)


class LoginView(APIView):
    ''' Home Page view '''

    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        ''' Receives the request '''

        return Response({}, template_name=self.template_name)



class LogoutView(APIView):
    ''' Home Page view '''

    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        ''' Receives the request '''

        return Response({}, template_name=self.template_name)


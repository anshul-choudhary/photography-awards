from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import Country
from useraccount.forms import SignupForm
from useraccount.models import Photographer


class SignupView(APIView):
    ''' Home Page view '''

    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        ''' Receives the request '''

        CountryQuerySet = Country.objects.all().order_by('name')
        return Response({'country': CountryQuerySet}, template_name=self.template_name)


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


class UserSignupView(APIView):
    ''' Home Page view '''

    template_name = 'register.html'
    signupform = SignupForm

    def get(self, request, *args, **kwargs):
        ''' Receives the request '''

        return Response({}, template_name=self.template_name)

    def post(self, request, *args, **kwargs):

        ctx = {}
        kwargs = request.POST.copy()
        signupform = self.signupform(kwargs)

        if signupform.is_valid():
            # user = authenticate(username=request.POST['username'], password=request.POST['password'])
            #Generate Otp
            # GenerateOtp(
            #     user_id=signupform.cleaned_data['user_id'], phone=signupform.cleaned_data['primary_contact_number'],
            #     first_name=signupform.cleaned_data['user_id']
            # )

            UserObj = signupform.save()

            #Create Photographer
            Photographer.objects.create(
                user_ref=UserObj, user_id=UserObj.user_id,
                firstname=UserObj.firstname, lastname=UserObj.lastname,
                username=UserObj.username, instagram_link1=UserObj.instagram_link1
            )

            #Add values in session
            ctx['username'] = signupform.cleaned_data['username']
            ctx['primary_contact_number'] = signupform.cleaned_data['primary_contact_number']
            ctx['password'] = signupform.cleaned_data['password']
            ctx['firstname'] = signupform.cleaned_data['firstname']
            ctx['lastname'] = signupform.cleaned_data['lastname']
            ctx['instagram_link1'] = signupform.cleaned_data['instagram_link1']
            ctx['email'] = signupform.cleaned_data['email']
            ctx['businessname'] = signupform.cleaned_data['businessname']
            ctx['city'] = signupform.cleaned_data['city']
            ctx['country'] = signupform.cleaned_data['countryval']
            request.session['new_user_credentials'] = ctx

            #Dummy Check
            user = authenticate(username=signupform.cleaned_data['username'], password=signupform.cleaned_data['password'])
            if user.is_active:
                login(request, user)
            return redirect("my_profile")

        else:
            CountryQuerySet = Country.objects.all().order_by('name')
            return Response({'signupform': signupform, 'country': CountryQuerySet}, template_name=self.template_name)
        # return Response(self.results, content_type="application/json")



class MyProfile(APIView):
    ''' Home Page view '''

    template_name = 'my-profile.html'

    def get(self, request, *args, **kwargs):
        ''' Receives the request '''

        return Response({}, template_name=self.template_name)



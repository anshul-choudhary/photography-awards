from django.contrib.auth import authenticate, login
from django.forms.utils import ErrorList
from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from awards.choices import IMAGE_NAME_CHOICES
from core.models import Country, Image
from useraccount.forms import SignupForm, UserLoginnForm, EditMyprofile, CompleteUploadForm
from useraccount.models import Photographer, UserProfile


class SignupView(APIView):
    ''' Home Page view '''

    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        ''' Receives the request '''

        if request.user.is_authenticated():
            return redirect('my_profile')

        CountryQuerySet = Country.objects.all().order_by('name')
        return Response({'country': CountryQuerySet}, template_name=self.template_name)


class LogoutView(APIView):
    ''' Home Page view '''

    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        """ This function renders the add listing page """

        from django.contrib.auth import logout
        logout(request)
        return redirect('home')


class UserLogin(APIView):
    """ Login view """

    template_name = 'login.html'
    loginform = UserLoginnForm


    def get(self, request, *args, **kwargs):
        """ This function renders the add listing page """

        if request.user.is_authenticated():
            return redirect('my_profile')

        return Response({}, template_name=self.template_name)


    def post(self, request, *args, **kwargs):
        """ Post Method """

        if request.user.is_authenticated():
            return redirect('user_logout')

        loginform = self.loginform(request.POST)
        if loginform.is_valid():
            user = authenticate(username=request.POST['username'].upper(), password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    ctx = {}
                    login(request, user)
                    #Add values in session
                    ctx['username'] = user.username
                    ctx['primary_contact_number'] = user.primary_contact_number
                    ctx['password'] = user.password
                    ctx['firstname'] = user.firstname
                    ctx['lastname'] = user.lastname
                    ctx['instagram_link1'] = user.instagram_link1
                    ctx['email'] = user.email
                    ctx['businessname'] = user.businessname
                    ctx['city'] = user.city
                    ctx['countryval'] = user.country.id
                    request.session['loggedin_user_credentials'] = ctx
                    return redirect('my_profile')

                else:
                    loginform.errors['password'] = '* Account disabled'
                    return Response({'login': loginform}, template_name='login.html')

            else:
                loginform.errors['password'] = '* Invalid username and password'
                return Response({'login': loginform}, template_name='login.html')

        else:
            if 'username' in loginform.errors:
                del loginform.errors['username']
            loginform.errors['password'] = '* Invalid username and password'
            return Response({'login': loginform}, template_name='login.html')



class UserSignupView(APIView):
    ''' Home Page view '''

    template_name = 'register.html'
    signupform = SignupForm

    def get(self, request, *args, **kwargs):
        ''' Receives the request '''

        CountryQuerySet = Country.objects.all().order_by('name')
        return Response({'country': CountryQuerySet}, template_name=self.template_name)

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
            ctx['countryval'] = signupform.cleaned_data['countryval']
            request.session['loggedin_user_credentials'] = ctx

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
    editform = EditMyprofile

    def get(self, request, *args, **kwargs):
        ''' Receives the request '''

        ctx = {}
        if 'loggedin_user_credentials' in request.session:
            ctx = request.session['loggedin_user_credentials']

        CountryQuerySet = Country.objects.all().order_by('name')
        editform = self.editform(ctx)

        editform.errors['firstname'] = ""
        editform.errors['city'] = ""
        editform.errors['primary_contact_number'] = ""
        editform.errors['businessname'] = ""
        editform.errors['email'] = ErrorList()
        editform.errors['username'] = ""
        editform.errors['countryval'] = ""


        ctx.update({'country': CountryQuerySet})
        ctx.update({'editform': editform})
        return Response(ctx, template_name=self.template_name)



class MyUploads(APIView):
    ''' Home Page view '''

    template_name = 'uploads.html'

    def get(self, request, *args, **kwargs):
        ''' Receives the request '''

        ctx = {}
        if 'loggedin_user_credentials' in request.session:
            ctx = request.session['loggedin_user_credentials']

        ctx.update({'username': request.user.username})
        return Response(ctx, template_name=self.template_name)

    def post(self, request, *args, **kwargs):
        ''' Receives the request '''

        pass
        # return Response(ctx, template_name=self.template_name)


class EditMyProfile(APIView):
    ''' Home Page view '''

    template_name = 'uploads.html'
    editform = EditMyprofile

    def get(self, request, *args, **kwargs):
        ''' Receives the request '''

        ctx = {}
        if 'loggedin_user_credentials' in request.session:
            ctx = request.session['loggedin_user_credentials']

        CountryQuerySet = Country.objects.all().order_by('name')
        editform = self.editform(ctx)

        editform.errors['firstname'] = ""
        editform.errors['city'] = ""
        editform.errors['primary_contact_number'] = ""
        editform.errors['businessname'] = ""
        editform.errors['email'] = ErrorList()
        editform.errors['username'] = ""
        editform.errors['countryval'] = ""


        ctx.update({'country': CountryQuerySet})
        ctx.update({'editform': editform})
        return Response(ctx, template_name='my-profile.html')


    def edit_form_save(self, UserObj, editform):

        ctx = {}
        if 'loggedin_user_credentials' in self.request.session:
            ctx = self.request.session['loggedin_user_credentials']

        UserObj.firstname = editform.data['firstname']
        UserObj.lastname = editform.data['lastname']
        UserObj.instagram_link1 = editform.data['instagram_link1']
        UserObj.email = editform.data['email']
        UserObj.businessname = editform.data['businessname']
        UserObj.city = editform.data['city']
        UserObj.primary_contact_number = editform.data['primary_contact_number']
        UserObj.country = Country.objects.get(id=int(editform.data['countryval']))
        UserObj.save()
        # UserObj = editform.save(instance=UserObj)

        try:
            PhotoObj = Photographer.objects.get(user_ref=UserObj)
            PhotoObj.firstname = editform.data['firstname']
            PhotoObj.lastname = editform.data['lastname']
            PhotoObj.instagram_link1 = editform.data['instagram_link1']
            PhotoObj.save()
        except:
            pass


        #Add values in session
        ctx['username'] = editform.data['username']
        ctx['primary_contact_number'] = editform.data['primary_contact_number']
        ctx['firstname'] = editform.data['firstname']
        ctx['lastname'] = editform.data['lastname']
        ctx['instagram_link1'] = editform.data['instagram_link1']
        ctx['email'] = editform.data['email']
        ctx['businessname'] = editform.data['businessname']
        ctx['city'] = editform.data['city']
        ctx['countryval'] = editform.data['countryval']

        self.request.session['loggedin_user_credentials'] = ctx
        return redirect("my_uploads")


    def post(self, request, *args, **kwargs):

        kwargs = request.POST.copy()
        editform = self.editform(kwargs)

        if editform.is_valid():
            UserObj = request.user
            return self.edit_form_save(UserObj, editform)

        else:
            # ActualUserObj = UserProfile.objects.get(username__exact=editform.data['username'])
            # UserObj = UserProfile.objects.get(primary_contact_number__exact=editform.data['primary_contact_number'])
            #
            # process_to_save = True
            # attrib = ['username', 'firstname', 'lastname', 'businessname', 'instagram_link1', 'countryval', 'city']
            # for k in attrib:
            #     if k in editform.errors:
            #         process_to_save = False
            #
            # if process_to_save:
            #     if 'primary_contact_number' in editform.errors and ActualUserObj.primary_contact_number == UserObj.primary_contact_number:
            #         UserObj = UserProfile.objects.get(email__exact=editform.data['email'])
            #         if 'email' in editform.errors and ActualUserObj.email == UserObj.email:
            #             return self.edit_form_save(UserObj, editform)
            #
            #         else:
            #             return self.edit_form_save(UserObj, editform)
            #     else:
            #         return self.edit_form_save(UserObj, editform)

            CountryQuerySet = Country.objects.all().order_by('name')
            return Response({'editform': editform, 'country': CountryQuerySet}, template_name='my-profile.html')










class CompleteUpload(APIView):
    ''' Home Page view '''

    template_name = 'description.html'
    form_class = CompleteUploadForm
    results = {'error_message': '', 'status': 'Ok'}


    def get(self, request, *args, **kwargs):
        """This function renders the add listing page"""

        if not request.user.is_authenticated():
            return redirect('user_login')
        return redirect('my_profile')

    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated():
            return redirect('user_login')

        response = (self.handle_form_save(request, self.form_class(request.POST)))
        return response

    # @transaction.atomic
    def handle_form_save(self, request, upload_form):
        """Save the data into database"""

        if upload_form.is_valid():
            try:
                PhotoObj = Photographer.objects.get(user_ref=request.user)
                PhotoObj.image_1_desc = upload_form.cleaned_data['image_1_desc']
                # PhotoObj.image_2_desc = upload_form.cleaned_data['image_2_desc']
                # PhotoObj.image_3_desc = upload_form.cleaned_data['image_3_desc']
                # PhotoObj.image_4_desc = upload_form.cleaned_data['image_4_desc']
                # PhotoObj.image_5_desc = upload_form.cleaned_data['image_5_desc']
                PhotoObj.save()

                # image = Image(content_object=PhotoObj, image_name=upload_form.cleaned_data['image_1_name'])
                image = Image(content_object=PhotoObj)
                (image.image,image_name) = Image().copy_upload_image(PhotoObj, upload_form.cleaned_data['image_1_name'], request.user.username)
                image.image_name = IMAGE_NAME_CHOICES['TYPE'].Award1
                image.image_a_name = image_name
                image.save()

                image = Image(content_object=PhotoObj)
                (image.image,image_name) = Image().copy_upload_image(PhotoObj, upload_form.cleaned_data['image_2_name'], request.user.username)
                image.image_name = IMAGE_NAME_CHOICES['TYPE'].Award2
                image.image_a_name = image_name
                image.save()

                image = Image(content_object=PhotoObj)
                (image.image,image_name) = Image().copy_upload_image(PhotoObj, upload_form.cleaned_data['image_3_name'], request.user.username)
                image.image_name = IMAGE_NAME_CHOICES['TYPE'].Award3
                image.image_a_name = image_name
                image.save()


                image = Image(content_object=PhotoObj)
                (image.image,image_name) = Image().copy_upload_image(PhotoObj, upload_form.cleaned_data['profile_image_name'], request.user.username)
                image.image_name = IMAGE_NAME_CHOICES['TYPE'].Profileimage
                image.image_a_name = image_name
                image.profile_image = True
                image.save()

                # image = Image(content_object=PhotoObj, image_name=upload_form.cleaned_data['image_2_name'])
                # image.image = Image().copy_upload_image(PhotoObj, upload_form.cleaned_data['image_2_name'], request.user_id, upload_form.cleaned_data['image_2'])
                # image.save()
                #
                # image = Image(content_object=PhotoObj, image_name=upload_form.cleaned_data['image_3_name'])
                # image.image = Image().copy_upload_image(PhotoObj, upload_form.cleaned_data['image_3_name'], request.user_id, upload_form.cleaned_data['image_3'])
                # image.save()
                #
                #
                # image = Image(content_object=PhotoObj, image_name=upload_form.cleaned_data['image_4_name'])
                # image.image = Image().copy_upload_image(PhotoObj, upload_form.cleaned_data['image_4_name'], request.user_id, upload_form.cleaned_data['image_4'])
                # image.save()
                #
                # image = Image(content_object=PhotoObj, image_name=upload_form.cleaned_data['image_5_name'])
                # image.image = Image().copy_upload_image(PhotoObj, upload_form.cleaned_data['image_5_name'], request.user_id, upload_form.cleaned_data['image_5'])
                # image.save()

                return Response({}, template_name=self.template_name)

            except Exception as ex:
                raise Exception(str(ex))
        else:
            try:
                if len(upload_form.cleaned_data['image_1_name']):
                    pass
                    # dt = upload_form.cleaned_data['image_1_name']
                    # fn = dt.split('_thumbnail')
                    # ln = fn[1]
                    # upload_form.cleaned_data['image_1_name'] = fn[0].split('/media/_versions/temp/')[1] + ln


                # if len(upload_form.cleaned_data['image_2']):
                #     dt = upload_form.cleaned_data['image_2']
                #     fn = dt.split('_thumbnail')
                #     ln = fn[1]
                #     upload_form.cleaned_data['image_2_name'] = fn[0].split('/media/_versions/temp/')[1] + ln
                #
                # if len(upload_form.cleaned_data['image_3']):
                #     dt = upload_form.cleaned_data['image_3']
                #     fn = dt.split('_thumbnail')
                #     ln = fn[1]
                #     upload_form.cleaned_data['image_3_name'] = fn[0].split('/media/_versions/temp/')[1] + ln
                #
                # if len(upload_form.cleaned_data['image_4']):
                #     dt = upload_form.cleaned_data['image_4']
                #     fn = dt.split('_thumbnail')
                #     ln = fn[1]
                #     upload_form.cleaned_data['image_4_name'] = fn[0].split('/media/_versions/temp/')[1] + ln
                #
                # if len(upload_form.cleaned_data['image_5']):
                #     dt = upload_form.cleaned_data['image_5']
                #     fn = dt.split('_thumbnail')
                #     ln = fn[1]
                #     upload_form.cleaned_data['image_5_name'] = fn[0].split('/media/_versions/temp/')[1] + ln


            except Exception as e:
                pass

            return Response({'upload_form': upload_form}, template_name='uploads.html')






import os
from django.contrib.auth import authenticate, login
from django.forms.utils import ErrorList
from django.http import HttpResponse
from django.shortcuts import redirect
from filebrowser.base import FileObject
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from awards.choices import IMAGE_NAME_CHOICES
from awards.settings import MEDIA_URL, TEMP_UPLOAD_DIR, FILEBROWSER_DIRECTORY, MEDIA_ROOT
from awards.utils import generate_version_add_watermark
from core.models import Country, Image, Setting
from useraccount.forms import SignupForm, UserLoginnForm, EditMyprofile, CompleteUploadForm
from useraccount.models import Photographer, UserProfile


class SignupView(APIView):
    ''' Home Page view '''

    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        ''' Receives the request '''

        if request.user.is_authenticated():
            return redirect('my_profile')

        try:
            if Setting.objects.get(key="REGISTRATION_ALLOWED").value == "0":
                return redirect("home")
        except:
            pass

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
        # if 'loggedin_user_credentials' in request.session:
        #     ctx = request.session['loggedin_user_credentials']

        if not len(ctx):
            Obj = Photographer.objects.get(user_ref=request.user)
            ctx.update({"username": request.user.username,
                        "firstname": Obj.firstname,
                        "lastname": Obj.lastname,
                        "businessname": request.user.businessname,
                        "instagram_link1": Obj.instagram_link1,
                        "primary_contact_number": request.user.primary_contact_number,
                        "countryval": request.user.country.id,
                        "city": request.user.city,
                        "email": request.user.email,
                        "website_link": Obj.website_link
            })
            # self.request.session['loggedin_user_credentials'] = ctx

        # ctx.update({"website_link": ""})
        CountryQuerySet = Country.objects.all().order_by('name')
        editform = self.editform(ctx)

        editform.errors['firstname'] = ""
        editform.errors['city'] = ""
        editform.errors['primary_contact_number'] = ""
        editform.errors['businessname'] = ""
        editform.errors['email'] = ErrorList()
        editform.errors['username'] = ""
        editform.errors['countryval'] = ""
        editform.errors['website_link'] = ""

        ctx.update({'country': CountryQuerySet})
        ctx.update({'editform': editform})
        ctx.update({"show_profile": "0"})

        try:
            PhotographerObj = Photographer.objects.get(user_ref=request.user)
            if len(PhotographerObj.image.all()):
                ctx.update({"show_profile": "1"})
        except:
            ctx.update({"show_profile": "0"})


        return Response(ctx, template_name=self.template_name)



class PhotographerProfile(APIView):
    ''' Home Page view '''

    template_name = 'photographerprofile.html'

    def get(self, request, *args, **kwargs):
        ''' Receives the request '''

        ctx = {}
        if 'loggedin_user_credentials' in request.session:
            ctx = request.session['loggedin_user_credentials']

        try:
            del ctx['password']
        except:
            pass

        PhotoObj = Photographer.objects.get(user_ref=request.user)
        CountryQuerySet = Country.objects.filter(id=PhotoObj.user_ref.country.id).order_by('name')

        ctx.update({'name': PhotoObj.firstname + ' ' + PhotoObj.lastname})
        ctx.update({'country': CountryQuerySet[0].name})
        ctx.update({'awards': PhotoObj.no_of_awards})
        ctx.update({'contact': PhotoObj.user_ref.primary_contact_number})
        ctx.update({'email': PhotoObj.user_ref.email})
        ctx.update({'instagram_link1': PhotoObj.instagram_link1})
        ctx.update({'instagram_link2': PhotoObj.instagram_link2})
        ctx.update({'home_page_desc': PhotoObj.home_page_desc})
        ctx.update({'website_link': PhotoObj.website_link})
        ctx.update({'images': []})

        for k in PhotoObj.image.all().order_by('created_date'):
            a = {'imagename': "", "imagedesc": ""}
            if k.profile_image:
                ctx.update({'profile_image': k.image.name})
            else:
                a["imagename"] = k.image.name
                a["imagedesc"] = k.image_desc
                ctx['images'].append(a)
        return Response(ctx, template_name=self.template_name)


class EditMyProfile(APIView):
    ''' Home Page view '''

    template_name = 'uploads.html'
    editform = EditMyprofile

    def get(self, request, *args, **kwargs):
        ''' Receives the request '''

        ctx = {}
        # if 'loggedin_user_credentials' in request.session:
        #     ctx = request.session['loggedin_user_credentials']

        if not len(ctx):
            Obj = Photographer.objects.get(user_ref=request.user)
            ctx.update({"username": request.user.username,
                        "firstname": Obj.firstname,
                        "lastname": Obj.lastname,
                        "businessname": request.user.businessname,
                        "instagram_link1": Obj.instagram_link1,
                        "primary_contact_number": request.user.primary_contact_number,
                        "countryval": request.user.country.id,
                        "city": request.user.city,
                        "email": request.user.email,
                        "website_link": Obj.website_link
            })
            # self.request.session['loggedin_user_credentials'] = ctx

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

        try:
            PhotographerObj = Photographer.objects.get(user_ref=request.user)
            if len(PhotographerObj.image.all()):
                ctx.update({"show_profile": "1"})
        except:
            ctx.update({"show_profile": "0"})

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
            PhotoObj.website_link = editform.data['website_link']
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
        ctx['website_link'] = editform.data['website_link']

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




class MyUploads(APIView):
    ''' Home Page view '''

    template_name = 'uploads.html'
    form_class = CompleteUploadForm

    def get(self, request, *args, **kwargs):
        ''' Receives the request '''

        ctx = {'show_profile': "0"}
        if 'loggedin_user_credentials' in request.session:
            ctx = request.session['loggedin_user_credentials']

        try:
            PhotographerObj = Photographer.objects.get(user_ref=request.user)
            if len(PhotographerObj.image.all()):
                formargs = {'username': request.user.username, 'home_page_desc': PhotographerObj.home_page_desc}

                count = 1
                for k in PhotographerObj.image.all().order_by('created_date'):
                    if k.profile_image:
                        rel_path = os.path.join(os.path.join(FILEBROWSER_DIRECTORY,request.user.username) + '/', k.image.filename)
                        a = FileObject(rel_path)
                        version = a.version_generate('thumbnail').url
                        formargs.update({'profile_image_name': k.image.filename,
                                         'profile_image': version})

                    name = 'image_' + str(count) + '_desc'
                    rel_path = os.path.join(os.path.join(FILEBROWSER_DIRECTORY,request.user.username) + '/', k.image.filename)
                    a = FileObject(rel_path)
                    version = a.version_generate('thumbnail').url

                    formargs.update({'image_' + str(count) + '_name': k.image.filename,
                                     'image_' + str(count): version
                                 })

                    formargs.update({'image_' + str(count) + '_desc': k.image_desc})
                    count += 1

                # formargs.update({'image_1_desc': PhotographerObj.image_1_desc,
                #                  'image_2_desc': PhotographerObj.image_2_desc,
                #                  'image_3_desc': PhotographerObj.image_3_desc,
                #                  'image_4_desc': PhotographerObj.image_4_desc,
                #                  })

                formsubmit = self.form_class(formargs)
                ctx.update({'upload_form': formsubmit})
                ctx.update({'show_profile': "1"})

        except Exception as e:
            ctx.update({'show_profile': "0"})
            pass

        ctx.update({'username': request.user.username})
        return Response(ctx, template_name=self.template_name)

    def post(self, request, *args, **kwargs):
        ''' Receives the request '''

        pass



class CompleteUpload(APIView):
    ''' Home Page view '''

    template_name = 'photographerprofile.html'
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
                if len(PhotoObj.image.all()):
                    for k in PhotoObj.image.all():
                        k.delete_image(os.path.join(MEDIA_ROOT, k.image.name))
                        k.delete()
                PhotoObj.home_page_desc = upload_form.cleaned_data['home_page_desc']
                # PhotoObj.image_1_desc = upload_form.cleaned_data['image_1_desc']
                # PhotoObj.image_2_desc = upload_form.cleaned_data['image_2_desc']
                # PhotoObj.image_3_desc = upload_form.cleaned_data['image_3_desc']
                PhotoObj.save()

                # image = Image(content_object=PhotoObj, image_name=upload_form.cleaned_data['image_1_name'])
                image = Image(content_object=PhotoObj)
                (image.image,image_name) = Image().copy_upload_image(PhotoObj, upload_form.cleaned_data['image_1_name'], request.user.username)
                image.image_name = IMAGE_NAME_CHOICES['TYPE'].Award1
                image.image_a_name = image_name
                image.image_desc = upload_form.cleaned_data['image_1_desc']
                image.save()
                generate_version_add_watermark(image.image.name, 'thumbnail')

                image = Image(content_object=PhotoObj)
                (image.image,image_name) = Image().copy_upload_image(PhotoObj, upload_form.cleaned_data['image_2_name'], request.user.username)
                image.image_name = IMAGE_NAME_CHOICES['TYPE'].Award2
                image.image_a_name = image_name
                image.image_desc = upload_form.cleaned_data['image_2_desc']
                image.save()
                generate_version_add_watermark(image.image.name, 'thumbnail')

                image = Image(content_object=PhotoObj)
                (image.image,image_name) = Image().copy_upload_image(PhotoObj, upload_form.cleaned_data['image_3_name'], request.user.username)
                image.image_name = IMAGE_NAME_CHOICES['TYPE'].Award3
                image.image_a_name = image_name
                image.image_desc = upload_form.cleaned_data['image_3_desc']
                image.save()
                generate_version_add_watermark(image.image.name, 'thumbnail')


                image = Image(content_object=PhotoObj)
                (image.image,image_name) = Image().copy_upload_image(PhotoObj, upload_form.cleaned_data['profile_image_name'], request.user.username)
                image.image_name = IMAGE_NAME_CHOICES['TYPE'].Profileimage
                image.image_a_name = image_name
                image.profile_image = True
                image.save()
                generate_version_add_watermark(image.image.name, 'thumbnail')

                return redirect("photographerprofile")

            except Exception as ex:
                raise Exception(str(ex))
        else:
            try:
                pass
                # if len(upload_form.cleaned_data['image_1_name']):
                #     dt = upload_form.cleaned_data['image_1_name']
                #     fn = dt.split('_thumbnail')
                #     ln = fn[1]
                #     upload_form.cleaned_data['image_1_name'] = fn[0].split('/media/_versions/temp/')[1] + ln


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

            return Response({'upload_form': upload_form, 'username': request.user.username}, template_name='uploads.html')






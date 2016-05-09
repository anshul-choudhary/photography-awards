import os
from django.conf import Settings
from django.shortcuts import redirect
from filebrowser.base import FileObject
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from awards.choices import USER
from awards.settings import TEMP_UPLOAD_DIR, MEDIA_URL, FILEBROWSER_VERSION_BASEDIR
from awards.settings import MEDIA_ROOT
from awards.utils import generate_unique_file_name
from core.forms import ImageUploadForm
from core.models import Footer, Country, Setting, Faqs
from useraccount.models import Photographer, WinnerMonth



class DummyHomeView(APIView):
    ''' Home Page view '''

    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        ''' Receives the request '''

        return Response({}, template_name=self.template_name)


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
        ctx['best_photographer'] = []

        # Best Photographer section
        BestPhotographers = Photographer.objects.filter(is_best_photographer=True)[:12]
        for obj in BestPhotographers:
            ar = {}
            CountryQuerySet = Country.objects.filter(id=obj.user_ref.country.id)
            ar.update({'name': obj.firstname + ' ' + obj.lastname, 'awards': obj.no_of_awards})
            ar.update({'country': CountryQuerySet[0].name})
            ar.update({'username': obj.user_id})

            for k in obj.image.all().order_by('created_date'):
                if k.profile_image:
                    ar.update({'profile_image': k.image.name})
            ctx['best_photographer'].append(ar)



        ctx['home_photographer'] = []
        # Home Page Profile Section
        BestPhotographers = Photographer.objects.filter(activate_home_page=True, is_winner=True).order_by("priority")
        for obj in BestPhotographers:
            ar = {}
            CountryQuerySet = Country.objects.filter(id=obj.user_ref.country.id)
            ar.update({'name': obj.firstname + ' ' + obj.lastname, 'awards': obj.no_of_awards})
            ar.update({'country': CountryQuerySet[0].name})
            ar.update({'username': obj.user_id})
            ar.update({'home_page_desc': obj.home_page_desc})
            ar.update({'images': {"imagename": "", "imagedesc": "", "profileimage": ""}})

            for k in obj.image.all().order_by('created_date'):
                if k.cover_image:
                    ar['images']['imagename'] = k.image.name
                    ar['images']['imagedesc'] = k.image_desc
                if k.profile_image:
                    ar['images']['profileimage'] = k.image.name

            ctx['home_photographer'].append(ar)


        res = []
        to_show = Setting.objects.get(key="HOME_PAGE_MONTHS").value.split(",")
        Objs = WinnerMonth.objects.all().values("id","month_name")
        for k in Objs:
            a = {"key": "", "val": ""}
            if dict(USER["WINNER_MONTH"]).get(k["month_name"]) in to_show:
                a["key"] = k["month_name"]
                a["val"] = dict(USER["WINNER_MONTH"]).get(k["month_name"])
                res.append(a)
        ctx.update({"winner_month": res})

        ctx.update({"home_page_heading": Setting.objects.get(key="HOME_PAGE_HEADING").value})

        return Response(ctx, template_name=self.template_name)




class MonthHomeView(APIView):
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
        ctx['best_photographer'] = []

        # Best Photographer section
        BestPhotographers = Photographer.objects.filter(is_best_photographer=True)[:12]
        for obj in BestPhotographers:
            ar = {}
            CountryQuerySet = Country.objects.filter(id=obj.user_ref.country.id)
            ar.update({'name': obj.firstname + ' ' + obj.lastname, 'awards': obj.no_of_awards})
            ar.update({'country': CountryQuerySet[0].name})
            ar.update({'username': obj.user_id})

            for k in obj.image.all().order_by('created_date'):
                if k.profile_image:
                    ar.update({'profile_image': k.image.name})
            ctx['best_photographer'].append(ar)



        ctx['home_photographer'] = []
        # Home Page Profile Section

        WMObj = WinnerMonth.objects.filter(month_name=int(kwargs.get("key")))
        BestPhotographers = Photographer.objects.filter(winner_month__in=WMObj,
                                    activate_home_page=True, is_winner=True).order_by("priority")
        # BestPhotographers = Photographer.objects.filter(activate_home_page=True, is_winner=True).order_by("priority")
        for obj in BestPhotographers:
            ar = {}
            CountryQuerySet = Country.objects.filter(id=obj.user_ref.country.id)
            ar.update({'name': obj.firstname + ' ' + obj.lastname, 'awards': obj.no_of_awards})
            ar.update({'country': CountryQuerySet[0].name})
            ar.update({'username': obj.user_id})
            ar.update({'home_page_desc': obj.home_page_desc})
            ar.update({'images': {"imagename": "", "imagedesc": "", "profileimage": ""}})

            for k in obj.image.all().order_by('created_date'):
                if k.cover_image:
                    ar['images']['imagename'] = k.image.name
                    ar['images']['imagedesc'] = k.image_desc
                if k.profile_image:
                    ar['images']['profileimage'] = k.image.name

            ctx['home_photographer'].append(ar)


        res = []
        to_show = Setting.objects.get(key="HOME_PAGE_MONTHS").value.split(",")
        Objs = WinnerMonth.objects.all().values("id","month_name")
        for k in Objs:
            a = {"key": "", "val": ""}
            if dict(USER["WINNER_MONTH"]).get(k["month_name"]) in to_show:
                a["key"] = k["month_name"]
                a["val"] = dict(USER["WINNER_MONTH"]).get(k["month_name"])
                res.append(a)
        ctx.update({"winner_month": res})

        ctx.update({"home_page_heading": Setting.objects.get(key="HOME_PAGE_HEADING").value})

        return Response(ctx, template_name=self.template_name)





class BestPhotographerProfile(APIView):
    ''' Home Page view '''

    template_name = 'bestphotographerprofile.html'

    def get(self, request, *args, **kwargs):
        ''' Receives the request '''

        ctx = {}
        if 'loggedin_user_credentials' in request.session:
            ctx = request.session['loggedin_user_credentials']

        try:
            del ctx['password']
        except:
            pass

        try:
            PhotoObj = Photographer.objects.get(user_id=kwargs['key'])
        except:
            return redirect("home")

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
            a = {"imagename": "", "imagedesc": ""}
            if k.profile_image:
                ctx.update({'profile_image': k.image.name})
            else:
                try:
                    a["imagename"] = k.image.name
                except:
                    a["imagename"] = ""
                a["imagedesc"] = k.image_desc
                ctx['images'].append(a)
        return Response(ctx, template_name=self.template_name)



class FaqsView(APIView):
    ''' Home Page view '''

    template_name = 'joinus.html'

    def get(self, request, *args, **kwargs):
        ''' Receives the request '''

        try:
            ctx = {"award_submission_date": Setting.objects.get(key="AWARD_SUBMISSION_DATE").value }
        except:
            ctx = {}

        FaqsObjs = Faqs.objects.all().order_by("priority")
        ctx.update({"faqs": FaqsObjs})
        return Response(ctx, template_name=self.template_name)



class PhotographersView(APIView):
    ''' Home Page view '''

    template_name = 'photographers.html'

    def get(self, request, *args, **kwargs):
        ''' Receives the request '''



        PhotoObjs = Photographer.objects.all()
        p_list = []

        for k in PhotoObjs:
            a = {}
            a["name"] = k.firstname + " " + k.lastname
            a["awards"] = k.no_of_awards
            a["country"] = k.user_ref.country.name if k.user_ref.country is not None else ""
            a["contact"] = k.user_ref.primary_contact_number
            a["website_link"] = k.website_link
            a["desc"] = k.home_page_desc
            a["user_id"] = k.user_id
            a["c_image"] = k.image.filter(cover_image=True)[0].image.name if k.image.filter(cover_image=True).count() else ""
            a["p_image"] = k.image.filter(profile_image=True)[0].image.name if k.image.filter(profile_image=True).count() else ""
            p_list.append(a)

        return Response({'photographers': p_list}, template_name=self.template_name)




class FileUploadHandler(APIView):

    renderer_classes = (JSONRenderer,)
    authentication_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """ Receives the request """

        resp_dict = {}

        if kwargs['operation'] == 'image':
            form = ImageUploadForm(request.POST, request.FILES)
            if form.is_valid():
                resp_dict = self.save_file(form.cleaned_data['db_image'])
                resp_dict['status'] = 'OK'
                return Response(resp_dict)
            else:
                if 'db_image' in form.errors:
                    err_msg = form.errors['db_image'][0]
                else:
                    err_msg = '* Upload failed !!'
                return Response({'status': 'error', 'msg': err_msg})

        # elif kwargs['operation'] == 'document':
        #     form = DocumentUploadForm(request.POST, request.FILES)
        #     if form.is_valid():
        #         resp_dict = self.save_file(form.cleaned_data['db_document'])
        #         c_type = ['image/png', 'image/jpeg', 'image/gif']
        #         if form.cleaned_data['db_document'].content_type not in c_type:
        #             resp_dict['ctype'] = form.cleaned_data['db_document'].name.split('.')[-1]
        #             resp_dict['ctype'] = resp_dict['ctype'].lower()
        #         resp_dict['status'] = 'OK'
        #         return Response(resp_dict)
        #     else:
        #         if 'db_document' in form.errors:
        #             err_msg = form.errors['db_document'][0]
        #         else:
        #             err_msg = '* Upload failed !!'
        #         return Response({'status': 'error', 'msg': err_msg})

        elif kwargs['operation'] == 'delete':
            try:
                filename = request.POST['name']
                self.delete_file(filename)
                return Response({'status': 'OK', 'msg': 'Deleted ok !!'})
            except OSError as ex:
                return Response({'status': 'error', 'msg': ex.message})

        return Response({'asda': 'asdasdasdasd'})


    def save_file(self, file):
        """
            Little helper to save a file default save to media/temp/
        """

        # original_name = file.name
        # extension = os.path.splitext(original_name)[1][1:]
        # filename = os.path.splitext(original_name)[0].strip('.')
        # filename = filename + '__' + str(time.time()) + '.' + extension
        # rel_path = os.path.join(TEMP_UPLOAD_DIR, filename)

        #Create user directory in temp folder
        try:
            os.makedirs(os.path.join(MEDIA_ROOT, TEMP_UPLOAD_DIR))
        except OSError:
            # Do nothing Assume that dir is already created.
            pass

        try:
            userdirpath = os.path.join(os.path.join(MEDIA_ROOT, TEMP_UPLOAD_DIR), self.request.user.username)
            os.makedirs(userdirpath)
        except OSError:
            # Do nothing Assume that dir is already created.
            pass

        source_dir = os.path.join(MEDIA_ROOT)
        destination_dir = os.path.join(source_dir,os.path.join(TEMP_UPLOAD_DIR,self.request.user.username))

        ext = '.' + os.path.splitext(file.name)[1][1:]
        img_name = file.name.split(ext)[0]
        img_name = generate_unique_file_name(destination_dir, img_name, ext)

        rel_path = os.path.join(os.path.join(TEMP_UPLOAD_DIR,self.request.user.username) + '/', img_name)
        fd = open(os.path.join(MEDIA_ROOT, rel_path), 'wb')
        for chunk in file.chunks():
            fd.write(chunk)
        fd.close()

        try:
            a = FileObject(rel_path)
            version = a.version_generate('thumbnail').url
        except Exception as e:
            pass

        return {'path': MEDIA_URL + rel_path, 'file': img_name, 'name': img_name, 'version': version}


    def delete_file(self, file):
        """
            Delete the specified media file
        """

        rel_path = os.path.join(TEMP_UPLOAD_DIR, os.path.join(self.request.user.username, file))
        os.remove(os.path.join(MEDIA_ROOT, rel_path))

        # Remove from version folder as well
        try:
            original_name = file
            extension = os.path.splitext(original_name)[1][1:]
            filename = os.path.splitext(original_name)[0].strip('.')
            filename = filename + '_thumbnail' + '.' + extension
            temp_path = os.path.join(TEMP_UPLOAD_DIR,os.path.join(self.request.user.username,filename))
            os.remove(os.path.join(os.path.join(MEDIA_ROOT, FILEBROWSER_VERSION_BASEDIR), temp_path))
        except Exception as e:
            pass






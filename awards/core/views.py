import os
from filebrowser.base import FileObject
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from awards.settings import TEMP_UPLOAD_DIR, MEDIA_URL, FILEBROWSER_VERSION_BASEDIR
from awards.settings import MEDIA_ROOT
from core.forms import ImageUploadForm
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

        rel_path = os.path.join(os.path.join(TEMP_UPLOAD_DIR,self.request.user.username) + '/', file.name)
        fd = open(os.path.join(MEDIA_ROOT, rel_path), 'wb')
        for chunk in file.chunks():
            fd.write(chunk)
        fd.close()

        try:
            a = FileObject(rel_path)
            version = a.version_generate('thumbnail').url
        except Exception as e:
            pass

        return {'path': MEDIA_URL + rel_path, 'file': file.name, 'name': file.name, 'version': version}


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






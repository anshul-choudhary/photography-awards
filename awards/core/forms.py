import os
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField
from django.template.defaultfilters import filesizeformat, slugify
from awards.settings import MEDIA_ROOT, UPLOAD_FOOTER_DIR
from core.models import Image, Footer
from filebrowser.fields import FileBrowseField


class ImageInlineForm(ModelForm):
    """
    Image inline form class, provides validations on inline models.
    """

    def __init__(self, *args, **kwargs):
        super(ImageInlineForm, self).__init__(*args, **kwargs)
        self.fields['image_name'].required = True

    class Meta:
        model = Image
        exclude = []


class RestrictedFileField(forms.FileField):
    """
        Same as FileField, but you can specify:
        * content_types - list containing allowed content_types.
        Example: ['application/pdf', 'image/jpeg']
        * max_upload_size - a number indicating the maximum file size allowed for upload.
        2.5MB - 2621440
        5MB - 5242880
        10MB - 10485760
        20MB - 20971520
        50MB - 5242880
        100MB - 104857600
        250MB - 214958080
        500MB - 429916160
    """

    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop("content_types")
        self.max_upload_size = kwargs.pop("max_upload_size")
        self.min_upload_size = kwargs.pop("min_upload_size", 0)

        super(RestrictedFileField, self).__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        file = super(RestrictedFileField, self).clean(data, initial)

        try:
            content_type = file.content_type
            if content_type in self.content_types:
                if file._size > self.max_upload_size:
                    raise ValidationError((
                        'Please keep filesize under {size}. Current filesize {filesize}').format(
                            size=filesizeformat(self.max_upload_size),
                            filesize=filesizeformat(file._size)
                        )
                    )
                if file._size < self.min_upload_size:
                    raise ValidationError((
                        'Please keep filesize above {size}. Current filesize {filesize}').format(
                            size=filesizeformat(self.min_upload_size),
                            filesize=filesizeformat(file._size)
                        )
                    )
            else:
                raise ValidationError(_('This type of file is not supported.'))
        except AttributeError:
            pass

        return data


class ImageUploadForm(forms.Form):
    """Image upload form."""

    db_image = RestrictedFileField(
        content_types=['image/png', 'image/jpeg', 'image/gif'], max_upload_size=5242880, min_upload_size=20480)


class FooterImageForm(ModelForm):
    footer_media_dir = CharField(label='', widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(FooterImageForm, self).__init__(*args, **kwargs)

        # We need to create directory for images and docs of this plan if uploaded from admin
        # since uploads/ is the root of file browser so build path from inside it.
        # Plan images are stored inside the project directory
        FooterObj = self.instance

        if FooterObj.id:
            media_path = str.format('{0}', slugify(str(FooterObj.id)))
            self.fields['footer_media_dir'].initial = media_path
            media_path = os.path.join(os.path.join(MEDIA_ROOT, UPLOAD_FOOTER_DIR), media_path)
            try:
                os.makedirs(media_path)
            except Exception as e:
                pass

    class Meta:
        model = Footer
        exclude = []






from __future__ import unicode_literals
import datetime
import os
import shutil
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from filebrowser import storage
from filebrowser.fields import FileBrowseField
from awards.choices import IMAGE_NAME_CHOICES
from awards.settings import MEDIA_ROOT, TEMP_UPLOAD_DIR, UPLOAD_DEVICE_DIR, UPLOAD_PHOTO_DIR
from awards.utils import generate_unique_file_name, normalize_file_name


class Country(models.Model):

    name = models.CharField(max_length=50)

    class Meta:

        verbose_name_plural = 'Countries'
        verbose_name = 'Country'
        db_table = 'country'

    def __unicode__(self):
        return '{name}'.format(name=unicode(self.name))

    def save(self, **kwargs):

        self.name = self.name.strip().upper()
        super(Country, self).save(kwargs)


class State(models.Model):

    name = models.CharField(max_length=50)
    country = models.ForeignKey('core.Country', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'States'
        verbose_name = 'State'
        db_table = 'state'

    def __unicode__(self):
        return '{name}'.format(name=unicode(self.name))

    def save(self, **kwargs):

        self.name = self.name.strip().upper()
        super(State, self).save(kwargs)


class City(models.Model):

    name = models.CharField(max_length=50)
    state = models.ForeignKey('core.State', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Cities'
        verbose_name = 'City'
        db_table = 'city'

    def __unicode__(self):
        return '{name}'.format(name=unicode(self.name))

    def save(self, **kwargs):

        self.name = self.name.strip().upper()
        super(City, self).save(kwargs)


class Locality(models.Model):

    name = models.CharField(max_length=50)
    city = models.ForeignKey('core.City', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Localities'
        verbose_name = 'Locality'
        db_table = 'locality'

    def __unicode__(self):
        return '{name} ({city},{db_id})'.format(name=unicode(self.name), city=self.city.name, db_id=self.id)

    def save(self, **kwargs):

        self.name = self.name.strip().upper()
        super(Locality, self).save(kwargs)


class Setting(models.Model):
    ''' Core setting Model '''

    key = models.CharField(
        max_length=50, null=False, blank=False, verbose_name="Settings Key",
        help_text="Key / Name of the Setting."
    )
    value = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="Settings Value",
        help_text="Value of the Setting."
    )
    description = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Settings Description",
        help_text="Description of the Setting."
    )
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True, verbose_name="Last Modified")

    @staticmethod
    def get_value(setting_key):
        try:
            return Setting.objects.get(key=setting_key).value
        except Setting.DoesNotExist:
            raise Exception('Key: ' + setting_key + ' does not found in Settings')

    class Meta:
        verbose_name_plural = 'Settings'
        verbose_name = 'Setting'
        db_table = 'setting'

    def __unicode__(self):
        return "%s" % unicode(self.key)

    def save(self, *args, **kwargs):
        ''' Prepares the cache if not exist o/w updates the cache '''

        # _val = get_settings_cache(self.key)  # #If key does not exist it just set it up
        # if _val is not None:
        #     set_cache(self.key, self.value)
        super(Setting, self).save(*args, **kwargs)
        return


class Image(models.Model):

    image = FileBrowseField(max_length=256, directory="images/")
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    #Image Type
    image_name = models.SmallIntegerField(
        blank=True, null=True, choices=IMAGE_NAME_CHOICES['TYPE'],
        help_text=('Fill image name from the dropdown.')
    )
    image_a_name = models.CharField(
        blank=True, null=True, max_length=50, help_text=('Fill actual image name.')
    )
    image_desc = models.TextField(blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    cover_image = models.BooleanField(
        default=False, verbose_name="Cover Image",
        help_text="Only one of the image can be selected as cover image of the Photographer."
    )
    profile_image = models.BooleanField(
        default=False, verbose_name="Profile Image",
        help_text="Only one of the image can be selected as profile image of the Photographer."
    )

    class Meta:
        verbose_name_plural = 'Images'
        verbose_name = 'Image'
        db_table = 'image'

    def __unicode__(self):
        return "%s" % str(self.id)

    # def __init__(self, *args, **kwargs):
    #     super(Image, self).__init__(*args, **kwargs)

    def copy_upload_image(self, PhotoPbj, img_name, username):
        """ """

        source_dir = os.path.join(MEDIA_ROOT)
        destination_rel = os.path.join(UPLOAD_PHOTO_DIR,username)
        destination_dir = os.path.join(MEDIA_ROOT, destination_rel)
        try:
            os.makedirs(destination_dir)
        except OSError:
            # Do nothing Assume that dir is already created.
            pass

        # src = os.path.join(source_dir, img_name)
        src = os.path.join(MEDIA_ROOT,os.path.join(TEMP_UPLOAD_DIR,username))
        src = os.path.join(src,img_name)

        ext = '.' + os.path.splitext(img_name)[1][1:]
        img_name = img_name.split(ext)[0]
        img_name = generate_unique_file_name(destination_dir, img_name, ext)

        shutil.copy(src, os.path.join(destination_dir, img_name))
        # os.remove(src)
        return (os.path.join(destination_rel, img_name),img_name)


    @staticmethod
    def delete_image(path_absolute):
        try:
            os.remove(path_absolute)
            return True
        except OSError:
            return None

    # def save(self, *args, **kwargs):
    #
    #     # if self.content_type.name == 'Vendor' or self.content_type.name == 'Devices':
    #     #     self.handle_images()
    #     super(Image, self).save(*args, **kwargs)

    def handle_images(self):
        """
        This method takes care of images of the project
        which includes renaming, watermark, generation of versions.
        """

        # deleting the versions and renaming the file
        fileobject = self.image
        fileobject.delete_versions()
        new_name = normalize_file_name(dict(IMAGE_NAME_CHOICES['TYPE']).get(int(self.image_name)))
        new_name = generate_unique_file_name(os.path.dirname(fileobject.path_full), new_name, fileobject.extension)
        self.image = os.path.join(fileobject.head, new_name)
        storage.move(fileobject.path, self.image)

        # generate versions and add watermarks
        # ext = self.image.name.split('.')[-1].lower()
        # if ext in ['jpg', 'jpeg', 'gif', 'png']:
        #     generate_version_add_watermark(self.image.name, 'medium')
        #     generate_version_add_watermark(self.image.name, 'large')


class Footer(models.Model):
    """
    """

    link1 = models.CharField(max_length=200, blank=True, null=True)
    image = GenericRelation('core.Image')
    priority = models.SmallIntegerField(blank=True, null=True, verbose_name="Order in which it will appear")
    active = models.BooleanField(default=False, verbose_name="To be displayed or not")

    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    modified_date = models.DateTimeField(auto_now=True, verbose_name="Last Modified")

    class Meta:
        verbose_name = 'Footer'
        verbose_name_plural = 'Footer'
        db_table = 'footer'


class Faqs(models.Model):
    """
    """

    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    priority = models.SmallIntegerField(blank=True, null=True, verbose_name="Order in which it will appear")

    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    modified_date = models.DateTimeField(auto_now=True, verbose_name="Last Modified")

    class Meta:
        verbose_name = 'Faqs'
        verbose_name_plural = 'Faqs'
        db_table = 'faqs'


class AboutUs(models.Model):
    """
    """

    content = models.TextField(blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    modified_date = models.DateTimeField(auto_now=True, verbose_name="Last Modified")
    class Meta:
        verbose_name = 'Aboutus'
        verbose_name_plural = 'Aboutus'
        db_table = 'aboutus'






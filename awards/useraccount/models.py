import random
import string
from time import timezone
import datetime
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.db import models
from django.utils.http import urlquote
from awards import settings

from awards.choices import USER
from awards.utils import generate_user_id



#Create Super User using the following command
# UserProfile.objects.create_superuser(username='aphdapplicant', password='Xcellins$tage23', email='aphdapplicant@gmail.com')

class UserProfileQuerySet(models.QuerySet):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """
            Creates and saves a User with the given email and password and
            primary_contact_number.
        """

        email = self.normalize_email(email)
        user = self.model(
            email=email, is_staff=is_staff, is_active=True,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)

        if user.user_id in [None,'']:
            user.user_id = generate_user_id()

        user.save(using=self._db)
        return user

    def normalize_email(self, email):

        """
        Normalize the email address by lowercasing the domain part of the it.
        """

        email = email or ''
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = '@'.join([email_name, domain_part.lower()])
        return email

    def create_user(self, email=None, password=None, primary_contact_number=None, **extra_fields):
        """
            Creates and saves a User with the given email and password and primary_contact_number.
        """

        extra_fields['primary_contact_number'] = primary_contact_number
        extra_fields['email'] = self.normalize_email(extra_fields.get('email'))
        user = self.model(
            email=email, is_staff=False, is_active=True,
            is_superuser=False,
            **extra_fields
        )
        user.set_password(password)

        if user.user_id in [None,'']:
            user.user_id = generate_user_id()

        user.save(using=self._db)

        # user = self._create_user(email, password, False, False, **extra_fields)

        return user

    # def get_userobj_via_email(self, email):
    #     """
    #         This method returns the user_profile object matching email
    #     """
    #
    #     return self.get(email__iexact=email)

    # def create_superuser(self, email, password, **extra_fields):
    #     """
    #         creates super user when using command >> createsuperuser.
    #     """
    #
    #     user = self._create_user(email, password, True, True, **extra_fields)
    #     return user


# class CustomUserManager(UserManager):
#     use_in_migrations = True
#
#     def get_queryset(self):
#         return UserProfileQuerySet(self.model, using=self._db)
#
#     def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
#         return self.get_queryset()._create_user(email, password, is_staff, is_superuser, **extra_fields)
#
#     def create_user(self, email=None, password=None, primary_contact_number=None, **extra_fields):
#         return self.get_queryset().create_user(email=None, password=None, primary_contact_number=None, **extra_fields)
#
#     def create_superuser(self, email, password, **extra_fields):
#         return self.get_queryset().create_superuser(email, password, **extra_fields)
#


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """
        An abstract base class implementing a fully featured User model with
        admin-compliant permissions.
        The idea is to remove the username field and also change the length of email field
    """

    # Unique user name for system log in
    username = models.CharField(max_length=50, unique=True)
    user_id = models.CharField(unique=True, max_length=20, null=True, blank=True, verbose_name="User ID")
    firstname = models.CharField(max_length=50, blank=True, null=True)
    lastname = models.CharField(max_length=50, blank=True, null=True)
    businessname = models.CharField(max_length=50, blank=True, null=True)

    instagram_link1 = models.CharField(max_length=200, blank=True, null=True)
    instagram_link2 = models.CharField(max_length=200, blank=True, null=True)

    country = models.ForeignKey('core.Country', verbose_name='Foreign Key Country', blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(max_length=128, blank=True, null=True)
    primary_contact_number = models.CharField(max_length=15, unique=True)
    secondary_contact_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(verbose_name='email address', max_length=50, unique=True, null=True,blank=True)
    dob = models.DateTimeField(verbose_name="Date of Birth", blank=True, null=True)

    is_staff = models.BooleanField(
        verbose_name='staff status', default=False,
        help_text='Designates whether the user can log into this admin site.'
    )
    is_active = models.BooleanField(
        verbose_name='active', default=True,
        help_text='Designates whether this user should be treated as active. \
            Unselect this instead of deleting accounts.'
    )

    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    modified_date = models.DateTimeField(auto_now=True, verbose_name="Last Modified")

    objects = UserManager()
    REQUIRED_FIELDS = ['primary_contact_number']
    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        db_table = 'userprofile'

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.username)

    def __unicode__(self):
        return "%s" % unicode(self.username)

    def get_short_name(self):

        return self.username

    def save(self, *args, **kwargs):
        """ """

        super(UserProfile, self).save(*args, **kwargs)
        if self.user_id in [None,'']:
            self.user_id = generate_user_id()


class WinnerMonth(models.Model):
    """
        An abstract base class implementing a fully featured User model with
        admin-compliant permissions.
        The idea is to remove the username field and also change the length of email field
    """

    month_name = models.SmallIntegerField(
        blank=True, null=True, choices=USER['WINNER_MONTH'],
        help_text=('Month in which photographer is announced as a winner')
    )

    def __unicode__(self):
        return "%s" % (unicode(self.month_name) + "," + dict(USER['WINNER_MONTH']).get(self.month_name))


class Photographer(models.Model):
    """
    Photographers model
    """

    user_ref = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Foreign Key User Model')

    username = models.CharField(max_length=50, unique=True)
    user_id = models.CharField(unique=True, max_length=20, null=True, blank=True, verbose_name="User ID")
    firstname = models.CharField(max_length=50, blank=True, null=True)
    lastname = models.CharField(max_length=50, blank=True, null=True)

    instagram_link1 = models.CharField(max_length=200, blank=True, null=True)
    instagram_link2 = models.CharField(max_length=200, blank=True, null=True)

    is_winner = models.BooleanField(
        verbose_name='Has been announced as a winner', default=False,
        help_text='Designates whether the user has won the award or not'
    )

    winner_month = models.ManyToManyField(WinnerMonth, blank=True, null=True)
    winning_date = models.DateTimeField(verbose_name="Winning Date", blank=True, null=True)

    image = GenericRelation('core.Image')

    activate_home_page = models.BooleanField(
        verbose_name='If True, Profile will be seen on the home page', default=False,
        help_text="Designates whether to show the photographer's profile on home page or not"
    )
    priority = models.IntegerField(verbose_name="Home page profile visibility priority", default=1)

    home_page_desc = models.TextField(blank=True, null=True)
    image_1_desc = models.TextField(blank=True, null=True)
    image_2_desc = models.TextField(blank=True, null=True)
    image_3_desc = models.TextField(blank=True, null=True)
    image_4_desc = models.TextField(blank=True, null=True)
    image_5_desc = models.TextField(blank=True, null=True)

    #Best photograph1er fields
    is_best_photographer = models.BooleanField(
        verbose_name='If True, Profile will be seen under best phtotographer section', default=False,
        help_text="Designates whether to show the photographer's profile under best photographer section"
    )

    best_photographer_desc = models.TextField(blank=True, null=True)
    no_of_awards = models.SmallIntegerField(verbose_name="No of awards being won", default=0)

    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    modified_date = models.DateTimeField(auto_now=True, verbose_name="Last Modified")


    class Meta:
        verbose_name = 'Photographer'
        verbose_name_plural = 'Photographers'
        db_table = 'photographer'


    def save(self, *args, **kwargs):
        """ """

        super(Photographer, self).save(*args, **kwargs)
        if self.user_id in [None,'']:
            self.user_id = generate_user_id()


    def get_email(self):
        if self.user_ref:
            return self.user_ref.email
        else:
            return ""

    get_email.short_description = 'Email'

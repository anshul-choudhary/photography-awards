import datetime
import os
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField
from django.forms.utils import ErrorList
from awards.choices import USER
from awards.settings import MEDIA_ROOT, TEMP_UPLOAD_DIR
from awards.utils import get_user_model
from core.models import Country
from useraccount.models import UserProfile, Photographer


class UserCreationForm(forms.ModelForm):

    primary_contact_number = forms.CharField(label="Mobile Number")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        # Note - include all *required* CustomUser fields here,
        fields = ("email", "primary_contact_number", "groups")

    def clean(self):
        cleaned_data = super(UserCreationForm, self).clean()

        # if len(self.cleaned_data['groups']) is 0:
        #     self._errors['groups'] = ErrorList()
        #     self._errors['groups'].append("You must select a user type !!")

        # case insensitive email existence check
        try:
            UserObj = UserProfile.objects.filter(email__iexact=cleaned_data['email'])
            if UserObj.count():
                self._errors['email'] = ErrorList()
                self._errors['email'].append("User already exist with same email address !!")

            UserObj = UserProfile.objects.filter(primary_contact_number__exact=cleaned_data['primary_contact_number'])
            if UserObj.count():
                self._errors['primary_contact_number'] = ErrorList()
                self._errors['primary_contact_number'].append("User already exist with same mobile number !!")

        except Exception as e:
            pass
        return cleaned_data


    def save(self, commit=True):

        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
        A form for updating users. Includes all the fields on
        the user, and extra field for  buyer_type/seller_type .
    """

    # B_type = [('', '----')] + USER['BUYER_TYPE']._choices
    # S_type = [('', '----')] + USER['SELLER_TYPE']._choices

    # buyer_type = forms.ChoiceField(choices=B_type, required=False)
    # seller_type = forms.ChoiceField(choices=S_type, required=False)

    def clean(self):
        cleaned_data = super(UserChangeForm, self).clean()

        # if len(self.cleaned_data['groups']) is 0:
        #     self._errors['groups'] = ErrorList()
        #     self._errors['groups'].append("You must select a user type !!")
        #
        # for group in self.cleaned_data['groups'].all():
        #     if group.name == "Seller" and not self.cleaned_data.get('seller_type'):
        #         self._errors['seller_type'] = ErrorList()
        #         self._errors['seller_type'].append(
        #             "Seller Type is required when Seller group is selected!!")
        #     elif group.name == "Buyer" and not self.cleaned_data.get('buyer_type'):
        #         self._errors['buyer_type'] = ErrorList()
        #         self._errors['buyer_type'].append(
        #             "Buyer Type is required when Buyer group is selected!!")

        return cleaned_data

    class Meta:
        model = get_user_model()
        fields = ("email", "primary_contact_number")



class UserLoginnForm(ModelForm):
    """
        A form for updating users. Includes all the fields on
        the user, and extra field for  buyer_type/seller_type .
    """

    username = forms.CharField(min_length=6, max_length=30, required=True)
    password = forms.CharField(required=True, min_length=6, max_length=20)

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')

    def clean_username(self):

        cleaned_data = super(UserLoginnForm, self).clean()

        if len(self._errors) > 0:
            return cleaned_data
        return cleaned_data

    def clean(self):
        cleaned_data = super(UserLoginnForm, self).clean()

        if len(self._errors) > 0:
            return cleaned_data
        return cleaned_data



class SignupForm(forms.ModelForm):

    firstname = forms.CharField(label="First Name", max_length=50, min_length=2)
    lastname = forms.CharField(label="Last Name", max_length=50, min_length=2)
    businessname = forms.CharField(label="Business Name", max_length=30, min_length=6)
    instagram_link1 = forms.CharField(label="Instagram Link", max_length=100, min_length=10)
    username = forms.CharField(label="Username", max_length=30, required=True, min_length=6)
    primary_contact_number = forms.CharField(label="Contact Number", max_length=15, min_length=8, required=True)
    countryval = forms.IntegerField(label="Country")
    city = forms.CharField(label="City", max_length=50)
    email = forms.EmailField(label="Email", max_length=50, required=True)
    password = forms.CharField(label="Password", min_length=6, max_length=20, required=True)

    class Meta:
        model = get_user_model()
        fields = ("firstname", "lastname", "username", "email", "primary_contact_number",
                  "instagram_link1", "city", "password")

    def clean(self):
        """ Clean Method """

        cleaned_data = super(SignupForm, self).clean()

        if len(self._errors) > 0:
            if 'country' in self._errors.keys():
                del self._errors['country']
            return cleaned_data

        try:
            UserObj = UserProfile.objects.filter(username__exact=cleaned_data['username'])
            if UserObj.count():
                self._errors['username'] = ErrorList()
                self._errors['username'].append("Username already exist, Please select another name")

            UserObj = UserProfile.objects.filter(primary_contact_number__exact=cleaned_data['primary_contact_number'])
            if UserObj.count():
                self._errors['primary_contact_number'] = ErrorList()
                self._errors['primary_contact_number'].append("Contact Number already exist, Please enter another contact")

            UserObj = UserProfile.objects.filter(email__iexact=cleaned_data['email'])
            if UserObj.count():
                self._errors['email'] = ErrorList()
                self._errors['email'].append("Email already exist, Please enter another email")

            if cleaned_data['countryval'] == -1:
                self._errors['countryval'] = ErrorList()
                self._errors['countryval'].append("This field is required")

        except Exception as e:
            pass
        return cleaned_data

    def save(self, commit=True):

        user = super(SignupForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        try:
            user.country = Country.objects.get(id=int(self.cleaned_data["countryval"]))
        except:
            pass

        if commit:
            user.save()
        return user




class EditMyprofile(forms.ModelForm):

    username = forms.CharField(label="User Name", max_length=20, min_length=6, required=True)
    firstname = forms.CharField(label="First Name", max_length=50, min_length=2, required=True)
    lastname = forms.CharField(label="Last Name", max_length=50, min_length=2, required=True)
    businessname = forms.CharField(label="Business Name", max_length=30, min_length=6, required=True)
    instagram_link1 = forms.CharField(label="Instagram Link", max_length=100, min_length=10, required=True)
    primary_contact_number = forms.CharField(label="Contact Number", max_length=15, min_length=8, required=True)
    countryval = forms.IntegerField(label="Country", required=True)
    city = forms.CharField(label="City", max_length=50, required=True)
    email = forms.EmailField(label="Email", max_length=50, required=True)


    def __init__(self, *args, **kwargs):
        super(EditMyprofile, self).__init__(*args, **kwargs)

        # del self.fields['primary_contact_number']
        # del self.fields['username']
        # del self.fields['email']
        # del self.fields['firstname']
        # del self.fields['lastname']
        # del self.fields['businessname']
        # del self.fields['instagram_link1']
        # del self.fields['countryval']
        # del self.fields['city']

    class Meta:
        model = get_user_model()
        fields = ("firstname", "lastname", "email", "primary_contact_number",
                  "instagram_link1", "city", "username")

    def validate_unique(self):
        pass

    def clean(self):
        """ Clean Method """

        cleaned_data = super(EditMyprofile, self).clean()

        if len(self._errors) > 0:
            if 'username' in self._errors.keys():
                del self._errors['username']

            if 'country' in self._errors.keys():
                del self._errors['country']

            if 'primary_contact_number' in self._errors.keys() and self._errors['primary_contact_number'] == "User with this Primary contact number already exists.":
                del self._errors['primary_contact_number']

            if 'email' in self._errors.keys() and self._errors['email'] == "User with this Email address already exists.":
                del self._errors['email']

            # return cleaned_data

        try:
            ActualUserObj = UserProfile.objects.get(username__exact=cleaned_data['username'])
            try:
                UserObj = UserProfile.objects.get(primary_contact_number__exact=cleaned_data['primary_contact_number'])
            except:
                UserObj = None
            if UserObj is None or (UserObj.primary_contact_number == ActualUserObj.primary_contact_number):
                pass
            else:
                self._errors['primary_contact_number'] = ErrorList()
                self._errors['primary_contact_number'].append("Contact Number already exist, Please enter another contact")

            try:
                UserObj = UserProfile.objects.get(email__exact=cleaned_data['email'])
            except:
                UserObj=None

            if UserObj is None or (UserObj.email == ActualUserObj.email):
                pass
            else:
                self._errors['email'] = ErrorList()
                self._errors['email'].append("Email already exist, Please enter another email")

            if cleaned_data['countryval'] == -1:
                self._errors['countryval'] = ErrorList()
                self._errors['countryval'].append("This field is required")

        except Exception as e:
            pass
        return cleaned_data


    def save(self, instance=None):

        # user = super(SignupForm, self).save(commit=False)
        try:
            if instance is not None:
                instance.save()
        except:
            pass
        return instance





class CompleteUploadForm(ModelForm):


    username = forms.CharField(max_length=500, required=True)
    home_page_desc = forms.CharField(max_length=500, required=True)
    image_1 = forms.CharField(max_length=250, required=True)
    image_1_name = forms.CharField(label='', widget=forms.HiddenInput(), required=True)
    image_1_desc = forms.CharField(label='', required=True)


    # # temporary field to store layout image location
    # image_1 = forms.CharField(max_length=250, required=False)
    # image_1_name = forms.CharField(label='', widget=forms.HiddenInput(), required=False)
    #
    #
    # # temporary field to store layout image location
    # image_1 = forms.CharField(max_length=250, required=False)
    # image_1_name = forms.CharField(label='', widget=forms.HiddenInput(), required=False)
    #
    #
    # # temporary field to store layout image location
    # image_1 = forms.CharField(max_length=250, required=False)
    # image_1_name = forms.CharField(label='', widget=forms.HiddenInput(), required=False)
    #
    #
    # # temporary field to store layout image location
    # image_1 = forms.CharField(max_length=250, required=False)
    # image_1_name = forms.CharField(label='', widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(CompleteUploadForm, self).__init__(*args, **kwargs)

        # self.fields['product_type'].widget.choices[0] = ('', '*Select Device Type')

    class Meta:
        model = Photographer
        fields = ['image_1_desc', 'home_page_desc']

    def clean(self):
        cleaned_data = super(CompleteUploadForm, self).clean()

        if len(self._errors) > 0:
            return cleaned_data

        if cleaned_data['image_1_name'] != '':
            plan_path = os.path.join(MEDIA_ROOT, os.path.join(TEMP_UPLOAD_DIR, cleaned_data['username']))
            if not os.path.exists(plan_path + '/' + cleaned_data['image_1_name']):
                raise ValidationError('Image does not exists!!')

        return cleaned_data

    def validate_unique(self):
        pass

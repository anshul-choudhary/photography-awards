import datetime
from django import forms
from django.forms import ModelForm, CharField
from django.forms.utils import ErrorList
from awards.choices import USER
from awards.utils import get_user_model
from useraccount.models import UserProfile


class UserCreationForm(forms.ModelForm):

    primary_contact_number = forms.CharField(label="Mobile Number")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        # Note - include all *required* CustomUser fields here,
        fields = ("email", "primary_contact_number", "groups", "country", "password")

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
        fields = ("email", "primary_contact_number", "password")

#
# class UserLoginForm(ModelForm):
#     """
#         A form for updating users. Includes all the fields on
#         the user, and extra field for  buyer_type/seller_type .
#     """
#
#     username = CharField(max_length=30, required=True)  #Customer Id
#     password = CharField(max_length=20, required=True)  #Customer Dob
#     primary_contact_number = CharField(max_length=30, required=True)  #Contact Number
#
#     def clean(self):
#         cleaned_data = super(UserLoginForm, self).clean()
#
#         if len(self._errors) > 0:
#             return cleaned_data
#
#         UserObj = UserProfile.objects.filter(user_id__exact=cleaned_data['user_id'].upper())
#         if not UserObj.count():
#             self._errors['user_id'] = ErrorList(["* Incorrect Customer Id"])
#             return cleaned_data
#         else:
#             if not UserObj[0].check_password(cleaned_data['password']):
#                 self._errors['password'] = ErrorList(["* Incorrect Username and Password"])
#                 return cleaned_data
#
#         if len(cleaned_data['password']) != 8:
#             self._errors['password'] = ErrorList(["* Invalid password"])
#             return cleaned_data
#
#         try:
#             dob = datetime.datetime.strptime(cleaned_data['password'], "%d%m%Y")
#         except:
#             #Wrong password entered
#             self._errors['password'] = ErrorList(["* Invalid date format"])
#             return cleaned_data
#
#         UserObj = UserProfile.objects.filter(user_id__exact=cleaned_data['user_id'].upper(), primary_contact_number__exact=cleaned_data['primary_contact_number'])
#         if not UserObj.count():
#             self._errors['primary_contact_number'] = ErrorList(["* Invalid Mobile No"])
#             return cleaned_data
#
#         UserObj = UserProfile.objects.filter(user_id__exact=cleaned_data['user_id'].upper(), primary_contact_number__exact=cleaned_data['primary_contact_number'], servicetype__in=[int(cleaned_data['servicetype'])])
#         if int(cleaned_data['servicetype']) not in [USER['SERVICE_TYPE'].Unknown, USER['SERVICE_TYPE'].Insurance, USER['SERVICE_TYPE'].Service]:
#             self._errors['servicetype'] = ErrorList(["* Invalid Service Type"])
#             return cleaned_data
#
#         return cleaned_data
#
#
#     class Meta:
#         model = get_user_model()
#         fields = ('user_id', 'password', 'primary_contact_number')
#
#
# class UserSignupForm(ModelForm):
#     """
#         A form for updating users. Includes all the fields on
#         the user, and extra field for  buyer_type/seller_type .
#     """
#
#     user_id = CharField(max_length=6, required=True)
#     password = forms.RegexField(regex=r'^\d{8}$', required=True)
#     primary_contact_number = forms.RegexField(regex=r'^\d{10}$', required=True, error_message="Enter a valid mobile number")
#     servicetype = CharField(max_length=20, required=True)
#
#     def clean(self):
#         cleaned_data = super(UserSignupForm, self).clean()
#
#         if len(self._errors) > 0:
#             return cleaned_data
#
#         UserObj = UserProfile.objects.filter(user_id__exact=cleaned_data['user_id'].upper())
#         if UserObj.count() > 0:
#             self._errors['user_id'] = ErrorList(["* User Id already exists, Type another one"])
#
#         if len(cleaned_data['password']) != 8:
#             self._errors['password'] = ErrorList(["* Invalid password"])
#
#         try:
#             dob = datetime.datetime.strptime(cleaned_data['password'], "%d%m%Y")
#         except:
#             #Wrong password entered
#             self._errors['password'] = ErrorList(["* Invalid date format"])
#
#         UserObj = UserProfile.objects.filter(primary_contact_number__exact=cleaned_data['primary_contact_number'])
#         if UserObj.count() > 0:
#             self._errors['primary_contact_number'] = ErrorList(["* Number already exists, Enter another one"])
#
#         if int(cleaned_data['servicetype']) not in [USER['SERVICE_TYPE'].Unknown, USER['SERVICE_TYPE'].Insurance, USER['SERVICE_TYPE'].Service]:
#             self._errors['servicetype'] = ErrorList(["* Service does not exist"])
#
#         return cleaned_data
#
#     class Meta:
#         model = get_user_model()
#         fields = ('user_id', 'password', 'primary_contact_number', 'servicetype')
#
#

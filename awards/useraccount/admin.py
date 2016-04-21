from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.core.checks import messages
from awards.utils import generate_user_id
from core.forms import ImageInlineForm
from core.models import Image
from useraccount.forms import UserCreationForm, UserChangeForm, PhotographerImageForm
from useraccount.models import UserProfile, Photographer, WinnerMonth


class UserProfileAdmin(UserAdmin):

    add_form = UserCreationForm
    form = UserChangeForm

    list_display = (
        'id', 'user_id', 'username', 'email', 'is_staff', 'is_superuser', 'primary_contact_number', 'created_date',
        'country'
    )

    fieldsets = [
        (
            'User Information',
            {
                'fields': (
                    'user_id', 'username', 'firstname', 'lastname', 'email', 'country', 'address',
                    'state', 'city', 'primary_contact_number',
                )
            }
        ),
        (
            'Account Info',
            {
                'fields': (
                    'last_login', 'groups', 'user_permissions', 'password'
                )
            }
        ),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
    ]

    restricted_fieldsets = (
        (
            'User Information',
            {
                'fields': (
                    'user_id', 'username', 'firstname', 'lastname', 'email', 'country', 'address',
                    'state', 'city', 'primary_contact_number',
                )
            }
        ),
    )

    add_fieldsets = (
        (
            'User Information',
            {
                'fields': (
                    'user_id', 'username', 'firstname', 'lastname', 'email', 'country', 'address',
                    'state', 'city', 'primary_contact_number',
                )
            }
        ),
        (
            'Account Info',
            {
                'fields': (
                    'last_login', 'groups', 'user_permissions', 'password'
                )
            }
        ),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
    )


    readonly_fields = ['user_id']
    ordering = ('-created_date',)

    list_filter = ('is_staff', 'is_superuser', 'is_active', 'created_date')
    search_fields = (
        'primary_contact_number', 'username', 'email', 'user_id',
        'id', 'firstname', 'lastname', 'country__name'
    )
    exclude = ('password1', 'password2')

    def get_fieldsets(self, request, obj=None):

        if not request.user.is_superuser:
            return self.restricted_fieldsets
        else:
            return super(UserProfileAdmin, self).get_fieldsets(request, obj=obj)

    def save_model(self, request, obj, form, change):
        """ """

        if request.user.is_superuser:
            if obj.user_id in [None,'']:
                obj.user_id = generate_user_id(prefix="USR")
            if change and ('password' in form.changed_data):
                obj.set_password(form.cleaned_data['password'])
            obj.save()
        else:
            messages.error(request, "You are not authorized to create an entry")
        return

    # def change_view(self, request, object_id,extra_context=None):
    #
    #     result = super(UserProfileAdmin, self).change_view(request, object_id, extra_context)
    #     result['Location'] = "/admin/useraccount/userprofile/"
    #     return result



class ImagePhotographerAdmin(GenericTabularInline):
    model = Image
    extra = 1
    verbose_name_plural = 'Images'
    form = ImageInlineForm


class PhotographerAdmin(admin.ModelAdmin):
    form = PhotographerImageForm
    inlines = [ImagePhotographerAdmin]

    list_display = (
        'id', 'user_ref', 'user_id', 'firstname', 'lastname', 'username', \
        'is_winner', 'activate_home_page', 'is_best_photographer', 'no_of_awards', 'created_date', \
        'modified_date',
    )

    fieldsets = [
        (
            'User Information',
            {
                'fields': (
                    'user_ref', 'user_id', 'username', 'firstname', 'lastname',
                )
            }
        ),
        (
            'Photography Related Information',
            {
                'fields': (
                    'instagram_link1', 'instagram_link2', 'is_winner', 'winner_month', 'winning_date', \
                    'activate_home_page', 'home_page_desc', 'is_best_photographer', \
                    'best_photographer_desc', 'no_of_awards',
                )
            }
        ),
    ]

    readonly_fields = []
    ordering = ('-created_date',)
    list_filter = ('is_winner', 'activate_home_page', 'is_best_photographer', 'activate_home_page', \
                   'created_date')

    search_fields = ('id', 'user_id', 'username', 'user_ref__email')

    class Media:
        js = ('/static/styles/js/photographeradmin.js',)

    # def save_model(self, request, obj, form, change):
    #     """ """
    #
    #     if request.user.is_superuser:
    #         obj.user_id = generate_user_id(prefix="USR")
    #         if change and ('password' in form.changed_data):
    #             obj.set_password(form.cleaned_data['password'])
    #         obj.save()
    #     else:
    #         messages.error(request, "You are not authorized to create an entry")
    #     return

    # def change_view(self, request, object_id,extra_context=None):
    #
    #     result = super(UserProfileAdmin, self).change_view(request, object_id, extra_context)
    #     result['Location'] = "/admin/useraccount/userprofile/"
    #     return result


class WinnermonthAdmin(admin.ModelAdmin):
    search_fields = ['month_name', 'id']
    list_display = ('id', 'month_name')



admin.site.register(Photographer, PhotographerAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(WinnerMonth, WinnermonthAdmin)




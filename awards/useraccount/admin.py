from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.core.checks import messages
from awards.utils import generate_user_id
from useraccount.forms import UserCreationForm, UserChangeForm
from useraccount.models import UserProfile


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
            obj.user_id = generate_user_id(prefix="USR")
            if change and ('password' in form.changed_data):
                obj.set_password(form.cleaned_data['password'])
            obj.save()
        else:
            messages.error(request, "You are not authorized to create an entry")
        return

    def change_view(self, request, object_id,extra_context=None):

        result = super(UserProfileAdmin, self).change_view(request, object_id, extra_context)
        result['Location'] = "/admin/useraccount/userprofile/"
        return result

admin.site.register(UserProfile, UserProfileAdmin)

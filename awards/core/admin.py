from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from core.forms import ImageInlineForm, FooterImageForm
from core.models import Image, Setting, Footer, Faqs, Country, State, City, Locality


class CountryAdmin(admin.ModelAdmin):

    search_fields = ['id', 'name']
    ordering = ('name',)
    list_display = ('id', 'name')


class StateAdmin(admin.ModelAdmin):

    search_fields = ['id', 'name', 'country__name']
    ordering = ('name',)
    list_display = ('id', 'name', 'country')
    list_select_related = ('country',)


class CityAdmin(admin.ModelAdmin):

    search_fields = ['id', 'name']
    ordering = ('name',)
    list_display = ('id', 'name', 'state')
    list_select_related = ('state',)

#
# def download_Localities_details(modeladmin, request, queryset):
#     """
#     Download localities data as a csv file.
#     """
#     from debroker.apps.geoinfo.utils import download_locality_details
#     return download_locality_details(request, queryset)
#
# download_Localities_details.short_description = "Download selected localities data"


class LocalityAdmin(admin.ModelAdmin):

    search_fields = ['id', 'name', '']
    ordering = ('name',)
    list_filter = ('city', 'city__state', 'city__state__country')
    list_display = ('id', 'name', 'city')
    list_select_related = ('city',)
    # actions = [download_Localities_details]


class ImageAdmin(GenericTabularInline):

    model = Image
    extra = 1
    verbose_name_plural = 'Images'


class SettingAdmin(admin.ModelAdmin):

    list_display = ('id', 'key', 'value', 'description', 'created_date', 'modified_date')
    save_on_top = True
    list_per_page = 40
    ordering = ('-created_date',)
    search_fields = ['key']


class FaqsAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'priority', 'description')
    save_on_top = True
    list_per_page = 40
    ordering = ('created_date',)
    search_fields = ['id']


class ImageFooterAdmin(GenericTabularInline):

    model = Image
    extra = 1
    verbose_name_plural = 'Images'
    form = ImageInlineForm


class FooterAdmin(admin.ModelAdmin):

    form = FooterImageForm
    inlines = [ImageFooterAdmin]
    list_display = ('id', 'link1', 'priority', 'active', 'created_date', 'modified_date')
    search_fields = ['id', 'link1']
    ordering = ('-created_date',)
    readonly_fields = ['created_date', 'modified_date']

    class Media:
        js = ('/static/styles/js/footeradmin.js',)

    # def get_footer_url(self, obj):
    #     ''' Make the urls clickable '''
    #
    #     return '<a href="%s" class="link" target="_blank">%s</a>' % (obj.url,obj.url)
    #
    # get_footer_url.short_description = 'Url'
    # get_footer_url.allow_tags = True


admin.site.register(Setting, SettingAdmin)
admin.site.register(Footer, FooterAdmin)
admin.site.register(Faqs, FaqsAdmin)

admin.site.register(Country, CountryAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Locality, LocalityAdmin)





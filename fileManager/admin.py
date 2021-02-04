from django.contrib import admin
from fileManager.models import UserContainer, Content


class ContainerAdmin(admin.ModelAdmin):
    list_display = ['email', 'name_container']


class ContentAdmin(admin.ModelAdmin):
    list_display = ['name_of_blob', 'unique_link_to_blob', 'container']
    list_display_links = ['container']


admin.site.register(UserContainer, ContainerAdmin)
admin.site.register(Content, ContentAdmin)
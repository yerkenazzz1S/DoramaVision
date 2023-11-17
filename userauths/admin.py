from .models import *
from django.contrib import admin


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username')
    list_display_links = ('id', 'email', 'username')
    search_fields = ('email', 'username')


admin.site.register(User, UserAdmin)

from django.contrib import admin


from accountapp.models import *


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name',)
    

admin.site.register(User, CustomUserAdmin)
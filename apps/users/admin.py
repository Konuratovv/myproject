from django.contrib import admin
from django.contrib.auth.models import Group

from apps.users.models import Profile
# Register your models here.

admin.site.unregister(Group)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'first_name',
        'last_name',
        'email',
        'desription',
        'city',
    ]

    readonly_fields = ['password']
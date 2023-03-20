from django.contrib import admin
from .models import UserAddProfile,UserRoles
# Register your models here.

admin.site.register(UserAddProfile)
admin.site.register(UserRoles)
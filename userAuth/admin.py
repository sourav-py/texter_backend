from django.contrib import admin
from .models import Profile, OTPObject, UserActivity

# Register your models here.

admin.site.register(Profile)
admin.site.register(OTPObject)
admin.site.register(UserActivity)

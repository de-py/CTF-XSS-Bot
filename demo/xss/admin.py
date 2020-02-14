from django.contrib import admin

# Register your models here.
from .models import Profile, IP, Session, Flag
from django.contrib.auth.models import User




admin.site.register(Profile)
admin.site.register(IP)
admin.site.register(Session)
admin.site.register(Flag)


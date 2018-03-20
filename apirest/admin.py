from django.contrib import admin
from .models import *
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.

UserAdmin.list_display = ('id','first_name','last_name','email','date_joined')
#UserAdmin.list_editable = ('first_name','last_name','email','date_joined')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(cliente)
admin.site.register(user_cli)
admin.site.register(grupo_juego)

from django.contrib import admin

from .models import Purchase, User

admin.site.register(User)
admin.site.register(Purchase)

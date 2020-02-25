from django.contrib import admin

# Register your models here.
from .models import Request,Comment,Event

admin.site.register(Request)
admin.site.register(Comment)
admin.site.register(Event)
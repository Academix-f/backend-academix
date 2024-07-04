from django.contrib import admin
from .models import Notification,Request, Report
# Register your models here.
admin.site.register(Notification)
admin.site.register(Request)
admin.site.register(Report)
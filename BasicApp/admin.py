from django.contrib import admin
from .models import Department, Course
from .models import Building

# Register your models here.

admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Building)

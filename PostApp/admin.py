from django.contrib import admin
from .models import MyUser
from CommunityApp.models import Club, Section
from BasicApp.models import Course
from .models import Post, Comment, Like

# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)

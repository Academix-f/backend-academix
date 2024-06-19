from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, Permission
# Create your models here.


class MyUser(AbstractUser):
    gender = models.CharField(max_length=20 , null=True)
    phone_number = models.CharField()
    student = models.OneToOneField('Student', null=True, on_delete=models.SET_NULL)
    admin = models.OneToOneField('Admin', null=True, on_delete=models.SET_NULL)
    telegram = models.CharField(max_length=20 , null=True)
    linkedin = models.CharField(max_length=20 , null=True)
    instagram = models.CharField(max_length=20 , null=True)


class Student(models.Model):
    student_id = models.CharField()
    academic_year = models.IntegerField(null=True)
    is_rep = models.BooleanField(default=False)
    section = models.ForeignKey('CommunityApp.Section', null=True, on_delete=models.SET_NULL, related_name='student')##
    department = models.ForeignKey('BasicApp.Department', null=True, on_delete=models.SET_NULL, related_name='student') ##
    groups = models.ManyToManyField(Group, related_name='student_users')
    user_permissions = models.ManyToManyField(Permission, related_name='student_users_permissions')

class Admin(models.Model):
    department = models.ForeignKey('BasicApp.Department', default=1, on_delete=models.CASCADE, related_name='admin') ##
    groups = models.ManyToManyField(Group, related_name='admin_users')
    user_permissions = models.ManyToManyField(Permission, related_name='admin_users_permissions')


    










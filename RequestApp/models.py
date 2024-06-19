from django.db import models
# Create your models here.

class Request(models.Model):
    description = models.TextField()
    student = models.OneToOneField('UserApp.MyUser', on_delete=models.CASCADE, related_name='student_request') ###
    post = models.JSONField( null = True)
    club = models.JSONField(null = True)
    event = models.JSONField( null = True)

class Report(models.Model):
    status = models.IntegerField(default=None)
    user = models.OneToOneField('UserApp.MyUser', on_delete=models.CASCADE) ##
    post = models.OneToOneField('PostApp.Post', on_delete=models.CASCADE) ##

class Notification(models.Model):
    to_user = models.ForeignKey('UserApp.MyUser' ,null=True , on_delete= models.CASCADE)
    status = models.IntegerField(null=True)
    content = models.TextField()





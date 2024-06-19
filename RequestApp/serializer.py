from rest_framework import serializers
from .models import Request, Report , Notification
from CommunityApp.views import create_club
from PostApp.views import post_detail
from CommunityApp.views import *
from UserApp.models import MyUser

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['id', 'description','student','post','club','event']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        user = MyUser.objects.filter(id=instance.student.id).first()
        ret['first_name'] = user.first_name
        ret['last_name'] = user.last_name
        ret['student_id'] = user.student.student_id
        return ret

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'user','post','status']
        
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

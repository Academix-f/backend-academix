from rest_framework import serializers
from .models import Student, Admin, MyUser
import re
from BasicApp.models import Department

class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'username', 'first_name', 'last_name', 'student', 'is_staff', 'phone_number', 'email', 'password', 'gender', 'telegram', 'linkedin', 'instagram']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.department:
            department = Department.objects.filter(id=instance.department).first()
            if department:
                ret['department_name'] = department.name
        return ret

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['student_id', 'academic_year', 'is_rep', 'section', 'department']

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['department']

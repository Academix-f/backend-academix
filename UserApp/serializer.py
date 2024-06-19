from rest_framework import serializers
from .models import Student, Admin, MyUser
import re
from BasicApp.models import Department


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'username', 'first_name', 'last_name', 'student',  'is_staff', 'phone_number', 'email', 'password', 'gender', 'telegram', 'linkedin', 'instagram']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        department = Department.objects.filter(id = instance.department)

        ret['department_name'] = department.name

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['student_id', 'academic_year', 'is_rep', 'section', 'department']
    
    def validate_student_id(self, value):
        if not re.match('[a-zA-Z]{3}[0-9]{4}\/[0-9]{2}', value):
            raise serializers.ValidationError('school id wrong eg. ETS0333/14')
        return value

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['department']

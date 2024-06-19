from rest_framework import serializers
from .models import Department, Course, Building


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", 'head', 'name', 'overview']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", 'name', 'department', 'academic_year', 'semester', 'credit_hour', 'lecture_hour', 'overview']

class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = ["id", 'name', 'block_number', 'tyoe', 'description']

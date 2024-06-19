from rest_framework import serializers
from .models import *
class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ['id','name','founder','overview','members']

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.member.add(self.context['request'].user)
        
        return instance

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id','club','building','start_time','end_time','description']

from rest_framework import serializers
from app01.models import *

class OldPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = oldperson_info
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = event_info
        exclude = ['id']


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = employee_info
        fields = '__all__'


class VolunteerSerializer(serializers.ModelSerializer):
    class Meta:
        model = volunteer_info
        fields = '__all__'


class SysUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = sys_user
        fields = '__all__'


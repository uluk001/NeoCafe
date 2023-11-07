from apps.branches.models import Branch, Schedule, Workdays
from rest_framework import serializers

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'


class WorkdaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workdays
        fields = '__all__'


class BranchSerializer(serializers.ModelSerializer):
    schedule = ScheduleSerializer()
    workdays = WorkdaysSerializer(many=True)

    class Meta:
        model = Branch
        fields = '__all__'
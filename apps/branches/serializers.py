from rest_framework import serializers
from .models import Branch, Schedule, Workdays

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['id', 'title', 'description']

class WorkdaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workdays
        fields = ['id', 'workday', 'start_time', 'end_time']

class BranchSerializer(serializers.ModelSerializer):
    schedule = ScheduleSerializer()
    workdays = WorkdaysSerializer(many=True, read_only=True)

    class Meta:
        model = Branch
        fields = ['id', 'image', 'schedule', 'address', 'phone_number', 'link_to_map', 'workdays']
    
    def validate_workdays(self, value):
        for workday_data in value:
            WorkdaysSerializer(data=workday_data).is_valid(raise_exception=True)
        return value

    def create(self, validated_data):
        schedule_data = validated_data.pop('schedule')
        schedule = Schedule.objects.create(**schedule_data)
        branch = Branch.objects.create(schedule=schedule, **validated_data)

        if 'workdays' in self.initial_data:
            workdays_data = self.initial_data['workdays']
            print(workdays_data)
            for workday_data in workdays_data:
                workday_serializer = WorkdaysSerializer(data=workday_data)
                if workday_serializer.is_valid(raise_exception=True):
                    workday = workday_serializer.save(schedule=schedule)

        return branch
from apps.storage.models import AvailableAtTheBranch, Category, Composition, Ingredient, Item, ReadyMadeProduct, ReadyMadeProductAvailableAtTheBranch
from rest_framework import serializers
from apps.accounts.models import CustomUser, EmployeeSchedule, EmployeeWorkdays


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Item
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class CompositionSerializer(serializers.ModelSerializer):
    item = ItemSerializer()
    ingredient = IngredientSerializer()

    class Meta:
        model = Composition
        fields = '__all__'


class ReadyMadeProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadyMadeProduct
        fields = '__all__'


class AvailableAtTheBranchSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()

    class Meta:
        model = AvailableAtTheBranch
        fields = '__all__'


class ReadyMadeProductAvailableAtTheBranchSerializer(serializers.ModelSerializer):
    ready_made_product = ReadyMadeProductSerializer()

    class Meta:
        model = ReadyMadeProductAvailableAtTheBranch
        fields = '__all__'


class ItemDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    composition = CompositionSerializer(many=True)
    available_at_the_branch = AvailableAtTheBranchSerializer(many=True)
    ready_made_product_available_at_the_branch = ReadyMadeProductAvailableAtTheBranchSerializer(many=True)

    class Meta:
        model = Item
        fields = '__all__'


class ItemsWithBranchesAndQuantitiesSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    available_at_the_branch = AvailableAtTheBranchSerializer(many=True)

    class Meta:
        model = Item
        fields = '__all__'


class EmployeeScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeSchedule
        fields = ['id', 'title']


class EmployeeWorkdaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeWorkdays
        fields = ['id', 'workday', 'start_time', 'end_time']


class EmployeeSerializer(serializers.ModelSerializer):
    schedule = EmployeeScheduleSerializer()
    workdays = EmployeeWorkdaysSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'first_name', 'position', 'birth_date', 'phone_number', 'branch', 'schedule', 'workdays']

    def validate_workdays(self, value):
        for workday_data in value:
            EmployeeWorkdaysSerializer(data=workday_data).is_valid(raise_exception=True)
        return value

    def create(self, validated_data):
        schedule_data = validated_data.pop('schedule')
        schedule = EmployeeSchedule.objects.create(**schedule_data)
        employee = CustomUser.objects.create(schedule=schedule, **validated_data)

        if 'workdays' in self.initial_data:
            workdays_data = self.initial_data['workdays']
            print(workdays_data)
            for workday_data in workdays_data:
                workday_serializer = EmployeeWorkdaysSerializer(data=workday_data)
                if workday_serializer.is_valid(raise_exception=True):
                    workday = workday_serializer.save(schedule=schedule)

        return employee
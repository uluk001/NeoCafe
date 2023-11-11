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


class EmployeeWorkdaysSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmployeeWorkdays
        fields = ['id', 'workday', 'start_time', 'end_time']


class EmployeeScheduleSerializer(serializers.ModelSerializer):
    workdays = EmployeeWorkdaysSerializer(many=True, read_only=True)

    class Meta:
        model = EmployeeSchedule
        fields = ['id', 'title', 'workdays']


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


class EmployeeCreateSerializer(serializers.ModelSerializer):
    workdays = EmployeeWorkdaysSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'first_name', 'position', 'birth_date', 'phone_number', 'branch', 'workdays']

    def validate_workdays(self, value):
        for workday_data in value:
            EmployeeWorkdaysSerializer(data=workday_data).is_valid(raise_exception=True)
        return value

    def create(self, validated_data):
        schedule_data = {"title": f"График работы {validated_data['first_name']}"}
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


class EmployeeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'position', 'birth_date', 'phone_number', 'branch']

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.position = validated_data.get('position', instance.position)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.branch = validated_data.get('branch', instance.branch)
        instance.save()
        return instance


class ScheduleUpdateSerializer(serializers.ModelSerializer):
    workdays = EmployeeWorkdaysSerializer(many=True)

    class Meta:
        model = EmployeeSchedule
        fields = ['title', 'workdays']

    def update(self, instance, validated_data):
        user_id = self.context['user_id']
        user = CustomUser.objects.get(id=user_id)
        schedule = user.schedule

        schedule.title = validated_data.get('title', schedule.title)
        schedule.save()

        # Удалить существующие записи
        schedule.workdays.all().delete()

        workdays_data = validated_data.pop('workdays', [])

        # Добавить новые записи
        for workday_data in workdays_data:
            workday_serializer = EmployeeWorkdaysSerializer(data=workday_data)
            if workday_serializer.is_valid(raise_exception=True):
                workday_serializer.save(schedule=schedule)

        return schedule
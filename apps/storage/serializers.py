from rest_framework import serializers

from apps.accounts.models import CustomUser, EmployeeSchedule, EmployeeWorkdays
from apps.storage.models import (
    AvailableAtTheBranch,
    Category,
    Composition,
    Ingredient,
    Item,
    ReadyMadeProduct,
    ReadyMadeProductAvailableAtTheBranch,
)


# Categories
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


# Employees
class EmployeeWorkdaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeWorkdays
        fields = ["id", "workday", "start_time", "end_time"]


class EmployeeScheduleSerializer(serializers.ModelSerializer):
    workdays = EmployeeWorkdaysSerializer(many=True, read_only=True)

    class Meta:
        model = EmployeeSchedule
        fields = ["id", "title", "workdays"]


class EmployeeSerializer(serializers.ModelSerializer):
    schedule = EmployeeScheduleSerializer()
    workdays = EmployeeWorkdaysSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "password",
            "first_name",
            "position",
            "birth_date",
            "phone_number",
            "branch",
            "schedule",
            "workdays",
        ]

    def validate_workdays(self, value):
        for workday_data in value:
            EmployeeWorkdaysSerializer(data=workday_data).is_valid(raise_exception=True)
        return value


class EmployeeCreateSerializer(serializers.ModelSerializer):
    workdays = EmployeeWorkdaysSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "password",
            "first_name",
            "position",
            "birth_date",
            "phone_number",
            "branch",
            "workdays",
        ]

    def validate_workdays(self, value):
        for workday_data in value:
            EmployeeWorkdaysSerializer(data=workday_data).is_valid(raise_exception=True)
        return value

    def create(self, validated_data):
        schedule_data = {"title": f"График работы {validated_data['first_name']}"}

        schedule = EmployeeSchedule.objects.create(**schedule_data)
        employee = CustomUser.objects.create(schedule=schedule, **validated_data)

        if "workdays" in self.initial_data:
            workdays_data = self.initial_data["workdays"]
            print(workdays_data)
            for workday_data in workdays_data:
                workday_serializer = EmployeeWorkdaysSerializer(data=workday_data)
                if workday_serializer.is_valid(raise_exception=True):
                    workday = workday_serializer.save(schedule=schedule)


class EmployeeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "username",
            "first_name",
            "position",
            "birth_date",
            "phone_number",
            "branch",
        ]

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.position = validated_data.get("position", instance.position)
        instance.birth_date = validated_data.get("birth_date", instance.birth_date)
        instance.phone_number = validated_data.get(
            "phone_number", instance.phone_number
        )
        instance.branch = validated_data.get("branch", instance.branch)
        instance.save()
        return instance


class ScheduleUpdateSerializer(serializers.ModelSerializer):
    workdays = EmployeeWorkdaysSerializer(many=True)

    class Meta:
        model = EmployeeSchedule
        fields = ["title", "workdays"]

    def update(self, instance, validated_data):
        user_id = self.context["user_id"]
        user = CustomUser.objects.get(id=user_id)
        schedule = user.schedule

        schedule.title = validated_data.get("title", schedule.title)
        schedule.save()

        schedule.workdays.all().delete()

        workdays_data = validated_data.pop("workdays", [])

        for workday_data in workdays_data:
            workday_serializer = EmployeeWorkdaysSerializer(data=workday_data)
            if workday_serializer.is_valid(raise_exception=True):
                workday_serializer.save(schedule=schedule)

        return schedule


# Ingredients
class AvailableAtTheBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableAtTheBranch
        fields = ["id", "branch", "quantity"]


class CreateIngredientSerializer(serializers.ModelSerializer):
    available_at_branches = AvailableAtTheBranchSerializer(many=True, write_only=True)

    class Meta:
        model = Ingredient
        fields = [
            "id",
            "category",
            "name",
            "measurement_unit",
            "minimal_limit",
            "available_at_branches",
        ]

    def create(self, validated_data):
        available_at_branches_data = validated_data.pop("available_at_branches", [])
        ingredient = Ingredient.objects.create(**validated_data)
        for available_at_branch_data in available_at_branches_data:
            AvailableAtTheBranch.objects.create(
                ingredient=ingredient, **available_at_branch_data
            )
        return ingredient

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["available_at_branches"] = AvailableAtTheBranchSerializer(
            AvailableAtTheBranch.objects.filter(ingredient=instance), many=True
        ).data
        return representation


class IngredientSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Ingredient
        fields = [
            "id",
            "name",
            "measurement_unit",
            "minimal_limit",
            "date_of_arrival",
            "category",
        ]


# Items
class CompositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Composition
        fields = ["id", "ingredient", "quantity"]


class CreateItemSerializer(serializers.ModelSerializer):
    composition = CompositionSerializer(many=True, write_only=True)

    class Meta:
        model = Item
        fields = [
            "id",
            "category",
            "name",
            "description",
            "price",
            "image",
            "composition",
            "is_available",
        ]

    def create(self, validated_data):
        composition_data = validated_data.pop("composition", [])
        item = Item.objects.create(**validated_data)
        for composition in composition_data:
            Composition.objects.create(item=item, **composition)
        return item

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["composition"] = CompositionSerializer(
            Composition.objects.filter(item=instance), many=True
        ).data
        return representation


class ItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    composition = CompositionSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = [
            "id",
            "name",
            "description",
            "price",
            "image",
            "composition",
            "is_available",
            "category",
        ]


class UpdateItemSerializer(serializers.ModelSerializer):
    composition = CompositionSerializer(many=True)

    class Meta:
        model = Item
        fields = [
            "id",
            "category",
            "name",
            "description",
            "price",
            "image",
            "composition",
            "is_available",
        ]

    def update(self, instance, validated_data):
        composition_data = validated_data.pop('composition', [])
        instance = super().update(instance, validated_data)

        instance.composition.all().delete()

        for composition in composition_data:
            Composition.objects.create(item=instance, **composition)

        return instance


# Ready-made products
class ReadyMadeProductAvailableAtTheBranchSerializer(serializers.ModelSerializer):
    ready_made_product = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ReadyMadeProductAvailableAtTheBranch
        fields = ["id", "branch", "ready_made_product", "quantity"]


class CreateReadyMadeProductSerializer(serializers.ModelSerializer):
    available_at_branches = ReadyMadeProductAvailableAtTheBranchSerializer(many=True, write_only=True)

    class Meta:
        model = ReadyMadeProduct
        fields = [
            "id",
            "name",
            "minimal_limit",
            "description",
            "price",
            "available_at_branches",
        ]

    def create(self, validated_data):
        available_at_branches_data = validated_data.pop("available_at_branches", [])
        product = ReadyMadeProduct.objects.create(**validated_data)
        for available_at_branch_data in available_at_branches_data:
            ReadyMadeProductAvailableAtTheBranch.objects.create(
                ready_made_product=product, **available_at_branch_data
            )
        return product

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["available_at_branches"] = ReadyMadeProductAvailableAtTheBranchSerializer(
            ReadyMadeProductAvailableAtTheBranch.objects.filter(ready_made_product=instance), many=True
        ).data
        return representation

class ReadyMadeProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadyMadeProduct
        fields = [
            "id",
            "name",
            "minimal_limit",
            "description",
            "price",
        ]

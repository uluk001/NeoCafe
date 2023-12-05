"""
Serializers for storage app.
"""
from django.db import models, transaction
from rest_framework import serializers

from apps.accounts.models import CustomUser, EmployeeSchedule, EmployeeWorkdays
from apps.storage.models import (AvailableAtTheBranch, Category, Composition,
                                 Ingredient, Item, MinimalLimitReached,
                                 ReadyMadeProduct,
                                 ReadyMadeProductAvailableAtTheBranch)


# =====================================================================
# CATEGORY SERIALIZER
# =====================================================================
class CategorySerializer(serializers.ModelSerializer):
    """
    Category serializer.
    """

    class Meta:
        model = Category
        fields = "__all__"


# =====================================================================
# EMPLOYEE SERIALIZERS
# =====================================================================
class EmployeeWorkdaysSerializer(serializers.ModelSerializer):
    """
    EmployeeWorkdays serializer.
    """

    class Meta:
        model = EmployeeWorkdays
        fields = ["id", "workday", "start_time", "end_time"]

    def create(self, validated_data):
        """
        Create employee workdays.
        """
        employee_workdays = EmployeeWorkdays.objects.create(**validated_data)
        return employee_workdays


class EmployeeScheduleSerializer(serializers.ModelSerializer):
    """
    EmployeeSchedule serializer for EmployeeSerializer and ScheduleUpdateSerializer.
    """

    workdays = EmployeeWorkdaysSerializer(many=True, read_only=True)

    class Meta:
        model = EmployeeSchedule
        fields = ["id", "title", "workdays"]


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Employee serializer.
    """

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
        """
        Validate workdays data.
        """
        for workday_data in value:
            EmployeeWorkdaysSerializer(data=workday_data).is_valid(raise_exception=True)
        return value


class EmployeeCreateSerializer(serializers.ModelSerializer):
    """
    Employee create serializer.
    """

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
        """
        Validate workdays data.
        """
        for workday_data in value:
            EmployeeWorkdaysSerializer(data=workday_data).is_valid(raise_exception=True)
        return value

    def create(self, validated_data):
        """
        Create employee.
        """

        if CustomUser.objects.filter(username=validated_data["username"]).exists():
            raise serializers.ValidationError(
                {"username": "User with this username already exists."}
            )

        schedule_data = {"title": f"{validated_data['first_name']}'s schedule"}

        schedule = EmployeeSchedule.objects.create(**schedule_data)
        password = validated_data.pop('password')
        user = CustomUser.objects.create(schedule=schedule, **validated_data)
        user.set_password(password)
        user.save()

        if "workdays" in self.initial_data:
            workdays_data = self.initial_data["workdays"]
            for workday_data in workdays_data:
                workday_serializer = EmployeeWorkdaysSerializer(data=workday_data)
                if workday_serializer.is_valid(raise_exception=True):
                    workday_serializer.save(schedule=schedule)

        return CustomUser.objects.get(username=validated_data["username"])


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
        """
        Update employee.
        """
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
    """
    Schedule update serializer.
    """

    workdays = EmployeeWorkdaysSerializer(many=True)

    class Meta:
        model = EmployeeSchedule
        fields = ["workdays"]

    def update(self, instance, validated_data):
        """
        Update schedule.
        """
        user_id = self.context["user_id"]
        user = CustomUser.objects.get(id=user_id)
        schedule = user.schedule

        schedule.title = f"{user.first_name}'s schedule"
        schedule.save()

        schedule.workdays.all().delete()

        workdays_data = validated_data.pop("workdays", [])

        for workday_data in workdays_data:
            workday_serializer = EmployeeWorkdaysSerializer(data=workday_data)
            if workday_serializer.is_valid(raise_exception=True):
                workday_serializer.save(schedule=schedule)

        return schedule


# =====================================================================
# INGREDIENT SERIALIZERS
# =====================================================================
class AvailableAtTheBranchSerializer(serializers.ModelSerializer):
    """
    AvailableAtTheBranch serializer.
    """

    branch = serializers.StringRelatedField()
    ingredient = serializers.StringRelatedField()

    class Meta:
        model = AvailableAtTheBranch
        fields = ["id", "branch", "ingredient", "quantity"]

    def to_representation(self, instance):
        """
        Change quantity to kg or l if measurement unit is kg or l.
        """
        representation = super().to_representation(instance)
        representation["ingredient"] = instance.ingredient.name
        representation["branch"] = instance.branch.name_of_shop
        quantity = (
            round(instance.quantity / 1000, 2)
            if instance.ingredient.measurement_unit in ["kg", "l"]
            else instance.quantity
        )
        representation["quantity"] = quantity
        return representation


class CreateAvailableAtTheBranchSerializer(serializers.ModelSerializer):
    """
    CreateAvailableAtTheBranch serializer.
    """

    minimal_limit = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = AvailableAtTheBranch
        fields = ["id", "branch", "quantity", "minimal_limit"]

    def create(self, validated_data):
        """
        Create available at the branch.
        """
        available_at_the_branch = AvailableAtTheBranch.objects.create(**validated_data)
        MinimalLimitReached.objects.create(
            branch=available_at_the_branch.branch,
            ingredient=available_at_the_branch.ingredient,
            quantity=validated_data["quantity"],
        )
        return available_at_the_branch


class CreateIngredientSerializer(serializers.ModelSerializer):
    """
    Create Ingredient serializer.
    """

    available_at_branches = CreateAvailableAtTheBranchSerializer(
        many=True, write_only=True
    )

    class Meta:
        model = Ingredient
        fields = [
            "id",
            "name",
            "measurement_unit",
            "available_at_branches",
        ]

    def create(self, validated_data):
        """
        Create ingredient.
        """
        available_at_branches_data = validated_data.pop("available_at_branches", [])
        ingredient = Ingredient.objects.create(**validated_data)
        for available_at_branch_data in available_at_branches_data:
            branch = available_at_branch_data.pop("branch")
            minimal_limit = available_at_branch_data.pop("minimal_limit")
            quantity = available_at_branch_data["quantity"]
            if ingredient.measurement_unit in ["kg", "l"]:
                quantity *= 1000
            AvailableAtTheBranch.objects.create(
                ingredient=ingredient, branch=branch, quantity=quantity
            )
            MinimalLimitReached.objects.create(
                branch=branch, ingredient=ingredient, quantity=minimal_limit
            )
        return ingredient


class AvailableAtTheBranchForIngredientSerializer(serializers.ModelSerializer):
    """
    AvailableAtTheBranchForIngredient serializer for IngredientDetailSerializer with minimal limit.
    """

    branch = serializers.StringRelatedField()
    minimal_limit = serializers.SerializerMethodField()

    class Meta:
        model = AvailableAtTheBranch
        fields = ["id", "branch", "quantity", "minimal_limit"]

    def get_minimal_limit(self, obj):
        if MinimalLimitReached.objects.filter(
            branch=obj.branch, ingredient=obj.ingredient
        ).exists():
            return MinimalLimitReached.objects.get(
                branch=obj.branch, ingredient=obj.ingredient
            ).quantity
        else:
            return 0

    def to_representation(self, instance):
        """
        Change quantity to kg or l if measurement unit is kg or l.
        """
        representation = super().to_representation(instance)
        representation["branch"] = instance.branch.name_of_shop
        quantity = (
            round(instance.quantity / 1000, 2)
            if instance.ingredient.measurement_unit in ["kg", "l"]
            else instance.quantity
        )
        representation["quantity"] = quantity
        return representation


class IngredientSerializer(serializers.ModelSerializer):
    """
    Ingredient serializer.
    """

    available_at_branches = serializers.SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = [
            "id",
            "name",
            "measurement_unit",
            "date_of_arrival",
            "available_at_branches",
        ]

    def get_available_at_branches(self, obj):
        return AvailableAtTheBranchForIngredientSerializer(
            AvailableAtTheBranch.objects.filter(ingredient=obj), many=True
        ).data

    def to_representation(self, instance):
        """
        Change quantity to kg or l if measurement unit is kg or l.
        """
        representation = super().to_representation(instance)
        total_quantity = AvailableAtTheBranch.objects.filter(
            ingredient=instance
        ).aggregate(total_quantity=models.Sum("quantity"))["total_quantity"]
        if total_quantity is not None:
            representation["total_quantity"] = (
                round(total_quantity / 1000, 2)
                if instance.measurement_unit in ["kg", "l"]
                else total_quantity
            )
        else:
            representation["total_quantity"] = 0
        representation["date_of_arrival"] = instance.date_of_arrival.strftime(
            "%Y-%m-%d"
        )
        return representation


class UpdateIngredientSerializer(serializers.ModelSerializer):
    """
    UpdateIngredient serializer.
    """

    class Meta:
        model = Ingredient
        fields = [
            "id",
            "name",
            "measurement_unit",
        ]

    def update(self, instance, validated_data):
        if (
            "measurement_unit" in validated_data
            and validated_data["measurement_unit"] != instance.measurement_unit
        ):
            if AvailableAtTheBranch.objects.filter(ingredient=instance).exists():
                for available_at_the_branch in AvailableAtTheBranch.objects.filter(
                    ingredient=instance
                ):
                    if instance.measurement_unit in ["kg", "l"]:
                        available_at_the_branch.quantity *= 1000
                    available_at_the_branch.save()
        return super().update(instance, validated_data)


class IngredientDetailSerializer(serializers.ModelSerializer):
    """
    IngredientDetail serializer.
    """

    available_at_branches = serializers.SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = [
            "id",
            "name",
            "measurement_unit",
            "date_of_arrival",
            "available_at_branches",
        ]

    def get_available_at_branches(self, obj):
        return AvailableAtTheBranchForIngredientSerializer(
            AvailableAtTheBranch.objects.filter(ingredient=obj), many=True
        ).data

    def to_representation(self, instance):
        """
        Change quantity to kg or l if measurement unit is kg or l.
        """
        representation = super().to_representation(instance)
        total_quantity = AvailableAtTheBranch.objects.filter(
            ingredient=instance
        ).aggregate(total_quantity=models.Sum("quantity"))["total_quantity"]
        if total_quantity is not None:
            representation["total_quantity"] = (
                round(total_quantity / 1000, 2)
                if instance.measurement_unit in ["kg", "l"]
                else total_quantity
            )
        else:
            representation["total_quantity"] = 0
        representation["date_of_arrival"] = instance.date_of_arrival.strftime(
            "%Y-%m-%d"
        )
        return representation


class IngredientQuantityUpdateSerializer(serializers.ModelSerializer):
    """
    IngredientQuantityUpdate serializer.
    """

    class Meta:
        model = AvailableAtTheBranch
        fields = ["id", "quantity"]

    def update(self, instance, validated_data):
        """
        Update quantity.
        """
        quantity = validated_data.get("quantity", instance.quantity)
        if instance.ingredient.measurement_unit in ["kg", "l"]:
            quantity *= 1000
        instance.quantity = quantity
        instance.save()
        return instance

    def to_representation(self, instance):
        """
        Change quantity to kg or l if measurement unit is kg or l.
        """
        representation = super().to_representation(instance)
        representation["ingredient"] = instance.ingredient.name
        representation["branch"] = instance.branch.name_of_shop
        quantity = instance.quantity
        if isinstance(quantity, str):
            quantity = float(quantity)
        quantity = (
            round(quantity / 1000, 2)
            if instance.ingredient.measurement_unit in ["kg", "l"]
            else quantity
        )
        representation["quantity"] = quantity
        return representation


class LowStockIngredientSerializer(serializers.Serializer):
    """
    LowStockIngredient serializer.
    """
    name_of_shop = serializers.CharField()
    ingredient_name = serializers.CharField()
    quantity = serializers.DecimalField(max_digits=10, decimal_places=2)
    min_limit = serializers.DecimalField(max_digits=10, decimal_places=2)

# =====================================================================
# ITEM SERIALIZERS
# =====================================================================
class CompositionSerializer(serializers.ModelSerializer):
    """
    Composition serializer.
    """

    class Meta:
        model = Composition
        fields = ["id", "ingredient", "quantity"]


class CreateItemSerializer(serializers.ModelSerializer):
    """
    CreateItem serializer.
    """

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
        """
        Create item.
        """
        composition_data = validated_data.pop("composition", [])
        item = Item.objects.create(**validated_data)
        for composition in composition_data:
            Composition.objects.create(item=item, **composition)
        return item

    def to_representation(self, instance):
        """
        Change quantity to kg or l if measurement unit is kg or l.
        """
        representation = super().to_representation(instance)
        representation["composition"] = CompositionSerializer(
            Composition.objects.filter(item=instance), many=True
        ).data
        return representation


class ItemSerializer(serializers.ModelSerializer):
    """
    Item serializer.
    """

    category = CategorySerializer(read_only=True)
    compositions = CompositionSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = [
            "id",
            "name",
            "description",
            "price",
            "image",
            "compositions",
            "is_available",
            "category",
        ]


class UpdateItemSerializer(serializers.ModelSerializer):
    """
    UpdateItem serializer.
    """

    compositions = CompositionSerializer(many=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Item
        fields = [
            "id",
            "name",
            "description",
            "price",
            "image",
            "compositions",
            "is_available",
            "category_id",
        ]

    def update(self, instance, validated_data):
        """
        Update item.
        """
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.price = validated_data.get("price", instance.price)
        instance.image = validated_data.get("image", instance.image)
        instance.is_available = validated_data.get(
            "is_available", instance.is_available
        )
        instance.category = Category.objects.get(
            id=validated_data.get("category_id", instance.category.id)
        )
        instance.save()
        return instance


class PutImageToItemSerializer(serializers.ModelSerializer):
    """
    PutImageToItem serializer for ItemImageUpdateView
    """

    class Meta:
        model = Item
        fields = ["image"]


# =====================================================================
# READY MADE PRODUCT SERIALIZERS
# =====================================================================
class ReadyMadeProductAvailableAtTheBranchSerializer(serializers.ModelSerializer):
    """
    ReadyMadeProductAvailableAtTheBranch serializer.
    """

    ready_made_product = serializers.PrimaryKeyRelatedField(read_only=True)
    minimal_limit = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = ReadyMadeProductAvailableAtTheBranch
        fields = ["id", "branch", "ready_made_product", "quantity", "minimal_limit"]


class CreateReadyMadeProductSerializer(serializers.ModelSerializer):
    """
    CreateReadyMadeProduct serializer.
    """

    available_at_branches = ReadyMadeProductAvailableAtTheBranchSerializer(
        many=True, write_only=True
    )

    class Meta:
        model = ReadyMadeProduct
        fields = [
            "id",
            "name",
            "available_at_branches",
        ]

    def create(self, validated_data):
        """
        Create ready-made product and available at the branch.
        """
        available_at_branches_data = validated_data.pop("available_at_branches", [])
        product = ReadyMadeProduct.objects.create(**validated_data)
        ready_made_product_list = []
        minimal_limit_list = []
        for available_at_branch_data in available_at_branches_data:
            try:
                branch = available_at_branch_data.pop("branch")
                minimal_limit = available_at_branch_data.pop("minimal_limit")
                quantity = available_at_branch_data["quantity"]
            except KeyError:
                raise serializers.ValidationError(
                    "Branch, minimal_limit and quantity are required."
                )
            ready_made_product_list.append(
                ReadyMadeProductAvailableAtTheBranch(
                    ready_made_product=product, branch=branch, quantity=quantity
                )
            )
            minimal_limit_list.append(
                MinimalLimitReached(
                    branch=branch, ready_made_product=product, quantity=minimal_limit
                )
            )
        with transaction.atomic():
            ReadyMadeProductAvailableAtTheBranch.objects.bulk_create(
                ready_made_product_list
            )
            MinimalLimitReached.objects.bulk_create(minimal_limit_list)
        return product


class ReadyMadeProductSerializer(serializers.ModelSerializer):
    """
    ReadyMadeProduct serializer.
    """

    available_at_branches = ReadyMadeProductAvailableAtTheBranchSerializer(
        source="minimal_limit_reached", many=True, read_only=True
    )

    class Meta:
        model = ReadyMadeProduct
        fields = [
            "id",
            "name",
            "date_of_arrival",
            "available_at_branches",
        ]

    def to_representation(self, instance):
        """
        Create ready-made product and available at the branch representation.
        """
        representation = super().to_representation(instance)
        representation["total_quantity"] = (
            ReadyMadeProductAvailableAtTheBranch.objects.filter(
                ready_made_product=instance
            ).aggregate(total_quantity=models.Sum("quantity"))["total_quantity"]
            or 0
        )
        representation["date_of_arrival"] = instance.date_of_arrival.strftime(
            "%Y-%m-%d"
        )
        return representation


class UpdateReadyMadeProductSerializer(serializers.ModelSerializer):
    """
    EditReadyMadeProduct serializer.
    """

    class Meta:
        model = ReadyMadeProduct
        fields = [
            "id",
            "name",
        ]

import json

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.accounts.models import CustomUser as User
from apps.accounts.models import EmployeeSchedule, EmployeeWorkdays
from apps.branches.models import Branch, Schedule, Workdays
from apps.storage.models import (AvailableAtTheBranch, Category, Ingredient,
                                 Item, ReadyMadeProduct,
                                 MinimalLimitReached,)


# ==================== Category Tests ==================== #
# Category Model Tests
class CategoryModelTest(TestCase):
    """Test Category model"""

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Category.objects.create(name="Test Category")

    def test_name_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field("name").verbose_name
        self.assertEquals(field_label, "name")

    def test_name_max_length(self):
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field("name").max_length
        self.assertEquals(max_length, 255)

    def test_object_name_is_name(self):
        category = Category.objects.get(id=1)
        expected_object_name = category.name
        self.assertEquals(expected_object_name, str(category))


# Category View Tests
class CategoryViewTest(TestCase):
    """Test Category endpoints"""

    @classmethod
    def setUpTestData(cls):
        # Common test data for all methods
        cls.user = User.objects.create(
            first_name="test",
            last_name="user",
            phone_number="+996700000000",
            username="testuser",
            password="testpassword",
            is_active=True,
        )
        cls.admin_user = User.objects.create(
            first_name="test",
            last_name="admin",
            phone_number="+996700000001",
            username="testadmin",
            password="testpassword",
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )
        cls.category = Category.objects.create(name="test category")

    def setUp(self):
        self.client = APIClient()

    def get_token(self, phone_number):
        response = self.client.post(
            path="/accounts/temporary-login/",
            data={"phone_number": phone_number},
        )
        return response.data["access"]

    def test_user_category_list(self):
        """Test getting category list by usual user"""
        token = self.get_token("+996700000000")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.get(path="/admin-panel/categories/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_category_list(self):
        """Test getting category list by admin user"""
        token = self.get_token("+996700000001")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.get(path="/admin-panel/categories/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_user_category_update(self):
        """Test updating category by usual user"""
        token = self.get_token("+996700000000")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.put(
            path=f"/admin-panel/categories/update/{self.category.id}/",
            data={"name": "new category"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            Category.objects.get(id=self.category.id).name, "test category"
        )

    def test_admin_category_update(self):
        """Test updating category by admin user"""
        token = self.get_token("+996700000001")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

    def test_user_category_creation(self):
        """Test creating category by usual user"""
        token = self.get_token("+996700000000")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.post(
            path="/admin-panel/categories/create/",
            data={"name": "new category"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Category.objects.count(), 1)

    def test_admin_category_creation(self):
        """Test creating category by admin user"""
        token = self.get_token("+996700000001")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.post(
            path="/admin-panel/categories/create/",
            data={"name": "another category"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)
        self.assertTrue(Category.objects.filter(name="another category").exists())

    def test_user_category_deletion(self):
        """Test deleting category by usual user"""
        token = self.get_token("+996700000000")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.delete(
            path=f"/admin-panel/categories/destroy/{self.category.id}/",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Category.objects.filter(id=self.category.id).exists())

    def test_admin_category_deletion(self):
        """Test deleting category by admin user"""
        token = self.get_token("+996700000001")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.delete(
            path=f"/admin-panel/categories/destroy/{self.category.id}/",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Category.objects.filter(id=self.category.id).exists())

    def test_admin_category_update(self):
        """Test updating category by admin user"""
        token = self.get_token("+996700000001")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.put(
            path=f"/admin-panel/categories/update/{self.category.id}/",
            data={"name": "new category"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Category.objects.get(id=self.category.id).name, "new category")


# ==================== Employee Tests ==================== #
# Employee Model Tests
class EmployeeModelTest(TestCase):
    """Test Employee model"""

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = User.objects.create(
            first_name="test",
            last_name="user",
            phone_number="+996700000000",
            username="testuser",
            password="testpassword",
            is_active=True,
        )
        cls.branch_schedule = Schedule.objects.create(title="Test Schedule")
        cls.branch = Branch.objects.create(
            schedule=cls.branch_schedule,
            name_of_shop="Test Branch",
            address="Test Address",
            phone_number="+996700000000",
            link_to_map="https://test.link",
        )
        cls.employee_schedule = EmployeeSchedule.objects.create(title="Test Schedule")
        cls.employee = User.objects.create(
            first_name="test",
            last_name="employee",
            phone_number="+996700000002",
            username="testemployee",
            password="testpassword",
            position="barista",
            is_active=True,
            branch=cls.branch,
            schedule=cls.employee_schedule,
        )

    def test_first_name_label(self):
        employee = User.objects.get(id=2)
        field_label = employee._meta.get_field("first_name").verbose_name
        self.assertEquals(field_label, "first name")

    def test_first_name_max_length(self):
        employee = User.objects.get(id=2)
        max_length = employee._meta.get_field("first_name").max_length
        self.assertEquals(max_length, 255)

    def test_last_name_label(self):
        employee = User.objects.get(id=2)
        field_label = employee._meta.get_field("last_name").verbose_name
        self.assertEquals(field_label, "last name")

    def test_last_name_max_length(self):
        employee = User.objects.get(id=2)
        max_length = employee._meta.get_field("last_name").max_length
        self.assertEquals(max_length, 255)

    def test_birth_date_label(self):
        employee = User.objects.get(id=2)
        field_label = employee._meta.get_field("birth_date").verbose_name
        self.assertEquals(field_label, "birth date")

    def test_birth_date_null(self):
        employee = User.objects.get(id=2)
        null = employee._meta.get_field("birth_date").null
        self.assertTrue(null)

    def test_birth_date_blank(self):
        employee = User.objects.get(id=2)
        blank = employee._meta.get_field("birth_date").blank
        self.assertTrue(blank)


# Employee View Tests
class EmployeeViewTest(TestCase):
    """Test Employee endpoints"""

    @classmethod
    def setUpTestData(cls):
        # Common test data for all methods
        cls.user = User.objects.create(
            first_name="test",
            last_name="user",
            phone_number="+996700000000",
            username="testuser",
            password="testpassword",
            is_active=True,
        )
        cls.admin_user = User.objects.create(
            first_name="test",
            last_name="admin",
            phone_number="+996700000001",
            username="testadmin",
            password="testpassword",
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )
        cls.branch_schedule = Schedule.objects.create(title="Test Schedule")
        cls.branch = Branch.objects.create(
            schedule=cls.branch_schedule,
            name_of_shop="Test Branch",
            address="Test Address",
            phone_number="+996700000000",
            link_to_map="https://test.link",
        )
        cls.employee_schedule = EmployeeSchedule.objects.create(title="Test Schedule")
        cls.employee = User.objects.create(
            first_name="test",
            last_name="employee",
            phone_number="+996700000002",
            username="testemployee",
            password="testpassword",
            position="barista",
            is_active=True,
            branch=cls.branch,
            schedule=cls.employee_schedule,
        )

    def setUp(self):
        self.client = APIClient()

    def get_token(self, phone_number):
        response = self.client.post(
            path="/accounts/temporary-login/",
            data={"phone_number": phone_number},
        )
        return response.data["access"]

    def test_create_employee_by_user(self):
        """Test creating employee by usual user"""
        token = self.get_token("+996700000000")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.post(
            path="/admin-panel/employees/create/",
            data={
                "first_name": "new",
                "last_name": "employee",
                "phone_number": "+996700000003",
                "username": "newemployee",
                "password": "testpassword",
                "position": "barista",
                "branch": self.branch.id,
                "schedule": self.employee_schedule.id,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(User.objects.count(), 3)

    def test_create_employee_by_admin(self):
        """Test creating employee by admin user"""
        token = self.get_token("+996700000001")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        data = {
            "username": "alexandrovolta",
            "password": "testpassword",
            "first_name": "Alexandro",
            "position": "waiter",
            "birth_date": "2007-01-01",
            "phone_number": "+996700000003",
            "branch": 1,
            "workdays": [
                {"workday": 1, "start_time": "09:00", "end_time": "17:00"},
                {"workday": 2, "start_time": "09:00", "end_time": "17:00"},
                {"workday": 3, "start_time": "09:00", "end_time": "17:00"},
                {"workday": 4, "start_time": "09:00", "end_time": "17:00"},
                {"workday": 5, "start_time": "09:00", "end_time": "17:00"},
            ],
        }
        response = self.client.post(
            path="/admin-panel/employees/create/",
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 4)
        self.assertTrue(User.objects.filter(username="alexandrovolta").exists())
        self.assertEqual(
            EmployeeSchedule.objects.filter(title="Alexandro's schedule").count(), 1
        )
        self.assertEqual(
            EmployeeWorkdays.objects.filter(
                schedule__title="Alexandro's schedule"
            ).count(),
            5,
        )

    def test_update_employee_by_user(self):
        """Test updating employee by usual user"""
        token = self.get_token("+996700000000")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.put(
            path=f"/admin-panel/employees/update/{self.employee.id}/",
            data={
                "first_name": "new",
                "last_name": "employee",
                "phone_number": "+996700000003",
                "username": "newemployee",
                "password": "testpassword",
                "position": "barista",
                "branch": self.branch.id,
                "schedule": self.employee_schedule.id,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(User.objects.get(id=self.employee.id).first_name, "test")

    def test_update_employee_by_admin(self):
        """Test updating employee by admin user"""
        token = self.get_token("+996700000001")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.put(
            path=f"/admin-panel/employees/update/{self.employee.id}/",
            data={
                "first_name": "new",
                "last_name": "employee",
                "phone_number": "+996700000003",
                "username": "newemployee",
                "password": "testpassword",
                "position": "barista",
                "branch": self.branch.id,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(id=self.employee.id).first_name, "new")

    def test_delete_employee_by_user(self):
        """Test deleting employee by usual user"""
        token = self.get_token("+996700000000")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.delete(
            path=f"/admin-panel/employees/destroy/{self.employee.id}/",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(User.objects.filter(id=self.employee.id).exists())

    def test_get_employee_list_by_user(self):
        """Test getting employee list by usual user"""
        token = self.get_token("+996700000000")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.get(path="/admin-panel/employees/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_employee_list_by_admin(self):
        """Test getting employee list by admin user"""
        token = self.get_token("+996700000001")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.get(path="/admin-panel/employees/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_delete_employee_by_admin(self):
        """Test deleting employee by admin user"""
        token = self.get_token("+996700000001")
        employee_name = self.employee.first_name
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.delete(
            path=f"/admin-panel/employees/destroy/{self.employee.id}/",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(User.objects.filter(id=self.employee.id).exists())
        self.assertFalse(
            EmployeeSchedule.objects.filter(
                title=f"{employee_name}'s schedule"
            ).exists()
        )

    def test_get_employee_by_user(self):
        """Test getting employee by usual user"""
        token = self.get_token("+996700000000")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.get(path=f"/admin-panel/employees/{self.employee.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_employee_by_admin(self):
        """Test getting employee by admin user"""
        token = self.get_token("+996700000001")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.get(path=f"/admin-panel/employees/{self.employee.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "test")

    def test_update_employee_schedule_by_user(self):
        """Test updating employee schedule by usual user"""
        token = self.get_token("+996700000000")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        data = {
            "title": "new schedule",
            "workdays": [
                {"workday": 1, "start_time": "09:00", "end_time": "17:00"},
                {"workday": 2, "start_time": "09:00", "end_time": "17:00"},
                {"workday": 3, "start_time": "09:00", "end_time": "17:00"},
                {"workday": 4, "start_time": "09:00", "end_time": "17:00"},
                {"workday": 5, "start_time": "09:00", "end_time": "17:00"},
            ],
        }
        response = self.client.put(
            path=f"/admin-panel/employees/schedule/update/{self.employee.id}/",
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(EmployeeSchedule.objects.filter(title="new schedule").exists())
        self.assertEqual(
            EmployeeWorkdays.objects.filter(schedule__title="new schedule").count(), 0
        )

    def test_update_employee_schedule_by_admin(self):
        """Test updating employee schedule by admin user"""
        token = self.get_token("+996700000001")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        data = {
            "workdays": [
                {"workday": 1, "start_time": "09:00", "end_time": "17:00"},
                {"workday": 2, "start_time": "09:00", "end_time": "17:00"},
                {"workday": 3, "start_time": "09:00", "end_time": "17:00"},
                {"workday": 4, "start_time": "09:00", "end_time": "17:00"},
                {"workday": 5, "start_time": "09:00", "end_time": "17:00"},
            ]
        }
        response = self.client.put(
            path=f"/admin-panel/employees/schedule/update/{self.employee.id}/",
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            EmployeeSchedule.objects.filter(title="test's schedule").exists()
        )
        self.assertEqual(
            EmployeeWorkdays.objects.filter(schedule__title="test's schedule").count(),
            5,
        )

    def test_delete_employee_by_user(self):
        """Test deleting employee by usual user"""
        token = self.get_token("+996700000000")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.delete(
            path=f"/admin-panel/employees/destroy/{self.employee.id}/",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(User.objects.filter(id=self.employee.id).exists())

    def test_delete_employee_by_admin(self):
        """Test deleting employee by admin user"""
        token = self.get_token("+996700000001")
        employee_name = self.employee.first_name
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.delete(
            path=f"/admin-panel/employees/destroy/{self.employee.id}/",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(User.objects.filter(id=self.employee.id).exists())
        self.assertFalse(
            EmployeeSchedule.objects.filter(
                title=f"{employee_name}'s schedule"
            ).exists()
        )


# ==================== Ingredient Tests ==================== #
# Ingredient Model Tests
class IngredientModelTest(TestCase):
    """Test Ingredient model"""

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.ingredient = Ingredient.objects.create(
            name="Test Ingredient", measurement_unit="g"
        )
        cls.branch_schedule = Schedule.objects.create(title="Test Schedule")
        cls.branch = Branch.objects.create(
            schedule=cls.branch_schedule,
            name_of_shop="Test Branch",
            address="Test Address",
            phone_number="+996700000000",
            link_to_map="https://test.link",
        )
        cls.minimal_limit = MinimalLimitReached.objects.create(
            branch=cls.branch, ingredient=cls.ingredient, quantity=100
        )

    def test_name_label(self):
        ingredient = Ingredient.objects.get(id=1)
        field_label = ingredient._meta.get_field("name").verbose_name
        self.assertEquals(field_label, "name")

    def test_name_max_length(self):
        ingredient = Ingredient.objects.get(id=1)
        max_length = ingredient._meta.get_field("name").max_length
        self.assertEquals(max_length, 255)

    def test_object_name_is_name(self):
        ingredient = Ingredient.objects.get(id=1)
        expected_object_name = ingredient.name
        self.assertEquals(expected_object_name, str(ingredient))

    def test_measurement_unit_label(self):
        ingredient = Ingredient.objects.get(id=1)
        field_label = ingredient._meta.get_field("measurement_unit").verbose_name
        self.assertEquals(field_label, "measurement unit")

    def test_minimal_limit(self):
        minimal_limit = MinimalLimitReached.objects.get(id=1)
        self.assertEquals(minimal_limit.quantity, 100)


# Ingredient View Tests
class IngredientViewTest(TestCase):
    """Test Ingredient endpoints"""

    @classmethod
    def setUpTestData(cls):
        # Common test data for all methods
        cls.user = User.objects.create(
            first_name="test",
            last_name="user",
            phone_number="+996700000000",
            username="testuser",
            password="testpassword",
            is_active=True,
        )
        cls.admin_user = User.objects.create(
            first_name="test",
            last_name="admin",
            phone_number="+996700000001",
            username="testadmin",
            password="testpassword",
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )
        cls.schedule = Schedule.objects.create(title="Test Schedule")
        cls.branch = Branch.objects.create(
            schedule=cls.schedule,
            name_of_shop="Test Branch",
            address="Test Address",
            phone_number="+996700000000",
            link_to_map="https://test.link",
        )
        cls.ingredient = Ingredient.objects.create(
            name="Test Ingredient", measurement_unit="g"
        )
        cls.available_at_the_branch = AvailableAtTheBranch.objects.create(
            branch=cls.branch, ingredient=cls.ingredient, quantity=100000
        )
        cls.minimal_limit = MinimalLimitReached.objects.create(
            branch=cls.branch, ingredient=cls.ingredient, quantity=100
        )

    def setUp(self):
        self.client = APIClient()

    def get_token(self, phone_number):
        response = self.client.post(
            path="/accounts/temporary-login/",
            data={"phone_number": phone_number},
        )
        return response.data["access"]

    def test_create_ingredient_by_user(self):
        """Test creating ingredient by usual user"""
        token = self.get_token("+996700000000")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.post(
            path="/admin-panel/ingredients/",
            data={
                "name": "New Ingredient",
                "measurement_unit": "g",
                "available_at_branches": [
                    {"branch": self.branch.id, "quantity": 100000, "minimal_limit": 100}
                ],
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_ingredient_by_admin(self):
        """Test creating ingredient by admin user"""
        token = self.get_token("+996700000001")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.post(
            path="/admin-panel/ingredients/",
            data={
                "name": "New Ingredient",
                "measurement_unit": "g",
                "available_at_branches": [
                    {"branch": self.branch.id, "quantity": 100000, "minimal_limit": 100}
                ],
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "New Ingredient")
        self.assertEqual(response.data["measurement_unit"], "g")
        self.assertEqual(response.data["available_at_branches"][0]["quantity"], 100000)
        self.assertEqual(response.data["available_at_branches"][0]["minimal_limit"], 100)

    def test_create_ingredient_by_user(self):
        """Test creating ingredient by usual user"""
        token = self.get_token("+996700000000")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.post(
            path="/admin-panel/ingredients/",
            data={
                "name": "New Ingredient",
                "measurement_unit": "g",
                "available_at_branches": [
                    {"branch": self.branch.id, "quantity": 100000, "minimal_limit": 100}
                ],
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_ingredient_by_admin(self):
        """Test creating ingredient by admin user"""
        token = self.get_token("+996700000001")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        data = {
            "name": "New Ingredient",
            "measurement_unit": "g",
            "available_at_branches": [
                {"branch": f"{self.branch.id}", "quantity": "100000", "minimal_limit": "100"}
            ],
        }
        response = self.client.post(
            path="/admin-panel/ingredients/create/",
            data=json.dumps(data),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            Ingredient.objects.filter(name="New Ingredient").count(), 1
        )
        self.assertEqual(
            AvailableAtTheBranch.objects.filter(
                ingredient__name="New Ingredient"
            ).count(),
            1,
        )
        self.assertEqual(
            MinimalLimitReached.objects.filter(
                ingredient__name="New Ingredient"
            ).count(),
            1,
        )

    def test_create_ingredient_by_admin_with_existing_name(self):
        """Test creating ingredient by admin user with existing name"""
        token = self.get_token("+996700000001")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.post(
            path="/admin-panel/ingredients/create/",
            data={
                "name": "Test Ingredient",
                "measurement_unit": "g",
                "available_at_branches": [
                    {"branch": self.branch.id, "quantity": 100000, "minimal_limit": 100}
                ],
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_ingredient_by_user(self):
        """Test updating ingredient by usual user"""
        token = self.get_token("+996700000000")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.put(
            path=f"/admin-panel/ingredients/{self.ingredient.id}/",
            data={
                "name": "Updated Ingredient",
                "measurement_unit": "kg",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_ingredient_by_admin(self):
        """Test updating ingredient by admin user"""
        token = self.get_token("+996700000001")
        ingredient_name = self.ingredient.name
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.put(
            path=f"/admin-panel/ingredients/update/{self.ingredient.id}/",
            data={
                "name": "Updated Ingredient",
                "measurement_unit": "kg",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(MinimalLimitReached.objects.filter(ingredient=self.ingredient, branch=self.branch).exists())

    def test_delete_ingredient_by_user(self):
        """Test deleting ingredient by usual user"""
        token = self.get_token("+996700000000")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.delete(path=f"/admin-panel/ingredients/{self.ingredient.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Ingredient.objects.filter(id=self.ingredient.id).exists())
        self.assertTrue(MinimalLimitReached.objects.filter(ingredient=self.ingredient, branch=self.branch).exists())

    def test_delete_ingredient_by_admin(self):
        """Test deleting ingredient by admin user"""
        token = self.get_token("+996700000001")
        ingredient_name = self.ingredient.name
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.delete(path=f"/admin-panel/ingredients/destroy/{self.ingredient.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Ingredient.objects.filter(id=self.ingredient.id).exists())
        self.assertFalse(
            AvailableAtTheBranch.objects.filter(
                ingredient__name=ingredient_name
            ).exists()
        )
        self.assertFalse(MinimalLimitReached.objects.filter(ingredient=self.ingredient, branch=self.branch).exists())
        self.assertEqual(
            MinimalLimitReached.objects.filter(branch=self.branch).count(), 0
        )

    def test_get_ingredient_by_user(self):
        """Test getting ingredient by usual user"""
        token = self.get_token("+996700000000")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.get(
            path=f"/admin-panel/ingredients/{self.ingredient.id}/",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_ingredient_by_admin(self):
        """Test getting ingredient by admin user"""
        token = self.get_token("+996700000001")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.get(
            path=f"/admin-panel/ingredients/{self.ingredient.id}/",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Ingredient")
        self.assertEqual(response.data["measurement_unit"], "g")
        self.assertEqual(response.data["available_at_branches"][0]["quantity"], 100000)
        self.assertEqual(response.data["available_at_branches"][0]["minimal_limit"], 100)

    def test_update_ingredient_quantity_by_user(self):
        """Test updating ingredient quantity by usual user"""
        token = self.get_token("+996700000000")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        data = {"quantity": 100}
        response = self.client.put(
            path=f"/admin-panel/ingredient-quantity-update/{self.ingredient.id}/",
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            AvailableAtTheBranch.objects.filter(
                ingredient__name="Test Ingredient", branch__id=1
            )
            .first()
            .quantity,
            100000,
        )
        self.assertEqual(
            MinimalLimitReached.objects.get(ingredient=self.ingredient, branch=self.branch).quantity,
            100,
        )

    def test_update_ingredient_quantity_by_admin(self):
        """Test updating ingredient quantity by admin user"""
        token = self.get_token("+996700000001")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        data = {"quantity": 100}
        response = self.client.put(
            path=f"/admin-panel/ingredient-quantity-update/{self.ingredient.id}/",
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            AvailableAtTheBranch.objects.filter(
                ingredient__name="Test Ingredient", branch__id=1
            )
            .first()
            .quantity,
            100,
        )
        self.assertEqual(
            MinimalLimitReached.objects.get(ingredient=self.ingredient, branch=self.branch).quantity,
            100,
        )

    def test_delete_ingredient_from_branch_by_user(self):
        """Test deleting ingredient from branch by usual user"""
        token = self.get_token("+996700000000")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.delete(
            path=f"/admin-panel/ingredients/destroy/{self.ingredient.id}/",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Ingredient.objects.filter(id=self.ingredient.id).exists())
        self.assertTrue(MinimalLimitReached.objects.filter(ingredient=self.ingredient, branch=self.branch).exists())

    def test_delete_ingredient_from_branch_by_admin(self):
        """Test deleting ingredient from branch by admin user"""
        token = self.get_token("+996700000001")
        ingredient_name = self.ingredient.name
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.delete(
            path=f"/admin-panel/ingredients/destroy/{self.ingredient.id}/",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Ingredient.objects.filter(id=self.ingredient.id).exists())
        self.assertFalse(
            AvailableAtTheBranch.objects.filter(
                ingredient__name=ingredient_name
            ).exists()
        )
        self.assertFalse(MinimalLimitReached.objects.filter(ingredient=self.ingredient, branch=self.branch).exists())


# ==================== Item Tests ==================== #
class ItemModelTest(TestCase):
    """Test Item model"""

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.category = Category.objects.create(name="Test Category")
        cls.item = Item.objects.create(
            name="Test Item",
            category=cls.category,
            price=100,
            description="Test Description",
        )

    def test_name_label(self):
        item = Item.objects.get(id=1)
        field_label = item._meta.get_field("name").verbose_name
        self.assertEquals(field_label, "name")

    def test_name_max_length(self):
        item = Item.objects.get(id=1)
        max_length = item._meta.get_field("name").max_length
        self.assertEquals(max_length, 255)

    def test_object_name_is_name(self):
        item = Item.objects.get(id=1)
        expected_object_name = item.name
        self.assertEquals(expected_object_name, str(item))

    def test_price_label(self):
        item = Item.objects.get(id=1)
        field_label = item._meta.get_field("price").verbose_name
        self.assertEquals(field_label, "price")

    def test_price_max_digits(self):
        item = Item.objects.get(id=1)
        max_digits = item._meta.get_field("price").max_digits
        self.assertEquals(max_digits, 10)


class ItemViewTest(TestCase):
    """Test Item endpoints"""

    @classmethod
    def setUpTestData(cls):
        # Common test data for all methods
        cls.admin_user = User.objects.create(
            first_name="test",
            last_name="admin",
            phone_number="+996700000001",
            username="testadmin",
            password="testpassword",
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )
        cls.category = Category.objects.create(name="Test Category")
        cls.item = Item.objects.create(
            name="Test Item",
            category=cls.category,
            price=100,
            description="Test Description",
        )
        cls.ingredient = Ingredient.objects.create(
            name="Test Ingredient", measurement_unit="g"
        )
        cls.ingredient2 = Ingredient.objects.create(
            name="Test Ingredient 2", measurement_unit="g"
        )

    def setUp(self):
        self.client = APIClient()

    def get_token(self, phone_number):
        response = self.client.post(
            path="/accounts/temporary-login/",
            data={"phone_number": phone_number},
        )
        return response.data["access"]

    def test_delete_item(self):
        """Test deleting item by admin user"""
        token = self.get_token("+996700000001")
        item_name = self.item.name
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.delete(
            path=f"/admin-panel/items/destroy/{self.item.id}/",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Item.objects.filter(id=self.item.id).exists())

    def test_get_item_list(self):
        """Test getting item list by admin user"""
        token = self.get_token("+996700000001")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.get(path="/admin-panel/items/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_item(self):
        """Test creating item by admin user"""
        token = self.get_token("+996700000001")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        data = {
            "category": "1",
            "name": "new item",
            "description": "Test Description",
            "price": 100,
            "is_available": True,
            "composition": [
                {"ingredient": "1", "quantity": 100},
                {"ingredient": "2", "quantity": 100},
            ],
        }
        response = self.client.post(
            path="/admin-panel/items/create/",
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 2)
        self.assertTrue(Item.objects.filter(name="new item").exists())
        self.assertEqual(
            Item.objects.filter(name="new item").first().compositions.count(), 2
        )

    def test_update_item(self):
        """Test updating item by admin user"""
        token = self.get_token("+996700000001")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        data = {
            "category_id": "1",
            "name": "new item",
            "description": "Test Description",
            "price": 100,
            "is_available": True,
            "compositions": [
                {"ingredient": "1", "quantity": 100},
                {"ingredient": "2", "quantity": 100},
            ],
        }
        response = self.client.put(
            path=f"/admin-panel/items/update/{self.item.id}/",
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Item.objects.filter(name="new item").count(), 1)

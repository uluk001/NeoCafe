import json

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.accounts.models import CustomUser as User
from apps.accounts.models import EmployeeSchedule, EmployeeWorkdays
from apps.branches.models import Branch, Schedule, Workdays
from apps.storage.models import (AvailableAtTheBranch, Category, Ingredient,
                                 Item, ReadyMadeProduct)

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
            name="Test Ingredient", measurement_unit="g", minimal_limit=100
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
        cls.ingredient = Ingredient.objects.create(
            name="Test Ingredient", measurement_unit="g", minimal_limit=100
        )
        cls.branch_schedule = Schedule.objects.create(title="Test Schedule")
        cls.branch = Branch.objects.create(
            schedule=cls.branch_schedule,
            name_of_shop="Test Branch",
            address="Test Address",
            phone_number="+996700000000",
            link_to_map="https://test.link",
        )
        cls.branch2 = Branch.objects.create(
            schedule=cls.branch_schedule,
            name_of_shop="Test Branch 2",
            address="Test Address 2",
            phone_number="+996700000000",
            link_to_map="https://test.link",
        )
        cls.available_at_the_branch = AvailableAtTheBranch.objects.create(
            ingredient=cls.ingredient, branch=cls.branch, quantity=100000
        )
        cls.available_at_the_branch2 = AvailableAtTheBranch.objects.create(
            ingredient=cls.ingredient, branch=cls.branch2, quantity=100000
        )

    def setUp(self):
        self.client = APIClient()

    def get_token(self, phone_number):
        response = self.client.post(
            path="/accounts/temporary-login/",
            data={"phone_number": phone_number},
        )
        return response.data["access"]

    def test_get_ingredient_list_by_user(self):
        """Test getting ingredient list by usual user"""
        token = self.get_token("+996700000000")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.get(path="/admin-panel/ingredients/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_ingredient_list_by_admin(self):
        """Test getting ingredient list by admin user"""
        token = self.get_token("+996700000001")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.get(path="/admin-panel/ingredients/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_ingredient_by_user(self):
        """Test creating ingredient by usual user"""
        token = self.get_token("+996700000000")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        data = {
            "name": "new ingredient",
            "measurement_unit": "kg",
            "minimal_limit": 100,
            "available_at_the_branch": [
                {"branch": 1, "quantity": 100},
                {"branch": 2, "quantity": 100},
            ],
        }
        response = self.client.post(
            path="/admin-panel/ingredients/create/",
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Ingredient.objects.count(), 1)

    def test_create_ingredient_by_admin(self):
        """Test creating ingredient by admin user"""
        token = self.get_token("+996700000001")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        data = {
            "name": "new ingredient",
            "measurement_unit": "kg",
            "minimal_limit": 100,
            "available_at_branches": [
                {"branch": 1, "quantity": 100},
                {"branch": 2, "quantity": 100},
            ],
        }
        response = self.client.post(
            path="/admin-panel/ingredients/create/",
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ingredient.objects.count(), 2)
        self.assertTrue(Ingredient.objects.filter(name="new ingredient").exists())
        self.assertEqual(
            AvailableAtTheBranch.objects.filter(
                ingredient__name="new ingredient"
            ).count(),
            2,
        )
        self.assertEqual(
            AvailableAtTheBranch.objects.filter(
                ingredient__name="new ingredient", branch__id=1
            )
            .first()
            .quantity,
            100000,
        )

    def test_update_ingredient_by_user(self):
        """Test updating ingredient by usual user"""
        token = self.get_token("+996700000000")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        data = {
            "name": "new ingredient",
            "measurement_unit": "kg",
            "minimal_limit": 100,
        }
        response = self.client.put(
            path=f"/admin-panel/ingredients/update/{self.ingredient.id}/",
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            Ingredient.objects.get(id=self.ingredient.id).name, "Test Ingredient"
        )

    def test_update_ingredient_by_admin(self):
        """Test updating ingredient by admin user"""
        token = self.get_token("+996700000001")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        data = {
            "name": "new ingredient",
            "measurement_unit": "kg",
            "minimal_limit": 100,
        }
        response = self.client.put(
            path=f"/admin-panel/ingredients/update/{self.ingredient.id}/",
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Ingredient.objects.get(id=self.ingredient.id).name, "new ingredient"
        )

    def test_delete_ingredient_by_user(self):
        """Test deleting ingredient by usual user"""
        token = self.get_token("+996700000000")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.delete(
            path=f"/admin-panel/ingredients/destroy/{self.ingredient.id}/",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Ingredient.objects.filter(id=self.ingredient.id).exists())

    def test_delete_ingredient_by_admin(self):
        """Test deleting ingredient by admin user"""
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

    def test_delete_ingredient_from_branch_by_user(self):
        """Test deleting ingredient from branch by usual user"""
        token = self.get_token("+996700000000")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.delete(
            path=f"/admin-panel/ingredients/destroy/{self.ingredient.id}/",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Ingredient.objects.filter(id=self.ingredient.id).exists())

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

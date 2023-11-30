"""
Module for testing branches app.
"""
import json

from django.test import TestCase
from apps.branches.models import Branch, Schedule, Workdays
from apps.accounts.models import CustomUser as User
from rest_framework import status
from rest_framework.test import APIClient

# ==================== Branch Test ==================== #
# Branch Model Test
class BranchTestCase(TestCase):
    """
    Class for testing branches app.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Create test data.
        """
        cls.schedule = Schedule.objects.create(
            title="Test title", description="Test description"
        )
        cls.branch = Branch.objects.create(
            image="Test image",
            name_of_shop="Test name",
            schedule=cls.schedule,
            address="Test address",
            phone_number="Test phone",
            link_to_map="Test link",
        )
        cls.workdays = Workdays.objects.create(
            schedule=cls.schedule, workday=1, start_time="10:00", end_time="20:00"
        )

    def test_branch(self):
        """
        Test branch model.
        """
        self.assertEqual(self.branch.image, "Test image")
        self.assertEqual(self.branch.name_of_shop, "Test name")
        self.assertEqual(self.branch.schedule.title, "Test title")
        self.assertEqual(self.branch.schedule.description, "Test description")
        self.assertEqual(self.branch.address, "Test address")
        self.assertEqual(self.branch.phone_number, "Test phone")
        self.assertEqual(self.branch.link_to_map, "Test link")

    def test_schedule(self):
        """
        Test schedule model.
        """
        self.assertEqual(self.schedule.title, "Test title")
        self.assertEqual(self.schedule.description, "Test description")

    def test_workdays(self):
        """
        Test workdays model.
        """
        self.assertEqual(self.workdays.schedule, self.schedule)
        self.assertEqual(self.workdays.workday, 1)
        self.assertEqual(self.workdays.start_time, "10:00")
        self.assertEqual(self.workdays.end_time, "20:00")


# Branch View Test
class BranchViewTestCase(TestCase):
    """
    Class for testing branches app views.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Create test data.
        """
        cls.schedule = Schedule.objects.create(
            title="Test title", description="Test description"
        )
        cls.branch = Branch.objects.create(
            image="Test image",
            name_of_shop="Test name",
            schedule=cls.schedule,
            address="Test address",
            phone_number="Test phone",
            link_to_map="Test link",
        )
        cls.workdays = Workdays.objects.create(
            schedule=cls.schedule, workday=1, start_time="10:00", end_time="20:00"
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

    def setUp(self):
        """
        Set up method for testing.
        """
        self.client = APIClient()

    def test_get_branches(self):
        """
        Test get branches.
        """
        response = self.client.get("/branches/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name_of_shop"], "Test name")
        self.assertEqual(response.data[0]["address"], "Test address")
        self.assertEqual(response.data[0]["phone_number"], "Test phone")

    def test_get_branch(self):
        """
        Test get branch.
        """
        response = self.client.get("/branches/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name_of_shop"], "Test name")
        self.assertEqual(response.data["address"], "Test address")
        self.assertEqual(response.data["phone_number"], "Test phone")

    def test_create_branch(self):
        """
        Test create branch.
        """
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "name_of_shop": "Test name",
            "address": "Test address",
            "phone_number": "+996700000001",
            "link_to_map": "https://www.google.com/maps/place/42.874722,74.612222",
            "workdays": [
                {
                    "workday": 1,
                    "start_time": "10:00",
                    "end_time": "20:00",
                }
            ],
        }

        response = self.client.post("/branches/create/", data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name_of_shop"], "Test name")
        self.assertEqual(response.data["address"], "Test address")
        self.assertEqual(response.data["phone_number"], "+996700000001")
        self.assertEqual(response.data["link_to_map"], "https://www.google.com/maps/place/42.874722,74.612222")
        self.assertEqual(response.data["workdays"][0]["workday"], 1)
        self.assertEqual(response.data["workdays"][0]["start_time"], "10:00:00")
        self.assertEqual(response.data["workdays"][0]["end_time"], "20:00:00")

    def test_update_branch(self):
        """
        Test update branch.
        """
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "name_of_shop": "Test name 5",
            "address": "Test address 5",
            "phone_number": "+996700000001",
            "link_to_map": "https://www.ggoogle.com/maps/place/42.874722,74.612222",
            "workdays": [
                {
                    "workday": 1,
                    "start_time": "10:00",
                    "end_time": "20:00",
                }
            ],
        }

        response = self.client.put("/branches/update/1/", data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name_of_shop"], "Test name 5")
        self.assertEqual(response.data["address"], "Test address 5")
        self.assertEqual(response.data["phone_number"], "+996700000001")
        self.assertEqual(response.data["link_to_map"], "https://www.ggoogle.com/maps/place/42.874722,74.612222")
        self.assertEqual(response.data["workdays"][0]["workday"], 1)
        self.assertEqual(response.data["workdays"][0]["start_time"], "10:00:00")
        self.assertEqual(response.data["workdays"][0]["end_time"], "20:00:00")

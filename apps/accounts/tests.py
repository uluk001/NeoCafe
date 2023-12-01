"""
Module for testing accounts app.
"""
from apps.accounts.views import (
    WaiterLoginView
)
from django.test import TestCase
from apps.accounts.models import CustomUser as User
from apps.branches.models import Branch, Schedule


class TestLoginWaiterView(TestCase):
    """
    Test login waiter view
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            first_name="test",
            last_name="user",
            phone_number="+996700000000",
            username="testuser",
            password="testpassword",
            position="waiter",
            is_active=True,
        )
        cls.schedule = Schedule.objects.create(
            title="test schedule",
        )
        cls.branch = Branch.objects.create(
            schedule=cls.schedule,
            name_of_shop="A branch where there's nothing",
            address="Test Address",
            phone_number="+996700000000",
            link_to_map="https://test.link",
        )

    def test_login_waiter(self):
        """
        Test login waiter
        """
        response = self.client.post(
            "/accounts/login-waiter/",
            data={
                "username": "testuser",
                "password": "testpassword",
            },
        )
        print(response.data)
        self.assertEqual(response.status_code, 200)

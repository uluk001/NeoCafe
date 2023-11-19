from django.test import TestCase
from apps.accounts.models import CustomUser as User
from apps.storage.models import Category
from rest_framework import status
from rest_framework.test import APIClient


# ==================== Category Model Test ==================== #
class CategoryModelTest(TestCase):
    """ Test Category endpoints """

    @classmethod
    def setUpTestData(cls):
        # Common test data for all methods
        cls.user = User.objects.create(
            first_name='test',
            last_name='user',
            phone_number='+996700000000',
            username='testuser',
            password='testpassword',
            is_active=True,
        )
        cls.admin_user = User.objects.create(
            first_name='test',
            last_name='admin',
            phone_number='+996700000001',
            username='testadmin',
            password='testpassword',
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )
        cls.category = Category.objects.create(name='test category')

    def setUp(self):
        self.client = APIClient()

    def get_token(self, phone_number):
        response = self.client.post(
            path='/accounts/temporary-login/',
            data={'phone_number': phone_number},
        )
        return response.data['access']

    def test_user_category_creation(self):
        """ Test creating category by usual user """
        token = self.get_token('+996700000000')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.post(
            path='/admin-panel/categories/create/',
            data={'name': 'new category'},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Category.objects.count(), 1)

    def test_admin_category_creation(self):
        """ Test creating category by admin user """
        token = self.get_token('+996700000001')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.post(
            path='/admin-panel/categories/create/',
            data={'name': 'another category'},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)
        self.assertTrue(Category.objects.filter(name='another category').exists())


class CategoryViewTest(TestCase):
    """ Test Category endpoints """

    @classmethod
    def setUpTestData(cls):
        # Common test data for all methods
        cls.user = User.objects.create(
            first_name='test',
            last_name='user',
            phone_number='+996700000000',
            username='testuser',
            password='testpassword',
            is_active=True,
        )
        cls.admin_user = User.objects.create(
            first_name='test',
            last_name='admin',
            phone_number='+996700000001',
            username='testadmin',
            password='testpassword',
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )
        cls.category = Category.objects.create(name='test category')

    def setUp(self):
        self.client = APIClient()

    def get_token(self, phone_number):
        response = self.client.post(
            path='/accounts/temporary-login/',
            data={'phone_number': phone_number},
        )
        return response.data['access']

    def test_user_category_list(self):
        """ Test getting category list by usual user """
        token = self.get_token('+996700000000')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(path='/admin-panel/categories/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_category_list(self):
        """ Test getting category list by admin user """
        token = self.get_token('+996700000001')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(path='/admin-panel/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_user_category_update(self):
        """ Test updating category by usual user """
        token = self.get_token('+996700000000')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.put(
            path=f'/admin-panel/categories/update/{self.category.id}/',
            data={'name': 'new category'},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Category.objects.get(id=self.category.id).name, 'test category')

    def test_admin_category_update(self):
        """ Test updating category by admin user """
        token = self.get_token('+996700000001')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
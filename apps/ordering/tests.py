from django.test import TestCase
import json
from rest_framework.test import APIClient
from utils.menu import update_ingredient_stock_on_cooking
from apps.storage.models import (
    Ingredient, AvailableAtTheBranch,
    Composition, Item, Category,
)
from apps.branches.models import Branch, Schedule
from apps.ordering.models import Order, OrderItem
from apps.accounts.models import CustomUser


# ==============================================================================
# update_ingredient_stock_on_cooking test
# ==============================================================================
class UpdateIngredientStockOnCookingTest(TestCase):
    """
    Tests for update_ingredient_stock_on_cooking function.
    """
    def setUp(self):
        """
        Set up test dependencies.
        """
        self.schedeule = Schedule.objects.create(
            title="Test schedule",
            description="Test description"
        )
        self.branch = Branch.objects.create(
            schedule=self.schedeule,
            name_of_shop="Test shop",
            address="Test address",
            phone_number="+375291234567",
            link_to_map="https://www.google.com/"
        )
        self.ingredients = [
            Ingredient.objects.create(
                name="Milk",
                measurement_unit="ml"
            ),
            Ingredient.objects.create(
                name="Sugar",
                measurement_unit="g"
            ),
            Ingredient.objects.create(
                name="Espresso",
                measurement_unit="g"
            ),
        ]
        self.available_ingredients = [
            AvailableAtTheBranch.objects.create(
                branch=self.branch,
                ingredient=self.ingredients[0],
                quantity=1000
            ),
            AvailableAtTheBranch.objects.create(
                branch=self.branch,
                ingredient=self.ingredients[1],
                quantity=1000
            ),
            AvailableAtTheBranch.objects.create(
                branch=self.branch,
                ingredient=self.ingredients[2],
                quantity=1000
            ),
        ]
        self.category = Category.objects.create(
            name='Coffee'
        )
        self.item = Item.objects.create(
            name="Latte",
            category=self.category,
            description="Test description",
            price=2.00
        )
        self.compositions = [
            Composition.objects.create(
                item=self.item,
                ingredient=self.ingredients[0],
                quantity=200
            ),
            Composition.objects.create(
                item=self.item,
                ingredient=self.ingredients[1],
                quantity=50
            ),
            Composition.objects.create(
                item=self.item,
                ingredient=self.ingredients[2],
                quantity=100
            ),
        ]

    def test_setup(self):
        """
        Test setup.
        """
        self.assertEqual(len(self.ingredients), 3)
        self.assertEqual(len(self.available_ingredients), 3)
        self.assertEqual(len(self.compositions), 3)

    def test_update_ingredient_stock_on_cooking(self):
        """
        Test update_ingredient_stock_on_cooking function.
        """
        update_ingredient_stock_on_cooking(self.branch.id, self.item.id, 1)
        self.assertEqual(AvailableAtTheBranch.objects.get(id=self.available_ingredients[0].id).quantity, 800)
        self.assertEqual(AvailableAtTheBranch.objects.get(id=self.available_ingredients[1].id).quantity, 950)
        self.assertEqual(AvailableAtTheBranch.objects.get(id=self.available_ingredients[2].id).quantity, 900)
        update_ingredient_stock_on_cooking(self.branch.id, self.item.id, 2)
        self.assertEqual(AvailableAtTheBranch.objects.get(id=self.available_ingredients[0].id).quantity, 400)
        self.assertEqual(AvailableAtTheBranch.objects.get(id=self.available_ingredients[1].id).quantity, 850)
        self.assertEqual(AvailableAtTheBranch.objects.get(id=self.available_ingredients[2].id).quantity, 700)


# ==============================================================================
# CreateOrderView test
# ==============================================================================
class CreateOrderViewTest(TestCase):
    """
    Tests for CreateOrderView.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data.
        """
        cls.schedeule = Schedule.objects.create(
            title="Test schedule",
            description="Test description"
        )
        cls.branch1 = Branch.objects.create(
            schedule=cls.schedeule,
            name_of_shop="Branch",
            address="213 Kurmanzhana Datka St, Osh, Kyrgyzstan",
            phone_number="+996 509‒01‒09‒05",
            link_to_map="https://2gis.kg/osh/firm/70000001059486856"
        )
        cls.branch2 = Branch.objects.create(
            schedule=cls.schedeule,
            name_of_shop="Brio",
            address="211 Kurmanzhana Datka St, Osh, Kyrgyzstan",
            phone_number="+996 550‒83‒25‒95",
            link_to_map="https://2gis.kg/osh/firm/70000001030716336?m=72.794608%2C40.52689%2F18"
        )
        cls.user1 = CustomUser.objects.create(
            phone_number="+996555555555",
            first_name="Hasbik",
            last_name="Magomedov",
            branch=cls.branch2,
            username="has6ig",
            password="Hasbik123",
            is_active=True,
            is_staff=True,
            is_superuser=True,
            bonus=100,
        )
        cls.user2 = CustomUser.objects.create(
            phone_number="+996777777777",
            first_name="Abdu",
            last_name="Rozik",
            branch=cls.branch1,
            username="abdu",
            password="AbduGiga",
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )
        cls.ingredients = [
            Ingredient.objects.create(
                name="Milk",
                measurement_unit="ml"
            ),
            Ingredient.objects.create(
                name="Sugar",
                measurement_unit="g"
            ),
            Ingredient.objects.create(
                name="Espresso",
                measurement_unit="g"
            ),
        ]
        cls.available_ingredients = [
            AvailableAtTheBranch.objects.create(
                branch=cls.branch1,
                ingredient=cls.ingredients[0],
                quantity=1000
            ),
            AvailableAtTheBranch.objects.create(
                branch=cls.branch1,
                ingredient=cls.ingredients[1],
                quantity=1000
            ),
            AvailableAtTheBranch.objects.create(
                branch=cls.branch1,
                ingredient=cls.ingredients[2],
                quantity=1000
            ),
            AvailableAtTheBranch.objects.create(
                branch=cls.branch2,
                ingredient=cls.ingredients[0],
                quantity=200
            ),
            AvailableAtTheBranch.objects.create(
                branch=cls.branch2,
                ingredient=cls.ingredients[1],
                quantity=200
            ),
            AvailableAtTheBranch.objects.create(
                branch=cls.branch2,
                ingredient=cls.ingredients[2],
                quantity=200
            ),
        ]
        cls.category = Category.objects.create(
            name='Coffee'
        )
        cls.item1 = Item.objects.create(
            name="Latte",
            category=cls.category,
            description="Test description",
            price=2.00
        )
        cls.item2 = Item.objects.create(
            name="Espresso",
            category=cls.category,
            description="Test description",
            price=1.00
        )
        cls.compositions = [
            Composition.objects.create(
                item=cls.item1,
                ingredient=cls.ingredients[0],
                quantity=200
            ),
            Composition.objects.create(
                item=cls.item1,
                ingredient=cls.ingredients[1],
                quantity=50
            ),
            Composition.objects.create(
                item=cls.item1,
                ingredient=cls.ingredients[2],
                quantity=100
            ),
            Composition.objects.create(
                item=cls.item2,
                ingredient=cls.ingredients[0],
                quantity=100
            ),
            Composition.objects.create(
                item=cls.item2,
                ingredient=cls.ingredients[1],
                quantity=25
            ),
            Composition.objects.create(
                item=cls.item2,
                ingredient=cls.ingredients[2],
                quantity=50
            ),
        ]

    def setUp(self):
        """
        Set up test dependencies.
        """
        self.client = APIClient()

    def test_setup(self):
        """
        Test setup.
        """
        self.assertEqual(len(self.ingredients), 3)
        self.assertEqual(len(self.available_ingredients), 6)
        self.assertEqual(len(self.compositions), 6)

    def get_token(self, phone_number):
        response = self.client.post(
            path="/accounts/temporary-login/",
            data={"phone_number": phone_number},
        )
        return response.data["access"]

    def test_create_order(self):
        """
        Test create order.
        """
        abdus_token = self.get_token(self.user2.phone_number)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {abdus_token}")
        data = {
            "total_price": 4.00,
            "spent_bonus_points": 0,
            "items": [
                {
                    "item": self.item1.id,
                    "quantity": 1,
                },
                {
                    "item": self.item2.id,
                    "quantity": 2,
                }
            ],
        }
        response = self.client.post(
            path="/ordering/create-order/",
            data=json.dumps(data),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["total_price"], "4.00")
        self.assertEqual(response.data["spent_bonus_points"], 0)
        self.assertEqual(len(response.data["items"]), 2)
        self.assertEqual(response.data["items"][0]["item"], self.item1.id)
        self.assertEqual(OrderItem.objects.get(id=response.data["items"][0]["id"]).quantity, 1)
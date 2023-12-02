"""
Module for testing customers app.
"""
from django.test import TestCase

from apps.accounts.models import CustomUser as User
from apps.branches.models import Branch, Schedule
from apps.storage.models import (AvailableAtTheBranch, Category, Composition,
                                 Ingredient, Item, MinimalLimitReached)
from utils.menu import (get_available_ingredients_with_quantity,
                        get_items_that_can_be_made)


class TestMenu(TestCase):
    """
    Test menu functions
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            first_name="test",
            last_name="user",
            phone_number="+996700000000",
            username="testuser",
            password="testpassword",
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
        cls.branch2 = Branch.objects.create(
            schedule=cls.schedule,
            name_of_shop="A branch where there's everything",
            address="Test Address",
            phone_number="+996700000000",
            link_to_map="https://test.link",
        )
        cls.branch3 = Branch.objects.create(
            schedule=cls.schedule,
            name_of_shop="A branch where there's something",
            address="Test Address",
            phone_number="+996700000000",
            link_to_map="https://test.link",
        )
        cls.ingredient = Ingredient.objects.create(
            name="Test Ingredient", measurement_unit="g"
        )
        cls.ingredient2 = Ingredient.objects.create(
            name="Test Ingredient 2", measurement_unit="g"
        )
        cls.ingredient3 = Ingredient.objects.create(
            name="Test Ingredient 3", measurement_unit="g"
        )
        cls.minimal_limits = [
            MinimalLimitReached.objects.create(
                ingredient=cls.ingredient, branch=cls.branch, quantity=100
            ),
            MinimalLimitReached.objects.create(
                ingredient=cls.ingredient2, branch=cls.branch, quantity=100
            ),
            MinimalLimitReached.objects.create(
                ingredient=cls.ingredient3, branch=cls.branch, quantity=100
            ),
            MinimalLimitReached.objects.create(
                ingredient=cls.ingredient, branch=cls.branch2, quantity=100
            ),
            MinimalLimitReached.objects.create(
                ingredient=cls.ingredient2, branch=cls.branch2, quantity=100
            ),
            MinimalLimitReached.objects.create(
                ingredient=cls.ingredient3, branch=cls.branch2, quantity=100
            ),
            MinimalLimitReached.objects.create(
                ingredient=cls.ingredient, branch=cls.branch3, quantity=100
            ),
            MinimalLimitReached.objects.create(
                ingredient=cls.ingredient2, branch=cls.branch3, quantity=100
            ),
            MinimalLimitReached.objects.create(
                ingredient=cls.ingredient3, branch=cls.branch3, quantity=100
            ),
        ]
        cls.category = Category.objects.create(name="Test Category")
        cls.category2 = Category.objects.create(name="Test Category 2")
        cls.category3 = Category.objects.create(name="Test Category 3")
        cls.item = Item.objects.create(
            name="Test Item",
            category=cls.category,
            price=100,
            is_available=True,
        )
        cls.item2 = Item.objects.create(
            name="Test Item 2",
            category=cls.category2,
            price=100,
            is_available=True,
        )
        cls.item3 = Item.objects.create(
            name="Test Item 3",
            category=cls.category3,
            price=100,
            is_available=True,
        )
        cls.available_at_the_branch = [
            AvailableAtTheBranch.objects.create(
                ingredient=cls.ingredient, branch=cls.branch, quantity=100
            ),
            AvailableAtTheBranch.objects.create(
                ingredient=cls.ingredient2, branch=cls.branch, quantity=50
            ),
            AvailableAtTheBranch.objects.create(
                ingredient=cls.ingredient3, branch=cls.branch, quantity=0
            ),
            AvailableAtTheBranch.objects.create(
                ingredient=cls.ingredient, branch=cls.branch2, quantity=200
            ),
            AvailableAtTheBranch.objects.create(
                ingredient=cls.ingredient2, branch=cls.branch2, quantity=150
            ),
            AvailableAtTheBranch.objects.create(
                ingredient=cls.ingredient3, branch=cls.branch2, quantity=100
            ),
        ]
        cls.compositions = [
            Composition.objects.create(
                item=cls.item, ingredient=cls.ingredient, quantity=50
            ),
            Composition.objects.create(
                item=cls.item, ingredient=cls.ingredient2, quantity=25
            ),
            Composition.objects.create(
                item=cls.item2, ingredient=cls.ingredient, quantity=150
            ),
            Composition.objects.create(
                item=cls.item2, ingredient=cls.ingredient2, quantity=75
            ),
            Composition.objects.create(
                item=cls.item3, ingredient=cls.ingredient, quantity=300
            ),
            Composition.objects.create(
                item=cls.item3, ingredient=cls.ingredient2, quantity=150
            ),
        ]

    def test_get_available_ingredients_with_quantity(self):
        """
        Test that get_available_ingredients_with_quantity returns the correct ingredients.
        """
        ingredients = get_available_ingredients_with_quantity(self.branch.id)
        self.assertEqual(len(ingredients), 3)
        self.assertEqual(ingredients[0]["ingredient"], self.ingredient)
        self.assertEqual(ingredients[0]["quantity"], 100)
        self.assertEqual(ingredients[1]["ingredient"], self.ingredient2)
        self.assertEqual(ingredients[1]["quantity"], 50)
        self.assertEqual(ingredients[2]["ingredient"], self.ingredient3)
        self.assertEqual(ingredients[2]["quantity"], 0)

    def test_get_items_that_can_be_made(self):
        """
        Test that get_items_that_can_be_made returns the correct items.
        """
        items = get_items_that_can_be_made(self.branch.id)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0], self.item)

        items = get_items_that_can_be_made(self.branch2.id)
        self.assertEqual(len(items), 2)
        self.assertIn(self.item, items)
        self.assertIn(self.item2, items)
        self.assertNotIn(self.item3, items)

    def test_get_items_that_cannot_be_made(self):
        """
        Test that get_items_that_can_be_made does not return items that cannot be made.
        """
        items = get_items_that_can_be_made(self.branch.id)
        self.assertNotIn(self.item2, items)
        self.assertNotIn(self.item3, items)

        items = get_items_that_can_be_made(self.branch2.id)
        self.assertNotIn(self.item3, items)

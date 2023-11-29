from django.test import TestCase
from apps.branches.models import Branch, Schedule
from apps.storage.models import Item, Ingredient, Composition, AvailableAtTheBranch, Category
from utils.menu import get_items_that_can_be_made

class MenuTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Pizza")
        self.ingredients = [
            Ingredient.objects.create(name="Tomato", measurement_unit="g"),
            Ingredient.objects.create(name="Cheese", measurement_unit="g"),
            Ingredient.objects.create(name="Dough", measurement_unit="g"),
        ]
        self.schedule = Schedule.objects.create(title="NeoCafe Dzerzhinka")
        self.branch = Branch.objects.create(name_of_shop="NeoCafe Dzerzhinka", schedule=self.schedule)

        self.item = Item.objects.create(
            name="Pizza",
            category=self.category,
            price=10,
        )

        self.compositions = [
            Composition.objects.create(
                ingredient=self.ingredients[0], item=self.item, quantity=200
            ),
            Composition.objects.create(
                ingredient=self.ingredients[1], item=self.item, quantity=200
            ),
            Composition.objects.create(
                ingredient=self.ingredients[2], item=self.item, quantity=200
            ),
        ]

        self.available_at_the_branch = [
            AvailableAtTheBranch.objects.create(
                ingredient=self.ingredients[0],
                branch=self.branch,
                quantity=200,
            ),
            AvailableAtTheBranch.objects.create(
                ingredient=self.ingredients[1],
                branch=self.branch,
                quantity=200,
            ),
            AvailableAtTheBranch.objects.create(
                ingredient=self.ingredients[2],
                branch=self.branch,
                quantity=200,
            ),
        ]

    def test_get_items_that_can_be_made(self):
        items_that_can_be_made = get_items_that_can_be_made(self.branch.id)
        self.assertEqual(len(items_that_can_be_made), 1)
        self.assertEqual(items_that_can_be_made[0].name, "Pizza")

    def test_get_items_that_can_be_made_with_empty_ingredients(self):
        self.available_at_the_branch[0].quantity = 0
        self.available_at_the_branch[0].save()
        items_that_can_be_made = get_items_that_can_be_made(self.branch.id)
        self.assertEqual(len(items_that_can_be_made), 0)

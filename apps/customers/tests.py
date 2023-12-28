"""
Module for testing customers app.
"""
from django.test import TestCase

from apps.accounts.models import CustomUser as User
from apps.branches.models import Branch, Schedule
from apps.storage.models import (
    AvailableAtTheBranch,
    Category,
    Composition,
    Ingredient,
    Item,
    MinimalLimitReached,
    ReadyMadeProduct,
    ReadyMadeProductAvailableAtTheBranch,
)
from utils.menu import (
    get_available_items,
    get_available_ready_made_products,
)


class TestMenu(TestCase):
    """
    Test menu functions
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data.
        """
        cls.schedeule = Schedule.objects.create(
            title="Test schedule", description="Test description"
        )
        cls.branch1 = Branch.objects.create(
            schedule=cls.schedeule,
            name_of_shop="Branch",
            address="213 Kurmanzhana Datka St, Osh, Kyrgyzstan",
            phone_number="+996 509‒01‒09‒05",
            link_to_map="https://2gis.kg/osh/firm/70000001059486856",
        )
        cls.branch2 = Branch.objects.create(
            schedule=cls.schedeule,
            name_of_shop="Brio",
            address="211 Kurmanzhana Datka St, Osh, Kyrgyzstan",
            phone_number="+996 550‒83‒25‒95",
            link_to_map="https://2gis.kg/osh/firm/70000001030716336?m=72.794608%2C40.52689%2F18",
        )
        cls.branch3 = Branch.objects.create(
            schedule=cls.schedeule,
            name_of_shop="Istanbul",
            address="232 Kurmanzhana Datka St, Osh, Kyrgyzstan",
            phone_number="+996 555 83 25 95",
            link_to_map="https://2gis.kg/osh/firm/70000001030716336?m=72.794608%2C40.52689%2F18",
        )
        cls.category1 = Category.objects.create(
            name="Coffee",
        )
        cls.category2 = Category.objects.create(
            name="Tea",
        )
        cls.category3 = Category.objects.create(
            name="Juice",
        )
        cls.ingredients = [
            Ingredient.objects.create(name="Milk", measurement_unit="ml"),
            Ingredient.objects.create(name="Water", measurement_unit="ml"),
            Ingredient.objects.create(name="Sugar", measurement_unit="g"),
            Ingredient.objects.create(name="Coffee", measurement_unit="g"),
            Ingredient.objects.create(name="Tea", measurement_unit="g"),
            Ingredient.objects.create(name="Orange", measurement_unit="g"),
            Ingredient.objects.create(name="Apple", measurement_unit="g"),
            Ingredient.objects.create(name="Banana", measurement_unit="g"),
            Ingredient.objects.create(name="Pineapple", measurement_unit="g"),
        ]
        cls.item1 = Item.objects.create(
            name="Americano", description="Americano", category=cls.category1, price=50
        )
        cls.item2 = Item.objects.create(
            name="Latte", description="Latte", category=cls.category1, price=70
        )
        cls.item3 = Item.objects.create(
            name="Green tea", description="Green tea", category=cls.category2, price=60
        )
        cls.item4 = Item.objects.create(
            name="Black tea", description="Black tea", category=cls.category2, price=60
        )
        cls.item5 = Item.objects.create(
            name="Orange juice",
            description="Orange juice",
            category=cls.category3,
            price=80,
        )
        cls.item6 = Item.objects.create(
            name="Apple juice",
            description="Apple juice",
            category=cls.category3,
            price=80,
        )
        cls.item7 = Item.objects.create(
            name="Banana juice",
            description="Banana juice",
            category=cls.category3,
            price=80,
        )
        cls.item8 = Item.objects.create(
            name="Pineapple juice",
            description="Pineapple juice",
            category=cls.category3,
            price=80,
        )
        cls.compositions = [
            Composition.objects.create(
                item=cls.item1, ingredient=cls.ingredients[0], quantity=1
            ),
            Composition.objects.create(
                item=cls.item1, ingredient=cls.ingredients[1], quantity=1
            ),
            Composition.objects.create(
                item=cls.item1, ingredient=cls.ingredients[2], quantity=1
            ),
            Composition.objects.create(
                item=cls.item2, ingredient=cls.ingredients[0], quantity=1
            ),
            Composition.objects.create(
                item=cls.item2, ingredient=cls.ingredients[1], quantity=1
            ),
            Composition.objects.create(
                item=cls.item2, ingredient=cls.ingredients[2], quantity=1
            ),
            Composition.objects.create(
                item=cls.item3, ingredient=cls.ingredients[1], quantity=1
            ),
            Composition.objects.create(
                item=cls.item3, ingredient=cls.ingredients[2], quantity=1
            ),
            Composition.objects.create(
                item=cls.item4, ingredient=cls.ingredients[1], quantity=1
            ),
            Composition.objects.create(
                item=cls.item4, ingredient=cls.ingredients[2], quantity=1
            ),
            Composition.objects.create(
                item=cls.item5, ingredient=cls.ingredients[5], quantity=1
            ),
            Composition.objects.create(
                item=cls.item5, ingredient=cls.ingredients[2], quantity=1
            ),
            Composition.objects.create(
                item=cls.item6, ingredient=cls.ingredients[6], quantity=1
            ),
            Composition.objects.create(
                item=cls.item6, ingredient=cls.ingredients[2], quantity=1
            ),
            Composition.objects.create(
                item=cls.item7, ingredient=cls.ingredients[7], quantity=1
            ),
            Composition.objects.create(
                item=cls.item7, ingredient=cls.ingredients[2], quantity=1
            ),
            Composition.objects.create(
                item=cls.item8, ingredient=cls.ingredients[8], quantity=1
            ),
            Composition.objects.create(
                item=cls.item8, ingredient=cls.ingredients[2], quantity=1
            ),
        ]
        cls.available_at_the_branches = [
            AvailableAtTheBranch.objects.create(
                branch=cls.branch1, ingredient=cls.ingredients[0], quantity=100
            ),
            AvailableAtTheBranch.objects.create(
                branch=cls.branch1, ingredient=cls.ingredients[1], quantity=100
            ),
            AvailableAtTheBranch.objects.create(
                branch=cls.branch1, ingredient=cls.ingredients[2], quantity=100
            ),
            AvailableAtTheBranch.objects.create(
                branch=cls.branch1, ingredient=cls.ingredients[3], quantity=100
            ),
            AvailableAtTheBranch.objects.create(
                branch=cls.branch1, ingredient=cls.ingredients[4], quantity=100
            ),
            AvailableAtTheBranch.objects.create(
                branch=cls.branch1, ingredient=cls.ingredients[5], quantity=100
            ),
            AvailableAtTheBranch.objects.create(
                branch=cls.branch1, ingredient=cls.ingredients[6], quantity=100
            ),
            AvailableAtTheBranch.objects.create(
                branch=cls.branch1, ingredient=cls.ingredients[7], quantity=100
            ),
            AvailableAtTheBranch.objects.create(
                branch=cls.branch1, ingredient=cls.ingredients[8], quantity=100
            ),
            AvailableAtTheBranch.objects.create(
                branch=cls.branch2, ingredient=cls.ingredients[0], quantity=100
            ),
            AvailableAtTheBranch.objects.create(
                branch=cls.branch2, ingredient=cls.ingredients[1], quantity=100
            ),
            AvailableAtTheBranch.objects.create(
                branch=cls.branch2, ingredient=cls.ingredients[2], quantity=100
            ),
            AvailableAtTheBranch.objects.create(
                branch=cls.branch2, ingredient=cls.ingredients[3], quantity=100
            ),
            AvailableAtTheBranch.objects.create(
                branch=cls.branch2, ingredient=cls.ingredients[4], quantity=100
            ),
            AvailableAtTheBranch.objects.create(
                branch=cls.branch2, ingredient=cls.ingredients[5], quantity=100
            ),
            AvailableAtTheBranch.objects.create(
                branch=cls.branch2, ingredient=cls.ingredients[6], quantity=100
            ),
            AvailableAtTheBranch.objects.create(
                branch=cls.branch2, ingredient=cls.ingredients[7], quantity=100
            ),
            AvailableAtTheBranch.objects.create(
                branch=cls.branch2, ingredient=cls.ingredients[8], quantity=100
            ),
            # Branch 3
            AvailableAtTheBranch.objects.create(
                branch=cls.branch3, ingredient=cls.ingredients[5], quantity=100
            ),
            AvailableAtTheBranch.objects.create(
                branch=cls.branch3, ingredient=cls.ingredients[6], quantity=100
            ),
            AvailableAtTheBranch.objects.create(
                branch=cls.branch3, ingredient=cls.ingredients[7], quantity=100
            ),
            AvailableAtTheBranch.objects.create(
                branch=cls.branch3, ingredient=cls.ingredients[8], quantity=100
            ),
            AvailableAtTheBranch.objects.create(
                branch=cls.branch3, ingredient=cls.ingredients[2], quantity=100
            ),
        ]

    def test_setUpData(self):
        self.assertEqual(len(self.ingredients), 9)
        self.assertEqual(len(self.compositions), 18)
        self.assertEqual(len(self.available_at_the_branches), 23)
        self.assertEqual(len(Item.objects.all()), 8)

    def test_get_available_items_for_first_branch(self):
        branch_id = self.branch1.id
        items_that_can_be_made = get_available_items(branch_id)
        self.assertEqual(len(items_that_can_be_made), 8)
        item_ids = [item["id"] for item in items_that_can_be_made]
        self.assertIn(self.item1.id, item_ids)
        self.assertIn(self.item2.id, item_ids)
        self.assertIn(self.item3.id, item_ids)
        self.assertIn(self.item4.id, item_ids)
        self.assertIn(self.item5.id, item_ids)
        self.assertIn(self.item6.id, item_ids)
        self.assertIn(self.item7.id, item_ids)
        self.assertIn(self.item8.id, item_ids)

    def test_get_available_items_for_third_branch(self):
        branch_id = self.branch3.id
        items_that_can_be_made = get_available_items(branch_id)
        self.assertEqual(len(items_that_can_be_made), 4)


# Test for ready made products
class TestReadyMadeProducts(TestCase):
    """
    Test ready made products functions
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data.
        """
        cls.schedeule = Schedule.objects.create(
            title="Test schedule", description="Test description"
        )
        cls.branch1 = Branch.objects.create(
            schedule=cls.schedeule,
            name_of_shop="Branch",
            address="213 Kurmanzhana Datka St, Osh, Kyrgyzstan",
            phone_number="+996 509‒01‒09‒05",
            link_to_map="https://2gis.kg/osh/firm/70000001059486856",
        )
        cls.branch2 = Branch.objects.create(
            schedule=cls.schedeule,
            name_of_shop="Brio",
            address="211 Kurmanzhana Datka St, Osh, Kyrgyzstan",
            phone_number="+996 550‒83‒25‒95",
            link_to_map="https://2gis.kg/osh/firm/70000001030716336?m=72.794608%2C40.52689%2F18",
        )
        cls.branch3 = Branch.objects.create(
            schedule=cls.schedeule,
            name_of_shop="Istanbul",
            address="232 Kurmanzhana Datka St, Osh, Kyrgyzstan",
            phone_number="+996 555 83 25 95",
            link_to_map="https://2gis.kg/osh/firm/70000001030716336?m=72.794608%2C40.52689%2F18",
        )
        cls.category1 = Category.objects.create(
            name="Выпечка",
        )
        cls.category2 = Category.objects.create(
            name="Салаты",
        )
        cls.category3 = Category.objects.create(
            name="Напитки",
        )
        cls.ready_made_products = [
            ReadyMadeProduct.objects.create(
                name="Круассан",
                description="Круассан",
                category=cls.category1,
                price=50,
            ),
            ReadyMadeProduct.objects.create(
                name="Салат Цезарь",
                description="Салат Цезарь",
                category=cls.category2,
                price=70,
            ),
            ReadyMadeProduct.objects.create(
                name="Салат Греческий",
                description="Салат Греческий",
                category=cls.category2,
                price=60,
            ),
            ReadyMadeProduct.objects.create(
                name="Кока-кола",
                description="Кока-кола",
                category=cls.category3,
                price=80,
            ),
            ReadyMadeProduct.objects.create(
                name="Фанта", description="Фанта", category=cls.category3, price=80
            ),
        ]
        cls.availables = [
            # Branch 1
            ReadyMadeProductAvailableAtTheBranch.objects.create(
                branch=cls.branch1,
                ready_made_product=cls.ready_made_products[0],
                quantity=100,
            ),
            ReadyMadeProductAvailableAtTheBranch.objects.create(
                branch=cls.branch1,
                ready_made_product=cls.ready_made_products[1],
                quantity=100,
            ),
            ReadyMadeProductAvailableAtTheBranch.objects.create(
                branch=cls.branch1,
                ready_made_product=cls.ready_made_products[2],
                quantity=100,
            ),
            ReadyMadeProductAvailableAtTheBranch.objects.create(
                branch=cls.branch1,
                ready_made_product=cls.ready_made_products[3],
                quantity=100,
            ),
            ReadyMadeProductAvailableAtTheBranch.objects.create(
                branch=cls.branch1,
                ready_made_product=cls.ready_made_products[4],
                quantity=100,
            ),
            # Branch 2
            ReadyMadeProductAvailableAtTheBranch.objects.create(
                branch=cls.branch2,
                ready_made_product=cls.ready_made_products[0],
                quantity=100,
            ),
            ReadyMadeProductAvailableAtTheBranch.objects.create(
                branch=cls.branch2,
                ready_made_product=cls.ready_made_products[1],
                quantity=100,
            ),
            ReadyMadeProductAvailableAtTheBranch.objects.create(
                branch=cls.branch2,
                ready_made_product=cls.ready_made_products[2],
                quantity=100,
            ),
            ReadyMadeProductAvailableAtTheBranch.objects.create(
                branch=cls.branch2,
                ready_made_product=cls.ready_made_products[3],
                quantity=100,
            ),
            ReadyMadeProductAvailableAtTheBranch.objects.create(
                branch=cls.branch2,
                ready_made_product=cls.ready_made_products[4],
                quantity=100,
            ),
            # Branch 3
            ReadyMadeProductAvailableAtTheBranch.objects.create(
                branch=cls.branch3,
                ready_made_product=cls.ready_made_products[0],
                quantity=100,
            ),
            ReadyMadeProductAvailableAtTheBranch.objects.create(
                branch=cls.branch3,
                ready_made_product=cls.ready_made_products[1],
                quantity=100,
            ),
        ]

    def test_setUpData(self):
        self.assertEqual(len(self.ready_made_products), 5)
        self.assertEqual(len(self.availables), 12)
        self.assertEqual(len(ReadyMadeProduct.objects.all()), 5)

    def test_get_available_ready_made_products_for_first_branch(self):
        branch_id = self.branch1.id
        ready_made_products_that_can_be_made = get_available_ready_made_products(
            branch_id
        )
        self.assertEqual(len(ready_made_products_that_can_be_made), 5)
        self.assertIn(
            [
                product
                for product in ready_made_products_that_can_be_made
                if product["id"] == self.ready_made_products[0].id
            ][0],
            ready_made_products_that_can_be_made,
        )
        self.assertIn(
            [
                product
                for product in ready_made_products_that_can_be_made
                if product["id"] == self.ready_made_products[1].id
            ][0],
            ready_made_products_that_can_be_made,
        )
        self.assertIn(
            [
                product
                for product in ready_made_products_that_can_be_made
                if product["id"] == self.ready_made_products[2].id
            ][0],
            ready_made_products_that_can_be_made,
        )
        self.assertIn(
            [
                product
                for product in ready_made_products_that_can_be_made
                if product["id"] == self.ready_made_products[3].id
            ][0],
            ready_made_products_that_can_be_made,
        )
        self.assertIn(
            [
                product
                for product in ready_made_products_that_can_be_made
                if product["id"] == self.ready_made_products[4].id
            ][0],
            ready_made_products_that_can_be_made,
        )

    def test_get_available_ready_made_products_for_third_branch(self):
        branch_id = self.branch3.id
        ready_made_products_that_can_be_made = get_available_ready_made_products(
            branch_id
        )
        self.assertEqual(len(ready_made_products_that_can_be_made), 2)

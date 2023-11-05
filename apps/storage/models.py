from django.db import models
from apps.branches.models import Branch


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images')


class Ingredient(models.Model):
    MEASUREMENT_CHOICES = [
        ('g', 'gram'),
        ('ml', 'milliliter'),
        ('l', 'liter'),
        ('kg', 'kilogram'),
    ]

    name = models.CharField(max_length=100)
    measurement_unit = models.CharField(max_length=3, choices=MEASUREMENT_CHOICES, default='g')
    minimal_limit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Composition(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.item.name} - {self.ingredient.name} - {self.amount} {self.ingredient.measurement_unit}'


class ReadyMadeProduct(models.Model):
    image = models.ImageField(upload_to='images')
    minimal_limit = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class AvailableAtTheBranch(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.branch.address} - {self.ingredient.name} - {self.amount} {self.ingredient.measurement_unit}'


class ReadyMadeProductAvailableAtTheBranch(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    ready_made_product = models.ForeignKey(ReadyMadeProduct, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.branch.address} - {self.ready_made_product.name} - {self.amount} {self.ready_made_product.measurement_unit}'
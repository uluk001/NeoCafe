from django.contrib import admin
from apps.storage.models import Category, Item, Ingredient, Composition, ReadyMadeProduct, AvailableAtTheBranch, ReadyMadeProductAvailableAtTheBranch


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description', 'price', 'image')
    list_filter = ('category',)
    search_fields = ('name', 'description')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit', 'minimal_limit')
    list_filter = ('measurement_unit',)
    search_fields = ('name',)


class CompositionAdmin(admin.ModelAdmin):
    list_display = ('item', 'ingredient', 'quantity')
    list_filter = ('item', 'ingredient')
    search_fields = ('item__name', 'ingredient__name')


class ReadyMadeProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'image', 'minimal_limit')
    search_fields = ('name', 'description')


class AvailableAtTheBranchAdmin(admin.ModelAdmin):
    list_display = ('branch', 'ingredient', 'quantity')
    list_filter = ('branch', 'ingredient')
    search_fields = ('branch__address', 'ingredient__name')


class ReadyMadeProductAvailableAtTheBranchAdmin(admin.ModelAdmin):
    list_display = ('branch', 'ready_made_product', 'quantity')
    list_filter = ('branch', 'ready_made_product')
    search_fields = ('branch__address', 'ready_made_product__name')



admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Composition, CompositionAdmin)
admin.site.register(ReadyMadeProduct, ReadyMadeProductAdmin)
admin.site.register(AvailableAtTheBranch, AvailableAtTheBranchAdmin)
admin.site.register(ReadyMadeProductAvailableAtTheBranch, ReadyMadeProductAvailableAtTheBranchAdmin)

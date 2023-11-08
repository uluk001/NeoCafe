from apps.storage.views import CreateCategoryView, DestroyCategoryView, ListCategoryView, CreateItemView, DestroyItemView, CreateIngredientView, DestroyIngredientView, ListIngredientView
from django.urls import path


urlpatterns = [
    path('categories/', ListCategoryView.as_view()), # storage/categories/
    path('categories/create/', CreateCategoryView.as_view()), # storage/categories/create/
    path('categories/destroy/<int:pk>/', DestroyCategoryView.as_view()), # storage/categories/destroy/<int:pk>/
    path('items/create/', CreateItemView.as_view()), # storage/items/create/
    path('items/destroy/<int:pk>/', DestroyItemView.as_view()), # storage/items/destroy/<int:pk>/
    path('ingredients/', ListIngredientView.as_view()), # storage/ingredients/
    path('ingredients/create/', CreateIngredientView.as_view()), # storage/ingredients/create/
    path('ingredients/destroy/<int:pk>/', DestroyIngredientView.as_view()), # storage/ingredients/destroy/<int:pk>/
]
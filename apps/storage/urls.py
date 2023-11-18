from django.urls import path

from apps.storage.views import (AvailableAtTheBranchView, CreateCategoryView,
                                CreateEmployeeView, CreateIngredientView,
                                CreateItemView, DestroyCategoryView,
                                EmployeeDetailView, EmployeeListView,
                                EmployeeUpdateView, IngredientListView,
                                ItemDetailView, ItemListView, ItemUpdateView,
                                ListCategoryView, PutImageToItemView,
                                ReadyMadeProductCreateView,
                                ReadyMadeProductListView, ScheduleUpdateView,
                                UpdateAvailableAtTheBranchView)

urlpatterns = [
    path("categories/", ListCategoryView.as_view()),  # storage/categories/
    path(
        "categories/create/", CreateCategoryView.as_view()
    ),  # storage/categories/create/
    path(
        "categories/destroy/<int:pk>/", DestroyCategoryView.as_view()
    ),  # storage/categories/destroy/<int:pk>/
    path(
        "employees/create/", CreateEmployeeView.as_view()
    ),  # storage/employees/create/
    path("employees/", EmployeeListView.as_view()),  # storage/employees/
    path(
        "employees/<int:pk>/", EmployeeDetailView.as_view()
    ),  # storage/employees/<int:pk>/
    path(
        "employees/update/<int:pk>/", EmployeeUpdateView.as_view()
    ),  # storage/employees/update/<int:pk>/
    path(
        "employees/schedule/update/<int:pk>/", ScheduleUpdateView.as_view()
    ),  # storage/employees/schedule/update/<int:pk>/
    path(
        "ingredients/create/", CreateIngredientView.as_view()
    ),  # storage/ingredients/create/
    path("ingredients/", IngredientListView.as_view()),  # storage/ingredients/
    path("items/create/", CreateItemView.as_view()),  # storage/items/create/
    path("items/", ItemListView.as_view()),  # storage/items/
    path("items/<int:pk>/", ItemDetailView.as_view()),  # storage/items/<int:pk>/
    path(
        "items/update/<int:pk>/", ItemUpdateView.as_view()
    ),  # storage/items/update/<int:pk>/
    path(
        "ready-made-products/create/", ReadyMadeProductCreateView.as_view()
    ),  # storage/ready-made-products/create/
    path(
        "ready-made-products/", ReadyMadeProductListView.as_view()
    ),  # storage/ready-made-products/
    path(
        "ready-made-products/<int:pk>/", ReadyMadeProductListView.as_view()
    ),  # storage/ready-made-products/<int:pk>/
    path(
        "available-at-the-branch/", AvailableAtTheBranchView.as_view()
    ),  # storage/available-at-the-branch/
    path(
        "put-image-to-item/<int:pk>/", PutImageToItemView.as_view()
    ),  # storage/put-image-to-item/<int:pk>/
    path(
        "update-available-at-the-branch/<int:id>/",
        UpdateAvailableAtTheBranchView.as_view(),
    ),  # storage/update-available-at-the-branch/<int:pk>/
]

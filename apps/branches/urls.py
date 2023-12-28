from django.urls import path

from .views import (
    BranchCreateView,
    BranchDeleteView,
    BranchDetailView,
    BranchListView,
    BranchUpdateView,
    PutImageBranchView,
    BranchScheduleUpdateView,
)

urlpatterns = [
    path("", BranchListView.as_view()),  # /branches/
    path("create/", BranchCreateView.as_view()),  # /branches/create/
    path("update/<int:id>/", BranchUpdateView.as_view()),  # /branches/update/1/
    path("delete/<int:id>/", BranchDeleteView.as_view()),  # /branches/delete/1/
    path("image/<int:id>/", PutImageBranchView.as_view()),  # /branches/image/1/
    path("<int:id>/", BranchDetailView.as_view()),  # /branches/1/
    path(
        "schedule/update/<int:id>/", BranchScheduleUpdateView.as_view()
    ),  # /branches/schedule/update/1/
]

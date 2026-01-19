from django.urls import path

from colony_manager import views

app_name = "colony_manager"

urlpatterns = [
    path(
        "", views.colony_index, name="colony_index"
    ),  # this view shows the colonies and add colony option
    path("create/colony/", views.colony_creator, name="create_colony"),
    path("manage/<str:colony>/", views.colony_editor, name="manage_colony"),
    path(
        "<str:colony>/<str:planetoid>/", views.planetoid_index, name="planetoid_index"
    ),
    path(
        "<str:colony>/create/planetoid/",
        views.planetoid_creator,
        name="create_planetoid",
    ),
    path(
        "<str:colony>/manage/<str:planetoid>/",
        views.planetoid_editor,
        name="manage_planetoid",
    ),
]

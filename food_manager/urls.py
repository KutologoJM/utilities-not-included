from django.urls import path

from food_manager import views

app_name = "food_manager"

urlpatterns = [
    path("", views.recipe_display, name="index"),
    path("blueprint/", views.blueprint_display, name="blueprint_display"),
]

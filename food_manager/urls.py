from django.urls import path
from food_manager import views

app_name = 'food_manager'

urlpatterns = [
    # path('url/', views.view, name='url'), keep name the same as the url or a more readable version of it
    path('', views.Index.as_view(), name='index'),
    path('search-recipes/', views.search_recipes, name='search_recipes'),
    path('calculate_and_render_chosen_recipes/', views.calculate_and_render_chosen_recipes, name='calculate_and_render_chosen_recipes'),
    path('manage-chosen-recipes/', views.manage_chosen_recipes, name='manage_chosen_recipes'),


]

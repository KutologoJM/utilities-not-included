from django.urls import path

from food_manager import views
app_name = 'food_manager'

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search_recipes, name='search'),
]
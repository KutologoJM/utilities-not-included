from django.urls import path

from food_manager import views
app_name = 'food_manager'

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search_recipes, name='search'),

    path(
        'blueprint/',
        views.blueprint_display,
        name='blueprint_display'
    )

]
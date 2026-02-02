from django.urls import path
from colony_manager import views

app_name = 'colony_manager'

urlpatterns = [
    # path('url/', views.view, name='url'), keep name the same as the url or a more readable version of it
    path('', views.Index.as_view(), name='index'),
    path('create-colony/', views.create_colony, name='create-colony'),
    path("edit/<str:colony>/", views.edit_colony, name="edit-colony"),
    path("<str:colony>/planetoid/", views.planetoid_index, name="planetoid-index"),
    path("<str:colony>/create/planetoid/", views.create_planetoid, name="create-planetoid"),
    path(
        "<str:colony>/edit/<str:planetoid>/", views.edit_planetoid, name="edit-planetoid"),
    path("<str:colony>/<str:planetoid>/blueprint/", views.blueprint_index, name="blueprint-index"),
    path("<str:colony>/<str:planetoid>/blueprint/blueprint-maker/", views.blueprint_maker, name="blueprint-maker"),
    path('create-blueprint/', views.create_blueprint, name='create-blueprint'),
    path('blueprint-creation-success/', views.blueprint_creation_success, name='blueprint-creation-success'),

]

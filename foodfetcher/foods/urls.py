from django.urls import path
from . import views

urlpatterns = [
    path('', views.foods, name='foods'),
    path('veggies', views.veggies, name='veggies'),
    path('run', views.schedule_favorite_foods, name='get_favorites')
]
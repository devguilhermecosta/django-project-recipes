from django.urls import path
from recipes import views

app_name: str = 'recipes'

urlpatterns = [
    path('', views.home, name='home'),
    path('recipe/search/', views.search, name='search'),
    path('recipe/<int:id>/', views.recipe, name='recipe'),
    path('recipe/category/<int:id>/', views.category, name='category'),
]

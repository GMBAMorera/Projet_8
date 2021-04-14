from django.urls import path
from home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('home/<nomatch>', views.home, name='nomatch'),
    path('search', views.search, name='search'),
    path('select', views.select, name='select'),
    path('unselect', views.unselect, name='unselect'),
    path('aliment/<name>', views.aliment, name='aliment'),
    path('aliment/<name>/<nosubst>', views.aliment, name='nosubst'),
    path('favorites', views.favorites, name="favorites")
]
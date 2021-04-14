from django.urls import path
from login import views

urlpatterns = [
    path('account', views.account, name='account'),
    path('login', views.login_page, name='login'),
    path('inscription', views.inscription, name='inscription')
]
from Projet_8 import settings
from django.conf.urls.static import static
from django.urls import path
from home import views

urlpatterns = [
    path('', views.home, name='home'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
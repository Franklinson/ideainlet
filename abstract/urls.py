from django.urls import path
from . import views


urlpatterns = [
    path('', views.home),
    path('abstract', views.abstract),
    path('reviewer', views.reviewer),
    path('author', views.author),
]
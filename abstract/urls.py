from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('abstract', views.abstract, name='abstract'),
    path('reviewer', views.reviewer, name='reviewer'),
    path('author/<str:pk>/', views.author, name='author'),
]
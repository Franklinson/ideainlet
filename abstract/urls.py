from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('', views.home, name='home'),
    path('abstract/', views.abstract, name='abstract'),
    path('reviewer/', views.reviewer, name='reviewer'),
    path('editor/', views.editor, name='editor'),
    path('author/<str:pk>/', views.author, name='author'),
    path('user/', views.userPage, name='user'),
    path('account/', views.accountSettings, name="account"),

    path('create_abstract/<str:pk>/', views.createAbstract, name="create_abstract"),
    path('update_abstract/<str:pk>/', views.updateAbstract, name="update_abstract"),
    path('delete_abstract/<str:pk>/', views.deleteAbstract, name="delete_abstract"),
]
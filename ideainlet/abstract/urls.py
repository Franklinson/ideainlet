from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('contact/', views.contactUs, name="contact"),
    path('assign_abstract/', views.assign_abstract, name='assign_abstract'),
    # path('assign_editors/<int:abstract_id>/', views.assign_editors, name='assign_editors'),

    path('', views.home, name='home'),
    path('abstract/', views.abstract, name='abstract'),
    path('reviewer/', views.reviewer, name='reviewer'),
    path('editor/', views.editor_dashboard, name='editor'),
    path('author/<str:pk>/', views.author, name='author'),
    path('user/', views.userPage, name='user'),
    path('account/', views.accountSettings, name="account"),

    path('create_abstract/<str:pk>/', views.createAbstract, name="create_abstract"),
    path('update_abstract/<str:pk>/', views.updateAbstract, name="update_abstract"),
    path('delete_abstract/<str:pk>/', views.deleteAbstract, name="delete_abstract"),


    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="abstract/password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="abstract/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="abstract/password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="abstract/password_reset_done.html"), 
        name="password_reset_complete"),


    path('place-order/', views.place_order, name="place-order"),
    path('verify-payment/<str:ref>/', views.verify_payment, name="verify-payment"),

]
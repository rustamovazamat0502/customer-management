from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name="home"),
    path("user_page/", views.userPage, name="user_page"),
    path("account/", views.account_settings, name='account'),

    path("register/", views.user_register, name='register'),
    path("login/", views.user_login, name='login'),
    path("logout/", views.user_logout, name='logout'),
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
         name="password_reset"),
    path("password-reset-done/",
         auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"),
         name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/",
         auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"),
         name="password_reset_confirm"),
    path("password-reset-complete/",
         auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"),
         name="password_reset_complete"),

    path("products/", views.show_products, name='products'),
    path("customer/<int:pk>/", views.get_customer_data, name="customer"),
    path("create_order/<int:pk>/", views.createOrder, name='create_order'),
    path("update_order/<int:pk>/update", views.updateOrder, name='update_order'),
    path("delete_order/<int:pk>/", views.deleteOrder, name='delete_order')
]

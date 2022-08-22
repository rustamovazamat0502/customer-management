from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("user_page/", views.userPage, name="user_page"),
    path("register/", views.user_register, name='register'),
    path("login/", views.user_login, name='login'),
    path("logout/", views.user_logout, name='logout'),
    path("account/", views.account_settings, name='account'),

    path("products/", views.show_products, name='products'),
    path("customer/<int:pk>/", views.get_customer_data, name="customer"),
    path("create_order/<int:pk>/", views.createOrder, name='create_order'),
    path("update_order/<int:pk>/update", views.updateOrder, name='update_order'),
    path("delete_order/<int:pk>/", views.deleteOrder, name='delete_order')
]

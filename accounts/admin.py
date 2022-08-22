from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "phone", "email", "date_created")
    list_display_links = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("pk", "tag")
    list_display_links = ("tag",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "price", "category", 'description', "date_created")
    list_display_links = ("name",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("pk", "status", "date_created")
    list_display_links = ("status",)

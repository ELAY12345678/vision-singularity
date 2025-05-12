from django.contrib import admin
from .models import Restaurant, Table, ServiceCall

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display  = ("id", "name", "address", "phone", "created_at")
    list_filter   = ("created_at",)
    search_fields = ("name", "address")
    ordering      = ("-created_at",)

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("id", "restaurant", "number", "camera_id")
    search_fields = ("restaurant__name", "camera_id")
    list_filter = ("restaurant",)

@admin.register(ServiceCall)
class ServiceCallAdmin(admin.ModelAdmin):
    list_display = ("id", "table", "event_type", "created_at", "status")
    search_fields = ("table__restaurant__name", "event_type")
    list_filter = ("status", "created_at")



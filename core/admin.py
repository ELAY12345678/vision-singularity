from django.contrib import admin
from .models import Restaurant

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display  = ("id", "name", "address", "phone", "created_at")
    list_filter   = ("created_at",)          # right-side filter
    search_fields = ("name", "address")      # top search box
    ordering      = ("-created_at",)         # newest first


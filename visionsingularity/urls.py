from django.contrib import admin
from django.urls import path
from core.views import restaurant_list, restaurant_detail  # Clearly import new detail view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('restaurants/', restaurant_list),
    path('restaurants/<int:pk>/', restaurant_detail),  # Clearly handles single-item CRUD
]


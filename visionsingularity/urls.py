from django.contrib import admin
from django.urls import path
from core.views import restaurant_list  # Removed 'hello_world' clearly

urlpatterns = [
    path('admin/', admin.site.urls),
    path('restaurants/', restaurant_list),  # Clearly CRUD endpoint
]


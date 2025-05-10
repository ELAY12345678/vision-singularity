from django.contrib import admin
from django.urls import path
from core.views import RestaurantList, RestaurantDetail  # class-based views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('restaurants/', RestaurantList.as_view()),
    path('restaurants/<int:pk>/', RestaurantDetail.as_view()),
]


from django.contrib import admin
from django.urls import path
from core.views import RestaurantList, RestaurantDetail, TableList, ServiceCallListCreate

# ADD these two imports
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # ADD these two JWT endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # existing restaurant routes
    path('restaurants/', RestaurantList.as_view()),
    path('restaurants/<int:pk>/', RestaurantDetail.as_view()),
    path('tables/', TableList.as_view()),
    path('events/', ServiceCallListCreate.as_view()),
]




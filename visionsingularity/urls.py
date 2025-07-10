from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from core.views import RestaurantList, RestaurantDetail, TableList, ServiceCallListCreate, ServiceCallDetail, cv_ingest

# ADD these two imports
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('restaurants/', RestaurantList.as_view()),
    path('restaurants/<int:pk>/', RestaurantDetail.as_view()),
    path('tables/', TableList.as_view()),
    path('events/', ServiceCallListCreate.as_view()),
    path('events/<int:pk>/', ServiceCallDetail.as_view()),
    path("frames/", cv_ingest),
    
    # Frontend routes
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('dashboard/', TemplateView.as_view(template_name='index.html'), name='dashboard'),
    path('test/', TemplateView.as_view(template_name='test_direct.html'), name='test'),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




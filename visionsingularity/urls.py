from django.contrib import admin
from django.urls import path
from core.views import hello_world  # ← Import your new view here

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_world),    # ← Your first REST endpoint
]

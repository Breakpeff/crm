from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from crm import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('crm/', include('crm.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', lambda request: redirect('dashboard', permanent=False)),
    ]